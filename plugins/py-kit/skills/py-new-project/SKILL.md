---
name: py-kit:py-new-project
description: >
  Create a new Python project from scratch with a full DDD-layered scaffold, dependency injection,
  rule files, and test skeleton. Trigger when the user asks to build a new Python project, package,
  or application from the ground up.
  Examples: "新しい Python プロジェクト作って", "create a Python project", "土台から作りたい".
  Do NOT trigger for simple scripts — use py-kit:py-script instead.
---

# py-kit:py-new-project — New Python Project

Creates a full DDD-layered Python project with scaffold, DI design, rules, and test skeleton.

---

## Tasks

### Step 1: Load standards

Read the shared Python standards:

```
{plugin_root}/references/python-standards.md
```

Read the entire document. Key sections for this skill: **Project Folder Structure**, **DDD**, **SOLID**, **Extensibility-Focused Design**, **Dependency Inversion**, **Pydantic Boundaries**, **Logger Specification**, **Test Policy**, **Bat Launcher Template**.

→ Proceed to Step 2

---

### Step 2: Requirements gathering

#### Process

1. Confirm the project name and package name (`snake_case`).
2. Identify the domain: what real-world problem does this project solve?
3. List the key use cases (3–5 verbs: "user places order", "admin generates report", etc.).
4. Identify external dependencies: databases, APIs, file systems, message queues.
5. Confirm the interface type: CLI / FastAPI / tkinter GUI / background worker.
6. Confirm environment variable requirements.

→ Proceed to Step 3

#### Output

- Domain, use cases, external dependencies, interface type confirmed

---

### Step 3: DDD layer design

#### Process

1. Map use cases to **Application Services** (one class per use case group).
2. Identify **Entities** (have identity, mutable) and **Value Objects** (immutable, equality by value).
3. Define **Aggregate roots** and their invariants.
4. Define **Repository Protocols** in `domain/repositories/` — one per aggregate root.
5. Identify **Domain Services** for logic that spans multiple entities.
6. Plan **Infrastructure** implementations: which repository protocols get which concrete class.
7. Present the layer diagram to the user for confirmation before generating code.

→ Proceed to Step 4

#### Output

- Layer diagram confirmed: entities, value objects, repositories, services, infrastructure

---

### Step 4: Generate project scaffold

#### Process

1. Create the full directory structure from the standards (Project Folder Structure section).
2. Create `pyproject.toml` with Python `>= 3.11` and dependencies pinned with `~=`.
3. Create `.gitignore` (include: `.env`, `__pycache__/`, `*.pyc`, `venv/`, `.venv/`, `log/`, `cache/`).
4. Create `.env.sample` with all required environment variable keys and placeholder values.
5. Create `setup/setup_venv.bat` (ASCII only — creates venv and installs dependencies).
6. Create `activate.bat`.
7. Add `.gitkeep` to empty folders (`log/`, `input/`, `output/`, `cache/` if used).
8. Create stub files for all planned modules (empty with correct imports and type stubs).
9. Create `logger.py` per the Logger Specification.
10. Create `constants.py` with `PROJECT_ROOT` and `LOG_DIR`.

→ Proceed to Step 5

#### Notes

##### Prohibitions

- Do not put `.bat` files in a `bat/` subfolder — all bat files go in the project root
- Do not put `README.md` in empty folders — use `.gitkeep` only
- Do not instantiate concrete classes inside class bodies — always inject via constructor

---

### Step 5: Dependency injection wiring

#### Process

1. Create `Protocol` definitions for all repository and service interfaces.
2. Create a composition root (typically `main.py` or a dedicated `container.py`) where all concrete implementations are instantiated and injected.
3. Ensure no high-level class imports a concrete implementation directly.
4. Apply Strategy / Factory / Decorator patterns where appropriate per the standards.

→ Proceed to Step 6

#### Output

- All dependencies flow from the composition root; no concrete imports in domain or application layers

---

### Step 6: Deploy rules

#### Process

1. Create `.claude/rules/class-structure.md` in the project root using the template from `{plugin_root}/rules/class-structure.md`.
2. Create `.claude/rules/config-source-link.md` using the template from `{plugin_root}/rules/config-source-link.md`.
3. Create `.claude/rules/source-test-link.md` using the template from `{plugin_root}/rules/source-test-link.md`.
4. Create `.claude/rules-jp/` versions (Japanese mirrors) for each rule.
5. Commit: `git add .claude/rules/ .claude/rules-jp/ && git commit -m "chore: add py-kit rules"`.

→ Proceed to Step 7

#### Output

- Three rule files deployed to `.claude/rules/` and `.claude/rules-jp/`

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
- DDD (Domain-Driven Design)
- SOLID Principles
- Extensibility-Focused Design
- Dependency Inversion / DI
- Pydantic Boundaries
- Logger Specification
- Test Policy
- Bat Launcher Template
- FastAPI run.bat Template
- Naming Conventions
- Language Rules
