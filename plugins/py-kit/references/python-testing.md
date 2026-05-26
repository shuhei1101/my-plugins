# Python Testing Standards — py-kit

Logger setup and test policy for Python projects.

---

## Logger Specification

Every project must include `{package_name}/logger.py` with a `setup_logger()` function:

- `constants.py` defines `LOG_DIR = PROJECT_ROOT / "log"`
- `setup_logger()` calls `LOG_DIR.mkdir(parents=True, exist_ok=True)`
- Log filename: `LOG_DIR / f"{datetime.now():%Y%m%d_%H%M%S}_{package_name}.log"` — new file every run
- Attach both `StreamHandler(sys.stdout)` and `FileHandler(..., encoding="utf-8")`
- Format: `[%(asctime)s] %(levelname)s %(name)s %(filename)s:%(lineno)d - %(message)s`
- Guard against duplicate handlers: `if logger.handlers: return logger`
- Submodules: `get_logger(__name__)`

Call `setup_logger()` immediately after entry in `main.py` / `__main__.py`.

---

## Test Policy

| Test type | Policy |
|---|---|
| Unit tests (individual methods/functions) | Not written — maintenance cost exceeds value in AI-assisted development |
| Module integration tests | Write when modules interact in non-obvious ways |
| Use case tests | Write per use case; mock only external I/O boundaries |
| E2E tests | Write for CLI entry points and HTTP API endpoints |

Use pytest. Mirror the source folder structure in `tests/`. Reusable mocks go in `tests/mocks/`.

Source and test files are linked — when a source file changes, always check and update corresponding tests.

### Test structure

```
tests/
├── mocks/
│   ├── mock_env.py       # environment variable mocking helper
│   └── mock_externals.py # stubs for external API / DB clients
├── conftest.py           # shared pytest fixtures
└── {feature}/
    └── test_{feature}.py
```

Tests mock only external I/O boundaries (DB, API, filesystem) — no unit tests for individual methods.
