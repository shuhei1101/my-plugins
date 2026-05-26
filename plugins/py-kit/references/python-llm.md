# Python LLM Client Standards — py-kit

Architecture conventions for projects that call LLM APIs (Claude, OpenAI, Gemini,
local OSS models, etc.). Read together with `python-core.md` and
`python-architecture.md`.

LLMs are external services and follow the same DDD layering rule: a Protocol
in `domain/`, a concrete implementation in `infrastructure/`, wired in the
composition root.

---

## 1. Architecture Overview

```
domain/
├── repositories/
│   └── llm_client.py            # LlmClient Protocol (the "what")
└── services/
    └── llms/                    # task-specific LLM Protocols (the "why")
        ├── response_generation_llm.py
        ├── classification_llm.py
        └── summarization_llm.py

infrastructure/
└── llm/
    ├── providers/               # vendor adapters (the "how")
    │   ├── base.py              # LlmProvider Protocol common to all vendors
    │   ├── claude_provider.py
    │   ├── openai_provider.py
    │   └── gemini_provider.py
    ├── instructor_clients/      # structured-output wrappers (Pydantic-bound)
    │   ├── response_generation_claude_client.py
    │   └── classification_openai_client.py
    ├── prompts/                 # prompt templates (.md files loaded at startup)
    │   ├── response_generation.md
    │   └── classification.md
    └── exceptions.py            # LLM-specific exception classes
```

### 1.1 Three-Layer Abstraction

| Layer | Purpose | Example |
|---|---|---|
| Task-specific LLM (`domain/services/llms/`) | The domain's view: "I need to classify a comment" | `ClassificationLlm.classify(comment: str) -> CommentCategory` |
| Vendor provider (`infrastructure/llm/providers/`) | Common adapter to a vendor's chat API | `ClaudeProvider.invoke(request: LlmRequest) -> str` |
| Wire SDK | The vendor's Python SDK | `anthropic.Anthropic`, `openai.OpenAI` |

Why three layers: the domain talks in business verbs (`classify`, `summarize`,
`generate_response`), not in "send this message to Claude". The provider layer
isolates vendor differences (auth, request shape, error types) behind a common
`LlmProvider` interface. Switching from Claude to OpenAI for one task only
requires changing the wiring in `main.py`.

---

## 2. The `LlmClient` Protocol

The minimal Protocol common to all LLM calls — used when the domain just needs
"a model that returns text":

```python
# domain/repositories/llm_client.py
from typing import Protocol

class LlmClient(Protocol):
    async def complete(
        self,
        prompt: str,
        *,
        max_tokens: int,
        temperature: float = 0.0,
    ) -> str: ...

    async def complete_structured[T: BaseModel](
        self,
        prompt: str,
        *,
        schema: type[T],
        max_tokens: int,
        temperature: float = 0.0,
    ) -> T: ...
```

For tasks that need only this minimal interface, inject `LlmClient`. For tasks
with their own input/output shape, define a task-specific Protocol (§ 4) and
inject that instead.

---

## 3. Vendor Provider Layer

### 3.1 Common Request Type

A shared request type lets every task-specific client speak the same vocabulary
to every vendor:

```python
# infrastructure/llm/providers/base.py
from typing import Protocol
from pydantic import BaseModel

class LlmMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class LlmRequest(BaseModel):
    model: str
    messages: list[LlmMessage]
    max_tokens: int
    temperature: float = 0.0
    response_format: dict | None = None  # vendor-specific structured output hint


class LlmProvider(Protocol):
    async def invoke(self, request: LlmRequest) -> str: ...
    async def invoke_with_retry(
        self,
        request: LlmRequest,
        *,
        max_retries: int = 3,
    ) -> str: ...
```

### 3.2 Concrete Provider Example — Claude

```python
# infrastructure/llm/providers/claude_provider.py
import anthropic
from anthropic import APIStatusError, RateLimitError

from {pkg}.infrastructure.llm.providers.base import LlmRequest
from {pkg}.infrastructure.llm.exceptions import (
    LlmRateLimitError,
    LlmServerError,
    LlmBadRequestError,
)
from {pkg}.logger import get_logger

logger = get_logger(__name__)


class ClaudeProvider:
    def __init__(self, api_key: str) -> None:
        self._client = anthropic.AsyncAnthropic(api_key=api_key)

    async def invoke(self, request: LlmRequest) -> str:
        try:
            response = await self._client.messages.create(
                model=request.model,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                system=self._extract_system(request),
                messages=self._to_anthropic_messages(request),
            )
            logger.debug(
                "claude usage: input=%d output=%d cache_read=%d cache_creation=%d",
                response.usage.input_tokens,
                response.usage.output_tokens,
                getattr(response.usage, "cache_read_input_tokens", 0),
                getattr(response.usage, "cache_creation_input_tokens", 0),
            )
            return response.content[0].text

        except RateLimitError as e:
            raise LlmRateLimitError(str(e)) from e
        except APIStatusError as e:
            if 400 <= e.status_code < 500:
                raise LlmBadRequestError(str(e)) from e
            raise LlmServerError(str(e)) from e

    async def invoke_with_retry(self, request: LlmRequest, *, max_retries: int = 3) -> str:
        attempt = 0
        delay = 1.0
        while True:
            try:
                return await self.invoke(request)
            except (LlmRateLimitError, LlmServerError) as e:
                attempt += 1
                if attempt > max_retries:
                    raise
                logger.warning("retrying after %s (attempt %d/%d): %s", delay, attempt, max_retries, e)
                await asyncio.sleep(delay)
                delay *= 2  # exponential backoff
```

