# Type hints

Python 3.12+ required. Write in PEP 695.

---

## Basics

- Place `from __future__ import annotations` at the top of every file
- Function / method arguments and return values **must always have type annotations**
- `Any` is a last resort. Leave a reason as a comment
- Internal state (class attributes / module variables) also gets type annotations

```python
from __future__ import annotations

def add(x: int, y: int) -> int:
    return x + y

count: int = 0
```

---

## PEP 695 — `type` statement and new generics

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

Do not use `TypeAlias` or `from typing import TypeAlias` (unify with PEP 695).

### Generic functions / classes

```python
def first[T](xs: list[T]) -> T | None:
    return xs[0] if xs else None

@dataclass
class Pair[K, V]:
    key: K
    value: V
```

### Constrained generics

```python
from pydantic import BaseModel

def parse[T: BaseModel](raw: str, schema: type[T]) -> T:
    return schema.model_validate_json(raw)

def serialize[T: BaseModel](model: T) -> str:
    return model.model_dump_json()
```

---

## `NewType` vs `type X = ...`

| Use case | Recommended |
|---|---|
| Lightweight distinction of identifier types | `type UserId = str` |
| Want the type checker to strictly prevent confusion with other strings | `UserId = NewType("UserId", str)` |

`NewType` is strictly separated by the type checker. The `type` statement is a mere alias,
so assignment compatibility is loose. Unify across the project (do not mix).

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

When overriding a superclass method, attach `@override` (catches typos):

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

## `TYPE_CHECKING` (type-only import)

Types you don't want loaded at runtime / want to avoid circular imports — put them under `TYPE_CHECKING`:

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .heavy_module import HeavyType

def fn(x: HeavyType) -> None: ...
```

Guidelines:
- When using only the types from heavy modules (pandas / numpy / matplotlib, etc.)
- Avoid circular imports
- Clarify types not used at runtime

---

## Literal and exhaustiveness checking (`assert_never`)

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

When you add a new value to `Status`, `assert_never` will catch it as a type error.

---

## Decorators

Recommended decorators (`@dataclass` / `@final` / `@cache` / `@cached_property` / `@override` / `@contextmanager`, etc.), handler decorators for cross-cutting concerns (`@catch_and_log` / `@catch_and_map` / `@with_retry` / `@with_timeout`), and `@overload` are covered separately:

→ `core/decorators.md`

This file covers only the type hint body.

---

## DTO definition: which to use

The Pydantic / dataclass / TypedDict / Protocol decision table is managed as the central section of `architecture/ts-style.md`. Not duplicated here to prevent duplication.

---

## Related files

- `core/decorators.md` — recommended decorators + handler decorators + `@overload`
- `architecture/ts-style.md` — DTO usage table / TypeScript-style style
- `core/language-rules.md` — exception hierarchy / import order
- `core/comments.md` — how to write field descriptions
