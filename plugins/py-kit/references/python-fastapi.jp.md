<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# Python FastAPI 規約 — py-kit（日本語ミラー）

> このファイルは `python-fastapi.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `python-fastapi.md` にも反映してください。

FastAPI プロジェクトの規約。`python-core.md` および `python-architecture.md` と
合わせて読む。本ファイルは `python-architecture.md § 8` の純DDDレイアウトを
前提とする — FastAPI は `interface/api/` に住む。

---

## 1. DDD レイアウト内での FastAPI の位置

FastAPI はインターフェース層の技術。`domain/` や `application/` には**置かない**。ルーターは HTTP をユースケース呼び出しに翻訳し、ユースケース結果を HTTP レスポンスに翻訳して返す。

```
{pkg}/interface/api/
├── __init__.py
├── main.py                  # FastAPI app を作成・ルーター + ミドルウェアを配線
├── routers/
│   ├── __init__.py
│   ├── orders.py
│   ├── customers.py
│   └── health.py
├── dependencies.py          # FastAPI Depends() ファクトリ — Container から引く
├── middleware.py            # CORS / 認証 / ロギング / エラーマッピングミドルウェア
├── error_handlers.py        # @app.exception_handler 関数
└── schemas/                 # リクエストボディ・レスポンス用の Pydantic モデル
    ├── __init__.py
    ├── order_request.py
    └── order_response.py
```

Container（`{pkg}/main.py`）は app 構築前に配線；ルーターは `Depends(...)` 経由で Container からユースケースを取得する。

---

## 2. App 構築

### 2.1 `build_app(container)` パターン

App ファクトリが Container を受け取るので、テストでフェイクに差し替え可能。

```python
# {pkg}/interface/api/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from {pkg}.container import Container
from {pkg}.interface.api.routers import orders, customers, health
from {pkg}.interface.api.middleware import RequestLoggingMiddleware
from {pkg}.interface.api.error_handlers import register_exception_handlers


def build_app(container: Container) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # 起動時
        container.logger.info("API starting on port %s", container.settings.port)
        yield
        # シャットダウン時
        container.logger.info("API shutting down")
        await container.cleanup()

    app = FastAPI(
        title=container.settings.app_name,
        version=container.settings.app_version,
        lifespan=lifespan,
    )

    app.state.container = container

    app.add_middleware(
        CORSMiddleware,
        allow_origins=container.settings.cors_allowed_origins,  # 明示・絶対 ["*"] にしない
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
    )
    app.add_middleware(RequestLoggingMiddleware)

    register_exception_handlers(app)

    app.include_router(health.router)
    app.include_router(orders.router, prefix="/orders", tags=["orders"])
    app.include_router(customers.router, prefix="/customers", tags=["customers"])

    return app
```

### 2.2 `__main__.py` エントリポイント

```python
# {pkg}/__main__.py
import uvicorn

from {pkg}.container import build_container
from {pkg}.interface.api.main import build_app


def run() -> None:
    container = build_container()
    app = build_app(container)
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=container.settings.port,
        log_config=None,    # 自前ロガー使用・uvicorn のは使わない
        access_log=False,   # RequestLoggingMiddleware でロギング
    )


if __name__ == "__main__":
    run()
```

### 2.3 lifespan — 非推奨 `@app.on_event` を置き換え

`lifespan` を使う（FastAPI 0.93+ 以降）。`@app.on_event("startup")` / `@app.on_event("shutdown")` は非推奨 — 使わない。

```python
# ✅ 良い
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 起動時
    await db.connect()
    yield
    # シャットダウン時
    await db.disconnect()

app = FastAPI(lifespan=lifespan)

# ❌ 悪い — 非推奨
@app.on_event("startup")
async def startup() -> None:
    await db.connect()
