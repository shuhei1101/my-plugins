---
paths: "*"
---

# Claude Code tools活用法
## Writeツール使用時の注意点
- Writeツールを使用するときはいきなり本文をいれないこと
  - まず、空のファイルを作成
    - →ルールが注入される
  - その後、Editツールを使用し、編集を行う

## ツール活用
- 作業実施時は極力以下タスクツールを活用する
  - TaskCreate
  - TaskUpdate
  - TaskGet
  - TaskList
- ユーザに質問をするときは極力以下ツールを活用する
  - AskUserQuestion

