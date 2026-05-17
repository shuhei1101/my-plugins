---
description: >
  Template for the source-test-link rule. Deploy to .claude/rules/source-test-link.md.
  Triggers when source files are modified and prompts an update to corresponding test files.
---

# py-kit rule template: source-test-link
# Copy to: {project}/.claude/rules/source-test-link.md
# Adjust paths to match your project's source layout.

---
paths:
  - "src/**/*.py"
---

# Source ↔ Test Linkage

When any source file matching this rule's paths is modified:

## Check before committing

1. **Find the corresponding test file:**
   - Mirror the source path: `src/foo/bar/baz.py` → `tests/foo/bar/test_baz.py`
   - If no test file exists yet, decide whether one should be created

2. **Determine if tests need updating:**
   - New public function or method added → add a test case
   - Existing function signature changed → update call sites in tests
   - Behavior changed → update assertions
   - Function removed → remove corresponding test case

3. **Test scope reminder:**
   - Write use case tests (end-to-end through the application layer)
   - Write integration tests for non-obvious module interactions
   - Mock only external I/O boundaries (DB, API, filesystem, message queue)
   - Do NOT write unit tests for individual private methods

4. **Run tests:**
   ```
   pytest tests/
   ```
   All tests must pass before committing.

## Mirror structure

```
src/
  {package}/
    application/
      order_service.py       ←→   tests/application/test_order_service.py
    domain/
      entities/
        user.py              ←→   tests/domain/entities/test_user.py
    infrastructure/
      postgres_repo.py       ←→   tests/infrastructure/test_postgres_repo.py
```
