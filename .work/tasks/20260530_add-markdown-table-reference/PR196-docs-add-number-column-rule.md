# PR196 — add-number-column-rule

## 概要

`markdown-table.md` および JP ミラー `markdown-table.jp.md` に、テーブルを作成する際は最左カラムにナンバーカラム（`#`）を設けるという規約を明文化する。

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | QA を `## QA` に記録する | - |
| - | ノートドキュメントを更新する | `.work/notes/` |
| - | ナンバーカラムルールを追加する | - `plugins/claude-kit/references/markdown-table.md`<br>- `plugins/claude-kit/references/markdown-table.jp.md` |
| - | ルール / CLAUDE.md を更新する | - |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/claude-kit/references/markdown-table.md` | 編集 | ナンバーカラムルールのセクションを追加 | - |
| `plugins/claude-kit/references/markdown-table.jp.md` | 編集 | 同上の JP ミラー | - |

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
| - | - | - |
