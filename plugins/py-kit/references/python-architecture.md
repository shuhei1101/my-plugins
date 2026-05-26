# Python Architecture Standards — py-kit

Architecture patterns and design principles for full Python projects.
Read together with `python-core.md`. This file is required reading for
any project work (new project, refactor, feature addition).

---

## 1. SOLID Principles

### 1.1 S — Single Responsibility

Each class has exactly one reason to change. Split by axis of change, not by file size.

```python
# ❌ Bad — three reasons to change: auth logic, email format, DB schema
class UserService:
    def authenticate(self, email: str, password: str) -> User: ...
    def send_welcome_email(self, user: User) -> None: ...
    def save(self, user: User) -> None: ...

# ✅ Good — one reason each
class AuthService:
    def authenticate(self, email: str, password: str) -> User: ...

class WelcomeEmailSender:
    def send(self, user: User) -> None: ...

class UserRepository(Protocol):
    def save(self, user: User) -> None: ...
```

**Detection heuristics:**
- The class name needs "and" to describe it (`UserAndEmailService`)
- Different methods change for different reasons in `git log`
- A method touches private fields no other method touches

### 1.2 O — Open / Closed

Open for extension, closed for modification. Add behavior by adding code, not by editing existing classes.

```python
# ❌ Bad — every new format requires editing this function
def export(data: list[dict], fmt: str) -> bytes:
    if fmt == "csv":
        return _to_csv(data)
    elif fmt == "json":
        return _to_json(data)
    elif fmt == "parquet":     # added next sprint
        return _to_parquet(data)
    raise ValueError(f"unknown format: {fmt}")

# ✅ Good — new format = new class; no edits to existing code
class ExportStrategy(Protocol):
    def export(self, data: list[dict]) -> bytes: ...

class CsvExporter:
    def export(self, data: list[dict]) -> bytes: ...

class JsonExporter:
    def export(self, data: list[dict]) -> bytes: ...

def export_with(strategy: ExportStrategy, data: list[dict]) -> bytes:
    return strategy.export(data)
```

When to apply OCP rigorously: code that is **read** by many other modules. When it's overkill: leaf code with no callers.

### 1.3 L — Liskov Substitution

A subclass must be substitutable for its base without breaking callers. Never:

- Weaken postconditions (return less than the base promises)
- Strengthen preconditions (require more from the caller than the base does)
- Throw exceptions the base does not document

```python
# ❌ Bad — subclass raises where base does not, breaks every caller
class FileRepository(Protocol):
    def save(self, content: bytes) -> None: ...

class ReadOnlyFileRepository:
    def save(self, content: bytes) -> None:
        raise NotImplementedError("read-only")  # LSP violation

# ✅ Good — split the Protocol so callers ask only for what they need
class FileReader(Protocol):
    def read(self) -> bytes: ...

class FileWriter(Protocol):
    def write(self, content: bytes) -> None: ...

class ReadOnlyFile(FileReader):
    def read(self) -> bytes: ...

class ReadWriteFile(FileReader, FileWriter):
    def read(self) -> bytes: ...
    def write(self, content: bytes) -> None: ...
```

### 1.4 I — Interface Segregation

Many small focused protocols over one large general interface. Clients depend only on what they use.

```python
# ❌ Bad — every consumer must accept stat / list even if they don't use them
class IStorage(Protocol):
    def read(self, path: str) -> bytes: ...
    def write(self, path: str, content: bytes) -> None: ...
    def delete(self, path: str) -> None: ...
    def list(self, prefix: str) -> list[str]: ...
    def stat(self, path: str) -> StorageStat: ...

# ✅ Good — clients depend on the smallest Protocol they need
class Readable(Protocol):
    def read(self, path: str) -> bytes: ...

class Writable(Protocol):
    def write(self, path: str, content: bytes) -> None: ...

class Listable(Protocol):
    def list(self, prefix: str) -> list[str]: ...

class ReadWritable(Readable, Writable, Protocol):
    """Compose smaller Protocols when a client really needs both."""
```

