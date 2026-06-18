---
name: gh:issue-resolve
description: 指定された GitHub Issue を 1 件解決する（ブランチ作成 → 実装 → PR 作成）
---

# issue-resolve — Issue を解決する

## 入力

| 引数 | 必須 | 内容 |
|---|---|---|
| Issue 番号 | 必須 | 例: `#42`。指定がなければユーザーに聞く |
| 採用方針 | 任意 | コメント欄で議論済みの結論を引用する場合 |

## タスク

### ステップ 1: Issue を読み込む

MCP `get_issue` で本文・ラベル・コメントを取得する。

`assignee` を自分（または bot user）に設定し、ラベルに `in-progress` を追加する（`update_issue`）。

### ステップ 2: 実装方針を確定

| 観点 | 判定 |
|---|---|
| 対応案が複数 | 直近コメントで採用案が決まっているか確認。決まってなければユーザーに `AskUserQuestion` で聞く（このスキルは AskUserQuestion 使用可） |
| `auto-merge` ラベルが付いているか | 付いていれば PR 作成後にレビューフェーズを飛ばして `targets/`（auto-merge 対象）に流す（ラベル `merge-ok` を付ける） |

### ステップ 3: ブランチ作成 → 実装

[サブエージェントで実行・完了を待つ] `issue-resolver` サブエージェントに以下を渡して起動する。
（戻り値: `{branch, pr_url, pr_number, status}`）

入力:
- Issue 番号 / Issue タイトル / Issue 本文
- ブランチ名候補（`type/issue-{N}-kebab-title`）
- 採用方針（採用案 + 補足）
- `auto_merge_ok`（`auto-merge` ラベルの有無）

### ステップ 4: 後処理

| 結果 | 動作 |
|---|---|
| PR 作成成功 + `auto_merge_ok=true` | PR にラベル `merge-ok` を付与（`add_labels`）。`/gh:auto-merge` が拾う |
| PR 作成成功 + `auto_merge_ok=false` | PR にラベル `needs-review` を付与。ユーザーがレビュー後 `merge-ok` ラベルへ手動で切替 |
| 失敗 | Issue に失敗理由をコメント投稿し、`in-progress` ラベルを外す |

### ステップ 5: 結果報告

| No | 報告項目 |
|---|---|
| 1 | 作成したブランチ名 |
| 2 | 作成した PR URL と番号 |
| 3 | 次のアクション（auto-merge 待ち / ユーザーレビュー待ち / 失敗対応） |

## 注意

- このスキルは PR 作成までで終わる（マージはしない）。マージは `/gh:auto-merge` の責務
- Issue クローズも GitHub 側に任せる（PR 本文に `Closes #N` を入れる → マージ時に自動クローズ）
