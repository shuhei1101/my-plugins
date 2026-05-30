# PR209 — docs-commit-bundle-pr-doc

## 概要

コミット時に PR ドキュメント（`## 作業内容` の `済` 更新・`## 変更内容` への列挙）を
実装コミットと同じコミットにまとめる規約を `templates/.work/CLAUDE.md` に追記する。

現状、実装コミット後に別コミットで PR ドキュメントを更新するケースがあり、
コミット粒度が細かくなりすぎる問題がある。

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | `templates/.work/CLAUDE.jp.md` の規約セクションに規約を追記 | - `plugins/work/templates/.work/CLAUDE.jp.md` |
| 済 | `templates/.work/CLAUDE.md` の規約セクションに規約を追記（JP ミラー後に反映） | - `plugins/work/templates/.work/CLAUDE.md` |

## 変更内容

実装したファイル（テスト以外）。コミットに積まれる全ファイルを列挙する。

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/work/templates/.work/CLAUDE.jp.md` | 編集 | コミットバンドル規約を追記 | - |
| `plugins/work/templates/.work/CLAUDE.md` | 編集 | コミットバンドル規約を追記 | - |

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|

## QA

特になし

## 参考ドキュメント

## 関連イシュー

## 関連PR

| PR番号 | 概要 |
|---|---|

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