### 1.5 D — Dependency Inversion

High-level modules depend on abstractions, not on concrete implementations. Inject dependencies via constructor.

```python
# ❌ Bad — ReportService is now hard-wired to PostgresDatabase
class ReportService:
    def __init__(self) -> None:
        self.db = PostgresDatabase()

# ✅ Good — depends on a Protocol; concrete class is injected
class ReportService:
    def __init__(self, repo: UserRepository) -> None:  # UserRepository is a Protocol
        self._repo = repo
```

**Detection heuristic:** if you cannot test the class without spinning up a real DB / HTTP server / file system, DIP is violated. The fix is to extract a Protocol and inject a fake implementation in tests.

---

## 2. DRY Principle — Carefully

Extract duplication only when it has a **stable, named concept** behind it. Three similar lines is better than a premature abstraction with no clear name.

| Duplicate kind | When to extract | What to extract |
|---|---|---|
| Same literal value in 3+ places | Almost always | Constant in `constants.py` |
| Same business rule expressed two ways | Always | Function with a domain-meaningful name |
| Same class structure across features | When the concept is named (`Repository`, `Aggregate`, `EventHandler`) | Base class or generic |
| Same config keys | Always | Config file / env var with a documented name |
| Looks-similar code in different domains | **Never** | The similarity is coincidental |

```python
# ❌ Bad — fake DRY: "process_with_logging" is not a domain concept
def process_user(u: User) -> None: ...
def process_order(o: Order) -> None: ...
def process_with_logging(item: Any) -> None:  # over-abstracted
    logger.info("processing %s", item)
    ...

# ✅ Good — kept duplicate because the concept of "process X with logging" is not a real concept
def process_user(u: User) -> None:
    logger.info("processing user %s", u.id)
    ...

def process_order(o: Order) -> None:
    logger.info("processing order %s", o.id)
    ...
```

When in doubt, **wait for the third instance** before extracting.

---

## 3. Layered Architecture — Pure DDD

py-kit's standard project layout is **pure Domain-Driven Design**: domain at the
center, application orchestrating use cases, infrastructure implementing external
concerns, interface translating between the outside world and use cases.

### 3.1 Dependency Direction (Hard Rule)

```
interface ──┐
            ├─► application ──► domain
infrastructure ──┘                ▲
                                  │
infrastructure also implements Protocols defined in domain
```

| Layer | May import from | Must NOT import from |
|---|---|---|
| `domain/` | stdlib, `typing`, `pydantic` (boundary models only) | application, infrastructure, interface, external service SDKs |
| `application/` | domain, stdlib | infrastructure, interface, external SDKs |
| `infrastructure/` | domain (to implement Protocols), application (rarely), stdlib, third-party SDKs | interface |
| `interface/` | application, domain (read-only — e.g. for type annotations) | infrastructure |

Violating the rule is a refactoring debt; do not work around it with `if TYPE_CHECKING`.

### 3.2 Layer Roles

| Layer | Responsibility | Example modules |
|---|---|---|
| `interface/` | Translate from the outside (HTTP, CLI, GUI) into a use case call; translate the result back. No business logic. | `interface/cli/main.py`, `interface/api/routers/users.py` |
| `application/` | Use case orchestration: receive a use case input, call domain services and repositories in the right order, return a use case output. | `application/use_cases/create_order.py` |
| `domain/` | Pure business rules. Entities, value objects, domain services, Protocol definitions for repositories and external services. | `domain/entities/order.py`, `domain/repositories/order_repository.py` |
| `infrastructure/` | Concrete implementations of domain Protocols. DB clients, HTTP adapters, file I/O, message queues. | `infrastructure/persistence/postgres_order_repository.py`, `infrastructure/external_apis/stripe_client.py` |

### 3.3 Boundary Rule — Protocol in Domain, Implementation in Infrastructure

Any code that touches an external service must:

