# __PLUGIN_NAME__ references-edit-guard hook —
# 編集／作成されたファイルが当プラグインの references/ 配下の .md なら、
# 対応する _index.yaml / _index.jp.yaml / _injection_rules.yaml への登録漏れを
# リマインドするプロンプトを Claude に注入する。
#
# Trigger : PreToolUse(Edit | Write | MultiEdit) — 編集を実行する前に注入することで、
#           実際の編集前にユーザー／Claude が登録漏れを意識できるようにする。
# Scope   : このプラグインの references/ 配下のみ。他プラグインの編集には反応しない。
# Dedup   : セッションごとに 1 回だけ注入（_common.already_dispatched_this_session）。

from __future__ import annotations

import pathlib
import sys

from _common import already_dispatched_this_session, emit_block_reason, read_hook_input


def main() -> None:
    data = read_hook_input()
    file_path = (data.get("tool_input") or {}).get("file_path", "") or ""
    if not file_path:
        return

    # フックスクリプトは {plugin_root}/hooks/scripts/references_edit_guard.py に置かれる。
    plugin_root = pathlib.Path(__file__).resolve().parents[2]
    references_root = plugin_root / "references"

    # 編集対象がこのプラグインの references/ 配下でなければ無視。
    try:
        target = pathlib.Path(file_path).resolve()
        target.relative_to(references_root)
    except (ValueError, OSError):
        return

    # references 本文（.md）のみ対象。_index.yaml / _injection_rules.yaml 自体の編集には反応しない。
    if target.suffix != ".md":
        return
    # JP ミラーは EN 原本編集時に発火するため重複させない。
    if target.name.endswith(".jp.md"):
        return

    session_id = data.get("session_id", "default")
    tag = "__PLUGIN_NAME__-references-edit-guard"
    if already_dispatched_this_session(tag, session_id):
        return

    emit_block_reason(pathlib.Path(sys.argv[1]))


if __name__ == "__main__":
    main()
