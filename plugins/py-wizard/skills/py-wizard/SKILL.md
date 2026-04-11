---
name: py-wizard
description: Pythonプロジェクトの新規作成から実装・テストまでを対話形式でサポートするスキル。「Pythonツール作りたい」「Pythonプロジェクト作成」「py-wizard」「新しいPythonアプリ」「Python開発」といったリクエストで起動する。
version: 1.3.6
---

# py-wizard — Python開発ウィザード

## このスキルについて

Pythonプロジェクトの新規作成から実装・テストまでを対話形式でサポートするスキル。

- **新規プロジェクト作成**: 要件定義 → README作成 → プロジェクト雛形生成 → GUI設計
- **実装・改修**: 要件整理 → 実装計画 → コード実装 → テスト設計・実行

各ツールは完全に独立したパッケージとして作成する（マイクロサービス設計）。

---

## 共通ルール

📁 **必読**: `references/python_rules.md` — Pythonルール一式（フォルダ構成・コーディングスタイル・ログ・GUI・技術選定等）

📁 **必読**: `references/readme_guide.md` — READMEセクション別作成ガイド

---

## 作業フロー

### フェーズ1: エントリーポイント

📁 **必読**: `references/phases/00_entry.md`

- ステップ1.1: モード選択（新規作成 / 実装・改修 / 前回セッション再開）

---

### フェーズ2: 新規プロジェクト作成

📁 **必読**: `references/phases/01_new_project.md`

- ステップ2.1: 要件ヒアリング
- ステップ2.2: 要件まとめ確認
- ステップ2.3: README — 概要
- ステップ2.4: README — 機能一覧
- ステップ2.5: README — ツール構成フロー図（/diagram-wizard）
- ステップ2.6: README — 開発技術
- ステップ2.7: README — フォルダ構成
- ステップ2.8: README — 使い方・インストール方法
- ステップ2.9: README最終確認
- ステップ2.10: 作成場所の確認
- ステップ2.11: プロジェクト雛形生成
- ステップ2.12: GUI設計（アスキーアート案）
- ステップ2.13: プロジェクト専用スキル生成
- ステップ2.14: 実装フェーズ移行確認

---

### フェーズ3: 実装・改修

📁 **必読**: `references/phases/02_implementation.md`

- ステップ3.1: 要件入力
- ステップ3.2: 実装計画まとめ（ユーザー確認）
- ステップ3.3: コード実装

---

### フェーズ4: テスト

📁 **必読**: `references/phases/03_test.md`

- ステップ4.1: テスト観点選択（ユーザー確認）
- ステップ4.2: モックファイル設計
- ステップ4.3: テストコード実装
- ステップ4.4: テスト実行・結果確認（ユーザー確認）
- ステップ4.5: プロジェクト専用スキル・ドキュメント更新

---

### フェーズ5: 完了

📁 **必読**: `references/phases/04_complete.md`

- ステップ5.1: 実行結果サマリー出力

---

## Memory活用ルール

スキル実行中の情報は `~/.claude/skill-memory/py-wizard/` に保存する。

- **セッション記録**: `{YYYYMMDDHHMMSS}_session.md`（テンプレート: `assets/session_template.md`）
- **図案アーカイブ**: `{ツール名}/diagram/{YYYYMMDDHHMMSS}_flow_diagram.md` — ツール構成フロー図の検討履歴
- プロジェクト専用スキル: `assets/project_skill_template.md` を参照
