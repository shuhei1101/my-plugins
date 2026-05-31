---
created_at: 2026-05-30
updates:
  - 2026-05-30 — 初版作成
  - 2026-05-30 — PR188: work-start の PR 用語をブランチ用語に統一
  - 2026-05-30 — PR190: index.yaml / index.archive.yaml の prs: キーを branches: に改名
  - 2026-05-31 — #230: pr-handoff → branch-reserve、pr-show → branch-show にリネーム
  - 2026-05-31 — #244: ブランチ文書ファイル名を日本語タイトル基準に変更、index.yaml に branch フィールド追加
  - 2026-05-31 — #248: user-prompt-submit.py・trim-index.py・issue-tool.py・plugin-config スキル・setup スキル内の残存 PR 用語をブランチ用語に統一
related_notes: []
related_prs:
  - PR188
  - PR189
  - PR190
  - PR191
  - "#244"
  - "#248"
---

# PR用語廃止・ブランチ用語統一

## 概要

workspace の work-start スキルを中心に「PR（Pull Request）」という GitHub 固有の用語と命名規則を廃止し、「ブランチ作成→マージ」というシンプルなフローの用語に統一する。

## 変更の動機

- 「PR」は GitHub 用語であり、git 自体の概念ではない
- ブランチ名に `PR{N}/` プレフィックスを付けるのは冗長で、ブランチの内容を表さない
- 「プルリクエストを作成」という言い方がワークフローの本質（ブランチを切って作業しマージする）を隠している

## 変更方針

### PR188: work-start 用語変更
- Step 1: 「PR番号を決定する」→「ブランチ名を決定する」
- ブランチ形式: `PR{N}/type/title` → `type/title`
- ワークツリー名: `wt-PR{N}` → `wt-{type}-{title}`
- SKILL.md 全体の「PR」→「ブランチ」

### PR189: タスクドキュメントのファイル名変更
- 現在: `PR{N}-type-title.md`
- 変更後: `YYMMDD-branch-name.md`
- setup-task.py の変更が必要

### PR190: index.yaml キー名変更
- `prs:` → `branches:`
- index-tool.py / trim-index.py とテンプレートの変更

**実施内容（PR190）:**
- QA-001: 新名称 → `branches:` を採用（`work_items:` / `tasks:` より明確）
- QA-002: 移行方針 → 一括置換（ローカルファイルなので後方互換不要）

| ファイル | 変更内容 |
|---|---|
| `plugins/work/scripts/index-tool.py` | `data.get("prs")` → `data.get("branches")`、変数名も統一 |
| `plugins/work/scripts/trim-index.py` | 同上 |
| `plugins/work/templates/.work/tasks/index.yaml` | `prs: []` → `branches: []` |
| `plugins/work/templates/.work/tasks/index.archive.yaml` | `archived_prs: []` → `branches: []`（既存バグ修正） |
| 各 `.work/tasks/index*.yaml`（gitignored） | 一括 sed 置換 |

**既存バグ修正:** テンプレート `index.archive.yaml` が `archived_prs:` キーを使っていたが、スクリプトは `"prs"` キーで読み書きしていた。PR190 で `branches:` に統一して修正済み。

### PR191: 既存フォルダ名の統一
- 8桁 YYYYMMDD → 6桁 YYMMDD 形式に一括リネーム
- 新規フォルダは日本語名を使う規約を追加

### #244: ブランチ文書ファイル名を日本語タイトル基準に変更

- ファイル名: `{YYMMDD}-{branch-hyphenated}.md` → `{YYMMDD}-{日本語タイトル}.md`
- テンプレートにブランチ名行 (`> ブランチ: \`{branch-name}\``) を追加（H1 直下）
- `setup-task.py` に `--ja-title` パラメータ追加
- `index.yaml` に `branch` フィールド追加（git ブランチ名）
- `index-tool.py` の `add` サブコマンドに `--branch` パラメータ追加
- PR 言語をスクリプトのコメント・出力メッセージから除去
- 関連スキル・フック・リファレンスのパス表記 `{branch-hyphenated}.md` → `{YYMMDD}-{日本語タイトル}.md` に統一

### #248: workプラグイン内の残存 PR 用語を一括修正

| # | ファイル | 変更内容 |
|---|---|---|
| 1 | `plugins/work/hooks/scripts/user-prompt-submit.py` | docstring「PR 在中チェック」→「ブランチ文書確認」、`WORK_PR_ENFORCEMENT`→`WORK_BRANCH_ENFORCEMENT` |
| 2 | `plugins/work/scripts/trim-index.py` | "completed PR(s)" / "active PR(s)" → "completed branch(es)" / "active branch(es)" |
| 3 | `plugins/work/scripts/issue-tool.py` | `--linked-pr`→`--linked-branch`、`linked_pr`→`linked_branch`、出力メッセージ修正 |
| 4 | `plugins/work/skills/plugin-config/SKILL.md` | `WORK_PR_ENFORCEMENT`→`WORK_BRANCH_ENFORCEMENT` |
| 5 | `plugins/work/skills/plugin-config/SKILL.jp.md` | 〃（JPミラー） |
| 6 | `plugins/work/skills/setup/SKILL.md` | "Task / PR folders"→"Task / branch folders" |
| 7 | `plugins/work/skills/setup/SKILL.jp.md` | "タスク・PR フォルダ"→"タスク・ブランチフォルダ" |

**留意:** legacy backward-compat 用途（`branch-index-cleanup`・`merge`・`worktree-create` スキルの `PR{N}/` 形式説明）は意図的に残存。これらは既存のレガシーブランチを扱うための文書であり、用語ではなく命名形式の説明のため対象外とした。

## 未決定事項

### index.yaml の ID 管理
- PR番号をブランチ名から除去した後、内部IDをどうするか
- 推奨: 内部IDは残し（採番継続）、ブランチ名・ファイル名には露出しない（PR188スコープ外）

### 既存ワークツリーの扱い
- 既存の `wt-PR{N}` ワークツリーはリネームしない（新規作成分から新形式）

## 影響範囲

- `plugins/workspace/skills/work-start/SKILL.md`
- `plugins/workspace/skills/work-add/SKILL.md`
- `plugins/workspace/scripts/setup-task.py`
- `plugins/workspace/scripts/index-tool.py`
- `plugins/workspace/templates/.work/tasks/index.yaml`
- `plugins/workspace/templates/.work/tasks/index.archive.yaml`
- 各 SKILL.jp.md ミラー
- merge スキル（#230 で更新済み）
- pr-handoff → branch-reserve にリネーム済み（#230）
- pr-show → branch-show にリネーム済み（#230）
