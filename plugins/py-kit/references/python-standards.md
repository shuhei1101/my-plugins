# Python Standards — py-kit Shared Reference

All py-kit skills draw from this document. Do not duplicate content in skill files — reference this instead.

---

## Naming Conventions

| Target | Convention | Example |
|---|---|---|
| Module / file | `snake_case` | `user_repository.py` |
| Class | `PascalCase` | `UserRepository` |
| Function / method | `snake_case` | `find_by_id()` |
| Variable | `snake_case` | `user_id` |
| Constant | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| Private | leading `_` | `_internal_cache` |
| Protocol / Interface | `{Name}able` (preferred), `I{Name}`, or `Base{Name}` — pick one per project | `Convertable`, `IConverter`, `BaseConverter` |
| Implementation | `{impl}_{name}.py` | `ffmpeg_converter.py` |

---

## Comment Rules

Write **why**, never what. Code already says what.

- Good: `# CP932 parses bat files — Japanese UTF-8 bytes become lead bytes and swallow following chars`
- Bad: `# Calls setup_logger`

One short line max. No multi-paragraph blocks, no docstrings that restate the signature.

Exception: module-level docstrings for scripts (see Simple Script section).

---

## Type Hints

Apply everywhere — function arguments, return types, class fields. No bare `Any`.

```python
from typing import Literal, Optional, Protocol, TypeVar
from collections.abc import Sequence

def process(items: Sequence[str], mode: Literal["fast", "slow"]) -> list[str]: ...
```

Use `Protocol` for structural interfaces (preferred over `ABC` for new code):

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Convertable(Protocol):
    def convert(self, source: str) -> str: ...
```

Use `ABC` only when shared default implementations are needed.

---

## SOLID Principles

### S — Single Responsibility

Each class has exactly one reason to change. Split by axis of change, not by size.

```python
# Bad: UserService handles auth + email + DB
# Good: AuthService, EmailService, UserRepository — each changes for one reason
```

### O — Open / Closed

Open for extension, closed for modification. Add behavior by adding code, not by editing existing classes.

```python
# Bad: if/elif chains that grow with each new type
# Good: Strategy pattern — new behavior = new class implementing the Protocol
class ExportStrategy(Protocol):
    def export(self, data: list[dict]) -> bytes: ...

class CsvExporter:
    def export(self, data: list[dict]) -> bytes: ...

class JsonExporter:
    def export(self, data: list[dict]) -> bytes: ...
```

### L — Liskov Substitution

A subclass must be substitutable for its base without breaking callers. Never weaken postconditions or strengthen preconditions in subclasses.

```python
# Bad: SquareRepository.find_all() raises NotImplementedError
# Good: every subclass fully implements the Protocol contract
```

### I — Interface Segregation

Many small focused protocols over one large general interface. Clients depend only on what they use.

```python
# Bad: class IStorage(Protocol): def read() / write() / delete() / list() / stat()
# Good: class Readable(Protocol): def read() / class Writable(Protocol): def write()
#       combine with: class ReadWritable(Readable, Writable, Protocol): ...
```

### D — Dependency Inversion

High-level modules depend on abstractions, not on concrete implementations. Inject dependencies via constructor.

```python
# Bad: class ReportService: def __init__(self): self.db = PostgresDatabase()
# Good:
class ReportService:
    def __init__(self, repo: UserRepository) -> None:  # UserRepository is a Protocol
        self._repo = repo
```

---

## DRY Principle

Extract duplication only when it has a **stable, named concept** behind it. Three similar lines is better than a premature abstraction.

- Duplicate values → constant
- Duplicate logic with the same concept → function
- Duplicate class structure across features → base class or generic
- Duplicate configuration → config file / environment variable

Never DRY across entirely different domains just because the code looks similar.

---

## Domain-Driven Design

Apply to projects with non-trivial business logic. Use the four-layer architecture:

```
interface/       ← CLI, FastAPI, GUI, bat launchers
application/     ← Use cases, orchestration (no domain logic here)
domain/          ← Entities, value objects, aggregates, domain services, repositories (Protocols)
infrastructure/  ← Concrete repository implementations, external API adapters, DB clients
```

### Building Blocks

**Entity** — has identity (ID), mutable state, equality by ID.

```python
@dataclass
class User:
    id: UserId
    name: str
    email: Email  # value object
```

**Value Object** — no identity, immutable, equality by value. Use `@dataclass(frozen=True)`.

```python
@dataclass(frozen=True)
class Email:
    value: str
    def __post_init__(self) -> None:
        if "@" not in self.value:
            raise ValueError(f"Invalid email: {self.value}")
