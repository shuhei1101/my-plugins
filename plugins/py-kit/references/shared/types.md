# shared/types.py — Common type aliases

Centralize type aliases and identifier types shared across multiple features.

---

## Placement policy

- Identifier types used cross-cutting (`UserId`, `OrderId`, etc.) → `shared/types.py`
- Types used only by a specific feature → `features/{feature}/types.py`
- When the same identifier type starts being **used across multiple features**, promote it to `shared`

---

## Identifier type samples

```python
# src/{pkg}/shared/types.py
from __future__ import annotations
from typing import NewType

# ----- 軽量エイリアス -----
type UserId = str
type SessionId = str
type RequestId = str

# ----- 厳格に区別したい型は NewType -----
OrderId = NewType("OrderId", str)
ProductId = NewType("ProductId", str)
```

### `type` vs `NewType`

| | `type X = str` | `X = NewType("X", str)` |
|---|---|---|
| Nature | Just an alias (loose compatibility) | A distinct type |
| Assignment compatibility | Accepts `str` directly | Requires explicit cast |
| Purpose | Identification "for the reader" | When you want "distinction by the type system" |
| Runtime cost | 0 | 0 (the actual representation is unchanged) |

```python
# type 文（軽量）
user_id: UserId = "u-123"   # OK（str がそのまま入る）

# NewType（厳格）
order_id: OrderId = OrderId("o-456")   # 明示キャスト必須
```

**Unify within the project** (do not mix).
For new projects, prefer `type X = str` (lighter and easier to work with).

---

## Common function type aliases

If multiple features use the same function signature, place it in `shared/types.py`:

```python
# src/{pkg}/shared/types.py
from typing import Callable, Awaitable

# 時刻取得（テスト時に固定値を返す Mock に差し替える）
type NowFn = Callable[[], datetime]

# UUID 生成
type GenerateId = Callable[[], str]

# 同期 HTTP fetch
type HttpFetch = Callable[[str], dict]

# 非同期 HTTP fetch
type AsyncHttpFetch = Callable[[str], Awaitable[dict]]
```

These can be swapped out at the composition root:

```python
# プロダクション
import uuid
from datetime import datetime, timezone

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

def gen_uuid() -> str:
    return str(uuid.uuid4())

# テスト
def now_fixed() -> datetime:
    return datetime(2026, 1, 1, tzinfo=timezone.utc)

def gen_test_id() -> str:
    return "test-id"
```

---

## Common DTOs

DTOs shared across multiple features (which should be extremely rare) can also live in `shared/types.py`:

```python
# 共通の Pagination
@dataclass(frozen=True, slots=True, kw_only=True)
class Pagination:
    page: int
    per_page: int

@dataclass(frozen=True, slots=True, kw_only=True)
class Page[T]:
    items: list[T]
    total: int
    page: int
    per_page: int
```

However, **most DTOs should stay inside a single feature**.
Move them only after a pattern emerges where multiple features cannot do without sharing (YAGNI).

---

## What not to do

```python
# ❌ User や Product のような業務 DTO を shared に置く
# → feature 間で密結合になる
# {pkg}/features/users/types.py に置くべき
```

```python
# ❌ shared を「何でも置き場」にする
# shared/types.py が肥大化するなら、本当に横断的か再評価する
```

```python
# ❌ Iterable 等は標準ライブラリの型を直接使えるので type 文不要
type ListOfInt = list[int]   # 不要、list[int] でいい
```

---

## Related files

- `core/type-hints.md` — details on `type` statement / NewType
- `core/naming.md` — naming conventions for type aliases
- `architecture/dependencies.md` — positioning of shared as a placement location
