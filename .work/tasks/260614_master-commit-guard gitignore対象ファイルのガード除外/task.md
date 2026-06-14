# master-commit-guard gitignore対象ファイルのガード除外

## 概要

master-commit-guard フックで、staged ファイルが全て `.gitignore` 対象の場合はブロックしないよう修正する。

## 作業内容

| 作業 | 完了 |
| ---- | ---- |
| `master-commit-guard.py` に gitignore チェックを追加 | 済 |

## 対象ファイル

- `plugins/work/hooks/master-commit-guard.py`
