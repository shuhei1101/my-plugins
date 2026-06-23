---
name: gh-kit:pr-plan-review
description: Draft PR（PR プラン）と紐づく Issue を照合し、Issue で定義された問題が解決される計画になっているかをレビューする。合格時は 確認:pr-implementer ラベルを付与して pr-implement-auto に引き渡す。
---

# pr-plan-review

Draft PR 本文（PR プラン）と紐づく Issue を照合し、実装計画の妥当性をレビューする。
実装コードのレビューは行わない（それは `pr-review` スキルの責務）。

## 入力

| 引数 | 内容 |
|---|---|
| PR 番号 | 例: 42 |
| base ブランチ | 通常 `master` |

## ステップ 0: Wiki チェックリストを読み込む

Wiki から `PRプランレビューチェックリスト` ページを取得する。

```bash
REPO_SLUG=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
CHECKLIST=$(curl -fsSL "https://raw.githubusercontent.com/wiki/${REPO_SLUG}/PRプランレビューチェックリスト.md" 2>/dev/null)
if [ -n "$CHECKLIST" ]; then
  echo "$CHECKLIST"
else
  echo "[WARN] PRプランレビューチェックリスト.md が取得できませんでした。デフォルト観点でレビューします。" >&2
fi
```

取得したチェックリストはステップ 4 のレビューで参照する。

## ステップ 1: PR 情報を取得

```bash
gh pr view {N} --json number,title,body,headRefName,baseRefName,labels,assignees,isDraft,comments
```

PR が Draft でない場合は警告を出力して続行する（`pr-plan-review-auto` が Draft を起点とするが、手動実行では非 Draft も許容）。

## ステップ 2: 紐づく Issue を取得

PR 本文から Issue 番号を抽出し、Issue 本文とコメントを取得する。

```bash
# PR 本文から Issue 番号を抽出
ISSUE_N=$(gh pr view {N} --json body --jq '.body' | grep -oP '(?:Refs|Closes|Fixes) #\K[0-9]+' | head -1)
if [ -z "$ISSUE_N" ]; then
  echo "[ERROR] PR 本文から Issue 番号を抽出できませんでした。" >&2
  exit 1
fi
gh issue view "$ISSUE_N" --json number,title,body,labels,comments
```

Issue が取得できない場合は verdict = `failed` で終了する。

## ステップ 3: issue-reviewer コメントを読む

ステップ 2 で取得した Issue コメントの中から `issue-reviewer` によるレビュー結果コメント（`🤖 issue-reviewer による AI レビュー結果` 等を含むコメント）を抽出し、採用方針・QA 回答・実装方針確定事項を読み込む。

これらの情報をステップ 4 の照合チェックで参照する。

## ステップ 4: PR プランと Issue を照合・レビュー

ステップ 0 で取得した `PRプランレビューチェックリスト` の観点に従い、PR 本文と Issue 内容を照合する。

以下の各観点で finding を作成する:

| 観点 | 確認内容 |
|---|---|
| Issue 照合 | Issue の問題・課題がタスクリストで解決できる計画になっているか |
| タスクリスト品質 | タスクが具体的・実装可能な単位になっているか |
| PR 本文構造 | 必須セクション・`Refs #N` が揃っているか |
| issue-reviewer 方針反映 | issue-reviewer の確定方針・QA 回答がタスクリストに反映されているか |

各 finding の構造:

| フィールド | 内容 |
|---|---|
| `section` | 観点名（例: `Issue 照合`） |
| `severity` | `blocker` / `major` / `minor` / `nit` |
| `body` | 問題の説明と修正提案（Markdown） |

## ステップ 5: verdict を決定

| 優先度 | 条件 | verdict | 次の動作 |
|---|---|---|---|
| 1 | Issue 番号が取得できない | `failed` | ステップ 8-C へ |
| 2 | `blocker` / `major` を含む | `needs-revision` | ステップ 7 へ（`$GH_KIT_LABEL_CONFIRM_PR_IMPLEMENT` ラベル付与） |
| 3 | `minor` / `nit` のみ、または finding なし | `approved` | ステップ 6 へ（`$GH_KIT_LABEL_CONFIRM_PR_IMPLEMENTER` ラベル付与） |

## ステップ 6: 合格時 — 確認:pr-implementer ラベル付与

```bash
# 確認:pr-implementer ラベルを付与して pr-implement-auto に引き渡す
gh pr edit {N} --add-label "$GH_KIT_LABEL_CONFIRM_PR_IMPLEMENTER"
```

| 状況 | verdict |
|---|---|
| ラベル付与成功 | `approved` |
| 失敗 | `failed` |

## ステップ 7: 不合格時 — 確認:pr-implementer ラベル付与

```bash
gh pr edit {N} --add-label "$GH_KIT_LABEL_CONFIRM_PR_IMPLEMENT"
```

verdict = `needs-revision`。PR 作成者（`pr-planner`）が修正して `確認:pr-plan-reviewer` ラベルを再付与するまで待つ。

## ステップ 8: レビュー結果コメントを投稿

```bash
gh pr comment {N} --body "$(cat <<'EOF'
## 🤖 pr-plan-reviewer によるレビュー結果

**verdict**: {verdict}

### Issue 照合サマリ

紐づく Issue: #{ISSUE_N} — {ISSUE_TITLE}

{照合結果サマリ（合格観点・不合格観点の一覧）}

### Findings

{finding 一覧（severity / 観点 / 内容）}

### 次アクション

{verdict に応じた次アクション}
EOF
)"
```

## ステップ 9: 戻り値

```json
{
  "verdict": "approved" | "needs-revision" | "failed",
  "pr_number": 42,
  "issue_number": 222,
  "findings_count": {"blocker": 0, "major": 0, "minor": 1, "nit": 0},
  "message": "詳細メッセージ"
}
```

| フィールド | 内容 |
|---|---|
| `verdict` | レビュー結果区分 |
| `pr_number` | レビューした PR 番号 |
| `issue_number` | 照合した Issue 番号 |
| `findings_count` | severity 別 finding 数 |
| `message` | 詳細メッセージ・主要 finding 要約 |

## 制約

| No | 禁止 |
|---|---|
| 1 | 実装コードのレビューはしない（それは `pr-review` の責務） |
| 2 | マージはしない |
| 3 | 自身の中でサブエージェントを起動しない |
| 4 | `wip` ラベルを除去しない（`pr-implement-auto` の排他制御が壊れるため） |
