<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# SKILL.jp.md — work-kit:setup スキル（日本語ミラー）

> このファイルは `SKILL.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `SKILL.md` にも反映してください。

---

**スキル名**: setup
**トリガー**: ユーザーが `/work-kit:setup` を実行したとき（自動起動なし）

---

## 概要

カレントプロジェクトに `.work/` ドキュメント構造を初期化するスキル。
ファイル作成はスクリプトに委譲する（Claude が直接作らない）。

展開される構造:
```
.work/
├── tasks/      # タスク・PR フォルダ（動的生成）
├── notes/      # 設計メモ・検討ノート（空フォルダ）
├── issues/     # issue-scan・issue-create で管理するイシューファイル
└── QA.md       # 未解決事項
```

---

## 作業内容

### ステップ1: セットアップスクリプトを実行する

#### 条件

- 常に — 最初に実行する

#### 処理内容

1. 以下のコマンドを実行する:

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/setup/scripts/setup.py"
```

→ ステップ2へ進む

#### 出力

- `.work/` がカレントディレクトリに展開済み

---

### ステップ2: 完了確認

#### 処理内容

1. スクリプトの出力を確認する
2. ユーザーに完了を報告する

#### 補足

##### チェックリスト

- [ ] `.work/tasks/` — 存在する
- [ ] `.work/notes/` — 存在する
- [ ] `.work/issues/` — 存在する（内部に `.gitignore` あり）
- [ ] `.work/QA.md` — 存在する
