# Python LLM Client Standards — py-kit

Architecture conventions for projects that call LLM APIs (Claude, OpenAI, etc.).
Read together with `python-core.md` and `python-architecture.md`.

---

## Architecture Principle

Treat the LLM as an external service. All LLM API calls go through a Protocol interface defined in the domain layer, with concrete implementations in the infrastructure layer.

```python
# domain/repositories/llm_client.py
class LlmClient(Protocol):
    async def complete(self, prompt: str, *, max_tokens: int = 1024) -> str: ...
    async def complete_structured(self, prompt: str, schema: type[T]) -> T: ...

# infrastructure/llm/claude_client.py
class ClaudeClient:
    def __init__(self, api_key: str, model: str) -> None:
        self._client = anthropic.Anthropic(api_key=api_key)
        self._model = model

    async def complete(self, prompt: str, *, max_tokens: int = 1024) -> str:
        response = self._client.messages.create(
            model=self._model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
```

---

## Structured Output

Use Pydantic models for structured LLM output. Prefer Instructor for schema enforcement.

```python
from instructor import from_anthropic
import anthropic
from pydantic import BaseModel

class IssueList(BaseModel):
    issues: list[str]
    priority: Literal["high", "medium", "low"]

client = from_anthropic(anthropic.Anthropic())
result: IssueList = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    response_model=IssueList,
    messages=[{"role": "user", "content": prompt}],
)
```

---

## Prompt Management

- Store prompt templates as `.md` files in `{package_name}/prompts/`
- Load at startup with `Path(__file__).parent / "prompts" / "{name}.md"`
- Never hardcode prompt text inside function bodies
- Use `str.format(**kwargs)` or `string.Template` for variable substitution

---

## Token and Cost Management

- Always set `max_tokens` explicitly — never rely on defaults
- Log token usage (input + output) at DEBUG level for every API call
- Apply prompt caching (`cache_control`) for static system prompts longer than 1024 tokens
- Use batch API for bulk operations (>10 independent calls)

---

## Error Handling

```python
from anthropic import RateLimitError, APIStatusError

try:
    result = await llm_client.complete(prompt)
except RateLimitError:
    # exponential backoff, max 3 retries
    ...
except APIStatusError as e:
    logger.error("LLM API error %s: %s", e.status_code, e.message)
    raise
```

Wrap LLM errors in domain exceptions before they reach the application layer.
