# PR199 — add-setup-wizard-reference

## 概要

新規プラグイン作成時に **`setup-wizard` スキルの実装を必須化** するため、claude-kit に専用リファレンスを追加する。

**背景**:

- 各プラグインは独自の env トグル・初期設定を持つが、ユーザーが初回利用時にそれを知る術がない（CLAUDE.md を能動的に読む必要がある）
- 既に `plugin-update` を「必須スキル」として規約化している前例があるので、同じパターンで `setup-wizard` を追加する
- 実装の中身（SessionStart フック + `.local.md` の `setup_done` フラグ + AskUserQuestion ベースの対話設定）は本 PR ではドキュメント化のみ。実プラグインへの組み込みは次 PR で別途行う

**設計サマリ**:

- フラグ保存先: `.claude/{plugin}.local.md` の YAML frontmatter（既存の `plugin-settings` の仕組みを再利用）
- フックタイミング: `SessionStart`（各プラグインが個別に持つ — `plugin-update` と同じ自律性）
- setup-wizard の役割: ユースケース別オンボーディングの **目次役**（本文は CLAUDE.md）。env 設定は `plugin-config` 系スキルへ委譲
- AskUserQuestion の制約: options は 2〜4 個（公式 schema で確認済 — `minItems: 2`, `maxItems: 4`, "Other" は自動付与）

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | `## QA` の未解決事項をユーザーに確認 | - |
| 済 | setup-wizard リファレンス本体を新規作成（テンプレート skeleton 付き） | - `plugins/claude-kit/references/setup-wizard.md`<br>- `plugins/claude-kit/references/setup-wizard.jp.md` |
| 済 | `plugin-structure.md` の「Required skills」セクションに `setup-wizard` + `plugin-config` を追加 | - `plugins/claude-kit/references/plugin-structure.md`<br>- `plugins/claude-kit/references/plugin-structure.jp.md` |
| 済 | references/index.yaml にエントリ追加（EN / JP 両方） | - `plugins/claude-kit/references/index.yaml`<br>- `plugins/claude-kit/references/index.jp.yaml` |
| 済 | injection_rules.yaml で `plugin.json` / `marketplace.json` 編集時に setup-wizard.md を required 注入 | - `plugins/claude-kit/references/injection_rules.yaml` |
| 済 | claude-kit バージョン bump（3.40.0 → 3.41.0）+ changelog 作成 | - `plugins/claude-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json`<br>- `plugins/claude-kit/changelogs/v3.41.0.md` |
| 済 | ノート作成（設計の経緯と決定事項を記録） | - `.work/notes/setup-wizard-pattern.md` |
| 済 | `plugin-config` スキル名を `config` に修正（setup-wizard.md / plugin-structure.md 等） | - `plugins/claude-kit/references/setup-wizard.md`<br>- `plugins/claude-kit/references/setup-wizard.jp.md`<br>- `plugins/claude-kit/references/plugin-structure.md`<br>- `plugins/claude-kit/references/plugin-structure.jp.md`<br>- `plugins/claude-kit/references/index.yaml`<br>- `plugins/claude-kit/references/index.jp.yaml` |

## 変更内容

実装したファイル（テスト以外）。コミットに積まれる全ファイルを列挙する。

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/claude-kit/references/setup-wizard.md` | 新規 | setup-wizard スキルの執筆ガイド（責務 / フック構成 / フラグ管理 / skeleton） | - |
| `plugins/claude-kit/references/setup-wizard.jp.md` | 新規 | JP ミラー | - |
| `plugins/claude-kit/references/plugin-structure.md` | 編集 | Required skills に `setup-wizard` を追加 | - |
| `plugins/claude-kit/references/plugin-structure.jp.md` | 編集 | JP ミラー同期 | - |
| `plugins/claude-kit/references/index.yaml` | 編集 | setup-wizard.md のエントリ追加 | - |
| `plugins/claude-kit/references/index.jp.yaml` | 編集 | JP ミラー同期 | - |
| `plugins/claude-kit/references/injection_rules.yaml` | 編集 | plugin.json / marketplace.json 編集時 setup-wizard.md を注入 | - |
| `plugins/claude-kit/.claude-plugin/plugin.json` | 編集 | バージョン bump 3.40.0 → 3.41.0 | MINOR（新リファレンス追加） |
| `.claude-plugin/marketplace.json` | 編集 | claude-kit バージョン同期 | - |
| `plugins/claude-kit/changelogs/v3.41.0.md` | 新規 | changelog | - |

## テスト

このリポジトリのリファレンスは静的ドキュメントのため、テストファイルの追加・変更はなし。

## QA

PR スコープの未決定事項を QA-XXX として記録する。決定後は本文の該当箇所に反映する。

### QA-001: setup-wizard 完了時に「セットアップ済み」マークをどこに記録するか

**決定**: 案 A（`setup_done: true` のみ。version 情報は持たせない）

加えて、`plugin-structure.md` に「プラグインを更新する際は setup-wizard も必ず合わせて更新する」旨を明記する。バージョン追従は規約で人間に守らせる方針。

**反映先**: `plugins/claude-kit/references/setup-wizard.md` の Flag schema、`plugin-structure.md` の Required skills

### QA-002: setup-wizard が `plugin-config` を呼ぶ仕組み

**決定**: 案 A（プラグインが env を持つなら、自身で `plugin-config` 相当のスキルを実装するのが必須。規約に明記）

加えて、`workspace/skills/config` を `workspace/skills/plugin-config` にリネームする方針。これは別 PR として予約。

**反映先**: `plugins/claude-kit/references/setup-wizard.md` の Env var setup delegation、`plugin-structure.md` の Required skills（plugin-config も必須スキルに追加）

## 参考ドキュメント

- `.work/notes/setup-wizard-pattern.md`: 本 PR の設計経緯と決定事項
- `.work/notes/plugin-config-skill.md`: 既存の plugin-config（現 `workspace:config`）スキル設計メモ
- `plugins/claude-kit/references/plugin-structure.md`: 既存「Required skills」セクション（`plugin-update`）の前例

## 関連PR

| PR番号 | 概要 |
|---|---|
| - | （直接の関連 PR なし） |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| document-askuserquestion-limits | AskUserQuestion の制約（options 2〜4 個、"Other" 自動付与、multiSelect、preview）を claude-kit リファレンスに正式に明記。本 PR では setup-wizard.md 内に最小限触れるが、汎用リファレンスとして独立させる | 即時実施可 |
| rename-workspace-config-to-plugin-config | `plugins/workspace/skills/config` を `plugins/workspace/skills/plugin-config` にリネーム。setup-wizard が委譲する命名を `plugin-config` に統一するため | 「add-setup-wizard-reference」が完了したら |
| rollout-setup-wizard-to-existing-plugins | 既存プラグイン（work, claude-kit, dev-kit, etc.）に setup-wizard スキルを遡及追加。各プラグインの env / 初期設定を整理し、SessionStart フックも合わせて整備 | 「rename-workspace-config-to-plugin-config」が完了したら |
