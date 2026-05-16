# PR16 — add-upgrade-command

## 概要

`tools/marketplace.py` に `upgrade` コマンドを追加する。
メインマーケットプレイスからインストール済みのプラグイン（ユーザー・プロジェクトスコープ両方）を全て最新バージョンに更新する。
未インストールのプラグインを新たにインストールすることはしない。スコープの変更もしない。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | `cmd_upgrade()` 関数を追加（メインマーケットプレイスキャッシュ更新 → インストール済みプラグインのみ更新） | - `tools/marketplace.py` |
| 済 | `parse_args()` に `upgrade` サブコマンドを追加 | - `tools/marketplace.py` |
| 済 | `main()` に `upgrade` コマンドの分岐を追加 | - `tools/marketplace.py` |
| 済 | docstring の Usage に `upgrade` の使い方を追記 | - `tools/marketplace.py` |

## 参考ドキュメント

- なし