1. Have its **Protocol** defined in `domain/repositories/` or `domain/services/`
2. Have its **concrete implementation** in `infrastructure/`
3. Be **wired** in the composition root (see § 5)

```python
# domain/repositories/order_repository.py — no external library imports here
from typing import Protocol
from {pkg}.domain.entities.order import Order

class OrderRepository(Protocol):
    def find_by_id(self, order_id: OrderId) -> Order | None: ...
    def save(self, order: Order) -> None: ...

# infrastructure/persistence/postgres_order_repository.py — concrete impl
import psycopg
from {pkg}.domain.entities.order import Order
from {pkg}.domain.repositories.order_repository import OrderRepository

class PostgresOrderRepository:
    def __init__(self, conn: psycopg.Connection) -> None:
        self._conn = conn

    def find_by_id(self, order_id: OrderId) -> Order | None: ...
    def save(self, order: Order) -> None: ...
```

This ensures:

- The business logic layer has zero knowledge of which external service is used
- External services can be swapped without touching business logic
- Tests can inject a fake implementation without hitting real infrastructure

### 3.4 Architecture Quality Checklist

- [ ] `domain/` imports only stdlib, internal modules, `typing`, and (optionally) Pydantic — no external SDKs
- [ ] `application/` imports only `domain/` and stdlib — no infrastructure imports
- [ ] All Protocols are defined in `domain/`; implementations live in `infrastructure/`
- [ ] No concrete external-library class is instantiated inside `domain/` or `application/`
- [ ] Dependency injection used at every boundary — constructor receives a Protocol, not a concrete class
- [ ] Composition root (typically `main.py` or `container.py`) is the only place where concrete classes are wired together

---

## 4. No Hardcoding

Never embed configuration values directly in source code. They belong in `.env`,
config files, or `constants.py` (computed paths only).

### 4.1 What Counts as Hardcoded

| Value kind | Where it belongs |
|---|---|
| URLs / endpoints | `.env` → `config.py` |
| Ports | `.env` → `config.py` |
| File paths | `constants.py` (if derived from `__file__`) or `.env` (if absolute) |
| Credentials / API keys | `.env` (never committed) |
| Retry / timeout values | `.env` or `config.py` |
| Feature flags | `.env` or config file |
| Magic numbers | Module constant with a meaningful name |
| User-facing error messages | Config file / template file |

### 4.2 Examples

```python
# ❌ Bad — hardcoded everywhere
class ApiClient:
    def fetch(self, path: str) -> dict:
        return httpx.get(
            f"https://api.example.com{path}",     # URL hardcoded
            timeout=30.0,                          # timeout hardcoded
            headers={"X-Api-Key": "sk-abc123"},   # credentials hardcoded
        ).json()

# ✅ Good — externalized
# constants.py
PROJECT_ROOT: Path = Path(__file__).parent.parent
LOG_DIR: Path = PROJECT_ROOT / "log"

# config.py
class Settings(BaseModel):
    api_base_url: str
    api_timeout: float = 30.0
    api_key: SecretStr

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            api_base_url=os.environ["API_BASE_URL"],
            api_timeout=float(os.environ.get("API_TIMEOUT", "30.0")),
            api_key=SecretStr(os.environ["API_KEY"]),
        )

# api_client.py
class ApiClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def fetch(self, path: str) -> dict:
        return httpx.get(
            f"{self._settings.api_base_url}{path}",
            timeout=self._settings.api_timeout,
            headers={"X-Api-Key": self._settings.api_key.get_secret_value()},
        ).json()
```

### 4.3 `.env.sample` Is the Spec

`.env.sample` documents every environment variable the project reads. It is checked into git; `.env` is not.

```bash
# .env.sample — every key the app reads, with a placeholder value and a comment
# 外部 API のベース URL
API_BASE_URL=https://api.example.com
# 外部 API のタイムアウト（秒）
API_TIMEOUT=30.0
# 外部 API の認証キー（コミット禁止）
API_KEY=sk-replace-me
```

