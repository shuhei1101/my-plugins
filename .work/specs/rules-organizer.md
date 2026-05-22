---
created_at: 2026-05-22
updates:
  - 2026-05-22 — 初版作成（rules-organizer）
  - 2026-05-23 — PR71: claude-refactor にリネーム・スコープ拡張
  - 2026-05-23 — PR71: file-types.md を共通リファレンスに集約、creator スキル群の二重管理を解消
  - 2026-05-23 — PR71: references を common/rules/skills/hooks/claude-md の5ファイルに分割（トークン効率改善）
related_specs: []
related_prs:
  - PR66
  - PR71
---

# claude-refactor — Claude 設定全体の監査・整理スキル

## 概要

`.claude/` 配下の rules / skills / CLAUDE.md / hooks を横断的に監査し、
フォルダ構成の整備・重複の統合・ファイルタイプ間の移管を提案するスキル。

旧名: `rules-organizer`（PR66 作成、PR71 で拡張・リネーム）

## 対象スコープ

| スコープ | 主な分析内容 |
|---|---|
| rules | フォルダ構成整備・重複検出・CLAUDE.md/hook/skill への移管提案 |
| skills | 重複統合・分割・ファイルタイプ移管提案 |
| CLAUDE.md | 肥大化検出・rules/skills への切り出し提案 |
| hooks | rules/CLAUDE.md 内のフック化候補の発見・既存フックの冗長性チェック |

## フォルダ設計方針（rules スコープ）

### 必須フォルダ

| フォルダ | 役割 |
|---|---|
| `core/` | プロジェクト全体にかかる規約・ワークフロー・環境設定。機能や開発フェーズに依存しない。 |
| `feature/` | 個別機能のドメイン知識・実装ルール。機能単位で 1 ファイル。 |

### 任意フォルダ（コードベース依存）

| フォルダ | 追加する目安 |
|---|---|
| `ui/` | フロントエンドがあるプロジェクト |
| `api/` | バックエンド API のルールが多いプロジェクト |
| `infra/` | インフラ・デプロイ系のルールが多いプロジェクト |

## ファイルタイプ判断基準（全スコープ共通）

| 内容の性質 | 最適なファイルタイプ |
|---|---|
| 複数の異なるフォルダをまたぐファイル同期リンク | rule |
| プロジェクト全体で常に必要な短い指示 | CLAUDE.md（ルート） |
| 複数ステップ・ユーザー確認・分岐があるワークフロー | skill |
| 繰り返し自動実行される処理 | hook |

## スキルの配置

- パス: `plugins/claude-kit/skills/claude-refactor/`
- コマンド名: `claude-kit:claude-refactor`
- バージョン: claude-kit 3.14.0
