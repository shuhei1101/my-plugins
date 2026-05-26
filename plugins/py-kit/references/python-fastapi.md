# Python FastAPI Standards — py-kit

Conventions for FastAPI projects. Read together with `python-core.md` and
`python-architecture.md`. This file assumes the pure-DDD layout from
`python-architecture.md § 8` — FastAPI lives in `interface/api/`.

---

## 1. Where FastAPI Fits in the DDD Layout

FastAPI is an interface-layer technology. It does **not** belong in `domain/`
or `application/`. Routers translate HTTP into use case calls and translate
use case results back into HTTP responses.

```
{pkg}/interface/api/
├── __init__.py
├── main.py                  # creates the FastAPI app, wires routers + middleware
├── routers/
│   ├── __init__.py
│   ├── orders.py
│   ├── customers.py
│   └── health.py
├── dependencies.py          # FastAPI Depends() factories — pull from the Container
├── middleware.py            # CORS / auth / logging / error-mapping middleware
├── error_handlers.py        # @app.exception_handler functions
└── schemas/                 # Pydantic models for request bodies and responses
    ├── __init__.py
    ├── order_request.py
    └── order_response.py
```

The Container (`{pkg}/main.py`) is wired before the app is constructed; routers
get use cases out of the Container via `Depends(...)`.

---

## 2. App Construction

### 2.1 `build_app(container)` Pattern

The app factory takes the Container so tests can swap in a fake one.

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
        # startup
        container.logger.info("API starting on port %s", container.settings.port)
        yield
        # shutdown
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
        allow_origins=container.settings.cors_allowed_origins,  # explicit, never ["*"]
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

### 2.2 `__main__.py` Entry Point

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
        log_config=None,    # use our logger, not uvicorn's
        access_log=False,   # we log via RequestLoggingMiddleware
    )


if __name__ == "__main__":
    run()
```

### 2.3 Lifespan — Replaces Deprecated `@app.on_event`

Use `lifespan` (since FastAPI 0.93+). Do not use `@app.on_event("startup")` /
`@app.on_event("shutdown")` — they are deprecated.

```python
# ✅ Good
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await db.connect()
    yield
    # shutdown
    await db.disconnect()

app = FastAPI(lifespan=lifespan)

# ❌ Bad — deprecated
@app.on_event("startup")
async def startup() -> None:
    await db.connect()