CI checks: a test that loads `.env.sample`, parses it, and verifies every key is consumed somewhere in the codebase.

### 4.4 `constants.py` — Computed Paths Only

`constants.py` exists only to hold paths computed at import time. It must not hold business constants, magic numbers, or configurable values.

```python
# ✅ Good
PROJECT_ROOT: Path = Path(__file__).parent.parent
LOG_DIR: Path = PROJECT_ROOT / "log"
TEMPLATE_DIR: Path = PROJECT_ROOT / "templates"

# ❌ Bad — these are configurable, not computed
MAX_RETRY = 3
API_BASE_URL = "https://api.example.com"
DEFAULT_LANGUAGE = "ja"
```

---

## 5. Composition Root and Dependency Injection

### 5.1 What the Composition Root Is

The composition root is the single place where:

- All concrete classes are instantiated
- All dependencies are wired together
- Settings are loaded

Typically `main.py` (for CLIs) or `container.py` (for FastAPI services). Every other file receives its dependencies through constructor parameters.

### 5.2 Minimal Composition Root

```python
# main.py
def build_container() -> Container:
    settings = Settings.from_env()
    logger = setup_logger(LOG_DIR)

    # infrastructure
    db_conn = psycopg.connect(settings.database_url)
    order_repo = PostgresOrderRepository(db_conn)
    stripe_client = StripeClient(settings.stripe_api_key)

    # application
    create_order = CreateOrderUseCase(order_repo, stripe_client)
    cancel_order = CancelOrderUseCase(order_repo, stripe_client)

    return Container(
        create_order=create_order,
        cancel_order=cancel_order,
        logger=logger,
    )

def main() -> None:
    container = build_container()
    # hand container to whatever entry point needs it
    ...

if __name__ == "__main__":
    main()
```

### 5.3 Constructor Injection — Mandatory

Every collaborator a class needs comes in through `__init__`. Never:

```python
# ❌ Bad — instantiating a concrete class inside the body
class CreateOrderUseCase:
    def __init__(self) -> None:
        self._repo = PostgresOrderRepository(...)
        self._payments = StripeClient(...)

# ❌ Bad — global singleton lookup
class CreateOrderUseCase:
    def execute(self, ...) -> Order:
        repo = ServiceLocator.get(OrderRepository)
        ...
```

```python
# ✅ Good — collaborators injected
class CreateOrderUseCase:
    def __init__(
        self,
        order_repo: OrderRepository,
        payments: PaymentGateway,
    ) -> None:
        self._order_repo = order_repo
        self._payments = payments

    def execute(self, input: CreateOrderInput) -> Order:
        ...
```

### 5.4 Container Class (Optional, for Larger Projects)

For projects with 20+ use cases, group them in a `Container` dataclass:

```python
@dataclass(frozen=True)
class Container:
    create_order: CreateOrderUseCase
    cancel_order: CancelOrderUseCase
    fulfill_order: FulfillOrderUseCase
    logger: logging.Logger
```

Pass the container into FastAPI via `app.state` or into a CLI via the main function.

Avoid heavy DI frameworks (`dependency-injector`, `injector`) unless the project genuinely outgrows manual wiring. Explicit wiring in `main.py` is the default.

---

## 6. Design Patterns

### 6.1 Strategy

Encapsulate interchangeable algorithms behind a Protocol. Use when:

- Multiple algorithms achieve the same outcome
- The choice is made at runtime (config, user input, plugin selection)
- New algorithms may be added in the future

```python
class SortStrategy(Protocol):
    def sort(self, items: list[int]) -> list[int]: ...

class QuickSort:
    def sort(self, items: list[int]) -> list[int]: ...

class MergeSort:
    def sort(self, items: list[int]) -> list[int]: ...

# Caller picks
def process(items: list[int], strategy: SortStrategy) -> list[int]:
    return strategy.sort(items)
```

Strategy gives the **caller** control of the algorithm — they can swap one strategy for another at any time.

### 6.2 Template Method

