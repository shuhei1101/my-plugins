---
name: gh-kit:pr-review
description: Review a single PR. If approved and needs-user-review is absent, take over base branch, resolve conflicts if needed, merge with --no-ff, remove worktree, and push.
---

# pr-review

Reviews one PR and, when it passes, merges it into the base branch automatically.

## Input

| Argument | Content |
|---|---|
| PR number | e.g. 42 |
| Base branch | e.g. `master` |
| Head branch | e.g. `feat/foo-bar` |
| Repository root | Absolute path to the main repository |
| Current label list | Used to check for the `needs-user-review` label |

## Step 1: Load review criteria

```bash
cat "${CLAUDE_PLUGIN_ROOT}/templates/観点メニュー.md"
```

Use this in Step 3 as the review checklist.

## Step 2: Fetch PR information

```bash
gh pr view {N} --json number,title,body,headRefName,baseRefName,labels,statusCheckRollup,comments,reviews,isDraft
gh pr diff {N} > /tmp/pr-{N}.diff
```

If CI status is `failure`, return `failed` and stop.

## Step 3: File scan and rule injection

Read the changed files with the Read tool. The PreToolUse hook automatically injects file-level rules — these form the primary review criteria.
Combine with the criteria menu from Step 1 to audit the diff.

When a finding originates from an injected rule, note `Rule: {name}` at the top of the body.

## Step 4: Build findings list

Structure for each finding:

| Field | Content |
|---|---|
| `path` | File path |
| `line` | Line number |
| `side` | `RIGHT` / `LEFT` |
| `severity` | `blocker` / `critical` / `major` / `minor` / `nit` |
| `body` | Comment body (Markdown) — why it is a problem + suggestion, 2-4 lines |

## Step 5: Post review via gh CLI

```bash
gh pr review {N} \
  --approve|--comment|--request-changes \
  --body-file <(cat <<'EOF'
{criteria-based summary}
EOF
)
# For inline comments use: gh api repos/:owner/:repo/pulls/{N}/comments
```

Event decision:

| Condition | Event | Next action |
|---|---|---|
| Contains blocker / critical / major | `--request-changes` | Step 7-A (do not merge) |
| Only minor / nit + no `needs-user-review` | `--approve` | Step 6 (proceed to merge) |
| Only minor / nit + `needs-user-review` present | `--approve` | Step 7-B (do not merge) |

## Step 6: Merge (approve + no needs-user-review only)

Sync the worktree, take in the base branch, resolve any conflicts, merge with `--no-ff`, remove the worktree, and push.

```bash
WT=".claude/worktrees/$(echo {HEAD_BRANCH} | tr '/' '-')"
git -C "$WT" fetch origin
git -C "$WT" reset --hard origin/{HEAD_BRANCH}
git -C "$WT" merge origin/{BASE_BRANCH}
```

If conflicts remain, inspect them with `git -C "$WT" status -s` (look for UU / AA / DD codes). Read both sides and resolve by preserving the stronger intent — never use `-X ours` / `-X theirs` for bulk resolution. After resolving: `git -C "$WT" add` / `git -C "$WT" commit`.

```bash
git -C {REPO_ROOT} merge --no-ff -m "{type}: {title}" {HEAD_BRANCH}
```

Call the `worktree_remove` tool from the `gh-kit-tools` MCP (`branch={HEAD_BRANCH}`) to delete the worktree and branch. Then push:

```bash
git -C {REPO_ROOT} push origin {BASE_BRANCH}
```

| Outcome | Verdict |
|---|---|
| All steps succeeded | `approved-merged` |
| Conflict could not be auto-resolved | `conflict` |
| Other failure | `failed` |

## Step 7-A: changes-requested

Do not merge. Return `verdict = changes-requested` with a summary of the key findings in `message`.

## Step 7-B: approved-user-review-pending

Do not merge. Return `verdict = approved-user-review-pending` with `message` stating "awaiting user review" and the reason.

## Step 8: Return value

```json
{
  "verdict": "approved-merged" | "approved-user-review-pending" | "changes-requested" | "conflict" | "failed",
  "pr_number": 42,
  "branch": "feat/foo-bar",
  "message": "Detailed message",
  "findings_count": {"blocker": 0, "critical": 0, "major": 1, "minor": 2, "nit": 3}
}
```

## Constraints

| No | Prohibited |
|---|---|
| 1 | Do not launch sub-agents internally |
| 2 | Do not use `git push --force` |
| 3 | Do not merge a PR that has `needs-user-review` without human approval |
| 4 | Do not post inline comments on lines far from the changed lines |
