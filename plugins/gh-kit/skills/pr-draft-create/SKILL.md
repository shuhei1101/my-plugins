---
name: gh-kit:pr-draft-create
description: "Create a Draft PR for one Issue: fetch PR body template → worktree_create MCP → empty commit → push → gh pr create --draft. Called by pr-draft-creator agent."
---

# pr-draft-create

Create one Draft PR (empty commit only) from a single Issue.
Do NOT implement anything — implementation is handled by `/gh-kit:pr-implement`.

## Input

| Argument | Required | Content |
|---|---|---|
| Issue number | Yes | e.g. 42 |
| Issue title | Yes | Used to generate the PR title |
| branch type | Yes | e.g. `feat`, `fix`, `refactor` |
| branch title | Yes | kebab-case slug, e.g. `issue-42-router` |
| base branch | Yes | usually `master` |
| split scope | Optional | Scope label when 1 Issue → multiple PRs |

## Step 1: Fetch PR body template

Call the `template_get` tool from the `gh-kit-tools` MCP with `template_name: "PRドキュメント.j2"`.

Fill the returned template with actual values to use as the Draft PR body.

## Step 2: Create branch + worktree

Call the `worktree_create` tool from the `gh-kit-tools` MCP (pass `branch_type` and `title`).
Extract the worktree path from the return value.

## Step 3: Create an empty commit

A Draft PR requires at least one commit to be pushed.

```bash
git -C {WORKTREE} commit --allow-empty -m "chore: open draft PR for issue #{Issue number} ({split scope})"
```

If `split scope` is empty, omit it from the commit message.

## Step 4: Push the branch

```bash
git -C {WORKTREE} push -u origin {branch}
```

## Step 5: Create Draft PR via gh CLI

```bash
gh pr create \
  --draft \
  --base {base} \
  --head {branch} \
  --title "{type}: {Issue title}" \
  --body-file <(cat <<'EOF'
{template body filled with actual values}
EOF
)
```

Rules:
- Do NOT use `Closes #N` — use `Refs #N` at the top of the body (supports 1 Issue → multiple PRs).
- Always use `--draft`.
- Label assignment (`wip`, etc.) is the responsibility of the caller (`/gh-kit:pr-draft-create-auto`).

## Step 6: Return value

```json
{
  "branch": "feat/issue-42-router",
  "pr_url": "https://github.com/.../pull/123",
  "pr_number": 123
}
```

## Constraints

| No | Prohibited |
|---|---|
| 1 | Do not implement anything (empty commit only) |
| 2 | Do not use `Closes` — use `Refs` |
| 3 | Always use `--draft` |
| 4 | Do not create new Issues or branches beyond what worktree_create produces |