Define the skeleton of an algorithm in a base class; subclasses override only the **steps that vary**. Use when:

- The overall flow is fixed (validate → transform → persist → notify)
- Only specific steps differ per concrete type
- You want the framework — not the subclass — to enforce the order

```python
from abc import ABC, abstractmethod

class ReportGenerator(ABC):
    """Template Method: defines the report generation algorithm.
    Subclasses override only _load and _format; the flow is fixed."""

    def generate(self, source: str) -> bytes:
        raw = self._load(source)
        validated = self._validate(raw)
        formatted = self._format(validated)
        return self._render(formatted)

    @abstractmethod
    def _load(self, source: str) -> dict: ...

    def _validate(self, data: dict) -> dict:
        """Default impl — subclasses may override if they need stricter validation."""
        if not data:
            raise EmptyReportSourceError(source)
        return data

    @abstractmethod
    def _format(self, data: dict) -> dict: ...

    def _render(self, data: dict) -> bytes:
        """Default impl — JSON. Override for CSV / PDF / etc."""
        return json.dumps(data).encode("utf-8")


class SalesReportGenerator(ReportGenerator):
    def _load(self, source: str) -> dict:
        return self._sales_repo.fetch(source)

    def _format(self, data: dict) -> dict:
        return {"total": sum(row["amount"] for row in data["rows"])}


class CsvSalesReportGenerator(SalesReportGenerator):
    def _render(self, data: dict) -> bytes:
        return to_csv(data).encode("utf-8")
```

#### Template Method vs Strategy — When to Pick Which

| Aspect | Template Method | Strategy |
|---|---|---|
| Who controls the algorithm flow | Base class (fixed) | Caller (free) |
| Where variation lives | Subclass override of specific steps | Separate class implementing a Protocol |
| Coupling | Strong — subclass inherits the base | Loose — strategy is composed in |
| Use when | The flow must not change; steps vary | The whole algorithm varies; flow is incidental |
| Risk | LSP violation if a subclass weakens postconditions | None specific |

**Pick Template Method when** you want to enforce "the framework runs these steps in this order; you cannot skip or reorder them; you can only fill in the blanks."

**Pick Strategy when** the variability is the algorithm itself, and you want callers to swap strategies freely.

### 6.3 Factory

Centralize object creation logic. Use when:

- Construction is complex or conditional
- The caller should not need to know which concrete class is returned

```python
def create_exporter(fmt: Literal["csv", "json", "parquet"]) -> ExportStrategy:
    match fmt:
        case "csv":     return CsvExporter()
        case "json":    return JsonExporter()
        case "parquet": return ParquetExporter()
```

For complex construction (multiple optional collaborators), use a builder-style factory class.

### 6.4 Decorator

Add cross-cutting behavior (logging, caching, retry, metrics) without modifying the original class. Use when:

- The cross-cutting concern applies to multiple unrelated classes
- You want to compose behavior (logging + caching + retry)

```python
class LoggingRepository:
    """Decorator: wraps another UserRepository, adds logging on every call."""

    def __init__(self, inner: UserRepository, logger: logging.Logger) -> None:
        self._inner = inner
        self._logger = logger

    def find_by_id(self, user_id: UserId) -> User | None:
        self._logger.debug("find_by_id %s", user_id)
        result = self._inner.find_by_id(user_id)
        self._logger.debug("find_by_id %s -> %s", user_id, "hit" if result else "miss")
        return result

    def save(self, user: User) -> None:
        self._logger.debug("save %s", user.id)
        self._inner.save(user)
```

Decorators compose: `RetryRepository(LoggingRepository(PostgresUserRepository(conn)))`.

### 6.5 Observer (use sparingly)

Notify multiple observers when an event happens. Use only when:

- Multiple unrelated subsystems must react to the same event
- The publisher truly should not know who is listening

For most Python apps, a direct call (or `asyncio.Queue` / `asyncio.Event`) is simpler. Reach for Observer only when the indirection genuinely earns its keep.

---

## 7. Pydantic Boundaries

