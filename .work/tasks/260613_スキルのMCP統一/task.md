# スキル内 Bash 直叩きを MCP ツール経由に統一

## 概要

work プラグインのスキル本文に Bash 直叩きの古い記述が残っており、SKILL.md が冗長
かつ古いパス（`/home/shuhei2441/.claude/work-scripts/...`）を参照していた。
すでに MCP に同等ツールが揃っているため、全部 MCP 経由に統一する。

## 作業内容

| 作業 | 完了 |
| ---- | ---- |
| `branch-index-cleanup/SKILL.md` の `index-tool.py add` を `index_add` MCP に置換 | 済 |
| `issue-resolve/SKILL.md` の `issue-tool.py set-status` を `issue_set_status` MCP に置換 | 済 |
| `issue-resolve-auto/SKILL.md` の `issue-tool.py set-status` を `issue_set_status` MCP に置換 | 済 |

## 参考ドキュメント
