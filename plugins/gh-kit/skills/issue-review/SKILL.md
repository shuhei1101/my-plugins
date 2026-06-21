---
name: gh-kit:issue-review
description: Review one Issue — fetch templates, read codebase, post a body-supplement comment (if needed), post a review-result comment, and return needs_user_review judgment.
---

# issue-review

Reviews one GitHub Issue and posts the result as comments via gh CLI.

!`cat "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"`

## Input

| Argument | Content |
|---|---|
| Issue number | e.g. 42 |

## Step 1: Load label definitions and templates

Label constants are sourced via bash (injected above via `!` syntax).
Fetch template bodies via the `gh-kit-tools` MCP `template_get` tool:

| Purpose | template_name |
|---|---|
| Issue body template | `イシュードキュメント.j2` |
| Review result comment | `レビュー結果コメント.j2` |
| `needs-user-review` criteria | `ユーザーレビュー要否判定.md` |

## Step 2: Fetch Issue and labels

```bash
gh issue view {N} --json number,title,body,labels,comments
```

Determine the origin from label presence:

| Label | Origin | Body state |
|---|---|---|
| `ai-code-scan` present | claude code (`code-scanner`) | Template-compliant, complete |
| absent | Human | May be missing sections (overview, background, etc.) |

## Step 3: Read codebase

Use the Read tool to check the areas and related files mentioned in the Issue.
The PreToolUse hook auto-injects file-level rules on each Read call.

### Step 3a: Fetch official documentation (only when external tool/library names are present)

If the Issue title or body contains the name of an external tool, library, framework, or service:
1. Use `WebFetch` to retrieve the official documentation page(s) most relevant to the Issue.
2. If fetching fails, note "参照不可（理由）" and continue without blocking.
3. Record each successfully retrieved URL in `{doc_urls}` for use in the review-result comment.

Skip entirely when the Issue contains no external tool/library names.

## Step 3.5: Behavior verification (optional — when feasible)

Attempt to confirm whether the reported problem actually occurs in the current codebase.

| Issue type | Verification method |
|---|---|
| Skill / Claude Code behavior | Launch a sub-agent and reproduce the scenario described in the Issue |
| Code bug (test exists) | Run the relevant test suite and check for failures |
| Code bug (no test) | Perform manual behavior confirmation |
| Verification not feasible | Note "確認不可（理由）" and continue |

Store the result in `{verification_result}` for inclusion in the review-result comment.
This step is **optional** — if infrastructure or context makes it impossible, skip gracefully.

## Step 4: Post body-supplement comment (only when needed)

Only when the Issue was human-authored **and** sections are missing: post an **additive comment** filling in only the missing sections, following `イシュードキュメント.j2`.
Do NOT restate sections already present.
Skip this step entirely when the body is already complete (AI-authored or human-authored but complete).

```bash
gh issue comment {N} --body-file <(cat <<'EOF'
> 🤖 issue-reviewer による本文補完

## 概要
（欠けていた概要を記入）

## 背景
（欠けていた背景を記入）
EOF
)
```

## Step 5: Post review-result comment

Using `レビュー結果コメント.j2` fetched in Step 1, write the implementation policy, questions, split proposals, and impact scope.
Omit sections for questions and split proposals when there are none.

```bash
gh issue comment {N} --body-file <(cat <<'EOF'
{review result body}
EOF
)
```

## Step 6: `needs-user-review` judgment

Evaluate against `ユーザーレビュー要否判定.md` fetched in Step 1.
Unconditionally `true` when Step 5 includes questions or a split proposal.

## Step 7: Return value

```json
{
  "issue_number": 42,
  "needs_user_review": true,
  "status": "ok"
}
```

Label updates are the caller's responsibility (`issue-review-auto`).

## Constraints

- Do NOT rewrite the main Issue body (do not call the GitHub Issue `update` API)
- Skip Step 4 if all sections are already present
- Always state a recommended approach explicitly (no "TBD" or "decide later")
