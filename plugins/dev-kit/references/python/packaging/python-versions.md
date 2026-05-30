# packaging/python-versions — Python version policy

py-kit's policy: **adopt the highest version possible**.

---

## Recommendation

- **New projects**: the latest stable version (3.13 at the time of writing) or one below (3.12)
- **Set `requires-python = ">=3.12"` as the minimum line**
- As a rule, do not support 3.11 or earlier

---

## Major feature support table from 3.12 onward

| Feature | Introduced | Description |
|---|---|---|
| PEP 695 `type X = ...` | 3.12 | Dedicated syntax for type aliases |
| PEP 695 generic functions `def f[T](...)` | 3.12 | New notation for generics |
| `@override` decorator | 3.12 | Explicit method override |
| f-string improvements (nested quoting) | 3.12 | `f"{'inner'}"` becomes writable |
| `tomllib` standard library | 3.11 | TOML reading (standard) |
| `Self` type | 3.11 | Return type for class methods |
| `ExceptionGroup` / `except*` | 3.11 | Combined with TaskGroup |
| `tomllib` writer is a separate package | — | For writing, install `tomli-w` |
| `asyncio.TaskGroup` | 3.11 | New API for concurrent execution |
| `asyncio.timeout` | 3.11 | New API for timeouts |
| `--disable-gil` build | 3.13 | Experimental; not recommended for production |
| `interpreters` standard module | 3.13 | Official API for subinterpreters |

py-kit fully adopts PEP 695, so **3.12+ is required**.

---

## Multi-version support is generally not pursued

For a library distributed widely, supporting older versions may be worth considering,
but for in-house projects / limited distribution, **pinning to the latest is overwhelmingly easier**:
- Just `from __future__ import annotations` is enough
- No need for compatibility shims such as `typing_extensions`
- Performance improvements (the speed gains since 3.11)

---

## How to pin the version

`pyproject.toml`:

```toml
[project]
requires-python = ">=3.12"
```

`.python-version` (for uv):

```
3.12
```

```bash
# プロジェクトディレクトリで
uv python install 3.12
uv python pin 3.12
```

---

## Matrix testing in CI

To verify behavior on multiple versions, use GitHub Actions:

```yaml
strategy:
  matrix:
    python-version: ["3.12", "3.13"]

steps:
  - uses: astral-sh/setup-uv@v3
    with:
      python-version: ${{ matrix.python-version }}
  - run: uv sync
  - run: uv run pytest
```

That said, for an in-house project, **pinning to a single version** is sufficient.

---

## New features in 3.13 (adoption judgment)

| Feature | Adopt |
|---|---|
| `--disable-gil` build | ❌ Wait and see (dependent libraries don't support it yet) |
| `interpreters` standard | ❌ Experimental |
| iOS / Android tier 3 | ❌ Not relevant |
| Improved REPL | ✅ Benefit only at development time |
| Type system improvements (PEP 696 default type arguments, etc.) | ✅ Use as needed |

Until 3.13 stabilizes, **pinning to 3.12** is fine.

---

## When you need an older Python

Only when integration with legacy environments is required, lower the minimum line:

```toml
requires-python = ">=3.10"
```

In that case:
- PEP 695 (`type X = ...`) is unavailable → substitute with `TypeAlias`
- The `Self` type must be replaced with `typing_extensions.Self`
- `asyncio.TaskGroup` is unavailable → fall back to `asyncio.gather`

If you have to write code like this, be prepared for **maintenance costs to skyrocket**.

---

## Related files

- `core/type-hints.md` — code using PEP 695
- `packaging/pyproject.md` — the `requires-python` field in pyproject.toml
- `packaging/dependencies.md` — Python version management with uv
