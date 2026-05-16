[work-kit] Before processing this prompt, check the current work context:

1. Scan `docs/tasks/` for in-progress PRs (`PR{N}/` folders)
2. If an in-progress PR exists, read its `TODO.md` to understand the current state
3. Determine whether this request is:
   - A continuation of an existing PR → check TODO.md and continue in the correct worktree
   - New work → run `/work-kit:work-start` to create the task/PR folder and TODO.md first
4. Check `docs/QA.md` for open questions relevant to this request
5. Check `docs/specs/` for relevant specifications
6. Ensure the active TODO.md includes what you plan to do this session; add items if missing
