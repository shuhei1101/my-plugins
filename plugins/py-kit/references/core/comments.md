# Comment Rules

Apply the same philosophy as next-kit's `frontend/conventions/comments.md` to Python.

---

## Language

Write comments in **Japanese**:
- Descriptions of functions / types / DTOs (docstrings)
- Descriptions of arguments / fields (the important ones)
- Block comments (labels for processing sections)
- Section markers
- Change history comments (PR number + intent)

Identifiers (variable / function / type names) stay in English.

---

## Required / Recommended Matrix

| Target | Comment required? | Form |
|---|---|---|
| Functions / types exported via `__init__.py` | Required | 1-line docstring |
| Public functions (not starting with `_`) | Required | 1-line docstring (multi-line if important) |
| Internal functions (starting with `_`) | Recommended | docstring optional; required if complex |
| **Design-significant** fields of Pydantic / dataclass | Required | `Field(description=...)` or `# ` inline comment |
| Ordinary (self-evident) fields | Not needed | — |
| Related statement blocks | Recommended | `# ` single-line label |
| Self-evident single lines | Not needed | — |
| Change history (PR number + intent) | Allowed | `# PR{N}: {what changed / why}` |
| TODO / FIXME | Allowed | Issue number required (`# TODO(#123): ...`) |

Since we write code with AI as a collaborator, **err on the side of more comments**. When AI reads it later, it gets the same benefit as a human.

---

## Pattern 1: Function docstring

Always give public functions / types a 1-line docstring.

```python
def create_user(input: CreateUserInput, *, save: SaveUser) -> User:
    """ユーザーを新規作成し、永続化する。"""
    ...

def find_user_by_id(id: UserId, *, find: FindUser) -> User | None:
    """ユーザーを ID で検索する。見つからなければ None。"""
    ...
```

When multi-line is needed, put a summary on line 1, a blank line, then details:

```python
def calculate_score(user: User, items: list[Item]) -> int:
    """ユーザーの累計スコアを計算する。

    プレミアム会員は基本点 +20%、購入回数が 10 を超えた items は対象外。
    """
    ...
```

Do not write JSDoc-style annotations like `@param` / `@returns` / `@type`.
The signature carries the types. **Write only the purpose.**

---

## Pattern 2: Descriptions of Design-Significant Fields

Criteria for "design-significant" (same as next-kit):
- Foreign keys / ID references
- Status-style enums / Literals
- Business-meaningful flags (public / archived / deleted, etc.)
- Optimistic-lock columns
- Audit columns (creator, updater, timestamps)
- Fields with business-complex meaning

### Pydantic

```python
from pydantic import BaseModel, Field
from typing import Literal

class CreateUserInput(BaseModel):
    name: str = Field(min_length=1, max_length=20)
    age: int = Field(ge=0, le=150)
    is_public: bool = Field(
        default=False,
        description="公開フラグ。true なら全ユーザーから閲覧可能",
    )
    status: Literal["draft", "published", "archived"] = Field(
        default="draft",
        description="ステータス。draft=下書き、published=公開、archived=非表示",
    )
```

### dataclass

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True, kw_only=True)
class CreateUserInput:
    name: str
    age: int
    # 公開フラグ — true なら全ユーザーから閲覧可能
    is_public: bool = False
    # ステータス — draft=下書き、published=公開、archived=非表示
    status: str = "draft"
```

### TypedDict

```python
from typing import TypedDict, NotRequired

class UserDict(TypedDict):
    id: str
    name: str
    # オプションフィールド — 未指定なら年齢不明
    age: NotRequired[int]
```

---

## Pattern 3: Block Comments (Processing Sections)

Inside a longer function, label logical blocks with `# ` single-line comments.

```python
async def handle_chat(input: ChatInput, *, chat: AsyncChatFn) -> ChatOutput:
    """ユーザー入力を LLM に投げ、レスポンスを整形して返す。"""

    # 入力の前処理
    cleaned = _strip_control_chars(input.text)
    messages = _build_messages(cleaned, input.history)

    # LLM 呼び出し
    raw = await chat(messages)

    # 後処理（Markdown 除去 + 文字数制限）
    text = _strip_markdown(raw)
    return ChatOutput(text=text[:MAX_RESPONSE_LEN])
```

---

## Pattern 4: Change History Comments

Record in one line any change whose intent cannot be read from the code. Japanese, with PR number.

```python
# PR123: 年齢上限フィールドを追加。要件 #45 対応。
age_upper: int | None = None

# PR101: 旧 calculate() を廃止し新仕様に統一。互換性のため null チェックを追加。
if value is None:
    return 0

# PR132: API ステータスを 200 → 204 に変更（フロントは互換）
return Response(status_code=204)
```

### When to write

- Intent that disappears from the code (compatibility shims, rare business cases)
- API / schema changes that affect external callers
- Transitional code intentionally left for a while
- Bug fixes whose root cause cannot be traced from the code

### When not to write

- Renames / formatting
- Behavior-preserving refactors
- Logging "every line you touched" — that's `git log`'s job

If 5+ history comments accumulate, consider consolidating them at the top of the file under a `# History:` block, or splitting them into a CHANGELOG.

---

## Pattern 5: TODO / FIXME

`TODO:` is unfinished work. Include enough context that someone can pick it up later.
**Issue number required** (to link to project management).

```python
# TODO(#123): コメントテーブル作成後に有効化する
# pinned_comment_id: UserId | None = None

# TODO(PR133): 子供が複数いる場合の選択 UI を追加
child_id = children[0].id if children else None
```

`FIXME:` is a known bug that must be fixed before merge / release.

```python
# FIXME(#234): age_from が None のとき NaN になる
age_diff = age_to - age_from
```

---

## What Not to Write

```python
# ❌ コードを言い換えただけ
# user_id を取得する
user_id = user.id

# ❌ 自明な動作
# state を更新する
is_open = True
```

```python
# ✅ 隠れた制約を説明する
# IME 入力中は Enter を無視する（変換確定キーと競合するため）
if event.key == "Enter" and not is_composing:
    handle_submit()

# ✅ 関数の目的
def select_family_quests(*, db: Db, family_id: FamilyId, page: int) -> list[Quest]:
    """家族 ID でクエストを絞り込み、ページネーションして返す。"""
    ...
```

---

## Constraints Summary

- Public functions / types / DTOs must have a 1-line docstring
- Design-significant fields on Pydantic / dataclass must be described
- Logical blocks of long functions should be labeled with `# `
- Change history comments only for non-obvious changes, 1 line in Japanese, with PR number
- TODO / FIXME require an issue / PR number
- Do not write `@param` / `@returns` / `@type` (leave to type hints)
- Do not repeat what the code already says
- `git log` is the primary change history

---

## Related Files

- `core/naming.md` — naming conventions
- `core/type-hints.md` — how to write type hints
- `architecture/ts-style.md` — concrete examples of DTO definitions
