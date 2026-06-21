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

## Step 2.5: Search for similar Issues

Extract 2–4 keywords from the Issue title and body, then search for open Issues using `gh issue list`:

```bash
# Run for each keyword combination (2–3 searches total, skip closed issues)
gh issue list --state open --search "{keyword1} {keyword2}" --json number,title,body --limit 20
```

Exclude the Issue being reviewed from results.
Collect up to 20 candidates total across all searches.

## Step 2.6: Similarity judgment and branching

Using the candidate list from Step 2.5, use LLM to judge similarity for each candidate.

Classify each pair as one of three categories:

| Category | Definition | Action |
|---|---|---|
| `partial_overlap` | Current Issue contains information not in the existing Issue, but topics overlap | Transfer additional info to existing Issue as comment → close current Issue with reference link |
| `full_duplicate` | Current Issue is completely covered by an existing Issue | Close current Issue with reference link (no comment transfer) |
| `unrelated` | No meaningful overlap | Skip (proceed to Step 3) |

**partial_overlap processing:**

```bash
# 1. Extract and summarize differential information (info in current Issue but not in existing Issue)
# 2. Post the extracted content as a comment on the existing Issue
gh issue comment {EXISTING_N} --body-file <(cat <<'EOF'
> 🤖 issue-reviewer による関連 Issue からの情報追記

## 追記情報（Issue #{N} より）

{差分要約: 既存 Issue に含まれていない追加情報のみを記載}

元 Issue: #{N}
EOF
)

# 3. Close the current Issue with a reference comment
gh issue comment {N} --body-file <(cat <<'EOF'
> 🤖 issue-reviewer による重複検出

類似する Issue #{EXISTING_N} が既に存在するため、この Issue をクローズします。
追加情報は #{EXISTING_N} にコメントとして転記しました。

移行先 Issue: {EXISTING_ISSUE_URL}
EOF
)
gh issue close {N}
```

**full_duplicate processing:**

```bash
# Close the current Issue with a reference comment
gh issue comment {N} --body-file <(cat <<'EOF'
> 🤖 issue-reviewer による重複検出

Issue #{EXISTING_N} と完全に重複しているため、この Issue をクローズします。

既存 Issue: {EXISTING_ISSUE_URL}
EOF
)
gh issue close {N}
```

When a `partial_overlap` or `full_duplicate` is found, **skip Steps 3–6** and jump directly to Step 7 with `status: "duplicate_merged"` or `status: "duplicate_closed"`.

If multiple candidates are found, prioritize by: highest similarity → smallest Issue number (oldest).

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

`status` possible values:

| Value | Meaning |
|---|---|
| `ok` | Normal review completed |
| `waiting` | AI review comment exists but user has not replied yet — caller ignores this issue |
| `duplicate_merged` | Partial overlap — differential info transferred to existing Issue, current Issue closed |
| `duplicate_closed` | Full duplicate — current Issue closed with reference link |

Label updates are the caller's responsibility (`issue-review-auto`).

## Constraints

- Do NOT rewrite the main Issue body (do not call the GitHub Issue `update` API)
- Skip Step 4 if all sections are already present or in `re-review` mode
- Always state a recommended approach explicitly (no "TBD" or "decide later")
- In `re-review` mode, read ALL comments to get full context (`gh issue view {N} --json comments`)
