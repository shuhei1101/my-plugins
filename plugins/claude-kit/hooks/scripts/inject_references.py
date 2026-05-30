"""claude-kit references auto-injection hook.

PreToolUse(Edit | Write | MultiEdit | Read) で発火し、対象ファイルパスを
references/_injection_rules.yaml の rules と照合する。マッチしたパターンの
required reference は **本文全量** を、optional reference は **パス + description のみ** を
Jinja2 で整形して `decision: block` の reason に注入する。

注入の重複は「パターン単位 + リファレンスファイル単位」の二層 TTL トークンで制御する:
    ~/.claude/tokens/claude-kit/{session_id}.yaml
は `patterns` と `references` の 2 つの名前空間を持つ YAML マップで、各エントリに
expires_at (epoch 秒) を持つ。expires_at は注入時に now + TTL で決まる。

  - patterns: そのパターンのリファレンス集合を再注入するかの判定。`now < expires_at` の間は
    そのパターンを丸ごとスキップする。
  - references: required リファレンスの **本文** を再注入するかの判定。あるリファレンスが
    別パターン経由で既にキャッシュ済み (`now < expires_at`) なら、required 欄には
    **パス + description のみ** を出し本文は流さない。未キャッシュなら本文全量を注入し
    キャッシュする。これにより複数パターンで共有される同一リファレンス本文の二重注入を防ぐ。

TTL はデフォルト 3600 秒、環境変数 CLAUDE_KIT_INJECTION_TTL (秒) で上書きできる
(patterns / references 共通)。フック発火のたびに全セッションのトークンを走査し、期限切れ
エントリ (now >= expires_at) を削除する (空になったファイルは削除)。期限切れ後に再びマッチ
すれば再注入される。

CLAUDE_KIT_INJECTION_DISABLE=true/1/yes/on で注入機構全体を停止できる (緊急停止用)。

description は references/_index.yaml (英語) から path -> description として取得する。
環境変数 CLAUDE_KIT_INJECTION_LANG=jp で _index.jp.yaml + injection.jp.md.j2 に切替。

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

PLUGIN_NAME = "claude-kit"
ENV_PREFIX = "CLAUDE_KIT"
LOG_TAG = "claude-kit-references-injection"
DEFAULT_TTL = 3600
TRUTHY = {"true", "1", "yes", "on"}


def _eprint(msg: str) -> None:
    """stderr に出力（フックの transcript に残り、Claude へは渡さない）。"""
    sys.stderr.write(f"[{LOG_TAG}] {msg}\n")


def _plugin_root() -> pathlib.Path:
    """plugin ルートを返す。

    Claude Code は hook 起動時に CLAUDE_PLUGIN_ROOT を設定するが、
    フォールバックとしてスクリプト位置の 3 階層上 (hooks/scripts/ の親の親) を使う。
    """
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
            _eprint(f"invalid {ENV_PREFIX}_INJECTION_TTL={raw!r}, using default {DEFAULT_TTL}")
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
        elif c in "[]":
            parts.append(c)
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
# トークン (patterns / references の 2 名前空間を持つセッション単位 YAML マップ)
#   { "patterns": {pattern: {expires_at}}, "references": {ref_path: {expires_at}} }
# --------------------------------------------------------------------------- #
TOKEN_NAMESPACES = ("patterns", "references")


def _load_token(path: pathlib.Path, yaml) -> dict[str, dict]:
    if not path.exists():
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as e:
        _eprint(f"token parse error ({path.name}): {e}")
        return {}
    return data if isinstance(data, dict) else {}


def _save_token(path: pathlib.Path, data: dict[str, dict], yaml) -> None:
    try:
        path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=True), encoding="utf-8")
    except Exception as e:
        _eprint(f"token write error ({path.name}): {e}")


def _cleanup_expired(token_dir: pathlib.Path, now: float, yaml) -> None:
    """全セッションのトークンを走査し、期限切れエントリ (now >= expires_at) を削除する。

    patterns / references の 2 名前空間それぞれについて掃除する。空になった名前空間は
    削除し、両方空になったファイルは削除する。未知のトップレベルキー (旧 schema の名残)
    も除去する。異常終了したセッションのトークンも期限切れ後にどこかでフックが発火した
    時点で自然に消える。
    """
    if not token_dir.exists():
        return
    for f in token_dir.glob("*.yaml"):
        data = _load_token(f, yaml)
        if not data:
            f.unlink(missing_ok=True)
            continue
        changed = False
        for key in list(data):
            if key not in TOKEN_NAMESPACES:
                del data[key]  # 旧 schema (pattern をトップレベルキーにした名残) を除去
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
    # ====== Master kill switch ======
    if os.environ.get(f"{ENV_PREFIX}_INJECTION_DISABLE", "").lower() in TRUTHY:
        return 0

    # 依存チェック (失敗時は静かに pass)
    try:
        import yaml
        from jinja2 import Environment, FileSystemLoader, StrictUndefined
    except ImportError as e:
        _eprint(f"missing dependency: {e}. install with: uv add --dev pyyaml jinja2")
        return 0

    try:
        data = json.loads(sys.stdin.read())
    except Exception as e:
        _eprint(f"stdin parse error: {e}")
        return 0

    tool_name = data.get("tool_name", "")
    if tool_name not in ("Edit", "Write", "MultiEdit", "Read"):
        return 0

    file_path: str = data.get("tool_input", {}).get("file_path", "") or ""
    if not file_path:
        return 0

    plugin_root = _plugin_root()
    refs_dir = plugin_root / "references"
    ref_injects_dir = refs_dir / ".ref-injects"

    # 言語選択: 環境変数 CLAUDE_KIT_INJECTION_LANG=jp で日本語版
    lang = os.environ.get(f"{ENV_PREFIX}_INJECTION_LANG", "en").lower()
    index_filename = "_index.jp.yaml" if lang == "jp" else "_index.yaml"
    template_filename = "injection.jp.md.j2" if lang == "jp" else "injection.md.j2"

    # JP ミラーモード: CLAUDE_KIT_JP_MIRROR=false で .jp.md 生成をスキップ
    jp_mirror_raw = os.environ.get(f"{ENV_PREFIX}_JP_MIRROR", "true").lower()
    jp_mirror = jp_mirror_raw not in ("false", "0", "no", "off")

    rules_yaml = ref_injects_dir / "_injection_rules.yaml"
    index_yaml = ref_injects_dir / index_filename
    if not rules_yaml.exists():
        _eprint(f"_injection_rules.yaml not found at {rules_yaml}")
        return 0
    if not index_yaml.exists():
        _eprint(f"{index_filename} not found at {index_yaml}")
        return 0

    # ----- _injection_rules.yaml をロード -----
    try:
        rules_doc = yaml.safe_load(rules_yaml.read_text(encoding="utf-8")) or {}
    except Exception as e:
        _eprint(f"_injection_rules.yaml parse error: {e}")
        return 0
    rules = rules_doc.get("rules") or []

    # ----- _index.yaml から path -> description -----
    descriptions: dict[str, str] = {}
    try:
        idx_doc = yaml.safe_load(index_yaml.read_text(encoding="utf-8")) or {}
        for ref in idx_doc.get("references") or []:
            p = ref.get("path")
            d = ref.get("description") or ""
            if p:
                descriptions[p] = d
    except Exception as e:
        _eprint(f"{index_filename} parse error: {e}")

    # ----- file_path の候補を作る (絶対パス + プロジェクトルートからの相対パス) -----
    norm: list[str] = [file_path.replace("\\", "/")]
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    try:
        rel = pathlib.Path(file_path).resolve().relative_to(pathlib.Path(project_dir).resolve())
        norm.append(str(rel).replace("\\", "/"))
    except (ValueError, OSError):
        pass

    def _dedup(xs: list[str]) -> list[str]:
        seen: set[str] = set()
        out: list[str] = []
        for x in xs:
            if x not in seen:
                seen.add(x)
                out.append(x)
        return out

    # ----- トークン: TTL 判定 + クリーンアップ -----
    session_id: str = data.get("session_id", "default")
    token_dir = pathlib.Path.home() / ".claude" / "tokens" / PLUGIN_NAME
    ttl = _ttl()
    now = time.time()
    _cleanup_expired(token_dir, now, yaml)

    token_path = token_dir / f"{session_id}.yaml"
    token_data = _load_token(token_path, yaml)
    pattern_map = token_data.get("patterns")
    if not isinstance(pattern_map, dict):
        pattern_map = {}
    ref_map = token_data.get("references")
    if not isinstance(ref_map, dict):
        ref_map = {}

    def _is_fresh(entry_map: dict, key: str) -> bool:
        entry = entry_map.get(key) or {}
        exp = entry.get("expires_at") if isinstance(entry, dict) else None
        return isinstance(exp, (int, float)) and now < exp

    # ----- injection_rules を照合し、未注入 or 期限切れパターンの reference を集める -----
    required: list[str] = []
    optional: list[str] = []
    patterns_to_mark: list[str] = []
    for rule in rules:
        pat = rule.get("pattern", "")
        if not pat or not _match_any(pat, norm):
            continue
        if _is_fresh(pattern_map, pat):
            continue  # パターンがまだ期限内 → そのパターンは丸ごとスキップ
        patterns_to_mark.append(pat)
        required.extend(rule.get("required") or [])
        optional.extend(rule.get("optional") or [])

    required = _dedup(required)
    optional = _dedup([p for p in optional if p not in set(required)])

    if not required and not optional:
        return 0  # マッチ無し、または全マッチパターンが TTL 内

    # ----- required をリファレンス単位キャッシュで「本文全量」と「パスのみ」に振り分け -----
    #   未キャッシュ (or 期限切れ) → 本文全量を注入し、このリファレンスをキャッシュ
    #   既にキャッシュ済み (期限内) → パス + description のみ (本文は流さない)
    refs_to_mark: list[str] = [p for p in required if not _is_fresh(ref_map, p)]

    # 注入するパターン / 本文注入するリファレンスの expires_at (= now + TTL) を保存
    token_dir.mkdir(parents=True, exist_ok=True)
    expiry = int(now) + ttl
    for pat in patterns_to_mark:
        pattern_map[pat] = {"expires_at": expiry}
    for p in refs_to_mark:
        ref_map[p] = {"expires_at": expiry}
    token_data["patterns"] = pattern_map
    token_data["references"] = ref_map
    _save_token(token_path, token_data, yaml)

    # ----- required = (未キャッシュ) 本文全量 / (キャッシュ済み) パスのみ / optional = パス + description -----
    # 注入テキスト内では ${CLAUDE_PLUGIN_ROOT} は展開されないため絶対パスを出す。
    fresh_refs = set(refs_to_mark)

    def _required_ref(rel_path: str) -> dict[str, str]:
        p = refs_dir / rel_path
        cached = rel_path not in fresh_refs  # このセッションで既に本文注入済み
        body = ""
        if not cached:
            try:
                body = p.read_text(encoding="utf-8")
            except Exception as e:
                _eprint(f"reference read error ({rel_path}): {e}")
        return {
            "path": rel_path,
            "abs_path": p.as_posix(),
            "description": descriptions.get(rel_path, ""),
            "body": body,
            "cached": cached,
        }

    def _optional_ref(rel_path: str) -> dict[str, str]:
        return {
            "path": rel_path,
            "abs_path": (refs_dir / rel_path).as_posix(),
            "description": descriptions.get(rel_path, ""),
        }

    required_data = [_required_ref(p) for p in required]
    optional_data = [_optional_ref(p) for p in optional]

    # ----- Jinja2 render -----
    tmpl_dir = plugin_root / "hooks" / "templates"
    env = Environment(
        loader=FileSystemLoader(str(tmpl_dir)),
        undefined=StrictUndefined,
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    try:
        tmpl = env.get_template(template_filename)
        reason = tmpl.render(
            file_path=file_path,
            required=required_data,
            optional=optional_data,
            jp_mirror=jp_mirror,
        )
    except Exception as e:
        _eprint(f"template render error ({template_filename}): {e}")
        lines = [f"# {PLUGIN_NAME} references (template error: {e})", "", f"target: {file_path}", ""]
        for r in required_data:
            lines.append(f"## {r['abs_path']} — {r['description']}")
            lines.append(r["body"])
        reason = "\n".join(lines)

    sys.stdout.buffer.write(
        json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False).encode("utf-8")
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
