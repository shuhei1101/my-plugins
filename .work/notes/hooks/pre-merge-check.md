# pre-merge-check — マージ前2段階安全チェックフック

## 概要

`git merge <branch>` 実行前に、master取り込み確認とdry-runコンフリクト検証の2段階チェックを行うPreToolUseフック。
`git merge master/main`（上流取り込み）は対象外。`WORK_GUARD=false` で無効化可能。

## チェック内容

| No | チェック | 手段 | NG時の動作 |
| --- | --- | --- | --- |
| 1 | masterがブランチの祖先かどうか | `git merge-base --is-ancestor master <branch>` | ブロック（master取り込みを案内） |
| 2 | dry-runマージでコンフリクト有無 | `git merge --no-commit --no-ff <branch>` → `git merge --abort` | ブロック（コンフリクト詳細を表示） |

## フックの実行順序

1. master-commit-guard（直接コミットブロック）
2. pre-merge-check（このフック）
3. git-guard（マージ確認・ワンタイムトークン）

## 参考リンク

- `plugins/work/hooks/pre-merge-check.py`: フックスクリプト
- `plugins/work/hooks/pre-merge-check.md`: プロンプトMD
- `plugins/work/hooks/hooks.json`: フック登録
