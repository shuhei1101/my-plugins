# llm/cost-cache — Token management and cost optimization

Standard patterns for reducing LLM API costs.

---

## Measure first

Log token usage before optimizing (see `llm/providers.md` for an example):

```python
logger.info("llm_call", extra={
    "provider": "openai",
    "model": "gpt-4o-mini",
    "input_tokens": usage.prompt_tokens,
    "output_tokens": usage.completion_tokens,
})
```

Aggregate JSON Lines and compute daily cost as `input_tokens × input_price + output_tokens × output_price`.

---

## Limit output with `max_tokens`

```python
response = await client.chat.completions.create(
    model="gpt-4o-mini",
    messages=req,
    max_tokens=512,    # 出力上限
)
```

Without a limit, "the model burns up the cap with verbose preambles" can happen. **Tune appropriately for the use case**:

| Use case | max_tokens target |
|---|---|
| Yes/No decision | 50 |
| Short classification tag | 100 |
| One-paragraph summary | 300 |
| Structured extraction (Pydantic) | 800-1024 |
| Long-form generation | 2048+ |

---

## Prompt cache — design premise (most important)

**Prompt caching only works for the "common prefix from the top".** Matching only the middle or tail does not hit the cache.

The input to the LLM is stacked like a **stack** from top to bottom, and **only the leading prefix that matches byte-for-byte** is eligible for caching.
For example: if the system prompt matches exactly → hits up to that point; user message diverges → from there on it misses. That's how it cuts off.

### Design rule: static at top, dynamic at bottom

| Position | Content |
|---|---|
| **Top (head)** | Immutable character settings / role definition / output schema / few-shot examples — **the part you want cached** |
| **Middle** | Fixed per session (base context of the conversation, persona) |
| **Bottom (tail)** | Values that change per request (recent conversation history, user input, timestamp) |

If you stack them in reverse (put dynamic values on top), a single-character difference will **miss the cache for everything below it**, blowing up the cost.

### Concrete how-to

- For `system` messages, **concatenate immutable blocks first**. Move dynamic instructions to the user message side
- For the `messages` array, **older history goes higher**. For "summary + last N messages", order as "summary → old-to-new history → latest user input"
- Place few-shot examples in system or the first user/assistant pair (no random order)
- **Do not embed `{timestamp}` in the system message** — caching breaks every time it changes by one second

### Typical cache-busting mistakes

```python
# ❌ system プロンプトに動的値を入れる
system = f"You are an assistant. Current time: {now_iso()}"
# → 毎回違うのでキャッシュ完全ミス

# ❌ user 履歴の順序を入れ替える
messages = sorted(messages, key=lambda m: m["importance"])   # 並び順が変わる
# → 同じ会話でもキャッシュヒットしない

# ✅ 不変部分を上、動的部分を最下段に
system = STATIC_ROLE_AND_RULES
messages = [
    {"role": "system", "content": SUMMARY_OF_HISTORY},  # session で固定
    *recent_messages,                                    # 末尾だけ毎回変わる
    {"role": "user", "content": user_input},
]
```

---

## Prompt cache (Anthropic)

The Claude API uses `cache_control` to explicitly cache the prompt prefix.
Effective when **the same system prompt is used many times** (read cost drops to 10% of the input price):

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

