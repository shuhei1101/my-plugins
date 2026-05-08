## Overview
Update wt skill to use --no-ff merge to preserve branch history

## Tasks
- [ ] Update merge command in Phase 4 to use --no-ff
- [ ] Update merge command in Key Git Commands Reference to use --no-ff
- [ ] Bump version to 1.0.3 in plugin.json and marketplace.json

## Implementation
| Action | File path | Change |
|--------|-----------|--------|
| edit | plugins/wt/skills/wt/SKILL.md | add --no-ff to merge commands |
| edit | plugins/wt/.claude-plugin/plugin.json | bump version to 1.0.3 |
| edit | .claude-plugin/marketplace.json | bump wt version to 1.0.3 |
