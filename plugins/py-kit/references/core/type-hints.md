# Type Hints

Python 3.12+ required. Write with PEP 695.

---

## Basics

- Put `from __future__ import annotations` at the top of every file
- **Type-annotate every** function / method argument and return value
- `Any` is a last resort. Leave a comment explaining why
- Type-annotate internal state too (class attributes / module variables)

```python
from __future__ import annotations

def add(x: int, y: int) -> int:
    return x + y

count: int = 0
```

---

## PEP 695 — `type` Statement and New Generics

### `type` statement (type alias)

```python
from typing import Callable, Awaitable

# 識別子型エイリアス
type UserId = str
type OrderId = str

# 構造化エイリアス
type ChatMessages = list[dict[str, str]]
type AsyncChatFn = Callable[[ChatMessages], Awaitable[str]]
```

Do not use `TypeAlias` or `from typing import TypeAlias` (unify on PEP 695).

### Generic functions / classes

```python
def first[T](xs: list[T]) -> T | None:
    return xs[0] if xs else None

@dataclass
class Pair[K, V]:
    key: K
    value: V
```

### Bounded generics

```python
from pydantic import BaseModel

def parse[T: BaseModel](raw: str, schema: type[T]) -> T:
    return schema.model_validate_json(raw)

def serialize[T: BaseModel](model: T) -> str:
    return model.model_dump_json()
```

---

## `NewType` vs `type X = ...`

| Use | Recommended |
|---|---|
| Lightly distinguish identifier types | `type UserId = str` |
| Want the type checker to strictly forbid mixing with other strings | `UserId = NewType("UserId", str)` |

`NewType` makes the type checker strictly separate them. A `type` statement is just an alias, so assignment compatibility is loose. Unify within a project (do not mix).

---

## `Self`

Use when a class method returns its own type:

```python
from typing import Self

@dataclass(frozen=True, slots=True, kw_only=True)
class Money:
    amount: int
    currency: str

    def with_amount(self, amount: int) -> Self:
        return type(self)(amount=amount, currency=self.currency)
```

---

## `@typing.override`

Mark methods that override a superclass with `@override` (catches typos):

```python
from typing import override

class Base:
    def name(self) -> str:
        return "base"

class Child(Base):
    @override
    def name(self) -> str:
        return "child"
```

---

## `Annotated`

Attach metadata to a type. Used with Pydantic Field, FastAPI Depends, validators, etc.:

```python
from typing import Annotated
from pydantic import BaseModel, Field

class CreateUserInput(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=20)]
    age: Annotated[int, Field(ge=0, le=150)]
```

FastAPI:

```python
from fastapi import Depends, Query

async def list_users(
    page: Annotated[int, Query(ge=1)] = 1,
    user: Annotated[User, Depends(get_current_user)],
) -> list[User]: ...
```

---

## `TYPE_CHECKING` (import for types only)

For types you do not want loaded at runtime / to avoid circular imports, put them under `TYPE_CHECKING`:

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .heavy_module import HeavyType

def fn(x: HeavyType) -> None: ...
```

Guidelines:
- When only types from heavy modules (pandas / numpy / matplotlib, etc.) are used
- To avoid circular imports
- To clarify types that are not used at runtime

---

## Literal and Exhaustiveness Check (`assert_never`)

```python
from typing import Literal, assert_never

type Status = Literal["draft", "published", "archived"]

def label(status: Status) -> str:
    match status:
        case "draft":
            return "下書き"
        case "published":
            return "公開中"
        case "archived":
            return "アーカイブ"
        case _:
            assert_never(status)
```

When a new value is added to `Status`, `assert_never` will detect it as a type error.

---

## Recommended Decorators

| Decorator | Use |
|---|---|
| `@dataclass(frozen=True, slots=True, kw_only=True)` | Immutable DTO standard |
| `@final` | Forbid inheritance for class / method |
| `@functools.cache` | Memoize pure functions (key by arguments) |
| `@functools.cached_property` | Lazy computation of class attribute |
| `@typing.override` | Explicit method override |
| `@contextlib.contextmanager` | Define a function for use with `with` |

---

## Handler Decorator Pattern

Bundle exception catching and other cross-cutting concerns **into function decorators** (no class-based AOP).

```python
from typing import Callable, Awaitable
from functools import wraps
import logging

def catch_and_log(*exc_types: type[Exception], level: str = "warning"):
    """指定例外をログだけ出してデフォルト値を返すデコレータ。"""
    def decorator[**P, R](fn: Callable[P, R]) -> Callable[P, R | None]:
        @wraps(fn)
        def wrapped(*args: P.args, **kwargs: P.kwargs) -> R | None:
            try:
                return fn(*args, **kwargs)
            except exc_types as e:
                logging.getLogger(fn.__module__).log(
                    getattr(logging, level.upper()),
                    f"{fn.__name__} failed: {e}",
                )
                return None
        return wrapped
    return decorator


@catch_and_log(ValueError, level="warning")
def parse_input(raw: str) -> Input:
    return Input.model_validate_json(raw)
```

Representative decorators:
- `@catch_and_log(*exc_types, level=...)` — swallow the given exceptions and log
- `@catch_and_map(SrcError, to=DstError)` — convert exception type
- `@with_retry(times=3, backoff=0.5)` — retry
- `@with_timeout(seconds=60)` — timeout
- `@measure_time(metric="...")` — execution time metric

---

## `@overload` (Limited Use)

Only for functions whose return type branches on argument type:

```python
from typing import overload, Literal

@overload
def parse(value: Literal["int"]) -> int: ...
@overload
def parse(value: Literal["str"]) -> str: ...
def parse(value: str) -> int | str:
    return 0 if value == "int" else ""
```

In most cases a type alias + Callable / Protocol is enough, so `@overload` rarely appears.

---

## DTO Definition Cheat Sheet

| Use | Recommended | Reason |
|---|---|---|
| External HTTP request/response | `pydantic.BaseModel` | Runtime validation |
| Configuration (.env / YAML / TOML) | `pydantic_settings.BaseSettings` | Validation + env loading |
| LLM structured output (Instructor) | `pydantic.BaseModel` | Instructor requires it |
| Parsed struct after CLI argument parsing | `pydantic.BaseModel` | Validation included |
| Internal DTO between functions (lightweight) | `@dataclass(frozen=True, slots=True, kw_only=True)` | Lightweight, type-safe |
| Argument object for a function | `@dataclass` | Lightweight, automatic `__init__` |
| Typing a temporary dict (from JSON) | `TypedDict` | Stays as a dict |
| Structural typing (duck typing) | `Protocol` | No inheritance needed |
| Inherit from a library-required base | That library's base | Unavoidable |

See `architecture/ts-style.md` for details.

---

## Related Files

- `architecture/ts-style.md` — main document on TypeScript-style Python
- `core/language-rules.md` — exception hierarchy
- `core/comments.md` — how to write field descriptions
