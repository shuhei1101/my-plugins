# Composition Root — Wiring Functions

`main.py` is where you **assemble function dependencies**. No class-based DI container is used.

---

## Basic pattern: `build_app(settings)`

```python
# src/{pkg}/main.py
from __future__ import annotations
from functools import partial
from dataclasses import dataclass
from typing import Awaitable, Callable

from {pkg}.shared.settings import Settings
from {pkg}.integrations.llm.openai_client import chat_with_openai
from {pkg}.features.chat.service import generate_response
from {pkg}.features.users.service import create_user


@dataclass(frozen=True, slots=True)
class Handlers:
    """配線済み関数の束。"""
    generate_response: Callable[[str], Awaitable[str]]
    create_user: Callable[[CreateUserInput], User]


def build_handlers(settings: Settings) -> Handlers:
    """設定から関数依存を組み立てて返す。"""
    # 外部依存の準備
    chat = partial(
        chat_with_openai,
        api_key=settings.openai_api_key.get_secret_value(),
        model=settings.openai_model,
    )

    save_user = partial(save_user_to_db, db=settings.database_url)
    generate_id = generate_uuid_v7

    # 配線済み関数
    return Handlers(
        generate_response=partial(generate_response, chat=chat),
        create_user=partial(create_user, save=save_user, generate_id=generate_id),
    )


def main() -> None:
    """CLI から起動するエントリポイント。"""
    settings = Settings()
    handlers = build_handlers(settings)
    # 何らかの処理を実行
    result = handlers.create_user(CreateUserInput(name="alice", age=30))
    print(result)


if __name__ == "__main__":
    main()
```

### Why use a `Handlers` dataclass

Returning the wiring result as a dict (`dict[str, Callable]`) **makes key typos undetectable by static analysis**.
With a `Handlers` dataclass:
- The list of wired functions is explicit (doubles as API documentation)
- IDE completion works
- Type mismatches become errors

---

## Combining with FastAPI

```python
# src/{pkg}/server/app.py
from contextlib import asynccontextmanager
from fastapi import FastAPI

from {pkg}.shared.settings import Settings
from {pkg}.main import build_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """起動・終了時の処理。"""
    settings = Settings()
    app.state.handlers = build_handlers(settings)
    yield
    # cleanup（必要なら）


def build_fastapi(settings: Settings | None = None) -> FastAPI:
    """FastAPI アプリを組み立てる。"""
    from {pkg}.server.routes import chat, health

    app = FastAPI(lifespan=lifespan)
    app.include_router(chat.router)
    app.include_router(health.router)
    return app
```

Access from routes via `app.state.handlers`:

```python
# src/{pkg}/server/routes/chat.py
from fastapi import APIRouter, Request

router = APIRouter(prefix="/chat")

@router.post("")
async def post_chat(request: Request, body: ChatRequest) -> ChatResponse:
    handlers: Handlers = request.app.state.handlers
    text = await handlers.generate_response(body.user_input)
    return ChatResponse(text=text)
```

---

## Combining with CLI

```python
# src/{pkg}/__main__.py
import argparse
import sys
from {pkg}.shared.settings import Settings
from {pkg}.main import build_handlers


def main() -> int:
    """python -m {pkg} で起動するエントリポイント。"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    args = parser.parse_args()

    settings = Settings()
    handlers = build_handlers(settings)
    user = handlers.create_user(CreateUserInput(name=args.name, age=0))
    print(user)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

---

## Use library-standard classes as they are

Don't twist standards to "do it with functions." If the library officially recommends class usage, keep it as a class:

| Library | Where class usage is required |
|---|---|
| FastAPI | `FastAPI()` instance, `APIRouter`, `Middleware` classes, `BaseHTTPMiddleware` subclassing |
| Pydantic | `BaseModel` subclassing, `BaseSettings` subclassing |
| typer / click | `Command` class, `Group` class |
| SQLAlchemy (if used) | `DeclarativeBase` subclassing |
| asyncio | `asyncio.Task`, `asyncio.Queue` |

These are acceptable under the "**follow library standards**" principle.

---

## When the composition root grows

When `build_handlers` becomes long, **split by functional category**:

```python
# src/{pkg}/main.py
def build_handlers(settings: Settings) -> Handlers:
    llm = _build_llm_handlers(settings)
    user = _build_user_handlers(settings)
    return Handlers(**llm, **user)


def _build_llm_handlers(settings: Settings) -> dict[str, Callable]:
    chat = partial(chat_with_openai, api_key=settings.openai_api_key.get_secret_value())
    return {
        "generate_response": partial(generate_response, chat=chat),
    }


def _build_user_handlers(settings: Settings) -> dict[str, Callable]:
    save_user = partial(save_user_to_db, db=settings.database_url)
    return {
        "create_user": partial(create_user, save=save_user, generate_id=uuid_v7),
    }
```

That said, the `Handlers` dataclass listing alone should provide enough organization in most cases.
Splitting can wait until it is genuinely needed.

---

## Swapping in tests

Create a test-specific function in place of `build_handlers` and inject mocks:

```python
# tests/conftest.py
from {pkg}.main import Handlers
from {pkg}.features.chat.service import generate_response
from {pkg}.integrations.llm.mock_client import chat_with_mock


def build_test_handlers() -> Handlers:
    return Handlers(
        generate_response=partial(generate_response, chat=chat_with_mock),
        create_user=partial(create_user, save=_save_user_memory, generate_id=lambda: "test-id"),
    )
```

**Design `build_app`-style functions with testing in mind.** Make every external dependency receivable as an argument so mocks can be easily injected during tests.

---

## Related files

- `architecture/ts-style.md` — Function type alias + injection patterns
- `architecture/layout.md` — Where to place main.py
- `architecture/dependencies.md` — Dependency direction
- `fastapi/app.md` — FastAPI-specific setup
