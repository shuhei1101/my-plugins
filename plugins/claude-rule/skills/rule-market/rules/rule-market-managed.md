---
paths:
  - ".claude/rules/**/*.md"
---

# Rule Market Managed Rules

<when_to_apply>
When editing any file under .claude/rules/.
</when_to_apply>

<policy>

Some rules in this project were installed from the `claude-rule` plugin's rule-market library.
If you modify one of those rules and want to contribute the improvement back to the library,
use the sync operation:

```
/claude-rule:rule-market sync <rule-name>
```

Or run the sync script directly. The script writes to the plugin's **source repository**,
not the cache. Steps:

1. Find the marketplace source repo (search for `marketplace.json` in common repo locations).
2. Locate the sync script in the cache:
   ```bash
   # Bash
   find ~/.claude -name "sync_rules.py" -path "*claude-rule*" 2>/dev/null | head -1
   ```
   ```powershell
   # PowerShell
   Get-ChildItem ~/.claude -Recurse -Filter "sync_rules.py" | Where-Object { $_.FullName -like "*claude-rule*" } | Select-Object -First 1 -ExpandProperty FullName
   ```
3. Run it:
   ```bash
   python <script-path> sync <project-root> <rule-name> --plugin-repo <marketplace-repo-root>
   ```
4. Update the JP mirror in `rules-jp/`, bump plugin version, and commit in the source repo.

</policy>

## Market-installed rules in this project

<!-- Add each installed rule name here when installing via rule-market: -->
<!-- - cascade-sync -->
<!-- - auto-register -->
