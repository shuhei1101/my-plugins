# PR216 — fix-setup-wizard-config-naming

## 概要

`claude-kit/references/setup-wizard.md` / `setup-wizard.jp.md` の2点を修正する。

1. **命名修正**: `plugin-config` スキルの命名が不要になり、単に `config` になった。
   `plugin-update` は引き続き `plugin-update` のまま（変更しない）。
2. **JP ミラーのスケルトン日本語化**: JP ミラー（setup-wizard.jp.md）の skeleton（コピー用）セクションの
   英語版 description frontmatter とステップタイトルを日本語に書き直す。
   英語版（setup-wizard.md）は英語のまま維持する。

ベースブランチ: `PR199/feat/add-setup-wizard-reference`（setup-wizard ファイルが存在するブランチ）

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA を `## QA` に記録する | - |
| 済 | ノートドキュメントを更新する（対象なし） | `.work/notes/` |
| 済 | `setup-wizard.jp.md` の `plugin-config` をすべて `config` に変更（`plugin-update` は除く） | `plugins/claude-kit/references/setup-wizard.jp.md` |
| 済 | `setup-wizard.jp.md` の skeleton セクションを日本語化 | `plugins/claude-kit/references/setup-wizard.jp.md` |
| 済 | `setup-wizard.md` の `plugin-config` をすべて `config` に変更（`plugin-update` は除く） | `plugins/claude-kit/references/setup-wizard.md` |
| - | ルール / CLAUDE.md を更新する（対象なし） | - |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/claude-kit/references/setup-wizard.jp.md` | 編集 | plugin-config → config、skeleton 日本語化 | - |
| `plugins/claude-kit/references/setup-wizard.md` | 編集 | plugin-config → config | skeleton は英語維持 |

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| - | - | テスト対象なし | - |

## QA

なし

## 参考ドキュメント

- `plugins/claude-kit/references/setup-wizard.jp.md`: 修正対象ファイル（JP ミラー）
- `plugins/claude-kit/references/setup-wizard.md`: 修正対象ファイル（英語版）

## 関連PR

| PR番号 | 概要 |
|---|---|
| PR199/feat/add-setup-wizard-reference | setup-wizard リファレンス追加（本PRのベース） |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |
