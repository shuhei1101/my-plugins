<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# llm/exceptions-retry — LLM 例外階層とリトライ戦略

> このファイルは `exceptions-retry.md` の日本語ミラーです。

LLM 由来の例外は `LlmError` をベースに分類し、リトライ可否を **型で判断** できるようにする。

---

## 例外階層（再掲）

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

## リトライすべきもの / すべきでないもの

| 例外 | リトライ |
|---|---|
| `LlmRateLimitError` | ✅ 指数バックオフ |
| `LlmServerError` | ✅ 短い待ちで |
| `IntegrationTimeoutError` | ✅ ジッタ付き |
| `LlmBadRequestError` | ❌ プロンプトを直さないと永遠に失敗 |
| `LlmAuthError` | ❌ API キー要修正 |
| `LlmContentFilterError` | ❌ 同じ入力なら同じ結果 |

---

## リトライ実装（ハンドラーデコレータ）

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

使い方:

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

## `Retry-After` ヘッダの活用

OpenAI / Anthropic の rate-limit エラーは `Retry-After` ヘッダで「何秒後に試して」を返す。

```python
from {pkg}.shared.errors import LlmRateLimitError


class LlmRateLimitError(LlmError):
    def __init__(self, msg: str, retry_after: float | None = None) -> None:
        super().__init__(msg)
        self.retry_after = retry_after
```

クライアント実装側で抽出:

```python
except openai.RateLimitError as e:
    retry_after = float(e.response.headers.get("retry-after", 0)) if e.response else None
    raise LlmRateLimitError(f"openai rate limit: {e}", retry_after=retry_after) from e
```

デコレータでは `retry_after` を尊重する:

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

## タイムアウト

クライアントレベル + デコレータレベルの 2 段:

```python
client = AsyncOpenAI(api_key=..., timeout=30.0)   # クライアント側

@with_timeout(seconds=60)   # 全体のラッパー（より外側でカット）
async def chat(req): ...
```

`with_timeout` 実装:

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

## サーキットブレーカー

連続失敗が続いたら一定時間停止する:

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

ただし、シンプルなリトライで足りるなら **不要**。本番で繰り返し落ちる事故があってから導入。

---

## ハンドラーデコレータの合成例

```python
@with_timeout(seconds=60)
@with_retry(retries=3, on=(LlmRateLimitError, LlmServerError, IntegrationTimeoutError))
@catch_and_map(openai.RateLimitError, to=LlmRateLimitError)
@catch_and_map(openai.APIStatusError, to=LlmServerError)
async def chat(req: ChatRequest) -> ChatResponse:
    response = await client.chat.completions.create(model=..., messages=req)
    return response.choices[0].message.content or ""
```

デコレータが外側から順に適用される:
1. vendor 例外を `Llm*` にマップ
2. 3 回までリトライ
3. 全体 60 秒で打ち切り

---

## ロギング

リトライ時には WARNING で:

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

最終失敗時は ERROR:

```python
logger.error(
    "llm call failed permanently",
    extra={"attempts": retries, "exception": str(last_exc)},
)
```

---

## 関連ファイル

- `shared/errors.md` — 全体の例外階層
- `core/type-hints.md` — ハンドラーデコレータの実装パターン
- `llm/providers.md` — vendor 例外のラップ
- `concurrency/async.md` — asyncio.timeout
