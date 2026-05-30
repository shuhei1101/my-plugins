# Design Principle Priorities

The basic priority order when judging code additions and refactoring.

---

## Priority

1. **DRY (Don't Repeat Yourself)** — **highest priority**
2. **SOLID** — important (especially `I` Interface Segregation and `L` Liskov)
3. **Extensibility awareness** — do not strictly enforce YAGNI; allow proactive abstraction

### DRY — highest priority

- Do not write the same logic, data, or structure in **two or more places**
- When you are about to write the second occurrence, first consider consolidation
- However, do not over-abstract "for the third occurrence and beyond" (the guideline of **abstract only after writing it three times** is in `refactoring-judgement.md`)
- Inline duplication (the same calculation, the same if-chain, the same dict-key enumeration) is the top priority target for DRY consolidation

### SOLID — important

- **S (Single Responsibility)**: ensure that a single function / module does not change for multiple reasons
- **O (Open/Closed)**: open for extension, closed for modification (important when adding a new feature / new provider)
- **L (Liskov Substitution)**: once you abstract via a Protocol, implementations must be **structurally equivalent** (return type / exception contract / scope of side effects)
- **I (Interface Segregation)**: do not build a giant Protocol. Split it small per purpose (separate `AsyncChatFn` and `EmbedFn` into different types)
- **D (Dependency Inversion)**: higher layers abstract lower layers via **function type aliases** (dev-kit Python uses function types — see `architecture/ts-style.md` / `architecture/dependencies.md`)

### Extensibility awareness (do not strictly enforce YAGNI)

- For extension points that "are likely to come eventually", **abstract via function types from the start** (cheaper than retrofitting)
- However, avoid increasing "abstractions you don't know are coming" (mass-producing `@overload` / `Protocol` is counter-productive)
- The threshold judgment for abstraction is in `refactoring-judgement.md`

---

## Class vs Function Priority

dev-kit Python is **function-first** (`architecture/ts-style.md`). Use classes for:
- DTOs (`@dataclass` / `BaseModel`)
- Library requirements (FastAPI Middleware, Pydantic BaseModel inheritance, CLI Command)
- Long-lived runtime state (connection pools, WebSocket sessions)

Everything else (services / Repositories / Providers / Validators, etc.) should be written as functions.

---

## Things you must not do

```python
# ❌ 同じパース処理を 2 箇所に書く
def handle_a(raw: str) -> int:
    return int(raw.strip().lower().replace(",", ""))

def handle_b(raw: str) -> int:
    return int(raw.strip().lower().replace(",", ""))   # DRY 違反、_helpers.py へ

# ❌ 1 関数が複数の理由で変わる
def process_order(order: Order) -> None:
    validate(order)
    save_to_db(order)
    send_email(order)
    log_audit(order)
    update_metrics(order)
    # ↑ S 違反、責務を分割
```

---

## Related files

- `architecture/refactoring-judgement.md` — judgment criteria for consolidation / abstraction / externalizing settings
- `architecture/ts-style.md` — function-first + DI via type aliases
- `architecture/dependencies.md` — dependency direction and DIP
