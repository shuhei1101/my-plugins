<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# packaging/distribution — 配布

> このファイルは `distribution.md` の日本語ミラーです。

ライブラリ / CLI ツールとして他のプロジェクトに配布する場合の標準フロー。

---

## wheel / sdist のビルド

```bash
uv build
```

`dist/` 配下に以下が生成される:
- `mypkg-{version}.tar.gz` — ソース配布 (sdist)
- `mypkg-{version}-py3-none-any.whl` — wheel

`hatchling` バックエンドが `pyproject.toml` の `[tool.hatch.build.targets.wheel]` を見て
パッケージを構築する。

---

## PyPI 公開

### 事前準備

1. PyPI アカウントを作成（https://pypi.org/account/register/）
2. API トークンを発行
3. `~/.pypirc` または環境変数 `UV_PUBLISH_TOKEN` で認証

### 公開

```bash
uv publish
```

Test PyPI で試したい場合:

```bash
uv publish --publish-url https://test.pypi.org/legacy/
```

---

## バージョン規約（SemVer）

| 変更 | バンプ |
|---|---|
| 後方互換のあるバグ修正 | PATCH (`0.1.0` → `0.1.1`) |
| 後方互換のある機能追加 | MINOR (`0.1.0` → `0.2.0`) |
| 破壊的変更 | MAJOR (`0.1.0` → `1.0.0`) |

`0.x` バージョンの間は MINOR を破壊的変更扱いにできる（柔軟）。
`1.0.0` 以降は厳密に SemVer を守る。

---

## CHANGELOG

`CHANGELOG.md` を維持する。Keep a Changelog 形式を推奨:

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

リリース時に `[Unreleased]` の中身を `[0.x.y] - YYYY-MM-DD` に移す。

---

## CLI エントリポイント

`pyproject.toml`:

```toml
[project.scripts]
mypkg = "mypkg.__main__:main"
mypkg-admin = "mypkg.cli.admin:main"
```

`pip install mypkg` 後、`mypkg --help` / `mypkg-admin --help` が使えるようになる。

`__main__:main` は `main() -> int` を返す関数。`sys.exit(main())` が裏で動く。

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

## 名前空間パッケージ

通常パッケージで OK。`namespace_packages` は使わない（複雑になる）。

---

## マニフェスト（同梱ファイル）

非 .py ファイル（プロンプト / YAML / テンプレ等）も配布したい場合:

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

## GitHub Actions での自動公開

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

タグ（`git tag v0.2.0 && git push --tags`）で自動公開。

---

## 関連ファイル

- `packaging/pyproject.md` — pyproject.toml の構造
- `packaging/dependencies.md` — uv で開発
- `packaging/python-versions.md` — 対応バージョン
