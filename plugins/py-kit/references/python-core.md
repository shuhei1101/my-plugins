# Python Core Standards — py-kit

The always-required baseline for every Python task. Read in full before writing or
editing any Python code. Skipping sections leads to inconsistent code that violates
project conventions.

---

## 1. Naming Conventions

### 1.1 Naming Table

Every name in the codebase must follow exactly one of these patterns. No exceptions.

| Target | Convention | Example | Bad example |
|---|---|---|---|
| Module / file | `snake_case` | `user_repository.py` | `UserRepository.py`, `user-repo.py` |
| Package directory | `snake_case` | `external_apis/` | `ExternalApis/`, `external-apis/` |
| Class | `PascalCase` | `UserRepository`, `OrderId` | `user_repository`, `orderID` |
| Exception class | `PascalCase` + `Error` suffix | `OrderNotFoundError` | `OrderNotFoundException`, `OrderNotFound` |
| Function / method | `snake_case`, verb-led | `find_by_id()`, `save()` | `findById()`, `Save()`, `user()` |
| Variable / argument | `snake_case`, noun-led | `user_id`, `order_total` | `userId`, `OrderTotal` |
| Module-level constant | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` | `MaxRetryCount`, `max_retry_count` |
| Private (module / class) | leading `_` | `_internal_cache`, `_build_query()` | `internalCache`, `__build_query` |
| Name-mangled | leading `__` (no trailing) | `__id` inside a class body | use only when you actually need name mangling |
| Protocol / Interface | `{Name}` (verb-able) — pick ONE style per project: `{Name}able`, `I{Name}`, or `Base{Name}` | `Convertable`, `IConverter`, `BaseConverter` | Mixing styles within one project |
| Type alias | `PascalCase` | `UserId = NewType("UserId", str)` | `user_id_t`, `t_user_id` |
| TypeVar | single uppercase letter or `PascalCase` with `T` suffix | `T`, `K`, `V`, `EntityT` | `entity_t`, `tEntity` |
| Test file | `test_{module}.py` mirroring source | `tests/users/test_user_repository.py` | `user_repo_test.py`, `UserRepoTests.py` |
| Test function | `test_{behavior}` | `test_returns_none_when_not_found()` | `test_1()`, `testReturnsNone()` |
| Fixture (pytest) | `snake_case` | `def user_repo() -> UserRepository:` | `def UserRepo():` |

### 1.2 Verb-Led / Noun-Led Naming

Function names start with a verb. Variables and attributes start with a noun.

```python
# ✅ Good
def fetch_user(user_id: UserId) -> User: ...
def is_valid(value: str) -> bool: ...
def has_permission(user: User, perm: Permission) -> bool: ...

current_user: User = ...
order_count: int = 0

# ❌ Bad — noun-led function, verb-led variable
def user(user_id: UserId) -> User: ...        # name says "what" not "do what"
def validity(value: str) -> bool: ...
fetch: User = ...                             # name says "do what" not "what"
```

### 1.3 Protocol / Interface Naming — Pick One Style

Choose **one** of the three styles for the entire project. Do not mix.

| Style | Pattern | Example |
|---|---|---|
| Adjective | `{Name}able` | `Convertable`, `Readable`, `Cacheable` |
| Hungarian-I | `I{Name}` | `IConverter`, `IReader`, `ICache` |
| Base-prefix | `Base{Name}` | `BaseConverter`, `BaseReader`, `BaseCache` |

> Recommendation: **`{Name}able` style** for pure Protocol definitions (no shared
> implementation), **`Base{Name}` style** for ABCs with shared implementation.
> Document the chosen style in the project's `CLAUDE.md`.

### 1.4 Implementation Class Naming

Implementation classes for a Protocol are prefixed with the implementation tech:

```python
# domain/repositories/user_repository.py
class UserRepository(Protocol):
    def find_by_id(self, user_id: UserId) -> Optional[User]: ...

# infrastructure/persistence/postgres_user_repository.py
class PostgresUserRepository:
    def find_by_id(self, user_id: UserId) -> Optional[User]: ...

# infrastructure/persistence/in_memory_user_repository.py
class InMemoryUserRepository:
    def find_by_id(self, user_id: UserId) -> Optional[User]: ...
