Direct commit to master/main detected.

**Run `/work-kit:work-start` to create a worktree, then commit there.**

Correct flow:
1. Run `/work-kit:work-start` to create a PR branch and worktree
2. Commit inside the worktree (`../repo-wt-PR{N}/`)
3. Run `/work-kit:merge` to merge into master

If committing directly to master is truly necessary, ask the user for explicit permission first.
