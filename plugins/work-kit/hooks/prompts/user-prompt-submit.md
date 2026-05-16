[work-kit] Check current work context before processing this prompt:

1. Read `.work/tasks/index.yaml` and find PRs with `completed: false`
2. If an in-progress PR exists:
   a. Read `.work/tasks/{YYYYMMDD}_{title}/PR{N}/QA.md`
   b. If unresolved QA entries exist, ask the user to resolve them before proceeding — do not continue with TODO while QA is open
   c. If QA is clear (or empty), read `.work/tasks/{YYYYMMDD}_{title}/PR{N}/TODO.md` and continue work
3. If no in-progress PR → run `/work-kit:work-start` first