```

The file name follows the class name: `postgres_user_repository.py` not `user_repository_postgres.py`.

### 1.5 Boolean Naming

Boolean variables, attributes, and functions start with a state-verb: `is_`, `has_`, `can_`, `should_`, `was_`, `will_`.

```python
# ✅ Good
is_active: bool = True
has_permission: bool = False
def can_edit(user: User, post: Post) -> bool: ...
def should_retry(error: Exception) -> bool: ...

# ❌ Bad
active: bool = True              # ambiguous (state vs imperative?)
permission: bool = False         # noun, not boolean
def edit_check(...): ...         # action-led, not state-led
```

### 1.6 Collection Naming

Collection variables are pluralized.

```python
# ✅ Good
users: list[User] = []
user_ids: set[UserId] = set()
user_by_id: dict[UserId, User] = {}

# ❌ Bad
user_list: list[User] = []       # type-suffix is redundant — the annotation says list
ids: set[UserId] = set()         # ambiguous (ids of what?)
user_map: dict[...] = {}         # ambiguous (key is what?)
```

For dicts, prefer `{value}_by_{key}` over `{key}_to_{value}` or `{key}_{value}_map`.

---

## 2. Comment Rules

### 2.1 What to Comment / What Not to Comment

Comments explain **why**, never what. Code already says what.

| Comment kind | Required? | Notes |
|---|---|---|
| Module-level docstring on script entry | ✅ Required (scripts only — see `python-scripts.md`) | Three-line minimum: name — purpose, usage line |
| Module-level docstring on library module | ⚠️ Optional (only if module purpose is non-obvious) | One line max |
| Class docstring | ⚠️ Optional (required only when class has subtle invariant) | One line, no signature restatement |
| Function / method docstring | ⚠️ Optional (required when function has hidden constraint, side effect, or non-obvious return semantics) | One line, no `:param:` / `:returns:` blocks |
| Inline comment explaining a non-obvious constraint or workaround | ✅ Required when the constraint exists | One line, leading `#` + space |
| Change-history comment | ✅ Required when a non-obvious decision was made for a specific PR | `# PR{N}: {what changed and why}` |
| Restating what code does | ❌ Forbidden | Code is the spec |
| Documenting type info already in the annotation | ❌ Forbidden | Type hints are the spec |

### 2.2 Good / Bad Examples

```python
# ✅ Good — explains hidden constraint
# CP932 parses bat files; Japanese UTF-8 bytes become lead bytes and swallow following chars
bat_text.encode("ascii", errors="strict")

# ✅ Good — explains a workaround tied to a specific bug
# vendored anthropic SDK 0.34 raises StreamError on empty deltas — skip them
if not chunk.delta:
    continue

# ✅ Good — explains business intent that is not obvious from the code
# Refund window is 30 days from the **shipped** date, not the order date (legal req)
if (today - order.shipped_at).days > 30:
    raise RefundWindowClosedError()

# ❌ Bad — restates what the code does
# Set is_open to True
self.is_open = True

# ❌ Bad — restates the type annotation
# user_id is a string
user_id: str = "..."

# ❌ Bad — restates the function name
# This function calculates the total
def calculate_total(items: list[Item]) -> int: ...

# ❌ Bad — long docstring that adds nothing
def find_by_id(user_id: UserId) -> Optional[User]:
    """
    Find a user by id.

    :param user_id: The id of the user to find.
    :returns: The user if found, None otherwise.
    """
```

### 2.3 Docstring Rules

When a docstring is required, keep it to one line and put it on a single physical line:

```python
# ✅ Good — single line, intent-only
def find_by_id(user_id: UserId) -> Optional[User]:
    """Return the user or None if not found. Hits the read replica, not primary."""
    ...

# ✅ Good — one line, behavior-only
def refund(order: Order) -> RefundReceipt:
    """Issue a refund. Raises RefundWindowClosedError after 30 days from ship date."""
    ...
```

Do not use multi-paragraph docstrings, `:param:` / `:returns:` / `Args:` / `Returns:` blocks, or any other RST/Sphinx markup. If you need a structured description, that signals either:

- The function has too many responsibilities (split it), or
- The intent belongs in a class docstring or module-level note, not on the function.

### 2.4 Change-History Comments

When a non-obvious change is made for a specific PR, leave a one-line comment with the PR number and the reason:

