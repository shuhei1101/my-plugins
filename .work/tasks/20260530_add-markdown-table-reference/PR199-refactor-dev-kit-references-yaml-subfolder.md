# PR199 — dev-kit-references-yaml-subfolder

## 概要

`dev-kit/references/` の `yaml.md` と `yaml.jp.md` を `yaml/` サブフォルダへ移動し、
`html/`・`next/`・`python/`・`markdown/` と同じ構造に揃える。

**背景（PR196 より）:**
PR196 で `markdown-table.md` を `dev-kit/references/markdown/` サブフォルダへ移動した。
この時点で `yaml.md` / `yaml.jp.md` だけがルートに残り、構造が不揃いになった。
PR196 の次PR候補として記録済みの作業。

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | QA を `## QA` に記録する | - |
| - | ノートドキュメントを更新する（対象なし） | `.work/notes/` |
| - | `yaml/` サブフォルダを作成して yaml.md / yaml.jp.md を移動する | - `plugins/dev-kit/references/yaml/yaml.md`（新規）<br>- `plugins/dev-kit/references/yaml/yaml.jp.md`（新規）<br>- `plugins/dev-kit/references/yaml.md`（削除）<br>- `plugins/dev-kit/references/yaml.jp.md`（削除） |
| - | `_injection_rules.yaml` のパスを更新する | `plugins/dev-kit/references/_injection_rules.yaml` |
| - | `_index.yaml` / `_index.jp.yaml` のパスを更新する | - `plugins/dev-kit/references/_index.yaml`<br>- `plugins/dev-kit/references/_index.jp.yaml` |
| - | dev-kit CLAUDE.md の Reference structure と Changelog を更新する | `plugins/dev-kit/CLAUDE.md` |
| - | プラグインバージョンをバンプする | - `plugins/dev-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |
| - | ルール / CLAUDE.md を更新する（対象なし） | - |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/dev-kit/references/yaml/yaml.md` | 新規 | 移動先ファイル | ルートから移動 |
| `plugins/dev-kit/references/yaml/yaml.jp.md` | 新規 | 同上の JP ミラー | - |
| `plugins/dev-kit/references/yaml.md` | 削除 | yaml/ サブフォルダへ移動 | - |
| `plugins/dev-kit/references/yaml.jp.md` | 削除 | yaml/ サブフォルダへ移動 | - |
| `plugins/dev-kit/references/_injection_rules.yaml` | 編集 | yaml パスを `yaml/yaml.md` に更新 | - |
| `plugins/dev-kit/references/_index.yaml` | 編集 | yaml パスを更新 | - |
| `plugins/dev-kit/references/_index.jp.yaml` | 編集 | yaml パスを更新 | - |
| `plugins/dev-kit/CLAUDE.md` | 編集 | Reference structure と Changelog を更新 | 4.4.0 → 4.5.0 |
| `plugins/dev-kit/.claude-plugin/plugin.json` | 編集 | 4.4.0 → 4.5.0 | MINOR: 構造変更 |
| `.claude-plugin/marketplace.json` | 編集 | dev-kit バージョンをバンプ | - |

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| - | - | テスト対象なし | - |

## QA

なし

## 参考ドキュメント

- `.work/tasks/20260530_add-markdown-table-reference/PR196-docs-add-number-column-rule.md`: 前回PR（yaml サブフォルダ化の動機）

## 関連PR

| PR番号 | 概要 |
|---|---|
| #196 | markdown-table を dev-kit/markdown/ へ移動（本PRの前提） |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |
