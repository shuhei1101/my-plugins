---
name: py-kit:py-project
description: >
  Work with a Python project — create a new project from scratch, or review/extend/refactor/fix
  an existing one. Covers both new project scaffolding (layered architecture, DI, rules, tests)
  and existing project work (quality review, feature addition, refactor, bug fix).
  Examples: "新しい Python プロジェクト作って", "土台から作りたい", "このコード見て",
  "機能追加して", "リファクタして", "バグ直して", "コードレビューして".
  Do NOT trigger for simple one-off scripts — use py-kit:py-script instead.
---

# py-kit:py-project — Python Project (New or Existing)

Handles full Python projects: either creates a new layered project from scratch
or works on an existing codebase while keeping it aligned with py-kit standards.

---

## Tasks

### Step 1: Load standards

Read the index file to identify which references to load:

```
{plugin_root}/references/python/_index.md
```

The plugin root is two levels above this skill file (e.g. `Base directory: .../skills/py-project` → plugin root is `.../{plugin-name}/`).

Then read:
- `{plugin_root}/references/python/python-core.md` — always required
- `{plugin_root}/references/python/python-architecture.md` — always required for projects
- `{plugin_root}/references/python/python-testing.md` — required for new projects and test-related tasks
- `{plugin_root}/references/python/python-fastapi.md` — if the project uses FastAPI
- `{plugin_root}/references/python/python-llm.md` — if the project calls LLM APIs

→ Proceed to Step 2

---

### Step 2: Determine mode (new vs existing)

#### Process

Identify whether the user wants to create a new project or work on an existing one:

| Signal | Mode |
|---|---|
| User says "新規"、"create a new project"、"土台から作りたい"、no project files yet | **New** — proceed to Step 3 |
| User says "このコード見て"、"機能追加"、"リファクタ"、"レビュー"、project already exists | **Existing** — skip to Step 9 |

If ambiguous, ask the user. Then branch:

- **New project** → continue with Step 3 (requirements gathering for the new project)
- **Existing project** → skip to Step 9 (understand project structure)

---

## New Project Path (Steps 3–8)

### Step 3: Requirements gathering

#### Process

1. Confirm the project name and package name (`snake_case`).
2. Describe the project: what problem does it solve? Who calls it?
3. List the key use cases (3–5 verbs: "process order", "generate report", etc.).
4. Identify external dependencies: databases, APIs, file systems, message queues.
5. Confirm the interface type: CLI / FastAPI / tkinter GUI / background worker.
6. Confirm environment variable requirements.

→ Proceed to Step 4

#### Output

- Use cases, external dependencies, interface type confirmed

---

### Step 4: Layer design

#### Process

1. Decide how to split code into layers (folder names are free — use what fits the project).
2. Identify which code touches external services and isolate it in a boundary layer.
3. Define `Protocol` interfaces in the business logic layer for each external boundary.
4. Plan concrete implementations in the boundary layer (DB client, HTTP adapter, file adapter, etc.).
5. Confirm composition root placement: where will all concrete classes be wired together?
6. Present the layer plan to the user for confirmation before generating code.

→ Proceed to Step 5

#### Output

- Layer plan confirmed: business logic, external boundaries, and their Protocol interfaces

---

### Step 5: Generate project scaffold

#### Process

1. Create the directory structure based on the layer plan (see `python-architecture.md`: Project Folder Structure for reference).
2. Create `pyproject.toml` with Python `>= 3.11` and dependencies pinned with `~=`.
3. Create `.gitignore` (include: `.env`, `__pycache__/`, `*.pyc`, `venv/`, `.venv/`, `log/`, `cache/`).
4. Create `.env.sample` with all required environment variable keys and placeholder values.
5. On Windows: create `setup/setup_venv.bat` (ASCII only) and `activate.bat`. Skip on Linux/macOS.
6. Add `.gitkeep` to empty folders (`log/`, `input/`, `output/`, `cache/` if used).
7. Create stub files for all planned modules (empty with correct imports and type stubs).
8. Create `logger.py` per the Logger Specification in `python-testing.md`.
9. Create `constants.py` with `PROJECT_ROOT` and `LOG_DIR` only — no magic numbers or strings.

→ Proceed to Step 6

#### Notes

##### Prohibitions

- Do not put `.bat` files in a `bat/` subfolder — all bat files go in the project root (Windows only)
- Do not put `README.md` in empty folders — use `.gitkeep` only
- Do not instantiate concrete classes inside class bodies — always inject via constructor
- Do not hardcode any config values, URLs, ports, paths, or credentials in source code

---

### Step 6: Dependency injection wiring

#### Process

1. Create `Protocol` definitions for all external boundary interfaces.
2. Create a composition root (typically `main.py` or a dedicated `container.py`) where all concrete implementations are instantiated and injected.
3. Verify: no high-level business logic class imports a concrete external-library class directly.
4. Apply Strategy / Factory / Decorator patterns where appropriate per `python-architecture.md`.

→ Proceed to Step 7

