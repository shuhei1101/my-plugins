# incidents-glossary-jp-mirror-missing — incidents/glossary JP Mirror Not Updated

## What happened

After editing `incidents.md` or `glossary.md`, the corresponding JP mirror files under
`rules-jp/core/` were not updated, leaving English and Japanese versions diverged for
an extended period.

## Root cause

No rule existed that enforced simultaneous JP mirror updates when `incidents.md` or
`glossary.md` were edited. The existing `skill-jp-mirror-sync.md`,
`hook-prompts-jp-mirror-sync.md`, and `claude-md-jp-mirror-sync.md` rules did not
cover `rules/core/incidents.md` and `rules/core/glossary.md`.

## Fix (PR112)

Added `incidents-glossary-jp-mirror-sync.md` rule that requires updating
`rules-jp/core/incidents.md` and `rules-jp/core/glossary.md` in the same commit
whenever the English originals are changed.

## Prevention

When creating a new JP mirror sync rule, also check whether other similar files
in the same directory follow the same "must sync JP mirror" pattern, and add
explicit rules for each category from the start.
