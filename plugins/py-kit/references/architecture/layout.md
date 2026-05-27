# Top-Level Layout + Feature-Internal Structure

The py-kit standard is a **feature-folder layout**. Pure DDD (domain / application / infrastructure / interface) is abolished.

---

## Top-level structure

```
src/{pkg}/
├── __init__.py
├── __main__.py
├── main.py                       # composition root (required)
├── shared/                       # cross-cutting infrastructure (required)
├── features/                     # business features (optional)
├── integrations/                 # external service integrations (optional)
├── runtime/                      # runtime infrastructure (optional)
└── server/                       # HTTP/WS server (optional)
```

### Required

| Path | Role |
|---|---|
| `__init__.py` | Package marker |
| `main.py` | Composition root (wires functions with `functools.partial`) |
| `shared/` | logger / settings / errors / types / constants / utils |

### Optional (create only if the project uses them)

| Path | Role | Example |
|---|---|---|
| `__main__.py` | Entry point launched via `python -m {pkg}` | CLI tool |
| `features/` | Business features | `features/chat/`, `features/auto_tweet/` |
| `integrations/` | External service integrations | `integrations/llm/`, `integrations/tts/`, `integrations/obs/` |
| `runtime/` | Runtime infrastructure (queue / workflow / state) | Needed at AITuber scale |
| `server/` | HTTP/WS server | When using FastAPI |

### Abolished concepts

- Do not create a `modes/` folder (place the same patterns under `features/`)
- Do not use `domain/` / `application/` / `infrastructure/` / `interface/`
- Do not create a `core/` folder (merge into `shared/`)

---

## Structure inside a feature folder

```
{pkg}/features/{feature}/
├── __init__.py             # Public API (required)
├── types.py                # Type definitions (DTOs + type aliases + Protocols)
├── query.py                # Read functions (find / list / get / search)
├── service.py              # Business logic functions (create / update / delete / compound operations)
├── route.py                # HTTP handlers (only when this feature is exposed to the web)
├── client.py               # External API call functions (mainly used under integrations)
├── db.py                   # Persistence (only when using a DB; basically unnecessary under the new policy)
├── prompts/                # Prompt files (LLM features only)
└── _helpers.py             # Helpers used only inside this feature
```

### Minimal structure for a small feature

```
{pkg}/features/chat/
├── __init__.py
├── types.py
└── service.py
```

This is not "put everything in"; it is the standard of "**when you use this name, this is its role**."
For small features, just `types.py` + `service.py` is fine.

### Sub-features

When a feature grows, create a sub-folder with the same structure:

```
{pkg}/features/chat/
├── __init__.py
├── types.py
├── service.py
├── personal/               # Sub-feature
│   ├── __init__.py
│   ├── types.py
│   └── service.py
└── auto_tweet/
    └── ...
```

---

## Contents of shared/

```
{pkg}/shared/
├── __init__.py
├── logger.py               # JSONL logger
├── settings.py             # Pydantic Settings
├── errors.py               # Exception hierarchy
├── types.py                # Common type aliases
├── constants.py            # Computed paths (PROJECT_ROOT, LOG_DIR)
└── utils.py                # Cross-business helpers
```

Do not create a `core/` folder (merged into shared/).
Library-like functionality (logger / settings / errors) and cross-business helpers (utils) are consolidated in one folder.

See each `shared/{xxx}.md` for details.

---

## Contents of integrations/

```
{pkg}/integrations/
├── __init__.py
├── llm/                    # LLM providers
│   ├── __init__.py
│   ├── types.py            # AsyncChatFn / ChatRequest / ChatResponse, etc.
│   ├── openai_client.py    # OpenAI implementation
│   ├── claude_client.py    # Anthropic implementation
│   ├── mock_client.py      # Mock for testing
│   └── prompts/            # Prompt files
├── tts/                    # TTS providers
│   └── ...
└── obs/                    # OBS WebSocket
    └── ...
```

`integrations/` is the **boundary with external services**.
- Define function type aliases (e.g., `AsyncChatFn`) in `types.py`
- Provide each provider implementation in a separate file
- Place test mocks in the same folder

---

## Contents of server/ (when using FastAPI)

```
{pkg}/server/
├── __init__.py
├── app.py                  # build_fastapi(settings) -> FastAPI
├── lifespan.py             # startup / shutdown
├── middleware.py           # CORS / auth / logging
├── routes/                 # Routers
│   ├── __init__.py
│   ├── chat.py             # /chat endpoints
│   └── health.py           # /healthz
└── ws/                     # WebSocket
    └── chat.py
```

When to choose `features/{feature}/route.py` vs `server/routes/{feature}.py`:

| Style | Recommended case |
|---|---|
| `features/{feature}/route.py` | Self-contained per feature. Route + service are tightly coupled |
| `server/routes/{feature}.py` | When you want full separation of route and service, or combine multiple features in one route |

For new projects, default to **`features/{feature}/route.py`** (self-contained within the feature).
Aggregate them via `include_router` in `server/app.py` at server startup.

---

## Contents of runtime/ (optional; used at AITuber scale)

```
{pkg}/runtime/
├── __init__.py
├── queue.py                # Message queue
├── workflow.py             # State machine / workflow
└── state.py                # Runtime state (connection pools, sessions, etc.)
```

---

## tests/ structure

```
tests/
├── __init__.py
├── conftest.py             # Shared fixtures
├── features/               # Mirrors features/
│   ├── chat/
│   │   └── test_chat.py    # Integration tests
│   └── ...
├── server/                 # Mirrors server/
│   └── test_routes_chat.py
└── smoke/                  # Smoke tests (only manual user execution)
    └── test_llm.py
```

See `testing/strategy.md` for details.

---

## Single-file script case

A simple script without `pyproject.toml`:

```
project/
├── script.py
├── log/                    # Execution log output directory
└── run.bat                 # Launcher
```

See `scripts/python-script.md` for details.

---

## Related files

- `architecture/ts-style.md` — Style of type aliases + functions used inside a feature
- `architecture/composition-root.md` — Responsibilities of main.py
- `architecture/dependencies.md` — Dependency direction
- `core/naming.md` — Standard filenames inside a feature
