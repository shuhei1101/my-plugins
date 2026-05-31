# PR168 — refactor-task-doc-structure

## 概要

workspace（旧 work-kit）のタスクドキュメント構造を刷新する。

旧構造は PR ごとに `.work/tasks/{YYYYMMDD}_{title}/PR{N}/TODO.md` と `QA.md` の 2 ファイルに分かれ、日付プレフィックスは 8 桁の `YYYYMMDD`。
新構造では PR ごとに 1 つの Markdown ファイルに統合し、日付プレフィックスを 6 桁 `YYMMDD`、ファイル名はブランチ名のスラッシュをハイフンに置換した形にする。実装ファイル / テストのテーブルも新規セクションとして導入する。

合わせて、`update` スキルを `plugin-update` にリネームし、内容を「workspace 自身の静的テンプレ（`.work/` 配下）を最新化する」スキルに整理。さらに claude-kit の plugin authoring guide (`plugins/claude-kit/references/plugin-structure.md`) に「全プラグインは `plugin-update` 同等のスキルを同梱すること」を必須化として明記する。

**master 反映**: 当初 work-kit プラグイン配下で実装したが、master では並行して PR165（mark-generated・provenance スタンプ全廃）／PR166（py-kit/html-kit/next-kit を dev-kit に統合）／PR169（guard-kit を workspace に統合）／PR170（version-sync 廃止）／PR172（work-kit → workspace リネーム）が進行していたため、`git merge master -X theirs` で取り込み、workspace 構造の上に PR168 の変更を再適用した。これに伴い:

