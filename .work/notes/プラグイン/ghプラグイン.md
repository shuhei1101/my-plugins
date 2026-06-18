# gh プラグイン — GitHub Issues/PR ベースの作業フロー

## 概要

GitHub 公式 MCP サーバー（Remote HTTP）を `.mcp.json` で同梱し、Issues / Pull Request を中心に作業を回すためのスキルとサブエージェントを提供するプラグイン。マージは `pr-review-auto` 1 経路に集約し、`pr-reviewer` を直列起動することで master 取り込み競合を構造的に防ぐ。

## セットアップ

| No | 手順 |
|---|---|
| 1 | https://github.com/settings/tokens で PAT 発行（`repo` / `read:org`） |
| 2 | `~/.bashrc` 等に `export GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxx` を追記 |
| 3 | Claude Code 再起動後 `/mcp` で `github` サーバーが connected か確認 |

## 同梱の MCP サーバー

| サーバー | エンドポイント | 役割 |
|---|---|---|
| `github` | `https://api.githubcopilot.com/mcp/` | 公式 Remote HTTP。default toolsets（`context, repos, issues, pull_requests, users`） |

## スキル一覧

| No | スキル | 概要 |
|---|---|---|
| 1 | `/gh:issue-scan` | 観点を N 件選び `issue-scanner` を並列起動 → findings を `create_issue` で起票 |
| 2 | `/gh:issue-resolve` | 1 Issue を `issue-resolver` に渡して PR 作成まで |
| 3 | `/gh:issue-resolve-auto` | `auto-resolve` ラベルの Issue を上から N 件並列で `issue-resolver` に渡す（PR 作成まで） |
| 4 | `/gh:pr-review-auto` | `auto-review` ラベルの PR を 1 件ずつ直列で `pr-reviewer` に渡す（マージまで） |

## サブエージェント一覧

| No | エージェント | 呼び元 | 役割 |
|---|---|---|---|
| 1 | `issue-scanner` | `/gh:issue-scan` | 1 観点でファイル走査し findings を返す（GitHub 操作はメインが担当） |
| 2 | `issue-resolver` | `/gh:issue-resolve` / `/gh:issue-resolve-auto` | `/work:start` で実装 → push → `create_pull_request`。マージはしない |
| 3 | `pr-reviewer` | `/gh:pr-review-auto` | 注入ルール準拠を中心にレビューし、合格時は `/work:merge` まで実行 |

## ラベル設計

| ラベル | 意味 | 付与者 | 外す者 |
|---|---|---|---|
| `scan` / `scan:{scope}` | `issue-scan` 起票 Issue / 観点識別 | `issue-scan` | 通常外さない |
| `auto-resolve` | `issue-resolve-auto` 対象 | ユーザー | スキル取得時 |
| `auto-review` | `pr-review-auto` 対象 | ユーザー or `issue-resolver` | スキル取得時 |
| `resolving` | `issue-resolve-auto` が処理中（排他） | スキル取得時 | 完了時 |
| `reviewing` | `pr-review-auto` が処理中（排他） | スキル取得時 | 完了時 |
| `needs-fix` | レビューで request_changes された PR | `pr-review-auto` | ユーザー再 push 後 |
| `conflict-needs-human` | コンフリクト自走解消失敗 | `pr-review-auto` | 人手解消後 |
| `auto-review-failed` | レビュー or マージで失敗 | `pr-review-auto` | 人手対応後 |
| `resolve-failed` | 実装失敗 | `issue-resolve-auto` | 人手対応後 |
| `wontfix-auto` | 自動却下指示 | ユーザー | スキル取得時に `wontfix` 置換 |

## 直列マージ原則

| 原則 | 内容 |
|---|---|
| 並列起動禁止 | `pr-review-auto` は `pr-reviewer` を必ず 1 件ずつ呼ぶ |
| ラベル排他 | `reviewing` / `resolving` が付いた対象は他セッションが触らない |
| コンフリクト方針 | `/work:merge` SKILL.md の方針に従う（一括 `-X` 禁止・両側の意味の強さで判断・サブエージェント委譲禁止） |

## work プラグイン依存

| 機能 | 依存先 |
|---|---|
| ブランチ作成 + worktree + タスクドキュメント雛形 | `/work:start` |
| 親取り込み・コンフリクト処理・マージ・worktree 削除 | `/work:merge` |
| 危険操作ガード（`-X ours/theirs` 等） | work プラグインの `dangerous-git-guard` フック |

## 参考リンク

- `plugins/gh/CLAUDE.md`: 同梱ドキュメント（セットアップ手順）
- `plugins/gh/.mcp.json`: GitHub MCP 接続定義
- `plugins/gh/skills/`: 4 スキルの SKILL.md
- `plugins/gh/agents/`: 3 サブエージェント定義
- [GitHub MCP Server (公式)](https://github.com/github/github-mcp-server)
- [Install GitHub MCP in Claude Code](https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-claude.md)
