<!-- This file is a Japanese mirror of pytest.md. When updating the English original, update this file too. -->
# testing/pytest — pytest 規約

> このファイルは `pytest.md` の日本語ミラーです。

---

## 基本設定（pyproject.toml）

```toml
[tool.pytest.ini_options]
minversion = "8.0"
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
asyncio_mode = "auto"
addopts = [
    "-ra",                # 短いサマリ
    "--strict-markers",   # 未定義 marker でエラー
    "--strict-config",
    "-W", "error",        # warning をエラーに
]
markers = [
    "smoke: real external-service tests (requires --run-smoke)",
]
```

---

## ファイル / 関数の命名

- ファイル: `test_*.py`
- 関数: `test_*()`
- クラス（任意）: `Test*` ※基本クラスは使わない、関数で書く

```python
# tests/features/chat/test_generate_response.py
import pytest

@pytest.mark.asyncio
async def test_generate_response_success() -> None: ...

@pytest.mark.asyncio
async def test_generate_response_with_empty_input() -> None: ...
```

テスト名は **「何を確認しているか」が読める英語** で書く:
- `test_generate_response_returns_text_when_llm_succeeds`
- `test_generate_response_raises_when_llm_rate_limited`
- `test_create_user_persists_to_repository`

---

## conftest.py — 共通 fixtures

```python
# tests/conftest.py
from __future__ import annotations
import pytest
from {pkg}.shared.settings import Settings


@pytest.fixture
def test_settings() -> Settings:
    """テスト用設定。env を上書き。"""
    return Settings(
        env="test",
        log_level="DEBUG",
        openai_api_key="sk-test",
        anthropic_api_key="sk-ant-test",
    )


@pytest.fixture
def freeze_time(monkeypatch: pytest.MonkeyPatch):
    """時刻を 2026-01-01 に固定する。"""
    from datetime import datetime, timezone
    fixed = datetime(2026, 1, 1, tzinfo=timezone.utc)

    def now_utc() -> datetime:
        return fixed

    monkeypatch.setattr("{pkg}.shared.types.now_utc", now_utc)
    return fixed
```

`conftest.py` は **ディレクトリ階層単位で自動ロード**される。
`tests/conftest.py` → 全テストで使える / `tests/features/conftest.py` → features/ 配下のみ。

---

## fixture の依存関係

```python
@pytest.fixture
def chat_mock_ok():
    async def _chat(req):
        return "ok response"
    return _chat


@pytest.fixture
def chat_mock_rate_limited():
    from {pkg}.shared.errors import LlmRateLimitError
    async def _chat(req):
        raise LlmRateLimitError("rate limited")
    return _chat


@pytest.mark.asyncio
async def test_success(chat_mock_ok) -> None:
    result = await generate_response("hi", chat=chat_mock_ok)
    assert result == "ok response"


@pytest.mark.asyncio
async def test_rate_limited(chat_mock_rate_limited) -> None:
    with pytest.raises(LlmRateLimitError):
        await generate_response("hi", chat=chat_mock_rate_limited)
```

---

## parametrize

複数パターンを 1 関数で:

```python
@pytest.mark.parametrize(
    "input_text, expected_len",
    [
        ("", 0),
        ("hi", 2),
        ("a" * 100, 100),
    ],
)
def test_count_chars(input_text: str, expected_len: int) -> None:
    assert count_chars(input_text) == expected_len
```

ケース名を明示したい場合:

```python
@pytest.mark.parametrize(
    "input_text, expected_len",
    [
        pytest.param("", 0, id="empty"),
        pytest.param("hi", 2, id="short"),
        pytest.param("a" * 100, 100, id="long"),
    ],
)
def test_count_chars(input_text: str, expected_len: int) -> None: ...
```

---

## pytest-asyncio

非同期関数のテストには `pytest-asyncio` を使う。
`asyncio_mode = "auto"` を設定済みなら `@pytest.mark.asyncio` を省略可能。

```python
async def test_async_thing() -> None:
    result = await some_async_fn()
    assert result == "expected"
```

---

## FastAPI ルートのテスト

`TestClient` を使った結合テスト:

```python
# tests/server/test_chat_route.py
from fastapi.testclient import TestClient
from {pkg}.server.app import build_fastapi
from {pkg}.main import Handlers, build_handlers


def test_post_chat_success() -> None:
    """POST /chat が 200 を返す。"""
    app = build_fastapi()

    # Mock を注入（テスト用 Handlers を差し込む）
    async def chat_mock(req):
        return "mocked response"

    handlers = Handlers(
        generate_response=partial(generate_response, chat=chat_mock),
        # ...
    )
    app.state.handlers = handlers

    with TestClient(app) as client:
        response = client.post("/chat", json={"user_input": "hi"})

    assert response.status_code == 200
    assert response.json()["text"] == "mocked response"
```

---

## マーカーの付け方

```python
import pytest

pytestmark = pytest.mark.smoke   # ファイル全体に


@pytest.mark.slow                # 関数単位
def test_heavy() -> None: ...


@pytest.mark.skipif(
    not has_gpu(),
    reason="requires GPU",
)
def test_gpu_only() -> None: ...
```

選択実行:

```bash
uv run pytest -m "not smoke"   # smoke 以外
uv run pytest -m "smoke"       # smoke だけ
```

---

## デバッグ tips

```bash
# 1 つだけ走らせる
uv run pytest tests/features/chat/test_generate_response.py::test_success -v

# print を表示する（デフォルト捕捉されている）
uv run pytest -s

# 失敗時に pdb 起動
uv run pytest --pdb

# 最初の失敗で止める
uv run pytest -x
```

---

## 関連ファイル

- `testing/テスト戦略.md` — テストの種類と方針
- `testing/モック.md` — Mock の作り方
- `packaging/pyproject設定.md` — pytest 設定の完全例