### 3.3 Provider Rules

| Rule | Reason |
|---|---|
| Wrap every vendor exception in a domain exception (`LlmRateLimitError`, `LlmServerError`, etc.) | Calling code should never `except anthropic.APIStatusError` |
| Always log token usage at DEBUG (`input`, `output`, `cache_read`, `cache_creation`) | Cost analysis, cache effectiveness |
| Always set `max_tokens` explicitly | Vendor defaults are unpredictable and change |
| `temperature=0.0` is the default — opt into higher values consciously | Reproducibility |
| `invoke_with_retry` is opt-in; raw `invoke` exists for use cases that want their own retry policy | Some tasks must not retry (idempotency concerns) |

---

## 4. Task-Specific LLM Clients

A task-specific client defines the Protocol that the domain depends on. It
typically uses **Instructor** (or vendor-native structured output) to bind a
Pydantic schema to the LLM call.

### 4.1 Task Protocol in the Domain

```python
# domain/services/llms/classification_llm.py
from typing import Protocol
from {pkg}.domain.value_objects.comment_category import CommentCategory

class ClassificationLlm(Protocol):
    async def classify(self, comment_text: str) -> CommentCategory: ...
```

### 4.2 Concrete Implementation — Instructor + Claude

```python
# infrastructure/llm/instructor_clients/classification_claude_client.py
import instructor
import anthropic
from pydantic import BaseModel, Field

from {pkg}.domain.value_objects.comment_category import CommentCategory
from {pkg}.infrastructure.llm.prompts import load_prompt
from {pkg}.logger import get_logger

logger = get_logger(__name__)


class _ClassificationResult(BaseModel):
    """Schema enforced by Instructor."""
    category: Literal["spam", "question", "praise", "criticism", "other"]
    confidence: float = Field(..., ge=0.0, le=1.0)


_SYSTEM_PROMPT = load_prompt("classification")  # prompts/classification.md


class ClassificationClaudeClient:
    def __init__(self, api_key: str, model: str) -> None:
        self._client = instructor.from_anthropic(anthropic.AsyncAnthropic(api_key=api_key))
        self._model = model

    async def classify(self, comment_text: str) -> CommentCategory:
        logger.debug("classifying comment: %d chars", len(comment_text))
        result = await self._client.messages.create(
            model=self._model,
            max_tokens=256,
            response_model=_ClassificationResult,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": comment_text},
            ],
        )
        return CommentCategory(value=result.category, confidence=result.confidence)
```

### 4.3 Why Instructor (Recommended)

