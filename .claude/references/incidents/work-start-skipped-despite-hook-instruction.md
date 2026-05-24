# Incident: work-start skipped despite explicit hook instruction

## Date

2026-05-25

## Summary

UserPromptSubmit フックが「work-start を先に実行すること」と明示的に指示しているにもかかわらず、Claude が実装を先に開始してしまった。

## What happened

1. ユーザーが「pr-show の disable-model-invocation を削除して」とリクエスト
2. UserPromptSubmit フックが「PR が進行中でなければ work-start を実行してから作業すること」と注入
3. Claude は work-start を実行せず、直接 master 上で SKILL.md / plugin.json / marketplace.json を編集
4. コミット時に master-commit-guard フックにブロックされ発覚
5. ユーザーに指摘され、ファイルを `git restore` で元に戻してから work-start を実行

## Root cause

フックが「PR がない場合は work-start を先に実行する」と明示していたにもかかわらず、Claude がその指示を読み飛ばして実装フェーズに入った。フックの指示は参考情報ではなく **必須の前提条件** であるが、その優先度認識が不十分だった。

## Correct approach

UserPromptSubmit フックの指示は **実装開始前の必須チェック**。フックが「先に X を実行せよ」と指示している場合は、どのような作業要求であっても X を先に完了させてから作業を開始する。特に work-start は「作業ディレクトリを保護する安全装置」であり、スキップは master 直接コミットや競合リスクに直結する。

## Prevention

- フックの指示（特に step-by-step の前提条件）を「実装の邪魔」ではなく「安全装置の有効化手順」として扱うこと
- PR が進行中かどうかを確認してから作業を開始すること
- 「少し変えるだけだから」という判断で work-start をスキップしないこと
