---
name: gh-kit:code-scan-auto
description: コードベースを観点ごとにスキャンし、見つかった問題を gh issue create で起票する
---

# code-scan-auto

メインは観点を選んで `code-scanner` サブエージェントに振り分けるだけ。

## 環境変数

| 変数 | 既定 | 用途 |
|---|---|---|
| `GH_KIT_CODE_SCAN_PARALLEL` | `5` | 並列起動するスキャナー数 |

## タスク

### ステップ 1: 既存 Issue を確認

```bash
gh issue list --state all --label "$GH_KIT_LABEL_AI_CODE_SCAN" --limit 50
```

直近の起票を取得し、観点の重複を避ける材料にする。

### ステップ 2: スキャン観点を N 件選ぶ

!`cat "${CLAUDE_PLUGIN_ROOT}/templates/観点メニュー.md"`

このメニューから既存 Issue とかぶらない観点を **N** 件（`GH_KIT_CODE_SCAN_PARALLEL`）選ぶ。

### ステップ 3: code-scanner を並列起動

[サブエージェントで並列実行・完了を待つ] 観点ごとに `code-scanner` を 1 体ずつ並列起動する。
（戻り値: `[{issue_number, issue_url, title}]`）

各サブエージェントに渡す入力: 観点（メニューから 1 件抜粋）

### ステップ 4: 起票結果に対して issue-review-auto を連鎖実行

ステップ 3 で 1 件以上 Issue が起票されたら、続けて `/gh-kit:issue-review-auto` を呼び出して
新規 Issue を AI レビューしてしまう（`needs-ai-review` 付きの Issue が対象）。
