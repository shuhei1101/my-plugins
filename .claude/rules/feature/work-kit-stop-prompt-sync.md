---
paths:
  - "plugins/work-kit/hooks/prompts/stop.md"
  - "plugins/work-kit/hooks/prompts/stop-no-merge.md"
---

# work-kit Stop Prompt Pair Sync

`stop.md` and `stop-no-merge.md` are a paired set of Stop hook prompts.
`stop-no-merge.md` is `stop.md` **minus step 4** (the merge suggestion).
When editing either file, keep steps 1–3 in sync between them.

## Relationship

| File | Contents |
|---|---|
| `stop.md` | Steps 1–4: TODO/QA/notes reminder + `/work-kit:merge` suggestion |
| `stop-no-merge.md` | Steps 1–3 only: TODO/QA/notes reminder (no merge suggestion) |

## When Editing

- **Editing `stop.md` steps 1–3** → apply the same change to `stop-no-merge.md`
- **Editing `stop.md` step 4** → no change needed in `stop-no-merge.md`
- **Never add step 4 to `stop-no-merge.md`** — its purpose is to omit the merge suggestion

## Context

The Stop hook inline Python in `hooks.json` selects between these two files based on `WORK_KIT_MERGE_PROPOSAL`:
- Truthy (default) → loads `stop.md`
- Falsy → loads `stop-no-merge.md`

Added in PR173.