- provenance スタンプ追加は全て撤回（PR165 追従）
- plugin-update スキルから `claude-kit:version-sync` 委譲を削除（PR170 追従）
- パス・namespace は全て `workspace:` 系に統一（PR172 追従）

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | 新テンプレ `templates/.work/tasks/yymmdd_xxx/PRNNN-type-title.md` を workspace 配下に作成 | - `plugins/workspace/templates/.work/tasks/yymmdd_xxx/PRNNN-type-title.md` |
| 済 | 旧テンプレ（`yyyymmdd_xxx/PRXXX/{TODO,QA}.md`、`templates/{TODO,QA}.md`）を削除 | - |
| 済 | `setup-task.py` を `--branch` 受付・単一ファイル生成・YYMMDD 対応に改修 | - `plugins/workspace/scripts/setup-task.py` |
| 済 | `work-start` SKILL.md を新構造に書き換え（YYMMDD、新セクション説明、Step 統合） | - `plugins/workspace/skills/work-start/SKILL.md` (jp) |
| 済 | `merge` / `pr-handoff` / `pr-show` / `qa-review` / `setup` のパス参照を新構造に更新 | - 各 `plugins/workspace/skills/*/SKILL.md` (jp) |
| 済 | フックプロンプト（`user-prompt-submit.md` / `stop.md`）を新構造に更新 | - `plugins/workspace/hooks/prompts/user-prompt-submit.md` (jp)<br>- `plugins/workspace/hooks/prompts/stop.md` (jp) |
| 済 | `update` スキルを `plugin-update` にリネーム＆内容を「workspace テンプレ最新化」に整理 | - `plugins/workspace/skills/plugin-update/SKILL.md` (jp)（旧 `skills/update/` は削除） |
| 済 | `templates/.work/CLAUDE.md` / `.jp.md` を新構造の説明に書き換え | - `plugins/workspace/templates/.work/CLAUDE.md`<br>- `plugins/workspace/templates/.work/CLAUDE.jp.md` |
| 済 | claude-kit の plugin authoring guide に `plugin-update` 必須記述を追加 | - `plugins/claude-kit/references/plugin-structure.md`<br>- `plugins/claude-kit/references/plugin-structure.jp.md` |
| 済 | glossary（英 / 日）に新規用語を追記 | - `.claude/rules/core/glossary.md`<br>- `.claude/rules-jp/core/glossary.md` |
| 済 | `plugin.json` / `marketplace.json` を workspace v2.44.0 にバンプ（MINOR） | - `plugins/workspace/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |
| 済 | master 取り込み（`git merge master -X theirs`）で workspace 構造に寄せる | - 各種衝突解消 |
| 済 | コミット | - |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/workspace/templates/.work/tasks/yymmdd_xxx/PRNNN-type-title.md` | 新規 | 新構造の PR ドキュメントテンプレート（TODO/変更内容/テスト/QA/参考/関連イシュー/関連PR/次PR候補を 1 ファイルに統合） | setup-task.py が読むテンプレ本体 |
| `plugins/workspace/templates/.work/tasks/yyyymmdd_xxx/PRXXX/{TODO,QA}.md` | 削除 | 旧テンプレ | - |
| `plugins/workspace/templates/{TODO,QA}.md` | 削除 | 旧 setup-task.py 用テンプレ（新テンプレに統合） | - |
| `plugins/workspace/templates/.work/CLAUDE.md` / `.jp.md` | 編集 | 新構造の説明に書き換え、`/workspace:plugin-update` を skills 表に追加 | - |
| `plugins/workspace/scripts/setup-task.py` | 編集 | `--branch` 引数追加・単一ファイル `{branch-hyphenated}.md` 生成・YYMMDD 対応 | - |
| `plugins/workspace/skills/work-start/SKILL.md` / `.jp.md` | 編集 | 新仕様（YYMMDD・新テンプレパス・新セクション説明）に書き換え。Step 6 を単一ファイル生成に、Step 9 を PR ドキュメント内 `## QA` 追記に変更 | - |
| `plugins/workspace/skills/merge/SKILL.md` / `.jp.md` | 編集 | TODO.md/QA.md パス参照を新構造（PR ドキュメント内セクション）に書き換え | - |
| `plugins/workspace/skills/pr-handoff/SKILL.md` / `.jp.md` | 編集 | TODO.md 言及を PR ドキュメントに置換 | - |
| `plugins/workspace/skills/pr-show/SKILL.md` / `.jp.md` | 編集 | `find -name TODO.md` を `find -type f -name "PR*.md"` に変更、文言を PR ドキュメント基準に | - |
| `plugins/workspace/skills/qa-review/SKILL.md` / `.jp.md` | 編集 | QA.md ファイル単独参照を PR ドキュメント内 `## QA` セクション参照に書き換え（`### QA-XXX` サブセクション対象） | - |
| `plugins/workspace/skills/setup/SKILL.md` / `.jp.md` | 編集 | 古い `.work/QA.md` 言及を削除（実体が存在しないため） | - |
| `plugins/workspace/skills/update/` | 削除 | `plugin-update` へリネーム | - |
| `plugins/workspace/skills/plugin-update/SKILL.md` / `.jp.md` | 新規 | workspace テンプレ最新化スキル（version-sync 委譲は持たない最小版） | - |
| `plugins/workspace/hooks/prompts/user-prompt-submit.md` / `.jp.md` | 編集 | Step 2 のパス参照を PR ドキュメント内セクションに書き換え（YYYYMMDD → YYMMDD も） | - |
| `plugins/workspace/hooks/prompts/stop.md` / `.jp.md` | 編集 | TODO/QA 言及を PR ドキュメント内セクション参照に書き換え | - |
| `plugins/workspace/.claude-plugin/plugin.json` | 編集 | v2.43.0 → v2.44.0（MINOR bump） | 新機能扱い |
| `.claude-plugin/marketplace.json` | 編集 | workspace エントリを v2.44.0 に | plugin.json と揃える |
| `plugins/claude-kit/references/plugin-structure.md` / `.jp.md` | 編集 | 「## Required skills」セクションを追加し、全プラグインに `plugin-update` 同梱を必須化 | - |
| `.claude/rules/core/glossary.md` / `.claude/rules-jp/core/glossary.md` | 編集 | 新用語 4 件を追記（PR ドキュメント単一ファイル化 / 変更内容セクション / テストセクション / plugin-update スキル） | - |
| `.work/tasks/260530_refactor-task-doc-structure/PR168-refactor-refactor-task-doc-structure.md` | 新規 | PR168 自身のタスクドキュメント（新フォーマットで自己生成） | - |

## テスト

このリファクタは Claude が読む Markdown / Python スクリプトの構造変更で、ランタイム挙動の検証は手動でのドッグフード（PR168 自体の作成・運用）で行う。テストファイルの追加はなし。

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| - | - | テスト追加なし（ドッグフードで検証） | - |

## QA

このセッションでユーザーと合意した設計判断を記録する。

### QA-001: PR ドキュメントのファイル名フォーマット

**背景**: 旧構造の `PR{N}/TODO.md` + `PR{N}/QA.md` を 1 ファイルに統合する際、ファイル名をどう命名するか。

