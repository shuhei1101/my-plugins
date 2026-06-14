# 削除ガードフック追加

## 目的

`.git` ディレクトリと `.claude` 配下への削除操作を PreToolUse(Bash) フックでブロックする。

## 作業内容

| No | 作業 | 完了 |
| --- | --- | --- |
| 1 | `delete-guard.py` を作成 | 未 |
| 2 | `delete-guard.md` を作成（ブロックメッセージ） | 未 |
| 3 | `hooks.json` に登録 | 未 |
| 4 | バージョンアップ（plugin.json / marketplace.json） | 未 |

## 仕様

- 対象: `rm` / `rmdir` コマンドで `.git` または `.claude` を含むパスを操作しようとしたとき
- ブロック方針: 永久ブロック（ワンタイムトークンなし）。いかなる場合も削除させない
- env `WORK_GUARD=false` でも無効化しない（意図的に恒久ブロック）

## 参考ドキュメント
