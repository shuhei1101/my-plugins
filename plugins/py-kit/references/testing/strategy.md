# testing/strategy — Testing Policy

py-kit's policy: **do not write unit tests.** Write only two kinds of tests: integration tests and smoke tests.

---

## Kinds of tests we use

| Kind | Purpose | Execution |
|---|---|---|
| **Integration tests** | Per use case, test the whole path: route → service → branches → result, as one unit. External dependencies (LLM, TTS, HTTP, time, etc.) are **mocked** | Automatic in CI / during development |
| **Smoke tests** | Verify **real connections** to external services (real LLM API, real TTS, etc.) | Manual execution by the user only. **Forbidden** to run automatically in CI / by AI |

**Do not write unit tests (tests against a single function).**

---

## Why we don't write unit tests

- AI-driven development is the premise, and the design treats **source code as the primary spec** that can be read at a glance.
- The cost of turning a single function's behavior into a test is high relative to the small reassurance it provides.
- Refactors break tests first (even when the spec hasn't changed).
- Integration tests are more directly tied to user value (closer to how the code is actually used).

Instead, we **cover this through design**:
- Function-first + type aliases create function boundaries that are easy to test.
- Integration tests let us spin through "the whole use case" quickly.
- Type checking (mypy / pyright strict) guarantees method-level correctness.

---

## Granularity of integration tests

One test file per use case.
Verify end-to-end that "a request came in → the service ran → the expected result was produced."

```python
# tests/features/chat/test_generate_response.py
import pytest
from {pkg}.features.chat.service import generate_response


@pytest.mark.asyncio
async def test_generate_response_success() -> None:
    """通常入力に対して LLM レスポンスが返る。"""
    async def chat_mock(req):
        return "hello world"

    result = await generate_response("hi", chat=chat_mock)

    assert result == "hello world"


@pytest.mark.asyncio
async def test_generate_response_strips_markdown() -> None:
    """LLM の返答から Markdown が除去される。"""
    async def chat_mock(req):
        return "**bold** text"

    result = await generate_response("hi", chat=chat_mock)

    assert "**" not in result
```

Key points:
- **External dependencies (`chat`) are injected as mocks**
- One file per use case; put multiple branches as parallel `test_*` functions
- Consolidate setup in fixtures (`conftest.py`)

---

## File layout

```
tests/
├── __init__.py
├── conftest.py                  # 共通 fixtures
├── features/
│   ├── chat/
│   │   ├── test_generate_response.py
│   │   └── test_save_message.py
│   └── users/
│       └── test_create_user.py
├── server/
│   └── test_chat_route.py       # FastAPI ルートの結合テスト（TestClient）
└── smoke/                       # スモーク（実接続）
    ├── conftest.py              # スモーク用 fixtures
    ├── test_openai_live.py
    └── test_anthropic_live.py
```

Mirror the feature structure with `tests/{feature}/test_{usecase}.py`.

---

## Running integration tests

```bash
uv run pytest tests/ -v --ignore=tests/smoke/
```

Exclude `tests/smoke/` in CI.

---

## Running smoke tests

Smoke tests are **guarded by an explicit flag**:

```python
# tests/smoke/conftest.py
import pytest

def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--run-smoke",
        action="store_true",
        default=False,
        help="run smoke tests against real external services",
    )


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if not config.getoption("--run-smoke"):
        skip = pytest.mark.skip(reason="need --run-smoke")
        for item in items:
            if "smoke" in item.keywords or "smoke" in str(item.fspath):
                item.add_marker(skip)
```

Run with:

```bash
uv run pytest tests/smoke/ --run-smoke
```

Only runs when the user explicitly passes `--run-smoke`.
**AI must not run this automatically** (external APIs incur charges).

---

## What goes in a smoke test

```python
# tests/smoke/test_openai_live.py
import pytest
import os
from {pkg}.integrations.llm.openai_client import chat_with_openai


pytestmark = pytest.mark.smoke


@pytest.mark.asyncio
async def test_openai_smoke() -> None:
    """OpenAI API への実接続が成立し、200 系で文字列が返ることを確認する。"""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY not set")

    result = await chat_with_openai(
        [{"role": "user", "content": "say hi in one word"}],
        api_key=api_key,
        model="gpt-4o-mini",
    )

    assert isinstance(result, str)
    assert len(result) > 0
```

Just confirm "the API works." **Do not verify business logic here** (that belongs in integration tests).

---

## Coverage

If using `pytest-cov`:

```bash
uv run pytest --cov={pkg} --cov-report=term-missing tests/ --ignore=tests/smoke/
```

That said, **do not lock yourself in to a coverage-percentage target**.
Make a qualitative judgment about whether the important use cases are covered by integration tests.

---

## Related files

- `testing/pytest.md` — pytest conventions, fixtures
- `testing/mocks.md` — Mock patterns for integration tests
- `architecture/ts-style.md` — Substitution via function type aliases
