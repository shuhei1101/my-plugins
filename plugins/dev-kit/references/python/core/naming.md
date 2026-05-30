# Naming Conventions

## Basic Rules

| Target | Rule | Example |
|---|---|---|
| Module / file | `snake_case` | `user_service.py`, `open_ai_client.py` |
| Function (public or internal) | `snake_case` | `create_user`, `find_user_by_id` |
| Internal-only function / module | Leading `_` | `_validate_input`, `_helpers.py` |
| Exported identifier (via `__init__.py`) | Normal name | `from .service import create_user` |
| Identifier to hide | `_` prefix | `_internal_state` |
| Type alias (`type X = ...`) | `UpperCamel` | `UserId`, `CreateUserInput`, `FindUser` |
| dataclass / Pydantic class | `UpperCamel` | `User`, `CreateUserInput` |
| Protocol | `UpperCamel` (no prefix) | `UserFinder`, `AsyncChatFn` (verb-based allowed) |
| Constant | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| TypeVar / generic param | Single uppercase letter or `UpperCamel + T` | `T`, `K`, `V`, `UserT` |

### Notes

- **Do not prefix Protocol names with `I`** (avoid Java-style `IUserFinder`)
- **Verb-based type alias names** are allowed: `AsyncChatFn`, `SaveUser`, `FindUser`
  - When used as a function type alias, a verb name makes the purpose clearer
- Identifier type aliases (`UserId`, `OrderId`, etc.) should be **nouns**

---

## Standard File Names Inside a feature Folder

Inside a feature folder `{pkg}/{feature}/`, the following names are recommended as the **standard pattern**.
For a small feature, `types.py` + `service.py` alone is fine.

| File name | Role |
|---|---|
| `__init__.py` | Re-export of public symbols (e.g. `from .service import create_user`) |
| `types.py` | Type aliases + DTOs + Protocols (the place for type definitions inside the feature) |
| `query.py` | Read-side functions (`find_*`, `list_*`, `get_*`) |
| `service.py` | Business logic functions (`create_*`, `update_*`, `delete_*`, composite operations) |
| `route.py` | HTTP handlers (FastAPI router; only when the server / feature is exposed over the web) |
| `client.py` | External API call functions (used mainly under `integrations/`) |
| `db.py` | Persistence operations (only when DB is used; not generally needed under the new policy) |
| `prompts/` | Prompt files (only for LLM features, as a subfolder) |
| `_helpers.py` | Helpers used only inside the feature |

The point is not "put all of these" but "**when you use this name, use it for this role**."

### Function Name Verb Prefixes

| Prefix | Use | Return value |
|---|---|---|
| `create_*` | Create new | The entity created |
| `update_*` | Update | The updated entity or `None` |
| `delete_*` | Delete | `None` |
| `find_*` | Search for one | `Entity \| None` |
| `get_*` | Get one (assumed to always exist) | `Entity` (raise if not found) |
| `list_*` | Get many | `list[Entity]` |
| `search_*` | Conditional search (many) | `list[Entity]` |

---

## Module Paths and "Public API"

- Each feature explicitly exports public symbols via `__init__.py`
- Do not let outsiders reach internals directly like `from {pkg}.features.chat.service import _internal_helper`
- Prefix functions / variables you want to keep private with `_`

```python
# {pkg}/features/chat/__init__.py
from .service import generate_response
from .types import ChatRequest, ChatResponse

__all__ = ["generate_response", "ChatRequest", "ChatResponse"]
```

---

## Related Files

- `architecture/layout.md` — overall feature folder structure conventions
- `core/comments.md` — docstring policy that goes with naming
- `architecture/ts-style.md` — concrete examples of type alias naming
