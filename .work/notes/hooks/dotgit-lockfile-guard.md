# dotgit-lockfile-guard — .git / lock ファイル Edit-Write 永久ブロック

## 概要

`.git/**` 配下、および主要パッケージマネージャの lock ファイルへの Edit / Write を永久ブロックする
PreToolUse(Edit|Write) フック。Read はガードしない。
ワンタイムトークンなし — 再実行しても通らない。

Bash 経由の削除は `delete-guard` がカバー（lock ファイル名は両フックで共有）。

## 保護対象

| No | パス | 理由 |
| --- | --- | --- |
| 1 | `.git/**`（パス成分に `.git` を含む） | Git 内部状態。直接編集すると壊れる |
| 2 | `package-lock.json` / `npm-shrinkwrap.json` | npm |
| 3 | `yarn.lock` | yarn |
| 4 | `pnpm-lock.yaml` | pnpm |
| 5 | `Cargo.lock` | cargo |
| 6 | `Gemfile.lock` | bundler |
| 7 | `Pipfile.lock` | pipenv |
| 8 | `poetry.lock` | poetry |
| 9 | `uv.lock` | uv |
| 10 | `composer.lock` | composer |
| 11 | `go.sum` | go modules |

## 仕様

- トリガー: `tool_input.file_path` のパスが保護対象に一致
- 判定: `.git` はパス成分（`/`/`\` 区切り）に含まれるか、lock は basename 完全一致
- 出力: `hookSpecificOutput.permissionDecision = "deny"`
- ブロック解除手段なし（env トグルも設けていない）
- Read はガードしない（`.git/HEAD` 等の参照は許可）

## 参考リンク

- `plugins/work/hooks/dotgit-lockfile-guard.py`: フックスクリプト本体
- `plugins/work/hooks/dotgit-lockfile-guard.md`: ブロック時のユーザー向けメッセージ
- `.work/notes/hooks/delete-guard.md`: Bash 経路の対となる削除ガード
