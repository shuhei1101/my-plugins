"""dev-kit references auto-injection hook (Python / HTML / Next.js / Markdown を一本化)。

PreToolUse(Edit | Write | MultiEdit | Read) で発火し、対象ファイルパスを
references/ 配下の各 .md ファイルのフロントマターと照合する。

各リファレンスファイルのフロントマターに以下のキーを記述する:

  ---
  paths:
    - "**/*.py"                         # required: true (デフォルト)
    - pattern: "**/*.py"
      required: false                   # optional 扱い
  tools: [Edit, Write, Read]            # 省略時は全ツール対象
  ---

マッチした required リファレンスは **本文全量** を、optional リファレンスは
**パス + description のみ** を Jinja2 で整形して `decision: block` の reason に注入する。

注入の重複はリファレンスファイル単位の TTL トークンで制御する:
    ~/.claude/tokens/dev-kit/{session_id}.yaml
は `references` 名前空間を持つ YAML マップで、各エントリに expires_at (epoch 秒) を持つ。
required リファレンスが注入済み (now < expires_at) なら本文を省略しパスのみ出す。

TTL はデフォルト 3600 秒、環境変数 DEV_KIT_INJECTION_TTL (秒) で上書きできる。
DEV_KIT_INJECTION_DISABLE=true/1/yes/on で注入機構全体を停止できる (緊急停止用)。

依存:
    - PyYAML  (uv/pip install pyyaml)
    - Jinja2  (uv/pip install jinja2)
"""
from __future__ import annotations

import json
import os
import pathlib
import re
import sys
import time

PLUGIN_NAME = "dev-kit"
ENV_PREFIX = "DEV_KIT"
LOG_TAG = "dev-kit-references-injection"
DEFAULT_TTL = 3600
TRUTHY = {"true", "1", "yes", "on"}


def _eprint(msg: str) -> None:
    sys.stderr.write(f"[{LOG_TAG}] {msg}\n")


def _plugin_root() -> pathlib.Path:
    env = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if env:
        return pathlib.Path(env)
    return pathlib.Path(__file__).resolve().parents[2]


def _ttl() -> int:
    raw = os.environ.get(f"{ENV_PREFIX}_INJECTION_TTL")
    if raw:
        try:
            return max(0, int(raw))
        except ValueError:
            _eprint(f"{ENV_PREFIX}_INJECTION_TTL={raw!r} が不正な値です。デフォルト {DEFAULT_TTL} を使用します。")
    return DEFAULT_TTL


# --------------------------------------------------------------------------- #
# glob -> regex  (** = 任意階層、* = 単一階層内、? = 1 文字)
# --------------------------------------------------------------------------- #
def _glob_to_regex(pattern: str) -> re.Pattern[str]:
    parts: list[str] = []
    i = 0
    while i < len(pattern):
        c = pattern[i]
        if c == "*" and i + 1 < len(pattern) and pattern[i + 1] == "*":
            parts.append(".*")
            i += 2
            if i < len(pattern) and pattern[i] == "/":
                i += 1
        elif c == "*":
            parts.append("[^/]*")
            i += 1
        elif c == "?":
            parts.append("[^/]")
            i += 1
        elif c == "[":
            # Next.js の [id] 等のルートパラメータをリテラルとして扱う
            parts.append(r"\[")
            i += 1
        elif c == "]":
            parts.append(r"\]")
            i += 1
        elif c == "{":
            parts.append("(?:")
            i += 1
        elif c == "}":
            parts.append(")")
            i += 1
        elif c == ",":
            parts.append("|")
            i += 1
        else:
            parts.append(re.escape(c))
            i += 1
    return re.compile("^" + "".join(parts) + "$")


def _match_any(pattern: str, candidates: list[str]) -> bool:
    rx = _glob_to_regex(pattern)
    return any(rx.match(c) for c in candidates)


# --------------------------------------------------------------------------- #
# フロントマター解析
# --------------------------------------------------------------------------- #
def _extract_description(content: str) -> str:
    """フロントマター後の本文から最初の # 見出し行をdescriptionとして取得する。"""
    for line in content.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def _parse_frontmatter(content: str) -> dict | None:
    """ファイル先頭の --- フロントマターを parse して dict で返す。なければ None。"""
    if not content.startswith("---\n"):
        return None
    end = content.find("\n---\n", 4)
    if end == -1:
        return None
    fm_text = content[4:end]
    try:
        import yaml
        fm = yaml.safe_load(fm_text)
        return fm if isinstance(fm, dict) else None
    except Exception:
        return None


