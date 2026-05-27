# packaging/dependencies — Dependency management

In py-kit projects, **`uv`** is the standard. `pip` / `poetry` are not used.

---

## Advantages of uv

- Fast (written in Rust; 10–100× faster than `pip install`)
- Built-in venv management (everything is done with `uv` alone)
- Reproducible dependency resolution via lockfile (`uv.lock`)
- Python version management (`uv python install`) is also integrated

---

## Setup

```bash
# uv 自体のインストール
curl -LsSf https://astral.sh/uv/install.sh | sh

# プロジェクト初期化
uv init mypkg --package      # src レイアウト + パッケージ化前提
cd mypkg

# Python バージョン固定
uv python pin 3.12
```

A `.python-version` file is created, and 3.12 is used automatically from then on.

---

## Adding / removing dependencies

```bash
# 本番依存
uv add httpx pydantic fastapi

# 特定バージョン
uv add "httpx>=0.27,<1.0"

# dev 依存
uv add --dev pytest pytest-asyncio mypy ruff

# 削除
uv remove httpx
```

The `dependencies` / `optional-dependencies.dev` sections of `pyproject.toml` are updated automatically.

---

## Environment sync

```bash
# pyproject.toml に従って .venv を再構築
uv sync

# dev 依存も含めて
uv sync --all-extras

# 本番のみ（CI でビルドする時など）
uv sync --no-dev
```

Once you run `uv sync`, `.venv/` is brought in line with `pyproject.toml`.

---

## Running

```bash
# venv を明示的に activate しなくても、uv run で実行できる
uv run pytest
uv run python -m mypkg
uv run uvicorn mypkg.server.app:build_fastapi --factory --reload
```

`uv run` looks at the .venv internally and runs the command. The same commands work in CI and in development.

---

## The .venv directory

```
mypkg/
├── pyproject.toml
├── uv.lock              # ロック（コミット対象）
├── .python-version      # コミット対象
├── .venv/               # .gitignore
└── src/
```

| File | Management |
|---|---|
| `pyproject.toml` | Git-managed |
| `uv.lock` | **Git-managed** (required for reproducibility) |
| `.python-version` | Git-managed |
| `.venv/` | `.gitignore` |

---

## The lockfile (`uv.lock`)

Automatically updated by `uv add` / `uv sync`. **Do not edit manually**.

In CI, use `uv sync --frozen` to verify that the lock content has not drifted:

```yaml
# .github/workflows/ci.yml
- name: Sync deps
  run: uv sync --frozen

- name: Run tests
  run: uv run pytest
```

---

## Pinning the Python version

`.python-version`:

```
3.12
```

`uv python install 3.12` automatically fetches the required version.
Because it does not depend on the system Python, developers all use the same Python version.

---

## Splitting into groups

To split into three or more dependency groups, use `[dependency-groups]` (PEP 735):

```toml
[dependency-groups]
dev = ["pytest", "mypy", "ruff"]
docs = ["sphinx", "myst-parser"]
benchmark = ["pyperf"]
```

```bash
uv sync --group docs
uv sync --group dev --group benchmark
```

Use `optional-dependencies` for "extra features for external users" (e.g. `pip install mypkg[redis]`),
and use `dependency-groups` for "developer working groups".

---

## Migrating an existing project to uv

From the `requirements.txt` style:

```bash
uv init --package
uv add -r requirements.txt
```

From `poetry`: hand-write the `[project]` section of `pyproject.toml`, then run `uv sync`.

---

## Things you must not do

```bash
# ❌ pip install で venv に突っ込む（uv の状態と乖離する）
pip install requests

# ✅ uv add を使う
uv add requests

# ❌ uv.lock を編集
# 手動で書き換えると整合性が壊れる

# ❌ .venv を Git 管理
# サイズ膨大、OS 依存、再現性なし → .gitignore
```

---

## Related files

- `packaging/pyproject.md` — how to write pyproject.toml
- `packaging/python-versions.md` — which version to choose
- `packaging/distribution.md` — publishing to PyPI
