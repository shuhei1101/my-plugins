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
| 1 | `/gh-kit:code-scan-auto` | 観点別スキャン → `code-scanner` が `gh issue create` で直接起票（`needs-ai-review` 必須付与） |
| 2 | `/gh-kit:issue-review` | `needs-ai-review` 付きの Issue に AI 方針/質問を投稿 |
| 3 | `/gh-kit:pr-wip-create` | needs-* なしの open Issue 全件 → Draft PR 生成（`wip` 付与） |
| 4 | `/gh-kit:pr-implement-auto` | `wip` Draft PR を N 件並列実装 → Ready 化（`needs-ai-review` 必須付与 + `needs-user-review` 状況判断） |
| 5 | `/gh-kit:pr-review-auto` | `needs-ai-review` Ready PR を直列でレビュー → 合格 + needs-user-review なしならマージ |

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
| `plugins/gh-kit/templates/ユーザーレビュー要否判定.md` | `needs-user-review` を付けるか判定基準 | `GH_KIT_USER_REVIEW_CRITERIA_PATH` |
| `plugins/gh-kit/scripts/labels.sh` | ラベル名一元定義 | （固定） |

SKILL/agent からは `!`cat "${ENV:-${CLAUDE_PLUGIN_ROOT}/templates/...}"`` で直展開、ラベル名は `. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"` で source。

## ラベル設計

詳細は `.work/notes/プラグイン/gh-kitラベル設計.md` を参照。ラベル名は `plugins/gh-kit/scripts/labels.sh` に一元化。

要点:

| ラベル種 | 例 |
|---|---|
| 共通排他 | `processing` |
| 共通レビュー | `needs-ai-review` / `needs-user-review` / `needs-fix` |
| Issue 出自 | `ai-code-scan` / `type:*` / `priority:*` |
| PR フェーズ | `wip` |

## 直列マージ原則

| 原則 | 内容 |
|---|---|
| 並列起動禁止 | `pr-review-auto` は `pr-reviewer` を 1 件ずつ呼ぶ |
| ラベル排他 | `processing` が付いた対象は他セッションが触らない |
| Draft 隔離 | `wip` + `draft: true` の PR は `pr-review-auto` の対象外 |
| マージ可能条件 | `needs-*` がすべて外れた + processing なし + draft でない + open |
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
