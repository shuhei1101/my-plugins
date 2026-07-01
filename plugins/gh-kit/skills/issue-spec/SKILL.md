---
name: gh-kit:issue-spec
description: Issue の機能要件・非機能要件・スコープ外を確定させ、フェーズ終了時に worktree + Draft PR 作成 + PR 本文骨組み配置を行う。Issue フェーズの最終ステップ。
argument-hint: "[issue-number]"
arguments: "issue_number"
---

# issue-spec

Issue のシステム要件（SA）を確定させる。「**何を作るか**」（要件レベル）まで扱い、UI 設計 / システム方式設計（SS）/ 実装計画は **PR 側** に移管する。

フェーズ終了時に **worktree + Draft PR 作成 + `## 紐づく Issue` 記入 + PR 本文骨組み配置** を実施し、後続の pr-ui / pr-arch にバトンを渡す。

## 入力

- Issue 番号: $issue_number

## コメント返信ルール（共通）

!`python "${CLAUDE_PLUGIN_ROOT}/scripts/gh/read_urls.py" "${WIKI_BASE}/gh-kit/規約/コメント.md"`

## ステップ 0: 起動時のラベル切り替え

```bash
gh issue edit $issue_number \
  --remove-label "$GH_KIT_LABEL_CONFIRM_ISSUE_SPEC" \
  --add-label "$GH_KIT_LABEL_PROCESSING_ISSUE_SPEC"
```


## ステップ 1: Issue 取得

```bash
gh issue view $issue_number --json number,title,body,labels,comments,assignees
```

`## 概要` / `## 背景` / `## 現状`（issue-triage が整備済）を読み込んで要件を整理する土台にする。

## ステップ 2: システム要件（SA）を本文に整理

`## システム要件（SA）` セクションの 3 サブセクションを埋める。骨組みは issue-triage が用意済み。

### ステップ 2a: `### 機能要件`

**No / カテゴリ / 要件 / 補足** の表形式で整理する。

- **カテゴリ**: `編集機能` / `閲覧機能` / `バリデーション` / `エラー表示` / `状態表示` / `レスポンシブ対応` など
- **エラーハンドリング / バリデーション / レスポンシブ対応の有無** はここに含める
- 情報源: `## 概要` / `## 背景` / `## 現状` + ユーザーとの対話

各サブエージェントに **注入する Wiki ページ**（`docs/wiki/` 配下、相対パス）:
- 該当領域の `設計図/バックエンド結合/README.md`（既存エンドポイント一覧）
- 該当領域の `設計図/フロントエンド結合/*.md`（既存画面操作）

### ステップ 2b: `### 非機能要件`

**No / カテゴリ / 要件 / 補足** の表形式で整理する。

- **カテゴリ**: `性能` / `セキュリティ` / `運用` など
- **当てはまるものがある時のみ書く**（該当なしなら「なし」 or サブセクション自体を空表で残す）
- 情報源: ユーザー要望・既存システムの SLA

### ステップ 2c: `### スコープ外`

**No / 項目 / 理由 / 補足** の表形式で整理する。

- 「今回はやらないこと」を明示
- 情報源: 機能要件・関連 Issue・ユーザー対話

