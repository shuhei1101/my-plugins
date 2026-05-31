# packaging/pyproject — Complete pyproject.toml sample

Standard `pyproject.toml` template for new Python projects.

---

## Full sample

```toml
# ================================================================
# Project metadata (PEP 621)
# ================================================================
[project]
name = "mypkg"
version = "0.1.0"
description = "短い説明（1 行）"
readme = "README.md"
requires-python = ">=3.12"
license = { text = "MIT" }
authors = [
    { name = "Your Name", email = "you@example.com" },
]
keywords = ["llm", "fastapi"]
classifiers = [
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

# 本番依存
dependencies = [
    "pydantic>=2.6",
    "pydantic-settings>=2.2",
    "httpx>=0.27",
    "fastapi>=0.110",
    "uvicorn[standard]>=0.27",
    "anthropic>=0.18",
    "openai>=1.10",
    "instructor>=1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "pytest-cov>=4.1",
    "respx>=0.20",
    "mypy>=1.8",
    "ruff>=0.5",
    "pyright>=1.1",
]

[project.urls]
Homepage = "https://github.com/you/mypkg"
Repository = "https://github.com/you/mypkg"

# CLI エントリポイント（python -m mypkg は __main__.py が自動で拾う）
[project.scripts]
mypkg = "mypkg.__main__:main"


# ================================================================
# Build system
# ================================================================
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/mypkg"]


# ================================================================
# uv（依存管理ツール）
# ================================================================
[tool.uv]
managed = true


# ================================================================
# ruff
# ================================================================
[tool.ruff]
line-length = 100
target-version = "py312"
src = ["src"]

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "F",    # pyflakes
    "I",    # isort
    "B",    # bugbear
    "UP",   # pyupgrade
    "SIM",  # simplify
    "RUF",  # ruff
]
ignore = [
    "E501",  # 行長は formatter に任せる
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"


# ================================================================
# mypy
# ================================================================
[tool.mypy]
python_version = "3.12"
strict = true
warn_unused_ignores = true
warn_redundant_casts = true
show_error_codes = true
pretty = true
plugins = ["pydantic.mypy"]


# ================================================================
# pyright（任意・エディタ統合用）
# ================================================================
[tool.pyright]
pythonVersion = "3.12"
typeCheckingMode = "strict"
include = ["src", "tests"]
exclude = ["**/node_modules", "**/.venv"]


# ================================================================
# pytest
# ================================================================
[tool.pytest.ini_options]
minversion = "8.0"
testpaths = ["tests"]
python_files = "test_*.py"
python_functions = "test_*"
asyncio_mode = "auto"
addopts = [
    "-ra",
    "--strict-markers",
    "--strict-config",
    "-W", "error",
]
markers = [
    "smoke: real external-service tests (requires --run-smoke)",
]


# ================================================================
# coverage（任意）
# ================================================================
[tool.coverage.run]
source = ["src/mypkg"]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
]
```

---

## src layout

Place code under `src/mypkg/` (src layout).
Compared to placing `mypkg/` directly at the root (flat layout), the src layout prevents confusion between tests and packages.

```
mypkg/
├── pyproject.toml
├── src/
│   └── mypkg/
│       ├── __init__.py
│       ├── __main__.py
│       ├── main.py
│       ├── shared/
│       └── features/
├── tests/
└── README.md
```

---

## Explanation of required sections

### `[project]`

PEP 621 standard. `name` / `version` / `requires-python` / `dependencies` are effectively required.

Pin the minimum version with `requires-python = ">=3.12"` (so PEP 695 can be used).

### `dependencies` vs `optional-dependencies.dev`

- `dependencies`: required in production. Installed by `pip install mypkg`.
- `optional-dependencies.dev`: development only. Installed by `pip install -e ".[dev]"`.

Keep test tools (pytest, etc.) **separated under dev**. This way `pytest` does not leak into the production image.

### `[project.scripts]`

If you write `mypkg = "mypkg.__main__:main"`, after `pip install` you can launch the CLI with `mypkg --arg foo`.

### `[build-system]`

`hatchling` is recommended. `setuptools` also works, but `hatchling` has shorter configuration.

---

## Operating with uv

```bash
# プロジェクトを初期化
uv init mypkg --package

# 依存追加
uv add httpx pydantic

# dev 依存
uv add --dev pytest mypy

# 同期
uv sync

# 実行
uv run pytest
uv run python -m mypkg --arg foo
```

`uv` is a fast unified version of `pip` + `venv` + `pip-tools`. In dev-kit Python projects, **uv is the standard**.
See `packaging/依存パッケージ管理.md` for details.

---

## .gitignore

```
# venv
.venv/

# secrets
.env

# Python
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
.ruff_cache/

# distribution
dist/
build/
*.egg-info/

# coverage
.coverage
coverage.xml
htmlcov/

# editor
.idea/
.vscode/
*.swp
```

---

## README.md

The `readme = "README.md"` setting in `pyproject.toml` is what gets shown on PyPI. At minimum:

```markdown
# mypkg

短い説明。

## Installation

```bash
pip install mypkg
# or
uv add mypkg
```

## Usage

```bash
mypkg --arg foo
```
```

---

## Related files

- `packaging/依存パッケージ管理.md` — how to use uv
- `packaging/配布設定.md` — publishing to PyPI
- `packaging/Pythonバージョン.md` — version selection
- `core/スタイル.md` — details of ruff / mypy configuration