```python
# ✅ Good
# PR142: order_date kept for backward compatibility — new code reads shipped_at
order_date: datetime
shipped_at: datetime

# PR98: must precede config.load() because logger.py reads PROJECT_ROOT from constants
import constants  # noqa: E402

# ❌ Bad — no PR number, no reason
# legacy field
order_date: datetime
```

Change-history comments age out — when the surrounding code is rewritten, delete the comment.

### 2.5 Section Marker Comments (Scripts Only)

For single-file scripts, use horizontal-rule section markers to delimit imports, constants, helpers, and main. See `python-scripts.md` for the exact format.

### 2.6 Forbidden Comment Patterns

- `# TODO:` without an owner or issue link — write the actual fix instead, or open an issue and reference it: `# TODO(#142): add retry`
- `# XXX:` / `# FIXME:` without context — meaningless; either fix it or explain why it's deferred
- Commented-out code blocks — delete them; git has the history
- ASCII-art separators inside function bodies — code blocks are already visually delimited

---

## 3. Type Hints

### 3.1 Coverage — Apply Everywhere

Every public symbol must be fully annotated. Internal helpers also benefit but are not strictly required to annotate every local variable.

| Position | Annotation required? |
|---|---|
| Function argument | ✅ Always |
| Function return | ✅ Always — including `-> None` for procedures |
| Class attribute (declared) | ✅ Always |
| `dataclass` / Pydantic field | ✅ Always |
| `__init__` parameters | ✅ Always |
| Local variable when type is inferable from RHS | ⚠️ Optional |
| Local variable when type is non-obvious | ✅ Required (e.g. `x: dict[str, list[int]] = {}`) |
| Lambda | ⚠️ Optional (prefer `def` for anything beyond one expression) |

```python
# ✅ Good — every public symbol annotated
def fetch_user(user_id: UserId) -> Optional[User]:
    cache: dict[UserId, User] = {}  # non-obvious type, annotate
    user = cache.get(user_id)       # inferable, no annotation needed
    return user

# ❌ Bad — missing return annotation
def fetch_user(user_id: UserId):
    ...

# ❌ Bad — missing arg annotations
def fetch_user(user_id):
    ...
```

### 3.2 No Bare `Any` — Tighten It

`Any` disables type checking. Use it only at unavoidable boundaries (parsing untyped data) and narrow as soon as possible.

```python
# ❌ Bad
def process(data: Any) -> Any: ...

# ✅ Good — narrow with TypedDict, dataclass, or Pydantic at the entry point
class RawOrder(TypedDict):
    id: str
    amount: int

def process(data: RawOrder) -> OrderId: ...

# ✅ Acceptable — boundary parsing where Any is unavoidable
def parse_json(raw: str) -> Any:
    return json.loads(raw)

def to_order(raw: Any) -> Order:  # narrow immediately
    return Order.model_validate(raw)
```

### 3.3 Protocol vs ABC

Use `Protocol` for structural interfaces in domain code. Use `ABC` only when you need to share default implementation across subclasses.

```python
# ✅ Protocol — structural typing, no inheritance required
from typing import Protocol, runtime_checkable

@runtime_checkable
class Convertable(Protocol):
    def convert(self, source: str) -> str: ...

# ✅ ABC — when default implementation is needed
from abc import ABC, abstractmethod

class BaseConverter(ABC):
    def convert(self, source: str) -> str:
        validated = self._validate(source)
        return self._convert(validated)

    def _validate(self, source: str) -> str:
        return source.strip()  # default impl

    @abstractmethod
    def _convert(self, source: str) -> str: ...
```

`@runtime_checkable` on Protocols enables `isinstance()` checks at runtime — useful when accepting plugin-like objects.

### 3.4 Modern Generics (Python 3.12+) and Legacy (3.11)

Use the new generic syntax on Python 3.12+:

```python
# Python 3.12+
def first[T](items: list[T]) -> T | None: ...

class Repository[EntityT]:
    def find(self, id: str) -> EntityT | None: ...
```

For 3.11 (and library code that needs broader compatibility), use `TypeVar`:

```python
# Python 3.11 / library code
from typing import TypeVar

T = TypeVar("T")
EntityT = TypeVar("EntityT", bound="Entity")

def first(items: list[T]) -> T | None: ...

class Repository(Generic[EntityT]):
    def find(self, id: str) -> EntityT | None: ...
```

