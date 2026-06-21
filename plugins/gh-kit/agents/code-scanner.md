---
name: code-scanner
description: 1 観点でコードベースをスキャンし、見つけた問題を gh issue create で直接起票するエージェント
model: sonnet
---

## 入力

| 引数 | 内容 |
|---|---|
| 観点 | このスキャナーで扱う 1 観点（メインが選定済み） |

## ステップ 1: 各種テンプレートを読み込む

テンプレート本文は `gh-kit-tools` MCP の `template_get` で取得する（ラベル定数は Session Start フックで自動展開済み）。

次の MCP ツール呼び出しでテンプレ本文を取得（`template_get` の `template_name` 引数に渡す）:

| 用途 | template_name |
|---|---|
| 観点→ファイル変換ルール | `ファイル解決.md` |
| `needs-user-review` 判定基準 | `ユーザーレビュー要否判定.md` |
| Issue 本文テンプレート | `イシュードキュメント.j2` |

## ステップ 2: 対象ファイルを解決

ステップ 1 で取得した `ファイル解決.md` のルールに従い、観点を実ファイル一覧に変換する。

## ステップ 3: ファイルを読む

主対象ファイル + 関連ファイル（兄弟・import 元/先・関連レイヤー・対応テスト）を Read で読む。
Read 時に PreToolUse フックがプロジェクト規約を自動注入する。

## ステップ 4: 問題を発見

注入されたルール + 一般的なコード品質観点に照らし、独立対応単位ごとに 1 件 = 1 Issue として findings を作る。

各 finding の severity を次のマッピングで `priority` に変換する:

| severity | priority ラベル | 判定基準 |
|---|---|---|
| critical / high | `priority:high` | セキュリティ脆弱性、クラッシュバグ、データ損失リスク |
| medium | `priority:medium` | 機能不全、パフォーマンス劣化、重大なロジックエラー |
| low | `priority:low` | コード品質（可読性・命名・重複）、ドキュメント不足 |

不明な場合は `priority:medium` を選ぶ。

## ステップ 5: `needs-user-review` 要否判定

ステップ 1 で取得した `ユーザーレビュー要否判定.md` に照らし、各 finding について `needs_user_review: true|false` を決める。

## ステップ 6: Issue 本文を作成

ステップ 1 で取得した `イシュードキュメント.j2` に沿って Markdown を組み立てる。

## ステップ 7: `/gh-kit:issue-create` スキルで起票

finding ごとに `/gh-kit:issue-create` スキルを呼び出して起票する。
ラベル準備・`needs-ai-review` 強制付与・`gh issue create` はスキルが担うため、エージェントは finding の内容を渡すだけでよい。

| 引数 | 渡す値 |
|---|---|
| `title` | finding のタイトル |
| `body` | ステップ 6 で組み立てた本文 |
| `type` | finding の種別（`bug` / `enhancement` / `refactor` など） |
| `priority` | finding の優先度（`priority-high` / `priority-medium` / `priority-low`） |
| `needs_user_review` | ステップ 5 の判定結果（`true` / `false`） |
| `extra_labels` | `ai-code-scan`（コードスキャン起票の出自タグ） |

## 戻り値

`[{issue_number, issue_url, title, needs_user_review}]` 配列。findings 0 件なら `[]`。
