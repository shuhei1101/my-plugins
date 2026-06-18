---
name: gh-kit:pr-wip-create
description: needs-* がすべて外れた open Issue を全件取り、各 Issue から Draft PR-WIP を作成する（1 Issue 複数派生対応）
---

# pr-wip-create

「実装着手 OK」になった Issue を全件巡回し、それぞれから Draft PR を作る。
1 Issue から複数派生してよい。実装は別途 `/gh-kit:pr-implement-auto` が担当。

「実装着手 OK」の条件:

| No | 条件 |
|---|---|
| 1 | `state: open` |
| 2 | `needs-ai-review` / `needs-user-review` / `needs-fix` / `processing` のいずれも付いていない |
| 3 | Issue 本文・コメントの todo チェックボックス（`- [ ]`）がすべて埋まっている（推奨案・QA 回答が選択済み） |

## 環境変数

| 変数 | 既定 | 用途 |
|---|---|---|
| `GH_KIT_PR_WIP_CREATE_PARALLEL` | `5` | 並列起動するサブエージェント上限件数 |

## 入力

| 引数 | 必須 | 内容 |
|---|---|---|
| Issue 番号 | 任意 | 指定時はその 1 件のみ処理 |
| 分割スコープ | 任意 | 1 Issue から複数派生する場合のスコープ名（カンマ区切り） |

引数なしのときは上記条件の Issue を全件取得し、`issue-review` の AI コメントの分割提案を読んで自動で分割スコープを決定する。

## ラベル定義の読み込み

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
```

## タスク

### ステップ 1: 対象 Issue を収集

```bash
gh issue list --state open --json number,title,body,labels,comments --limit 100
```

取得結果を以下でフィルタ:

- `needs-ai-review` / `needs-user-review` / `needs-fix` / `processing` のいずれも含まない
- Issue 本文・コメントを連結して `- [ ]` の残数 0（推奨案・QA 回答が選択済み）

0 件なら停止。

### ステップ 2: 各 Issue から作る Draft PR の数を決定

| 条件 | 作る PR 数 |
|---|---|
| `issue-review` コメントに分割提案表あり | 分割提案表の行数（各スコープ 1 PR） |
| 引数で分割スコープ指定あり | 指定数 |
| 上記なし | 1 PR（Issue 全体） |

各 Draft PR の生成タスクを並列実行待ち行列に積む（上限 **N**）。

### ステップ 3: 排他制御

```bash
gh issue edit {N} --add-label "$LABEL_PROCESSING"
```

### ステップ 4: pr-wip-creator を並列起動

[サブエージェントで並列実行・完了を待つ] 各 Draft PR 生成タスクに `pr-wip-creator` サブエージェントを起動する。
（戻り値: `[{branch, pr_url, pr_number}]`）

入力:
- Issue 番号 / タイトル
- 分割スコープ（未指定なら Issue 全体）
- ブランチ名候補: `{type}/issue-{N}-{kebab-scope}`
- base ブランチ

### ステップ 5: 後処理

```bash
# 作成された各 PR にラベル wip を付与
gh pr edit {PR番号} --add-label "$LABEL_WIP"

# 元 Issue にコメント追加 + processing 解除
gh issue comment {N} --body "PR #{番号} を起票（スコープ: {scope}）"
gh issue edit {N} --remove-label "$LABEL_PROCESSING"
```

### ステップ 6: 完了報告

| No | 報告項目 |
|---|---|
| 1 | 対象 Issue 件数 / 作成した Draft PR 件数 |
| 2 | 各 PR の URL と紐づく Issue 番号 |
| 3 | 次のアクション（`/gh-kit:pr-implement-auto` を実行） |

## 注意

| No | 内容 |
|---|---|
| 1 | 必ず **draft** で作成（`--draft` フラグ） |
| 2 | `Closes #N` ではなく `Refs #N` を使う |
| 3 | 同一 Issue から派生する PR はブランチ名のスコープで識別 |
