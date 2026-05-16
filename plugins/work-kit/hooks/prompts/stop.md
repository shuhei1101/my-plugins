[work-kit] Before finishing this response:

1. Read `.work/tasks/index.yaml` to identify the PR with `completed: false`
2. Update `.work/tasks/{YYYYMMDD}_{title}/PR{N}/TODO.md` and mark completed tasks as `- [x]`
3. If all items are `- [x]`, **suggest** that the user run `/work-kit:merge` — do nothing more

⚠️ **Strictly forbidden**: Claude must never automatically invoke or execute `/work-kit:merge`.
Merging requires explicit user approval. Never merge for any reason without direct instruction from the user.
