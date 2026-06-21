# ノートインデックス

## プラグイン

- [guard-kitプラグイン](プラグイン/guard-kitプラグイン.md): ローカル Git 保護フック群（master 直接コミット阻止 / 危険 git コマンド阻止 / セッション規約注入）
- [gh-kitプラグイン](プラグイン/gh-kitプラグイン.md): GitHub Issues/PR/Wiki + ワークツリー操作のフルキット（gh CLI + worktree MCP + pre-merge-check）
- [gh-kitラベル設計](プラグイン/gh-kitラベル設計.md): Issue/PR の状態を表すラベル一覧と状態遷移図

## フック・自動化

- [post-merge-upgrade](hooks/post-merge-upgrade.md): マージ後自動 push & upgrade フック
- [pre-merge-version-check](hooks/pre-merge-version-check.md): マージ前バージョンチェックフック
- [pre-merge-check](hooks/pre-merge-check.md): マージ前2段階安全チェック（master取り込み確認＋dry-runコンフリクト検証）
- [mcp-server](hooks/mcp-server.md): my-plugins MCP サーバー（ツール群の MCP 公開）
- [work-mcpサーバー](hooks/work-mcpサーバー.md): work-tools MCP サーバー（work コマンドの MCP 公開と Stop フック制御）
- [master-commit-guard](hooks/master-commit-guard.md): 保護ブランチへの直接コミットを完全ブロック
- [protected-branch-guard](hooks/protected-branch-guard.md): 保護ブランチへの直接ファイル編集をブロック（Edit/Write フック）
- [delete-guard](hooks/delete-guard.md): .git / .claude / .gitignore / .gitattributes / lock ファイルへの削除操作を永久ブロック
- [dotgit-lockfile-guard](hooks/dotgit-lockfile-guard.md): .git/** および lock ファイルへの Edit/Write を永久ブロック
- [scripts-branch-guard](hooks/scripts-branch-guard.md): work プラグイン scripts (index-tool / issue-tool / trim-index) を master/main/develop で実行禁止にするスクリプト側ガード
- [dangerous-git-guard](hooks/dangerous-git-guard.md): 危険な git コマンド（worktree remove --force / git rm 重要ファイル / -X ours/theirs 等）を永久ブロック
- [post-commit-deletion-check](hooks/post-commit-deletion-check.md): 直近コミットで N 件超の削除を検知したら警告コンテキストを注入（Stop hook）
- [worktree-base-ref](hooks/worktree-base-ref.md): worktree 作成時の base ref を origin/&lt;current&gt; に強制（古い HEAD 分岐防止）
- [session_start](hooks/session_start.md): SessionStart 時に「やってはいけないこと」を Jinja2 経由で注入し、env (WORK_*) で出し分け

- [rules-structure](hooks/rules-structure.md): hooksルール配置構成（スクリプトとルールの分離）
- [inject_rules注入ロジック](hooks/inject_rules注入ロジック.md): inject_rules.py の注入動作・トークン管理・分割読み込み仕様
