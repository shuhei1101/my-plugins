<!-- This file is a Japanese mirror of routes.md. When updating the English original, update this file too. -->
# fastapi/routes — ルーター実装パターン

ルーターは **薄い**。引数のパース・認証・例外マッピングを行い、本処理は `service.py` に委譲。

---

## 配置方針

| 配置 | 推奨ケース |
|---|---|
| `features/{feature}/route.py` | feature 単位で完結 |
| `server/routes/{feature}.py` | サーバ層で複数 feature をオーケストレーション |

新規プロジェクトでは **`features/{feature}/route.py`** を基本にする。
詳細は `architecture/layout.md`。

---

## 基本パターン

```python
# src/{pkg}/features/chat/route.py
from __future__ import annotations
from fastapi import APIRouter, Request, Depends
from typing import Annotated

from .types import ChatRequest, ChatResponse
from .service import generate_response

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_model=ChatResponse)
async def post_chat(
    body: ChatRequest,
    request: Request,
) -> ChatResponse:
    """ユーザー入力に対する LLM レスポンスを返す。"""
    handlers = request.app.state.handlers
    text = await handlers.generate_response(body.user_input)
    return ChatResponse(text=text)
```

---

## Annotated[Type, Depends/Query/Path] パターン

FastAPI 推奨。引数の意味と検証を 1 行に集約できる:

```python
from fastapi import Path, Query, Depends, Header
from typing import Annotated

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: Annotated[str, Path(min_length=1, max_length=64)],
    include_deleted: Annotated[bool, Query(description="削除済みも返すか")] = False,
    request_id: Annotated[str | None, Header(alias="x-request-id")] = None,
) -> UserResponse:
    ...
```

---

## Dependencies

共通ロジック（認証・DB セッション・request_id 等）は `Depends`:

```python
# src/{pkg}/server/deps.py
from fastapi import Depends, Header, HTTPException
from typing import Annotated

from {pkg}.shared.errors import UnauthorizedError

async def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
) -> User:
    """Authorization ヘッダから現在のユーザーを取得。"""
    if not authorization:
        raise UnauthorizedError("missing authorization header")
    # トークン検証
    user = _validate_token(authorization)
    return user

# 型エイリアス化
CurrentUser = Annotated[User, Depends(get_current_user)]

# ルートで使う
@router.get("/me", response_model=UserResponse)
async def get_me(user: CurrentUser) -> UserResponse:
    return UserResponse.from_domain(user)
```

---

## ハンドラを 1 関数に詰め込みすぎない

```python
# ❌ Bad: route 関数に処理本体が直書き
@router.post("/orders")
async def create_order(body: CreateOrderRequest, request: Request) -> OrderResponse:
    # 100 行ある処理
    items = await _fetch_items(...)
    total = sum(...)
    if total > limit:
        raise HTTPException(...)
    ...
```

```python
# ✅ Good: 処理本体は service.py へ
@router.post("/orders", response_model=OrderResponse)
async def create_order(
    body: CreateOrderRequest,
    request: Request,
) -> OrderResponse:
    handlers = request.app.state.handlers
    order = await handlers.create_order(body.to_domain())
    return OrderResponse.from_domain(order)
```

ルートの責務:
1. 入力パース（Pydantic でやる）
2. 認証（Depends）
3. service 関数呼び出し
4. レスポンス変換

---

## レスポンスモデルとステータスコード

```python
@router.post(
    "/users",
    response_model=UserResponse,
    status_code=201,                # 作成系は明示
    responses={
        201: {"description": "ユーザー作成成功"},
        400: {"description": "入力検証エラー"},
        409: {"description": "メールアドレス重複"},
    },
)
async def create_user(body: CreateUserRequest) -> UserResponse:
    ...
```

OpenAPI スキーマに反映される（`/docs` で見える）。

---

## ストリーミング応答

LLM のストリーミング応答を SSE で:

```python
from fastapi.responses import StreamingResponse

@router.post("/chat/stream")
async def post_chat_stream(body: ChatRequest, request: Request) -> StreamingResponse:
    handlers = request.app.state.handlers

    async def event_stream():
        async for chunk in handlers.chat_stream(body.user_input):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
```

---

## エラー処理

`AppError` 系は `register_exception_handlers` で HTTP に変換される（`shared/errors.md`）。
route 内では **直接 HTTPException を raise しない**:

```python
# ❌ Bad
if not user:
    raise HTTPException(404, "user not found")

# ✅ Good
if not user:
    raise NotFoundError(f"user {user_id} not found")
# → exception_handler が 404 にマップする
```

---

## ルーターの登録

```python
# src/{pkg}/server/app.py
from {pkg}.features.chat.route import router as chat_router
from {pkg}.features.users.route import router as users_router

app.include_router(chat_router)
app.include_router(users_router)
```

prefix と tags は各 router 側で設定済みなので `include_router` には追加しない。

---

## やってはいけないこと

```python
# ❌ ビジネスロジックを route 関数に書く
@router.post("/orders")
async def create_order(...):
    # 100 行の処理 ...

# ❌ route 内で直接 DB / 外部 API を叩く
@router.get("/users/{id}")
async def get_user(id: str):
    response = await httpx.get(f"...")   # service.py に分ける

# ❌ Pydantic 以外で引数を受ける（dict / list）
@router.post("/data")
async def post_data(body: dict): ...   # 型がない、検証ない
```

---

## 関連ファイル

- `fastapi/schemas.md` — ChatRequest / ChatResponse の作り方
- `fastapi/auth-and-errors.md` — Depends + exception_handler
- `fastapi/app.md` — アプリ全体構成
- `architecture/layout.md` — route.py の位置づけ
