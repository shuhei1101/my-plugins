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
| 分割スコープ | 1 Issue 複数派生時のスコープ |
| ブランチ名候補 | 例: `feat/issue-42-router` |
| base ブランチ | 通常 `master` |

## ステップ 1: ブランチ + worktree 作成

`/work:start` スキルを実行する。

## ステップ 2: PR 用 README 雛形をコミット

ワークツリーに `PR.md` を作成し以下を記述してコミットする:

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

## ステップ 3: ブランチを push

```bash
git -C {WORKTREE} push -u origin {branch}
```

## ステップ 4: gh CLI で Draft PR を作成

```bash
gh pr create \
  --draft \
  --base {base} \
  --head {branch} \
  --title "{type}: {Issue タイトル} — {分割スコープ}" \
  --body-file <(cat <<'EOF'
{PR 本文 = README + Refs #N}
EOF
)
```

`Closes #N` は使わない（1 Issue 複数 PR を考慮）。

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
- `Closes #N` を使わない
- 必ず `--draft` で作成
