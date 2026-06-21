---
name: work:setup
description: ユーザーが `/work:setup` を実行したとき（自動起動なし）
---

カレントプロジェクトに `.work/notes/` を初期化するスキル。ファイル作成はスクリプトに委譲する。

## タスク

### ステップ 1: セットアップスクリプトを実行

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/setup/scripts/setup.py"
```

### ステップ 2: 完了確認

スクリプト出力を確認し、`.work/notes/` が存在することをユーザーに報告する。
