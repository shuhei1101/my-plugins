# PR188 — rename-pr-to-branch

## 概要

workspace の work-start スキルを中心に、「PR（Pull Request）」という用語と命名規則を廃止し、「ブランチ」ベースの言い回しに統一する。

GitHubのPR概念に縛られた命名（`PR{N}/type/title` 形式のブランチ名、PR番号管理等）をやめ、シンプルなブランチ作成・マージフローに移行するための第一歩。

**具体的な変更点:**
- work-start Step 1: 「PR番号を決定する」→「ブランチ名を決定する」（index-tool.py の `next-id` を廃止）
- ブランチ名形式: `PR{N}/type/title` → `type/title`（PR番号プレフィックスを除去）
- ワークツリー名: `{repo}-wt-PR{N}` → `{repo}-wt-{type}-{title}` 形式
- SKILL.md 全体の「PR」表記を「ブランチ」に変更（Pull Request 概念への言及を除去）
- work-add SKILL.md: PR番号引数を除去し、ブランチ名だけ受け取る形に変更

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | QA を確認・記録する | - |
| - | `.work/notes/` の作業メモを更新 | - |
| - | work-start SKILL.md の Step 1 を「ブランチ名決定」に変更（`next-id` 廃止） | - `plugins/workspace/skills/work-start/SKILL.md` |
| - | work-start SKILL.md のブランチ名形式を `type/title` に変更（PR番号除去） | - 同上 |
| - | work-start SKILL.md 全体の「PR」用語を「ブランチ」に統一 | - 同上 |
| - | work-add SKILL.md をブランチ名のみ受け取る形に変更 | - `plugins/workspace/skills/work-add/SKILL.md` |
| - | work-add SKILL.md でワークツリー名を `wt-{type}-{title}` 形式に変更 | - 同上 |
| - | 他の workspace スキル（merge, pr-handoff 等）で PR番号に強く依存する箇所を調査・更新 | - 関連スキル全般 |
| - | 各 SKILL.jp.md を同期 | - 対象の `.jp.md` ファイル |
| - | ルール・CLAUDE.md を更新（必要なら） | - |
| - | コミット | - |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| - | - | テスト追加なし | - |

## QA

### QA-001: PR番号なしになったときの index.yaml の役割

**背景**: 現在 index.yaml は `last_id` でPR番号を採番し、ブランチ名にも `PR{N}` が入る。PR番号をブランチ名から除去した場合、index.yaml のID管理をどうするか。

| 案 | 内容 |
|---|---|
| A | index.yaml の `last_id` / `id` フィールドを廃止し、ブランチ名をキーとして管理 |
| B | 内部IDは残す（採番継続）が、ブランチ名・ドキュメントファイル名には露出しない |
| C | index.yaml 自体を廃止し、git branch 一覧で管理 |

**推奨方式**: B — 内部IDは残し、ブランチ名からは除去する。PR188 のスコープでは index.yaml の構造変更は PR190 に委ねる。

**状態**: 未解決（PR188 着手時に確認）

**決定したら反映先**: `## 作業内容` の「他の workspace スキル調査」行、および PR190 のスコープ定義

### QA-002: 既存ワークツリーとの命名衝突

**背景**: 現在 `wt-PR{N}` で命名されているワークツリーが複数存在する。新形式 `wt-{type}-{title}` に変えたとき、既存のワークツリーとの共存や命名衝突をどう扱うか。

| 案 | 内容 |
|---|---|
| A | 既存ワークツリーはそのまま（renameしない）。新規作成分から新形式に切り替え |
| B | 既存ワークツリーも新形式にリネーム（移行スクリプト作成） |

**推奨方式**: A — 既存は変えない。新規作成分から切り替える。

**状態**: 未解決（PR188 着手時に確認）

**決定したら反映先**: `## 作業内容` の work-add 変更行

## 参考ドキュメント

- `.work/notes/rename-pr-to-branch.md` — 本変更の設計メモ（動機・方針・影響範囲）
- `plugins/workspace/skills/work-start/SKILL.md` — 変更対象メインスキル
- `plugins/workspace/skills/work-add/SKILL.md` — ワークツリー作成スキル

## 関連PR

| PR番号 | 概要 |
|---|---|
| #168 | PR ドキュメント単一ファイル化（命名規則の前回変更） |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| タスクドキュメントのファイル名を YYMMDD-ブランチ名形式に変更 | setup-task.py と work-start Step 6 を変更し、`PR{N}-type-title.md` → `YYMMDD-branch-name.md` 形式にする | 「rename-pr-to-branch」が完了してから |
| index.yaml の prs: キーを branches: に改名 | index-tool.py とテンプレート（index.yaml / index.archive.yaml）の `prs:` キーを `branches:` に改名する | 即時実施可 |
| 既存タスクフォルダの日付プレフィックスを 6 桁に統一 | 8桁 YYYYMMDD 形式のフォルダを 6桁 YYMMDD 形式に一括リネーム。新規フォルダは日本語名を使う規約を SKILL.md に追記 | 即時実施可 |
