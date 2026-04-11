---
name: mcp-wizard
description: MCPサーバーの総合管理を行う。最新MCP情報の取得・おすすめMCP探索・登録・管理を対話形式でガイドする。「MCPを登録したい」「おすすめMCPを教えて」「MCP管理」「MCPって何」「MCP情報を更新したい」といったリクエストで起動。
---

# MCP Wizard — MCP総合管理スキル

## このスキルについて

MCPサーバーの総合管理を対話形式でガイドするスキル。MCP初心者でも迷わず使えるよう、各ステップで丁寧な説明を提供する。

### 主要機能
1. **最新MCP情報取得**: 公式レジストリ・FastMCP等から最新のMCPサーバー情報を取得し、カタログに保存
2. **おすすめMCP探索**: SKILL.mdや開発コードを分析し、カタログ未登録のMCPからおすすめを提案
3. **MCP登録**: CLIコマンドまたは設定ファイル直接編集でMCPサーバーを登録
4. **MCP管理**: 登録済みMCPの一覧表示・編集・削除・有効無効切替

### ターゲット
MCP初心者（MCPを使ったことがない人）

### 出力言語
日本語

---

## 前提知識

### カタログ（`mcp-catalog/`）
- MCP情報を分野別に管理するローカルデータベース
- 各ファイルは `| MCP名 | 概要 | URL |` の表形式
- 情報取得時に自動更新される
- おすすめ探索では、カタログに未登録のMCPのみ結果に含める

### MCP設定方法
- **CLI**: `claude mcp add/remove/list/get` コマンド
- **設定ファイル**: `.mcp.json`（プロジェクト）、`~/.claude/settings.local.json`（ユーザー）
- **接続タイプ**: stdio（ローカル）/ HTTP（リモート）/ SSE（リモート）
- **スコープ**: user（全プロジェクト共通）/ project（プロジェクト限定）

---

## 関連ファイル

### ガイド・テンプレート
- `references/mcp_intro.md` — MCP初心者向け説明テンプレート
- `references/sources_guide.md` — 情報源の一覧・特徴・サブエージェントへの指示
- `references/category_rules.md` — 分野カテゴリの判定基準

### カタログ（動的データ）
- `mcp-catalog/development.md` — 開発ツール系MCP
- `mcp-catalog/data.md` — データ系MCP
- `mcp-catalog/search.md` — 検索・情報取得系MCP
- `mcp-catalog/productivity.md` — 生産性系MCP
- `mcp-catalog/cloud.md` — クラウド・インフラ系MCP

---

## 作業フロー

### フェーズ1: エントリー

📁 **必読**: `references/wizards/00_entry.md`

**含まれるステップ**:
- ステップ1: メインメニュー（モード選択、自動ジャンプ対応）
- ステップ1.5: MCPとは？（初心者向け説明）

---

### フェーズ2: MCP情報取得

📁 **必読**: `references/wizards/01_fetch.md`

**含まれるステップ**:
- ステップ2: 情報源選択
- ステップ3: サブエージェント並列検索
- ステップ4: 結果表示と次のアクション

---

### フェーズ3: おすすめMCP探索

📁 **必読**: `references/wizards/02_explore.md`

**含まれるステップ**:
- ステップ5: 調査方法選択
- ステップ6: おすすめ結果表示

---

### フェーズ4: MCP登録

📁 **必読**: `references/wizards/03_register.md`

**含まれるステップ**:
- ステップ7: 登録方法選択
- ステップ8: 情報入力
- ステップ9: 確認と実行

---

### フェーズ5: MCP管理

📁 **必読**: `references/wizards/04_manage.md`

**含まれるステップ**:
- ステップ10: 一覧表示
- ステップ11: 操作選択
- ステップ12: 確認と実行

---

### フェーズ6: 完了

📁 **必読**: `references/wizards/05_complete.md`

**含まれるステップ**:
- ステップ13: 実行結果サマリー
