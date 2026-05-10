---
paths:
  - "src/**/*.py"
---

# Implementation Work

## Before writing code

1. Confirm the spec exists in `wiki/`. If the relevant wiki doc is missing or contradicts the request, stop and surface that to the user.
2. If open Issues touch this area (`wiki/Issues.md`), notify the user before proceeding.
3. Read the `/py:py` skill before writing Python code.

## Pre-commit checklist

- [ ] Code / config files changed
- [ ] `docs/PR/PR{N}.md` created or updated
- [ ] Wiki documents updated if the implementation changes documented behavior
- [ ] `.gitignore` updated if new file types or directories were added
- [ ] New design decisions recorded in `wiki/Issues.md` or the relevant feature doc