```

---

## 3. Routers

### 3.1 One Router File per Resource

| Resource | File |
|---|---|
| `/orders/*` | `routers/orders.py` |
| `/customers/*` | `routers/customers.py` |
| `/users/*` | `routers/users.py` |
| `/health` | `routers/health.py` |

Cross-resource endpoints (`/admin/dashboard`, `/me/feed`) get their own file
named after the feature, not the resource.

### 3.2 Router Module Template

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

### 3.3 Route Function Rules (Hard)

| Rule | Reason |
|---|---|
| Route functions are **thin** — at most: log, build use case input, call use case, build response | Business logic belongs in the use case |
| No business logic, no calls to repositories or external SDKs in route bodies | Route functions are an interface concern |
| Request body type = a Pydantic model in `schemas/` | Validation at the boundary |
| Response type = a Pydantic model in `schemas/` (via `response_model=` or annotation) | Serialization shape is explicit |
| Path parameters are converted to value objects at the boundary | `OrderId(order_id)`, not raw `str` |
| `status_code=` is set explicitly when not 200 | Avoid accidental 200s for creates / deletes |
| `logger.info` once per route entry (after auth, with key params, no PII) | Audit trail; debuggability |

### 3.4 Route Naming and HTTP Verbs

| Action | Verb | Path | Status code on success |
|---|---|---|---|
| Create | `POST` | `/orders` | 201 |
| Read one | `GET` | `/orders/{id}` | 200 |
| Read list | `GET` | `/orders` | 200 |
| Replace whole | `PUT` | `/orders/{id}` | 200 |
| Partial update | `PATCH` | `/orders/{id}` | 200 |
| Delete | `DELETE` | `/orders/{id}` | 204 |
| Action (non-CRUD) | `POST` | `/orders/{id}/cancel` | 200 (or 204 if no body) |

Never use `GET` for state-changing operations. Never use `POST` for read-only queries.

### 3.5 Query Parameters and Pagination

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

Cursor-based pagination is preferred for any list that may grow beyond a few hundred items; page-based is acceptable for small admin tables.

---

## 4. Dependency Injection via `Depends()`

### 4.1 Pulling Use Cases out of the Container

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

Routers never call repositories or instantiate use cases — they only resolve them via `Depends`.

### 4.2 Auth Dependency

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

Then on routes that require auth:

```python
@router.post("", response_model=OrderResponse)
async def create_order(
    body: CreateOrderRequest,
    user: User = Depends(current_user),
    use_case: CreateOrderUseCase = Depends(get_create_order),
) -> OrderResponse:
    ...
```

### 4.3 Per-Request DB Session (When Using a Synchronous ORM)

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

For async ORMs (asyncpg, async SQLAlchemy) the pattern is the same with `async with` / `await`.

---

## 5. Pydantic Schemas

### 5.1 One File per Resource, Request and Response Separated

```
schemas/
├── order_request.py    # CreateOrderRequest, UpdateOrderRequest, ...
├── order_response.py   # OrderResponse, OrderListResponse, OrderSummaryResponse
└── ...
```

### 5.2 Request Schema Pattern

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

### 5.3 Response Schema Pattern

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

### 5.4 Schema Rules

| Rule | Reason |
|---|---|
| Request schemas have `Field(...)` constraints (min/max, length, ranges) | Validates at boundary, before any business logic runs |
| Response schemas have a `from_domain()` classmethod | Single place that maps domain → wire format |
| Schemas use `str` for identifiers, not `NewType` value objects | Pydantic doesn't auto-handle `NewType`; convert in `to_domain_*` methods |
| No business logic in `to_domain_*` / `from_domain` beyond field translation | Validation is the schema's job; business logic is the use case's |
| Reuse: nested Pydantic models (`LineItemRequest`) for repeated structures | Single source of truth for the wire shape |

---

## 6. Middleware

### 6.1 Request Logging Middleware

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

### 6.2 CORS — Never `*` in Production

```python
# ✅ Good — explicit list from settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,  # ["https://app.example.com"]
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-Request-Id"],
)

# ❌ Bad — wildcard in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # blocks `allow_credentials=True` anyway
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

If you need wildcard for local development, gate it on the environment:

```python
allow_origins = ["*"] if settings.env == "local" else settings.cors_allowed_origins
```

### 6.3 Auth Middleware vs Auth Dependency

| Pattern | When to use |
|---|---|
| `Depends(current_user)` on each route | Most apps — explicit per-route |
| Auth middleware that populates `request.state.user` | When 95%+ of routes require the same auth — and you have a clean public-route allowlist |

Prefer the dependency pattern — it's explicit and visible at the route signature.

---

## 7. Error Handling

### 7.1 Domain Exception → HTTP Status Mapping

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

### 7.2 Error Response Shape

Use a consistent error envelope across the API:

```json
{
  "error": "order_not_found",
  "message": "Order o-123 not found",
  "details": { ... }       // optional, for validation errors
}
```

Pydantic validation errors are handled automatically by FastAPI (422); wrap them
if you want a different shape via `@app.exception_handler(RequestValidationError)`.

### 7.3 Never Let Raw `Exception` Leak to the Client

The catch-all `Exception` handler in § 7.1 returns 500 with a generic message
and logs the full traceback server-side. The client never sees stack traces,
SQL errors, or third-party SDK error messages.

---

## 8. Testing FastAPI Apps

See `python-testing.md § 2.7` for the full pattern. Quick recap:

```python
def test_post_orders_returns_201() -> None:
    app = build_app(container=build_fake_container())
    client = TestClient(app)
    response = client.post("/orders", json={"customer_id": "cust-1", "line_items": [...]})
    assert response.status_code == 201
```

`build_fake_container()` wires use cases against in-memory repositories so the
test exercises routing + middleware + serialization + use case + domain logic,
but never touches a real DB or external API.

---

## 9. Definition of Done — FastAPI Checklist

Before considering an endpoint "done":

- [ ] Lives in `interface/api/routers/{resource}.py` — not in `application/` or `domain/`
- [ ] Route body is thin (log + build input + call use case + build response)
- [ ] Request and response are Pydantic models in `schemas/`
- [ ] Identifiers converted to value objects at the boundary (`OrderId(s)`)
- [ ] `status_code=` set explicitly for non-200 responses
- [ ] Auth dependency applied where required
- [ ] Logger logs request entry with key params (no PII / secrets)
- [ ] Domain exceptions handled in `error_handlers.py` with correct HTTP status (§ 7.1)
- [ ] CORS origins explicit, not `*` (§ 6.2)
- [ ] Lifespan handler used for startup / shutdown (§ 2.3)
- [ ] At least one `TestClient` test for the endpoint (§ 8)
