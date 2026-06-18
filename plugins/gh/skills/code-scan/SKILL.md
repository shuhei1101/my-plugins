---
name: gh:code-scan
description: コードベースを観点ごとにスキャンし、見つかった問題を GitHub Issues に起票する
---

# code-scan — コードベーススキャン

メインは観点を選んで `code-scanner` サブエージェントに振り分けるだけ。起票はスキャナーが行う。

## 環境変数

| 変数 | 既定 | 用途 |
|---|---|---|
| `GH_CODE_SCAN_PERSPECTIVES` | `5` | 1 回のスキャンで起動するスキャナー数（観点数） |

## タスク

### ステップ 1: 既存 Issue を確認

MCP `list_issues` / `search_issues` で open + 直近クローズ済みの Issue を取得し、観点の重複を避ける材料にする（ラベル `code-scan` 付きを優先）。

### ステップ 2: スキャン観点を N 件選ぶ

下記メニューから既存 Issue とかぶらない観点を **N** 件選ぶ。

!`cat "${CLAUDE_PLUGIN_ROOT}/templates/code-scan-perspectives.md"`

### ステップ 3: code-scanner を並列起動

[サブエージェントで並列実行・完了を待つ] 観点ごとに `code-scanner` を 1 体ずつ並列起動する。
（戻り値: `[{issue_number, issue_url, title}]` の配列）

各サブエージェントに渡す入力:
- 観点: 何をスキャンするか（このメニューから 1 件抜粋）

### ステップ 4: 完了報告

| No | 報告項目 |
|---|---|
| 1 | 起票された Issue 番号と URL の一覧 |
| 2 | findings 0 件で終わった観点（あれば） |
