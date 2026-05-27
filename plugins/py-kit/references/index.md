# py-kit references index

One-line description of each reference file. Bodies live in the same directory.
Auto-injection rules (the star chart that maps edit-target file paths to references) live in `injection_rules.yaml`.

The `inject_references.py` hook reads this file (English) to look up `description` strings when rendering the injection prompt.

---

## core — language rules

| Path | Description |
|---|---|
| `core/naming.md` | Naming conventions. Functions snake_case, type aliases UpperCamel, files/modules snake_case. Standard file names inside a feature folder (types/service/query/route/client/db). |
| `core/comments.md` | Comment rules. 1-line docstring required on exported functions/types; description required on design-significant Pydantic/dataclass fields; PR-numbered change history; TODO must carry an issue number. |
| `core/type-hints.md` | Type hints body. PEP 695 generics, Self, @typing.override, Annotated, TYPE_CHECKING, type statement, NewType, assert_never, Literal+match. |
| `core/decorators.md` | Recommended decorators (@dataclass / @final / @cache / @cached_property / @override / @contextmanager) and handler decorators for cross-cutting concerns (@catch_and_log / @catch_and_map / @with_retry / @with_timeout); limited use of @overload. |
| `core/language-rules.md` | Language rules. Comments in Japanese; print/logger/bat in English; f-string for formatting; import order; exception hierarchy (AppError base class). |
| `core/style.md` | Style settings. Recommended config for ruff/mypy/pyright; line length 100; double quotes; section markers. |

## architecture

| Path | Description |
|---|---|
| `architecture/layout.md` | Top-level layout. Only `shared/` and `main.py` are required; `features` / `integrations` / `runtime` / `server` are optional. Standard structure inside a feature folder (types.py / service.py / query.py / route.py / client.py). |
| `architecture/ts-style.md` | The central document for TypeScript-style Python. Type-alias for function types + Callable for DI; Protocol for structural typing; usage table for @dataclass / Pydantic / TypedDict. |
| `architecture/composition-root.md` | Responsibilities of main.py. Wire functions in `build_handlers(settings)` with `functools.partial`; hold them in a `Handlers` dataclass for type-safe access. Library-standard classes (FastAPI, CLI, etc.) are used as-is. |
| `architecture/dependencies.md` | Dependency direction rule. One-way: features/server → integrations → shared. Same-layer cross-reference is forbidden. Dependency inversion (DIP) is done via function-type aliases. |
| `architecture/design-principles.md` | Design-principle priorities. DRY > SOLID > extensibility awareness. Function-first; class use is restricted to DTOs and library requirements. |
| `architecture/refactoring-judgement.md` | Refactoring judgement. How many times before extracting; when to abstract; when to externalize config; when to split a file. |

## shared — cross-cutting infrastructure

| Path | Description |
|---|---|
| `shared/logger.md` | Standard JSON Lines logger. `get_logger(__name__)`, structured logging, log-level policy. |
| `shared/settings.md` | Standard pattern for `pydantic_settings.BaseSettings`. `.env` / `.env.sample` workflow; `SecretStr`; nested settings. |
| `shared/secrets-and-env.md` | Separation of secrets / environment / structure / assets / runtime state. How to choose between `.env` / `settings.yaml` / code / `index.yaml` / `data/`. |
| `shared/errors.md` | Exception hierarchy. `AppError` base class; domain sub-classes; mapping to HTTP errors. |
| `shared/types.md` | Common type aliases. Choosing between `NewType` and `type` statement; standard for identifier types (e.g. `UserId`). |
| `shared/constants.md` | Role boundary of `constants.py`. Storage for pre-computed paths such as `PROJECT_ROOT`, `LOG_DIR`. Runtime-variable values go to `settings`. |

## scripts

