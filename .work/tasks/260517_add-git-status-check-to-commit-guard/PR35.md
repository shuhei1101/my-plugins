# PR35 — add-git-status-check-to-commit-guard

## 概要

`master-commit-guard` フックで確認を求める前に、`git status` で実際に変更があるかどうかを確認する注記を追加する。
変更がない場合はコミット不要なので、ユーザーに確認せずスキップすべきだという注意書きを重要ルールに加える。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | 重要ルールに「確認前に git status で変更の有無を確認する」注記を追加 | - `plugins/work-kit/hooks/prompts/master-commit-guard.jp.md`<br>- `plugins/work-kit/hooks/prompts/master-commit-guard.md` |

## 参考ドキュメント

- `plugins/work-kit/hooks/prompts/master-commit-guard.md`: 対象フックファイル（英語）
- `plugins/work-kit/hooks/prompts/master-commit-guard.jp.md`: 対象フックファイル（日本語ミラー）

## QA

なし
