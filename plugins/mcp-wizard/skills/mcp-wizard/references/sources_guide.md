# MCP情報源ガイド

各情報源の特徴と、サブエージェントへの指示をまとめたガイド。

---

## 1. 公式レジストリAPI（おすすめ）

- **特徴**: Anthropic公式。400+サーバーのメタデータを網羅
- **URL**: `https://api.anthropic.com/mcp-registry/v0/servers`
- **取得方法**: WebFetch
- **サブエージェントへの指示**:
  - 上記URLからJSONを取得
  - 各サーバーの name, description, repository_url を抽出
  - `| MCP名 | 概要 | URL |` 形式に整形
  - `references/category_rules.md` に従って分野カテゴリを判定

---

## 2. FastMCP（おすすめ）

- **特徴**: 人気度・月間トレンド・インストール数がわかる
- **URL**: `https://fastmcp.me`
- **取得方法**: WebFetch
- **サブエージェントへの指示**:
  - 人気ランキング・トレンド情報を取得
  - 月間インストール数・スター数等の人気指標を含めて整形
  - `| MCP名 | 概要 | URL |` 形式に整形
  - 人気度情報は概要欄に含める

---

## 3. GitHub

- **特徴**: 公式リポジトリのREADME・スター数から情報取得
- **URL**: `https://github.com/modelcontextprotocol/servers`
- **取得方法**: WebFetch
- **サブエージェントへの指示**:
  - リポジトリのREADMEからサーバー一覧を抽出
  - 各サーバーの名前・説明・リンクを取得
  - `| MCP名 | 概要 | URL |` 形式に整形

---

## 4. npm検索

- **特徴**: パッケージ名・ダウンロード数で検索
- **取得方法**: Bash（`npm search mcp-server --json` 等）
- **サブエージェントへの指示**:
  - `npm search` でMCP関連パッケージを検索
  - パッケージ名・説明・npmリンクを取得
  - ダウンロード数を概要欄に含める
  - `| MCP名 | 概要 | URL |` 形式に整形

---

## 5. Context7

- **特徴**: 最新ドキュメント・コード例の取得に強い
- **取得方法**: Context7 MCP（インストール済みの場合）
- **サブエージェントへの指示**:
  - Context7のツールを使用してMCP関連の最新ドキュメントを取得
  - 新しいMCPサーバーの情報を抽出
  - `| MCP名 | 概要 | URL |` 形式に整形
- **注意**: Context7 MCPが未インストールの場合は使用不可。その旨を通知して他の情報源で続行する
