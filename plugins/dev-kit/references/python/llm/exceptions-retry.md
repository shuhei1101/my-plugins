# llm/exceptions-retry — LLM exception hierarchy and retry strategy

Classify LLM-originated exceptions under `LlmError` so retry eligibility can be **determined by type**.

---

## Exception hierarchy (recap)

```python
# {pkg}/shared/errors.py
class IntegrationError(AppError):
    """外部サービス連携の包括エラー。"""

class IntegrationTimeoutError(IntegrationError):
    """外部サービスがタイムアウト。"""

class LlmError(IntegrationError):
    """LLM API 由来の包括エラー。"""

class LlmRateLimitError(LlmError):
    """レート制限超過。指数バックオフで待って再試行可。"""

class LlmServerError(LlmError):
    """LLM サーバ側 5xx。短い待ちで再試行可。"""

class LlmBadRequestError(LlmError):
    """LLM リクエストが不正（4xx）。リトライ不可。"""

class LlmAuthError(LlmError):
    """認証エラー（401/403）。リトライ不可。"""

class LlmContentFilterError(LlmError):
    """コンテンツフィルタによる拒否。リトライ不可。"""
```

---

## What to retry / what not to retry

| Exception | Retry |
|---|---|
| `LlmRateLimitError` | ✅ Exponential backoff |
| `LlmServerError` | ✅ Short wait |
| `IntegrationTimeoutError` | ✅ With jitter |
| `LlmBadRequestError` | ❌ Will fail forever unless the prompt is fixed |
| `LlmAuthError` | ❌ API key needs to be corrected |
| `LlmContentFilterError` | ❌ Same input → same result |

---

## Retry implementation (handler decorator)

```python
# {pkg}/shared/decorators.py
from __future__ import annotations
import asyncio
import random
from functools import wraps
from typing import Awaitable, Callable


def with_retry[**P, R](
    *,
    retries: int = 3,
    on: tuple[type[Exception], ...],
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    jitter: float = 0.2,
):
    """指定例外で指数バックオフ + ジッタによるリトライ。"""
    def decorator(fn: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(fn)
        async def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
            last_exc: Exception | None = None
            for attempt in range(retries + 1):
                try:
                    return await fn(*args, **kwargs)
                except on as e:
                    last_exc = e
                    if attempt == retries:
                        break
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    delay *= 1.0 + random.uniform(-jitter, jitter)
                    await asyncio.sleep(delay)
            assert last_exc is not None
            raise last_exc
        return wrapped
    return decorator
```

Usage:

```python
from {pkg}.shared.errors import LlmRateLimitError, LlmServerError, IntegrationTimeoutError

@with_retry(
    retries=3,
    on=(LlmRateLimitError, LlmServerError, IntegrationTimeoutError),
    base_delay=2.0,
)
async def chat(req: ChatRequest) -> ChatResponse:
    ...
```

---

## Using the `Retry-After` header

OpenAI / Anthropic rate-limit errors return a `Retry-After` header telling you "try again in N seconds".

```python
from {pkg}.shared.errors import LlmRateLimitError


class LlmRateLimitError(LlmError):
    def __init__(self, msg: str, retry_after: float | None = None) -> None:
        super().__init__(msg)
        self.retry_after = retry_after
```

Extract it on the client side:

```python
except openai.RateLimitError as e:
    retry_after = float(e.response.headers.get("retry-after", 0)) if e.response else None
    raise LlmRateLimitError(f"openai rate limit: {e}", retry_after=retry_after) from e
```

Honor `retry_after` in the decorator:

```python
except on as e:
    if isinstance(e, LlmRateLimitError) and e.retry_after:
        delay = e.retry_after
    else:
        delay = min(base_delay * (2 ** attempt), max_delay)
    delay *= 1.0 + random.uniform(-jitter, jitter)
    await asyncio.sleep(delay)
```

---

## Timeout

Two layers: client-level and decorator-level:

```python
client = AsyncOpenAI(api_key=..., timeout=30.0)   # クライアント側

@with_timeout(seconds=60)   # 全体のラッパー（より外側でカット）
async def chat(req): ...
```

`with_timeout` implementation:

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

---

## Circuit breaker

Halt for a period when consecutive failures persist:

```python
class CircuitBreaker:
    def __init__(self, *, threshold: int = 5, cooldown: float = 60.0) -> None:
        self.failures = 0
        self.opened_at: float | None = None
        self.threshold = threshold
        self.cooldown = cooldown

    def is_open(self) -> bool:
        if self.opened_at is None:
            return False
        if time.monotonic() - self.opened_at >= self.cooldown:
            self.opened_at = None
            self.failures = 0
            return False
        return True

    def record_success(self) -> None:
        self.failures = 0
        self.opened_at = None

    def record_failure(self) -> None:
        self.failures += 1
        if self.failures >= self.threshold:
            self.opened_at = time.monotonic()
```

That said, **not needed** if simple retries are enough. Adopt only after you've actually seen repeated production failures.

---

## Example of composing handler decorators

```python
@with_timeout(seconds=60)
@with_retry(retries=3, on=(LlmRateLimitError, LlmServerError, IntegrationTimeoutError))
@catch_and_map(openai.RateLimitError, to=LlmRateLimitError)
@catch_and_map(openai.APIStatusError, to=LlmServerError)
async def chat(req: ChatRequest) -> ChatResponse:
    response = await client.chat.completions.create(model=..., messages=req)
    return response.choices[0].message.content or ""
```

The decorators apply from outside in:
1. Map vendor exceptions to `Llm*`
2. Retry up to 3 times
3. Cut off the whole thing at 60 seconds

---

## Logging

WARNING on retry:

```python
logger.warning(
    "retrying llm call",
    extra={
        "attempt": attempt,
        "max": retries,
        "exception": str(e),
        "delay_sec": delay,
    },
)
```

ERROR on final failure:

```python
logger.error(
    "llm call failed permanently",
    extra={"attempts": retries, "exception": str(last_exc)},
)
```

---

## Related files

- `shared/errors.md` — Overall exception hierarchy
- `core/type-hints.md` — Implementation patterns for handler decorators
- `llm/providers.md` — Wrapping vendor exceptions
- `concurrency/async.md` — asyncio.timeout
