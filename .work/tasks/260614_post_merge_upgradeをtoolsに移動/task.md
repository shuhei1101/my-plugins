# post_merge_upgradeをtoolsに移動

## 概要

scripts/post_merge_upgrade.py を tools/ に移動し、
フック・MCPサーバーからの参照パスを更新する。
scriptsフォルダが空になるため削除する。

## 作業内容

| 完了 | 内容 |
| ---- | ---- |
| 済 | scripts/post_merge_upgrade.py を tools/post_merge_upgrade.py に移動 |
| 済 | scripts/ フォルダを削除 |
| 済 | .claude/hooks/post-merge-upgrade.py のパスを tools/ に更新 |
| 済 | tools/mcp_server.py の SCRIPTS 参照を tools/ に更新 |

## 参考ドキュメント

- [post-merge-upgrade](../../notes/hooks/post-merge-upgrade.md)
