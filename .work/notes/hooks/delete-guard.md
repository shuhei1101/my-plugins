# delete-guard — 重要ファイル削除ブロックフック

## 概要

`rm` / `rmdir` で重要ファイル/ディレクトリを削除しようとしたとき、永久にブロックする PreToolUse(Bash) フック。
ワンタイムトークンなし — 再実行しても通らない。

## 保護対象

| No | パス | 理由 |
| --- | --- | --- |
| 1 | `.git` ディレクトリ | リポジトリ管理に不可欠 |
| 2 | `.claude` ディレクトリ | 設定・ルール・プラグインキャッシュ |
| 3 | `.gitignore` | 消失すると build artifacts / node_modules が tracked 扱いになる |
| 4 | `.gitattributes` | マージドライバや改行設定が失われる |

## 仕様

- トリガー: `rm` / `rmdir` を含む Bash コマンドに保護対象がパスコンポーネントとして登場
- 除外: `.gitlab-ci.yml` など `.git` の直後に英数字が続くパスは対象外
- ブロック解除手段なし（env トグルも設けていない）

## 検出ロジック

1. `\b(?:rm|rmdir)\b` でコマンドに削除操作が含まれるか確認
2. 保護対象パターンが含まれるか確認（ディレクトリは末尾区切り、ファイルは完全一致）
3. 両方ヒット → `decision: block`

## 参考リンク

- `plugins/work/hooks/delete-guard.py`: フックスクリプト本体
- `plugins/work/hooks/delete-guard.md`: ブロック時のユーザー向けメッセージ
