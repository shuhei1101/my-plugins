# Incident: Unnecessary JP Mirror Sync Rule Created for Agent Files

## What happened

In PR137, a JP mirror sync rule (`agent-jp-mirror-sync.md`) was created for `plugins/{name}/agents/*.md` files,
following the pattern of `skill-jp-mirror-sync.md` and `hook-prompts-jp-mirror-sync.md`.
In PR141, the user deleted it as unnecessary.

## Why it was created

AI generalized from an existing pattern: SKILL.md and hook prompt files each have a dedicated sync rule,
so AI assumed agent files would also need one after they gained JP mirrors in PR133.

## Why it was unnecessary

1. **Warning comment is sufficient**: every `*.jp.md` already contains `<!-- This file is a Japanese mirror... -->`, which reminds editors to update both files.
2. **Agent files are rarely edited**: unlike SKILL.md (edited whenever a skill is updated) or hook prompts (edited when hook behavior changes), agent definition files are structural and infrequently modified. The high-frequency-edit assumption that justifies a sync rule does not apply.
3. **No path trigger that makes sense**: a useful sync rule loads automatically when a related file is *read*. Agent files are not read as frequently as SKILL.md or CLAUDE.md.

## Lesson

JP mirror sync rules are justified only for **frequently-edited, high-risk-of-drift** file types:

| File type | Sync rule needed? | Reason |
|---|---|---|
| `SKILL.md` | Yes | Edited on every skill update; JP mirror must stay in sync |
| `hooks/prompts/*.md` | Yes | Edited when hook behavior changes; directly injected into context |
| `CLAUDE.md` | Yes | Edited often; wrong JP mirror causes confusion |
| `agents/*.md` | **No** | Rarely edited; warning comment is sufficient |
| `*.jp.md` mirrors generally | No | The warning comment covers it |

## Correct approach

Do NOT create a dedicated sync rule for every file type that has a JP mirror.
Only create one when:
- The file type is edited frequently
- Missing the JP mirror update causes real confusion or bugs
- The warning comment alone is not enough
