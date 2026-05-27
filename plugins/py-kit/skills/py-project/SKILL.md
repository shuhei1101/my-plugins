---
name: py-kit:py-project
description: >
  Work with a Python project — create a new project from scratch, or review/extend/refactor/fix
  an existing one. Covers both new project scaffolding (feature-folder layout, function-first
  design, index.yaml, test skeleton) and existing project work (review, feature addition,
  refactor, bug fix).
  Examples: "新しい Python プロジェクト作って", "土台から作りたい", "このコード見て",
  "機能追加して", "リファクタして", "バグ直して", "コードレビューして".
  Do NOT trigger for simple one-off scripts — use py-kit:py-script instead.
---

# py-kit:py-project — Python Project (New or Existing)

Handles Python projects under py-kit's new policy
(feature-folder layout + TypeScript-style + function-first).

---

## Tasks

### Step 1: Load standards

First, read the references index:

```
{plugin_root}/references/index.yaml
```

The plugin root is two levels above this skill file (e.g. `Base directory: .../skills/py-project` → plugin root is `.../py-kit/`).

The `references:` section of `index.yaml` lists each file with a short summary, and the
`injection_rules:` section defines "which references to assign to which file paths".

Always read the following for this skill:
- `{plugin_root}/references/core/naming.md`
- `{plugin_root}/references/core/comments.md`
- `{plugin_root}/references/core/type-hints.md`
- `{plugin_root}/references/core/language-rules.md`
- `{plugin_root}/references/core/style.md`
- `{plugin_root}/references/architecture/layout.md`
- `{plugin_root}/references/architecture/ts-style.md`
- `{plugin_root}/references/architecture/composition-root.md`
- `{plugin_root}/references/architecture/dependencies.md`

Add the following depending on the task:
- New project → `testing/strategy.md`, `packaging/pyproject.md`, `packaging/dependencies.md`
- Using FastAPI → `fastapi/app.md`, `fastapi/routes.md`, `fastapi/schemas.md`
- Using an LLM → `llm/providers.md`, `llm/exceptions-retry.md` (and `llm/instructor.md`, `llm/prompts.md` if needed)

→ Proceed to Step 2

---

### Step 2: Determine mode (new vs existing)

#### Process

Identify whether the user wants to create a new project or work on an existing one:

| Signal | Mode |
|---|---|
| "新規" / "create a new project" / "土台から作りたい" / no project files yet | **New** → Step 3 |
| "このコード見て" / "機能追加" / "リファクタ" / "レビュー" / project already exists | **Existing** → Step 8 |

If ambiguous, confirm with the user.

---

## New Project Path (Steps 3–7)

### Step 3: Requirements gathering

1. Confirm the project name and package name (`snake_case`).
2. Confirm the project's purpose and who calls it.
3. List 3–5 primary use cases (features), verb-based.
4. Identify external dependencies (LLM / TTS / OBS / HTTP API, etc.).
   - Note: DBs are basically out of scope. If persistence is required, discuss separately.
5. Confirm the interface type (CLI / FastAPI / GUI / background worker).
6. Confirm environment-variable requirements.

→ Proceed to Step 4

---

### Step 4: Feature-folder design

Following the conventions in `architecture/layout.md`:

1. **Required folders**: `shared/` + `main.py`
2. **Optional folders**: create only what is needed
   - `features/` — business features (one per use case)
   - `integrations/` — external services (LLM, TTS, etc.)
   - `runtime/` — runtime infrastructure (queues, etc. — AITuber-scale)
   - `server/` — only if using FastAPI
3. **Each feature's internal structure**: `types.py` + `service.py` as the minimum, adding `query.py` / `route.py` / `client.py` / `prompts/` as needed
4. **Present the design to the user** and get confirmation.

→ Proceed to Step 5

---

### Step 5: Generate the project skeleton

1. Create the directory structure (`src/{pkg}/...`, `tests/`, `log/`, use `.gitkeep` to preserve empty folders).
2. Create `pyproject.toml` (see the full sample in `packaging/pyproject.md`, `requires-python = ">=3.12"`).
3. Create `.gitignore` (include `.env`, `__pycache__/`, `.venv/`, `log/`, `dist/`).
4. Create `.env.sample` (required env keys with placeholder values).
5. Create `.python-version` (pinned to `3.12`).
6. `src/{pkg}/shared/`:
   - `logger.py` (template from `shared/logger.md`)
   - `settings.py` (template from `shared/settings.md`)
   - `errors.py` (exception hierarchy from `shared/errors.md`)
   - `types.py` (shared type aliases)
   - `constants.py` (precomputed paths)
