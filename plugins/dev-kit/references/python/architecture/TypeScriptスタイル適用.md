# TypeScript-Style Python — Function-First Design

The central document of dev-kit Python. Reproduce TypeScript's core features in Python with **function-first + type aliases + DTOs + Protocols**.

---

## Basic principles

1. **Function-first**: Behavior lives in **module-level functions**. Classes only for DTOs and when libraries require them
2. **DTOs + functions**: Data is `@dataclass` / `BaseModel` / `TypedDict`; behavior is functions
3. **Define function types via type aliases**: `type FindUser = Callable[[UserId], User | None]`
4. **Protocols for structural typing**: When grouping multiple methods/attributes
5. **`@overload` used sparingly**: Almost never needed

---

## Conditions for using a class (limited)

You may write a class only in these cases:

1. **DTOs** (immutable data containers): `@dataclass(frozen=True, slots=True, kw_only=True)` or `pydantic.BaseModel`
2. **Library-mandated**: FastAPI Middleware, Pydantic BaseModel subclassing, CLI Command classes, Enum, etc.
3. **Long-lived runtime state**: DB connection pool, WebSocket session

Everything else (service logic, Repository, Provider, Validator, etc.) **must be written as functions**.

---

## Complete sample of the recommended style

```python
# src/{pkg}/features/users/types.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable

# ----- 識別子型エイリアス -----
type UserId = str

# ----- DTO（軽量・不変） -----
@dataclass(frozen=True, slots=True, kw_only=True)
class CreateUserInput:
    """ユーザー新規作成の入力。"""
    name: str
    age: int

@dataclass(frozen=True, slots=True, kw_only=True)
class User:
    """ユーザー DTO。"""
    id: UserId
    name: str
    age: int

# ----- 関数の型エイリアス -----
type FindUser = Callable[[UserId], User | None]
type SaveUser = Callable[[User], None]
type DeleteUser = Callable[[UserId], None]
type GenerateUserId = Callable[[], UserId]
```

```python
# src/{pkg}/features/users/service.py
from __future__ import annotations
from .types import CreateUserInput, User, SaveUser, GenerateUserId

def create_user(
    input: CreateUserInput,
    *,
    save: SaveUser,
    generate_id: GenerateUserId,
) -> User:
    """ユーザーを新規作成し、永続化する。"""
    user = User(id=generate_id(), name=input.name, age=input.age)
    save(user)
    return user
```

```python
# src/{pkg}/features/users/query.py
from __future__ import annotations
from .types import UserId, User, FindUser

def find_user_by_id(id: UserId, *, find: FindUser) -> User | None:
    """ユーザーを ID で検索する。"""
    return find(id)
```

```python
# src/{pkg}/features/users/_in_memory.py（実装の 1 つ）
from __future__ import annotations
from .types import UserId, User

_users: dict[UserId, User] = {}

def save_user_in_memory(user: User) -> None:
    _users[user.id] = user

def find_user_in_memory(id: UserId) -> User | None:
    return _users.get(id)
```

Not a single class appears. DTOs are `@dataclass`, everything is composed of functions + type aliases.

---

## Defining "function types" with type aliases + DI

External dependencies (LLM API, TTS, HTTP client, DB, etc.) are abstracted as **function-type aliases** and received as arguments:

```python
# src/{pkg}/integrations/llm/types.py
from __future__ import annotations
from typing import Awaitable, Callable

type ChatRequest = list[dict[str, str]]
type ChatResponse = str
type AsyncChatFn = Callable[[ChatRequest], Awaitable[ChatResponse]]
type SyncChatFn = Callable[[ChatRequest], ChatResponse]
```

```python
# src/{pkg}/integrations/llm/openai_client.py
async def chat_with_openai(req: ChatRequest) -> ChatResponse:
    """OpenAI Chat API を呼び出す。"""
    ...

# src/{pkg}/integrations/llm/mock_client.py
async def chat_with_mock(req: ChatRequest) -> ChatResponse:
    """テスト用 Mock。固定文字列を返す。"""
    return "[mocked response]"
```

```python
# src/{pkg}/features/chat/service.py
from {pkg}.integrations.llm.types import AsyncChatFn

async def generate_response(
    user_input: str,
    *,
    chat: AsyncChatFn,     # ← 型で受ける。実装は注入
) -> str:
    """ユーザー入力に対する LLM レスポンスを生成する。"""
    return await chat([{"role": "user", "content": user_input}])
```

```python
# 呼び出し側（main.py）
from functools import partial
from {pkg}.integrations.llm.openai_client import chat_with_openai
from {pkg}.features.chat.service import generate_response

chat = partial(chat_with_openai)  # 必要なら api_key 等の固定引数もここで埋める
wired_generate = partial(generate_response, chat=chat)

# テストでは
from {pkg}.integrations.llm.mock_client import chat_with_mock
wired_generate_test = partial(generate_response, chat=chat_with_mock)
```

**You switch between real / mock just by swapping the injected function.**
Vastly lighter than class-based DI (Repository classes, Provider classes).

---

## Structural typing with Protocol

When you want to group multiple methods/attributes, use `Protocol`. **No inheritance required** (duck typing).

