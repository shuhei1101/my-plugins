---
description: >
  Template for the config-source-link rule. Deploy to .claude/rules/config-source-link.md.
  Triggers when configuration files or source files that read config are modified,
  and prompts synchronization between the two.
---

# py-kit rule template: config-source-link
# Copy to: {project}/.claude/rules/config-source-link.md
# Adjust paths to match your project's config and source locations.

---
paths:
  - "*.yaml"
  - "*.yml"
  - "*.toml"
  - "*.json"
  - ".env.sample"
  - "src/**/config.py"
  - "src/**/settings.py"
  - "src/**/constants.py"
---

# Config ↔ Source Linkage

When any file matching this rule's paths is modified:

## If a configuration file changed (yaml / toml / json / .env.sample)

1. Find source files that read this config:
   - Search for the config filename or key names in `src/`
   - Check `config.py` and `settings.py` for related fields
2. Verify the source still correctly reads the updated structure:
   - New keys added → does the source handle missing keys (default or validation error)?
   - Keys renamed or removed → update source to match
   - Type changed → update Pydantic model or type annotation in source

## If a source file that reads config changed (config.py / settings.py / constants.py)

1. Check corresponding config files for consistency:
   - New fields in the source → add to `.env.sample` and schema files
   - Removed fields → clean up config files
2. Check Pydantic models at the boundary match the config structure

## Tip

Keep config key names and source field names identical to make this check mechanical.
