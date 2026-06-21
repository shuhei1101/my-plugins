---
name: gh-kit:pr-implement
description: "Implement a single wip Draft PR: restore worktree → fetch/reset → implement → commit → push → gh pr ready. Called by pr-implementer agent."
---

# pr-implement

Implement the content of one existing Draft PR and mark it Ready for review.
Do NOT create new branches or PRs.

## Input

| Argument | Required | Content |
|---|---|---|
| PR number | Yes | e.g. 42 |
| branch | Yes | e.g. `feat/issue-42-router` |
| base branch | Yes | usually `master` |
| Issue number | Yes | linked Issue number |
| adopted policy | Yes | extracted from `issue-reviewer` comment on the Issue |
| split scope | Optional | scope handled by this PR (when 1 Issue → multiple PRs) |

## Step 1: Load needs-user-review judgment criteria

```bash
cat "${CLAUDE_PLUGIN_ROOT}/templates/ユーザーレビュー要否判定.md"
```

Referenced in Step 5.

## Step 2: Restore worktree and sync with remote

```bash
WT=".claude/worktrees/$(echo {branch} | tr '/' '-')"
if [ ! -d "$WT" ]; then
  echo "worktree missing, please call gh-kit-tools worktree_create MCP for branch={branch}" >&2
  exit 1
fi
git -C "$WT" fetch origin
git -C "$WT" reset --hard origin/{branch}
```

## Step 3: Implement

Follow the adopted policy and split scope to make code changes. Commits may be granular.

| No | Action |
|---|---|
| 1 | Change code according to the adopted policy |
| 2 | Add / update tests for affected scope |
| 3 | Run project tests |

## Step 4: Push

```bash
git -C "$WT" push origin {branch}
```

## Step 5: Re-evaluate `needs-user-review`

Based on the criteria loaded in Step 1, determine `needs_user_review: true|false` from the actual code changes.
The judgment may differ from the one made at Issue creation time (e.g., if what was planned as a refactor turns out to touch specs → true).

## Step 6: Mark PR Ready

```bash
gh pr ready {PR_NUMBER}
gh pr comment {PR_NUMBER} --body "Implementation complete. Awaiting review. {change summary}"
```

Label assignment (`needs-ai-review` / `needs-user-review`) is the responsibility of the caller (`/gh-kit:pr-implement-auto`).

## Step 7: Return value

```json
{
  "branch": "feat/issue-42-router",
  "pr_number": 42,
  "status": "ready",
  "needs_user_review": true,
  "commits_added": 5,
  "message": "detailed message"
}
```

## Constraints

| No | Prohibited |
|---|---|
| 1 | Do not create new branches or PRs |
| 2 | Do not merge |
| 3 | Stop and report to caller on conflict (no `-X ours/theirs`) |
| 4 | Do not use `git push --force` |
