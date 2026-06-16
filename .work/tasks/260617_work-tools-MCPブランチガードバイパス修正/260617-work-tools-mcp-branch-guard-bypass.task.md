# work-tools MCPブランチガードバイパス修正

> ブランチ: `fix/mcp-branch-guard-bypass`

## 概要

`index-tool.py` / `issue-tool.py` / `trim-index.py` の `main()` 先頭で呼ばれる `assert_not_protected_branch()` が、MCPサーバー経由の呼び出し（`cwd=CLAUDE_PROJECT_DIR` = メインリポジトリ = master）でも発動してしまい、書き換え系ツールが全て `exit 1` で失敗するバグを修正する。

### 実施条件

即時実施可

## 作業内容

| No | 完了 | 作業内容 |
|---|---|---|
| 1 | - | `_branch_guard.py` に環境変数バイパス（`WORK_MCP_CALL=1`）を追加 |
| 2 | - | `server.py` の `_run_script()` で `WORK_MCP_CALL=1` を環境変数に渡す |
| 3 | - | 動作確認：`index_add` MCPツールが master 上でも成功することを確認 |
| 4 | - | `.work/notes/` の関連ノートを更新する |

## 変更内容

| No | ファイル名 | 新規/編集 | 内容 |
|---|---|---|---|
| 1 | `plugins/work/scripts/_branch_guard.py` | 編集 | `WORK_MCP_CALL=1` 環境変数があればガードをスキップ |
| 2 | `plugins/work/mcp/server.py` | 編集 | `_run_script()` で `WORK_MCP_CALL=1` を子プロセスに渡す |

## テスト

| No | 確認内容 | 実測結果 | 判定 |
|---|---|---|---|
| 1 | `index_add` MCPツールがmaster上で成功する | (未実施) | - |
| 2 | `issue_move_to_progress` MCPツールが動作する | (未実施) | - |
| 3 | `worktree_create` は引き続き正常に動作する | (未実施) | - |

## 参考リンク

- `plugins/work/scripts/_branch_guard.py`: ブランチガード共通モジュール
- `plugins/work/mcp/server.py`: work-tools MCPサーバー
