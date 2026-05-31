<!-- This file is a Japanese mirror of Instructor.md. When updating the English original, update this file too. -->
# llm/instructor — Instructor + Pydantic で構造化出力

> このファイルは `Instructor.md` の日本語ミラーです。

LLM の出力を Pydantic モデルとして受け取るには [Instructor](https://python.useinstructor.com/) を使う。
スキーマ検証 + リトライが組み込まれている。

---

## セットアップ

```bash
uv add instructor pydantic
```

OpenAI クライアントを `instructor` でラップする:

```python
# src/{pkg}/integrations/llm/structured_client.py
from __future__ import annotations
import instructor
from openai import AsyncOpenAI


def make_structured_openai(api_key: str) -> instructor.AsyncInstructor:
    """構造化出力対応の OpenAI クライアントを作る。"""
    raw_client = AsyncOpenAI(api_key=api_key)
    return instructor.from_openai(raw_client, mode=instructor.Mode.TOOLS)
```

Anthropic 版:

```python
import anthropic

def make_structured_anthropic(api_key: str) -> instructor.AsyncInstructor:
    raw_client = anthropic.AsyncAnthropic(api_key=api_key)
    return instructor.from_anthropic(raw_client, mode=instructor.Mode.ANTHROPIC_TOOLS)
```

---

## Pydantic スキーマで受け取る

```python
# src/{pkg}/features/extract/types.py
from pydantic import BaseModel, Field
from typing import Literal


class ExtractedEvent(BaseModel):
    """ニュース記事から抽出したイベント情報。"""

    title: str = Field(description="イベント名（簡潔に）")
    date: str = Field(description="開催日（YYYY-MM-DD 形式）")
    location: str = Field(description="開催場所")
    category: Literal["concert", "exhibition", "sports", "other"]
    confidence: float = Field(ge=0.0, le=1.0, description="抽出の確信度")
```

---

## 抽出関数

```python
# src/{pkg}/features/extract/service.py
from __future__ import annotations
import instructor
from {pkg}.features.extract.types import ExtractedEvent


async def extract_event(
    article: str,
    *,
    client: instructor.AsyncInstructor,
    model: str = "gpt-4o-mini",
) -> ExtractedEvent:
    """記事本文からイベント情報を抽出する。"""
    return await client.chat.completions.create(
        model=model,
        response_model=ExtractedEvent,
        messages=[
            {"role": "system", "content": "次のニュース記事からイベント情報を抽出してください。"},
            {"role": "user", "content": article},
        ],
        max_retries=3,    # 検証失敗時にリトライ
    )
```

`response_model=ExtractedEvent` を渡すだけで:
- LLM 出力を JSON で受ける
- Pydantic で検証
- 検証失敗時は LLM に修正させて再試行（`max_retries`）

---

## 配線

```python
# src/{pkg}/main.py
from functools import partial
from {pkg}.integrations.llm.structured_client import make_structured_openai
from {pkg}.features.extract.service import extract_event


def build_handlers(settings: Settings) -> Handlers:
    structured = make_structured_openai(settings.openai_api_key.get_secret_value())

    return Handlers(
        extract_event=partial(extract_event, client=structured, model=settings.openai_model),
    )
```

---

## バリデーションエラーをハンドリング

```python
from pydantic import ValidationError
from {pkg}.shared.errors import LlmError


async def extract_event_safe(
    article: str,
    *,
    client: instructor.AsyncInstructor,
) -> ExtractedEvent | None:
    """検証失敗時は None を返す。"""
    try:
        return await extract_event(article, client=client)
    except ValidationError as e:
        logger.warning(f"validation failed: {e}")
        return None
    except LlmError:
        raise
```

---

## ネストしたスキーマ

```python
class Speaker(BaseModel):
    name: str
    affiliation: str | None = None


class ConferenceEvent(BaseModel):
    title: str
    date: str
    speakers: list[Speaker] = Field(description="登壇者一覧")
    topics: list[str]
```

LLM が複雑な構造を一発で出してくれる。

---

## Streaming with structured output

```python
async for partial in client.chat.completions.create_partial(
    model="gpt-4o-mini",
    response_model=ExtractedEvent,
    messages=[...],
):
    print(partial)   # 部分的に埋まったオブジェクトが yield される
```

UI で逐次表示するのに便利。

---

## Task-specific client パターン

LLM を「ある特定タスクに特化した関数」として封じる:

```python
# 関数の型エイリアス
type ExtractEventFn = Callable[[str], Awaitable[ExtractedEvent]]


def make_extract_event_fn(
    *,
    client: instructor.AsyncInstructor,
    model: str,
) -> ExtractEventFn:
    """記事 → ExtractedEvent の関数を作って返す。"""
    async def fn(article: str) -> ExtractedEvent:
        return await extract_event(article, client=client, model=model)
    return fn
```

呼び出し側は `client` も `model` も知らなくていい:

```python
extract = make_extract_event_fn(client=structured, model="gpt-4o-mini")

# 使う時は記事だけ渡せばよい
result = await extract("...article text...")
```

---

## プロンプトとスキーマを 1 ファイルにまとめる

```python
# src/{pkg}/features/extract/event_extractor.py
from __future__ import annotations
import instructor
from pydantic import BaseModel, Field
from typing import Literal


# ----- スキーマ -----
class ExtractedEvent(BaseModel):
    title: str
    date: str
    category: Literal["concert", "exhibition", "sports", "other"]


# ----- プロンプト（短いものはコード内、長ければ prompts/ に） -----
_SYSTEM = "ニュース記事から構造化されたイベント情報を抽出してください。"


# ----- 関数 -----
async def extract_event(
    article: str,
    *,
    client: instructor.AsyncInstructor,
    model: str = "gpt-4o-mini",
) -> ExtractedEvent:
    return await client.chat.completions.create(
        model=model,
        response_model=ExtractedEvent,
        messages=[
            {"role": "system", "content": _SYSTEM},
            {"role": "user", "content": article},
        ],
        max_retries=3,
    )
```

タスクが小さければ 1 ファイルで完結。スキーマ・プロンプト・関数を 1 セットで読める。

---

## 関連ファイル

- `llm/プロバイダー.md` — 素のチャット呼び出し（非構造化）
- `llm/prompts.md` — 長いプロンプトの管理
- `llm/例外とリトライ.md` — リトライ戦略
- `architecture/TypeScriptスタイル適用.md` — task-specific 関数の型設計
