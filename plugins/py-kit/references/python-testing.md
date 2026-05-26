# Python Testing Standards — py-kit

Logger setup, test policy, and pytest conventions for full Python projects.
Read together with `python-core.md` and `python-architecture.md`.

This file does **not** apply to simple scripts — those use inline
`logging.basicConfig()` and have no test suite. See `python-scripts.md`.

---

## 1. Logger Specification

### 1.1 Required `logger.py`

Every project ships a `{package_name}/logger.py` with a `setup_logger()` function. Below is the canonical implementation that satisfies every rule in this section.

```python
"""{package_name}.logger — application-wide logger setup."""

import logging
import sys
from datetime import datetime
from pathlib import Path

from {package_name}.constants import LOG_DIR, PROJECT_NAME

LOG_FORMAT = "[%(asctime)s] %(levelname)s %(name)s %(filename)s:%(lineno)d - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(level: int = logging.INFO) -> logging.Logger:
    """Initialize the root application logger. Idempotent: safe to call twice."""
    root = logging.getLogger(PROJECT_NAME)
    if root.handlers:
        return root  # already configured; avoid duplicate handlers

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / f"{datetime.now():%Y%m%d_%H%M%S}_{PROJECT_NAME}.log"

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    root.setLevel(level)
    root.addHandler(stream_handler)
    root.addHandler(file_handler)
    root.propagate = False  # do not bubble up to the global root logger

    return root


def get_logger(name: str) -> logging.Logger:
    """Return a child logger of the application root. Use in submodules."""
    return logging.getLogger(f"{PROJECT_NAME}.{name}")
```

### 1.2 Logger Rules (Hard)

| Rule | Reason |
|---|---|
| `LOG_DIR` defined in `constants.py`, not hardcoded inside `logger.py` | Other code reads `LOG_DIR` too (rotation, cleanup) |
| `LOG_DIR.mkdir(parents=True, exist_ok=True)` inside `setup_logger()` | Empty `log/` is removed by some Windows cleanup tools |
| Log filename includes timestamp: `YYYYMMDD_HHMMSS_{package_name}.log` | One file per run; never overwritten; sortable |
| Both `StreamHandler(sys.stdout)` and `FileHandler(..., encoding="utf-8")` | Console for the dev, file for the audit trail |
| `encoding="utf-8"` on the `FileHandler` | Default is platform-dependent — explicit is safer |
| Format includes `filename:lineno` | Cuts debugging time when a message comes from an unexpected place |
| Idempotency guard: `if root.handlers: return root` | `setup_logger()` may be called more than once (e.g. tests) |
| `root.propagate = False` | Prevents duplicate output via Python's global root logger |
| Submodules: `get_logger(__name__)` | Hierarchical logger naming; per-module level control later |

### 1.3 Where to Call `setup_logger()`

Exactly once, in the composition root (`main.py` or `__main__.py`), as early as
possible. Use the returned logger to log the boot sequence.

```python
# {package_name}/main.py
from {package_name}.logger import setup_logger

def main() -> None:
    logger = setup_logger()
    logger.info("Starting %s", PROJECT_NAME)
    ...
```

### 1.4 Using the Logger in Submodules

```python
# {package_name}/application/use_cases/create_order.py
from {package_name}.logger import get_logger

logger = get_logger(__name__)  # module-level

class CreateOrderUseCase:
    def execute(self, input: CreateOrderInput) -> Order:
        logger.info("Creating order for customer %s", input.customer_id)
        ...
```

### 1.5 Log Level Per Subsystem (Advanced)

When some modules are too chatty, raise their level individually:

```python
# main.py, after setup_logger()
logging.getLogger(f"{PROJECT_NAME}.infrastructure.persistence").setLevel(logging.WARNING)
```

Configure via env var if you need it at runtime:

```python
# config.py
class Settings(BaseModel):
    log_level: str = "INFO"
    log_levels_per_module: dict[str, str] = Field(default_factory=dict)
```

### 1.6 Forbidden Logger Patterns

```python
# ❌ Bad — module-level basicConfig in a library module
import logging
logging.basicConfig(level=logging.DEBUG)  # leaks into every caller

# ❌ Bad — f-string in logger call (defeats deferred formatting)
logger.info(f"Order {order.id} created")

# ✅ Good — % formatting; cost is deferred when level is off
logger.info("Order %s created", order.id)

# ❌ Bad — bare `print()` for runtime errors
print(f"Failed: {e}")

# ✅ Good — logger.error captures stack frame, severity, file location
logger.error("Failed", exc_info=True)

# ❌ Bad — Japanese in logger output (CP932 corruption in bat-launched runs)
logger.info("注文を作成しました")

# ✅ Good — English
logger.info("Order created")
```

---

## 2. Test Policy

