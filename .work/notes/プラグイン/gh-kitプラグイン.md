# gh-kit プラグイン — GitHub Issues/PR を真実のソースとした作業フローキット

## 概要

GitHub Issues / Pull Request を真実のソースとして作業を回すプラグインキット。
GitHub 操作はすべて `gh` CLI に統一し、MCP は使わない（CLI 直叩きで認可・レート制御がシンプル）。
タスクドキュメント・ローカルイシュー管理は持たず、GitHub の Issue/PR ライフサイクルにすべて乗せる。
マージは `pr-review-auto` 1 経路に集約し `pr-reviewer` を直列起動することで master 取り込み競合を構造的に防ぐ。

## ワークフロー

```mermaid
flowchart TD
  U[ユーザー or /gh-kit:code-scan-auto] -->|gh issue create| Issue[(GitHub Issue)]
  Issue -->|/gh-kit:issue-review| Review[AI が方針/質問を Issue コメント]
  Review -->|議論→go ラベル| Go[(go ラベル付き Issue)]
  Go -->|/gh-kit:pr-wip-create| WIP[(Draft PR + wip)]
  WIP -->|/gh-kit:pr-implement-auto| Ready[(Ready PR + auto-review)]
  Ready -->|/gh-kit:pr-review-auto| Master[master]
```

## セットアップ

| No | 手順 |
|---|---|
| 1 | `gh` CLI をインストール（https://cli.github.com/） |
| 2 | `gh auth login` で認証（or `GH_TOKEN` 環境変数を設定） |
| 3 | `gh auth status` で接続確認 |

## スキル一覧

| No | スキル | 概要 |
|---|---|---|
| 1 | `/gh-kit:code-scan-auto` | 観点別スキャン → `code-scanner` が `gh issue create` で直接起票 |
| 2 | `/gh-kit:issue-review` | 未レビュー Issue に AI 方針/質問を Issue コメント投稿 |
| 3 | `/gh-kit:pr-wip-create` | `go` ラベル Issue 全件巡回 → Draft PR 生成 |
| 4 | `/gh-kit:pr-implement-auto` | `wip` Draft PR を N 件並列実装 → Ready 化 |
| 5 | `/gh-kit:pr-review-auto` | `auto-review` Ready PR を直列でレビュー → 合格ならマージ |

## サブエージェント一覧

| No | エージェント | 呼び元 | 役割 |
|---|---|---|---|
| 1 | `code-scanner` | `/gh-kit:code-scan-auto` | 1 観点でファイル走査し `gh issue create` で直接起票 |
| 2 | `issue-reviewer` | `/gh-kit:issue-review` | 1 Issue を読みコメント本文を返す（投稿はメイン） |
| 3 | `pr-wip-creator` | `/gh-kit:pr-wip-create` | `/work:start` でブランチ作成 → Draft PR 起票 |
| 4 | `pr-implementer` | `/gh-kit:pr-implement-auto` | 既存 Draft PR に実装コミットを積み Ready 化 |
| 5 | `pr-reviewer` | `/gh-kit:pr-review-auto` | レビュー → 合格時は `/work:merge` まで実行 |

## テンプレート（共通リソース）

| ファイル | 用途 | 差し替え用 env |
|---|---|---|
| `plugins/gh-kit/templates/スキャン観点.md` | `code-scan-auto` が選ぶ観点メニュー | `GH_KIT_SCAN_PERSPECTIVES_PATH` |
| `plugins/gh-kit/templates/ファイル解決.md` | `code-scanner` の観点→実ファイル変換ルール | `GH_KIT_FILE_RESOLUTION_PATH` |
| `plugins/gh-kit/templates/イシュー本文テンプレート.md` | `code-scanner` が起票する Issue 本文 | `GH_KIT_ISSUE_BODY_TEMPLATE_PATH` |

SKILL/agent からは `!`cat "${ENV:-${CLAUDE_PLUGIN_ROOT}/templates/...}"`` で直展開する。

## ラベル設計

詳細は `.work/notes/プラグイン/gh-kitラベル設計.md` を参照。
要点:

| ラベル種 | 例 | 寿命 |
|---|---|---|
| 出自 | `code-scan` / `type:*` / `priority:*` | 永続 |
| AI レビュー結果 | `ai-reviewed` / `needs-clarification` / `ready-for-go` / `split-needed` | 状態と連動 |
| ユーザーシグナル | `go` | 派生完了まで |
| 排他 | `wip-creating` / `implementing` / `reviewing` | 取得〜完了 |
| 進捗（PR） | `wip` / `auto-review` | 次フェーズで自動入れ替え |
| 失敗 | `implement-failed` / `auto-review-failed` / `conflict-needs-human` / `needs-fix` | 人手対応まで |

## 直列マージ原則

| 原則 | 内容 |
|---|---|
| 並列起動禁止 | `pr-review-auto` は `pr-reviewer` を 1 件ずつ呼ぶ |
| ラベル排他 | `reviewing` / `implementing` / `wip-creating` が付いた対象は他セッションが触らない |
| Draft 隔離 | `wip` ラベル + `draft: true` の PR は `pr-review-auto` の対象外 |
| コンフリクト方針 | `/work:merge` SKILL.md の方針に従う |
| Issue 早期クローズ防止 | PR 本文は `Refs #N`（`Closes` ではない） |

## work プラグイン依存

| 機能 | 依存先 |
|---|---|
| ブランチ + worktree 作成 | `/work:start` |
| 親取り込み + コンフリクト処理 + マージ + worktree 削除 | `/work:merge` |
| 危険操作ガード | work プラグインの hooks |

## 参考リンク

- `plugins/gh-kit/CLAUDE.md`: 同梱ドキュメント
- `plugins/gh-kit/skills/`: 5 スキルの SKILL.md
- `plugins/gh-kit/agents/`: 5 サブエージェント定義
- `plugins/gh-kit/templates/`: スキャン観点 / ファイル解決 / イシュー本文テンプレート
- `.work/notes/プラグイン/gh-kitラベル設計.md`: ラベル一覧・状態遷移図
- [gh CLI manual](https://cli.github.com/manual/)
