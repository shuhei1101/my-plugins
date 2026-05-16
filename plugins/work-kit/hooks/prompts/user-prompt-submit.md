[work-kit] Check current work context before processing this prompt:

1. Scan `.work/tasks/` for an active PR (`PR{N}/` folder)
2. If found, read its `TODO.md`
3. Determine the request type:
   - Continuation of existing PR → continue in the correct worktree
   - New work → run `/work-kit:work-start` first

For detailed rules:
- Creating or updating TODO.md → use `/work-kit:todo`
- Recording or closing a QA entry → use `/work-kit:qa`