py-kit projects use a **boundary-testing** policy: tests verify behavior at
meaningful boundaries (use case, repository, API endpoint), not individual
methods.

### 2.1 What to Test / What Not to Test

| Test kind | Policy | Why |
|---|---|---|
| Use case tests | ✅ Always | The use case is the unit of value; testing it covers what the user actually does |
| Domain logic tests (pure functions, value objects) | ✅ When complex | If the rule is hard to verify by reading, write a test |
| Repository tests (infrastructure) | ✅ Against a real test DB (Postgres in a container) or in-memory impl | Catches SQL / schema mistakes |
| HTTP endpoint tests (interface) | ✅ With FastAPI `TestClient` | Catches routing / serialization mistakes |
| E2E tests (CLI / API end-to-end) | ✅ For top critical paths only | High maintenance cost |
| Unit tests for individual methods | ❌ Do not write | Maintenance cost > value in AI-assisted development; tests follow refactoring poorly |
| Tests of getters / setters / dataclass fields | ❌ Do not write | Tests trivial code |
| Tests of third-party libraries | ❌ Do not write | Not your code |

### 2.2 Mock Policy — Mock Only at Boundaries

Tests mock only external I/O boundaries: DB, HTTP, file system, message queues,
LLM APIs, OS APIs. Domain logic and application services are tested with their
real implementations.

