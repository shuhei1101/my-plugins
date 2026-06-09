---
paths:
  - "**/features/**/types.py"
  - "**/features/**/service.py"
  - "**/features/**/query.py"
  - "**/features/**/client.py"
  - "**/integrations/**/client.py"
---
<!-- This file is a Japanese mirror of TypeScriptスタイル適用.md. When updating the English original, update this file too. -->
# TypeScript 風 Python — 関数ファースト設計

dev-kit Python の中心ドキュメント。**関数ファースト + 型エイリアス + DTO + Protocol** で TypeScript の主要機能を Python で再現する。

---

## 基本原則

1. **関数ファースト**: 振る舞いは **モジュールレベルの関数**。クラスは DTO とライブラリ要求時のみ
2. **DTO + 関数**: データは `@dataclass` / `BaseModel` / `TypedDict`、振る舞いは関数
3. **型エイリアスで関数の型を定義**: `type FindUser = Callable[[UserId], User | None]`
4. **Protocol で構造的型付け**: 複数メソッド/属性をまとめるとき
5. **`@overload` は限定使用**: ほぼ不要

---

## クラスを使う条件（限定）

クラスを書いて OK なのは以下のみ:

1. **DTO**（不変データコンテナ）: `@dataclass(frozen=True, slots=True, kw_only=True)` または `pydantic.BaseModel`
2. **ライブラリが強要するもの**: FastAPI Middleware、Pydantic BaseModel 継承、CLI Command クラス、Enum など
3. **長期保持のランタイム状態**: DB 接続プール、WebSocket セッション

それ以外（サービスロジック、Repository、Provider、Validator 等）は**すべて関数で書く**。

---

## 推奨スタイルの完全サンプル

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

クラスは 1 つも出てこない。DTO は `@dataclass`、すべて関数 + 型エイリアスで構成。

---

## 型エイリアスで「関数の型」を定義 + DI

外部依存（LLM API、TTS、HTTP client、DB 等）は **関数の型エイリアス** で抽象化し、引数で受け取る:

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

**注入する関数を切り替えるだけで本物 / モックが切り替わる**。
クラスベース DI（Repository クラス・Provider クラス）より圧倒的に軽量。

---

## Protocol で構造的型付け

複数メソッド/属性をまとめたい場合は `Protocol` を使う。**継承不要**（duck typing）。

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

`@runtime_checkable` を付ければ `isinstance(obj, LlmClient)` も可能。

---

## インターフェース抽象化の 3 段階

| 段階 | パターン | 用途 |
|---|---|---|
| 1. 単純関数 1 つ | `type FindUser = Callable[[UserId], User \| None]` | 1 機能の差し替え |
| 2. 複数メソッド/属性 | `Protocol` | クラス的 API の抽象化 |
| 3. 戻り値が引数型で分岐 | `@overload`（稀） | パラメトリック関数 |

「クラスを継承させて差し替え」は **やらない**。継承の概念は使わず、duck typing で済ます。

---

## DTO の使い分け（早見表）

| 用途 | 推奨 | 理由 |
|---|---|---|
| 外部 HTTP リクエスト/レスポンス | `pydantic.BaseModel` | ランタイム検証必要 |
| 設定（.env / YAML / TOML） | `pydantic_settings.BaseSettings` | 検証 + env 読み込み |
| LLM 構造化出力（Instructor） | `pydantic.BaseModel` | Instructor 要求 |
| CLI 引数（argparse 後の構造体） | `pydantic.BaseModel` | 検証あり |
| 関数間の内部 DTO（軽量） | `@dataclass(frozen=True, slots=True, kw_only=True)` | 軽量・型安全 |
| 関数の引数オブジェクト | `@dataclass` | 軽量、`__init__` 自動 |
| 一時的な dict 型付け（JSON 由来） | `TypedDict` | dict のまま扱える |
| 構造的型付け（duck typing） | `Protocol` | 継承不要 |
| ライブラリが要求する継承先 | そのライブラリの基底 | やむなし |

### Pydantic vs dataclass vs TypedDict 補足

- **Pydantic**: 動作はやや重い（検証あり）。**外部境界**に使う
- **dataclass**: 軽量。**内部 DTO** に使う。`frozen=True, slots=True, kw_only=True` で安全性 + 速度
- **TypedDict**: 実体は `dict`。型チェッカー用。**JSON データをそのまま扱う**時に便利
  - `json.dumps(user)` がそのまま使える
  - `dict.get()` / `dict.update()` も使える
  - メソッドは生やせない

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

## Pick / Omit 相当（規約化しない）

TypeScript の `Pick` / `Omit` 相当は Python に直接ない。必要な時の選択肢:

- **Pydantic**: `model_dump(exclude={"password"})` で実質 Omit、継承で Pick / Extend
- **dataclass**: 別 dataclass を手書きで定義
- **TypedDict**: `class UserPublic(TypedDict): id: str; name: str`

DB を使わない方針なので入出力境界の派生型は少ない。**その都度判断** でよい。

---

## ハンドラーデコレータ（例外横断）

例外キャッチや retry / timeout は関数デコレータで束ねる:

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

実装例は `core/型ヒント.md` の Recommended Decorators 節を参照。

---

## `@overload`（限定使用）

戻り値が引数型で分岐する関数のみ:

```python
from typing import overload, Literal

@overload
def parse(value: Literal["int"]) -> int: ...
@overload
def parse(value: Literal["str"]) -> str: ...
def parse(value: str) -> int | str:
    return 0 if value == "int" else ""
```

ほとんどのケースでは型エイリアス + Callable / Protocol で済む。

---

## 関連ファイル

- `architecture/レイアウト.md` — フォルダ構成
- `architecture/コンポジションルート.md` — main.py で関数を partial で配線する方法
- `architecture/依存パッケージ管理.md` — 依存方向と DIP
- `core/命名規則.md` — 型エイリアス命名規約
- `core/型ヒント.md` — PEP 695 / ハンドラーデコレータ / `assert_never`