### 3.5 `Optional[T]` vs `T | None`

Prefer `T | None` (PEP 604) over `Optional[T]`. Both are valid; pick one per project.

```python
# ✅ Preferred
def find(id: UserId) -> User | None: ...

# ✅ Acceptable
def find(id: UserId) -> Optional[User]: ...
```

### 3.6 `Literal` for Closed Sets

When an argument is restricted to a fixed set of string / int values, use `Literal`.

```python
# ✅ Good — type checker enforces the closed set
def export(fmt: Literal["csv", "json", "parquet"]) -> bytes: ...

# ❌ Bad — accepts any string, defers the check to runtime
def export(fmt: str) -> bytes:
    if fmt not in ("csv", "json", "parquet"):
        raise ValueError(...)
```

For more than ~5 variants or when adding behavior, use an `Enum` instead.

### 3.7 `NewType` for Identifiers

Wrap primitive-typed identifiers in `NewType` to prevent mix-ups at the type level:

```python
from typing import NewType

UserId = NewType("UserId", str)
OrderId = NewType("OrderId", str)

def find_user(user_id: UserId) -> User: ...

# ✅ Caller must explicitly construct UserId
find_user(UserId("abc"))

# ❌ Type checker rejects this — even though both are strings underneath
find_user(OrderId("abc"))
```

### 3.8 `TypedDict` for Structured Dicts at Boundaries

When data crosses a boundary as a dict (e.g. JSON payloads inside a function), use `TypedDict` to document the shape.

```python
from typing import TypedDict, NotRequired

class WebhookPayload(TypedDict):
    event: Literal["order.created", "order.shipped"]
    order_id: str
    timestamp: int
    note: NotRequired[str]   # optional field
```

For external API boundaries where validation matters, prefer Pydantic. See `python-architecture.md` § Pydantic Boundaries.

### 3.9 Type-Only Imports

Use `from typing import TYPE_CHECKING` for type-only imports to avoid runtime import cycles:

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.entities.user import User

def fetch(user_id: UserId) -> User: ...
```

`from __future__ import annotations` makes all annotations lazy (strings) — required for the above pattern on Python <3.13.

---

## 4. Imports and Module Layout

### 4.1 Import Ordering

```python
# 1. Future
from __future__ import annotations

# 2. stdlib
import argparse
from pathlib import Path
from typing import Optional, Protocol

# 3. Third-party
import httpx
from pydantic import BaseModel

# 4. Local (absolute imports preferred)
from {package_name}.domain.entities.user import User
from {package_name}.domain.repositories.user_repository import UserRepository
```

Use absolute imports for internal modules. Relative imports (`from .user import User`) are acceptable only within tightly-coupled sibling modules — never across layers.

### 4.2 No Wildcard Imports

```python
# ❌ Bad — pollutes namespace, breaks type checking
from {package_name}.domain import *

# ✅ Good
from {package_name}.domain.entities.user import User
from {package_name}.domain.entities.order import Order
```

### 4.3 No Unused Imports

Remove unused imports before commit. Configure ruff / flake8 to fail on `F401`.

---

## 5. Error Handling

### 5.1 Custom Exception Classes per Domain

Define domain-specific exception classes. Do not raise built-in exceptions for business errors.

```python
# ✅ Good — domain exception
class OrderNotFoundError(Exception):
    def __init__(self, order_id: OrderId) -> None:
        super().__init__(f"Order not found: {order_id}")
        self.order_id = order_id

raise OrderNotFoundError(order_id)

# ❌ Bad — built-in for business error
raise ValueError(f"Order {order_id} not found")
```

### 5.2 Exception Layering — Wrap at Boundaries

Catch low-level exceptions at infrastructure boundaries and re-raise as domain exceptions:

```python
# infrastructure/persistence/postgres_order_repository.py
class PostgresOrderRepository:
    def find_by_id(self, order_id: OrderId) -> Order:
        try:
            row = self._conn.execute("SELECT ... WHERE id = ?", (order_id,)).fetchone()
        except psycopg.OperationalError as e:
            raise RepositoryUnavailableError(str(e)) from e
        if row is None:
            raise OrderNotFoundError(order_id)
        return Order.from_row(row)
