# work Stop Prompt Pair Sync

`stop.md` and `stop-no-merge.md` are a paired set of Stop hook prompts.
`stop-no-merge.md` is `stop.md` **minus step 4** (the merge suggestion).
When editing either file, keep steps 1–3 in sync between them.
Japanese mirror: `references/work-stop-prompt-sync.jp.md`

---

## Relationship

| File | Contents |
|---|---|
| `plugins/work/hooks/prompts/stop.md` | Steps 1–4: TODO/QA/notes reminder + `/work:merge` suggestion |
| `plugins/work/hooks/prompts/stop-no-merge.md` | Steps 1–3 only: TODO/QA/notes reminder (no merge suggestion) |

## When Editing

| Change | Action |
|---|---|
| Editing `stop.md` steps 1–3 | Apply the same change to `stop-no-merge.md` |
| Editing `stop.md` step 4 | No change needed in `stop-no-merge.md` |
| Never add step 4 to `stop-no-merge.md` | Its purpose is to omit the merge suggestion |

## Context

The Stop hook script in `hooks.json` selects between these two files based on `WORK_MERGE_PROPOSAL`:
- Truthy (default) → loads `stop.md`
- Falsy → loads `stop-no-merge.md`

## Checklist before committing

- [ ] Steps 1–3 are identical between `stop.md` and `stop-no-merge.md`
- [ ] Step 4 exists only in `stop.md`
- [ ] JP mirrors (`stop.jp.md`, `stop-no-merge.jp.md`) are updated in the same commit
