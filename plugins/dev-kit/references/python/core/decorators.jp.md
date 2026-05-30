<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# 推奨デコレータ + ハンドラーデコレータ

> このファイルは `decorators.md` の日本語ミラーです。

py-kit で使用を推奨するデコレータ群と、横断関心事を吸収する **ハンドラーデコレータ** パターン。

---

## Recommended Decorators

| デコレータ | 用途 |
|---|---|
| `@dataclass(frozen=True, slots=True, kw_only=True)` | 不変 DTO 標準 |
| `@final` | 継承禁止クラス / メソッド |
| `@functools.cache` | 純粋関数のメモ化（引数キー固定） |
| `@functools.cached_property` | クラス属性の lazy 計算 |
| `@typing.override` | メソッドオーバーライド明示 |
| `@contextlib.contextmanager` | with 文用関数定義 |
| `@contextlib.asynccontextmanager` | async with 用 |

サンプル:

```python
from dataclasses import dataclass
from functools import cache, cached_property
from typing import final, override
from contextlib import contextmanager


@dataclass(frozen=True, slots=True, kw_only=True)
class User:
    id: str
    name: str


@cache
def expensive_compute(x: int) -> int:
    return x * x


@final
class Singleton:
    @cached_property
    def heavy(self) -> Heavy:
        return Heavy()


class Child(Parent):
    @override
    def name(self) -> str:
        return "child"


@contextmanager
def temp_chdir(path: Path) -> Iterator[None]:
    prev = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev)
```

---

## ハンドラーデコレータ（横断関心事）

例外キャッチ / リトライ / タイムアウト / メトリクス等の **横断関心事は関数デコレータで束ねる**。
クラスベース AOP（aspect-oriented programming）は使わない。

### 代表的なデコレータ

| デコレータ | 用途 |
|---|---|
| `@catch_and_log(*exc_types, level=...)` | 指定例外を握りつぶしてログ、`None` を返す |
| `@catch_and_map(SrcError, to=DstError)` | 例外型を変換（vendor 例外 → ドメイン例外） |
| `@with_retry(times=3, backoff=0.5)` | 指数バックオフでリトライ |
| `@with_timeout(seconds=60)` | 全体タイムアウト |
| `@measure_time(metric="...")` | 実行時間メトリクス |

これらは `{pkg}/shared/decorators.py` にまとめて定義し、必要な箇所から import する。

### `@catch_and_log` 実装例

```python
# {pkg}/shared/decorators.py
from __future__ import annotations
import logging
from functools import wraps
from typing import Callable


def catch_and_log(*exc_types: type[Exception], level: str = "warning"):
    """指定例外をログだけ出して None を返すデコレータ。"""
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

### `@catch_and_map` 実装例

vendor 例外（OpenAI / Anthropic / httpx）をドメイン例外にラップする時に使う:

```python
def catch_and_map(src: type[Exception], *, to: type[Exception]):
    """例外型を変換する。raise from で原因連鎖。"""
    def decorator[**P, R](fn: Callable[P, R]) -> Callable[P, R]:
        @wraps(fn)
        def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                return fn(*args, **kwargs)
            except src as e:
                raise to(str(e)) from e
        return wrapped
    return decorator


@catch_and_map(anthropic.APIStatusError, to=LlmServerError)
async def call_claude(messages: list[Message]) -> str: ...
```

### `@with_retry` 実装例

詳細は `llm/exceptions-retry.md`。同じ実装を `shared/decorators.py` に置けば LLM 以外でも使える。

### `@with_timeout` 実装例

`asyncio.timeout` のラッパー。詳細は `concurrency/async.md`。

```python
def with_timeout[**P, R](*, seconds: float):
    def decorator(fn: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(fn)
        async def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                async with asyncio.timeout(seconds):
                    return await fn(*args, **kwargs)
            except TimeoutError as e:
                raise IntegrationTimeoutError(f"{fn.__name__} timed out") from e
        return wrapped
    return decorator
```

### 合成して使う

外側から順に適用される。読み方は「下から上」:

```python
@with_timeout(seconds=60)               # 3. 全体 60 秒で打ち切り
@with_retry(retries=3, on=(LlmRateLimitError, LlmServerError))   # 2. 3 回までリトライ
@catch_and_map(openai.APIStatusError, to=LlmServerError)         # 1. vendor 例外を変換
async def chat(req: ChatRequest) -> ChatResponse:
    response = await client.chat.completions.create(model=..., messages=req)
    return response.choices[0].message.content or ""
```

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

## 自作デコレータの注意

1. **必ず `@functools.wraps(fn)`** を付ける（メタデータ保持）
2. **型ヒント** は PEP 695 の `[**P, R]` パラメータ仕様を使う
3. **async / sync を分ける** 場合は別関数で
4. **副作用は最小限**: ログだけ・例外変換だけ等 1 責務に絞る

---

## 関連ファイル

- `core/type-hints.md` — 型ヒント基本
- `shared/errors.md` — 例外階層
- `llm/exceptions-retry.md` — `@with_retry` の本格実装
- `concurrency/async.md` — `asyncio.timeout`
