---
created_at: 2026-05-22
updates:
  - 2026-05-22 — 初版作成
related_specs: []
related_prs:
  - PR67
---

# 次PR候補セクション — TODO.md でセッション内PR予約を記録する

## 概要

work-start で生成される TODO.md に `## 次PR候補` セクションを追加し、
セッション中に浮かんだ「次にやること」をその場で記録できるようにする。

## 背景・課題

会話セッションの中で「次のPRはこれをやろう」という話が出ても、
セッションが長くなると忘れてしまう。TODO.md に専用セクションを設けることで、
次 work-start を実行したときに前回の候補を参照できる。

## 設計

### 追加するセクション

```markdown
## 次PR候補

| タイトル | 概要 |
|---|---|
| {次にやること} | {背景・目的} |
```

### テンプレート対象ファイル

| ファイル | 役割 |
|---|---|
| `plugins/work-kit/templates/TODO.md` | work-kit インストール時の参照テンプレート |
| `plugins/work-kit/templates/.work/tasks/yyyymmdd_xxx/PRXXX/TODO.md` | `.work/` フォルダ内の example テンプレート |

### work-start スキルの変更

Step 7 に以下を追記:
- ユーザーがセッション内で言及した次PR候補を `## 次PR候補` テーブルに記入する
- 言及がなければプレースホルダー行をそのまま残す（セクション自体は削除しない）
