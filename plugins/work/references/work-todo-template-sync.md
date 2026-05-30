# work TODO Template Sync

Keep the task document template in sync with the fill-in guidance in `work-start` SKILL.md Step 7.
If the section structure in the template diverges from the fill-in guidance, generated task
documents will not match the documented workflow.
Japanese mirror: `references/work-todo-template-sync.jp.md`

---

## Related files

| File path | Role |
|---|---|
| `plugins/work/templates/note.md` | Note template shipped with the work plugin |
| `plugins/work/skills/start/SKILL.md` | Skill that defines how to fill in the task document (Step 7) |
| `plugins/work/skills/pr-handoff/SKILL.md` | Skill that reads `## 次PR候補` in the task doc (Step 1) to determine which PRs to reserve |

## When editing

Whenever any file in this domain changes, verify the others:

- [ ] Section structure in `templates/note.md` matches the fill-in instructions in `work-start` SKILL.md Step 7
- [ ] A newly added section has a corresponding fill-in instruction in SKILL.md Step 7
- [ ] A removed or renamed section has its SKILL.md Step 7 entry removed or updated
- [ ] If `## 次PR候補` is renamed or removed, update `pr-handoff` SKILL.md Step 1 to match
- [ ] If the columns of `## 次PR候補` change, update both `pr-handoff` and `work-start` SKILL.md Step 7

## Checklist before committing

- [ ] Template and SKILL.md Step 7 fill-in guidance are in sync
- [ ] `pr-handoff` SKILL.md Step 1 matches the `## 次PR候補` section structure