# 使用量に cache_read_input_tokens / cache_creation_input_tokens が出る
logger.info("llm_call", extra={
    "cache_read_tokens": response.usage.cache_read_input_tokens,
    "cache_creation_tokens": response.usage.cache_creation_input_tokens,
})
```

**Conditions**:
- System prompt must be >= 1024 tokens (2048 for Haiku)
- Hits within 5 minutes of re-call (`ephemeral`). For longer-term, `cache_control: {"type": "ephemeral", "ttl": "1h"}` is also possible
- `cache_control` blocks can be attached to system / messages / tools. **Up to 4 blocks**
- A block boundary is "where the cache can be cut". The mental model: deliberately mark "fixed up to here"

---

## Prompt cache (OpenAI)

OpenAI also has **automatic prompt caching** (gpt-4o / o1 and later).
For prompts of **>= 1024 tokens**, sending **the same prefix automatically gets a 50% discount**. **No code changes required**.
The log shows the `usage.prompt_tokens_details.cached_tokens` field.

```python
response = await client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": LONG_SYSTEM_PROMPT},   # 同一テキストを送れば自動ヒット
        *messages,
    ],
)
logger.info("llm_call", extra={
    "cached_tokens": response.usage.prompt_tokens_details.cached_tokens,
})
```

**Conditions**:
- At least **the first 1024 tokens from the start** of the prompt must match the previous call
- Matching granularity is per 128 tokens (remainder is truncated)
- Cache expires in 5–10 minutes (no explicit control)

### Common operational points for both

- **Do not embed dynamic values in the system prompt** (see "typical cache-busting mistakes" above)
- High benefit for use cases that send the same system + history many times in one session (chat / streaming / batch extraction)
- No benefit for one-shot use cases (rather, Anthropic costs 25% extra during cache creation, making it more expensive)

---

## Anthropic cache — additional gotchas (brief)

Just the pitfalls you hit during implementation:

- **Stacking order**: hashed in `tools → system → messages` order. Changing a higher layer invalidates everything below (changing tools invalidates everything; changing system invalidates all messages, etc.)
- **Where to place the breakpoint**: put `cache_control` on the **last block that does not change**. Putting it on a variable block (timestamp / incoming message) means a cache miss + write every time — *more* expensive
- **Automatic vs explicit**:
  - **Automatic** (single `cache_control` at request root): API automatically places the breakpoint on the last cacheable block. Best default for **multi-turn conversations** because it follows the growing history
  - **Explicit** (`cache_control` per block, up to 4): use when you want to cache tools / system / past history independently
- **Lookback is 20 blocks**: an explicit breakpoint's lookback for prior writes is 20 blocks deep. In long conversations, once the breakpoint drifts 20+ blocks past the last write, hits stop — add a second explicit breakpoint in the static section so a write is always reachable
- **Minimum cacheable size** (below this, caching is silently disabled, no error):
  - Opus 4.5+ / Haiku 4.5: **4096 tokens**
  - Sonnet 4.x / Opus 4.x (pre-4.5): **1024 tokens**
  - Haiku 3.5: 2048 tokens
  - Verify: if `response.usage.cache_creation_input_tokens` and `cache_read_input_tokens` are both 0, nothing was cached
- **5m vs 1h cache**:
  - **5m**: default, write costs base input × 1.25, and each use refreshes it for free
  - **1h**: write costs base input × 2.0. Only worth it when reuse falls **between 5 min and 1 h**
  - When mixing, place **1h blocks before 5m blocks** (the longer TTL must come first, otherwise the API returns 400)
- **Pre-warming**: send a request with `max_tokens: 0` to write your system / tools into the cache and return immediately. Useful for warming the cache before users arrive

---

## Model selection

| Use case | Recommended model |
|---|---|
| Simple classification / Yes-No / tagging | `gpt-4o-mini` / `claude-haiku-4-5` |
| Structured extraction / mid-level reasoning | `gpt-4o` / `claude-sonnet-4-6` |
| Complex reasoning / long text / code generation | `claude-opus-4-7` / `o3` |

**Try the smallest model first → escalate if needed**. Starting with the biggest model is wasteful.

---

## Batch API

Both OpenAI and Anthropic have Batch APIs. **Asynchronous, processed within 24h**, with **50% discount**.

- Ideal for bulk processing that doesn't need real-time (nightly batch classification / extraction, etc.)
- Responses are retrieved via S3 / Files API in bulk

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

See each vendor's docs for details. The code is standardized, so consider adoption when "nightly batch" is decided.

---

## Streaming (UX improvement, not a cost reducer)

```python
async for chunk in chat_stream(req):
    print(chunk, end="", flush=True)
```

Improves perceived UX. Reduces time-to-first-token (TTFT).
Cost is unchanged (slightly increased by metadata).

---

## Pruning history

If you keep stacking conversation history, tokens grow exponentially.
The standard pattern is **last N messages + summarize old history**:

```python
async def trimmed_messages(history: list[Message], summary: str) -> list[Message]:
    """要約 + 直近 10 件だけ残す。"""
    recent = history[-10:]
    return [
        {"role": "system", "content": f"会話の要約: {summary}"},
        *recent,
    ]
```

Do the summarization with an LLM too (with a smaller model).

---

## Things you must not do

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

- `llm/providers.md` — implementation of token usage logging
- `llm/exceptions-retry.md` — rate-limit also affects cost
- `shared/logger.md` — cost aggregation via structured logs
