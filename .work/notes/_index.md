# ノートインデックス

## フック・自動化

- [post-merge-upgrade](hooks/post-merge-upgrade.md): マージ後自動 push & upgrade フック
- [pre-merge-version-check](hooks/pre-merge-version-check.md): マージ前バージョンチェックフック
- [pre-merge-check](hooks/pre-merge-check.md): マージ前2段階安全チェック（master取り込み確認＋dry-runコンフリクト検証）
- [mcp-server](hooks/mcp-server.md): my-plugins MCP サーバー（ツール群の MCP 公開）
- [work-mcpサーバー](hooks/work-mcpサーバー.md): work-tools MCP サーバー（work コマンドの MCP 公開と Stop フック制御）
- [master-commit-guard](hooks/master-commit-guard.md): 保護ブランチへの直接コミットを完全ブロック
- [protected-branch-guard](hooks/protected-branch-guard.md): 保護ブランチへの直接ファイル編集をブロック（Edit/Write フック）
- [delete-guard](hooks/delete-guard.md): .git / .claude / .gitignore / .gitattributes への削除操作を永久ブロック
- [dangerous-git-guard](hooks/dangerous-git-guard.md): 危険な git コマンド（worktree remove --force / git rm 重要ファイル / -X ours/theirs 等）を永久ブロック
- [post-commit-deletion-check](hooks/post-commit-deletion-check.md): 直近コミットで N 件超の削除を検知したら警告コンテキストを注入（Stop hook）
- [worktree-base-ref](hooks/worktree-base-ref.md): worktree 作成時の base ref を origin/&lt;current&gt; に強制（古い HEAD 分岐防止）

- [rules-structure](hooks/rules-structure.md): hooksルール配置構成（スクリプトとルールの分離）
- [inject_rules注入ロジック](hooks/inject_rules注入ロジック.md): inject_rules.py の注入動作・トークン管理・分割読み込み仕様
