---
name: gh-kit:issue-review
description: Review one Issue — fetch templates, read codebase, post a body-supplement comment (if needed), post a review/re-review result comment, and return re_review_needed judgment.
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
| `re_review_needed` judgment criteria | `ユーザーレビュー要否判定.md` |

## Step 2: Fetch Issue, labels, and comments — determine review mode

```bash
gh issue view {N} --json number,title,body,labels,comments
```

**Determine review mode:**

| Condition | Mode |
|---|---|
| No existing AI review comment in `comments` | `initial` — perform first review |
| AI review comment exists **and** user has replied after it | `re-review` — read user reply, check if further questions are needed |
| AI review comment exists but no user reply yet | `waiting` — skip (no action, return status "waiting") |

**Determine Issue origin (for Step 4):**

| Label | Origin | Body state |
|---|---|---|
| `ai-code-scan` present | claude code (`code-scanner`) | Template-compliant, complete |
| absent | Human | May be missing sections (overview, background, etc.) |

## Step 3: Read codebase

Use the Read tool to check the areas and related files mentioned in the Issue.
The PreToolUse hook auto-injects file-level rules on each Read call.

## Step 4: Post body-supplement comment (only when needed — `initial` mode only)

Only when the Issue was human-authored **and** sections are missing: post an **additive comment** filling in only the missing sections, following `イシュードキュメント.j2`.
Do NOT restate sections already present.
Skip this step entirely when the body is already complete or in `re-review` mode.

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

**`initial` mode:** Using `レビュー結果コメント.j2` fetched in Step 1, write the implementation policy, questions, split proposals, and impact scope.
Omit sections for questions and split proposals when there are none.

**`re-review` mode:** Read all comments via `gh issue view {N} --json comments` (full context).
Check whether the user's reply resolves all outstanding questions from the previous AI review.
- If further questions remain → post an **additional QA comment** only (do not repeat the full review).
- If all questions are resolved → post a short confirmation comment (e.g. "ご回答確認しました。Draft PR 作成に進みます。").

```bash
gh issue comment {N} --body-file <(cat <<'EOF'
{review result body}
EOF
)
```

## Step 6: Determine `re_review_needed`

**`initial` mode:** `re_review_needed: true` when Step 5 includes questions or a split proposal (i.e. the user needs to reply before Draft PR creation can proceed). Otherwise `false`.

**`re-review` mode:**
- Further questions posted → `re_review_needed: true`
- All resolved → `re_review_needed: false`

## Step 7: Return value

```json
{
  "issue_number": 42,
  "re_review_needed": true,
  "status": "ok"
}
```

(`status` can be `"ok"` or `"waiting"` — caller ignores `"waiting"` issues.)

Label updates are the caller's responsibility (`issue-review-auto`).

## Constraints

- Do NOT rewrite the main Issue body (do not call the GitHub Issue `update` API)
- Skip Step 4 if all sections are already present or in `re-review` mode
- Always state a recommended approach explicitly (no "TBD" or "decide later")
- In `re-review` mode, read ALL comments to get full context (`gh issue view {N} --json comments`)
