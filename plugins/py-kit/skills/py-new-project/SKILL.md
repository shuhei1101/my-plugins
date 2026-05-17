---
name: py-kit:py-new-project
description: >
  Create a new Python project from scratch with a layered scaffold, dependency injection,
  rule files, and test skeleton. Trigger when the user asks to build a new Python project, package,
  or application from the ground up.
  Examples: "新しい Python プロジェクト作って", "create a Python project", "土台から作りたい".
  Do NOT trigger for simple scripts — use py-kit:py-script instead.
---

# py-kit:py-new-project — New Python Project

Creates a layered Python project with scaffold, DI design, rules, and test skeleton.

---

## Tasks

### Step 1: Load standards

Read the shared Python standards:

```
{plugin_root}/references/python-standards.md
```

The plugin root is two levels above this skill file (e.g. `Base directory: .../skills/py-new-project` → plugin root is `.../{plugin-name}/`).

Read the entire document. Key sections for this skill: **Project Folder Structure**, **Layered Architecture**, **No Hardcoding**, **SOLID**, **Extensibility-Focused Design**, **Dependency Inversion**, **Pydantic Boundaries**, **Logger Specification**, **Test Policy**, **Bat Launcher Template**.

→ Proceed to Step 2

---

### Step 2: Requirements gathering

#### Process

1. Confirm the project name and package name (`snake_case`).
2. Describe the project: what problem does it solve? Who calls it?
3. List the key use cases (3–5 verbs: "process order", "generate report", etc.).
4. Identify external dependencies: databases, APIs, file systems, message queues.
5. Confirm the interface type: CLI / FastAPI / tkinter GUI / background worker.
6. Confirm environment variable requirements.

→ Proceed to Step 3

#### Output

- Use cases, external dependencies, interface type confirmed

---

### Step 3: Layer design

#### Process

1. Decide how to split code into layers (folder names are free — use what fits the project).
2. Identify which code touches external services and isolate it in a boundary layer.
3. Define `Protocol` interfaces in the business logic layer for each external boundary.
4. Plan concrete implementations in the boundary layer (DB client, HTTP adapter, file adapter, etc.).
5. Confirm composition root placement: where will all concrete classes be wired together?
6. Present the layer plan to the user for confirmation before generating code.

→ Proceed to Step 4

#### Output

- Layer plan confirmed: business logic, external boundaries, and their Protocol interfaces

---

### Step 4: Generate project scaffold

#### Process

1. Create the directory structure based on the layer plan (see standards: Project Folder Structure for reference).
2. Create `pyproject.toml` with Python `>= 3.11` and dependencies pinned with `~=`.
3. Create `.gitignore` (include: `.env`, `__pycache__/`, `*.pyc`, `venv/`, `.venv/`, `log/`, `cache/`).
4. Create `.env.sample` with all required environment variable keys and placeholder values.
5. On Windows: create `setup/setup_venv.bat` (ASCII only) and `activate.bat`. Skip on Linux/macOS.
6. Add `.gitkeep` to empty folders (`log/`, `input/`, `output/`, `cache/` if used).
7. Create stub files for all planned modules (empty with correct imports and type stubs).
8. Create `logger.py` per the Logger Specification.
9. Create `constants.py` with `PROJECT_ROOT` and `LOG_DIR` only — no magic numbers or strings.

→ Proceed to Step 5

#### Notes

##### Prohibitions

- Do not put `.bat` files in a `bat/` subfolder — all bat files go in the project root (Windows only)
- Do not put `README.md` in empty folders — use `.gitkeep` only
- Do not instantiate concrete classes inside class bodies — always inject via constructor
- Do not hardcode any config values, URLs, ports, paths, or credentials in source code

---

### Step 5: Dependency injection wiring

#### Process

1. Create `Protocol` definitions for all external boundary interfaces.
2. Create a composition root (typically `main.py` or a dedicated `container.py`) where all concrete implementations are instantiated and injected.
3. Verify: no high-level business logic class imports a concrete external-library class directly.
4. Apply Strategy / Factory / Decorator patterns where appropriate per the standards.

→ Proceed to Step 6

#### Output

- All dependencies flow from the composition root; business logic layers import only Protocols

---

### Step 6: Create linkage rules

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
git add .claude/rules/ .claude/rules-jp/ && git commit -m "chore: add py-kit rules"
```

→ Proceed to Step 7

#### Output

- Three rules created in `.claude/rules/` and `.claude/rules-jp/` via `/claude-kit:rule-creator`

---

### Step 7: Create test skeleton

#### Process

1. Create `tests/conftest.py` with shared pytest fixtures.
2. Create `tests/mocks/mock_env.py` (environment variable mocking helper).
3. Create `tests/mocks/mock_externals.py` (stubs for external API / DB clients).
4. For each planned use case, create a corresponding `tests/{feature}/test_{feature}.py` stub.
5. Tests mock only external I/O boundaries — no unit tests for individual methods.

→ Done

#### Output

- Test skeleton created mirroring the source structure

---

## References

See `{plugin_root}/references/python-standards.md`:
- Project Folder Structure
- Layered Architecture
- No Hardcoding
- SOLID Principles
- Extensibility-Focused Design
- Dependency Inversion / DI
- Pydantic Boundaries
- Logger Specification
- Test Policy
- Bat Launcher Template (Windows only)
- Naming Conventions
- Language Rules
