# Subagent Delegation Guide

When and how to delegate step processing to subagents inside a skill.
Japanese mirror: `references/subagents.jp.md`

---

## Delegation markers

Mark steps delegated to a subagent with one of the markers below, placed at the start of the step item.
Include the return value in parentheses:

| Marker | When to use |
|---|---|
| `[subagent: run · await]` | Single subagent, awaited before continuing |
| `[subagent: parallel · await all]` | Multiple subagents in parallel, all awaited before continuing |
| `[subagent: parallel · no-await]` | Fire-and-forget — rare; only when the result is never needed |

**Example:**

```markdown
#### Process
1. [subagent: parallel · await all] Glob .claude/skills/ and collect each description
   (return: `[{name, description}]`)
→ Proceed to Step 2
```

---

## When to delegate

| Situation | Verdict |
|---|---|
| Little context needed (chat history / file content barely referenced) | ✅ Good for subagent |
| Simple conversion, transcription, or translation | ✅ Good for subagent |
| Same processing applied to multiple files or items in parallel | ✅ Good for subagent |
| Want to prevent main agent context bloat | ✅ Good for subagent |
| Must reference a large amount of main-agent conversation history | ❌ Run in main agent |
| The subagent's internal processing is also needed by the main agent | ❌ Run in main agent |

---

## Constraints

- **Return value only**: the subagent's internal processing detail does not return to the main agent. Confirm that the return value alone is sufficient.
- **Await by default**: `no-await` (fire-and-forget) is rare. Even when running multiple subagents in parallel, await all before proceeding.
- **Empty context**: a subagent starts with no conversation history. Pass all required information explicitly in the prompt.
