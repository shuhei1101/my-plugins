# Refactoring Judgment Criteria

Judgment criteria for "when to DRY", "when to abstract", and "when to externalize settings".

---

## DRY judgment — how many times before consolidating

| Trigger | Action |
|---|---|
| First time | Just write it |
| **Second time (copy-paste occurs)** | **Start considering consolidation** (if small, turn it into a function / constant on the spot) |
| Third time | **Always consolidate**. Move to `_helpers.py` / `shared/utils.py` / a function type alias |
| Found at the fourth occurrence or later | A missed consolidation. Highest priority to fix |

Decision helpers:
- The moment "I'm about to write another one by copy-paste" is the signal to consolidate
- If the logic is ≥ 3 lines and a candidate for reuse, turn it into a function
- For 1–2 line identical expressions, **inline duplication is fine** (cases where the cost of consolidation exceeds the benefit)

---

## Abstraction judgment — when to introduce a Protocol / type alias

| Situation | Action |
|---|---|
| Only one implementation exists | **Do not abstract** (YAGNI) |
| A **second implementation** is visible / a test Mock is needed | Introduce a function type alias (`Callable`) |
| **Three or more implementations** exist or the behavior is complex | Introduce a `Protocol` |
| The extension point is clear (a new provider is already planned) | Abstract via a type alias from the start |

The cost of adding an abstraction is "the readers having to chase one more type jump". Ask every time whether it is really needed.

Detailed patterns are in the "Three stages of interface abstraction" section of `architecture/ts-style.md`.

---

## Externalization judgment — when to take values out of code

| Kind | Location | Examples |
|---|---|---|
| **Values you want to change per environment** | `.env` / `settings.py` | API keys, model names, host names |
| **Fixed values referenced from multiple files** | `shared/constants.py` | `PROJECT_ROOT`, `MAX_RETRY_COUNT` |
| **Business-fixed choices** | `Literal[...]` or `StrEnum` | statuses, categories |
| **Long text / multi-column / multilingual** | Files like `prompts/*.md` | LLM prompts, templates |
| **Values the streamer / non-engineers touch** | YAML / `settings.yaml` | display labels, screen parameters |

See also `shared/secrets-and-env.md`.

Decision helpers:
- "I want to change the value without changing code" → put it in settings
- "Multiple files reference the same value" → make it a constant
- "A number / string literal carries meaning" → give it a name (no magic numbers)

---

## File splitting judgment — when to split a file

| Situation | Action |
|---|---|
| 1 file ~200 lines | OK |
| 1 file 200–400 lines | Consider splitting by content (by role: types / service / query / route, etc.) |
| 1 file 400 lines or more | **Splitting recommended**. Split by role or by feature |
| 5 or more section markers (`# ===`) | Signal to split |

For references (`*.md`):
- From the perspective of "do not include unnecessary information" at the hook-injection unit, split finely
- Principle of one topic per reference. If multiple topics exist, split

---

## Things you must not do

```python
# ❌ 1 回目で抽象化（過剰設計）
class AbstractUserService(Protocol):
    def find(self, id: str) -> User | None: ...

class UserServiceImpl:   # ← 実装が 1 個しかないのに Protocol を切らない
    ...

# ❌ 3 回コピペしたまま放置
def parse_a(raw): return int(raw.strip().replace(",", ""))
def parse_b(raw): return int(raw.strip().replace(",", ""))
def parse_c(raw): return int(raw.strip().replace(",", ""))   # → 共通化必須

# ❌ マジックナンバー
if user.age > 18:   # 18 とは何か？ MIN_ADULT_AGE = 18 へ
    ...

# ❌ 設定値をコードに直書き
OPENAI_MODEL = "gpt-4o-mini"   # → settings.py で env 切替可能に
```

---

## Related files

- `architecture/design-principles.md` — the priority of DRY > SOLID > extensibility
- `architecture/ts-style.md` — abstraction patterns (type aliases / Protocol / overload)
- `shared/secrets-and-env.md` — secret boundaries + placement of settings values
- `shared/constants.md` — where to put constants
