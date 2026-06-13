# pushスキルをMCPに移行・フック/スクリプト分離

> ブランチ: `refactor/push-mcp-hooks-separation`

## 概要

pushスキルをMCPツールに移行し、フックとコア処理スクリプトを明確に分離する。
`scripts/`フォルダを新設しコア処理を配置。フック（`.claude/hooks/`）はそれをラップする形に整理する。

### 実施条件

即時実施可

## 作業内容

| No | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | `scripts/`フォルダを作成し`post_merge_upgrade.py`を移動 |
| 2 | 済 | `.claude/hooks/post-merge-upgrade.py`が`scripts/`を呼ぶ形に変更 |
| 3 | 済 | `tools/mcp_server.py`にpushツールを追加（`scripts/`呼び出し） |
| 4 | 済 | `tools/post_merge_upgrade.py`を削除 |
| 5 | 済 | `.claude/skills/push/SKILL.md`を削除 |
| 6 | 済 | workプラグインのバージョンバンプ（1.5 → 1.6） |

## 変更内容

| No | ファイル名 | 新規/編集/削除 | 内容 |
|---|---|---|---|
| 1 | `scripts/post_merge_upgrade.py` | 新規（移動） | push + upgrade + reload のコア処理 |
| 2 | `.claude/hooks/post-merge-upgrade.py` | 編集 | scripts/を呼ぶ形に変更（条件チェック部分は残す） |
| 3 | `tools/mcp_server.py` | 編集 | pushツールをscripts/呼び出しに変更 |
| 4 | `tools/post_merge_upgrade.py` | 削除 | scripts/に移動済み |
| 5 | `.claude/skills/push/SKILL.md` | 削除 | MCPツールに移行 |

## 参考ドキュメント

- [post-merge-upgrade](.work/notes/hooks/post-merge-upgrade.md)
- [MCP サーバー](.work/notes/hooks/mcp-server.md)
