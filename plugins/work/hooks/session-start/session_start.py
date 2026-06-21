"""SessionStart フック: work プラグインの概要を Jinja2 でレンダリングして注入する。

環境変数で各ガードの ON/OFF を切り替えると、表示される「やってはいけないこと」も
それに合わせて条件分岐される (`session_start.j2` 側で `{% if ... %}` 制御)。

Args:
    sys.argv[1]: 注入する Jinja2 テンプレートのパス (通常は session_start.j2)
"""
from __future__ import annotations

import json
import os
import pathlib
import sys


def _is_true(value: str | None, default: bool) -> bool:
    """env 値を真偽に解釈する。未設定時は default。"""
    if value is None:
        return default
    return value.strip().lower() not in {"false", "0", "no", "off"}


def _build_context() -> dict:
    """テンプレートに渡す変数と、デフォルトから外れている env 値の一覧を構築する。"""
    # 各フックが参照する env 名と既定値
    raw_protected = os.environ.get("WORK_PROTECTED_BRANCHES")
    protected_branches = (raw_protected or "master,main,develop").split(",")
    protected_branches_display = " / ".join(f"`{b.strip()}`" for b in protected_branches if b.strip())

    raw_allow_master = os.environ.get("WORK_ALLOW_MASTER_COMMIT")
    allow_master_commit = _is_true(raw_allow_master, default=False)

    raw_guard = os.environ.get("WORK_GUARD")
    guard_enabled = _is_true(raw_guard, default=True)

    raw_enforcement = os.environ.get("WORK_BRANCH_ENFORCEMENT")
    branch_enforcement = _is_true(raw_enforcement, default=True)

    # ユーザーが明示的に上書きしている env だけを表示する（情報過多を防ぐ）
    overrides: list[tuple[str, str]] = []
    for name, raw in (
        ("WORK_PROTECTED_BRANCHES", raw_protected),
        ("WORK_ALLOW_MASTER_COMMIT", raw_allow_master),
        ("WORK_GUARD", raw_guard),
        ("WORK_BRANCH_ENFORCEMENT", raw_enforcement),
    ):
        if raw is not None:
            overrides.append((name, raw))

    return {
        "protected_branches_display": protected_branches_display,
        "allow_master_commit": allow_master_commit,
        "guard_enabled": guard_enabled,
        "branch_enforcement": branch_enforcement,
        "env_overrides": overrides,
    }


def _render(template_path: pathlib.Path) -> str:
    """Jinja2 で session_start.j2 をレンダリングする。"""
    try:
        from jinja2 import Environment, FileSystemLoader
    except ImportError as e:
        # jinja2 がない環境ではテンプレートをそのまま返す（{% if %} がそのまま見えるが致命的でない）
        sys.stderr.write(f"warning: jinja2 が見つからないため未展開のまま注入します: {e}\n")
        return template_path.read_text("utf-8")

    env = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    tmpl = env.get_template(template_path.name)
    return tmpl.render(**_build_context())


def main() -> None:
    """セッション開始時にプラグイン概要を additionalContext として注入する。"""
    if len(sys.argv) < 2:
        return

    template_path = pathlib.Path(sys.argv[1])
    if not template_path.exists():
        return

    payload = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": _render(template_path),
        },
    }
    sys.stdout.buffer.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))


if __name__ == "__main__":
    main()
