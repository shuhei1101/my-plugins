# fastapi/app — FastAPI Application Composition

Build `build_fastapi(settings) -> FastAPI` in `server/app.py`.
Wire dependencies through `build_handlers(settings)` from `main.py`.

---

## Sample

```python
# src/{pkg}/server/app.py
from __future__ import annotations
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from {pkg}.shared.settings import Settings
from {pkg}.shared.errors import AppError
from {pkg}.main import build_handlers, Handlers
from {pkg}.server.routes import chat, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """起動・終了時の処理。"""
    settings = Settings()
    app.state.settings = settings
    app.state.handlers = build_handlers(settings)
    yield
    # cleanup（必要なら）


def build_fastapi() -> FastAPI:
    """FastAPI アプリを組み立てる。`uvicorn --factory` で呼ぶ。"""
    app = FastAPI(
        title="MyApp",
        version="0.1.0",
        lifespan=lifespan,
    )

    # ----- ミドルウェア -----
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ----- ルーター -----
    app.include_router(health.router)
    app.include_router(chat.router)

    # ----- 例外ハンドラ -----
    from {pkg}.server.error_handlers import register_exception_handlers
    register_exception_handlers(app)

    return app
```

---

## Launching

```bash
uv run uvicorn {pkg}.server.app:build_fastapi --factory --reload --host 127.0.0.1 --port 8000
```

Adding `--factory` uses the return value of calling `build_fastapi()` (resilient to parameterization).

---

## lifespan

Express startup / shutdown with a lifespan using `@asynccontextmanager`:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ----- startup -----
    settings = Settings()
    app.state.settings = settings
    app.state.handlers = build_handlers(settings)
    logger.info("starting", extra={"env": settings.env})

    yield

    # ----- shutdown -----
    logger.info("shutting down")
    # close connections, flush logs, etc.
```

`on_event("startup")` / `on_event("shutdown")` are **deprecated** (consolidate on lifespan).

---

## Referencing from routes

If a route function receives `Request`, it can access via `request.app.state.handlers`:

```python
# src/{pkg}/server/routes/chat.py
from fastapi import APIRouter, Request
from {pkg}.features.chat.types import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def post_chat(request: Request, body: ChatRequest) -> ChatResponse:
    handlers: Handlers = request.app.state.handlers
    text = await handlers.generate_response(body.user_input)
    return ChatResponse(text=text)
```

Or wrap with `Depends`:

```python
# src/{pkg}/server/deps.py
from fastapi import Request, Depends
from typing import Annotated

def get_handlers(request: Request) -> Handlers:
    return request.app.state.handlers

HandlersDep = Annotated[Handlers, Depends(get_handlers)]


# routes 側
@router.post("")
async def post_chat(body: ChatRequest, handlers: HandlersDep) -> ChatResponse:
    text = await handlers.generate_response(body.user_input)
    return ChatResponse(text=text)
```

Use the `Annotated[T, Depends(...)]` pattern as the default (FastAPI recommended).

---

## CORS

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,    # 環境ごとに切替
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

In production avoid `allow_origins=["*"]`; use a whitelist instead.

---

## Custom middleware

```python
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class RequestIdMiddleware(BaseHTTPMiddleware):
    """X-Request-Id ヘッダを付与・ログに残す。"""

    async def dispatch(self, request: Request, call_next) -> Response:
        rid = request.headers.get("x-request-id") or _gen_id()
        request.state.request_id = rid

        response = await call_next(request)
        response.headers["x-request-id"] = rid
        return response


# 登録
app.add_middleware(RequestIdMiddleware)
```

Middleware is **class-based** by default (FastAPI requirement).
Write internal processing as functions (inside `dispatch`).

---

## Health check

```python
# src/{pkg}/server/routes/health.py
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/healthz")
async def healthz() -> dict[str, str]:
    """シンプルな疎通確認。"""
    return {"status": "ok"}
```

Do not include dependencies like the DB (avoid being judged unhealthy when external dependencies fail).

See `fastapi/health.md` for details.

---

## OpenAPI schema

The values of `FastAPI(title=, version=)` appear in `/docs`.
To add more metadata:

```python
app = FastAPI(
    title="MyApp",
    version="0.1.0",
    description="LLM-driven chat service.",
    openapi_tags=[
        {"name": "chat", "description": "Chat endpoints"},
        {"name": "health", "description": "Health check"},
    ],
)
```

Adding `tags=[...]` on a router groups them.

---

## Do not

```python
# ❌ グローバル変数で settings を持つ
SETTINGS = Settings()   # モジュールロード時に env が読まれる→テストやりにくい
# → lifespan で app.state へ

# ❌ build_fastapi の引数を増やしすぎる
def build_fastapi(settings, handlers, logger, db_pool, ...) -> FastAPI:
    ...
# → lifespan に集約

# ❌ on_event を使う
@app.on_event("startup")
async def startup(): ...   # 非推奨、lifespan に統一
```

---

## Related files

- `fastapi/routes.md` — Router implementation patterns
- `fastapi/schemas.md` — Request/response Pydantic
- `fastapi/auth-and-errors.md` — Authentication and exception handlers
- `fastapi/health.md` — Health check
- `architecture/composition-root.md` — Integration with build_handlers
