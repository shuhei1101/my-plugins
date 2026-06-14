# ノートインデックス

## フック・自動化

- [post-merge-upgrade](hooks/post-merge-upgrade.md): マージ後自動 push & upgrade フック
- [pre-merge-version-check](hooks/pre-merge-version-check.md): マージ前バージョンチェックフック
- [pre-merge-check](hooks/pre-merge-check.md): マージ前2段階安全チェック（master取り込み確認＋dry-runコンフリクト検証）
- [mcp-server](hooks/mcp-server.md): my-plugins MCP サーバー（ツール群の MCP 公開）
- [work-mcpサーバー](hooks/work-mcpサーバー.md): work-tools MCP サーバー（work コマンドの MCP 公開と Stop フック制御）
- [master-commit-guard](hooks/master-commit-guard.md): 保護ブランチへの直接コミットを完全ブロック
- [protected-branch-guard](hooks/protected-branch-guard.md): 保護ブランチへの直接ファイル編集をブロック（Edit/Write フック）
- [delete-guard](hooks/delete-guard.md): .git / .claude ディレクトリへの削除操作を永久ブロック

- [rules-structure](hooks/rules-structure.md): hooksルール配置構成（スクリプトとルールの分離）
- [inject_rules注入ロジック](hooks/inject_rules注入ロジック.md): inject_rules.py の注入動作・トークン管理・分割読み込み仕様
