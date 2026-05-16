[work-kit] Check current work context before processing this prompt:

1. Read `.work/tasks/index.yaml` and find PRs with `completed: false`
2. If an in-progress PR exists, read its `TODO.md`
3. Determine the request type:
   - Continuation of existing PR → continue in the correct worktree
   - New work → run `/work-kit:work-start` first
