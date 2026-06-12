"""PreToolUse フック: 対象ファイルにマッチするルール .md を Claude へ自動注入する。"""
from __future__ import annotations

import json
import os
import pathlib
import re
import sys

LOG_TAG      = "rules-injection"
TARGET_TOOLS = ("Edit", "Write", "Read")

RULES_DIR  = pathlib.Path(__file__).resolve().parent   # .md ルールファイルの置き場所
CACHE_PATH = RULES_DIR / "cache.json"                  # スキャン結果キャッシュ
TOKEN_DIR  = pathlib.Path.home() / ".claude" / "tokens" / "work" / "rules"  # セッショントークン保存先（プラグイン別）


def _eprint(msg: str) -> None:
    sys.stderr.write(f"[{LOG_TAG}] {msg}\n")


def _glob_to_regex(pattern: str) -> re.Pattern[str]:
    """glob パターンを正規表現にコンパイルする。** はディレクトリ区切りをまたぐ。

    例:
      "**/foo.py"  → "src/bar/foo.py", "foo.py" にマッチ
      "src/*.py"   → "src/main.py" にマッチ、"src/sub/main.py" には非マッチ
      "{a,b}.py"   → "a.py", "b.py" にマッチ
    """
    parts: list[str] = []
    i = 0
    while i < len(pattern):
        c = pattern[i]
        if c == "*" and i + 1 < len(pattern) and pattern[i + 1] == "*":
            parts.append(".*")          # ** = 区切りをまたぐ任意パス
            i += 2
            if i < len(pattern) and pattern[i] == "/":
                i += 1                  # **/ の / を読み飛ばす
        elif c == "*":
            parts.append("[^/]*")       # * = 区切り以外の任意文字列
            i += 1
        elif c == "?":
            parts.append("[^/]")        # ? = 区切り以外の任意1文字
            i += 1
        elif c == "[":
            parts.append(r"\[")
            i += 1
        elif c == "]":
            parts.append(r"\]")
            i += 1
        elif c == "{":
            parts.append("(?:")         # { → 非キャプチャグループ開始
            i += 1
        elif c == "}":
            parts.append(")")
            i += 1
        elif c == ",":
            parts.append("|")           # , → 選択（{a,b} の区切り）
            i += 1
        else:
            parts.append(re.escape(c))
            i += 1
    return re.compile("^" + "".join(parts) + "$")


def _match_any(pattern: str, candidates: list[str]) -> bool:
    """candidates のいずれかが pattern にマッチするか判定する。"""
    regex = _glob_to_regex(pattern)
    return any(regex.match(c) for c in candidates)


