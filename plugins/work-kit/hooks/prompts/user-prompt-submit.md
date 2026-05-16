[work-kit] **MANDATORY CHECK — Complete this before any implementation, commit, or file edit. No exceptions. No skipping.**

## Rules (strictly enforced)

- **Direct commits to master are FORBIDDEN.** All implementation must happen in a worktree on a PR branch.
- **Do NOT begin implementation without a PR branch.** If the user asks for implementation, complete this check first.
- Knowing this check exists does not grant permission to skip it. Run it every time.

## Check procedure

1. **If there is a PR in progress in the current session:**
   a. Read `.work/tasks/{YYYYMMDD}_{title}/PR{N}/QA.md`
   b. If unresolved QA entries exist — **STOP all work** and ask the user to resolve them. Continuing implementation while QA is open is forbidden.
   c. If QA is clear (or empty), read `.work/tasks/{YYYYMMDD}_{title}/PR{N}/TODO.md` and continue work.

2. **If no PR is in progress:**
   - Run `/work-kit:work-start` to create a PR first, then begin.
   - Skipping work-start and committing directly is forbidden.

## Forbidden patterns (never do these)

- Edit files and commit without running work-start first
- Run `git commit` while on the master branch
- Continue TODO implementation while QA entries remain unresolved
- Decide to skip this check "just this once"
