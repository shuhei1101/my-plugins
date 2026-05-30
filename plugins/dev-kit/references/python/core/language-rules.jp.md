<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# 言語ルール

> このファイルは `language-rules.md` の日本語ミラーです。

---

## 文字種・言語の使い分け

| 対象 | 言語 |
|---|---|
| コメント / docstring | **日本語** |
| 識別子（変数 / 関数 / 型 / モジュール） | **英語** |
| `print()` / `logger.info()` の出力文字列 | **英語** |
| bat / sh / PowerShell スクリプトの出力 | **英語** |
| エラーメッセージ（例外 `raise` 時） | **英語** |
| UI 表示文字列 / ユーザー向けメッセージ | **日本語**（必要なら） |

理由:
- ログは grep / 共有 / 検索しやすいよう英語
- コメントは「設計意図」の共有なので日本語が読みやすい
- 文字エンコーディング事故（CP932 等）を避けるため、文字列は ASCII 範囲が望ましい

---

## 文字列フォーマット

f-string（`f"..."`）を標準にする。

```python
# ✅ 標準
logger.info(f"user {user_id} created, took {elapsed_ms}ms")

# ❌ % フォーマット（古い）
logger.info("user %s created" % user_id)

# ❌ .format()（冗長）
logger.info("user {} created".format(user_id))
```

例外: 国際化（i18n）が必要な場合のみ `gettext` ベースの記法。

`logger` の構造化引数（extra）と f-string は使い分ける:

```python
# 検索性重視 → 構造化引数
logger.info("user_created", extra={"user_id": user_id, "elapsed_ms": elapsed_ms})

# 一目で読みたい開発ログ → f-string
logger.debug(f"trying provider {provider_name}")
```

---

## import の並び

ruff の `I` ルール（isort 互換）に従って自動整理する。グループ:

1. **`from __future__ import ...`**（最初に必ず）
2. **標準ライブラリ**
3. **サードパーティライブラリ**
4. **自パッケージ（`{pkg}.*`）**

各グループ間に空行 1 つ。

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

## 例外階層

すべてのドメイン例外は `AppError` を継承する:

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

詳細は `shared/errors.md`。

### ベストプラクティス

- **広い `except Exception:` は禁止**（ハンドラーデコレータ / 最上位ハンドラ以外）
- vendor 例外（`anthropic.APIError`、`httpx.HTTPError` 等）は `IntegrationError` 系にラップ
- 例外メッセージは英語 1 行で書く
- `raise X from e` で原因例外を必ず連鎖

```python
try:
    response = await anthropic_client.messages.create(...)
except anthropic.APIError as e:
    raise LlmError(f"anthropic call failed: {e}") from e
```

---

## エラーハンドリング方針

- **Result 型 / Either は使わない**（Python 標準的でない）
- 例外を普通に投げる
- 横断関心事（ログ・リトライ・タイムアウト・例外変換）は **ハンドラーデコレータ**で束ねる（`core/type-hints.md` 参照）
- 最上位（main / FastAPI exception_handler）で `AppError` を catch して適切に処理

---

## ロギングの基本姿勢

- `print` ではなく `logger` を使う
- ログレベル運用:
  - `logger.debug(...)` 開発時のみ
  - `logger.info(...)` 業務イベント（リクエスト受領、ユースケース完了）
  - `logger.warning(...)` 想定内エラー（retry で吸収できるもの）
  - `logger.error(...)` 想定外エラー（人間が見るべき）
  - `logger.critical(...)` プロセス継続不能
- 詳細は `shared/logger.md`

---

## ファイルエンコーディング

すべて UTF-8。BOM なし。

Windows で bat / sh / 設定ファイルを読み書きする場合は `encoding="utf-8"` を明示:

```python
config_text = Path("config.yaml").read_text(encoding="utf-8")
```

---

## 関連ファイル

- `shared/errors.md` — 例外階層の詳細
- `shared/logger.md` — ログ運用
- `core/type-hints.md` — ハンドラーデコレータの実装例
