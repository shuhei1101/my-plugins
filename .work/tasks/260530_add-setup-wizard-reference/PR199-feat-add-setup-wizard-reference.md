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
| - | `## QA` の未解決事項をユーザーに確認 | - |
| - | setup-wizard リファレンス本体を新規作成（テンプレート skeleton 付き） | - `plugins/claude-kit/references/setup-wizard.md`<br>- `plugins/claude-kit/references/setup-wizard.jp.md` |
| - | `plugin-structure.md` の「Required skills」セクションに `setup-wizard` を追加（`plugin-update` と並べる） | - `plugins/claude-kit/references/plugin-structure.md`<br>- `plugins/claude-kit/references/plugin-structure.jp.md` |
| - | references/index.yaml にエントリ追加（EN / JP 両方） | - `plugins/claude-kit/references/index.yaml`<br>- `plugins/claude-kit/references/index.jp.yaml` |
| - | injection_rules.yaml で `plugin.json` / `marketplace.json` 編集時に setup-wizard.md を required 注入 | - `plugins/claude-kit/references/injection_rules.yaml` |
| - | claude-kit バージョン bump（3.40.0 → 3.41.0）+ changelog 作成 | - `plugins/claude-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json`<br>- `plugins/claude-kit/changelogs/v3.41.0.md` |
| - | ノート作成（設計の経緯と決定事項を記録） | - `.work/notes/setup-wizard-pattern.md` |

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

**背景**: ユーザーは `.claude/{plugin}.local.md` の YAML frontmatter に `setup_done: true` を書き込む方針で合意済。ただし「再セットアップしたい」場合のフローも考える必要がある。

| 案 | 内容 |
|---|---|
| A | `setup_done: true` のみ。再実行は `/{plugin}:setup-wizard` を明示的に呼べばいい |
| B | `setup_done: true` + `setup_version: <plugin version>` を持たせ、バージョン更新時に自動再実行 |

**推奨方式**: A（最小構成）。バージョン更新時の再案内は別途 `plugin-update` 経由で対応すべきで、setup-wizard の責務を絞る。

**状態**: 未解決

**決定したら反映先**: `plugins/claude-kit/references/setup-wizard.md` の「Flag schema」セクション

### QA-002: setup-wizard が `plugin-config` を呼ぶ仕組み

**背景**: setup-wizard は env 設定を `plugin-config` 系スキルに委譲する設計。ただし、各プラグインが `plugin-config` 同等スキルを持つわけではないので、フォールバックが必要。

| 案 | 内容 |
|---|---|
| A | プラグインが env を持つなら、自身で `plugin-config` 相当のスキルを実装するのが必須（規約に明記） |
| B | claude-kit が汎用的な env 設定スキルを 1 つ提供し、各プラグインの env を読んで設定するアプローチ |
| C | `workspace/skills/config` が既に汎用的なので、setup-wizard からそれを呼ぶ前提にする |

**推奨方式**: C → A の二段。まずは `workspace/skills/config` が既存トグルを扱える前提で setup-wizard を書き、将来的に各プラグインが独自 config スキルを持つ余地を残す。

**状態**: 未解決

**決定したら反映先**: `plugins/claude-kit/references/setup-wizard.md` の「Env var setup delegation」セクション

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
| rollout-setup-wizard-to-existing-plugins | 既存プラグイン（work, claude-kit, dev-kit, etc.）に setup-wizard スキルを遡及追加。各プラグインの env / 初期設定を整理し、SessionStart フックも合わせて整備 | 「add-setup-wizard-reference」が完了したら |
