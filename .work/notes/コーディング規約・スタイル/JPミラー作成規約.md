# JPミラー作成規約 — .jp.md ファイルの作成ルール

## 概要

すべての英語ソースファイル（`.md`）には対応する日本語ミラーファイル（`.jp.md`）が必要。
Claude Code が読み込む英語ファイルに対してユーザーが参照する日本語版を提供する。

## 対象ファイル種別

| 英語ソース | JP ミラーパス |
|---|---|
| `plugins/{name}/references/**/*.md` | 同ディレクトリに `*.jp.md` |
| `plugins/{name}/skills/{skill}/SKILL.md` | `SKILL.jp.md`（同ディレクトリ） |
| `plugins/{name}/hooks/prompts/*.md` | `*.jp.md`（同ディレクトリ） |
| `plugins/{name}/CLAUDE.md` | `CLAUDE.jp.md`（同ディレクトリ） |

## ミラーヘッダー

すべての `.jp.md` ファイルの先頭に以下のコメントを付ける:

```
<!-- This file is a Japanese mirror of {source}.md. When updating the English original, update this file too. -->
```

## フックプロンプトファイルの特別ルール

`hooks/prompts/*.md` はフック実行時にそのままプロンプトとして読み込まれるプレーンテキストファイル。
JP ミラーでも**見出し（`#`）やセクション構造（`---` 区切り等）を追加してはならない**。
EN オリジナルと同じ構造（見出し数 0、プレーンテキスト）を維持すること。

## 作業ワークフロー

新規ファイル追加時は JP ミラーを同時作成し、同一コミットに含める。

## 既知の問題（ISSUE-062）

以下のファイルは JP ミラーなしで運用されていた（2026-05-31 修正済み）:

| No | ファイル | 対処 |
|---|---|---|
| 1 | `claude-kit/references/common/環境変数.md` | JP ミラー新規作成 |
| 2 | `dev-kit/references/next/backend/DB-ID設計.md` | JP ミラー新規作成 |
| 3 | `dev-kit/references/next/frontend/空状態.md` | JP ミラー新規作成 |
| 4 | `dev-kit/references/next/frontend/編集ページ-tsx.md` | JP ミラー新規作成 |
| 5 | `dev-kit/references/next/frontend/詳細ページ-tsx.md` | JP ミラー新規作成 |
| 6 | `dev-kit/skills/html-debug-fab/SKILL.md` | JP ミラー新規作成 |
| 7 | `ref-inject/templates/references/.ref-injects/CLAUDE.md` | JP ミラー新規作成 |

## ISSUE-065 との関連

`git-guard.jp.md` がフックプロンプトファイルにもかかわらず見出し・セクション構造を持っていた
（2026-05-31 修正済み）。フックプロンプトの JP ミラーはプレーンテキストを維持する必要がある。

## 変更履歴

| 日付 | 変更内容 |
|---|---|
| 2026-05-31 | ノート新規作成。ISSUE-062/065 の修正内容を記録 |
