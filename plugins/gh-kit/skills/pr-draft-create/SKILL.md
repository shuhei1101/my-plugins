---
name: gh-kit:pr-draft-create
description: "1 Issue から Draft PR を作成する: PR 本文テンプレ取得 → worktree_create MCP → 空コミット → push → gh pr create --draft。pr-draft-creator エージェントから呼ばれる。"
---

# pr-draft-create

1 件の Issue から Draft PR（空コミットのみ）を作成する。
実装は行わない — 実装は `/gh-kit:pr-implement` が担当。

## 入力

| 引数 | 必須 | 内容 |
|---|---|---|
| Issue 番号 | 必須 | 例: 42 |
| Issue タイトル | 必須 | PR タイトル生成に使う |
| ブランチ種別 | 必須 | 例: `feat`, `fix`, `refactor` |
| ブランチタイトル | 必須 | ケバブケース、例: `issue-42-router` |
| base ブランチ | 必須 | 通常 `master` |
| 分割スコープ | 任意 | 1 Issue 複数 PR の場合のスコープ名 |

## ステップ 0: Wiki チェックリストを読み込む

`GH_KIT_CHECKLIST_PAGES` が設定されている場合に限り、指定されたチェックリストページをリモート Wiki から取得してコンテキストに注入する。
ページが存在しない場合は警告を出力して続行する。

```bash
REPO_SLUG=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
IFS=',' read -ra PAGES <<< "${GH_KIT_CHECKLIST_PAGES:-共通チェックリスト}"
for PAGE in "${PAGES[@]}"; do
  PAGE=$(echo "$PAGE" | xargs)  # trim whitespace
  CONTENT=$(curl -fsSL "https://raw.githubusercontent.com/wiki/${REPO_SLUG}/${PAGE}.md" 2>/dev/null)
  if [ -n "$CONTENT" ]; then
    echo "# Wiki チェックリスト: $PAGE"
    echo "$CONTENT"
  else
    echo "[INFO] Wiki チェックリストページが見つかりません: ${PAGE}.md" >&2
  fi
done
```

取得できたチェックリスト内容は、Draft PR 本文・タスクリストの作成時に参照する。

## ステップ 1: PR 本文テンプレートを取得

リモート Wiki から `PRドキュメント` ページを取得する。

```bash
curl -fsSL "https://raw.githubusercontent.com/wiki/$(gh repo view --json nameWithOwner --jq '.nameWithOwner')/PRドキュメント.md"
```

返却されたテンプレートを実値で埋め、Draft PR 本文として使用する。

## ステップ 2: ブランチ + worktree を作成

`gh-kit-tools` MCP の `worktree_create` ツールを呼ぶ（`branch_type` と `title` を渡す）。
戻り値からワークツリーパスを取得する。

## ステップ 3: 空コミットを作成

Draft PR を作成するには最低 1 件のコミットが必要。

```bash
git -C {WORKTREE} commit --allow-empty -m "chore: open draft PR for issue #{Issue 番号} ({分割スコープ})"
```

分割スコープが空の場合は括弧ごと省略する。

## ステップ 4: ブランチを push

```bash
git -C {WORKTREE} push -u origin {branch}
```

## ステップ 5: gh CLI で Draft PR を作成

```bash
gh pr create \
  --draft \
  --base {base} \
  --head {branch} \
  --title "{type}: {Issue タイトル}" \
  --body-file <(cat <<'EOF'
{ステップ 1 のテンプレを実値で埋めた本文}
EOF
)
```

ルール:
- `Closes #N` は使わない — 本文先頭に `Refs #N` を置く（1 Issue 複数 PR に対応）。
- 必ず `--draft` を付ける。
- ラベル付与（`wip` 等）は呼び出し側（`/gh-kit:pr-draft-create-auto`）の責務。

## ステップ 6: Issue の優先度ラベルを PR に継承

Issue に `$GH_KIT_LABEL_PRIORITY_URGENT` または `$GH_KIT_LABEL_PRIORITY_LOW` ラベルが付いていれば、同じラベルを Draft PR にも付与する。
これにより `pr-implement-auto` と `pr-review-auto` の優先度順処理が正しく機能する。

```bash
# Issue のラベルを取得
ISSUE_LABELS=$(gh issue view {Issue 番号} --json labels --jq '.labels | map(.name) | .[]')

# 優先度ラベルを PR に継承
if echo "$ISSUE_LABELS" | grep -q "$GH_KIT_LABEL_PRIORITY_URGENT"; then
  gh pr edit {pr_number} --add-label "$GH_KIT_LABEL_PRIORITY_URGENT"
elif echo "$ISSUE_LABELS" | grep -q "$GH_KIT_LABEL_PRIORITY_LOW"; then
  gh pr edit {pr_number} --add-label "$GH_KIT_LABEL_PRIORITY_LOW"
fi
```

## ステップ 7: 戻り値

```json
{
  "branch": "feat/issue-42-router",
  "pr_url": "https://github.com/.../pull/123",
  "pr_number": 123
}
```

## 制約

| No | 禁止 |
|---|---|
| 1 | 実装はしない（空コミットのみ） |
| 2 | `Closes` 禁止 — `Refs` を使う |
| 3 | 必ず `--draft` |
| 4 | worktree_create が生成するもの以外のブランチや Issue を作らない |
