# PR188 — rename-pr-to-branch

## 概要

workspace の work-start スキルを中心に、「PR（Pull Request）」という用語と命名規則を廃止し、「ブランチ」ベースの言い回しに統一する。

GitHubのPR概念に縛られた命名（`PR{N}/type/title` 形式のブランチ名、PR番号管理等）をやめ、シンプルなブランチ作成・マージフローに移行するための第一歩。

**具体的な変更点:**
- work-start Step 1: 「PR番号を決定する」→「ブランチ名を決定する」（index-tool.py の `next-id` を廃止）
- ブランチ名形式: `PR{N}/type/title` → `type/title`（PR番号プレフィックスを除去）
- ワークツリー名: `{repo}-wt-PR{N}` → `{repo}-wt-{branch-name}` 形式（例: `wt-refactor-rename-pr-to-branch`）
- SKILL.md 全体の「PR」表記を「ブランチ」に変更（Pull Request 概念への言及を除去）
- work-add SKILL.md: PR番号引数を除去し、ブランチ名だけ受け取る形に変更
- PRドキュメント内のセクション名変更: `## 関連PR` → `## 関連ブランチ`、`## 次PR候補` → `## 次ブランチ候補`

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA を確認・記録する | - |
| 済 | `.work/notes/` の作業メモを更新 | - |
| 済 | work-start SKILL.md の Step 1 を「ブランチ名決定」に変更（内部 ID 採番は継続） | - `plugins/workspace/skills/work-start/SKILL.md` |
| 済 | work-start SKILL.md のブランチ名形式を `type/title` に変更（PR番号除去） | - 同上 |
| 済 | work-start SKILL.md 全体の「PR」用語を「ブランチ」に統一 | - 同上 |
| 済 | work-add SKILL.md をブランチ名のみ受け取る形に変更（レガシー PR{N} は後方互換で破棄） | - `plugins/workspace/skills/work-add/SKILL.md` |
| 済 | work-add SKILL.md でワークツリー名を `wt-{branch-name}` 形式に変更（既存は変えない） | - 同上 |
| 済 | PRドキュメントテンプレートをリネーム + セクション名変更（関連PR→関連ブランチ、次PR候補→次ブランチ候補） | - `plugins/workspace/templates/.work/tasks/yymmdd_xxx/{PRNNN-type-title.md → type-title.md}` |
| 済 | setup-task.py の `--pr` → `--id` 化、テンプレート参照を新ファイル名へ | - `plugins/workspace/scripts/setup-task.py` |
| 済 | merge / pr-handoff / pr-show / impl-review / qa-review / plugin-update / branch-index-cleanup の PR 用語をブランチ用語に更新 | - 関連スキル全般 |
| 済 | hook prompts (stop / stop-no-merge / user-prompt-submit) を更新 | - `plugins/workspace/hooks/prompts/*` |
| 済 | templates/.work/CLAUDE.md（jp）と templates/note.md, templates/.work/notes/xxx.md を更新 | - `plugins/workspace/templates/**` |
| 済 | 各 SKILL.jp.md / *.jp.md を同期 | - 対象の `.jp.md` ファイル |
| 済 | plugin.json / marketplace.json を v3.0.0 にバージョンアップ | - 該当ファイル |
| 済 | コミット | - |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/workspace/skills/work-start/SKILL.md` | 編集 | Step 1 を「ブランチ名決定」に変更、ブランチ形式 `{type}/{title}`、ワークツリー `wt-{type}-{title}`、用語を全面「ブランチ」に。setup-task.py 引数を `--id` 化 | 内部 ID は採番継続 |
| `plugins/workspace/skills/work-start/SKILL.jp.md` | 編集 | 英語版に追随した JP ミラー | jp-mirror-translator 出力 |
| `plugins/workspace/skills/work-add/SKILL.md` | 編集 | 引数を `{type}/{title}` 単体に、ワークツリー `../{repo}-wt-{type}-{title}`、レガシー `PR{N}` は後方互換で破棄 | - |
| `plugins/workspace/skills/work-add/SKILL.jp.md` | 編集 | 英語版に追随した JP ミラー | - |
| `plugins/workspace/scripts/setup-task.py` | 編集 | `--pr` → `--id` (alias `--pr` 残し)、テンプレートパスを `type-title.md` に。`{N}/{タイトル}/{ブランチ名}` プレースホルダ展開 | - |
| `plugins/workspace/templates/.work/tasks/yymmdd_xxx/type-title.md` | 新規（リネーム） | 旧 `PRNNN-type-title.md` を rename。本文を `# {ブランチ名}` 形式に再構成、`## 関連ブランチ` / `## 次ブランチ候補` セクションへ | git mv |
| `plugins/workspace/skills/merge/SKILL.md` | 編集 | branch 用語に統一、`{WORKTREE_PATH}` `{BRANCH_NAME}` 変数化、コミット cross-ref `#PR{N}` → `#{N}`、レガシー対応の注記 | - |
| `plugins/workspace/skills/merge/SKILL.jp.md` | 編集 | JP ミラー | - |
| `plugins/workspace/skills/pr-handoff/SKILL.md` | 編集 | `次PR候補` → `次ブランチ候補` 等。スキル名は互換維持 | - |
| `plugins/workspace/skills/pr-handoff/SKILL.jp.md` | 編集 | JP ミラー | - |
| `plugins/workspace/skills/pr-show/SKILL.md` | 編集 | `次PR候補` → `次ブランチ候補`、表ヘッダ PR → Branch、find パターン更新 | - |
| `plugins/workspace/skills/pr-show/SKILL.jp.md` | 編集 | JP ミラー | - |
| `plugins/workspace/skills/impl-review/SKILL.md` | 編集 | PR → working branch 用語統一、引数説明を更新 | - |
| `plugins/workspace/skills/impl-review/SKILL.jp.md` | 編集 | JP ミラー（手動更新） | - |
| `plugins/workspace/skills/qa-review/SKILL.md` | 編集 | PR document → branch document、find パターン更新 | - |
| `plugins/workspace/skills/qa-review/SKILL.jp.md` | 編集 | JP ミラー（手動更新） | - |
| `plugins/workspace/skills/plugin-update/SKILL.md` | 編集 | PR branch → working branch、コミットメッセージテンプレ更新 | - |
| `plugins/workspace/skills/plugin-update/SKILL.jp.md` | 編集 | JP ミラー | - |
| `plugins/workspace/skills/branch-index-cleanup/SKILL.md` | 編集 | 新形式/レガシー両対応の照合ロジックに更新 | - |
| `plugins/workspace/skills/branch-index-cleanup/SKILL.jp.md` | 編集 | JP ミラー | - |
| `plugins/workspace/hooks/prompts/stop.md` | 編集 | PR → ブランチ用語統一、merge 候補表示を branch 名で | - |
| `plugins/workspace/hooks/prompts/stop.jp.md` | 編集 | JP ミラー | - |
| `plugins/workspace/hooks/prompts/stop-no-merge.md` | 編集 | PR → ブランチ用語統一、`[work-kit]` → `[workspace]` | - |
| `plugins/workspace/hooks/prompts/stop-no-merge.jp.md` | 編集 | JP ミラー | - |
| `plugins/workspace/hooks/prompts/user-prompt-submit.md` | 編集 | 「PR が進行中」→「ブランチが進行中」等 | - |
| `plugins/workspace/hooks/prompts/user-prompt-submit.jp.md` | 編集 | JP ミラー | - |
| `plugins/workspace/templates/.work/CLAUDE.md` | 編集 | ディレクトリ説明・セクション名を branch 用語に統一 | - |
| `plugins/workspace/templates/.work/CLAUDE.jp.md` | 編集 | JP ミラー | - |
| `plugins/workspace/templates/note.md` | 編集 | `related_prs` → `related_branches` | - |
| `plugins/workspace/templates/.work/notes/xxx.md` | 編集 | `related_prs` → `related_branches` | - |
| `plugins/workspace/.claude-plugin/plugin.json` | 編集 | version 2.44.0 → 3.0.0、description 更新 | breaking |
| `.claude-plugin/marketplace.json` | 編集 | workspace 行 version 2.44.0 → 3.0.0、description 更新 | breaking |

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

