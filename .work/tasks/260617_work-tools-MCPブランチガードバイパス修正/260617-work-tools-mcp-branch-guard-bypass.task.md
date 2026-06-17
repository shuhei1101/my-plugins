# work-tools MCPブランチガードバイパス修正

> ブランチ: `fix/mcp-branch-guard-bypass`

## 概要

`index-tool.py` / `issue-tool.py` / `trim-index.py` の `main()` 先頭で呼ばれる `assert_not_protected_branch()` が、MCPサーバー経由の呼び出し（`cwd=CLAUDE_PROJECT_DIR` = メインリポジトリ = master）でも発動してしまい、書き換え系ツールが全て `exit 1` で失敗するバグを修正する。

### 実施条件

即時実施可

## 作業内容

| No | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | `index-tool.py` / `issue-tool.py` / `trim-index.py` から `assert_not_protected_branch` の import と呼び出しを削除 |
| 2 | 済 | 動作確認：master上でスクリプトが正常に動作することを確認 |
| 3 | - | `.work/notes/` の関連ノートを更新する |

## 変更内容

| No | ファイル名 | 新規/編集 | 内容 |
|---|---|---|---|
| 1 | `plugins/work/scripts/index/index-tool.py` | 編集 | `assert_not_protected_branch` の import と呼び出しを削除 |
| 2 | `plugins/work/scripts/index/trim-index.py` | 〃 | 〃 |
| 3 | `plugins/work/scripts/issue/issue-tool.py` | 〃 | 〃 |
| 4 | `plugins/work/.claude-plugin/plugin.json` | 〃 | バージョン 1.21 → 1.22 |
| 5 | `.claude-plugin/marketplace.json` | 〃 | 〃 |

## テスト

| No | 確認内容 | 実測結果 | 判定 |
|---|---|---|---|
| 1 | master上で `index-tool.py list-active` が成功する | 正常に一覧表示された | OK |
| 2 | `index_add` MCPツールがmaster上で成功する | (未実施) | - |

## 参考リンク

- `plugins/work/scripts/_branch_guard.py`: ブランチガード共通モジュール
- `plugins/work/mcp/server.py`: work-tools MCPサーバー