#### Output

- All dependencies flow from the composition root; business logic layers import only Protocols

---

### Step 7: Create linkage rules

After the scaffold is generated, create rules to keep implementation, docs, and tests in sync.
Use the `/claude-kit:rule-creator` skill for each rule below.

#### Rules to create

1. **Class structure linkage** — links Protocols and their concrete implementations.
   Trigger: any class in the inheritance or Protocol hierarchy changes.
   Check: verify the full hierarchy for ripple effects (signatures, LSP, sibling classes).

2. **Config ↔ source linkage** — links config files (`.yaml`, `.toml`, `.env`, `.json`) and the source files that read them.
   Trigger: config file or config-reading source file changes.
   Check: new/renamed/removed keys propagate to both sides.

3. **Source ↔ test linkage** — links source files and test files.
   Trigger: source file changes.
   Check: corresponding test file is updated.

#### Process

For each rule above, run `/claude-kit:rule-creator` and provide:
- The files to link (globs)
- The trigger condition
- The check to perform

Commit after all rules are created:
```
git add .claude/rules/ && git commit -m "chore: add py-kit rules"
```

→ Proceed to Step 8

#### Output

- Three rules created in `.claude/rules/` via `/claude-kit:rule-creator`

---

### Step 8: Create test skeleton

#### Process

1. Create `tests/conftest.py` with shared pytest fixtures.
2. Create `tests/mocks/mock_env.py` (environment variable mocking helper).
3. Create `tests/mocks/mock_externals.py` (stubs for external API / DB clients).
4. For each planned use case, create a corresponding `tests/{feature}/test_{feature}.py` stub.
5. Tests mock only external I/O boundaries — no unit tests for individual methods.

→ Done (new project flow complete)

#### Output

- Test skeleton created mirroring the source structure

---

## Existing Project Path (Steps 9–13)

### Step 9: Understand project structure

#### Process

1. Read the project's top-level directory listing.
2. Identify the layer structure: is DDD used? What layers exist?
3. Read `pyproject.toml` (if present) to understand dependencies and package config.
4. Identify the main entry point and any existing tests.
5. Note any existing `.claude/rules/` files.

→ Proceed to Step 10

#### Output

- Project structure understood: layers, entry points, dependencies, test coverage

---

### Step 10: Quality check

#### Process

1. Check naming conventions (modules, classes, functions, variables) against `python-core.md`.
2. Check type hint coverage — flag any missing annotations.
3. Check for SOLID violations (see `python-architecture.md`):
   - SRP: classes with multiple reasons to change?
   - OCP: open/elif chains that should be Strategy pattern?
   - DIP: concrete class instantiation inside high-level classes?
4. Check layer separation:
   - Does business logic import external libraries directly (DB drivers, HTTP clients)?
   - Are all external service calls behind a `Protocol` interface?
   - Is the composition root the only place where concrete classes are instantiated?
5. Check for hardcoded values:
   - Magic numbers, string literals (URLs, ports, file paths, credentials) embedded in source code?
   - All config values should come from `.env` / config files via `constants.py` or `config.py`
6. Check for duplicate logic.
7. Check Pydantic usage at system boundaries.
8. Report findings. For a review-only request, stop here and present the report.

→ Proceed to Step 11 if implementation is needed

---

### Step 11: Implement changes

#### Process

1. Apply the task (feature addition, refactor, bug fix).
2. Follow all standards from the reference documents.
3. Apply type hints everywhere in new/modified code.
4. Do not create abstractions beyond what the task requires.
5. Inject dependencies via constructor — do not instantiate concrete classes in class bodies.
6. Write `print()` / logger output in English only.

→ Proceed to Step 12

---

### Step 12: Rule check

#### Process

1. Check if any of the following changed during this task:
   - Abstract classes, Protocols, or concrete classes implementing them
   - Configuration files (`.yaml`, `.toml`, `.env`, `.json`)
   - Source files that read configuration
   - Source files that have corresponding test files
2. For each changed type, apply the relevant rule.
3. If `.claude/rules/` does not yet exist in the project, create the rules now using `/claude-kit:rule-creator`.

→ Proceed to Step 13

#### Output

- Rule linkage verified; related files flagged for update if needed

---

### Step 13: Update tests

#### Process

1. Identify test files corresponding to any changed source files (mirror path: `src/foo/bar.py` → `tests/foo/test_bar.py`).
2. Update or create test cases for the changed behavior.
3. Tests mock only external I/O boundaries — no unit tests for individual methods.
4. Run `pytest` and confirm tests pass.

→ Done (existing project flow complete)

#### Output

- Affected test files updated and passing

---

## References

See `{plugin_root}/references/python/_index.md` for the full list. Sections by mode:

**New project (Steps 3–8):** `python-core.md`, `python-architecture.md`, `python-testing.md`; add `python-fastapi.md` or `python-llm.md` as needed

**Existing project (Steps 9–13):** `python-core.md`, `python-architecture.md`; add others based on the task
