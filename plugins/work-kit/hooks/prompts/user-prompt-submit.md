[work-kit] Before processing this prompt, check the current work context:

1. Read `docs/tasks/index.yaml` and identify any in-progress PR (`completed: false`)
2. If an in-progress PR exists, read its task document to understand the current state
3. Determine whether this request is:
   - A continuation of an existing PR → continue work in that worktree
   - New work → run `/work-kit:work-start` to create a worktree, branch, and PR doc first
4. Ensure the active PR's task document includes what you plan to do this session; add items if missing