def _load_ref_entries(refs_dir: pathlib.Path, yaml) -> list[dict]:
    """references/ 配下の全 .md のフロントマターを読み込む。

    各エントリ:
      {
        "rel_path": str,
        "patterns": [(pattern_str, required_bool), ...],
        "tools": list[str] | None,   # None = 全ツール対象
      }
    """
    result = []
    for md_file in sorted(refs_dir.rglob("*.md")):
        # .ref-inject/ は廃止フォルダのためスキップ
        if ".ref-inject" in str(md_file):
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception as e:
            _eprint(f"ファイル読み込みエラー ({md_file}): {e}")
            continue
        fm = _parse_frontmatter(content)
        if fm is None:
            continue
        raw_paths = fm.get("paths")
        if not raw_paths:
            continue
        patterns: list[tuple[str, bool]] = []
        for p in raw_paths:
            if isinstance(p, str):
                patterns.append((p, True))
            elif isinstance(p, dict):
                pat = p.get("pattern", "")
                req = p.get("required", True)
                if pat:
                    patterns.append((pat, bool(req)))
        if not patterns:
            continue
        raw_tools = fm.get("tools")
        tools = [str(t) for t in raw_tools] if raw_tools else None
        rel_path = str(md_file.relative_to(refs_dir)).replace("\\", "/")
        result.append({
            "rel_path": rel_path,
            "patterns": patterns,
            "tools": tools,
        })
    return result


# --------------------------------------------------------------------------- #
# TTL トークン（references 名前空間）
# --------------------------------------------------------------------------- #
TOKEN_NAMESPACE = "references"


def _load_token(path: pathlib.Path, yaml) -> dict[str, dict]:
    if not path.exists():
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as e:
        _eprint(f"トークンパースエラー ({path.name}): {e}")
        return {}
    return data if isinstance(data, dict) else {}


def _save_token(path: pathlib.Path, data: dict[str, dict], yaml) -> None:
    try:
        path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=True), encoding="utf-8")
    except Exception as e:
        _eprint(f"トークン書き込みエラー ({path.name}): {e}")


