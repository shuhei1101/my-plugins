<!-- This file is a Japanese mirror of Pythonバージョン.md. When updating the English original, update this file too. -->
# packaging/python-versions — Python バージョン方針

> このファイルは `Pythonバージョン.md` の日本語ミラーです。

dev-kit Python の方針: **極力高いバージョンを採用する**。

---

## 推奨

- **新規プロジェクト**: 最新安定版（執筆時点で 3.13）または 1 つ下（3.12）
- **`requires-python = ">=3.12"` を最低ラインに**
- 3.11 以下のサポートは原則しない

---

## 3.12 以降の主要機能対応表

| 機能 | 導入 | 説明 |
|---|---|---|
| PEP 695 `type X = ...` | 3.12 | 型エイリアス専用構文 |
| PEP 695 ジェネリック関数 `def f[T](...)` | 3.12 | ジェネリクスの新書式 |
| `@override` decorator | 3.12 | メソッドオーバーライド明示 |
| `f-string` の改善（ネスト引用） | 3.12 | `f"{'inner'}"` が書けるように |
| `tomllib` 標準ライブラリ | 3.11 | TOML 読み込み（標準） |
| `Self` 型 | 3.11 | クラスメソッドの戻り値型 |
| `ExceptionGroup` / `except*` | 3.11 | TaskGroup と組み合わせ |
| `tomllib` writer は別パッケージ | — | 書き込みは `tomli-w` を入れる |
| `asyncio.TaskGroup` | 3.11 | 並行実行の新 API |
| `asyncio.timeout` | 3.11 | タイムアウトの新 API |
| `--disable-gil` ビルド | 3.13 | 実験的・本番未推奨 |
| `interpreters` 標準モジュール | 3.13 | subinterpreter 公式 API |

dev-kit Python は PEP 695 を全面採用するので **3.12+ 必須**。

---

## マルチバージョンサポートは原則しない

ライブラリとして広く配布するなら旧バージョン互換も検討する価値があるが、
内製プロジェクト / 限定配布なら **最新固定が圧倒的に楽**:
- `from __future__ import annotations` だけで済む
- `typing_extensions` 等の互換 shim 不要
- パフォーマンス改善（3.11 以降のスピード向上）

---

## バージョン固定方法

`pyproject.toml`:

```toml
[project]
requires-python = ">=3.12"
```

`.python-version`（uv 用）:

```
3.12
```

```bash
# プロジェクトディレクトリで
uv python install 3.12
uv python pin 3.12
```

---

## CI でのマトリクステスト

複数バージョンで動作確認するなら GitHub Actions で:

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

ただし、内製プロジェクトなら **1 バージョン固定** で十分。

---

## 3.13 の新機能（採用判断）

| 機能 | 採用 |
|---|---|
| `--disable-gil` ビルド | ❌ 様子見（依存ライブラリ未対応） |
| `interpreters` 標準 | ❌ 実験的 |
| iOS / Android tier 3 | ❌ 関係なし |
| 改善された REPL | ✅ 開発時のみ恩恵あり |
| 型システムの改善（PEP 696 デフォルト型引数等） | ✅ 必要なら使う |

3.13 が安定するまで **3.12 固定** でも問題ない。

---

## 古い Python が必要になったら

レガシー環境との連携が必要な場合のみ、最小ラインを下げる:

```toml
requires-python = ">=3.10"
```

ただしその場合:
- PEP 695 (`type X = ...`) は使えない → `TypeAlias` で代用
- `Self` 型は `typing_extensions.Self` で代用
- `asyncio.TaskGroup` 使えない → `asyncio.gather` でフォールバック

このようなコードを書く必要があるなら、**メンテコストが跳ね上がる**ことを覚悟する。

---

## 関連ファイル

- `core/型ヒント.md` — PEP 695 を使ったコード
- `packaging/pyproject設定.md` — pyproject.toml の `requires-python`
- `packaging/依存パッケージ管理.md` — uv での Python バージョン管理
