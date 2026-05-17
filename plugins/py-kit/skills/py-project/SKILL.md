---
name: py-kit:py-project
description: >
  Work with an existing Python project — review code quality, add features, refactor, or fix bugs.
  Covers both checking and implementation. Trigger when the user is working on an already-existing
  Python codebase (not starting from scratch).
  Examples: "このコード見て", "機能追加して", "リファクタして", "バグ直して", "コードレビューして".
  Do NOT trigger for new projects — use py-kit:py-new-project instead.
---

# py-kit:py-project — Existing Python Project

Reviews, extends, or fixes an existing Python project while keeping it aligned with py-kit standards.

---

## Tasks

### Step 1: Load standards

Read the shared Python standards:

```
{plugin_root}/references/python-standards.md
```

Read the entire document. This skill uses all sections depending on what the task requires.

→ Proceed to Step 2

---

### Step 2: Understand project structure

#### Process

1. Read the project's top-level directory listing.
2. Identify the layer structure: is DDD used? What layers exist?
3. Read `pyproject.toml` (if present) to understand dependencies and package config.
4. Identify the main entry point and any existing tests.
5. Note any existing `.claude/rules/` files.

→ Proceed to Step 3

#### Output

- Project structure understood: layers, entry points, dependencies, test coverage

---

### Step 3: Quality check

#### Process

1. Check naming conventions (modules, classes, functions, variables) against the standards.
2. Check type hint coverage — flag any missing annotations.
3. Check for SOLID violations:
   - SRP: classes with multiple reasons to change?
   - OCP: open/elif chains that should be Strategy pattern?
   - DIP: concrete class instantiation inside high-level classes?
4. Check DDD boundary violations: domain layer importing infrastructure? Application layer containing domain logic?
5. Check Pydantic usage at system boundaries.
6. Report findings. For a review-only request, stop here and present the report.

→ Proceed to Step 4 if implementation is needed

---

### Step 4: Implement changes

#### Process

1. Apply the task (feature addition, refactor, bug fix).
2. Follow all standards from the reference document.
3. Apply type hints everywhere in new/modified code.
4. Do not create abstractions beyond what the task requires — but do design for extensibility when adding new modules.
5. Inject dependencies via constructor — do not instantiate concrete classes in class bodies.
6. Write `print()` / logger output in English only.

→ Proceed to Step 5

---

### Step 5: Rule check

#### Process

1. Check if any of the following changed during this task:
   - Abstract classes, Protocols, or concrete classes implementing them
   - Configuration files (`.yaml`, `.toml`, `.env`, `.json`)
   - Source files that read configuration
   - Source files that have corresponding test files
2. For each changed type, apply the relevant rule:
   - **Class structure change** → check all classes in the inheritance / Protocol hierarchy for needed updates
   - **Config change** → check source files that read this config; or vice versa
   - **Source change** → check corresponding test files need updating
3. If `.claude/rules/` does not yet exist in the project, create it now using the templates from `{plugin_root}/rules/`.

→ Proceed to Step 6

#### Output

- Rule linkage verified; related files flagged for update if needed

---

### Step 6: Update tests

#### Process

1. Identify test files corresponding to any changed source files (mirror path: `src/foo/bar.py` → `tests/foo/test_bar.py`).
2. Update or create test cases for the changed behavior.
3. Tests mock only external I/O boundaries (DB, API, filesystem) — no unit tests for individual methods.
4. Run `pytest` and confirm tests pass.

→ Done

#### Output

- Affected test files updated and passing

---

## References

See `{plugin_root}/references/python-standards.md`:
- SOLID Principles
- DDD (Domain-Driven Design)
- Extensibility-Focused Design
- Naming Conventions
- Type Hints
- Pydantic Boundaries
- Test Policy
- Comment Rules
- Language Rules
