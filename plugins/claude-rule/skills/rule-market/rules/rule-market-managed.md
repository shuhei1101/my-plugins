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

Or run the sync script directly (locate it first):
```powershell
Get-ChildItem ~/.claude -Recurse -Filter "sync_rules.py" |
  Where-Object { $_.FullName -like "*claude-rule*" }
python <script-path> sync <project-root> <rule-name>
```

After syncing, update the JP mirror in `rules-jp/` and bump the plugin version.

</policy>

## Market-installed rules in this project

<!-- Add each installed rule name here when installing via rule-market: -->
<!-- - cascade-sync -->
<!-- - auto-register -->
