# packaging/distribution — Distribution

Standard flow for distributing a library or CLI tool to other projects.

---

## Building the wheel / sdist

```bash
uv build
```

The following are generated under `dist/`:
- `mypkg-{version}.tar.gz` — source distribution (sdist)
- `mypkg-{version}-py3-none-any.whl` — wheel

The `hatchling` backend reads `[tool.hatch.build.targets.wheel]` in `pyproject.toml`
to build the package.

---

## Publishing to PyPI

### Preparation

1. Create a PyPI account (https://pypi.org/account/register/)
2. Issue an API token
3. Authenticate via `~/.pypirc` or the `UV_PUBLISH_TOKEN` environment variable

### Publishing

```bash
uv publish
```

If you want to try with Test PyPI:

```bash
uv publish --publish-url https://test.pypi.org/legacy/
```

---

## Versioning convention (SemVer)

| Change | Bump |
|---|---|
| Backward-compatible bug fix | PATCH (`0.1.0` → `0.1.1`) |
| Backward-compatible feature addition | MINOR (`0.1.0` → `0.2.0`) |
| Breaking change | MAJOR (`0.1.0` → `1.0.0`) |

While on a `0.x` version, you may treat MINOR bumps as breaking changes (flexible).
After `1.0.0`, follow SemVer strictly.

---

## CHANGELOG

Maintain a `CHANGELOG.md`. The Keep a Changelog format is recommended:

```markdown
# Changelog

## [Unreleased]

### Added
- 新機能の説明

### Changed
- 既存機能の変更

### Fixed
- バグ修正

## [0.2.0] - 2026-05-28

### Added
- /chat エンドポイント追加

## [0.1.0] - 2026-04-01

- 初回リリース
```

On release, move the contents of `[Unreleased]` to `[0.x.y] - YYYY-MM-DD`.

---

## CLI entry points

`pyproject.toml`:

```toml
[project.scripts]
mypkg = "mypkg.__main__:main"
mypkg-admin = "mypkg.cli.admin:main"
```

After `pip install mypkg`, `mypkg --help` / `mypkg-admin --help` become available.

`__main__:main` is a function that returns `main() -> int`. `sys.exit(main())` runs behind the scenes.

---

## __main__.py

```python
# src/mypkg/__main__.py
"""python -m mypkg で起動するエントリポイント。"""
from __future__ import annotations
import argparse
import sys
from mypkg.main import build_handlers
from mypkg.shared.settings import Settings


def main() -> int:
    parser = argparse.ArgumentParser(prog="mypkg")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # `mypkg run` サブコマンド
    run_p = sub.add_parser("run")
    run_p.add_argument("--input", required=True)

    args = parser.parse_args()
    settings = Settings()
    handlers = build_handlers(settings)

    if args.cmd == "run":
        result = handlers.do_something(args.input)
        print(result)
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
```

---

## Namespace packages

Regular packages are fine. Do not use `namespace_packages` (it adds complexity).

---

## Manifest (bundled files)

If you want to distribute non-`.py` files (prompts, YAML, templates, etc.):

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/mypkg"]

[tool.hatch.build]
include = [
    "src/mypkg/**/*.py",
    "src/mypkg/**/*.yaml",
    "src/mypkg/**/*.md",     # プロンプトファイル等
]
```

---

## Automated publishing with GitHub Actions

`.github/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    tags:
      - "v*"

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write   # PyPI trusted publishing
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv build
      - uses: pypa/gh-action-pypi-publish@release/v1
```

Tags (`git tag v0.2.0 && git push --tags`) trigger automatic publishing.

---

## Related files

- `packaging/pyproject.md` — structure of pyproject.toml
- `packaging/dependencies.md` — developing with uv
- `packaging/python-versions.md` — supported versions
