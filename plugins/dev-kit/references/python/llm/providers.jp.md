<!-- This file is a Japanese mirror of providers.md. When updating the English original, update this file too. -->
# llm/providers — LLM プロバイダ実装

LLM API（Claude / OpenAI / Gemini 等）を **関数で抽象化** して、注入できる形にする。

---

## 関数の型エイリアス

```python
# src/{pkg}/integrations/llm/types.py
from __future__ import annotations
from typing import Awaitable, Callable, TypedDict

# ----- メッセージ型 -----
class Message(TypedDict):
    role: str        # "user" / "assistant" / "system"
    content: str

type ChatRequest = list[Message]
type ChatResponse = str

# ----- 関数の型 -----
type AsyncChatFn = Callable[[ChatRequest], Awaitable[ChatResponse]]
type SyncChatFn = Callable[[ChatRequest], ChatResponse]
```

複数 feature で `AsyncChatFn` を引数に取れば、プロバイダの差し替えが透過的。

---

## OpenAI 実装

```python
# src/{pkg}/integrations/llm/openai_client.py
from __future__ import annotations
from openai import AsyncOpenAI
import openai

from {pkg}.shared.errors import (
    LlmError, LlmRateLimitError, LlmServerError,
    LlmBadRequestError, IntegrationTimeoutError,
)
from {pkg}.shared.logger import get_logger
from .types import ChatRequest, ChatResponse

logger = get_logger(__name__)

def make_openai_chat(
    *,
    api_key: str,
    model: str = "gpt-4o-mini",
    timeout: float = 30.0,
    max_tokens: int = 1024,
) -> AsyncChatFn:
    """OpenAI クライアントを作って AsyncChatFn を返す。"""
    client = AsyncOpenAI(api_key=api_key, timeout=timeout)

    async def chat(req: ChatRequest) -> ChatResponse:
        try:
            response = await client.chat.completions.create(
                model=model,
                messages=req,
                max_tokens=max_tokens,
            )
        except openai.RateLimitError as e:
            raise LlmRateLimitError(f"openai rate limit: {e}") from e
        except openai.APIStatusError as e:
            if 500 <= e.status_code < 600:
                raise LlmServerError(f"openai 5xx: {e}") from e
            if e.status_code == 400:
                raise LlmBadRequestError(f"openai bad request: {e}") from e
            raise LlmError(f"openai api error: {e}") from e
        except openai.APITimeoutError as e:
            raise IntegrationTimeoutError(f"openai timeout: {e}") from e

        # トークン使用量をログ
        usage = response.usage
        logger.info(
            "llm_call",
            extra={
                "provider": "openai",
                "model": model,
                "input_tokens": usage.prompt_tokens if usage else None,
                "output_tokens": usage.completion_tokens if usage else None,
            },
        )

        return response.choices[0].message.content or ""

    return chat
```

`make_openai_chat(...)` で配線済み `AsyncChatFn` が返る。

---

## Anthropic (Claude) 実装

