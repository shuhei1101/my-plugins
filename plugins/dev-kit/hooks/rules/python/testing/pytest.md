---
paths:
  - "**/benchmarks/**/*.py"
  - "**/tests/**/test_*.py"
  - "**/tests/conftest.py"
---

# pytest 規約

設定値（testpaths / asyncio_mode / addopts / markers）は `packaging/pyproject設定.md` の `[tool.pytest.ini_options]` を参照。

## 命名

- ファイル `test_*.py`、関数 `test_*()`。クラスは使わず関数で書く

## fixtures

- 共通 fixture は `conftest.py`（ディレクトリ階層単位で自動ロード。`tests/conftest.py` は全体、`tests/features/conftest.py` は配下のみ）
- テスト用 `Settings` は fixture で env を上書きして生成
- 時刻固定は `monkeypatch.setattr` で `now_utc` を差し替え
- Mock 関数（成功 / rate-limited 等）も fixture 化して注入

## parametrize

複数パターンは `@pytest.mark.parametrize`、ケース名は `pytest.param(..., id="empty")` で明示。

## 非同期

`asyncio_mode = "auto"` なら `@pytest.mark.asyncio` 省略可。

## FastAPI ルート

`build_fastapi()` → `app.state.handlers` にテスト用 Handlers（Mock 注入済み）をセット → `TestClient` で叩く。

## マーカー

- ファイル全体は `pytestmark = pytest.mark.smoke`、関数単位は `@pytest.mark.slow` 等
- 選択実行は `pytest -m "not smoke"`

## デバッグ

`-v`（詳細）/ `-s`（print 表示）/ `--pdb`（失敗時デバッガ）/ `-x`（最初の失敗で停止）/ `path::test_name` で 1 つだけ実行。
