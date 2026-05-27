# Style

Policy for formatting and static analysis configuration. For example entries in `pyproject.toml`, see `packaging/pyproject.md`.

---

## Tool Setup

| Tool | Role |
|---|---|
| `ruff` | Formatter + linter (equivalent to black + isort + flake8) |
| `mypy` | Type checker (CI / strict) |
| `pyright` | Fast type checker for editor integration (optional) |
| `pytest` | Test runner |

---

## Recommended ruff Settings

`pyproject.toml`:

```toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = [
  "E",    # pycodestyle errors
  "F",    # pyflakes
  "I",    # isort
  "B",    # bugbear（バグになりやすいパターン）
  "UP",   # pyupgrade（古い書き方の自動修正）
  "SIM",  # simplify（簡潔な書き方の提案）
  "RUF",  # ruff 独自
]
ignore = [
  "E501",  # 行長は formatter に任せる
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

---

## Recommended mypy Settings

```toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_unused_ignores = true
warn_redundant_casts = true
show_error_codes = true
pretty = true

# Pydantic と組み合わせる場合
plugins = ["pydantic.mypy"]
```

Main checks included in `strict = true`:
- `--check-untyped-defs`
- `--disallow-any-generics`
- `--disallow-untyped-defs`
- `--no-implicit-optional`
- `--warn-return-any`

---

## Recommended pyright Settings (Optional)

`pyproject.toml`:

```toml
[tool.pyright]
pythonVersion = "3.12"
typeCheckingMode = "strict"
reportMissingImports = "error"
reportMissingTypeStubs = "warning"
```

Combine with editor (VS Code / Cursor) Pylance for instant detection during development.

---

## Line Length

- **100 characters** as standard (a bit looser than black's 88, prioritizing readability)
- Exceptions: URLs, long string literals, tables inside Markdown

```python
# OK（100 文字以内）
def create_user(input: CreateUserInput, *, save: SaveUser, generate_id: GenerateUserId) -> User:
    ...
```

---

## Quotes / Strings

- Double quotes (`"..."`) as the standard (matches black / ruff format)
- f-strings are `f"..."`
- docstrings are `"""..."""`
- When the string contains `"`, switching to single quotes is allowed (`'I said "hi"'`)

---

## Import Style

See `core/language-rules.md` for details. ruff's `I` rule sorts automatically.

---

## Section Markers

In long modules, you may use section markers to separate major logical blocks.

```python
# ================================================================
# DTO
# ================================================================

@dataclass(frozen=True, slots=True, kw_only=True)
class User: ...


# ================================================================
# Service
# ================================================================

def create_user(input: CreateUserInput, *, save: SaveUser) -> User: ...
```

That said, **once it grows long enough to need sections, prioritize splitting the file**
(into `types.py` / `service.py`, etc.). Section markers are the last resort for "not big enough to split, but I want a heading."

---

## Related Files

- `packaging/pyproject.md` — full pyproject.toml sample
- `core/language-rules.md` — import ordering and logging
- `core/naming.md` — naming conventions
