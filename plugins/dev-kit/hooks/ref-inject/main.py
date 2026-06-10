"""dev-kit references auto-injection hook。

PreToolUse(Edit | Write | Read) で発火し、対象ファイルパスを references/ 配下の
各 .md のフロントマターと照合する。マッチした注入対象リファレンスの本文を
Claude Code フックの JSON 形式 (hookSpecificOutput) で注入する。

フロントマター仕様:
  ---
  paths:
    - **/*.py            # クォート有無どちらでも可
    - "**/foo.py"
  required: false        # 省略時 true。false なら paths にマッチしても注入しない
  tools: [e, w]          # 省略時 [Edit, Write]。e/w/r・edit/write/read・大小文字可
  ---

- paths: トリガーするファイルパターンの配列（glob）。クォート省略可。
- required: 注入するか否かの単一の真偽値（既定 true）。false ならマッチしても注入しない。
- tools: 発火するツール。省略時は [Edit, Write]（Read では発火しない）。

メタデータは同階層の cache.yaml にキャッシュする。cache.yaml があればそれを読み、
無ければ references/ を走査して生成する。references を更新したら cache.yaml を
削除すれば次回再生成される。

出力:
  - Edit / Write: permissionDecision="deny" + permissionDecisionReason に注入。
  - Read: permissionDecision="allow" + additionalContext に注入（Read はキャンセルしない）。
  いずれも exit 0 で返す（exit 2 だと stdout の JSON が無視されるため使わない）。

注入の重複はセッション単位の TTL トークン (~/.claude/tokens/dev-kit/{session_id}.yaml)
で防ぐ。一度注入したリファレンスは TTL 内は本文を省略しパスのみ出す。
TTL は既定 3600 秒、DEV_KIT_INJECTION_TTL(秒) で変更可。
DEV_KIT_INJECTION_DISABLE=true/1/yes/on で注入機構全体を停止する。

依存: PyYAML
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
FALSY = {"false", "0", "no", "off"}

# tools 省略時に発火するツール（Read を含めないので読み取りでは注入しない）
DEFAULT_TOOLS = ["Edit", "Write"]

# tools 指定の正規化テーブル（e/w/r・edit/write/read・大文字小文字を吸収）
TOOL_ALIASES = {
    "e": "Edit", "edit": "Edit",
    "w": "Write", "write": "Write",
    "r": "Read", "read": "Read",
}


def _eprint(msg: str) -> None:
    sys.stderr.write(f"[{LOG_TAG}] {msg}\n")


def _self_dir() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parent


def _refs_dir() -> pathlib.Path:
    return _self_dir() / "references"


def _cache_path() -> pathlib.Path:
    return _self_dir() / "cache.yaml"


def _ttl() -> int:
    raw = os.environ.get(f"{ENV_PREFIX}_INJECTION_TTL")
    if raw:
        try:
            return max(0, int(raw))
        except ValueError:
            _eprint(f"{ENV_PREFIX}_INJECTION_TTL={raw!r} が不正。既定 {DEFAULT_TTL} を使用。")
    return DEFAULT_TTL


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


def _unquote(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] in "\"'" and s[-1] == s[0]:
        return s[1:-1]
    return s


def _parse_inline_list(s: str) -> list[str]:
    s = s.strip()
    if s.startswith("["):
        s = s[1:]
    if s.endswith("]"):
        s = s[:-1]
    return [_unquote(x) for x in s.split(",") if x.strip()]


def _parse_frontmatter(content: str) -> dict | None:
    """先頭の --- フロントマターを行ベースで解析し paths/required/tools を返す。

    YAML safe_load は `- **/*.py` のようなクォートなし glob をエイリアス参照と
    解釈して壊すため、フロントマターは行単位で独自に解析する。
    """
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None

    paths: list[str] = []
    required = True
    tools: list[str] | None = None
    current_key: str | None = None

    for line in lines[1:end]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- "):
            val = _unquote(stripped[2:])
            if current_key == "paths":
                paths.append(val)
            elif current_key == "tools":
                tools = (tools or []) + [val]
            continue
        if ":" in stripped:
            key, _, rest = stripped.partition(":")
            key = key.strip().lower()
            rest = rest.strip()
            current_key = key
            if key == "paths":
                if rest.startswith("["):
                    paths.extend(_parse_inline_list(rest))
                    current_key = None
                elif rest:
                    # paths: "**/foo" のように 1 値をインラインで書いた形
                    paths.append(_unquote(rest))
                    current_key = None
            elif key == "required":
                required = _unquote(rest).lower() not in FALSY
                current_key = None
            elif key == "tools":
                if rest.startswith("["):
                    tools = _parse_inline_list(rest)
                    current_key = None
                elif rest:
                    tools = [rest]
                    current_key = None
            else:
                current_key = None

    if not paths:
        return None
    return {"paths": paths, "required": required, "tools": tools}


def _normalize_tools(raw: list[str] | None) -> list[str] | None:
    if not raw:
        return None
    out: list[str] = []
    for t in raw:
        norm = TOOL_ALIASES.get(str(t).strip().lower())
        if norm and norm not in out:
            out.append(norm)
    return out or None


def _scan_references() -> list[dict]:
    refs_dir = _refs_dir()
    entries: list[dict] = []
    for md in sorted(refs_dir.rglob("*.md")):
        try:
            content = md.read_text(encoding="utf-8")
        except Exception as e:
            _eprint(f"読み込みエラー ({md}): {e}")
            continue
        fm = _parse_frontmatter(content)
        if not fm:
            continue
        entries.append({
            "rel_path": str(md.relative_to(refs_dir)).replace("\\", "/"),
            "paths": fm["paths"],
            "required": fm["required"],
            "tools": _normalize_tools(fm["tools"]),
        })
    return entries


def _load_entries(yaml) -> list[dict]:
    cache_path = _cache_path()
    if cache_path.exists():
        try:
            data = yaml.safe_load(cache_path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return data
        except Exception as e:
            _eprint(f"cache 読み込みエラー: {e}")
    entries = _scan_references()
    try:
        cache_path.write_text(
            yaml.safe_dump(entries, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
    except Exception as e:
        _eprint(f"cache 書き込みエラー: {e}")
    return entries


def _load_token(path: pathlib.Path, yaml) -> dict:
    if not path.exists():
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as e:
        _eprint(f"トークンパースエラー ({path.name}): {e}")
        return {}
    return data if isinstance(data, dict) else {}


def _save_token(path: pathlib.Path, data: dict, yaml) -> None:
    try:
        path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=True), encoding="utf-8")
    except Exception as e:
        _eprint(f"トークン書き込みエラー ({path.name}): {e}")


def _cleanup_expired(token_dir: pathlib.Path, now: float, yaml) -> None:
    if not token_dir.exists():
        return
    for f in token_dir.glob("*.yaml"):
        data = _load_token(f, yaml)
        if not data:
            f.unlink(missing_ok=True)
            continue
        changed = False
        for key in list(data):
            if key != "references":
                del data[key]
                changed = True
                continue
            ns = data.get(key)
            if not isinstance(ns, dict):
                del data[key]
                changed = True
                continue
            for sub in list(ns):
                entry = ns.get(sub) or {}
                exp = entry.get("expires_at") if isinstance(entry, dict) else None
                if not isinstance(exp, (int, float)) or now >= exp:
                    del ns[sub]
                    changed = True
            if not ns:
                del data[key]
                changed = True
        if not data:
            f.unlink(missing_ok=True)
        elif changed:
            _save_token(f, data, yaml)


def _split_body(content: str) -> tuple[str, str]:
    body = content
    if content.startswith("---"):
        lines = content.splitlines(keepends=True)
        count = 0
        idx = 0
        for i, line in enumerate(lines):
            if line.strip() == "---":
                count += 1
                if count == 2:
                    idx = i + 1
                    break
        if count == 2:
            body = "".join(lines[idx:])
    description = ""
    for line in body.splitlines():
        if line.startswith("# "):
            description = line[2:].strip()
            break
    return body.lstrip("\n"), description


def main() -> int:
    if os.environ.get(f"{ENV_PREFIX}_INJECTION_DISABLE", "").lower() in TRUTHY:
        return 0

    try:
        import yaml
    except ImportError as e:
        _eprint(f"PyYAML が見つかりません: {e}。`uv add --dev pyyaml` でインストールしてください。")
        return 0

    try:
        data = json.loads(sys.stdin.read())
    except Exception as e:
        _eprint(f"stdin パースエラー: {e}")
        return 0

    tool_name = data.get("tool_name", "")
    if tool_name not in ("Edit", "Write", "Read"):
        return 0

    file_path: str = (data.get("tool_input") or {}).get("file_path", "") or ""
    if not file_path:
        return 0

    norm: list[str] = [file_path.replace("\\", "/")]
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    try:
        rel = pathlib.Path(file_path).resolve().relative_to(pathlib.Path(project_dir).resolve())
        norm.append(str(rel).replace("\\", "/"))
    except (ValueError, OSError):
        pass

    entries = _load_entries(yaml)

    matched: list[str] = []
    seen: set[str] = set()
    for entry in entries:
        if not entry.get("required", True):
            continue
        tools = entry.get("tools") or DEFAULT_TOOLS
        if tool_name not in tools:
            continue
        if any(_match_any(p, norm) for p in entry.get("paths", [])):
            rp = entry["rel_path"]
            if rp not in seen:
                seen.add(rp)
                matched.append(rp)

    if not matched:
        return 0

    session_id: str = data.get("session_id", "default")
    token_dir = pathlib.Path.home() / ".claude" / "tokens" / PLUGIN_NAME
    ttl = _ttl()
    now = time.time()
    _cleanup_expired(token_dir, now, yaml)

    token_path = token_dir / f"{session_id}.yaml"
    token_data = _load_token(token_path, yaml)
    ref_map = token_data.get("references")
    if not isinstance(ref_map, dict):
        ref_map = {}

    def _fresh(rp: str) -> bool:
        entry = ref_map.get(rp) or {}
        exp = entry.get("expires_at") if isinstance(entry, dict) else None
        return isinstance(exp, (int, float)) and now < exp

    to_inject = [rp for rp in matched if not _fresh(rp)]

    token_dir.mkdir(parents=True, exist_ok=True)
    expiry = int(now) + ttl
    for rp in to_inject:
        ref_map[rp] = {"expires_at": expiry}
    token_data["references"] = ref_map
    _save_token(token_path, token_data, yaml)

    refs_dir = _refs_dir()
    fresh_set = set(to_inject)
    blocks: list[str] = []
    for rp in matched:
        abs_path = (refs_dir / rp).as_posix()
        if rp in fresh_set:
            content = ""
            try:
                content = (refs_dir / rp).read_text(encoding="utf-8")
            except Exception as e:
                _eprint(f"リファレンス読み込みエラー ({rp}): {e}")
            body, desc = _split_body(content)
            header = f"## {rp}" + (f" — {desc}" if desc else "")
            blocks.append(f"{header}\n\n{body}")
        else:
            blocks.append(
                f"## {rp}\n\n_（本セッションで注入済み。必要なら `{abs_path}` を再 Read してください）_"
            )

    reason = (
        "# dev-kit リファレンス — 自動注入\n\n"
        f"`{file_path}` を編集するにあたり、以下の規約に従ってください。"
        "未注入のものは本文を展開し、注入済みのものはパスのみ記載します。\n\n"
        "---\n\n"
        + "\n\n---\n\n".join(blocks)
    )

    if tool_name == "Read":
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "additionalContext": reason,
            }
        }
    else:
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        }
    sys.stdout.buffer.write(json.dumps(output, ensure_ascii=False).encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