```

The application layer should never see `psycopg.OperationalError` — only domain or repository exceptions.

### 5.3 `raise ... from ...` Always

Always preserve the original exception with `from`:

```python
# ✅ Good
try:
    ...
except KeyError as e:
    raise ConfigKeyMissingError(str(e)) from e

# ❌ Bad — original traceback lost
except KeyError as e:
    raise ConfigKeyMissingError(str(e))
```

### 5.4 No Bare `except:` — Be Specific

```python
# ❌ Bad — catches KeyboardInterrupt, SystemExit, everything
try: ...
except: ...

# ❌ Bad — too broad
try: ...
except Exception: ...

# ✅ Good — specific
try: ...
except (httpx.ConnectError, httpx.TimeoutException) as e:
    ...
```

The only legitimate `except Exception:` is at the very top of a long-running loop where the loop must continue after logging an unexpected error.

---

## 6. Language Rules

### 6.1 Print and Logger Output — English Only

All `print()` and logger output is in English. Reason: bat launchers run in `cmd.exe`, which uses CP932 on Japanese Windows; non-ASCII output corrupts the log file and the console.

```python
# ✅ Good
print("Starting batch job")
logger.info("Order %s shipped to %s", order_id, address.zip)

# ❌ Bad
print("バッチ処理を開始します")
logger.info("注文 %s を発送しました", order_id)
```

### 6.2 Where Japanese Is Allowed

| Location | Japanese OK? | Notes |
|---|---|---|
| `print()` / logger output | ❌ No | CP932 corruption |
| Code comments | ✅ Yes | But prefer English for shared codebases |
| `.env.sample` comments | ✅ Yes | Read by humans, not bat files |
| GUI display strings (tkinter, etc.) | ✅ Yes | Runs in Python's stdout, not bat |
| Exception message | ⚠️ English preferred | Travels into logs; CP932 may corrupt |
| Docstring | ✅ Yes | Tools read in UTF-8 |
| Pytest test names / messages | ⚠️ English preferred | Test output may flow into CI logs |

### 6.3 String Formatting

| Use case | Pick |
|---|---|
| Inline interpolation in code | f-string: `f"User {user.id} created"` |
| Logger calls | `%`-style: `logger.info("User %s created", user.id)` — defers formatting cost when log level is off |
| User-facing template (multi-line, parameterized) | `string.Template` or a Jinja2 template loaded from file |

```python
# ✅ Good — f-string for inline
msg = f"Order {order.id} totalled {order.total}"

# ✅ Good — % for logger (deferred formatting)
logger.info("Order %s totalled %s", order.id, order.total)

# ❌ Bad — f-string in logger (formatting happens even if log level filters out)
logger.info(f"Order {order.id} totalled {order.total}")
```

### 6.4 No Hardcoded User-Facing Strings — Configurable

User-facing strings (error messages displayed to end users, email templates, etc.) belong in config files or template files, not in source. See `python-architecture.md` § No Hardcoding.

---

## 7. Code Style Quick Reference

| Aspect | Rule |
|---|---|
| Line length | 100 chars (project may override to 88 or 120; document in pyproject.toml) |
| Indentation | 4 spaces — no tabs |
| Quotes | Double quotes for strings; single quotes only for dict keys when consistent within a file |
| Trailing comma | Required on multi-line collection / argument lists |
| Blank lines | 2 between top-level defs, 1 between methods |
| Walrus operator (`:=`) | Use only when it genuinely improves readability — avoid in conditions with side effects |
| Match statement | Use for tagged unions / closed sets — preferred over long `if/elif` |

Enforce with ruff:

```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM", "TCH"]
```

---

## 8. Definition of Done — Core Checklist

Before considering a Python file "done", verify:

- [ ] All names follow § 1 (Naming Conventions)
- [ ] No restating-the-code comments; non-obvious why-comments are in place (§ 2)
- [ ] Every public symbol has type annotations (§ 3.1) — no bare `Any` (§ 3.2)
- [ ] Imports follow § 4 (ordering, no wildcards, no unused)
- [ ] Errors use domain exception classes with `raise ... from ...` (§ 5)
- [ ] All `print()` / logger output is English (§ 6.1)
- [ ] f-string for inline, `%` for logger (§ 6.3)
- [ ] No hardcoded user-facing strings (§ 6.4)
- [ ] ruff passes (or whatever the project's linter is)
