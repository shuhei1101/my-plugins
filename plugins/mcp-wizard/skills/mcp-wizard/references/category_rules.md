# 分野カテゴリ判定基準

MCPサーバーを以下の分野カテゴリに分類する基準。

---

## カテゴリ一覧

### development（開発ツール系）
- **対応ファイル**: `mcp-catalog/development.md`
- **該当条件**: ブラウザ自動化、Git/GitHub連携、CI/CD、テスト、デバッグ、IDE連携、コードフォーマッタ、リンター
- **キーワード例**: browser, playwright, github, git, test, debug, lint, format, ci, deploy

### data（データ系）
- **対応ファイル**: `mcp-catalog/data.md`
- **該当条件**: データベース、ファイルシステム、ストレージ、データ変換、ETL、スプレッドシート
- **キーワード例**: database, db, sql, postgres, mysql, mongo, redis, file, storage, csv, excel, sheet

### search（検索・情報取得系）
- **対応ファイル**: `mcp-catalog/search.md`
- **該当条件**: Web検索、ドキュメント検索、ナレッジベース、スクレイピング、API連携
- **キーワード例**: search, brave, google, fetch, scrape, crawl, knowledge, wiki, context7

### productivity（生産性系）
- **対応ファイル**: `mcp-catalog/productivity.md`
- **該当条件**: メール、カレンダー、チャット（Slack等）、タスク管理、ノート、ワークフロー自動化
- **キーワード例**: slack, email, gmail, calendar, notion, todoist, zapier, workflow, automation

### cloud（クラウド・インフラ系）
- **対応ファイル**: `mcp-catalog/cloud.md`
- **該当条件**: AWS、GCP、Azure、Docker、Kubernetes、監視、ログ管理
- **キーワード例**: aws, gcp, azure, docker, kubernetes, k8s, terraform, monitor, log, grafana

---

## 分類ルール

1. **キーワードマッチ**: MCP名・概要からキーワードを照合し、最も一致度の高いカテゴリに分類
2. **複数該当**: 複数カテゴリに該当する場合、主要機能に基づいて1つを選択
3. **該当なし**: どのカテゴリにも該当しない場合、最も近いカテゴリに分類するか、概要を確認して判断
