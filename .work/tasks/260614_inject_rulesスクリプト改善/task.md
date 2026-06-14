# inject_rules スクリプト改善

## 概要

`inject_rules.py`（dev-kit / work プラグイン共通）の3件修正。

## 作業内容

| No | 項目 | 内容 | 完了 |
| -- | ---- | ---- | ---- |
| 1 | 進捗表示の統一 | 1万文字に収まる場合でも「N/M ファイル」を表示する（現状は超過時のみ表示） | 済 |
| 2 | 大ファイル分割読み込み | 1件で1万文字超えるときトークンにオフセットを保存し、次回呼び出しで続きを読む | 済 |
| 3 | TOKEN_DIR バグ修正 | work版が `tokens/dev-kit/rules/` を参照しているのを `tokens/work/rules/` に修正 | 済 |

## 対象ファイル

| No | ファイル | 変更内容 |
| -- | -------- | -------- |
| 1 | `plugins/work/hooks/inject_rules.py` | 上記 1〜3 |
| 2 | `plugins/dev-kit/hooks/inject_rules.py` | 上記 1〜2（TOKEN_DIR は dev-kit のまま） |
| 3 | `plugins/work/hooks/inject_message.j2` | 進捗表示の統一（常に件数表示） |
| 4 | `plugins/dev-kit/hooks/inject_message.j2` | 〃 |

## QA

なし

## 参考ドキュメント

- [inject_rules注入ロジック](.work/notes/hooks/inject_rules注入ロジック.md): inject_rules.py の現在の動作仕様
