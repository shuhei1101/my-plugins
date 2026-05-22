---
paths:
  - "plugins/claude-kit/skills/conversation-to-claude/**"
  - "plugins/claude-kit/skills/skill-creator/**"
  - "plugins/claude-kit/skills/rule-creator/**"
  - "plugins/claude-kit/skills/hook-creator/**"
  - "plugins/claude-kit/skills/claude-creator/**"
---

# claude-kit Skill Dependencies

## Overview

`conversation-to-claude` delegates to four creator skills in Step 3.
When editing any of these files, check that the delegation interface stays consistent.

## Related Files

| File | Role |
|---|---|
| `plugins/claude-kit/skills/conversation-to-claude/SKILL.md` | Orchestrator — calls creator skills in Step 3 |
| `plugins/claude-kit/skills/skill-creator/SKILL.md` | Delegate for skill creation |
| `plugins/claude-kit/skills/rule-creator/SKILL.md` | Delegate for rule creation |
| `plugins/claude-kit/skills/hook-creator/SKILL.md` | Delegate for hook creation |
| `plugins/claude-kit/skills/claude-creator/SKILL.md` | Delegate for CLAUDE.md authoring |

## When Editing

- Changed `conversation-to-claude` Step 3 delegation table → verify the target creator skill still accepts the same context
- Changed a creator skill's expected inputs → update `conversation-to-claude`'s "Context to pass" column
- Added a new artifact type to `conversation-to-claude` → add the corresponding creator skill row

## Rule Maintenance

- Added a new creator skill → add it to `paths:` and the Related Files table
- Renamed or removed a creator skill → update `paths:` and Related Files accordingly
