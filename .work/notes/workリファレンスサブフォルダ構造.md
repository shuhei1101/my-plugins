---
created_at: 2026-05-31
updates:
  - 2026-05-31 — 初版作成（refactor/references-subfolder-split にてサブフォルダ分割実施）
  - 2026-05-31 — work-dir/ をテンプレート別に細分化（タスクドキュメント/タスクインデックス/イシュー追加・ドットワークディレクトリ構成→ワークディレクトリ構成）。injection をパス別に再構成。TODOテンプレート同期削除（refactor/work-templates-to-ref-inject）
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
│   ├── ワークディレクトリ構成.md / .jp.md      # .work/ 俯瞰
│   ├── タスクドキュメント.md / .jp.md          # ブランチドキュメントテンプレート
│   ├── タスクインデックス.md / .jp.md          # index.yaml スキーマ
│   └── イシュー.md / .jp.md                    # ISSUE-N.md 構成
└── skill-sync/
    ├── マージスキル同期.md / .jp.md
    ├── スタートスキル同期.md / .jp.md
    └── ストッププロンプト同期.md / .jp.md
```

## カテゴリ定義

| # | フォルダ | 対象 |
|---|---|---|
| 1 | `work-dir/` | `.work/` 各サブフォルダの構成定義・テンプレート（俯瞰 + tasks/index/issues を細分化） |
| 2 | `notes/` | `.work/notes/` のファイル命名・記述内容に関するルール |
| 3 | `skill-sync/` | プラグイン本体のスキルファイル間の同期ルール（マージ・スタート・ストップ） |

## injection ルール概要

テンプレート／構成定義は `.work/` の該当パスを作成・編集するときに ref-inject の Write/Edit
フックで注入される（テンプレートは「コピー」ではなく「注入されたものを元に Claude が直接作成」）。

| # | パターン | 注入リファレンス |
|---|---|---|
| 1 | `plugins/work/hooks/prompts/{stop,stop-no-merge}*.md` | `skill-sync/ストッププロンプト同期.md` |
| 2 | `plugins/work/skills/merge/SKILL*.md` | `skill-sync/マージスキル同期.md` |
| 3 | `plugins/work/skills/{start,worktree-create,vscode-workspace-sync}/SKILL*.md` | `skill-sync/スタートスキル同期.md` |
| 4 | `.work/**` | `work-dir/ワークディレクトリ構成.md` |
| 5 | `.work/tasks/**/*.branch.md` | `work-dir/タスクドキュメント.md` |
| 6 | `.work/tasks/index*.yaml` | `work-dir/タスクインデックス.md` |
| 7 | `.work/notes/**` | `notes/ノート命名規則.md` + `notes/ノート記述内容ルール.md` |
| 8 | `.work/issues/**` | `work-dir/イシュー.md` |

## 変更履歴

| # | 日付 | 内容 |
|---|---|---|
| 1 | 2026-05-31 | v2.54.0: `work-dir/` をテンプレート別に細分化（タスクドキュメント/タスクインデックス/イシューを追加、ドットワークディレクトリ構成→ワークディレクトリ構成）。injection をパス別（`.work/**` / `.branch.md` / `index*.yaml` / `notes/**` / `issues/**`）に再構成。`TODOテンプレート同期` 削除。テンプレートは ref-inject 注入で配信する方式に統一 |
| 2 | 2026-05-31 | サブフォルダ分割実施（v2.53.1）。それ以前はリファレンスが `references/` 直下に平置き |