Use Pydantic models (not just type hints) at system boundaries where runtime validation matters.

### 7.1 When to Use Pydantic

| Use case | Pydantic? |
|---|---|
| External HTTP request body / response | ✅ Yes |
| LLM input / output via Instructor | ✅ Yes |
| Config file read (YAML / JSON / `.env`) | ✅ Yes |
| Data passed between processes / threads as serialized payload | ✅ Yes |
| CSV / JSONL records (one Pydantic model per row) | ✅ Yes |
| User input parsing (CLI args, form submissions) | ✅ Yes |
| Internal function arguments where validation has already happened upstream | ❌ No — type hints are enough |
| `dict` / `list` expressions that stay within a single function | ❌ No |
| Pure dataclass needs (no validation) | ❌ Use `@dataclass` |

### 7.2 Boundary Pattern

Validate at the boundary, pass typed objects inward, return raw types at the outbound boundary.

```python
# interface/api/routers/orders.py — inbound boundary
class CreateOrderRequest(BaseModel):
    customer_id: str
    line_items: list[LineItem]

@router.post("/orders")
async def create_order(body: CreateOrderRequest, container: Container = Depends(...)) -> dict:
    input = CreateOrderInput(customer_id=CustomerId(body.customer_id), line_items=body.line_items)
    order = container.create_order.execute(input)
    return CreateOrderResponse.from_domain(order).model_dump()
```

### 7.3 Pydantic v2 Patterns

```python
from pydantic import BaseModel, Field, model_validator

class Settings(BaseModel):
    api_base_url: str = Field(..., min_length=1)
    api_timeout: float = Field(default=30.0, ge=0.1, le=600.0)
    feature_flags: dict[str, bool] = Field(default_factory=dict)

    @model_validator(mode="after")
    def check_timeout_consistency(self) -> "Settings":
        # cross-field validation
        return self
```

Prefer `BaseModel` over `pydantic.dataclasses.dataclass` for new code — better tooling support.

---

## 8. Project Folder Structure — Pure DDD (Standard)

py-kit's standard layout is **pure Domain-Driven Design**. Folder roles are
fixed; only file names inside each folder vary by project.

```
{project_name}/
├── pyproject.toml
├── README.md
├── .env.sample
├── .gitignore
├── activate.bat                  # Windows only
├── {mode}.bat                    # Windows only — entry per run mode
├── setup/
│   └── setup_venv.bat            # Windows only
├── {package_name}/
│   ├── __init__.py
│   ├── __main__.py               # `python -m {package_name}` entry
│   ├── main.py                   # composition root (see § 5)
│   ├── config.py                 # Settings model + from_env loader
│   ├── constants.py              # computed paths only (no magic values)
│   ├── logger.py                 # setup_logger() — see python-testing.md
│   ├── exceptions.py             # cross-cutting exception base classes
│   ├── interface/                # outside ↔ use case translation
│   │   ├── __init__.py
│   │   ├── cli/                  # CLI entry points (if any)
│   │   │   └── main.py
│   │   └── api/                  # HTTP routes (if FastAPI — see python-fastapi.md)
│   │       ├── __init__.py
│   │       ├── routers/
│   │       │   ├── orders.py
│   │       │   └── users.py
│   │       ├── dependencies.py
│   │       └── middleware.py
│   ├── application/              # use case orchestration
│   │   ├── __init__.py
│   │   └── use_cases/
│   │       ├── create_order.py
│   │       ├── cancel_order.py
│   │       └── list_orders.py
│   ├── domain/                   # pure business rules — no external deps
│   │   ├── __init__.py
│   │   ├── entities/
│   │   │   ├── order.py
│   │   │   ├── customer.py
│   │   │   └── line_item.py
│   │   ├── value_objects/
│   │   │   ├── order_id.py       # NewType("OrderId", str) or BaseModel
│   │   │   ├── money.py
│   │   │   └── address.py
│   │   ├── repositories/         # Protocol definitions only
│   │   │   ├── order_repository.py
│   │   │   ├── customer_repository.py
│   │   │   └── payment_gateway.py
│   │   ├── services/             # domain services (logic that spans entities)
│   │   │   └── order_pricing_service.py
│   │   └── events/               # domain events (optional)
│   │       └── order_placed.py
│   └── infrastructure/           # concrete implementations
│       ├── __init__.py
│       ├── persistence/          # DB / file repositories
│       │   ├── postgres_order_repository.py
│       │   ├── in_memory_order_repository.py
│       │   └── postgres_customer_repository.py
│       ├── external_apis/        # third-party HTTP / SDK adapters
│       │   ├── stripe_payment_gateway.py
│       │   └── sendgrid_email_sender.py
│       └── messaging/            # message queues (optional)
│           └── sqs_event_publisher.py
├── tests/
│   ├── conftest.py
│   ├── mocks/
│   │   ├── mock_env.py
│   │   └── mock_externals.py
│   ├── domain/                   # mirrors source domain/
│   │   └── entities/
│   │       └── test_order.py
│   ├── application/
│   │   └── use_cases/
│   │       └── test_create_order.py
│   ├── infrastructure/
│   │   └── persistence/
│   │       └── test_postgres_order_repository.py
│   └── e2e/                      # end-to-end tests (CLI / API)
│       └── test_create_order_e2e.py
└── log/                          # generated at runtime — .gitkeep'd, .gitignore'd
    └── .gitkeep
```