```

**Aggregate** — cluster of entities with invariants. Access only through the aggregate root. The root enforces all invariants.

**Repository** — defined as a `Protocol` in `domain/`, implemented in `infrastructure/`.

```python
# domain/repositories/user_repository.py
class UserRepository(Protocol):
    def find_by_id(self, user_id: UserId) -> Optional[User]: ...
    def save(self, user: User) -> None: ...
```

**Domain Service** — stateless logic that doesn't belong to a single entity.

**Application Service** — orchestrates domain objects to fulfill a use case. No domain logic here — only coordination.

---

## Extensibility-Focused Design

Design for future change by default. Avoid locking in implementations.

### Dependency Injection

Always inject dependencies via constructor. Never instantiate concrete classes inside a class body.

```python
# Bad
class OrderService:
    def __init__(self) -> None:
        self._repo = SqlOrderRepository()  # hard-coded concrete

# Good
class OrderService:
    def __init__(self, repo: OrderRepository) -> None:  # Protocol
        self._repo = repo
```

### Strategy Pattern

Encapsulate interchangeable algorithms behind a Protocol.

```python
class SortStrategy(Protocol):
    def sort(self, items: list[int]) -> list[int]: ...

class QuickSort:
    def sort(self, items: list[int]) -> list[int]: ...

class MergeSort:
    def sort(self, items: list[int]) -> list[int]: ...
```

### Factory Pattern

Centralize object creation logic. Use factory functions or classes when construction is complex or conditional.

```python
def create_exporter(fmt: Literal["csv", "json"]) -> ExportStrategy:
    match fmt:
        case "csv": return CsvExporter()
        case "json": return JsonExporter()
```

### Decorator Pattern

Add cross-cutting behavior (logging, caching, retry) without modifying the original class.

```python
class LoggingRepository:
    def __init__(self, inner: UserRepository, logger: Logger) -> None:
        self._inner = inner
        self._logger = logger

    def find_by_id(self, user_id: UserId) -> Optional[User]:
        self._logger.debug("find_by_id %s", user_id)
        return self._inner.find_by_id(user_id)
```

---

## Pydantic Boundaries

Use Pydantic models (not just type hints) at system boundaries where runtime validation matters.

**Use Pydantic for:**
- External API request bodies and responses
- LLM inputs and outputs (via Instructor)
- Config file reads (YAML / JSON)
- Data passed between files (CSV / JSONL records)
- User input parsing
- Inter-thread / inter-process event data

**`typing` alone is sufficient for:**
- Function argument / return type hints on internal logic
- `dict` / `list` expressions that stay within a single function

---

## Logger Specification

Every project must include `{package_name}/logger.py` with a `setup_logger()` function:

- `constants.py` defines `LOG_DIR = PROJECT_ROOT / "log"`
- `setup_logger()` calls `LOG_DIR.mkdir(parents=True, exist_ok=True)`
- Log filename: `LOG_DIR / f"{datetime.now():%Y%m%d_%H%M%S}_{package_name}.log"` — new file every run
- Attach both `StreamHandler(sys.stdout)` and `FileHandler(..., encoding="utf-8")`
- Format: `[%(asctime)s] %(levelname)s %(name)s %(filename)s:%(lineno)d - %(message)s`
- Guard against duplicate handlers: `if logger.handlers: return logger`
- Submodules: `get_logger(__name__)`

Call `setup_logger()` immediately after entry in `main.py` / `__main__.py`.

---

## Test Policy

| Test type | Policy |
|---|---|
| Unit tests (individual methods/functions) | Not written — maintenance cost exceeds value in AI-assisted development |
| Module integration tests | Write when modules interact in non-obvious ways |
| Use case tests | Write per use case; mock only external I/O boundaries |
| E2E tests | Write for CLI entry points and HTTP API endpoints |

Use pytest. Mirror the source folder structure in `tests/`. Reusable mocks go in `tests/mocks/`.

Source and test files are linked — when a source file changes, always check and update corresponding tests.

---

## Project Folder Structure

```
{package-name}/
├── {package_name}/
│   ├── interface/           # CLI, GUI, HTTP handlers
│   ├── application/         # Use cases
│   ├── domain/
│   │   ├── entities/
│   │   ├── value_objects/
│   │   ├── repositories/    # Protocol definitions
│   │   └── services/        # Domain services
│   ├── infrastructure/      # Concrete implementations
│   ├── __init__.py
│   ├── __main__.py
│   ├── config.py
│   ├── main.py
│   ├── logger.py
│   ├── exceptions.py
│   └── constants.py
├── tests/
│   ├── mocks/
│   │   ├── mock_env.py
│   │   └── mock_externals.py
│   ├── conftest.py
│   └── {feature}/
│       └── test_{feature}.py
├── setup/
│   └── setup_venv.bat
├── {mode}.bat
├── activate.bat
├── .env.sample
├── .gitignore
├── README.md
└── pyproject.toml
```

---

## Simple Script Structure

For single-file scripts that do not need a full project scaffold:

**File header (required):**

```python
"""
{script_name} — {one-line description}

Usage:
  python {script_name}.py [options] {positional_args}
"""
```

**Code structure:**

```python
"""...(header)..."""

