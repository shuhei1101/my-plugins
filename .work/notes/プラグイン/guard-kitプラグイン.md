# guard-kit プラグイン — ローカル Git 保護フック群

## 概要

ローカル Git 操作に対するガード群を提供する最小プラグイン。master 直接コミット阻止、危険 git コマンド阻止、`.git/` と lock ファイルの保護、削除検知、セッション開始時の規約注入。ワークツリー操作（`worktree_create` / `worktree_remove` MCP、pre-merge-check hook）は gh-kit プラグインに統合されている。

## バージョン

| バージョン | 主な変更 |
|---|---|
| 1.0 | 旧 work（v2.3）から保護フックだけを切り出した新規プラグイン。`work` プラグイン自体は v3.0 として再構築され、start/merge スキル + worktree MCP + start_reminder / merge_reminder / pre-merge-check / task_reminder を担当 |

## フック一覧

| No | フック | イベント | 役割 |
|---|---|---|---|
| 1 | `inject_rules` | PreToolUse(Edit/Write/Read) | rules/ 配下の .md ルールを自動注入 |
| 2 | `protected-branch-guard` | PreToolUse(Edit/Write) | 保護ブランチでの Edit/Write を阻止し `worktree_create` MCP の利用を促す |
| 3 | `dotgit-lockfile-guard` | PreToolUse(Edit/Write) | `.git/**` と各種 lock ファイルの編集を永久ブロック |
| 4 | `delete-guard` | PreToolUse(Bash) | `.git` / `.claude` / `.gitignore` 等の削除操作をブロック |
| 5 | `dangerous-git-guard` | PreToolUse(Bash) | `-X ours/theirs` / `git rm` 重要ファイル等の危険操作を永久ブロック |
| 6 | `master-commit-guard` | PreToolUse(Bash) | 保護ブランチへの直接コミット (`git add`/`git commit`) をブロック |
| 7 | `git-guard` | PreToolUse(Bash) | `git push` / `git merge` 実行時に確認を挟む |
| 8 | `session_start` | SessionStart | プロジェクト規約を Jinja2 でレンダリングして注入 |
| 9 | `post-commit-deletion-check` | Stop | 直近コミットで N 件超の削除があれば警告を注入 |
| 10 | `reload_deferred` | Stop | 保留中の `/reload-plugins` を自セッションへ遅延送信 |
| 11 | `clear_session_token` | PreCompact | コンパクション前に dev-kit / guard-kit の rules トークンを削除 |

## 環境変数

| 変数 | 用途 |
|---|---|
| `GUARD_KIT_GUARD` | `false` で `git-guard` を無効化 |
| `GUARD_KIT_ALLOW_MASTER_COMMIT` | `true` で `master-commit-guard` を通過させる（例外作業用） |
| `GUARD_KIT_BRANCH_ENFORCEMENT` | `false` で session_start の作業フロー注入を簡略化 |
| `GUARD_KIT_PROTECTED_BRANCHES` | カンマ区切りで保護対象ブランチを上書き（既定: `master,main,develop`） |

## トークンパス

| パス | 用途 |
|---|---|
| `~/.claude/tokens/guard-kit/rules/<session>.json` | inject_rules の注入済みルール記録 |
| `~/.claude/tokens/guard-kit/reload-pending/<tmux>` | reload_deferred の保留情報 |

## 参考リンク

- `plugins/guard-kit/CLAUDE.md`: 同梱ドキュメント
- `plugins/guard-kit/hooks/hooks.json`: フック登録設定
- `plugins/guard-kit/scripts/_branch_guard.py`: 保護ブランチ実行ガードの共通ヘルパー
