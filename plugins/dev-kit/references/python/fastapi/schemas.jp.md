<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# fastapi/schemas — 入出力 Pydantic スキーマ

> このファイルは `schemas.md` の日本語ミラーです。

FastAPI のリクエスト / レスポンスは Pydantic で。内部 DTO（`@dataclass`）とは分離する。

---

## なぜ分離するか

- **API 互換**: 外部 API スキーマは凍結したい。内部 DTO は自由にリファクタしたい
- **検証ルール**: API は外部入力検証が厳しい（max length 等）。内部は信頼前提でもよい
- **公開フィールドの選択**: 内部 DTO の全フィールドを公開したくないことがある
- **シリアライズ形式**: snake_case 内部 / camelCase 外部などの差を吸収

---

## 配置

```
features/chat/
├── types.py            # 内部 DTO（@dataclass）+ 関数型
├── schemas.py          # 外部 Pydantic（route で使う）
├── route.py
└── service.py
```

または、規模が小さければ `types.py` 1 つにまとめてもよい。

---

## サンプル

```python
# src/{pkg}/features/chat/schemas.py
from __future__ import annotations
from pydantic import BaseModel, Field
from .types import ChatRequest as DomainChatRequest, ChatResult as DomainChatResult


class ChatRequest(BaseModel):
    """POST /chat のリクエストボディ。"""

    user_input: str = Field(min_length=1, max_length=1000, description="ユーザー入力テキスト")
    session_id: str | None = Field(default=None, description="会話セッション ID。新規なら省略")

    def to_domain(self) -> DomainChatRequest:
        """API スキーマ → 内部 DTO へ変換。"""
        return DomainChatRequest(
            text=self.user_input,
            session_id=self.session_id,
        )


class ChatResponse(BaseModel):
    """POST /chat のレスポンス。"""

    text: str = Field(description="LLM レスポンス本文")
    session_id: str = Field(description="セッション ID（新規生成された場合は新値）")
    tokens_used: int = Field(ge=0, description="このリクエストで使用したトークン数")

    @classmethod
    def from_domain(cls, result: DomainChatResult) -> ChatResponse:
        """内部 DTO → API スキーマへ変換。"""
        return cls(
            text=result.text,
            session_id=result.session_id,
            tokens_used=result.tokens,
        )
```

---

## `to_domain` / `from_domain` のメソッド

両方向の変換を **スキーマクラスのメソッドで定義** すると、route はワンライナーになる:

```python
# route.py
@router.post("", response_model=ChatResponse)
async def post_chat(body: ChatRequest, request: Request) -> ChatResponse:
    handlers = request.app.state.handlers
    result = await handlers.chat(body.to_domain())
    return ChatResponse.from_domain(result)
```

---

## Field 制約

| 制約 | 用途 |
|---|---|
| `min_length` / `max_length` | 文字列長 |
| `ge` / `le` / `gt` / `lt` | 数値範囲 |
| `pattern` | 正規表現 |
| `default` / `default_factory` | デフォルト値 |
| `description` | OpenAPI 用説明 |
| `examples` | OpenAPI のサンプル値 |

```python
class CreateUserRequest(BaseModel):
    name: str = Field(min_length=1, max_length=20, description="ユーザー表示名")
    email: str = Field(pattern=r"^[\w.+-]+@[\w-]+\.[\w.-]+$", description="メールアドレス")
    age: int = Field(ge=0, le=150)
    bio: str | None = Field(default=None, max_length=500)
```

---

## カスタムバリデーション

```python
from pydantic import field_validator, model_validator


class CreateUserRequest(BaseModel):
    name: str
    age: int

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if v.strip() != v:
            raise ValueError("name must not have leading/trailing spaces")
        return v

    @model_validator(mode="after")
    def validate_consistency(self) -> CreateUserRequest:
        # 複数フィールド横断の検証
        if self.age < 0 and self.name == "admin":
            raise ValueError("admin must have non-negative age")
        return self
```

ValidationError は FastAPI が 422 にマップしてくれる。

---

## camelCase ⇔ snake_case

API が camelCase を要求する場合:

```python
from pydantic import ConfigDict


class ChatRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=_to_camel)

    user_input: str = Field(alias="userInput")
    session_id: str | None = Field(default=None, alias="sessionId")


def _to_camel(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(p.title() for p in parts[1:])
```

ただし、フロント側で snake_case を受け入れられるなら **そのまま** が一番楽。

---

## レスポンスの整形

`response_model=` を渡すと FastAPI が:
- 余計なフィールドを削る
- 型を検証
- OpenAPI スキーマに反映

```python
@router.get("/users/{id}", response_model=UserResponse)
async def get_user(id: str) -> User:   # 内部 DTO を返す
    return await fetch_user(id, find=...)
    # ↑ FastAPI が User → UserResponse に勝手に変換
```

ただし、明示変換のほうが読みやすいことが多い:

```python
@router.get("/users/{id}", response_model=UserResponse)
async def get_user(id: str) -> UserResponse:
    user = await fetch_user(id, find=...)
    return UserResponse.from_domain(user)
```

---

## 列挙型（enum / Literal）

```python
from typing import Literal


class CreatePostRequest(BaseModel):
    title: str
    status: Literal["draft", "published"] = "draft"
    visibility: Literal["public", "private", "friends"] = "public"
```

OpenAPI に enum として出る。型チェッカーも厳密に判定できる。

---

## やってはいけないこと

```python
# ❌ 内部 DTO（@dataclass）を直接 route で使う
@router.post("")
async def post_chat(body: DomainChatRequest):   # NG
    # Pydantic でないので検証が動かない

# ❌ dict / list を route 引数に使う
@router.post("/data")
async def post_data(body: dict): ...   # NG（型なし）

# ❌ from_domain / to_domain を route 関数内に書き散らす
@router.post("")
async def post_chat(body):
    domain = DomainChatRequest(text=body.user_input, session_id=body.session_id)
    # ↑ schemas.py に書く
```

---

## 関連ファイル

- `fastapi/routes.md` — schemas を使った route 実装
- `architecture/ts-style.md` — 内部 DTO (@dataclass) のスタイル
- `core/comments.md` — フィールド description
