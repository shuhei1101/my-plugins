---
created_at: 2026-05-31
updates:
  - 2026-05-31 — 初版作成（refactor/references-subfolder-split にてサブフォルダ分割実施）
  - 2026-05-31 — injection ルール更新（refactor/work-templates-to-ref-inject にて templates/** → scripts/setup-task.py に変更）
related_specs: []
related_branches:
  - refactor/references-subfolder-split
  - refactor/work-templates-to-ref-inject
---

# work リファレンスサブフォルダ構造

## 現在のフォルダ構成

```
plugins/work/references/
├── .ref-injects/
│   ├── CLAUDE.md / CLAUDE.jp.md
│   ├── _index.yaml / _index.jp.yaml
│   └── _injection_rules.yaml
├── _index.md
├── notes/
│   ├── ノート命名規則.md / .jp.md
│   └── ノート記述内容ルール.md / .jp.md
├── work-dir/
│   └── ドットワークディレクトリ構成.md / .jp.md
└── skill-sync/
    ├── マージスキル同期.md / .jp.md
    ├── スタートスキル同期.md / .jp.md
    ├── ストッププロンプト同期.md / .jp.md
    └── TODOテンプレート同期.md / .jp.md
```

## カテゴリ定義

| # | フォルダ | 対象 |
|---|---|---|
| 1 | `notes/` | `.work/notes/` のファイル命名・記述内容に関するルール |
| 2 | `work-dir/` | `.work/` ディレクトリ構成・コミット規約に関するガイド |
| 3 | `skill-sync/` | スキルファイル間の同期ルール（マージ・スタート・ストップ・TODO テンプレート） |

## injection ルール概要

| # | パターン | 注入リファレンス |
|---|---|---|
| 1 | `plugins/work/hooks/prompts/{stop,stop-no-merge}*.md` | `skill-sync/ストッププロンプト同期.md` |
| 2 | `plugins/work/skills/merge/SKILL*.md` | `skill-sync/マージスキル同期.md` |
| 3 | `plugins/work/skills/{start,worktree-create,vscode-workspace-sync}/SKILL*.md` | `skill-sync/スタートスキル同期.md` |
| 4 | `plugins/work/scripts/setup-task.py` / `skills/{start,pr-handoff}/SKILL*.md` | `skill-sync/TODOテンプレート同期.md` |
| 5 | `.work/**` | `work-dir/ドットワークディレクトリ構成.md` |
| 6 | `.work/notes/**` | `notes/ノート命名規則.md` + `notes/ノート記述内容ルール.md` |

## 変更履歴

| # | 日付 | 内容 |
|---|---|---|
| 1 | 2026-05-31 | injection ルールを更新（v2.54.0）。`templates/**` → `scripts/setup-task.py` に変更（templates/ 廃止に伴う） |
| 2 | 2026-05-31 | サブフォルダ分割実施（v2.53.1）。それ以前はリファレンスが `references/` 直下に平置き |
