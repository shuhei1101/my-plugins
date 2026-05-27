<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# 型ヒント

> このファイルは `type-hints.md` の日本語ミラーです。

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

## 推奨デコレータ（Recommended Decorators）

| デコレータ | 用途 |
|---|---|
| `@dataclass(frozen=True, slots=True, kw_only=True)` | 不変 DTO 標準 |
| `@final` | 継承禁止クラス / メソッド |
| `@functools.cache` | 純粋関数のメモ化（引数キー固定） |
| `@functools.cached_property` | クラス属性の lazy 計算 |
| `@typing.override` | メソッドオーバーライド明示 |
| `@contextlib.contextmanager` | with 文用関数定義 |

---

## ハンドラーデコレータパターン

例外キャッチや横断関心事は **関数デコレータで束ねる**（クラスベース AOP は使わない）。

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

代表的なデコレータ:
- `@catch_and_log(*exc_types, level=...)` — 指定例外を握りつぶしてログ
- `@catch_and_map(SrcError, to=DstError)` — 例外型を変換
- `@with_retry(times=3, backoff=0.5)` — リトライ
- `@with_timeout(seconds=60)` — タイムアウト
- `@measure_time(metric="...")` — 実行時間メトリクス

---

## `@overload`（限定使用）

戻り値が引数型で分岐する関数のみ:

```python
from typing import overload, Literal

@overload
def parse(value: Literal["int"]) -> int: ...
@overload
def parse(value: Literal["str"]) -> str: ...
def parse(value: str) -> int | str:
    return 0 if value == "int" else ""
```

ほとんどのケースでは型エイリアス + Callable / Protocol で済むので、`@overload` の出番は少ない。

---

## DTO 定義の使い分け早見表

| 用途 | 推奨 | 理由 |
|---|---|---|
| 外部 HTTP リクエスト/レスポンス | `pydantic.BaseModel` | ランタイム検証 |
| 設定（.env / YAML / TOML） | `pydantic_settings.BaseSettings` | 検証 + env 読み込み |
| LLM 構造化出力（Instructor） | `pydantic.BaseModel` | Instructor 要求 |
| CLI 引数のパース後の構造体 | `pydantic.BaseModel` | 検証あり |
| 関数間の内部 DTO（軽量） | `@dataclass(frozen=True, slots=True, kw_only=True)` | 軽量・型安全 |
| 関数の引数オブジェクト | `@dataclass` | 軽量、`__init__` 自動 |
| 一時的な dict 型付け（JSON 由来） | `TypedDict` | dict のまま扱える |
| 構造的型付け（duck typing） | `Protocol` | 継承不要 |
| ライブラリが要求する継承先 | そのライブラリの基底 | やむなし |

詳しくは `architecture/ts-style.md` 参照。

---

## 関連ファイル

- `architecture/ts-style.md` — TypeScript 風 Python の中心ドキュメント
- `core/language-rules.md` — 例外階層
- `core/comments.md` — フィールド説明の書き方
