<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# py-kit Python リファレンス — インデックス（日本語ミラー）

> このファイルは `_index.md` の日本語ミラーです。Claude Code には読み込まれません。

このディレクトリには py-kit スキルが参照する Python 規約リファレンスを格納する。
スキルはまずこのインデックスを読み込み、タスクに応じて必要なファイルを選択して読む。

---

## ファイル一覧

| ファイル | 内容 | 読むタイミング |
|---|---|---|
| `python-core.md` | 命名規則・コメントルール・型ヒント・言語ルール | あらゆる Python タスク — ベースライン規約 |
| `python-architecture.md` | SOLID・DRY・レイヤードアーキテクチャ・DI・ハードコード禁止・Pydantic・プロジェクトフォルダ構成 | フルプロジェクト・アーキテクチャレビュー・リファクタリング |
| `python-scripts.md` | 簡易スクリプト構造・bat ランチャーテンプレート・FastAPI run.bat・tkinter GUI | スクリプト作成・bat ファイル生成・簡単な自動化 |
| `python-testing.md` | ロガー仕様・テストポリシー | テスト追加・ロギング設定・新規プロジェクト雛形 |
| `python-fastapi.md` | FastAPI エンドポイント設計・DI パターン・共通ミドルウェア | FastAPI プロジェクト |
| `python-llm.md` | LLM クライアントアーキテクチャ・プロンプト管理・トークン管理 | LLM API を呼ぶプロジェクト |

---

## 使い分けガイド

**py-script**（簡易スクリプト）: `python-core.md` と `python-scripts.md` を読む

**py-project 新規**: `python-core.md`・`python-architecture.md`・`python-testing.md` を読む。FastAPI の場合は `python-fastapi.md` を追加

**py-project 既存**: `python-core.md`・`python-architecture.md` を読む。タスクに応じて他ファイルを追加

**FastAPI タスク**: `python-core.md`・`python-architecture.md`・`python-fastapi.md` を読む

**LLM タスク**: `python-core.md`・`python-llm.md` を読む
