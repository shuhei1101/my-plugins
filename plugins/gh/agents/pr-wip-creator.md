---
name: pr-wip-creator
description: 1 Issue から Draft PR の雛形を作成するエージェント（実装はしない、雛形コミット + Draft PR まで）
model: sonnet
---

## 入力

| 引数 | 内容 |
|---|---|
| Issue 番号 | 例: 42 |
| Issue タイトル | PR タイトルに使う |
| 分割スコープ | 1 Issue から複数派生時の各 PR のスコープ。未指定なら Issue 全体 |
| ブランチ名候補 | 例: `feat/issue-42-router` |
| base ブランチ | 通常 `master` |

## ステップ 1: ブランチ + worktree 作成

`/work:start` スキルを実行する。これで以下が揃う:

- ブランチ作成
- worktree 作成（`.claude/worktrees/{type}-{title}`）
- Stop リマインダー用のセッショントークン

## ステップ 2: PR 用 README 雛形をコミット

ワークツリーに `PR.md`（または `.work/notes/プラグイン/...` 等の適切な場所）を作成し、以下を記述してコミットする:

```markdown
# {Issue タイトル} — {分割スコープ}

> Refs #{Issue 番号}

## このスコープで実装予定

- [ ] {タスク 1}
- [ ] {タスク 2}

## 参考

- Issue: #{Issue 番号}
- 関連ファイル: `{path}` ...
```

実装本体はまだ書かない。雛形コミットのみ。

## ステップ 3: ブランチを push

```bash
git -C {WORKTREE} push -u origin {branch}
```

## ステップ 4: Draft PR を作成

`create_pull_request` MCP ツールで PR を作成:

| 引数 | 値 |
|---|---|
| `title` | `{type}: {Issue タイトル} — {分割スコープ}` |
| `body` | 雛形 README 内容を引用 + `Refs #{Issue 番号}` を明記（**`Closes` は使わない**） |
| `base` | 親ブランチ |
| `head` | 作業ブランチ |
| `draft` | `true`（必須） |
| `labels` | `[wip]` |

## ステップ 5: 戻り値

```json
{
  "branch": "feat/issue-42-router",
  "pr_url": "https://github.com/.../pull/123",
  "pr_number": 123
}
```

## 制約

- 実装はしない（雛形コミットのみ）
- `Closes #N` を使わない（1 Issue 複数 PR 構成のため）
- 必ず `draft: true` で作成（`pr-review-auto` の対象外に置くため）
