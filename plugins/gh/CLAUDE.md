# gh プラグイン

GitHub Issues/Pull Request 上で作業フロー（スキャン・解決・自動マージ・レビュー）を回すためのプラグイン。

## セットアップ

| No | 手順 |
|---|---|
| 1 | https://github.com/settings/tokens で Personal Access Token を発行する（スコープ: `repo` / `read:org`）。Fine-grained PAT 推奨 |
| 2 | シェル起動ファイル（`~/.bashrc` 等）に `export GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxx` を追記 |
| 3 | Claude Code を再起動 |
| 4 | `/mcp` で `github` サーバーが connected になっているか確認 |

## 同梱の MCP サーバー

| No | サーバー | エンドポイント | 役割 |
|---|---|---|---|
| 1 | `github` | `https://api.githubcopilot.com/mcp/`（公式 Remote HTTP） | issue/PR/repo 全般。default toolsets（`context, repos, issues, pull_requests, users`） |

## スキル / サブエージェント早見表

| No | 種別 | 名前 | 概要 |
|---|---|---|---|
| 1 | スキル | `/gh:issue-scan` | コードベースを観点ごとにスキャンして GitHub Issue を起票 |
| 2 | 〃     | `/gh:issue-resolve` | 1 件の Issue を解決（ブランチ作成 → 実装 → PR 作成） |
| 3 | 〃     | `/gh:auto-merge` | レビュー OK の PR を直列でマージ |
| 4 | 〃     | `/gh:pr-review` | PR を観点別に AI レビューしコメント投稿 |
| 5 | サブエージェント | `issue-scanner` | `issue-scan` から観点単位で並列起動 |
| 6 | 〃               | `issue-resolver` | `issue-resolve` から 1 件の Issue 実装を担当 |
| 7 | 〃               | `auto-merger` | `auto-merge` から 1 PR ずつ直列で呼ばれる |
| 8 | 〃               | `pr-reviewer` | `pr-review` から観点単位で並列起動 |

## マージ直列化

`auto-merge` は **必ず 1 件ずつ** 処理し、並列起動しない（master 取り込みとマージの競合を避けるため）。並列実装は許容、並列マージは禁止。

## 前提

- リポジトリに GitHub remote（`origin` が github.com）があること
- work プラグインも有効化されていること（`/work:merge` のローカルマージ・ワークツリー後片付けに依存）