| Path | Description |
|---|---|
| `scripts/python-script.md` | Structure of a single-file Python script. Docstring, argparse, `main() -> int`, section markers. |
| `scripts/launchers-windows.md` | Windows bat launcher. `chcp 65001`, `setlocal`, PowerShell timestamps, `log/` directory output. **Never write Japanese inside a bat file** (absolute). |
| `scripts/launchers-unix.md` | UNIX shell script. `set -euo pipefail`, `tee` for logging, `.venv` activation. |
| `scripts/tkinter.md` | tkinter GUI conventions. Standard style, settings dialog, blue accent color. |

## testing

| Path | Description |
|---|---|
| `testing/strategy.md` | Test policy. No unit tests; only integration tests + smoke tests. Smoke tests hit real external services and are user-triggered only (AI must not auto-run them). |
| `testing/pytest.md` | pytest conventions. `conftest.py`, fixtures, parametrize, pytest-asyncio, `tests/` layout. |
| `testing/mocks.md` | Mock patterns for integration tests. LLM mocks, HTTP mocks, time mocks, swapping implementations via function-type aliases. |

## concurrency

| Path | Description |
|---|---|
| `concurrency/async.md` | asyncio conventions. `TaskGroup`, `asyncio.timeout`, sync/async boundaries, async generators / context managers. |
| `concurrency/parallelism.md` | Parallel processing. Choosing between multiprocessing / threading / subinterpreters; the GIL; CPU bound vs IO bound. |

## packaging

| Path | Description |
|---|---|
| `packaging/pyproject.md` | Complete `pyproject.toml` sample. `[project]` / `[tool.ruff]` / `[tool.mypy]` / `[tool.pyright]` / `[tool.pytest]`. |
| `packaging/dependencies.md` | Dependency management. uv is the standard; `optional-dependencies.dev` required; unified `.venv`; lockfile workflow. |
| `packaging/distribution.md` | Distribution. wheel/sdist, PyPI publish, exposing the CLI via `entry_points`. |
| `packaging/python-versions.md` | Python version policy. Use the newest version possible; feature-table for 3.12+. |

## performance

| Path | Description |
|---|---|
| `performance/cheatsheet.md` | Performance cheatsheet. Choosing between profilers (cProfile / snakeviz / line_profiler / py-spy / scalene / memray); hot-path checklist. |

## llm

| Path | Description |
|---|---|
| `llm/providers.md` | LLM provider implementation. Abstract Claude / OpenAI / Gemini as functions; wrap vendor exceptions into domain exceptions; log token usage. |
| `llm/instructor.md` | Structured outputs with Instructor + Pydantic. How to build task-specific client functions. |
| `llm/prompts-authoring.md` | Authoring and assembling prompt files. `prompts/` at project root; H3-section-sized parts; static (.md) vs dynamic (.j2); SoT management via `index.yaml`; assembly via `includes`. |
| `llm/prompts-loader.md` | Prompt loader implementation. Place `index_loader` / `builder` / `types` under `src/{pkg}/integrations/llm/prompts/`; Jinja2 + `StrictUndefined`; `build_prompt` / `build_bundle`. |
| `llm/cost-cache.md` | Cost management. Design premise of prompt caching (stack from top; static at top, dynamic at bottom); Anthropic `cache_control`; OpenAI automatic cache; `max_tokens`; Batch API; streaming. |
| `llm/exceptions-retry.md` | LLM exception hierarchy. rate-limit / server / bad-request / auth / timeout / content-filter; retry strategies; honoring `Retry-After`. |

## fastapi

| Path | Description |
|---|---|
| `fastapi/app.md` | FastAPI app composition. `build_app` pattern, lifespan, middleware, CORS. |
| `fastapi/routes.md` | Router implementation. `Annotated[Type, Depends/Path/Query]`; route functions stay thin; business logic in `service.py`. |
| `fastapi/schemas.md` | I/O Pydantic schemas. Field constraints; `to_domain` / `from_domain` methods to keep feature-internal DTOs separate. |
| `fastapi/auth-and-errors.md` | Authentication with `Depends` + handling `SecretStr` + error handling via `exception_handler`. |
| `fastapi/health.md` | Health check. Simple `/healthz` that just returns 200. |
