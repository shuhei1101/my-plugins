# Python Core Standards — py-kit

Baseline conventions for all Python work. Read this for every Python task.

---

## Naming Conventions

| Target | Convention | Example |
|---|---|---|
| Module / file | `snake_case` | `user_repository.py` |
| Class | `PascalCase` | `UserRepository` |
| Function / method | `snake_case` | `find_by_id()` |
| Variable | `snake_case` | `user_id` |
| Constant | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| Private | leading `_` | `_internal_cache` |
| Protocol / Interface | `{Name}able` (preferred), `I{Name}`, or `Base{Name}` — pick one per project | `Convertable`, `IConverter`, `BaseConverter` |
| Implementation | `{impl}_{name}.py` | `ffmpeg_converter.py` |

---

## Comment Rules

Write **why**, never what. Code already says what.

- Good: `# CP932 parses bat files — Japanese UTF-8 bytes become lead bytes and swallow following chars`
- Bad: `# Calls setup_logger`

One short line max. No multi-paragraph blocks, no docstrings that restate the signature.

Exception: module-level docstrings for scripts (see `python-scripts.md`).

---

## Type Hints

Apply everywhere — function arguments, return types, class fields. No bare `Any`.

```python
from typing import Literal, Optional, Protocol, TypeVar
from collections.abc import Sequence

def process(items: Sequence[str], mode: Literal["fast", "slow"]) -> list[str]: ...
```

Use `Protocol` for structural interfaces (preferred over `ABC` for new code):

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Convertable(Protocol):
    def convert(self, source: str) -> str: ...
```

Use `ABC` only when shared default implementations are needed.

---

## Language Rules

- **English only**: all `print()` and `logger` output (bat files render Japanese as garbage in CP932)
- **Japanese allowed**: code comments, `.env.sample` comments, GUI display strings
