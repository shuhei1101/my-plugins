# 削除ガードフック追加

## 目的

`.git` ディレクトリと `.claude` 配下への削除操作を PreToolUse(Bash) フックでブロックする。

## 作業内容

| No | 作業 | 完了 |
| --- | --- | --- |
| 1 | `delete-guard.py` を作成 | 済 |
| 2 | `delete-guard.md` を作成（ブロックメッセージ） | 済 |
| 3 | `hooks.json` に登録 | 済 |
| 4 | バージョンアップ（plugin.json / marketplace.json） | 済 |

## 仕様

- 対象: `rm` / `rmdir` コマンドで `.git` または `.claude` を含むパスを操作しようとしたとき
- ブロック方針: 永久ブロック（ワンタイムトークンなし）。いかなる場合も削除させない
- env `WORK_GUARD=false` でも無効化しない（意図的に恒久ブロック）

## 参考ドキュメント

- [delete-guard ノート](../../notes/hooks/delete-guard.md)
