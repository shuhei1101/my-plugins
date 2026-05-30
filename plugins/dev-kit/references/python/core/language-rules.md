# Language Rules

---

## Choice of Character Set / Language

| Target | Language |
|---|---|
| Comments / docstrings | **Japanese** |
| Identifiers (variable / function / type / module) | **English** |
| Output strings of `print()` / `logger.info()` | **English** |
| Output of bat / sh / PowerShell scripts | **English** |
| Error messages (when `raise`-ing exceptions) | **English** |
| UI display strings / user-facing messages | **Japanese** (when needed) |

Reasons:
- Logs are easier to grep / share / search when in English
- Comments express "design intent", which is more readable in Japanese
- To avoid character-encoding accidents (CP932, etc.), strings should preferably stay in ASCII range

---

## String Formatting

Use f-strings (`f"..."`) as the standard.

```python
# ✅ 標準
logger.info(f"user {user_id} created, took {elapsed_ms}ms")

# ❌ % フォーマット（古い）
logger.info("user %s created" % user_id)

# ❌ .format()（冗長）
logger.info("user {} created".format(user_id))
```

Exception: use `gettext`-style notation only when internationalization (i18n) is required.

Distinguish between `logger`'s structured arguments (extra) and f-strings:

```python
# 検索性重視 → 構造化引数
logger.info("user_created", extra={"user_id": user_id, "elapsed_ms": elapsed_ms})

# 一目で読みたい開発ログ → f-string
logger.debug(f"trying provider {provider_name}")
```

---

## Import Ordering

Sort automatically with ruff's `I` rule (isort-compatible). Groups:

1. **`from __future__ import ...`** (always first)
2. **Standard library**
3. **Third-party libraries**
4. **Own package (`{pkg}.*`)**

One blank line between each group.

```python
from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

import httpx
from pydantic import BaseModel, Field

from mypkg.shared.logger import get_logger
from mypkg.features.chat.types import ChatRequest

if TYPE_CHECKING:
    from mypkg.shared.types import UserId

logger = get_logger(__name__)
```

---

## Exception Hierarchy

All domain exceptions inherit from `AppError`:

```python
# {pkg}/shared/errors.py
class AppError(Exception):
    """アプリケーション共通の例外基底クラス。"""

class ValidationError(AppError):
    """入力検証エラー。"""

class NotFoundError(AppError):
    """対象が見つからない。"""

class ConflictError(AppError):
    """状態競合（重複・不整合）。"""

class UnauthorizedError(AppError):
    """認証 / 認可エラー。"""

class IntegrationError(AppError):
    """外部サービス連携エラー（ネットワーク / 外部 API）。"""

class LlmError(IntegrationError):
    """LLM API 由来のエラー。"""

class LlmRateLimitError(LlmError):
    """LLM のレート制限超過。"""
```

See `shared/errors.md` for details.

### Best Practices

- **Broad `except Exception:` is forbidden** (except inside handler decorators / top-level handlers)
- Wrap vendor exceptions (`anthropic.APIError`, `httpx.HTTPError`, etc.) into the `IntegrationError` family
- Write exception messages as a single line in English
- Always chain the cause with `raise X from e`

```python
try:
    response = await anthropic_client.messages.create(...)
except anthropic.APIError as e:
    raise LlmError(f"anthropic call failed: {e}") from e
```

---

## Error Handling Policy

- **Do not use Result / Either types** (not Pythonic standard)
- Just raise exceptions normally
- Bundle cross-cutting concerns (logging, retry, timeout, exception mapping) into **handler decorators** (see `core/type-hints.md`)
- Catch `AppError` at the top level (main / FastAPI exception_handler) and handle appropriately

---

## Basic Logging Stance

- Use `logger` rather than `print`
- Log level usage:
  - `logger.debug(...)` development only
  - `logger.info(...)` business events (request received, use case completed)
  - `logger.warning(...)` expected errors (absorbed by retry, etc.)
  - `logger.error(...)` unexpected errors (a human should look)
  - `logger.critical(...)` process cannot continue
- See `shared/logger.md` for details

---

## File Encoding

All UTF-8. No BOM.

On Windows, when reading/writing bat / sh / config files, specify `encoding="utf-8"` explicitly:

```python
config_text = Path("config.yaml").read_text(encoding="utf-8")
```

---

## Related Files

- `shared/errors.md` — details of the exception hierarchy
- `shared/logger.md` — logging operations
- `core/type-hints.md` — implementation examples of handler decorators
