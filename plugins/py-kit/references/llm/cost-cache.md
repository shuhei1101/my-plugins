# llm/cost-cache — Token management and cost optimization

Standard tactics for keeping LLM API costs down.

---

## Measure first

Before optimizing, log token usage (see the example in `llm/providers.md`):

```python
logger.info("llm_call", extra={
    "provider": "openai",
    "model": "gpt-4o-mini",
    "input_tokens": usage.prompt_tokens,
    "output_tokens": usage.completion_tokens,
})
```

Aggregate the JSON Lines and compute daily cost as `input_tokens × input_unit_price + output_tokens × output_unit_price`.

---

## Limit output with `max_tokens`

```python
response = await client.chat.completions.create(
    model="gpt-4o-mini",
    messages=req,
    max_tokens=512,    # 出力上限
)
```

Without a limit, the model can "use up the full quota with verbose preamble". **Tighten it appropriately for the use case**:

| Use case | max_tokens guideline |
|---|---|
| Yes/No decision | 50 |
| Short classification tag | 100 |
| One-paragraph summary | 300 |
| Structured extraction (Pydantic) | 800-1024 |
| Long-form generation | 2048+ |

---

## Prompt caching (Anthropic)

The Claude API can cache the front portion of a prompt with `cache_control`.
Effective when **the same system prompt is used many times** (90% discount):

```python
response = await client.messages.create(
    model="claude-haiku-4-5-20251001",
    system=[
        {
            "type": "text",
            "text": LONG_SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"},   # 5 分キャッシュ
        },
    ],
    messages=[{"role": "user", "content": user_text}],
    max_tokens=1024,
)

# 使用量に cache_read_input_tokens が出る
logger.info("llm_call", extra={
    "cache_read_tokens": response.usage.cache_read_input_tokens,
    "cache_creation_tokens": response.usage.cache_creation_input_tokens,
})
```

**Conditions**:
- System prompt must be >= 1024 tokens (2048 for Haiku)
- Hits when called again within 5 minutes
- Part of the system + user message can also be cached

---

## Prompt caching (OpenAI)

OpenAI also has automatic prompt caching (gpt-4o and later). When you send a prompt
of `>= 1024 tokens` with the same prefix, a 50% discount is applied automatically. **No code changes needed**.
A `cached_tokens` field appears in the log.

---

## Model selection

| Use case | Recommended model |
|---|---|
| Simple classification / Yes-No / tagging | `gpt-4o-mini` / `claude-haiku-4-5` |
| Structured extraction / moderate reasoning | `gpt-4o` / `claude-sonnet-4-6` |
| Complex reasoning / long text / code generation | `claude-opus-4-7` / `o3` |

**Try the smallest model first; bump up if needed**. Starting with the biggest model is wasteful.

---

## Batch API

Both OpenAI and Anthropic have a Batch API. **Asynchronous, processed within 24h**, **50% discount**.

- Optimal for bulk processing that doesn't need to be real-time (e.g. nightly classification/extraction batches)
- Responses are fetched in bulk via S3 / Files API

```python
# OpenAI Batch
batch_input = [
    {
        "custom_id": "req-1",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {"model": "gpt-4o-mini", "messages": [...]},
    },
    ...
]
# JSONL ファイルにして Files API でアップロード、Batches API で submit
```

See each vendor's documentation for details. The code is standardized, so consider adopting it once you've decided on a "nightly batch."

---

## Streaming (not a cost saving, but a UX improvement)

```python
async for chunk in chat_stream(req):
    print(chunk, end="", flush=True)
```

Improves perceived performance. Shortens time-to-first-token (TTFT).
Cost is unchanged (actually slightly higher due to metadata).

---

## Pruning history

If you keep piling up conversation history, tokens grow exponentially.
**Keep the most recent N + summarize older history** is standard:

```python
async def trimmed_messages(history: list[Message], summary: str) -> list[Message]:
    """要約 + 直近 10 件だけ残す。"""
    recent = history[-10:]
    return [
        {"role": "system", "content": f"会話の要約: {summary}"},
        *recent,
    ]
```

Use an LLM (a small one) for the summary itself.

---

## What not to do

```python
# ❌ max_tokens 無制限
# 一発のリクエストで無駄に多くの出力をされる

# ❌ プロンプトキャッシュなしで巨大システムを毎回送る
# 同じプロンプトを 1000 回送ると 90% 損する

# ❌ 単純タスクに巨大モデル
# Yes/No 判定に Opus は過剰

# ❌ レスポンスをログに垂れ流す（コスト追跡できない）
# token 数を必ず構造化ログに残す
```

---

## Related files

- `llm/providers.md` — Implementing token usage logs
- `llm/exceptions-retry.md` — Rate-limit, alongside cost impact
- `shared/logger.md` — Aggregate cost via structured logs