def _parse_frontmatter(content: str) -> dict | None:
    """先頭の --- フロントマターを行ベースで解析し paths を返す。

    paths の値はクォート必須。クォートなしのエントリは無視する。
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
    current_key: str | None = None

    for line in lines[1:end]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- "):
            if current_key == "paths":
                val = stripped[2:].strip()
                # クォートで囲まれた値のみ受け付ける
                if len(val) >= 2 and val[0] in "\"'" and val[-1] == val[0]:
                    paths.append(val[1:-1])
            continue
        if ":" in stripped:
            key, _, rest = stripped.partition(":")
            key = key.strip().lower()
            rest = rest.strip()
            current_key = key
            if key == "paths" and rest and not rest.startswith("["):
                # paths: "foo.py" 形式のインライン値
                if len(rest) >= 2 and rest[0] in "\"'" and rest[-1] == rest[0]:
                    paths.append(rest[1:-1])
                current_key = None
            elif key != "paths":
                current_key = None

    return {"paths": paths} if paths else None


def _scan_rules() -> list[dict]:
    """RULES_DIR 配下の .md を走査してフロントマターを解析し、エントリ一覧を返す。"""
    entries: list[dict] = []
    for md in sorted(RULES_DIR.rglob("*.md")):
        try:
            content = md.read_text(encoding="utf-8")
        except Exception as e:
            _eprint(f"読み込みエラー ({md}): {e}")
            continue
        frontmatter = _parse_frontmatter(content)
        if not frontmatter:
            continue
        entries.append({
            "rel_path": str(md.relative_to(RULES_DIR)).replace("\\", "/"),
            "paths": frontmatter["paths"],
        })
    return entries


def _load_entries() -> list[dict]:
    """キャッシュがあればそれを使い、なければ _scan_rules() で生成してキャッシュに書く。"""
    if CACHE_PATH.exists():
        try:
            data = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return data
        except Exception as e:
            _eprint(f"cache 読み込みエラー: {e}")
    entries = _scan_rules()
    try:
        CACHE_PATH.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        _eprint(f"cache 書き込みエラー: {e}")
    return entries


def _load_token(path: pathlib.Path) -> dict:
    """セッショントークンファイルを読み込む。存在しないか壊れていれば空 dict を返す。"""
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        _eprint(f"トークンパースエラー ({path.name}): {e}")
        return {}
    return data if isinstance(data, dict) else {}


def _save_token(path: pathlib.Path, data: dict) -> None:
    """セッショントークンをファイルに書き込む。"""
    try:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        _eprint(f"トークン書き込みエラー ({path.name}): {e}")



def _split_body(content: str) -> str:
    """フロントマターを除いた本文を返す。"""
    if not content.startswith("---"):
        return content.lstrip("\n")
    lines = content.splitlines(keepends=True)
    count = 0
    end_index = 0
    for i, line in enumerate(lines):
        if line.strip() == "---":
            count += 1
            if count == 2:
                end_index = i + 1
                break
    if count < 2:
        return content.lstrip("\n")
    return "".join(lines[end_index:]).lstrip("\n")


CHAR_LIMIT = 10_000


def _render_injection(blocks: list[dict], overflow: bool = False) -> str:
    """inject_message.j2 テンプレートをレンダリングして注入テキストを生成する。

    blocks の各要素: {"abs_path": str, "patterns": list[str], "body": str}
    overflow=True のとき、ファイルパスリストのみを出力するフォールバックモードになる。
    """
    try:
        from jinja2 import Environment, FileSystemLoader
    except ImportError as e:
        raise ImportError(
            f"jinja2 が見つかりません: {e}。`pip install jinja2` でインストールしてください。"
        ) from e
    env = Environment(
        loader=FileSystemLoader(str(RULES_DIR)),
        keep_trailing_newline=True,
        trim_blocks=True,    # {% %} タグ直後の改行を自動除去
        lstrip_blocks=True,  # {% %} タグ行の先頭空白を自動除去
    )
    tmpl = env.get_template("inject_message.j2")
    return tmpl.render(blocks=blocks, overflow=overflow)


def main() -> int:
    try:
        data = json.loads(sys.stdin.read())
    except Exception as e:
        _eprint(f"stdin パースエラー: {e}")
        return 0

    tool_name = data.get("tool_name", "")
    if tool_name not in TARGET_TOOLS:
        return 0

    file_path: str = (data.get("tool_input") or {}).get("file_path", "") or ""
    if not file_path:
        return 0

    # マッチング用に絶対パスと cwd 相対パスの両方を用意する
    norm: list[str] = [file_path.replace("\\", "/")]
    try:
        rel_path = pathlib.Path(file_path).resolve().relative_to(pathlib.Path(os.getcwd()).resolve())
        norm.append(str(rel_path).replace("\\", "/"))
    except (ValueError, OSError):
        pass

    entries = _load_entries()

    # マッチしたルールの rel_path を重複なし・順序保持で収集
    matched: list[str] = []
    seen: set[str] = set()
    for entry in entries:
        if any(_match_any(p, norm) for p in entry.get("paths", [])):
            rel_path = entry["rel_path"]
            if rel_path not in seen:
                seen.add(rel_path)
                matched.append(rel_path)

    if not matched:
        return 0

    session_id: str = data.get("session_id", "default")
    token_path = TOKEN_DIR / f"{session_id}.json"
    token_data = _load_token(token_path)

    # 注入済みルールのリスト（セッション中は有効期限なし）
    _rules = token_data.get("rules")
    injected_rules: list[str] = _rules if isinstance(_rules, list) else []

    # このセッションでまだ注入していないルールだけ抽出
    to_inject = [rel_path for rel_path in matched if rel_path not in injected_rules]

    # 新規注入がなければ何も出力しない（全ルールが注入済み）
    if not to_inject:
        return 0

    TOKEN_DIR.mkdir(parents=True, exist_ok=True)
    token_data["rules"] = list(set(injected_rules) | set(to_inject))  # 注入済みリストを更新
    _save_token(token_path, token_data)

    # rel_path → glob パターン一覧の引き当てマップ
    entry_paths_map = {entry["rel_path"]: entry.get("paths", []) for entry in entries}

    # 注入済みは渡さない。to_inject のみ本文展開してテンプレートへ渡す
    blocks: list[dict] = []
    for rel_path in to_inject:
        abs_path = (RULES_DIR / rel_path).as_posix()
        patterns = entry_paths_map.get(rel_path, [])
        rule_content = ""
        try:
            rule_content = (RULES_DIR / rel_path).read_text(encoding="utf-8")
        except Exception as e:
            _eprint(f"ルール読み込みエラー ({rel_path}): {e}")
        body = _split_body(rule_content)
        blocks.append({
            "abs_path": abs_path,   # 絶対パス（AI が参照用に使う）
            "patterns": [f"`{p}`" for p in patterns],  # glob パターン一覧（`...` でクォート）
            "body": body,           # フロントマターを除いた本文
        })

    reason = _render_injection(blocks)
    overflow = len(reason) > CHAR_LIMIT
    if overflow:
        reason = _render_injection(blocks, overflow=True)
    file_list = ", ".join(to_inject)

    overflow_notice = (
        f"⚠️ 注入するコンテキストが {CHAR_LIMIT:,} 文字を超えたため、ファイルパスのみを通知します。\n"
        if overflow else ""
    )
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "additionalContext": reason,
        },
        "systemMessage": "[rules-injection] " + overflow_notice + "\n" + "".join(f"  · {f}\n" for f in to_inject),
    }
    sys.stdout.buffer.write(json.dumps(output, ensure_ascii=False).encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