Instructor (or LangChain's `with_structured_output`) gives:

- A typed Pydantic object instead of a raw string to parse
- Automatic schema-to-vendor-format conversion
- Automatic retries on parse failure
- Same code shape across vendors

Without Instructor you need per-vendor JSON-schema plumbing, regex parsing of
fenced code blocks, and bespoke retry-on-malformed-output logic — all of which
is bug-prone.

### 4.4 Output Schema Rules

| Rule | Reason |
|---|---|
| Output schema is a Pydantic `BaseModel` | Instructor requires it; validation at the boundary |
| Field validation (`Field(..., ge=0, le=1)`) for ranged values | LLMs return out-of-range values silently |
| `Literal[...]` for closed-set categories | LLMs return synonyms ("praise" vs "compliment") |
| One schema per task; do not reuse for unrelated tasks | A unified schema becomes a god-object |
| Domain value object wraps the schema before crossing the boundary | Schema is internal; domain code receives the value object |

---

## 5. Prompt Management

### 5.1 Prompts Live in Files, Not in Code

```
infrastructure/llm/prompts/
├── classification.md
├── response_generation.md
├── summarization.md
└── ...
```

### 5.2 Loader

```python
# infrastructure/llm/prompts/__init__.py
from functools import cache
from pathlib import Path

_PROMPTS_DIR = Path(__file__).parent


@cache
def load_prompt(name: str) -> str:
    """Load a prompt template by name. Cached after first read."""
    path = _PROMPTS_DIR / f"{name}.md"
    return path.read_text(encoding="utf-8")
```

### 5.3 Templating

For prompts with variable substitution, use `string.Template` or Jinja2 — never
f-strings on file contents (no compile-time check that all variables exist).

```python
# infrastructure/llm/prompts/response_generation.md
You are responding to: ${user_name}.
The context is: ${context}.
```

```python
from string import Template

template = Template(load_prompt("response_generation"))
prompt = template.substitute(user_name=user.name, context=ctx)
```

For complex prompts (loops, conditionals), use Jinja2:

```python
from jinja2 import Template
template = Template(load_prompt("complex_prompt"))
prompt = template.render(history=messages, user=user)
```

### 5.4 Prompt Versioning

When you change a prompt that's in production:

1. Add a comment at the top with the PR number and reason
2. Save the previous version inline (commented) for at least one release cycle
3. If the change affects output structure, also bump the Pydantic schema

```markdown
<!-- PR142: tightened the tone instruction. Output is more concise. -->
You are a concise assistant.
...

<!-- PR130 (previous):
You are a helpful assistant.
...
-->
```

### 5.5 System vs User Roles

| Content | Role |
|---|---|
| Persona, task description, output format, examples | `system` |
| Actual input the model should react to | `user` |
| Previous turns in a multi-turn dialog | `user` / `assistant` alternating |

Never put dynamic user data in the `system` role — it can leak into other turns via prompt caching.

---

## 6. Token, Cost, and Cache Management

### 6.1 Always Set `max_tokens`

Vendor defaults differ and can silently cap output. Always set it.

```python
# ✅ Good — explicit
LlmRequest(model="claude-sonnet-4-6", messages=[...], max_tokens=1024)

# ❌ Bad — silent default
client.messages.create(model="claude-sonnet-4-6", messages=[...])
```

Pick `max_tokens` based on the expected output size, with ~30% headroom.

### 6.2 Log Token Usage

Every provider implementation logs token usage at DEBUG so cost analysis is
possible without rerunning calls.

```python
logger.debug(
    "claude usage: input=%d output=%d cache_read=%d cache_creation=%d",
    r.usage.input_tokens, r.usage.output_tokens,
    getattr(r.usage, "cache_read_input_tokens", 0),
    getattr(r.usage, "cache_creation_input_tokens", 0),
)
```

A periodic job aggregates these into a daily cost report.

### 6.3 Prompt Caching

For static system prompts ≥1024 tokens, set `cache_control` to cut input cost:

```python
# Claude — Anthropic-specific
response = await client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": LONG_SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"},
        }
    ],
    messages=[{"role": "user", "content": user_input}],
)
```

The first call writes the cache (paid extra); subsequent calls read it for free.
Cache TTL is ~5 minutes — design retries / batches to land within that window.

### 6.4 Batch API for Bulk Operations

When you have ≥10 independent calls that don't need a response right now, use
the batch API (Anthropic Batch API, OpenAI Batch API). It's ~50% cheaper and
gives 24-hour turnaround.

```python
# Acceptable as a fire-and-forget background job
batch = await client.messages.batches.create(requests=[...])
# poll batch.id, retrieve results later
```

For latency-sensitive paths (chat UI), use streaming, not batching.

### 6.5 Streaming for User-Facing Output

```python
async with client.messages.stream(
    model=request.model,
    max_tokens=request.max_tokens,
    messages=self._to_anthropic_messages(request),
) as stream:
    async for text in stream.text_stream:
        yield text
```

Streaming improves perceived latency on chat-style UIs. Don't use streaming for
structured output (Instructor) — wait for the complete response.

---

## 7. Provider Selection and Multi-Model Setups

Inspired by the AITuber pattern: different tasks may use different vendors and
models.

### 7.1 Per-Task Model Configuration

```python
# config.py
class LlmModelsConfig(BaseModel):
    classification: str = "claude-haiku-4-5-20251001"      # fast, cheap
    response_generation: str = "claude-sonnet-4-6"          # quality
    summarization: str = "claude-sonnet-4-6"
    embedding: str = "voyage-3"                              # different vendor

class Settings(BaseModel):
    anthropic_api_key: SecretStr
    voyage_api_key: SecretStr
    llm_models: LlmModelsConfig = Field(default_factory=LlmModelsConfig)
```

### 7.2 Wiring in the Composition Root

```python
# main.py
claude = ClaudeProvider(settings.anthropic_api_key.get_secret_value())
voyage = VoyageProvider(settings.voyage_api_key.get_secret_value())

classification_llm = ClassificationClaudeClient(
    api_key=settings.anthropic_api_key.get_secret_value(),
    model=settings.llm_models.classification,
)
response_llm = ResponseGenerationClaudeClient(
    api_key=settings.anthropic_api_key.get_secret_value(),
    model=settings.llm_models.response_generation,
)
embedding_llm = EmbeddingClient(provider=voyage)
```

The domain doesn't know which vendor it's using; it depends only on the task-
specific Protocol. Switching the response-generation task to OpenAI is a
config + wiring change, never a domain change.

### 7.3 Fallback Across Providers (Optional)

For high-availability scenarios:

```python
class FallbackProvider:
    """Provider Decorator: tries primary, falls back to secondary on server errors."""

    def __init__(self, primary: LlmProvider, secondary: LlmProvider) -> None:
        self._primary = primary
        self._secondary = secondary

    async def invoke(self, request: LlmRequest) -> str:
        try:
            return await self._primary.invoke(request)
        except LlmServerError as e:
            logger.warning("primary LLM failed, falling back: %s", e)
            return await self._secondary.invoke(request)
```

This is a Decorator (per `python-architecture.md § 6.4`); compose it in the
wiring step.

---

## 8. Error Handling

### 8.1 LLM Exception Hierarchy

```python
# infrastructure/llm/exceptions.py
class LlmError(Exception): ...

class LlmRateLimitError(LlmError): ...       # retryable
class LlmServerError(LlmError): ...           # retryable
class LlmBadRequestError(LlmError): ...       # NOT retryable — fix the prompt
class LlmAuthenticationError(LlmError): ...   # NOT retryable — fix the key
class LlmTimeoutError(LlmError): ...           # retryable
class LlmContentFilterError(LlmError): ...    # NOT retryable — content policy
```

### 8.2 What to Retry / What Not To

| Exception | Retry | Action |
|---|---|---|
| `LlmRateLimitError` | ✅ Yes | Exponential backoff, respect Retry-After header |
| `LlmServerError` (5xx) | ✅ Yes | Exponential backoff, max 3 |
| `LlmTimeoutError` | ✅ Yes | Backoff, max 2 |
| `LlmBadRequestError` (4xx) | ❌ No | Bubble up; the prompt or request is wrong |
| `LlmAuthenticationError` | ❌ No | Bubble up; fix the config |
| `LlmContentFilterError` | ❌ No | Bubble up; the input violated the vendor's policy |

### 8.3 Wrap LLM Errors at the Use Case Boundary

The use case translates LLM errors into domain exceptions:

```python
# application/use_cases/classify_comment.py
class ClassifyCommentUseCase:
    def __init__(self, llm: ClassificationLlm) -> None:
        self._llm = llm

    async def execute(self, comment_text: str) -> CommentCategory:
        try:
            return await self._llm.classify(comment_text)
        except LlmContentFilterError:
            return CommentCategory.skipped("content_policy")
        except LlmError as e:
            raise ClassificationUnavailableError("LLM failure") from e
```

The HTTP layer never sees an `anthropic.APIStatusError` — only domain exceptions.

---

## 9. Testing LLM Code

LLM calls are non-deterministic. Test against a **fake LLM** that returns
canned responses, not against the real API.

```python
# tests/mocks/fake_classification_llm.py
from {pkg}.domain.value_objects.comment_category import CommentCategory
from {pkg}.domain.services.llms.classification_llm import ClassificationLlm

class FakeClassificationLlm:
    def __init__(self, response_map: dict[str, CommentCategory]) -> None:
        self._response_map = response_map

    async def classify(self, comment_text: str) -> CommentCategory:
        return self._response_map.get(comment_text, CommentCategory.other())
```

```python
# tests/application/use_cases/test_classify_comment.py
def test_returns_skipped_when_content_filter_triggers():
    llm = FakeClassificationLlm({...})
    # ...
```

For integration tests that genuinely need the real model (rare — record-and-
replay snapshot tests using `vcrpy` or similar are preferred), gate them behind
an env var so CI doesn't burn tokens on every run.

---

## 10. Definition of Done — LLM Checklist

For an LLM-touching change:

- [ ] Domain has a task-specific Protocol (`domain/services/llms/`) — not just generic `LlmClient`
- [ ] Concrete client lives in `infrastructure/llm/instructor_clients/` (Pydantic-bound) or `infrastructure/llm/providers/` (raw text)
- [ ] Prompt is in a `.md` file under `infrastructure/llm/prompts/`, not in code
- [ ] Pydantic schema for structured output uses `Field` constraints and `Literal` for closed sets (§ 4.4)
- [ ] `max_tokens` set explicitly (§ 6.1)
- [ ] Token usage logged at DEBUG (§ 6.2)
- [ ] Vendor exceptions wrapped as domain exceptions in the provider (§ 8.1)
- [ ] Use case wraps LLM exceptions into domain exceptions (§ 8.3)
- [ ] Tests use a fake LLM, not the real API (§ 9)
- [ ] If the prompt is static and large, prompt caching is applied (§ 6.3)
- [ ] Per-task model configurable via `Settings.llm_models.{task}` (§ 7.1)
