---
name: work:issue-resolve
description: 
---

# issue-resolve — レビュー済みイシューを消化する

## タスク
- 指定されたイシューを読む（イシューが指定されなければユーザに聞く）
- メインリポジトリの `_index.yaml` でイシューを in-progress にする
```bash
python "/home/shuhei2441/.claude/work-scripts/issue-tool.py" set-status \
  --issues-dir .work/issues --issue-id ISSUE-{N} --status in_progress
```
- ブランチ名を決める（`type/kebab-title`）
- `worktree-create`スキルを実行し、ワークツリーを作る
- `/work-start`スキルを実行し、作業を進める
  - 関連イシューがユーザのマージ確認が必要でない場合、`/merge`スキルを実行する
