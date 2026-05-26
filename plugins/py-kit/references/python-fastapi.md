# Python FastAPI Standards — py-kit

Conventions for FastAPI projects. Read together with `python-core.md` and `python-architecture.md`.

---

## Project Structure

```
{package_name}/
├── interface/
│   └── api/
│       ├── routers/         # one file per resource group
│       │   ├── users.py
│       │   └── orders.py
│       ├── dependencies.py  # FastAPI Depends() factories
│       └── middleware.py    # CORS, auth, logging middleware
├── application/             # use cases (no FastAPI imports here)
├── domain/                  # entities, Protocols, value objects
└── infrastructure/          # DB, external API adapters
```

---

## Endpoint Design

- One router file per resource group (`users.py`, `orders.py`)
- Route functions are thin — call use case, return response model
- No business logic inside route functions
- Use Pydantic models for request bodies and response schemas

```python
@router.post("/users", response_model=UserResponse, status_code=201)
async def create_user(body: CreateUserRequest, use_case: CreateUserUseCase = Depends(get_create_user)) -> UserResponse:
    return await use_case.execute(body)
```

---

## Dependency Injection

Use FastAPI `Depends()` to inject use cases and repositories:

```python
def get_user_repository() -> UserRepository:
    return PostgresUserRepository(get_db_connection())

def get_create_user(repo: UserRepository = Depends(get_user_repository)) -> CreateUserUseCase:
    return CreateUserUseCase(repo)
```

Never instantiate use cases or repositories directly inside route functions.

---

## Common Middleware

- **CORS**: always configure explicitly — no wildcard `*` in production
- **Auth**: JWT verification as a `Depends()` function, not middleware
- **Logging**: log request method + path + status code + duration at INFO level
- **Error handling**: use `@app.exception_handler` for domain exceptions → HTTP status mapping

---

## Startup / Shutdown

Use `lifespan` context manager (preferred over deprecated `on_event`):

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await db.connect()
    yield
    # shutdown
    await db.disconnect()

app = FastAPI(lifespan=lifespan)
```

---

## Run and Deployment

For local development (Windows): see `python-scripts.md` → FastAPI run.bat Template

For production: run with `uvicorn {package_name}.__main__:app --host 0.0.0.0 --port {PORT}`