### 8.1 Layer Folder Rules

| Folder | What goes in | What does NOT go in |
|---|---|---|
| `domain/entities/` | Entity classes (mutable identity-bearing objects) | DB row classes, DTOs, JSON dicts |
| `domain/value_objects/` | Value object classes (immutable, equality by value) | Anything with identity |
| `domain/repositories/` | Protocol definitions for persistence | Concrete repository classes |
| `domain/services/` | Domain services (logic across multiple entities) | Use cases (those go in `application/`) |
| `application/use_cases/` | One use case = one class | Domain logic, infrastructure code |
| `infrastructure/persistence/` | Concrete repository implementations | Protocol definitions |
| `infrastructure/external_apis/` | Adapters for third-party HTTP / SDKs | Business logic |
| `interface/` | Route handlers / CLI parsers / GUI events | Business logic |

### 8.2 File-per-Class Rule

Each public class lives in its own file. The file name matches the class name in `snake_case`:

| Class | File |
|---|---|
| `Order` | `domain/entities/order.py` |
| `OrderRepository` (Protocol) | `domain/repositories/order_repository.py` |
| `PostgresOrderRepository` | `infrastructure/persistence/postgres_order_repository.py` |
| `CreateOrderUseCase` | `application/use_cases/create_order.py` |

Private helper classes / small dataclasses used in one place may share a file with their consumer.

### 8.3 Test Mirror Rule

`tests/` mirrors the source folder structure. A test for `{pkg}/domain/entities/order.py` lives at `tests/domain/entities/test_order.py`.

E2E tests that span multiple layers go in `tests/e2e/`.

---

## 9. Definition of Done — Architecture Checklist

Before considering an architecture change "done", verify:

- [ ] All Protocols are defined in `domain/`; no Protocol lives in `infrastructure/`
- [ ] No `domain/` file imports an external SDK
- [ ] No `application/` file imports from `infrastructure/`
- [ ] Every use case is a class with a single `execute()` method
- [ ] All dependencies flow through constructors (no service-locator, no global singleton)
- [ ] Composition root (`main.py` or `container.py`) is the only place where concrete classes are instantiated
- [ ] No hardcoded URLs / credentials / paths — all in `.env` or `constants.py` (per § 4)
- [ ] `.env.sample` lists every key the app reads, with a comment
- [ ] Pydantic models guard every system boundary (§ 7)
- [ ] Folder layout follows § 8
- [ ] When a new pattern was added, it's the right one — checked against § 6 (Strategy vs Template Method vs Decorator)