| 案 | 内容 |
|---|---|
| A | `PR{N}-{title}.md` |
| B | `PR{N}-{type}-{title}.md`（ブランチ名のスラッシュをハイフン化） |
| C | `PR{N}.md` |

**推奨方式**: B（ブランチ名全体をハイフン化）。

**状態**: 解決済み — 案 B 採用

**決定したら反映先**: `setup-task.py` の `--branch` 処理、各 SKILL.md / CLAUDE.md / glossary

### QA-002: 既存タスクフォルダ（PR1〜PR167）の移行範囲

**背景**: 既存に大量の `{YYYYMMDD}_{title}/PR{N}/{TODO,QA}.md` フォルダが存在する。

| 案 | 内容 |
|---|---|
| A | 放置、PR168 以降のみ新構造 |
| B | 全件リネーム＆統合（スクリプト必須） |

**推奨方式**: A。

**状態**: 解決済み — 案 A 採用

**決定したら反映先**: `work-start` Step 5 ノート

### QA-003: PR168 自身のドキュメントを新構造で作るか

**推奨方式**: A（先に setup-task.py を改修して、新構造で生成）。

**状態**: 解決済み — 案 A 採用

### QA-004: 日付フォーマット

**推奨方式**: 6 桁 `YYMMDD`。

**状態**: 解決済み

### QA-005: `update` スキルのリネーム名

| 案 | 内容 |
|---|---|
| A | `sync-templates` |
| B | `align-to-latest` |
| C | `update-plugin` → `plugin-update` |

**推奨方式**: C — ユーザー指示「plugin-update にして」で確定。

**状態**: 解決済み — `plugin-update` 採用

### QA-006: master 取り込み時の戦略

**背景**: 着手時点では master が `work-kit` のままだったが、進行中に PR165/PR166/PR169/PR170/PR172 が次々マージされ、PR168 の前提（plugins/work-kit/ 配下を編集、mark-generated でスタンプ、version-sync に委譲）が崩れた。

| 案 | 内容 |
|---|---|
| A | PR168 を破棄して再設計 |
| B | `git merge master` で取り込み手動衝突解消（PR168 をほぼ書き直し） |
| C | `git merge master -X theirs` で master 優先取り込み、新ファイルだけ workspace に移植 |

**推奨方式**: C。

**状態**: 解決済み — ユーザー指示「最新の master に寄せて、それに PR168 の変更を加える」で C を採用

**決定したら反映先**: 本ドキュメント全体（workspace 構造ベースに書き換え）

### QA-007: plugin-update スキルを必須プラグイン要素として規定する場所

**背景**: ユーザー要望「`plugin-update` スキルは今後プラグインを作るときに必ず含めてほしい。プラグイン作成のリファレンスに書いておいて」。

**推奨方式**: `plugins/claude-kit/references/plugin-structure.md` (jp) に「## Required skills」セクションを追加し、`plugin-update` を必須スキルとして明文化する。標準仕様（命名・トリガー・最初の動作・スコープ・参考実装）も同セクションに記す。

**状態**: 解決済み

**決定したら反映先**: `plugins/claude-kit/references/plugin-structure.md` / `.jp.md`

## 参考ドキュメント

- `plugins/claude-kit/references/plugin-structure.md`: plugin-update 必須記述追加先
- `.claude/rules/core/glossary.md`: 新用語追加先

## 関連PR

| PR番号 | 概要 |
|---|---|
| #164 | env トグル一覧の導入（workspace 系運用見直し） |
| #165 | mark-generated と provenance スタンプ全廃（PR168 のスタンプ追加を撤回） |
| #166 | py-kit / html-kit / next-kit を dev-kit に統合 |
| #169 | guard-kit を workspace に統合 |
| #170 | version-sync 廃止（PR168 の plugin-update から委譲削除） |
| #172 | work-kit → workspace リネーム（PR168 のパス・namespace 全置換） |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| migrate-legacy-task-folders | PR1〜PR167 の旧構造タスクフォルダを新構造（{YYMMDD}_{title}/{branch}.md）に一括移行するスクリプトと移行作業 | 即時実施可（必要になった時点で） |
| dev-kit-plugin-update-skill | dev-kit に `plugin-update` スキルを追加（plugin-structure.md の必須化に追従） | 即時実施可 |
| claude-kit-plugin-update-skill | claude-kit に `plugin-update` スキルを追加（同上） | 即時実施可 |
| ref-inject-plugin-update-skill | ref-inject に `plugin-update` スキルを追加（同上） | 即時実施可 |
