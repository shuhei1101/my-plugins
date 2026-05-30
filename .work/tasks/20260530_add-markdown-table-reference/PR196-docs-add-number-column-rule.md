# PR196 — add-number-column-rule

## 概要

`markdown-table.md` および JP ミラー `markdown-table.jp.md` に、テーブルを作成する際は最左カラムにナンバーカラム（`#`）を設けるという規約を明文化する。

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA を `## QA` に記録する | - |
| 済 | ノートドキュメントを更新する（対象なし） | `.work/notes/` |
| 済 | ナンバーカラムルールを追加する（初版） | - `plugins/claude-kit/references/markdown-table.md`<br>- `plugins/claude-kit/references/markdown-table.jp.md` |
| - | `#` カラムはすべての行で必須（空白禁止）に修正する | 上記2ファイル |
| - | markdown-table を dev-kit へ移動する | - `plugins/dev-kit/references/markdown/markdown-table.md`（新規）<br>- `plugins/dev-kit/references/markdown/markdown-table.jp.md`（新規）<br>- `plugins/claude-kit/references/markdown-table.md`（削除）<br>- `plugins/claude-kit/references/markdown-table.jp.md`（削除） |
| - | injection_rules / index を更新する | - `plugins/claude-kit/references/injection_rules.yaml`<br>- `plugins/claude-kit/references/index.yaml`<br>- `plugins/claude-kit/references/index.jp.yaml`<br>- `plugins/dev-kit/references/injection_rules.yaml`<br>- `plugins/dev-kit/references/index.yaml`<br>- `plugins/dev-kit/references/index.jp.yaml` |
| - | プラグインバージョンをバンプする | - `plugins/claude-kit/.claude-plugin/plugin.json`<br>- `plugins/dev-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |
| - | ルール / CLAUDE.md を更新する（対象なし） | - |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/dev-kit/references/markdown/markdown-table.md` | 新規 | 移動先ファイル（#修正・ルール整理済み） | claude-kit から移動 |
| `plugins/dev-kit/references/markdown/markdown-table.jp.md` | 新規 | 同上の JP ミラー | - |
| `plugins/claude-kit/references/markdown-table.md` | 削除 | dev-kit へ移動 | - |
| `plugins/claude-kit/references/markdown-table.jp.md` | 削除 | dev-kit へ移動 | - |
| `plugins/claude-kit/references/injection_rules.yaml` | 編集 | `**/*.md` → markdown-table のルールを削除 | - |
| `plugins/claude-kit/references/index.yaml` | 編集 | markdown-table エントリを削除 | - |
| `plugins/claude-kit/references/index.jp.yaml` | 編集 | markdown-table エントリを削除 | - |
| `plugins/dev-kit/references/injection_rules.yaml` | 編集 | `**/*.md` → `markdown/markdown-table.md` のルールを追加 | - |
| `plugins/dev-kit/references/index.yaml` | 編集 | markdown-table エントリを追加 | - |
| `plugins/dev-kit/references/index.jp.yaml` | 編集 | markdown-table エントリを追加 | - |
| `plugins/claude-kit/.claude-plugin/plugin.json` | 編集 | 3.40.0 → 3.41.0 | MINOR: reference 削除 |
| `plugins/dev-kit/.claude-plugin/plugin.json` | 編集 | 4.1.0 → 4.2.0 | MINOR: markdown カテゴリ追加 |
| `.claude-plugin/marketplace.json` | 編集 | 両プラグインのバージョンをバンプ | - |

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| - | - | テスト対象なし | - |

## QA

なし

## 参考ドキュメント

- `plugins/claude-kit/references/markdown-table.md`: 既存のMarkdownテーブル規約

## 関連PR

| PR番号 | 概要 |
|---|---|
| #178 | markdown-table reference を追加した元PR |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| dev-kit-references-yaml-subfolder | dev-kit references の `yaml.md` / `yaml.jp.md` を `yaml/` サブフォルダへ移動し、他言語（html/next/python）と構造を揃える | 即時実施可 |