| Test target | Mocked | Real |
|---|---|---|
| Use case | repositories, payment gateway, LLM client | domain entities, value objects |
| Domain service | nothing (it's pure) | everything |
| Repository | database connection / HTTP client | the SQL / serialization code |
| HTTP endpoint | the full use case via in-memory infrastructure | router, middleware, Pydantic |

Use the Protocols defined in `domain/repositories/` as the seam — implement
fake versions for tests in `tests/mocks/`.

### 2.3 Test Folder Structure

`tests/` mirrors the source package, plus shared fixtures and mocks at the top.

```
tests/
├── conftest.py                   # shared fixtures (loaded automatically by pytest)
├── mocks/
│   ├── __init__.py
│   ├── mock_env.py               # env var mocking helper
│   ├── mock_externals.py         # stubs for external API clients
│   └── in_memory_order_repository.py  # fake repository implementing the Protocol
├── domain/                       # mirrors {pkg}/domain/
│   ├── entities/
│   │   └── test_order.py
│   └── value_objects/
│       └── test_money.py
├── application/                  # mirrors {pkg}/application/
│   └── use_cases/
│       └── test_create_order.py
├── infrastructure/               # mirrors {pkg}/infrastructure/
│   └── persistence/
│       └── test_postgres_order_repository.py
├── interface/                    # mirrors {pkg}/interface/
│   └── api/
│       └── routers/
│           └── test_orders_router.py
└── e2e/                          # cross-layer scenarios
    └── test_create_order_e2e.py
```

### 2.4 Test File / Function Naming

| Target | Convention |
|---|---|
| Test file | `test_{module}.py` — mirrors the source module name |
| Test function | `test_{behavior}` — describes what is verified, not what is called |
| Test class (only when grouping is genuinely useful) | `Test{ClassName}` |

```python
# ✅ Good — describes the behavior under test
def test_returns_none_when_not_found(): ...
def test_raises_refund_window_closed_after_30_days(): ...
def test_create_order_emits_order_placed_event(): ...

# ❌ Bad — describes the call, not the behavior
def test_find_by_id(): ...
def test_refund(): ...
def test_main(): ...
```

### 2.5 Use Case Test Template

```python
# tests/application/use_cases/test_create_order.py
import pytest

from {pkg}.application.use_cases.create_order import (
    CreateOrderUseCase,
    CreateOrderInput,
)
from {pkg}.domain.entities.order import Order
from {pkg}.domain.value_objects.customer_id import CustomerId
from tests.mocks.in_memory_order_repository import InMemoryOrderRepository
from tests.mocks.fake_payment_gateway import FakePaymentGateway


@pytest.fixture
def order_repo() -> InMemoryOrderRepository:
    return InMemoryOrderRepository()


@pytest.fixture
def payments() -> FakePaymentGateway:
    return FakePaymentGateway()


@pytest.fixture
def use_case(order_repo: InMemoryOrderRepository, payments: FakePaymentGateway) -> CreateOrderUseCase:
    return CreateOrderUseCase(order_repo, payments)


def test_saves_order_and_charges_customer(use_case: CreateOrderUseCase, order_repo: InMemoryOrderRepository, payments: FakePaymentGateway) -> None:
    input = CreateOrderInput(
        customer_id=CustomerId("cust-1"),
        line_items=[...],
    )

    order = use_case.execute(input)

    saved = order_repo.find_by_id(order.id)
    assert saved is not None
    assert saved.customer_id == input.customer_id
    assert payments.charged_amount(input.customer_id) == order.total
```

### 2.6 Repository Test Template — Against a Real DB

For repository tests, hit a real test database (Postgres in a container, SQLite
in a temp file, etc.). Mocks here defeat the purpose of testing the SQL.

```python
# tests/infrastructure/persistence/test_postgres_order_repository.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from {pkg}.infrastructure.persistence.postgres_order_repository import PostgresOrderRepository

@pytest.fixture
def session() -> Session:
    engine = create_engine("postgresql://test:test@localhost:5433/test_db")
    with Session(engine) as s:
        yield s
        s.rollback()  # leave the DB clean


def test_find_by_id_returns_saved_order(session: Session) -> None:
    repo = PostgresOrderRepository(session)
    order = Order(id=OrderId("o-1"), ...)
    repo.save(order)
    session.commit()

    fetched = repo.find_by_id(OrderId("o-1"))

    assert fetched is not None
    assert fetched.id == order.id
```

### 2.7 HTTP Endpoint Test Template

```python
# tests/interface/api/routers/test_orders_router.py
from fastapi.testclient import TestClient

from {pkg}.main import build_app
from tests.mocks.fake_container import build_fake_container


def test_post_orders_returns_201_on_success() -> None:
    app = build_app(container=build_fake_container())
    client = TestClient(app)

    response = client.post("/orders", json={"customer_id": "cust-1", "line_items": [...]})

    assert response.status_code == 201
    assert response.json()["id"]
```

`build_fake_container()` wires the same use cases with in-memory infrastructure
so the test exercises routing + serialization + business logic without DB.

### 2.8 Parametrized Tests

For closed-set inputs, use `@pytest.mark.parametrize`:

```python
@pytest.mark.parametrize(
    ("amount", "expected_tax"),
    [
        (100, 8),
        (500, 40),
        (10_000, 800),
    ],
)
def test_calculates_tax(amount: int, expected_tax: int) -> None:
    assert calculate_tax(amount) == expected_tax
```

### 2.9 Fixtures — Scope and Sharing

| Scope | Use for |
|---|---|
| `function` (default) | Most fixtures — fresh state per test |
| `module` | Expensive setup shared by one test file (e.g. spin up a webdriver) |
| `session` | Truly global setup (e.g. start a test container once) |
| `class` | Rare — only when tests in a class need shared state |

Put broadly-shared fixtures in the **top-level** `conftest.py`. Put folder-specific fixtures in a nested `conftest.py` (pytest discovers them automatically).

---

## 3. Source ↔ Test Linkage

When a source file is changed, the corresponding test file must be updated. This
is a project-level rule (enforce via `.claude/rules/source-test-link.md`).

| Source change | Test action |
|---|---|
| New public method on use case / repository | Add a test verifying the new behavior |
| Changed signature of public method | Update affected tests; ensure callers still pass |
| Bug fix | Add a regression test that fails before the fix and passes after |
| Refactor with no behavior change | Verify the existing tests still pass; do not add new ones |
| Removed code | Delete the corresponding test |

The test file path is mechanical: `{pkg}/domain/entities/order.py` → `tests/domain/entities/test_order.py`.

---

## 4. Running Tests

### 4.1 Local

```bash
pytest                    # all tests
pytest tests/application  # one folder
pytest -k create_order    # by name substring
pytest -x                 # stop on first failure
pytest --lf               # rerun last failures
pytest -v                 # verbose
```

### 4.2 With Coverage

```bash
pytest --cov={package_name} --cov-report=term-missing
```

A coverage threshold (e.g. 80%) can be enforced in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = "--cov={package_name} --cov-fail-under=80"
```

> Coverage is a smell-detector, not a quality metric. High coverage of trivial
> getters is meaningless. Aim for high coverage of use cases and domain logic;
> infrastructure coverage is best measured by whether all branches are exercised
> by realistic scenarios.

### 4.3 Test Discovery

pytest discovers tests in `tests/` automatically. Configuration in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
python_classes = ["Test*"]
```

---

## 5. Definition of Done — Testing Checklist

Before considering a change "done":

- [ ] All affected use cases have at least one test covering the new / changed behavior (§ 2.1)
- [ ] Bug fixes have a regression test that fails on the old code (§ 3)
- [ ] Mocks are used only at external I/O boundaries (§ 2.2)
- [ ] Test file path mirrors source path (§ 2.3)
- [ ] Test function name describes behavior, not call (§ 2.4)
- [ ] `pytest` passes with no warnings
- [ ] Coverage of the changed code is meaningful (not just lines covered, but branches)
- [ ] Logger is set up per § 1 (if the change touched the boot sequence)
- [ ] No `print()` debugging left in the code (replace with `logger.debug`)
