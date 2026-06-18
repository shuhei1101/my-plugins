---
name: gh-kit:code-scan-auto
description: コードベースを観点ごとにスキャンし、見つかった問題を gh issue create で起票する
---

# code-scan-auto

メインは観点を選んで `code-scanner` サブエージェントに振り分けるだけ。
起票はスキャナーが `gh issue create` で直接行う。

## 環境変数

| 変数 | 既定 | 用途 |
|---|---|---|
| `GH_KIT_CODE_SCAN_PARALLEL` | `5` | 1 回のスキャンで起動するスキャナー数 |
| `GH_KIT_SCAN_PERSPECTIVES_PATH` | （未設定時は同梱版） | スキャン観点メニューのパス |

## タスク

### ステップ 1: 既存 Issue を確認

`gh issue list --state all --label code-scan --limit 50` で直近の起票を取得し、観点の重複を避ける材料にする。

### ステップ 2: スキャン観点を N 件選ぶ

スキャン観点メニューを直展開する（未設定なら同梱版）。

!`cat "${GH_KIT_SCAN_PERSPECTIVES_PATH:-${CLAUDE_PLUGIN_ROOT}/templates/スキャン観点.md}"`

このメニューから既存 Issue とかぶらない観点を **N** 件（`GH_KIT_CODE_SCAN_PARALLEL`）選ぶ。

### ステップ 3: code-scanner を並列起動

[サブエージェントで並列実行・完了を待つ] 観点ごとに `code-scanner` を 1 体ずつ並列起動する。
（戻り値: `[{issue_number, issue_url, title}]` の配列）

各サブエージェントに渡す入力: 観点（このメニューから 1 件抜粋）

### ステップ 4: 完了報告

| No | 報告項目 |
|---|---|
| 1 | 起票された Issue 番号と URL の一覧 |
| 2 | findings 0 件で終わった観点（あれば） |
