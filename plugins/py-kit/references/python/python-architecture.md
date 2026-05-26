# Python Architecture Standards — py-kit

Architecture patterns and design principles for full Python projects.

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

## Layered Architecture

Structure code in layers. Folder names are not prescribed — organize according to what makes sense for the project. The key constraint is the **dependency direction**: high-level layers depend on abstractions; low-level layers provide implementations.

### Layer roles

| Layer | Responsibility |
|---|---|
| Entry point / interface | CLI arg parsing, HTTP routing, GUI events, bat launchers. No business logic. |
| Business logic | Core rules and use-case orchestration. Calls out through Protocol interfaces only. |
| External boundary | Concrete implementations of those interfaces: DB clients, external API adapters, file I/O, message queues. |

### External boundary isolation

Any code that touches an external service (HTTP API, database, file system, message queue) must be placed in the external boundary layer and accessed only through a `Protocol` defined in the business logic layer.

```python
# Defined in business logic layer — no import from external libraries here
class OrderRepository(Protocol):
    def find_by_id(self, order_id: str) -> Optional[Order]: ...
    def save(self, order: Order) -> None: ...

# Implemented in external boundary layer
class PostgresOrderRepository:
    def __init__(self, conn: Connection) -> None:
        self._conn = conn
    def find_by_id(self, order_id: str) -> Optional[Order]: ...
    def save(self, order: Order) -> None: ...
```

### Architecture quality checklist

- [ ] Business logic layer imports only stdlib, internal modules, and Protocols — no external library imports
- [ ] All external service calls go through a Protocol interface
- [ ] No concrete external-library class instantiated inside the business logic layer
- [ ] Dependency injection used everywhere — constructor receives Protocol, not concrete class

---

## No Hardcoding

Never embed configuration values directly in source code.

**Hardcoded (bad):**

```python
BASE_URL = "https://api.example.com"  # inside business logic
TIMEOUT = 30
MAX_RETRY = 3
OUTPUT_DIR = "/tmp/output"
```

**Externalized (good):**

```python
# constants.py — project-wide computed paths only
PROJECT_ROOT = Path(__file__).parent.parent
LOG_DIR = PROJECT_ROOT / "log"

# config.py — reads from environment / config file at startup
BASE_URL: str = os.environ["API_BASE_URL"]
TIMEOUT: int = int(os.environ.get("API_TIMEOUT", "30"))
```

**Rules:**
- All URLs, ports, file paths, credentials, thresholds, and feature flags go in `.env` / config files
- Use `.env.sample` to document every required variable
- `constants.py` is only for computed paths derived from `__file__` (not for magic numbers or strings)
- Search for bare string literals and magic numbers in business logic before every commit

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
