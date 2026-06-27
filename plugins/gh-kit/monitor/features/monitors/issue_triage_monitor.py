"""issue-triage モニター: 確認ラベル付き Issue を 1 件ずつトリアージする。"""

from __future__ import annotations

from features.monitors._base import Monitor
from shared.labels import load_constants_sh

# このモニターが参照する確認/処理中ラベル定数を constants.sh から注入
load_constants_sh(globals())


class IssueTriageMonitor(Monitor):
    """issue-triage の固有設定だけを持つ具象モニター。"""

    @property
    def confirm_label(self) -> str:
        return GH_KIT_LABEL_CONFIRM_ISSUE_TRIAGE  # noqa: F821 — constants.sh から動的注入

    @property
    def processing_label(self) -> str:
        return GH_KIT_LABEL_PROCESSING_ISSUE_TRIAGE  # noqa: F821

    def skill_command(self, n: int) -> str:
        return f"/gh-kit:issue-triage {n}"

    @property
    def name(self) -> str:
        return "issue-triage"


# main.py から `issue_triage.poll()` で呼ばれるためのモジュールレベル束縛
poll = IssueTriageMonitor().poll
