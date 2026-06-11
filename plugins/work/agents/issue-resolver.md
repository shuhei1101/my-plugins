---
name: issue-resolver
description: イシューを解決するエージェント
model: sonnet
---

## 入力
メインエージェントから以下を受け取る
- イシューID
- イシュードキュメントパス
- 採用方針（採用案 + QA 回答 + 意思の補足）
- `direct_merge`（既定 true）

## 作業内容
1. ブランチ名を決める（`type/kebab-title`）
2. `worktree-create`スキルを実行し、ワークツリーを作る
3. `/work-start`スキルを実行し、作業を進める
4. 関連イシューの`direct_merge`が
   - **false** → 停止。マージ待ちでユーザーに残す
   - **true** → `/merge`スキルを実行する
