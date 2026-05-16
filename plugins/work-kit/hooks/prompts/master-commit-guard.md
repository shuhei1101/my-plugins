Direct commit to master/main detected.

**Run `/work-kit:work-start` to create a worktree, then commit there.**

Correct flow:
1. Run `/work-kit:work-start` to create a PR branch and worktree
2. Commit inside the worktree (`../repo-wt-PR{N}/`)
3. Run `/work-kit:merge` to merge into master

If committing directly to master is truly necessary:
1. Ask the user for explicit permission
2. After the user grants permission, create a one-time permission token:
   ```
   python -c "import pathlib,tempfile; pathlib.Path(tempfile.gettempdir(),'work-kit-master-commit-guard-allowed').touch()"
   ```
3. Then retry the commit
