---
created_at: 2026-05-31
updates:
  - 2026-05-31 — 初版作成
related_notes: []
related_branches:
  - feat/document-askuserquestion-limits
---

# AskUserQuestion 制約リファレンス — スキルからの呼び出しガイド

## 概要

`AskUserQuestion` ツールの制約と正しい使い方を claude-kit リファレンスとして文書化する取り組み。
スキル作成者が options 数やフィールドを誤って使うことを防ぐため、制約を一元的にまとめる。

## 背景

`AskUserQuestion` は一般的なターン終了（Stop フック）を発火させない。そのため、スキル定義や
ユーザーの明示的指示がない限り呼んではいけない制約が CLAUDE.md に記載されている。しかし
この制約はリファレンスとして存在しておらず、スキルの注入対象になっていなかった。

## 制約一覧

| # | 制約 | 値 |
|---|---|---|
| 1 | questions 数 | 1〜4 |
| 2 | options 数 | 2〜4 |
| 3 | "Other" オプション | UI が自動付与 — 手動追加禁止 |
| 4 | `multiSelect` | 排他でない選択肢に使う |
| 5 | `preview` | single-select のみ対応 |
| 6 | 使用制限 | スキル定義またはユーザーの明示指示時のみ |

## ファイル構成

| # | ファイル | 役割 |
|---|---|---|
| 1 | `plugins/claude-kit/references/askuserquestion.md` | 英語リファレンス（正本） |
| 2 | `plugins/claude-kit/references/askuserquestion.jp.md` | JP ミラー |
| 3 | `plugins/claude-kit/references/_index.yaml` | インデックスエントリ追加 |
| 4 | `plugins/claude-kit/references/_index.jp.yaml` | JP インデックスエントリ追加 |
| 5 | `plugins/claude-kit/references/_injection_rules.yaml` | skills パターンに optional 追加 |

## 注入タイミング

`_injection_rules.yaml` の `**/skills/*/SKILL{.jp,}.md` パターンに `optional` として追加。
スキル作成中に必要に応じて Read できる。