# ── stdlib ──────────────────────────────────────────────────
import argparse
from pathlib import Path
from typing import Optional

# ── third-party ─────────────────────────────────────────────
import some_lib  # pip install some_lib

# ── constants ───────────────────────────────────────────────
SOME_CONSTANT: str = "value"

# ── private helpers ─────────────────────────────────────────
def _helper(value: str) -> str:
    return value.strip()

# ── main ────────────────────────────────────────────────────
def main(args: argparse.Namespace) -> None:
    ...

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    return parser.parse_args()

if __name__ == "__main__":
    main(parse_args())
```

No `logger.py`, `config.py`, tests, bat files, setup scripts, or `pyproject.toml`. Document required packages with `# pip install {package}` inline.

---

## Bat Launcher Template

```bat
@echo off
chcp 65001 > nul
setlocal

set "LOG_DIR=%~dp0log"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMddHHmmss"') do set "TS=%%I"
set "BAT_LOG=%LOG_DIR%\%TS%_run_bat.log"

echo [%date% %time%] Starting >> "%BAT_LOG%"
echo [%date% %time%] CWD: %cd% >> "%BAT_LOG%"

if exist "%~dp0venv\Scripts\activate.bat" (
    call "%~dp0venv\Scripts\activate.bat" >> "%BAT_LOG%" 2>&1
)

python -m {package_name} %* >> "%BAT_LOG%" 2>&1
set "EXITCODE=%ERRORLEVEL%"

if %EXITCODE% neq 0 (
    echo [ERROR] Exit code %EXITCODE%. See: %BAT_LOG%
    pause
)

endlocal & exit /b %EXITCODE%
```

**Rules:**
- Timestamped log filenames are mandatory — never use a fixed name
- All bat file content must be ASCII only — Japanese causes CP932 parse errors in cmd.exe
- Use PowerShell `Get-Date` for timestamps — `wmic` is removed in Windows 11 24H2+

For simultaneous console + log output (long-running commands):

```bat
long_command.exe 2>&1 | powershell -NoProfile -Command "[Console]::InputEncoding=[System.Text.Encoding]::UTF8; $input | ForEach-Object { Write-Host $_; Add-Content -LiteralPath '%BAT_LOG%' -Value $_ -Encoding utf8 }"
```

---

## FastAPI run.bat Template

```bat
@echo off
chcp 65001 > nul
setlocal

set "LOG_DIR=%~dp0log"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMddHHmmss"') do set "TS=%%I"
set "BAT_LOG=%LOG_DIR%\%TS%_run.log"

if not "%1"=="" set "PORT=%1"

echo [%date% %time%] Starting. PORT=%PORT% >> "%BAT_LOG%"

if exist "%~dp0.venv\Scripts\activate.bat" (
    call "%~dp0.venv\Scripts\activate.bat" >> "%BAT_LOG%" 2>&1
)

python -m {package_name} >> "%BAT_LOG%" 2>&1
set "EXITCODE=%ERRORLEVEL%"

if %EXITCODE% neq 0 (
    echo [ERROR] Exit code %EXITCODE%. See: %BAT_LOG%
    pause
)

endlocal & exit /b %EXITCODE%
```

Port conventions: reserve a fixed port for the main repo; use fixed-port + 1 or higher for worktree test servers.

---

## GUI (tkinter)

- Action buttons: blue color
- Settings button → opens modal settings dialog
- Settings dialog: all config items editable from GUI; saves to `.env`
- Settings requiring restart: shown in red with "再起動後に適用されます"
- Layout: generate 3 proposals → user selects one

---

## Language Rules

- **English only**: all `print()` and `logger` output (bat files render Japanese as garbage in CP932)
- **Japanese allowed**: code comments, `.env.sample` comments, GUI display strings
