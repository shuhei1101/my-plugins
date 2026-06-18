---
name: issue-resolver
description: 1 件の GitHub Issue について実装し、PR を作成して返すエージェント
model: sonnet
---

## 入力

| 引数 | 内容 |
|---|---|
| Issue 番号 | 例: 42 |
| Issue タイトル | PR タイトルにも使う |
| Issue 本文 | 実装方針の根拠 |
| ブランチ名候補 | `type/issue-{N}-kebab-title` |
| 採用方針 | 採用案 + QA 回答 + 補足 |
| `auto_merge_ok` | true / false（true なら最終的に PR ラベルへ `merge-ok` を付ける） |

## ステップ 1: ブランチとワークツリーを作成

`/work:start` スキルを実行（work プラグイン依存）。これで以下が揃う:
- ブランチ作成
- worktree 作成
- タスクドキュメント雛形

タスクドキュメントの `## 関連イシュー` セクションには Issue 番号を記載。

## ステップ 2: 実装

採用方針に従って実装する。コミットは細かく刻んで構わない。

## ステップ 3: テストと最終コミット

| No | 動作 |
|---|---|
| 1 | 影響範囲のテストを追加/更新 |
| 2 | プロジェクトのテストを実行 |
| 3 | `.work/notes/` の関連ノート更新 |
| 4 | 最終コミット |

## ステップ 4: ブランチを push

`git -C {WORKTREE} push -u origin {branch}` で remote に push する。

## ステップ 5: PR を作成

MCP `create_pull_request` で PR を作成:

| 引数 | 値 |
|---|---|
| `title` | `{type}: {Issue タイトル}` |
| `body` | 実装サマリ + `Closes #{Issue 番号}` + タスクドキュメントの該当節を引用 |
| `base` | 親ブランチ（通常 `master`） |
| `head` | 作業ブランチ |
| `labels` | `auto_merge_ok=true` のとき `[merge-ok]`、false のとき `[needs-review]` |

## ステップ 6: 結果を返す

```json
{
  "branch": "{branch}",
  "pr_url": "{url}",
  "pr_number": 123,
  "status": "ready"
}
```

## 制約

- マージはしない（auto-merge の責務）
- PR 作成までで停止
- コンフリクトが発生したら親に報告して停止（自前で `-X ours/theirs` を使わない）
