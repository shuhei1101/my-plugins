# delete-guard — .git / .claude 削除ブロックフック

## 概要

`rm` / `rmdir` で `.git` または `.claude` ディレクトリを削除しようとしたとき、永久にブロックする PreToolUse(Bash) フック。
ワンタイムトークンなし — 再実行しても通らない。

## 仕様

- トリガー: `rm` / `rmdir` を含む Bash コマンドに `.git` または `.claude` がパスコンポーネントとして登場
- 除外: `.gitignore` など `.git`/`.claude` の後に英数字が続くパスは対象外
- ブロック解除手段なし（env トグルも設けていない）

## 検出ロジック

1. `\b(?:rm|rmdir)\b` でコマンドに削除操作が含まれるか確認
2. `(?:^|[\s/\"\'\\])\.(?:git|claude)(?:[/\s\"\'\\]|$)` で保護対象パスが含まれるか確認
3. 両方ヒット → `decision: block`

## 参考リンク

- `plugins/work/hooks/delete-guard.py`: フックスクリプト本体
- `plugins/work/hooks/delete-guard.md`: ブロック時のユーザー向けメッセージ
