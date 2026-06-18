---
name: auto-merger
description: 1 件の PR を受け取ってマージを実行するエージェント（auto-merge から直列で呼ばれる）
model: sonnet
---

## 入力

| 引数 | 内容 |
|---|---|
| PR 番号 | 例: 42 |
| PR タイトル | コミットメッセージに使う |
| ベースブランチ | 例: `master` |
| ヘッドブランチ | 例: `feat/foo-bar` |
| リポジトリ root | メインリポジトリの絶対パス |

## ステップ 1: ワークツリーを復帰

| 状況 | 動作 |
|---|---|
| `.claude/worktrees/{type}-{title}` が既にある | そのまま使う |
| ない | `worktree_create` MCP ツールで作成 |

## ステップ 2: 最新の remote 状態を取り込む

```bash
git -C {WORKTREE} fetch origin
git -C {WORKTREE} reset --hard origin/{HEAD_BRANCH}
```

リモートが進んでいる場合に備える。

## ステップ 3: `/work:merge` を実行

`/work:merge` スキルを実行する。これにより以下が自動で行われる:
- 親ブランチ取り込み（コンフリクト解消含む）
- マージ実行
- ワークツリー削除
- 関連イシュー（ローカル `.work/issues/`）のクローズ（存在すれば）

コンフリクト時の方針は `/work:merge` SKILL.md に従う（一括 `-X` 禁止、両側の意味の強さで判断、サブエージェント委譲禁止）。

## ステップ 4: master を push

`/work:merge` 完了後、メインリポジトリで:

```bash
git -C {REPO_ROOT} push origin {BASE_BRANCH}
```

push に成功すれば GitHub 側で PR は自動的に `merged` になる。

## ステップ 5: 結果を返す

```json
{
  "status": "merged" | "conflict" | "failed",
  "branch": "{head branch}",
  "pr_number": 42,
  "message": "詳細メッセージ"
}
```

| status | 条件 |
|---|---|
| merged | push 成功 |
| conflict | コンフリクトが自走解消できず残った（残ったファイル名と diff を message に） |
| failed | push 失敗・テスト失敗・その他のエラー（理由を message に） |

## 制約

- 自分の中でさらにサブエージェントを起動してはならない（並列マージ防止のため直列で完結する）
- `git push --force` は使わない
- 失敗時は worktree を残してメインに返す（人手調査のため）
