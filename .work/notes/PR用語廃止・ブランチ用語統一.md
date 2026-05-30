---
created_at: 2026-05-30
updates:
  - 2026-05-30 — 初版作成
related_specs: []
related_prs:
  - PR188
  - PR189
  - PR190
  - PR191
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
- index-tool.py とテンプレートの変更

### PR191: 既存フォルダ名の統一
- 8桁 YYYYMMDD → 6桁 YYMMDD 形式に一括リネーム
- 新規フォルダは日本語名を使う規約を追加

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
- merge, pr-handoff, pr-show など PR番号に依存するスキル群
