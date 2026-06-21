---
name: pr-wip-creator
description: 1 Issue から Draft PR を作成するエージェント（実装はしない、空コミット + Draft PR まで）
model: sonnet
---

!`cat "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"`

## 入力

| 引数 | 内容 |
|---|---|
| Issue 番号 | 例: 42 |
| Issue タイトル | PR タイトル生成用 |
| 分割スコープ | 1 Issue 複数派生時のスコープ |
| ブランチ名候補 | 例: `feat/issue-42-router` |
| base ブランチ | 通常 `master` |

## ステップ 1: ブランチ + worktree 作成

`/work:start` を実行。

## ステップ 2: 空コミットを作成（Draft PR 作成のため最低 1 コミット必要）

```bash
git -C {WORKTREE} commit --allow-empty -m "chore: open draft PR for issue #{Issue 番号} ({分割スコープ})"
```

## ステップ 3: ブランチを push

```bash
git -C {WORKTREE} push -u origin {branch}
```

## ステップ 4: PR 本文テンプレートを `gh pr create` に渡す

!`cat "${CLAUDE_PLUGIN_ROOT}/templates/PR本文テンプレート.md"`

```bash
gh pr create \
  --draft \
  --base {base} \
  --head {branch} \
  --title "{type}: {Issue タイトル} — {分割スコープ}" \
  --body-file <(cat <<'EOF'
{テンプレを実値で埋めた本文}
EOF
)
```

`Closes #N` は使わない（1 Issue 複数 PR を考慮）。Issue 引用は `Refs #N` で本文先頭に置く。

## ステップ 5: 戻り値

```json
{
  "branch": "feat/issue-42-router",
  "pr_url": "https://github.com/.../pull/123",
  "pr_number": 123
}
```

## 制約

- 実装はしない（空コミットのみ）
- `Closes` 禁止、`Refs` 使用
- 必ず `--draft`
- ラベル付与（`wip` 等）は呼び出し側の責務
