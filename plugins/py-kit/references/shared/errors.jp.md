<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# errors — 例外階層

> このファイルは `errors.md` の日本語ミラーです。

すべてのドメイン例外は **`AppError` を継承** する単一階層にする。

---

## 階層

```python
# src/{pkg}/shared/errors.py
from __future__ import annotations


class AppError(Exception):
    """アプリケーション共通の例外基底クラス。"""


# ----- 入力・検証 -----
class ValidationError(AppError):
    """入力検証エラー。"""


# ----- 業務状態 -----
class NotFoundError(AppError):
    """対象が見つからない。"""


class ConflictError(AppError):
    """状態競合（重複・整合性違反・楽観ロック失敗等）。"""


class ForbiddenError(AppError):
    """操作が許可されていない（権限不足）。"""


# ----- 認証・認可 -----
class UnauthorizedError(AppError):
    """未認証 / 認証失敗。"""


# ----- 外部連携 -----
class IntegrationError(AppError):
    """外部サービス連携の包括エラー。"""


class IntegrationTimeoutError(IntegrationError):
    """外部サービス連携でタイムアウト。"""


# ----- LLM 個別 -----
class LlmError(IntegrationError):
    """LLM API 由来のエラー。"""


class LlmRateLimitError(LlmError):
    """レート制限超過。"""


class LlmServerError(LlmError):
    """LLM サーバ側のエラー（5xx）。"""


class LlmBadRequestError(LlmError):
    """LLM リクエストが不正（4xx）。"""


class LlmContentFilterError(LlmError):
    """コンテンツフィルタによる拒否。"""
```

---

## 設計原則

1. **すべて `AppError` を継承**: 最上位で `except AppError:` 1 つで全業務例外を捕まえられる
2. **vendor 例外はラップする**: `anthropic.APIError`、`httpx.HTTPError` などは直接外に流さず、`LlmError` / `IntegrationError` に変換
3. **メッセージは英語 1 行**: ログの一貫性のため
4. **`raise X from e` で原因連鎖**: 必ず原因例外を保持

---

## vendor 例外のラップ

```python
# {pkg}/integrations/llm/openai_client.py
import openai
from {pkg}.shared.errors import LlmError, LlmRateLimitError, LlmServerError


async def chat_with_openai(req: ChatRequest) -> ChatResponse:
    try:
        response = await _client.chat.completions.create(...)
    except openai.RateLimitError as e:
        raise LlmRateLimitError(f"openai rate limit: {e}") from e
    except openai.APIStatusError as e:
        if 500 <= e.status_code < 600:
            raise LlmServerError(f"openai 5xx: {e}") from e
        raise LlmError(f"openai api error: {e}") from e
    except openai.APITimeoutError as e:
        raise IntegrationTimeoutError(f"openai timeout: {e}") from e
    return response.choices[0].message.content or ""
```

これにより:
- features / server レイヤは `LlmError` 系だけ知っていればよい
- vendor を入れ替えても features 側のコードは変わらない
- リトライ判定が型で書ける（`except LlmRateLimitError:` なら待って retry）

---

## HTTP エラーへのマッピング（FastAPI）

```python
# src/{pkg}/server/app.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from {pkg}.shared.errors import (
    AppError, ValidationError, NotFoundError, ConflictError,
    ForbiddenError, UnauthorizedError, IntegrationError,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ValidationError)
    async def _(_: Request, e: ValidationError):
        return JSONResponse({"error": str(e)}, status_code=400)

    @app.exception_handler(UnauthorizedError)
    async def _(_: Request, e: UnauthorizedError):
        return JSONResponse({"error": str(e)}, status_code=401)

    @app.exception_handler(ForbiddenError)
    async def _(_: Request, e: ForbiddenError):
        return JSONResponse({"error": str(e)}, status_code=403)

    @app.exception_handler(NotFoundError)
    async def _(_: Request, e: NotFoundError):
        return JSONResponse({"error": str(e)}, status_code=404)

    @app.exception_handler(ConflictError)
    async def _(_: Request, e: ConflictError):
        return JSONResponse({"error": str(e)}, status_code=409)

    @app.exception_handler(IntegrationError)
    async def _(_: Request, e: IntegrationError):
        return JSONResponse({"error": "external service error"}, status_code=502)

    @app.exception_handler(AppError)
    async def _(_: Request, e: AppError):
        # それ以外の AppError は 500 扱い
        return JSONResponse({"error": str(e)}, status_code=500)
```

詳細は `fastapi/auth-and-errors.md`。

---

## CLI での処理

```python
# src/{pkg}/__main__.py
import sys
from {pkg}.shared.errors import AppError, ValidationError
from {pkg}.shared.logger import get_logger

logger = get_logger(__name__)

def main() -> int:
    try:
        ...
        return 0
    except ValidationError as e:
        logger.error(f"validation failed: {e}")
        return 2
    except AppError as e:
        logger.exception("app error")
        return 1
    except Exception as e:
        logger.exception("unexpected error")
        return 99


if __name__ == "__main__":
    sys.exit(main())
```

---

## ハンドラーデコレータで横断的に処理

`core/type-hints.md` のハンドラーデコレータと組み合わせる:

```python
@catch_and_map(openai.RateLimitError, to=LlmRateLimitError)
@catch_and_map(openai.APIStatusError, to=LlmError)
async def chat_with_openai(req: ChatRequest) -> ChatResponse:
    response = await _client.chat.completions.create(...)
    return response.choices[0].message.content or ""
```

---

## やってはいけないこと

```python
# ❌ 広い except Exception で握りつぶす
try:
    ...
except Exception:
    pass   # NG

# ❌ str を raise する
raise "user not found"   # NG（必ず例外クラスをインスタンス化）

# ❌ from を付けずに raise
try:
    ...
except SomeError as e:
    raise AppError("failed")   # NG（原因が失われる）

# ✅ from で連鎖
except SomeError as e:
    raise AppError("failed") from e
```

---

## 関連ファイル

- `core/language-rules.md` — 例外メッセージは英語
- `core/type-hints.md` — ハンドラーデコレータ
- `llm/exceptions-retry.md` — LLM 例外階層とリトライ
- `fastapi/auth-and-errors.md` — FastAPI での exception_handler
