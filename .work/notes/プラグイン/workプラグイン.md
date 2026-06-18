# work プラグイン — ワークツリー駆動のブランチ作業基盤

## 概要

ワークツリーでブランチ作業を行うための最小限の基盤プラグイン。`/work:start` でブランチ + worktree を作り、実装を進め、`/work:merge` で親に取り込む。タスクドキュメント・タスクインデックス・ローカルイシュー管理は v2.0 で全廃止され、それらは gh プラグイン経由で GitHub Issues/PR として扱う。

## バージョン

| バージョン | 主な変更 |
|---|---|
| 1.x | タスク + ローカルイシュー管理を含むフル機能 |
| 2.0 | タスク/イシュー機能を全廃止。`/work:start` `/work:merge` `/work:setup` + 保護フック群に縮小 |

## スキル一覧

| No | スキル | 概要 |
|---|---|---|
| 1 | `/work:start` | ブランチ + worktree 作成、実装開始 |
| 2 | `/work:merge` | 親取り込み + コンフリクト処理 + マージ + worktree 削除 |
| 3 | `/work:setup` | `.work/notes/` を初期化 |

## MCP ツール

| ツール | 用途 |
|---|---|
| `worktree_create` | ブランチ `{type}/{title}` + worktree 作成 + Stop リマインダー用セッショントークン書き込み |
| `worktree_remove` | マージ済みブランチの worktree + ブランチ + セッショントークンを削除 |

## フック群（残存）

| No | フック | 役割 |
|---|---|---|
| 1 | `dangerous-git-guard` | `-X ours/theirs` / `git rm` 重要ファイル / `worktree remove --force` 等を永久ブロック |
| 2 | `master-commit-guard` | 保護ブランチへの直接コミットをブロック |
| 3 | `protected-branch-guard` | 保護ブランチでの Edit/Write をブロック |
| 4 | `delete-guard` | `.git` / `.claude` / `.gitignore` / lock ファイル削除をブロック |
| 5 | `dotgit-lockfile-guard` | `.git/**` と lock ファイルの Edit/Write をブロック |
| 6 | `pre-merge-check` | マージ前の master 取り込み + dry-run コンフリクト検証 |
| 7 | `git-guard` | `git push` / `git merge` 実行時に確認を挟む |
| 8 | `post-commit-deletion-check` | 直近コミットで N 件超の削除を検知したら警告を注入 |
| 9 | `worktree-base-ref`（worktree-tool.py 内） | worktree 作成時 base ref を `origin/<current>` に強制 |
| 10 | `inject_rules` | PreToolUse でファイル系ルールを自動注入 |
| 11 | `session_start` | セッション開始時に「やってはいけないこと」を注入 |

## 廃止された機能（v2.0）

| 廃止対象 | 移管先 |
|---|---|
| タスクドキュメント (`*.task.md`) / タスクインデックス (`tasks/index.yaml`) | 廃止（GitHub PR 本文で代替） |
| ローカルイシュー (`.work/issues/*.md`) | gh プラグインの GitHub Issues |
| `/work:issue-scan` / `issue-review` / `issue-create` / `issue-resolve` / `issue-resolve-auto` | gh プラグインの対応スキル |
| `/work:impl-review` | gh プラグインの `/gh:pr-review-auto`（PR diff レビュー） |
| `/work:branch-blank-work` / `branch-index-cleanup` / `branch-reserve` | 廃止 |
| MCP ツール `index_*` / `issue_*` | 廃止 |
| `issue-resolver` / `issue-scanner` / `branch-blank-worker` サブエージェント | gh プラグイン側に再構築 |

## ディレクトリ構成

```txt
.work/
└── notes/
    ├── _index.md
    └── {カテゴリ}/{topic}.md
```

## 参考リンク

- `plugins/work/CLAUDE.md`: 同梱ドキュメント
- `plugins/work/skills/`: `start` / `merge` / `setup` の SKILL.md
- `plugins/work/hooks/`: 保護フック群
- `plugins/work/mcp/server.py`: `worktree_create` / `worktree_remove` の MCP 定義