def _cleanup_expired(token_dir: pathlib.Path, now: float, yaml) -> None:
    """全セッションのトークンを走査し、期限切れエントリ (now >= expires_at) を削除する。"""
    if not token_dir.exists():
        return
    for f in token_dir.glob("*.yaml"):
        data = _load_token(f, yaml)
        if not data:
            f.unlink(missing_ok=True)
            continue
        changed = False
        # references 名前空間以外の古いキーを削除
        for key in list(data):
            if key != TOKEN_NAMESPACE:
                del data[key]
                changed = True
                continue
            ns = data.get(key)
            if not isinstance(ns, dict):
                del data[key]
                changed = True
                continue
            for sub_key in list(ns):
                entry = ns.get(sub_key) or {}
                exp = entry.get("expires_at") if isinstance(entry, dict) else None
                if not isinstance(exp, (int, float)) or now >= exp:
                    del ns[sub_key]
                    changed = True
            if not ns:
                del data[key]
                changed = True
        if not data:
            f.unlink(missing_ok=True)
        elif changed:
            _save_token(f, data, yaml)


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main() -> int:
    # 強制停止スイッチ
    if os.environ.get(f"{ENV_PREFIX}_INJECTION_DISABLE", "").lower() in TRUTHY:
        return 0

    # 依存チェック (失敗時は静かに pass)
    try:
        import yaml
        from jinja2 import Environment, FileSystemLoader, StrictUndefined
    except ImportError as e:
        _eprint(f"依存ライブラリが見つかりません: {e}。`uv add --dev pyyaml jinja2` でインストールしてください。")
        return 0

    try:
        data = json.loads(sys.stdin.read())
    except Exception as e:
        _eprint(f"stdin パースエラー: {e}")
        return 0

    tool_name = data.get("tool_name", "")
    if tool_name not in ("Edit", "Write", "MultiEdit", "Read"):
        return 0

    file_path: str = data.get("tool_input", {}).get("file_path", "") or ""
    if not file_path:
        return 0

    plugin_root = _plugin_root()
    refs_dir = plugin_root / "references"

    # 対象ファイルパスを正規化（絶対パスと相対パスの両形式で照合）
    norm: list[str] = [file_path.replace("\\", "/")]
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    try:
        rel = pathlib.Path(file_path).resolve().relative_to(pathlib.Path(project_dir).resolve())
        norm.append(str(rel).replace("\\", "/"))
    except (ValueError, OSError):
        pass

    # 全リファレンスファイルのフロントマターを走査
    ref_entries = _load_ref_entries(refs_dir, yaml)

    def _dedup(xs: list[str]) -> list[str]:
        seen: set[str] = set()
        out: list[str] = []
        for x in xs:
            if x not in seen:
                seen.add(x)
                out.append(x)
        return out

    session_id: str = data.get("session_id", "default")
    token_dir = pathlib.Path.home() / ".claude" / "tokens" / PLUGIN_NAME
    ttl = _ttl()
    now = time.time()
    _cleanup_expired(token_dir, now, yaml)

    token_path = token_dir / f"{session_id}.yaml"
    token_data = _load_token(token_path, yaml)
    ref_map = token_data.get(TOKEN_NAMESPACE)
    if not isinstance(ref_map, dict):
        ref_map = {}

    def _is_fresh(key: str) -> bool:
        entry = ref_map.get(key) or {}
        exp = entry.get("expires_at") if isinstance(entry, dict) else None
        return isinstance(exp, (int, float)) and now < exp

    required: list[str] = []
    optional: list[str] = []

    for entry in ref_entries:
        # tools フィルタ: このリファレンスが現在のツール呼び出しで発火すべきか判定
        if entry["tools"] is not None and tool_name not in entry["tools"]:
            continue

        rel_path = entry["rel_path"]
        # このリファレンスのパターンのいずれかが対象ファイルにマッチするか確認
        matched_required = False
        matched_optional = False
        for pattern, is_required in entry["patterns"]:
            if _match_any(pattern, norm):
                if is_required:
                    matched_required = True
                else:
                    matched_optional = True

        if matched_required:
            required.append(rel_path)
        elif matched_optional:
            optional.append(rel_path)

    required = _dedup(required)
    optional = _dedup([p for p in optional if p not in set(required)])

    if not required and not optional:
        return 0

    # TTL 未満の required は本文をスキップ（キャッシュ済み扱い）
    refs_to_mark: list[str] = [p for p in required if not _is_fresh(p)]

    token_dir.mkdir(parents=True, exist_ok=True)
    expiry = int(now) + ttl
    for p in refs_to_mark:
        ref_map[p] = {"expires_at": expiry}
    token_data[TOKEN_NAMESPACE] = ref_map
    _save_token(token_path, token_data, yaml)

    fresh_refs = set(refs_to_mark)

    def _required_ref(rel_path: str) -> dict[str, str]:
        p = refs_dir / rel_path
        cached = rel_path not in fresh_refs
        body = ""
        description = ""
        if not cached:
            try:
                content = p.read_text(encoding="utf-8")
                description = _extract_description(content)
                # フロントマターを除いた本文を body に
                if content.startswith("---\n"):
                    end = content.find("\n---\n", 4)
                    if end != -1:
                        body = content[end + 5:]
                    else:
                        body = content
                else:
                    body = content
            except Exception as e:
                _eprint(f"リファレンス読み込みエラー ({rel_path}): {e}")
        return {
            "path": rel_path,
            "abs_path": p.as_posix(),
            "description": description,
            "body": body,
            "cached": cached,
        }

    def _optional_ref(rel_path: str) -> dict[str, str]:
        p = refs_dir / rel_path
        description = ""
        try:
            content = p.read_text(encoding="utf-8")
            description = _extract_description(content)
        except Exception:
            pass
        return {
            "path": rel_path,
            "abs_path": p.as_posix(),
            "description": description,
        }

    required_data = [_required_ref(p) for p in required]
    optional_data = [_optional_ref(p) for p in optional]

    tmpl_dir = plugin_root / "hooks" / "templates"
    jinja_env = Environment(
        loader=FileSystemLoader(str(tmpl_dir)),
        undefined=StrictUndefined,
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template_filename = "injection.md.j2"
    try:
        tmpl = jinja_env.get_template(template_filename)
        reason = tmpl.render(
            file_path=file_path,
            required=required_data,
            optional=optional_data,
        )
    except Exception as e:
        _eprint(f"テンプレートレンダリングエラー ({template_filename}): {e}")
        lines = [f"# {PLUGIN_NAME} references (template error: {e})", "", f"target: {file_path}", ""]
        for r in required_data:
            lines.append(f"## {r['abs_path']} — {r['description']}")
            lines.append(r["body"])
        reason = "\n".join(lines)

    if tool_name == "Read":
        # Read はキャンセルせずコンテキストだけ注入する
        sys.stdout.buffer.write(
            json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "allow",
                    "additionalContext": reason,
                }
            }, ensure_ascii=False).encode("utf-8")
        )
    else:
        sys.stdout.buffer.write(
            json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False).encode("utf-8")
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
