# Top-level layout + feature internal structure

dev-kit Python's standard is **feature-folder layout**. Pure DDD (domain / application / infrastructure / interface) is discontinued.

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
| `__init__.py` | package marker |
| `main.py` | composition root (wire functions via `functools.partial`) |
| `shared/` | logger / settings / errors / types / constants / utils |

### Optional (create only if used in the project)

| Path | Role | Example |
|---|---|---|
| `__main__.py` | entry point for `python -m {pkg}` | CLI tool |
| `features/` | business features | `features/chat/`, `features/auto_tweet/` |
| `integrations/` | external service integrations | `integrations/llm/`, `integrations/tts/` |
| `runtime/` | runtime infrastructure (queue / workflow / state) | as needed |
| `server/` | HTTP/WS server | when using FastAPI |

---

## Inside a feature folder

```
{pkg}/features/{feature}/
├── __init__.py             # public API (required)
├── types.py                # type definitions (DTO + type aliases + Protocol)
├── query.py                # read-only functions (find / list / get / search)
├── service.py              # business logic functions (create / update / delete / composite ops)
├── route.py                # HTTP handlers (only when the feature is exposed on the Web)
├── client.py               # external API call functions (mainly used under integrations)
├── db.py                   # persistence (only if DB is used. With the new policy, generally not needed)
├── prompts/                # prompt files (LLM features only)
└── _helpers.py             # helpers internal to this feature only
```

### Minimum layout for small features

```
{pkg}/features/chat/
├── __init__.py
├── types.py
└── service.py
```

Not "put everything", but rather a standard of "**when you use this name, this is the role**".
For small features, just `types.py` + `service.py` is fine.

### Sub-features

When a feature grows, branch off sub-folders with the same structure:

```
{pkg}/features/chat/
├── __init__.py
├── types.py
├── service.py
└── personal/               # sub-feature
    ├── __init__.py
    ├── types.py
    └── service.py
```

---

## Inside shared/

```
{pkg}/shared/
├── __init__.py
├── logger.py               # JSONL logger
├── settings.py             # Pydantic Settings
├── errors.py               # exception hierarchy
├── types.py                # common type aliases
├── constants.py            # precomputed paths (PROJECT_ROOT, LOG_DIR)
└── utils.py                # cross-business helpers
```

Do not create a `core/` folder (consolidated into shared/).
Library-like utilities (logger / settings / errors) and cross-business helpers (utils) live together in one folder.

See each `shared/{xxx}.md` for details.

---

## Inside integrations/

```
{pkg}/integrations/
├── __init__.py
└── llm/                    # sub-folder per service type
    ├── __init__.py
    ├── types.py            # function type aliases (AsyncChatFn etc.) and DTOs
    ├── openai_client.py    # per-vendor implementations
    ├── claude_client.py
    └── mock_client.py      # mock for testing
```

`integrations/` is the **boundary with external services**.
- Define function type aliases (`AsyncChatFn` etc.) in `types.py`
- Provide each provider implementation in a separate file
- Place the test mock in the same folder

> Prompt files live in **`prompts/` directly under the project root** (see `llm/prompts-authoring.md`).
> Under `integrations/llm/`, place only loaders and provider implementations.

---

## Inside server/ (when using FastAPI)

```
{pkg}/server/
├── __init__.py
├── app.py                  # build_fastapi(settings) -> FastAPI
├── lifespan.py             # startup / shutdown
├── middleware.py           # CORS / auth / logging
├── routes/                 # routers
│   ├── __init__.py
│   ├── chat.py             # /chat endpoints
│   └── health.py           # /healthz
└── ws/                     # WebSocket
    └── chat.py
```

Choosing between placing routes in `features/{feature}/route.py` vs `server/routes/{feature}.py`:

| Style | Recommended case |
|---|---|
| `features/{feature}/route.py` | self-contained per feature. route + service tightly coupled |
| `server/routes/{feature}.py` | want full separation of route and service. Aggregate multiple features into one route |

For new projects, default to **`features/{feature}/route.py`** (self-contained inside the feature).
At server startup, aggregate via `include_router` from `server/app.py`.

---

## Inside runtime/ (optional, used in large projects)

```
{pkg}/runtime/
├── __init__.py
├── queue.py                # message queue
├── workflow.py             # state machine / workflow
└── state.py                # runtime state (connection pools, sessions, etc.)
```

---

## tests/ structure

```
tests/
├── __init__.py
├── conftest.py             # shared fixtures
├── features/               # mirrors features/
│   ├── chat/
│   │   └── test_chat.py    # integration tests
│   └── ...
├── server/                 # mirrors server/
│   └── test_routes_chat.py
└── smoke/                  # smoke tests (user manual execution only)
    └── test_llm.py
```

See `testing/strategy.md` for details.

---

## Single-file scripts

Simple scripts without a `pyproject.toml`:

```
project/
├── script.py
├── log/                    # execution log output
└── run.bat                 # launcher
```

See `scripts/python-script.md` for details.

---

## Related files

- `architecture/ts-style.md` — type aliases + function style used inside features
- `architecture/composition-root.md` — responsibilities of main.py
- `architecture/dependencies.md` — dependency direction
- `core/naming.md` — standard file names inside a feature
