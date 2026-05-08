## Overview
Add `yaml-rule` plugin — YAML file management conventions for assets and project configuration

## Tasks
- [ ] Create plugin directory structure
- [ ] Write SKILL.md (English, authoritative)
- [ ] Write SKILL.jp.md (Japanese reference)
- [ ] Register in marketplace.json
- [ ] Update CLAUDE.md / CLAUDE.jp.md plugin table

## Implementation
| Action | File path | Change |
|--------|-----------|--------|
| add | plugins/yaml-rule/.claude-plugin/plugin.json | plugin manifest |
| add | plugins/yaml-rule/skills/yaml-rule/SKILL.md | English skill definition |
| add | plugins/yaml-rule/skills/yaml-rule/SKILL.jp.md | Japanese reference |
| edit | .claude-plugin/marketplace.json | register yaml-rule |
| edit | CLAUDE.md | add yaml-rule to plugin table |
| edit | CLAUDE.jp.md | add yaml-rule to plugin table |

## Design Notes
### Skill content
- Asset/media files can be freely organized; programs reference them via YAML
- `index.yaml`: asset catalog, created once, environment-independent
- `settings.yaml`: environment-specific values (like .env), needs `settings.yaml.sample`
- Developer note block required at top of `index.yaml` and `settings.yaml.sample` (management rules + change history per PR/commit)
- `settings.yaml` actual file does NOT need a developer note
- No bilingual YAML split — index.yaml is not always AI-read; depends on the app