7. Stubs for each feature:
   - `types.py` (DTOs + type aliases)
   - `service.py` (functions + simple logic)
   - `query.py` / `route.py` if needed
8. `src/{pkg}/main.py` (`build_handlers(settings) -> Handlers` pattern)
9. If a Windows launcher is needed, `setup/setup_venv.bat` + `run.bat` (`scripts/launchers-windows.md`)

→ Proceed to Step 6

---

### Step 6: Wire functions

1. Abstract every external dependency as a **function type alias** (`architecture/ts-style.md`).
2. Wire dependencies in `main.py`'s `build_handlers(settings)` using `functools.partial`.
3. Return a `Handlers` dataclass to hold them type-safely.
4. Do **not** create a "class-based DI container" or "Repository class".
5. For FastAPI, wire `app.state.handlers = build_handlers(settings)` in `server/app.py`'s lifespan.

→ Proceed to Step 7

---

### Step 7: Create the test skeleton

Follow the policy in `testing/strategy.md`:

1. `tests/conftest.py` (shared fixtures: test_settings, freeze_time, etc.)
2. `tests/{feature}/test_{usecase}.py` stubs
3. **Do not create unit tests**. Write integration tests only.
4. Inject external dependencies (LLM, etc.) via mock functions (`testing/mocks.md`).
5. Isolate smoke tests under `tests/smoke/` and guard them with a `--run-smoke` flag (AI auto-execution prohibited).

→ Done (new-project flow complete)

---

## Existing Project Path (Steps 8–12)

### Step 8: Understand the project structure

1. Read the top-level directory listing.
2. Identify the layout (feature-folder / pure DDD / other).
3. Read `pyproject.toml` (dependencies and Python version).
4. Identify the main entry point (`main.py` / `__main__.py` / `server/app.py`) and existing tests.
5. Check `.env.sample` / `.python-version`.

→ Proceed to Step 9

---

### Step 9: Quality check

Review from the new-policy perspective:

1. **Naming**: matches `core/naming.md` (snake_case functions, UpperCamel types)?
2. **Comments**: required items from `core/comments.md` (docstrings on exported functions, descriptions on design-critical fields)?
3. **Type hints**: written in PEP 695, no overuse of `Any`?
4. **Function-first**: are classes overused (any classes outside DTOs / library requirements)?
5. **Dependency direction**: is `shared` ← `integrations` ← `features/server` respected?
6. **DI**: are external dependencies injected as function type aliases?
7. **Exceptions**: is the `AppError` hierarchy used, and are vendor exceptions wrapped?
8. **Tests**: integration-focused, with smoke tests separated?
9. For a review-only request, report findings here and stop.

→ Proceed to Step 10 if implementation is required

---

### Step 10: Implement changes

1. Carry out the task (feature addition / refactor / bug fix).
2. Check `index.yaml`'s `injection_rules` for the edited file paths and read the matching references.
3. Implement according to the standards:
   - Behavior in functions (classes only for DTOs / library requirements)
   - Inject external dependencies as function type aliases
   - Type hints everywhere
   - `print` / English messages / Japanese comments
4. Do not add abstractions beyond the task's requirements (YAGNI).

→ Proceed to Step 11

---

### Step 11: Sync check

Identify what must be updated alongside the changed files:

| Changed location | Must be updated together |
|---|---|
| DTO in `features/{feature}/types.py` | corresponding `schemas.py` (when using FastAPI) |
| New exception in `shared/errors.py` | mapping in `server/error_handlers.py` |
| Dependency in `pyproject.toml` | `uv.lock` (update via `uv sync`) |
| Feature added | wire it in `main.py`'s `build_handlers` + add to `Handlers` dataclass |
| FastAPI route added | `include_router` in `server/app.py` |

→ Proceed to Step 12

---

### Step 12: Update tests

1. Update the integration tests (`tests/{feature}/test_{usecase}.py`) that correspond to the changed source.
2. Inject external dependencies via mock functions (`testing/mocks.md`).
3. Confirm tests pass with `uv run pytest tests/ --ignore=tests/smoke/`.
4. **Do not run** smoke tests (user manual execution only).

→ Done (existing-project flow complete)

---

## References

See `{plugin_root}/references/index.yaml` for full details.

Typical references covered by this skill:
- `core/*` — language rules
- `architecture/*` — layout and function wiring
- `shared/*` — cross-cutting infrastructure
- `testing/*` — integration-test policy
- `packaging/*` — pyproject.toml and uv
- `fastapi/*` — when using FastAPI
- `llm/*` — when using an LLM