```python
# {pkg}/integrations/llm/types.py
from __future__ import annotations
from typing import Protocol, Awaitable

class LlmClient(Protocol):
    """LLM クライアントの構造的型。"""
    async def chat(self, messages: list[dict[str, str]]) -> str: ...
    async def embed(self, text: str) -> list[float]: ...
```

```python
# {pkg}/integrations/llm/openai_client.py
class OpenAiClient:
    """OpenAI 実装。LlmClient Protocol を満たす（継承宣言不要）。"""
    async def chat(self, messages: list[dict[str, str]]) -> str: ...
    async def embed(self, text: str) -> list[float]: ...

# 別ファイル / 別実装も Protocol を満たすので注入可能
class ClaudeClient:
    async def chat(self, messages: list[dict[str, str]]) -> str: ...
    async def embed(self, text: str) -> list[float]: ...
```

```python
# 関数側は Protocol で受ける
async def analyze(text: str, *, client: LlmClient) -> Analysis: ...

await analyze("hello", client=OpenAiClient())   # OK
await analyze("hello", client=ClaudeClient())   # OK
```

If you add `@runtime_checkable`, `isinstance(obj, LlmClient)` becomes possible too.

---

## Three levels of interface abstraction

| Level | Pattern | Use case |
|---|---|---|
| 1. A single simple function | `type FindUser = Callable[[UserId], User \| None]` | Swap a single capability |
| 2. Multiple methods/attributes | `Protocol` | Abstracting a class-like API |
| 3. Return type branches on argument type | `@overload` (rare) | Parametric functions |

"Swap implementations via class inheritance" is **not done**. Don't use the inheritance concept; rely on duck typing.

---

## DTO selection (quick reference)

| Use case | Recommended | Reason |
|---|---|---|
| External HTTP request/response | `pydantic.BaseModel` | Runtime validation required |
| Settings (.env / YAML / TOML) | `pydantic_settings.BaseSettings` | Validation + env loading |
| LLM structured output (Instructor) | `pydantic.BaseModel` | Required by Instructor |
| CLI args (post-argparse struct) | `pydantic.BaseModel` | Validation provided |
| Internal DTO between functions (lightweight) | `@dataclass(frozen=True, slots=True, kw_only=True)` | Lightweight, type-safe |
| Function argument object | `@dataclass` | Lightweight, auto `__init__` |
| Temporary dict typing (JSON-derived) | `TypedDict` | Keep using as a dict |
| Structural typing (duck typing) | `Protocol` | No inheritance required |
| Library-required base class | That library's base class | Unavoidable |

### Pydantic vs dataclass vs TypedDict notes

- **Pydantic**: Slightly heavy (does validation). Use at **external boundaries**
- **dataclass**: Lightweight. Use for **internal DTOs**. `frozen=True, slots=True, kw_only=True` gives safety + speed
- **TypedDict**: Underlying value is `dict`. For type-checker use. Handy **when handling JSON data as-is**
  - `json.dumps(user)` works directly
  - `dict.get()` / `dict.update()` are usable
  - Cannot define methods

```python
from typing import TypedDict, NotRequired

class UserDict(TypedDict):
    id: str
    name: str
    age: NotRequired[int]   # オプション

user: UserDict = {"id": "u1", "name": "alice"}
print(user["id"])
user["age"] = 30
```

---

## Pick / Omit equivalents (no formal convention)

Python has no direct equivalent of TypeScript's `Pick` / `Omit`. Options when needed:

- **Pydantic**: `model_dump(exclude={"password"})` for de facto Omit; inheritance for Pick / Extend
- **dataclass**: Hand-write a separate dataclass
- **TypedDict**: `class UserPublic(TypedDict): id: str; name: str`

Since the policy is to avoid DBs, derived types at I/O boundaries are few. **Decide case-by-case**.

---

## Handler decorators (cross-cutting exceptions)

Exception handling, retry, and timeout are bundled via function decorators:

```python
@catch_and_log(ValueError, level="warning")
def parse_input(raw: str) -> Input: ...

@catch_and_map(anthropic.APIStatusError, to=LlmServerError)
async def call_claude(messages: list[Message]) -> str: ...

@with_retry(times=3, backoff=0.5)
async def fetch_external(url: str) -> dict: ...

@with_timeout(seconds=60)
async def long_running(...) -> None: ...
```

See the Recommended Decorators section in `core/型ヒント.md` for implementation examples.

---

## `@overload` (limited use)

Only for functions whose return type branches on argument type:

```python
from typing import overload, Literal

@overload
def parse(value: Literal["int"]) -> int: ...
@overload
def parse(value: Literal["str"]) -> str: ...
def parse(value: str) -> int | str:
    return 0 if value == "int" else ""
```

In most cases, type aliases + Callable / Protocol suffice.

---

## Related files

- `architecture/レイアウト.md` — Folder structure
- `architecture/コンポジションルート.md` — How to wire functions with partial in main.py
- `architecture/依存パッケージ管理.md` — Dependency direction and DIP
- `core/命名規則.md` — Type alias naming conventions
- `core/型ヒント.md` — PEP 695 / handler decorators / `assert_never`
