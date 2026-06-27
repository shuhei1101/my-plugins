---
name: gh-kit:issue-triage
description: 起票直後の Issue を 1 件トリアージし、本文整形・後続セクション骨組み作成・タイトル更新・タイプ/優先度ラベル付与・現状調査（コードベース/関連テスト/関連 Issue/PR/関連ドキュメント/再現実行）を行い、結果を本文に反映してユーザー確認待ちにする
---

# issue-triage

GitHub Issue を 1 件トリアージし、起票直後の状態から「分かっていることだけを整理した状態」へ持っていく。仕様や実装方針の決定は **しない**（後続の issue-spec 以降に任せる）。

## 入力

| 引数       | 内容    |
| ---------- | ------- |
| Issue 番号 | 例: 42  |

## コメント返信ルール（共通）

!`python "${CLAUDE_PLUGIN_ROOT}/scripts/gh/read_urls.py" "${WIKI_BASE}/gh-kit_規約_コメント.md"`

## ステップ 0: 起動時のラベル切り替え

```bash
gh issue edit {N} \
  --remove-label "$GH_KIT_LABEL_CONFIRM_ISSUE_TRIAGE" \
  --add-label "$GH_KIT_LABEL_PROCESSING_ISSUE_TRIAGE"
```


## ステップ 1: Issue 取得

```bash
gh issue view {N} --json number,title,body,labels,comments,assignees
```

## ステップ 2: 本文の整形・骨組み作成

### ステップ 2a: 既存本文の整文・整形

- ユーザー入力の誤字脱字・改行整理・文言修正を行う
- **ユーザーが書いた範囲を超えた内容を加えない**（情報の追加は後続フェーズ）

### ステップ 2b: 後続フェーズのセクション骨組みを作成

下記テンプレートに沿って、欠けているセクションを骨組みとして用意する。
issue-triage が自身で埋めるのは `## 概要` / `## 背景` / `## 現状` のみ。

### Issue 本文テンプレート
