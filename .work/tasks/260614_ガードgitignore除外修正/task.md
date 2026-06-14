# ガード gitignore 除外修正

## 概要

master-commit-guard に追加した不要な gitignore チェックを revert し、
protected-branch-guard に gitignore 対象ファイルの除外を追加する。

## 作業内容

| 作業 | 完了 |
| ---- | ---- |
| `master-commit-guard.py` の gitignore チェックを revert | 済 |
| `protected-branch-guard.py` に gitignore 対象ファイルの除外を追加 | 済 |