**状態**: 解決済み — **B を採用**。内部 ID は採番継続、ブランチ名・ファイル名には露出しない。

**決定したら反映先**: `## 作業内容` の「他の workspace スキル調査」行、および PR190 のスコープ定義

### QA-002: 既存ワークツリーとの命名衝突

**背景**: 現在 `wt-PR{N}` で命名されているワークツリーが複数存在する。新形式 `wt-{branch-name}` に変えたとき、既存のワークツリーとの共存や命名衝突をどう扱うか。

| 案 | 内容 |
|---|---|
| A | 既存ワークツリーはそのまま（renameしない）。新規作成分から新形式に切り替え |
| B | 既存ワークツリーも新形式にリネーム（移行スクリプト作成） |

**推奨方式**: A — 既存は変えない。新規作成分から切り替える。

**状態**: 解決済み — **A を採用**。既存ワークツリーはそのまま。新規は `wt-{branch-name}` 形式（例: `my-plugins-wt-refactor-rename-pr-to-branch`）。

**決定したら反映先**: `## 作業内容` の work-add 変更行

## 参考ドキュメント

- `.work/notes/rename-pr-to-branch.md` — 本変更の設計メモ（動機・方針・影響範囲）
- `plugins/workspace/skills/work-start/SKILL.md` — 変更対象メインスキル
- `plugins/workspace/skills/work-add/SKILL.md` — ワークツリー作成スキル

## 関連ブランチ

| ブランチ | 概要 |
|---|---|
| PR168/refactor/refactor-task-doc-structure | PR ドキュメント単一ファイル化（命名規則の前回変更） |

## 次ブランチ候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| タスクドキュメントのファイル名を YYMMDD-ブランチ名形式に変更 | setup-task.py と work-start Step 6 を変更し、`PR{N}-type-title.md` → `YYMMDD-branch-name.md` 形式にする | 「rename-pr-to-branch」が完了してから |
| index.yaml の prs: キーを branches: に改名 | index-tool.py とテンプレート（index.yaml / index.archive.yaml）の `prs:` キーを `branches:` に改名する | 即時実施可 |
| 既存タスクフォルダの日付プレフィックスを 6 桁に統一 | 8桁 YYYYMMDD 形式のフォルダを 6桁 YYMMDD 形式に一括リネーム。新規フォルダは日本語名を使う規約を SKILL.md に追記 | 即時実施可 |