```

---

## 3. ルーター

### 3.1 リソースごとに1ルーターファイル

| リソース | ファイル |
|---|---|
| `/orders/*` | `routers/orders.py` |
| `/customers/*` | `routers/customers.py` |
| `/users/*` | `routers/users.py` |
| `/health` | `routers/health.py` |

リソース横断のエンドポイント（`/admin/dashboard`・`/me/feed`）は機能名で別ファイル。

### 3.2 ルーターモジュールテンプレート

```python
# {pkg}/interface/api/routers/orders.py
from fastapi import APIRouter, Depends, status

from {pkg}.application.use_cases.create_order import CreateOrderUseCase, CreateOrderInput
from {pkg}.application.use_cases.cancel_order import CancelOrderUseCase, CancelOrderInput
from {pkg}.application.use_cases.list_orders import ListOrdersUseCase, ListOrdersInput
from {pkg}.domain.value_objects.customer_id import CustomerId
from {pkg}.domain.value_objects.order_id import OrderId
from {pkg}.interface.api.dependencies import get_create_order, get_cancel_order, get_list_orders
from {pkg}.interface.api.schemas.order_request import CreateOrderRequest
from {pkg}.interface.api.schemas.order_response import OrderResponse, OrderListResponse
from {pkg}.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    body: CreateOrderRequest,
    use_case: CreateOrderUseCase = Depends(get_create_order),
) -> OrderResponse:
    logger.info("POST /orders customer=%s", body.customer_id)
    input = CreateOrderInput(
        customer_id=CustomerId(body.customer_id),
        line_items=body.to_domain_line_items(),
    )
    order = use_case.execute(input)
    return OrderResponse.from_domain(order)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    list_use_case: ListOrdersUseCase = Depends(get_list_orders),
) -> OrderResponse:
    order = list_use_case.find_by_id(OrderId(order_id))
    return OrderResponse.from_domain(order)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_order(
    order_id: str,
    use_case: CancelOrderUseCase = Depends(get_cancel_order),
) -> None:
    use_case.execute(CancelOrderInput(order_id=OrderId(order_id)))
```

### 3.3 ルート関数ルール（硬性）

| ルール | 理由 |
|---|---|
| ルート関数は**薄い** — 最大でも：log・ユースケース入力構築・ユースケース呼び出し・レスポンス構築 | ビジネスロジックはユースケースに |
| ルートボディにビジネスロジック・リポジトリ呼び出し・外部 SDK 呼び出し禁止 | ルート関数はインターフェース関心 |
| リクエストボディ型 = `schemas/` の Pydantic モデル | 境界でバリデーション |
| レスポンス型 = `schemas/` の Pydantic モデル（`response_model=` かアノテーション） | シリアライズ shape を明示 |
| パスパラメータは境界で値オブジェクトに変換 | `OrderId(order_id)`・生 `str` ではない |
| 200 以外は `status_code=` を明示 | 作成・削除の偶発 200 を避ける |
| ルート入口で `logger.info` 1回（認証後・主要パラメータ付き・PII なし） | 監査ログ・デバッグ性 |

### 3.4 ルート命名と HTTP 動詞

| アクション | 動詞 | パス | 成功ステータス |
|---|---|---|---|
| 作成 | `POST` | `/orders` | 201 |
| 1件読み出し | `GET` | `/orders/{id}` | 200 |
| 一覧読み出し | `GET` | `/orders` | 200 |
| 全置換 | `PUT` | `/orders/{id}` | 200 |
| 部分更新 | `PATCH` | `/orders/{id}` | 200 |
| 削除 | `DELETE` | `/orders/{id}` | 204 |
| アクション（非CRUD） | `POST` | `/orders/{id}/cancel` | 200（ボディなしなら 204） |

状態変化操作に `GET` を絶対使わない。読み取り専用クエリに `POST` を絶対使わない。

### 3.5 クエリパラメータとページネーション

```python
@router.get("", response_model=OrderListResponse)
async def list_orders(
    customer_id: str | None = None,
    status_: Literal["pending", "shipped", "cancelled"] | None = Query(default=None, alias="status"),
    limit: int = Query(default=20, ge=1, le=100),
    cursor: str | None = None,
    use_case: ListOrdersUseCase = Depends(get_list_orders),
) -> OrderListResponse:
    ...
```

数百件以上に育つ可能性のあるリストはカーソルベースを推奨；小さな管理画面ならページベースで可。

---

## 4. `Depends()` による依存性注入

### 4.1 Container からユースケースを取り出す

```python
# {pkg}/interface/api/dependencies.py
from fastapi import Request

from {pkg}.application.use_cases.create_order import CreateOrderUseCase
from {pkg}.application.use_cases.cancel_order import CancelOrderUseCase
from {pkg}.container import Container


def get_container(request: Request) -> Container:
    return request.app.state.container


def get_create_order(container: Container = Depends(get_container)) -> CreateOrderUseCase:
    return container.create_order


def get_cancel_order(container: Container = Depends(get_container)) -> CancelOrderUseCase:
    return container.cancel_order
```

ルーターはリポジトリ呼び出しもユースケースインスタンス化も**しない** — `Depends` だけで解決。

### 4.2 認証依存

```python
# {pkg}/interface/api/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer = HTTPBearer()


async def current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    container: Container = Depends(get_container),
) -> User:
    try:
        return await container.auth_service.verify_token(credentials.credentials)
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token") from e
```

認証必須ルートで：

```python
@router.post("", response_model=OrderResponse)
async def create_order(
    body: CreateOrderRequest,
    user: User = Depends(current_user),
    use_case: CreateOrderUseCase = Depends(get_create_order),
) -> OrderResponse:
    ...
```

### 4.3 リクエスト毎の DB セッション（同期 ORM 使用時）

```python
async def db_session(container: Container = Depends(get_container)) -> AsyncIterator[Session]:
    with container.db_session_factory() as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
```

非同期 ORM（asyncpg・async SQLAlchemy）でも `async with` / `await` で同じパターン。

---

## 5. Pydantic Schema

### 5.1 リソース毎に1ファイル・request と response 分離

```
schemas/
├── order_request.py    # CreateOrderRequest, UpdateOrderRequest, ...
├── order_response.py   # OrderResponse, OrderListResponse, OrderSummaryResponse
└── ...
```

### 5.2 リクエスト Schema パターン

```python
# schemas/order_request.py
from pydantic import BaseModel, Field

class LineItemRequest(BaseModel):
    sku: str = Field(..., min_length=1, max_length=64)
    quantity: int = Field(..., ge=1, le=999)


class CreateOrderRequest(BaseModel):
    customer_id: str = Field(..., min_length=1)
    line_items: list[LineItemRequest] = Field(..., min_length=1, max_length=100)
    note: str | None = Field(default=None, max_length=500)

    def to_domain_line_items(self) -> list[LineItem]:
        return [LineItem(sku=Sku(item.sku), quantity=item.quantity) for item in self.line_items]
```

### 5.3 レスポンス Schema パターン

```python
# schemas/order_response.py
from pydantic import BaseModel
from {pkg}.domain.entities.order import Order

class OrderResponse(BaseModel):
    id: str
    customer_id: str
    status: str
    total: int
    created_at: datetime

    @classmethod
    def from_domain(cls, order: Order) -> "OrderResponse":
        return cls(
            id=str(order.id),
            customer_id=str(order.customer_id),
            status=order.status.value,
            total=order.total.amount,
            created_at=order.created_at,
        )


class OrderListResponse(BaseModel):
    orders: list[OrderResponse]
    next_cursor: str | None = None
```

### 5.4 Schema ルール

| ルール | 理由 |
|---|---|
| リクエスト Schema は `Field(...)` 制約（min/max・長さ・範囲）を持つ | ビジネスロジックが走る前に境界バリデーション |
| レスポンス Schema は `from_domain()` classmethod を持つ | ドメイン → ワイヤー形式マッピングを1箇所に集約 |
| Schema は識別子に `str` を使う（`NewType` 値オブジェクトではない） | Pydantic は `NewType` を自動処理しない；`to_domain_*` メソッドで変換 |
| `to_domain_*` / `from_domain` にフィールド翻訳以外のビジネスロジック禁止 | バリデーションは Schema の仕事・ビジネスロジックはユースケースの仕事 |
| 再利用：繰り返し構造はネスト Pydantic モデル（`LineItemRequest`） | ワイヤー shape の単一情報源 |

---

## 6. ミドルウェア

### 6.1 リクエストロギングミドルウェア

```python
# {pkg}/interface/api/middleware.py
import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from {pkg}.logger import get_logger

logger = get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))
        request.state.request_id = request_id

        start = time.perf_counter()
        logger.info("request: %s %s req_id=%s", request.method, request.url.path, request_id)

        response = await call_next(request)

        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "response: %s %s status=%s req_id=%s duration_ms=%.1f",
            request.method, request.url.path, response.status_code, request_id, elapsed_ms,
        )
        response.headers["X-Request-Id"] = request_id
        return response
```

### 6.2 CORS — 本番で `*` 禁止

```python
# ✅ 良い — settings から明示的なリスト
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,  # ["https://app.example.com"]
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-Request-Id"],
)

# ❌ 悪い — 本番でワイルドカード
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # allow_credentials=True と併用不可
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

ローカル開発でワイルドカードが必要なら環境でガード：

```python
allow_origins = ["*"] if settings.env == "local" else settings.cors_allowed_origins
```

### 6.3 認証ミドルウェア vs 認証依存

| パターン | 使う場面 |
|---|---|
| 各ルートに `Depends(current_user)` | ほとんどのアプリ — ルート単位で明示 |
| `request.state.user` を埋める認証ミドルウェア | 95%+ のルートが同じ認証で・公開ルート許可リストがクリーンなとき |

依存パターンを推奨 — 明示的でルートシグネチャから見える。

---

## 7. エラー処理

### 7.1 ドメイン例外 → HTTP ステータスマッピング

```python
# {pkg}/interface/api/error_handlers.py
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from {pkg}.domain.exceptions import (
    OrderNotFoundError,
    RefundWindowClosedError,
    InvalidOrderStateError,
)
from {pkg}.infrastructure.exceptions import RepositoryUnavailableError
from {pkg}.logger import get_logger

logger = get_logger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(OrderNotFoundError)
    async def handle_not_found(request: Request, exc: OrderNotFoundError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "order_not_found", "message": str(exc)},
        )

    @app.exception_handler(RefundWindowClosedError)
    async def handle_refund_closed(request: Request, exc: RefundWindowClosedError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error": "refund_window_closed", "message": str(exc)},
        )

    @app.exception_handler(InvalidOrderStateError)
    async def handle_invalid_state(request: Request, exc: InvalidOrderStateError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "invalid_order_state", "message": str(exc)},
        )

    @app.exception_handler(RepositoryUnavailableError)
    async def handle_repo_unavailable(request: Request, exc: RepositoryUnavailableError) -> JSONResponse:
        logger.error("repository unavailable: %s", exc, exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"error": "service_unavailable"},
        )

    @app.exception_handler(Exception)
    async def handle_unexpected(request: Request, exc: Exception) -> JSONResponse:
        logger.error("unexpected error", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "internal_server_error"},
        )
```

### 7.2 エラーレスポンス形式

API 全体で一貫したエラー封筒を使う：

```json
{
  "error": "order_not_found",
  "message": "Order o-123 not found",
  "details": { ... }       // バリデーションエラー等で任意
}
```

Pydantic バリデーションエラーは FastAPI が自動で 422 を返す；形式を変えたいなら `@app.exception_handler(RequestValidationError)` でラップ。

### 7.3 生 `Exception` を絶対クライアントに漏らさない

§ 7.1 のキャッチオール `Exception` ハンドラが 500 と汎用メッセージを返し・トレースバックをサーバ側でログる。クライアントはスタックトレース・SQL エラー・サードパーティ SDK エラーメッセージを絶対見ない。

---

## 8. FastAPI アプリのテスト

完全パターンは `python-testing.md § 2.7` 参照。要点：

```python
def test_post_orders_returns_201() -> None:
    app = build_app(container=build_fake_container())
    client = TestClient(app)
    response = client.post("/orders", json={"customer_id": "cust-1", "line_items": [...]})
    assert response.status_code == 201
```

`build_fake_container()` はユースケースをインメモリリポジトリで配線するので、テストは routing + middleware + serialization + use case + domain logic を実行するが、実 DB・実外部 API を絶対触らない。

---

## 9. Definition of Done — FastAPI チェックリスト

エンドポイントを「完了」とする前に：

- [ ] `interface/api/routers/{resource}.py` に住む — `application/` や `domain/` ではない
- [ ] ルートボディが薄い（log・入力構築・ユースケース呼び出し・レスポンス構築）
- [ ] リクエスト・レスポンスが `schemas/` の Pydantic モデル
- [ ] 境界で識別子を値オブジェクトに変換（`OrderId(s)`）
- [ ] 非 200 レスポンスは `status_code=` 明示
- [ ] 必要なら認証依存を適用
- [ ] ルート入口で主要パラメータをログ（PII・シークレットなし）
- [ ] ドメイン例外が正しい HTTP status で `error_handlers.py` 処理（§ 7.1）
- [ ] CORS origin が明示・`*` ではない（§ 6.2）
- [ ] 起動・シャットダウンに lifespan ハンドラ使用（§ 2.3）
- [ ] エンドポイントに最低1つの `TestClient` テスト（§ 8）
