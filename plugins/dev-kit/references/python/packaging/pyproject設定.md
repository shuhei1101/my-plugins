<!-- This file is a Japanese mirror of pyproject設定.md. When updating the English original, update this file too. -->
# packaging/pyproject — pyproject.toml 完全サンプル

新規 Python プロジェクトの `pyproject.toml` 標準テンプレート。

---

## 全体サンプル

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

## src レイアウト

`src/mypkg/` 配下にコードを置く（src レイアウト）。
ルート直下に `mypkg/` を置く形式（flat レイアウト）より、テストとパッケージの混同を防げる。

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

## 必須セクションの説明

### `[project]`

PEP 621 標準。`name` / `version` / `requires-python` / `dependencies` は必須相当。

`requires-python = ">=3.12"` で最低バージョンを固定（PEP 695 使うため）。

### `dependencies` vs `optional-dependencies.dev`

- `dependencies`: 本番で必要。`pip install mypkg` で入る
- `optional-dependencies.dev`: 開発時のみ。`pip install -e ".[dev]"` で入る

テストツール（pytest 等）は **dev に分離**。本番イメージで `pytest` が混入しない。

### `[project.scripts]`

`mypkg = "mypkg.__main__:main"` を書くと、`pip install` 後に `mypkg --arg foo` で CLI 起動できる。

### `[build-system]`

`hatchling` を推奨。`setuptools` でもよいが `hatchling` の方が設定が短い。

---

## uv での運用

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

`uv` は `pip` + `venv` + `pip-tools` を統合した高速版。dev-kit Python プロジェクトでは **uv 標準**。
詳細は `packaging/依存パッケージ管理.md`。

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

`pyproject.toml` の `readme = "README.md"` が PyPI に表示される。最低限:

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

## 関連ファイル

- `packaging/依存パッケージ管理.md` — uv の使い方
- `packaging/配布設定.md` — PyPI 公開
- `packaging/Pythonバージョン.md` — バージョン選定
- `core/スタイル.md` — ruff / mypy 設定の詳細
