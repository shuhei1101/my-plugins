# dangerous-git-guard — 危険な git コマンドのブロックフック

## 概要

事故誘発につながる git コマンドを PreToolUse(Bash) で永久ブロックする。
ワンタイムトークンなし — 再実行しても通らない。

## 検出対象

| No | パターン | ブロック理由 |
| --- | --- | --- |
| 1 | `git worktree remove --force` / `-f` | 作業中ワークツリーを強制削除して in-progress 作業が消える |
| 2 | `git rm` で `.gitignore` / `.gitattributes` / `.claude/` | 重要ファイルの追跡削除 |
| 3 | `git checkout/restore` で同上 | 重要ファイルの上書き復元 |
| 4 | `git merge -X ours/theirs` / `--strategy-option=ours/theirs` | 自動コンフリクト解消 — master 側追加ファイル誤削除の原因 |
| 5 | `git checkout/merge --ours/--theirs` | 同上 |

## 設計上のポイント

- 先頭ドットファイル（`.gitignore`）の検出は `\b` ではなく `(?:\s|/|^)` を使う（`\b` は `.` の前で単語境界が成立しないため）
- `decision: block` で完全ブロック、env トグルも設けない

## 参考リンク

- `plugins/work/hooks/dangerous-git-guard.py`: フックスクリプト本体
- `plugins/work/hooks/dangerous-git-guard.md`: ブロック時のユーザー向けメッセージ
