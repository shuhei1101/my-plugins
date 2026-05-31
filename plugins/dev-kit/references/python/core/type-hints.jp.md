<!-- This file is a Japanese mirror of type-hints.md. When updating the English original, update this file too. -->
# 型ヒント

Python 3.12+ 必須。PEP 695 で書く。

---

## 基本

- `from __future__ import annotations` を全ファイル冒頭に置く
- 関数 / メソッドの引数と返り値には**必ず型注釈**
- `Any` は最終手段。理由をコメントで残す
- 内部状態（クラス属性 / モジュール変数）にも型注釈

```python
from __future__ import annotations

def add(x: int, y: int) -> int:
    return x + y

count: int = 0
```

---

## PEP 695 — `type` 文と新ジェネリクス

### `type` 文（型エイリアス）

```python
from typing import Callable, Awaitable

# 識別子型エイリアス
type UserId = str
type OrderId = str

# 構造化エイリアス
type ChatMessages = list[dict[str, str]]
type AsyncChatFn = Callable[[ChatMessages], Awaitable[str]]
```

`TypeAlias` や `from typing import TypeAlias` は使わない（PEP 695 に統一）。

### ジェネリック関数 / クラス

```python
def first[T](xs: list[T]) -> T | None:
    return xs[0] if xs else None

@dataclass
class Pair[K, V]:
    key: K
    value: V
```

### 制約付きジェネリクス

```python
from pydantic import BaseModel

def parse[T: BaseModel](raw: str, schema: type[T]) -> T:
    return schema.model_validate_json(raw)

def serialize[T: BaseModel](model: T) -> str:
    return model.model_dump_json()
```

---

## `NewType` vs `type X = ...`

| 用途 | 推奨 |
|---|---|
| 軽量に識別子型を区別したい | `type UserId = str` |
| 型レベルで他の文字列と混同したくない | `UserId = NewType("UserId", str)` |

`NewType` は型チェッカーが厳しく分離してくれる。`type` 文は単なるエイリアスなので
代入互換性は緩い。プロジェクト内で統一すること（混在しない）。

---

## `Self`

クラスのメソッドが自分自身の型を返す場合に使う:

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

スーパークラスのメソッドを上書きするときは `@override` を付ける（タイポを検出できる）:

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

メタデータを型に付与する。Pydantic Field、FastAPI Depends、validator などで使う:

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

## `TYPE_CHECKING`（型のみインポート）

実行時にロードしたくない / 循環インポートを避けたい型は `TYPE_CHECKING` 配下で:

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .heavy_module import HeavyType

def fn(x: HeavyType) -> None: ...
```

ガイドライン:
- 重いモジュール（pandas / numpy / matplotlib 等）の型だけ使う場合
- 循環インポート回避
- ランタイムで使わない型を明確化

---

## Literal と網羅性チェック（`assert_never`）

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

`Status` に新しい値を増やしたら、`assert_never` が型エラーとして検知してくれる。

---

## デコレータ系

推奨デコレータ (`@dataclass` / `@final` / `@cache` / `@cached_property` / `@override` / `@contextmanager` 等) と、横断関心事を扱うハンドラーデコレータ (`@catch_and_log` / `@catch_and_map` / `@with_retry` / `@with_timeout`)、および `@overload` の解説は分離した:

→ `core/decorators.md`

このファイルでは型ヒント本体だけを扱う。

---

## DTO 定義の使い分け

Pydantic / dataclass / TypedDict / Protocol の使い分け表は `architecture/ts-style.md` の中心セクションで管理している。重複防止のためここには置かない。

---

## 関連ファイル

- `core/decorators.md` — 推奨デコレータ + ハンドラーデコレータ + `@overload`
- `architecture/ts-style.md` — DTO 使い分け表 / TypeScript 風スタイル
- `core/language-rules.md` — 例外階層 / import 順
- `core/comments.md` — フィールド説明の書き方
