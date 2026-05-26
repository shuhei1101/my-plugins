<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# py-kit リファレンス — インデックス（日本語ミラー）

> このファイルは `CLAUDE.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `CLAUDE.md` にも反映してください。

このファイルは py-kit のすべての Python リファレンスへの入口。py-kit スキル
（`py-kit:py-script`・`py-kit:py-project`）はステップ1でまずこのファイルを読み、
タスクに応じた具体的なリファレンスファイルを次に読む。

このファイルは `plugins/py-kit/references/` に置く — 配下のいずれかのファイルが
読まれるとインデックスが会話コンテキストに乗るようにするため。

---

## どのファイルをいつ読むか

タスクに合うリファレンスを選ぶ。`python-core.md` は常に必ず読む。

| タスク | 読むファイル |
|---|---|
| すべての Python 作業（ベースライン・必須） | `python-core.md` |
| プロジェクト設計・雛形生成・リファクタリング・品質レビュー | `python-architecture.md` |
| 単一ファイルの簡易スクリプト作成（`pyproject.toml` なし・テストなし） | `python-core.md` + `python-scripts.md` |
| bat ランチャー・FastAPI run.bat・tkinter GUI の生成 | `python-scripts.md` |
| `logger.py` 作成・pytest 雛形・モック整備 | `python-testing.md` |
| FastAPI エンドポイント・ルーター・ミドルウェアの実装 | `python-fastapi.md` |
| LLM API（Claude / OpenAI）のラップ・Instructor・プロンプトファイル | `python-llm.md` |

---

## 「○○ を作る」クイックマップ

| 作るもの | 読む順序 |
|---|---|
| 単発 Python スクリプト | `python-core.md` → `python-scripts.md` |
| 新規レイヤード構成のプロジェクト（FastAPI・LLM なし） | `python-core.md` → `python-architecture.md` → `python-testing.md` |
| 新規 FastAPI サービス | `python-core.md` → `python-architecture.md` → `python-fastapi.md` → `python-testing.md` |
| 新規 LLM 駆動サービス | `python-core.md` → `python-architecture.md` → `python-llm.md` → `python-testing.md` |
| 既存プロジェクトのレビュー | `python-core.md` → `python-architecture.md` →（変更箇所に応じた個別ファイル） |

---

## ファイル一覧

| ファイル | 一言説明 |
|---|---|
| `python-core.md` | 命名規則・コメントルール・型ヒント・言語ルール — 常に必須のベースライン |
| `python-architecture.md` | SOLID・DRY・デザインパターン（Strategy / Template Method / Factory / Decorator）・DI・Pydantic 境界・レイヤードアーキテクチャ・プロジェクトフォルダ構成（純DDD） |
| `python-scripts.md` | 単一ファイルスクリプト構造・argparse パターン・bat ランチャーテンプレート（Windows）・FastAPI run.bat・tkinter GUI |
| `python-testing.md` | ロガー仕様・テストポリシー・pytest 規約・モック整理 |
| `python-fastapi.md` | DDD準拠のプロジェクト構成・ルーターパターン・依存性注入・ミドルウェア・lifespan |
| `python-llm.md` | LLM クライアント Protocol 抽象化・プロバイダパターン・タスク特化型 LLM・構造化出力（Pydantic + Instructor）・プロンプトファイル・トークン/コスト管理・エラーハンドリング |

各ファイルには JP ミラー（`*.jp.md`）が同じ構造で存在する。

---

## スキルのリファレンス読み込み手順

1. まずこの `CLAUDE.md` を読む — どのリファレンスが該当するかを特定する
2. 該当するリファレンスファイルを**全部・通しで**読む（コード生成前に）
3. セクション飛ばし読み禁止 — 各セクションに、書こうとしているコード種別に効くルールが含まれている
4. ルールがユーザーの明示指示と矛盾する場合は逸脱前に確認する
