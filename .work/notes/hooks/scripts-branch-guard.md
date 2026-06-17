# scripts-branch-guard — work プラグイン scripts 共通の保護ブランチガードモジュール

## 概要

`plugins/work/scripts/_branch_guard.py` に `assert_not_protected_branch()` を実装している共通ヘルパー。
現在は各スクリプトから呼び出されていない（v1.22 で削除）。

## 現在の状態

- `_branch_guard.py` はファイルとして存在するが、どのスクリプトからも import・呼び出しされていない
- `index-tool.py` / `issue-tool.py` / `trim-index.py` はすべて MCP サーバー経由でのみ呼ばれる設計のため、ガードは不要と判断して削除した
- `worktree-tool.py` は元々ガードを持っていない（master から worktree を切る入口のため）

## 削除した理由

MCP サーバー（`server.py`）は `cwd=CLAUDE_PROJECT_DIR`（= メインリポジトリ = master）でスクリプトを実行する。
ガードが `cwd` の git ブランチを見て判定するため、正当な MCP 経由の呼び出しでも常に `exit 1` になっていた。
「CLI の直叩き防止」という意図だったが、MCP が間に入っている以上、直叩きリスクはないため削除が適切。

## 参考リンク

- `plugins/work/scripts/_branch_guard.py`: ガードモジュール本体（未使用）
- `plugins/work/mcp/server.py`: `_run_script` の cwd 渡し（`CLAUDE_PROJECT_DIR`）
