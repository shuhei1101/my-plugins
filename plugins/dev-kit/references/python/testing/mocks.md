# testing/mocks — Mock Patterns for Integration Tests

In integration tests, **mock out all external dependencies**. Because dev-kit Python injects dependencies via function type aliases, mocks are just plain functions.

---

## Basics: pass a function mock

```python
from {pkg}.features.chat.service import generate_response


async def test_generate_response_ok() -> None:
    # 関数の型 AsyncChatFn を満たす Mock
    async def chat_mock(req):
        return "mocked"

    result = await generate_response("hi", chat=chat_mock)
    assert result == "mocked"
```

You can also use `unittest.mock`'s `AsyncMock`, but **a plain function reads more clearly**.

---

## LLM mock

Make a function that satisfies the `AsyncChatFn` type:

```python
# tests/conftest.py
from typing import Awaitable, Callable
from {pkg}.integrations.llm.types import ChatRequest, ChatResponse


def make_chat_mock(*responses: str):
    """順番に固定文字列を返す LLM Mock を作る。"""
    queue = list(responses)

    async def _chat(req: ChatRequest) -> ChatResponse:
        if not queue:
            return "default"
        return queue.pop(0)

    return _chat


@pytest.fixture
def chat_simple():
    return make_chat_mock("hello world")


@pytest.fixture
def chat_sequence():
    return make_chat_mock("first", "second", "third")
```

To verify call counts / arguments, **hold a counter in a closure**:

```python
def make_chat_spy():
    calls: list[ChatRequest] = []

    async def _chat(req: ChatRequest) -> ChatResponse:
        calls.append(req)
        return "ok"

    _chat.calls = calls   # type: ignore[attr-defined]
    return _chat


async def test_chat_called_with_user_input() -> None:
    chat = make_chat_spy()
    await generate_response("hello", chat=chat)
    assert len(chat.calls) == 1
    assert chat.calls[0][0]["content"] == "hello"
```

---

## Error-injection mock

```python
from {pkg}.shared.errors import LlmRateLimitError, LlmServerError


def make_chat_error(exc: Exception):
    async def _chat(req):
        raise exc
    return _chat


@pytest.fixture
def chat_rate_limited():
    return make_chat_error(LlmRateLimitError("too many requests"))


@pytest.fixture
def chat_server_error():
    return make_chat_error(LlmServerError("500"))
```

---

## HTTP mock (httpx)

```python
import httpx
import respx


async def test_http_call(respx_mock) -> None:
    respx_mock.get("https://api.example.com/users/1").mock(
        return_value=httpx.Response(200, json={"id": "1", "name": "alice"})
    )

    async with httpx.AsyncClient() as client:
        resp = await client.get("https://api.example.com/users/1")

    assert resp.json()["name"] == "alice"
```

`respx` lets you declaratively mock httpx requests.

Alternative: if you've abstracted the HTTP fetch function with a function type alias, just substitute a mock function:

```python
type AsyncHttpFetch = Callable[[str], Awaitable[dict]]

# プロダクション実装
async def fetch_via_httpx(url: str) -> dict: ...

# Mock
async def fetch_mock(url: str) -> dict:
    return {"id": "1", "name": "alice"}

# 注入
await my_service("...", fetch=fetch_mock)
```

---

## Time mock

If you abstract time as `type NowFn = Callable[[], datetime]`, the test just passes a fixed-time function:

```python
from datetime import datetime, timezone


def now_fixed() -> datetime:
    return datetime(2026, 1, 1, tzinfo=timezone.utc)


def test_with_fixed_time() -> None:
    result = create_log_entry("hello", now=now_fixed)
    assert result.timestamp == datetime(2026, 1, 1, tzinfo=timezone.utc)
```

You can also use `freezegun`, but **function injection is simpler**.

---

## ID-generation mock

```python
type GenerateId = Callable[[], str]

ids = iter(["id-1", "id-2", "id-3"])

def gen_id_seq() -> str:
    return next(ids)


def test_create_user_assigns_id() -> None:
    user = create_user(
        CreateUserInput(name="alice", age=30),
        save=_save_user_memory,
        generate_id=gen_id_seq,
    )
    assert user.id == "id-1"
```

---

## In-memory repository mock

Our policy is not to use a DB, but if you have something persistence-like, write an in-memory function:

```python
# テスト内で使い捨ての in-memory 実装
def make_user_repo():
    storage: dict[UserId, User] = {}

    def save(user: User) -> None:
        storage[user.id] = user

    def find(id: UserId) -> User | None:
        return storage.get(id)

    return save, find


def test_create_then_find() -> None:
    save, find = make_user_repo()

    user = create_user(
        CreateUserInput(name="alice", age=30),
        save=save,
        generate_id=lambda: "u-1",
    )
    assert find("u-1") == user
```

---

## monkeypatch (env vars / module-level substitution)

```python
def test_with_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    settings = Settings()
    assert settings.openai_api_key.get_secret_value() == "sk-test"


def test_replace_function(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_now() -> datetime:
        return datetime(2026, 1, 1, tzinfo=timezone.utc)

    monkeypatch.setattr("{pkg}.shared.types.now_utc", fake_now)
    # ...
```

That said, if you **inject dependencies as arguments** at design time, monkeypatch usage stays minimal.

---

## Things you must not do

```python
# ❌ unittest.mock.patch で深い階層を直接差し替える
@patch("{pkg}.features.chat.service.chat_with_openai")
async def test_chat(mock_chat) -> None:
    mock_chat.return_value = "..."
    # ↑ 関数を引数で受ける設計にしておけば、このパッチは不要

# ❌ 本物の外部サービスに通信する結合テスト
async def test_chat_real_openai() -> None:
    result = await chat_with_openai(...)   # 課金 / 不安定 → smoke に分ける
```

---

## Related files

- `testing/strategy.md` — Integration testing policy
- `testing/pytest.md` — How to write fixtures
- `architecture/ts-style.md` — Function type alias + DI patterns
