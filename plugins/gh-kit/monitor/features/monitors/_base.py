"""モニター共通の Template Method 抽象基底。

各モニター（issue-triage / issue-spec / pr-plan / ...）は ``Monitor`` を継承し、
**3 つのメンバー**（プロパティ ``confirm_label`` / ``processing_label`` とメソッド ``skill_command``）
を実装するだけで、以下の共通処理が自動で動く:

1. 確認ラベル付き Issue/PR を gh から一覧取得
2. 処理中ラベルが付いているものを候補から除外
3. 優先度ラベルでソート（急ぎ → 通常 → いつでも → 同ランクは番号昇順）
4. 各候補に対し: 処理中ラベル付与 → claude -p 起動 → 処理中ラベル除去
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import settings
from integrations.claude.runner import run_claude_prompt
from integrations.github import client as github
from shared.labels import has_label_prefix, load_constants_sh, priority_rank
from shared.logger import logger

# 本ベース内で参照する共通ラベル（処理中プレフィックス・優先度ラベル）を constants.sh から注入
load_constants_sh(globals())


class Monitor(ABC):
    """1 モニター = 確認ラベル付き対象を 1 件ずつ AI に渡すループの抽象基底。"""

    # ---------- サブクラスが実装する 3 つ ----------

    @property
    @abstractmethod
    def confirm_label(self) -> str:
        """このモニターが監視する確認ラベル名（constants.sh の値を返す）。"""
        ...

    @property
    @abstractmethod
    def processing_label(self) -> str:
        """処理中マークとして付与するラベル名（constants.sh の値を返す）。"""
        ...

    @abstractmethod
    def skill_command(self, n: int) -> str:
        """claude -p に渡すスキル起動文字列を組み立てて返す。

        例: ``f"/gh-kit:issue-triage {n}"``
        """
        ...

    # ---------- 表示名（任意でサブクラス上書き）----------

    @property
    def name(self) -> str:
        """ログ表示用の短縮名。サブクラスで上書き可。"""
        return self.__class__.__name__

    # ---------- 公開 API（main.py から呼ばれる）----------

    def poll(self) -> None:
        """1 回のポーリングのエントリーポイント。"""
        numbers = self._find_next_targets()
        if not numbers:
            logger.info(f"[{self.name}] 対象なし — {settings.POLL_INTERVAL}s 待機")
            return
        # 候補が複数あるなら優先度順に 1 件ずつ処理
        for n in numbers:
            self._process_one(n)

    # ---------- 内部ヘルパー（サブクラス非公開）----------

    def _find_next_targets(self) -> list[int]:
        """確認ラベル付き・処理中ではない対象を優先度順に返す。"""
        issues = github.list_issues(self.confirm_label)
        if not issues:
            return []
        # 処理中ラベルが付いていない対象だけを候補にする
        candidates = [
            i for i in issues
            if not has_label_prefix(
                [lbl["name"] for lbl in i.get("labels", [])],
                GH_KIT_LABEL_PROCESSING_PREFIX,  # noqa: F821 — constants.sh から動的注入
            )
        ]
        candidates.sort(key=self._sort_key)
        return [c["number"] for c in candidates]

    def _sort_key(self, issue: dict) -> tuple[int, int]:
        """ソート用キー（優先度ランク, 番号）。同ランクは番号昇順で古いものから処理。"""
        names = [lbl["name"] for lbl in issue.get("labels", [])]
        rank = priority_rank(
            names,
            GH_KIT_LABEL_PRIORITY_URGENT,  # noqa: F821
            GH_KIT_LABEL_PRIORITY_LOW,  # noqa: F821
        )
        return (rank, issue["number"])

    def _process_one(self, number: int) -> None:
        """1 件の対象を処理する: 処理中ラベル付与 → claude -p 起動 → 処理中ラベル除去。"""
        logger.info(f"[{self.name}] #{number} の処理を開始します")

        if not github.add_label(number, self.processing_label):
            logger.warning(f"[{self.name}] 処理中ラベルの付与に失敗しました（#{number}）")

        try:
            exit_code = run_claude_prompt(self.skill_command(number))
            if exit_code != 0:
                # 異常終了: 処理中ラベルだけ外してキュー再投入させる（次のポーリングで再試行）
                logger.error(
                    f"[{self.name}] claude -p が異常終了しました"
                    f"（#{number}, exit_code={exit_code}）"
                )
                return
            logger.info(f"[{self.name}] #{number} の処理が完了しました")
        finally:
            github.remove_label(number, self.processing_label)
