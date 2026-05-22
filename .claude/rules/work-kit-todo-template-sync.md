---
paths:
  - "plugins/work-kit/templates/TODO.md"
  - "plugins/work-kit/templates/.work/tasks/yyyymmdd_xxx/PRXXX/TODO.md"
  - "plugins/work-kit/skills/work-start/SKILL.md"
---

# work-kit TODO Template Sync Rule

## Overview

Keep work-kit's TODO.md templates in sync with the Step 7 instructions in work-start SKILL.md.

If the section structure in TODO.md templates diverges from the fill-in guidance in
SKILL.md Step 7, generated TODO.md files will not match the documented workflow.
Whenever either side changes, update the other.

## Related Files

| File path | Role |
|---|---|
| `plugins/work-kit/templates/TODO.md` | Reference template shipped with the work-kit plugin |
| `plugins/work-kit/templates/.work/tasks/yyyymmdd_xxx/PRXXX/TODO.md` | Example template inside the `.work/` folder |
| `plugins/work-kit/skills/work-start/SKILL.md` | Skill that defines how to fill in TODO.md (Step 7) |

## When Editing

Whenever any file in this domain changes, verify the others:

- [ ] Section structure in `templates/TODO.md` matches the fill-in instructions in `SKILL.md` Step 7
- [ ] The example template (`templates/.work/.../TODO.md`) has the same sections as `templates/TODO.md`
- [ ] A newly added section has a corresponding fill-in instruction in `SKILL.md` Step 7
- [ ] A removed or renamed section has its corresponding `SKILL.md` Step 7 entry removed or updated
- [ ] If **a new template file was added**, have you updated `paths:` and the Related Files list in this rule?

## Rule Maintenance

When performing file operations in this domain:
- **Added a new template file** → add it to `paths:` and the Related Files list
- **Deleted or renamed a template file** → remove or update it in `paths:` and Related Files
- **SKILL.md structure changed significantly** → update the Overview section