```python
# src/{pkg}/integrations/llm/anthropic_client.py
from __future__ import annotations
import anthropic
from anthropic import AsyncAnthropic

from {pkg}.shared.errors import (
    LlmError, LlmRateLimitError, LlmServerError, IntegrationTimeoutError,
)
from {pkg}.shared.logger import get_logger
from .types import ChatRequest, ChatResponse

logger = get_logger(__name__)

def make_anthropic_chat(
    *,
    api_key: str,
    model: str = "claude-haiku-4-5-20251001",
    max_tokens: int = 1024,
    timeout: float = 30.0,
) -> AsyncChatFn:
    """Anthropic クライアントを作って AsyncChatFn を返す。"""
    client = AsyncAnthropic(api_key=api_key, timeout=timeout)

    async def chat(req: ChatRequest) -> ChatResponse:
        # Anthropic は system を別パラメータに分離する
        system = "\n".join(m["content"] for m in req if m["role"] == "system")
        messages = [m for m in req if m["role"] != "system"]

        try:
            response = await client.messages.create(
                model=model,
                system=system or None,
                messages=messages,
                max_tokens=max_tokens,
            )
        except anthropic.RateLimitError as e:
            raise LlmRateLimitError(f"anthropic rate limit: {e}") from e
        except anthropic.APIStatusError as e:
            if 500 <= e.status_code < 600:
                raise LlmServerError(f"anthropic 5xx: {e}") from e
            raise LlmError(f"anthropic api error: {e}") from e
        except anthropic.APITimeoutError as e:
            raise IntegrationTimeoutError(f"anthropic timeout: {e}") from e

        usage = response.usage
        logger.info(
            "llm_call",
            extra={
                "provider": "anthropic",
                "model": model,
                "input_tokens": usage.input_tokens,
                "output_tokens": usage.output_tokens,
                "cache_read_tokens": getattr(usage, "cache_read_input_tokens", 0),
            },
        )

        return "".join(b.text for b in response.content if b.type == "text")

    return chat
```

---

## Mock 実装

```python
# src/{pkg}/integrations/llm/mock_client.py
from __future__ import annotations
from .types import ChatRequest, ChatResponse, AsyncChatFn

def make_mock_chat(*responses: str) -> AsyncChatFn:
    """テスト用 Mock。順番に固定文字列を返す。"""
    queue = list(responses) or ["[mocked response]"]
    index = 0

    async def chat(req: ChatRequest) -> ChatResponse:
        nonlocal index
        result = queue[min(index, len(queue) - 1)]
        index += 1
        return result

    return chat
```

---

## composition root での組み立て

```python
# src/{pkg}/main.py
from functools import partial
from {pkg}.shared.settings import Settings
from {pkg}.integrations.llm.openai_client import make_openai_chat
from {pkg}.integrations.llm.anthropic_client import make_anthropic_chat
from {pkg}.features.chat.service import generate_response

def build_handlers(settings: Settings) -> Handlers:
    # 主要プロバイダを 1 つ選ぶ
    chat = make_openai_chat(
        api_key=settings.openai_api_key.get_secret_value(),
        model=settings.openai_model,
    )

    return Handlers(
        generate_response=partial(generate_response, chat=chat),
    )
```

プロバイダ切替は **設定 1 行で**:

```python
# 別実装に切り替え
chat = make_anthropic_chat(
    api_key=settings.anthropic_api_key.get_secret_value(),
    model=settings.anthropic_model,
)
```

`generate_response` のシグネチャは変わらない。

---

## 複数プロバイダを fallback

```python
async def chat_with_fallback(req: ChatRequest) -> ChatResponse:
    """1 段目失敗時に 2 段目へ。"""
    try:
        return await primary(req)
    except (LlmServerError, IntegrationTimeoutError):
        logger.warning("primary failed, falling back to secondary")
        return await secondary(req)
```

---

## ストリーミング

応答を 1 トークンずつ受け取る場合:

```python
# src/{pkg}/integrations/llm/types.py
from typing import AsyncIterator

type AsyncChatStreamFn = Callable[[ChatRequest], AsyncIterator[str]]

# 実装
def make_openai_chat_stream(*, api_key: str, model: str) -> AsyncChatStreamFn:
    client = AsyncOpenAI(api_key=api_key)

    async def chat_stream(req: ChatRequest):
        async with client.chat.completions.stream(model=model, messages=req) as stream:
            async for event in stream:
                if event.type == "content.delta":
                    yield event.delta

    return chat_stream
```

詳細は `concurrency/async.md` の async generator。

---

## 関連ファイル

- `llm/instructor.md` — Pydantic で構造化出力
- `llm/exceptions-retry.md` — 例外 + リトライ
- `llm/cost-cache.md` — トークン管理
- `llm/prompts.md` — プロンプトファイル管理
- `architecture/ts-style.md` — 関数の型エイリアスの設計思想
