# ノートインデックス

`.work/notes/` 配下の設計メモ・構想ノートの一覧。カテゴリ別に分類。

---

## フック・自動化

フックの実装・設計・修正に関するメモ。

| ファイル | タイトル |
|---|---|
| [claude-kit-creator-skill-hook.md](claude-kit-creator-skill-hook.md) | クリエータースキルフック (claude-kit) — UserPromptSubmit フック設計メモ |
| [dev-kit-hooks.md](dev-kit-hooks.md) | dev-kit フック設計メモ |
| [fix-read-hook.md](fix-read-hook.md) | py-kit / next-kit 注入フック修正メモ |
| [hook-revert-direct-reason.md](hook-revert-direct-reason.md) | フック直接差し戻し方式の選択理由 — 設計判断メモ |
| [pre-compact-hook.md](pre-compact-hook.md) | PreCompact フック — conversation-to-claude 自動実行 |
| [split-hook-inline-python-to-scripts.md](split-hook-inline-python-to-scripts.md) | フックインライン Python 切り出し — hooks.json スクリプト分離 |
| [typescript-lint-hook.md](typescript-lint-hook.md) | TypeScript 型チェックフック (PR143) |

---

## スキル設計

スキルの設計・実装に関するメモ。

| ファイル | タイトル |
|---|---|
| [generator-metadata.md](generator-metadata.md) | ジェネレーターメタデータ — creator スキル生成物の出自トレース機構 |
| [interactive-review-skills.md](interactive-review-skills.md) | インタラクティブレビュースキル — AskUserQuestion を使った 2 つのレビュー |
| [next-kit-plan-skill.md](next-kit-plan-skill.md) | next-kit:plan スキル — Next.js プロジェクト設計計画書生成 |
| [plugin-config-skill.md](plugin-config-skill.md) | プラグイン設定スキル — 設計メモ (PR167) |
| [pr-show.md](pr-show.md) | pr-show スキル — 次 PR 候補一覧の状況表示 |
| [ref-inject-generator.md](ref-inject-generator.md) | ref-inject — リファレンス自動注入プラグインのジェネレータ |
| [work-kit-skills.md](work-kit-skills.md) | work-kit スキル群 — 設計メモ |

---

## プラグイン構成・統合

プラグインの構成変更・統合・廃止に関するメモ。

| ファイル | タイトル |
|---|---|
| [deprecate-rules-migrate-to-references.md](deprecate-rules-migrate-to-references.md) | ルール廃止とリファレンス移行 — .claude/rules/ 削除方針 |
| [integrate-guard-kit-into-workspace.md](integrate-guard-kit-into-workspace.md) | guard-kit を workspace に統合 — PR169 |
| [merge-language-plugins.md](merge-language-plugins.md) | py-kit / html-kit / next-kit → dev-kit 統合 (PR166) |
| [plugin-claude-md-standard.md](plugin-claude-md-standard.md) | プラグイン CLAUDE.md 標準構成 — 標準セクション定義 |

---

## 環境・設定・ポリシー

env 設定・運用ポリシー・用語規約に関するメモ。

| ファイル | タイトル |
|---|---|
| [add-protected-branches-env.md](add-protected-branches-env.md) | 保護ブランチ env 化 — PR177 |
| [env-toggles-for-hooks-and-steps.md](env-toggles-for-hooks-and-steps.md) | env トグル実装メモ — PR164 |
| [jp-mirror-policy.md](jp-mirror-policy.md) | JP ミラーポリシー — .md 作成時の .jp.md 強制 |
| [rename-pr-to-branch.md](rename-pr-to-branch.md) | PR 用語廃止・ブランチ用語統一 |

---

## バグ・不具合

バグ修正・不具合記録のメモ。

| ファイル | タイトル |
|---|---|
| [statusline-display-bug.md](statusline-display-bug.md) | ステータスライン非表示バグ — PR116 後の不具合メモ |

---

## ワークフロー・マージ

開発ワークフロー・マージフローに関するメモ。

| ファイル | タイトル |
|---|---|
| [incident-criteria.md](incident-criteria.md) | インシデント判定基準ノート (PR112) |
| [merge-next-pr-list.md](merge-next-pr-list.md) | マージ Step 12 — 次 PR 一覧の出力フォーマット |

---

## 構想・企画

アイデア・構想段階のメモ。

| ファイル | タイトル |
|---|---|
| [AIイシュー自動発見システム構想.md](AIイシュー自動発見システム構想.md) | AI イシュー自動発見システム — 構想ノート |
