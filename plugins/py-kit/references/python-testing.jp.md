<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# Python テスト規約 — py-kit（日本語ミラー）

> このファイルは `python-testing.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `python-testing.md` にも反映してください。

本格 Python プロジェクト向けのロガー設定・テストポリシー・pytest 規約。
`python-core.md` と `python-architecture.md` と合わせて読む。

このファイルは簡易スクリプトには**適用しない** — そちらは
`logging.basicConfig()` インラインで済ませ、テストスイートも持たない。
`python-scripts.md` を参照。

---

## 1. ロガー仕様

### 1.1 必須 `logger.py`

すべてのプロジェクトに `{package_name}/logger.py` と `setup_logger()` 関数を持たせる。以下が本セクションのルールを満たす正規実装。

```python
"""{package_name}.logger — アプリケーション全体のロガーセットアップ。"""

import logging
import sys
from datetime import datetime
from pathlib import Path

from {package_name}.constants import LOG_DIR, PROJECT_NAME

LOG_FORMAT = "[%(asctime)s] %(levelname)s %(name)s %(filename)s:%(lineno)d - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(level: int = logging.INFO) -> logging.Logger:
    """ルートアプリケーションロガーを初期化。冪等：2回呼んでも安全。"""
    root = logging.getLogger(PROJECT_NAME)
    if root.handlers:
        return root  # 設定済み・重複ハンドラー回避

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / f"{datetime.now():%Y%m%d_%H%M%S}_{PROJECT_NAME}.log"

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    root.setLevel(level)
    root.addHandler(stream_handler)
    root.addHandler(file_handler)
    root.propagate = False  # グローバルルートロガーへの伝播を防ぐ

    return root


def get_logger(name: str) -> logging.Logger:
    """アプリケーションルートの子ロガーを返す。サブモジュールで使う。"""
    return logging.getLogger(f"{PROJECT_NAME}.{name}")
```

### 1.2 ロガールール（硬性）

| ルール | 理由 |
|---|---|
| `LOG_DIR` は `constants.py` で定義（`logger.py` 内ハードコード禁止） | 他のコード（ローテーション・クリーンアップ）も `LOG_DIR` を読む |
| `setup_logger()` 内で `LOG_DIR.mkdir(parents=True, exist_ok=True)` | 空 `log/` を Windows のクリーンアップツールが消すため |
| ログファイル名にタイムスタンプ：`YYYYMMDD_HHMMSS_{package_name}.log` | 1実行1ファイル・上書きされない・ソート可 |
| `StreamHandler(sys.stdout)` と `FileHandler(..., encoding="utf-8")` 両方 | 開発時はコンソール・監査用にファイル |
| `FileHandler` に `encoding="utf-8"` | デフォルトはプラットフォーム依存 — 明示の方が安全 |
| フォーマットに `filename:lineno` | 想定外の場所からメッセージが来るときデバッグ時間短縮 |
| 冪等性ガード：`if root.handlers: return root` | `setup_logger()` が複数回呼ばれる可能性あり（テスト等） |
| `root.propagate = False` | Python のグローバルルートロガー経由の重複出力を防ぐ |
| サブモジュール：`get_logger(__name__)` | 階層的ロガー名・モジュール別レベル制御 |

### 1.3 `setup_logger()` を呼ぶ場所

composition root（`main.py` または `__main__.py`）で**1回だけ**・できるだけ早く呼ぶ。返り値のロガーで起動シーケンスをログる。

```python
# {package_name}/main.py
from {package_name}.logger import setup_logger

def main() -> None:
    logger = setup_logger()
    logger.info("Starting %s", PROJECT_NAME)
    ...
```

### 1.4 サブモジュールでのロガー使用

```python
# {package_name}/application/use_cases/create_order.py
from {package_name}.logger import get_logger

logger = get_logger(__name__)  # モジュールレベル

class CreateOrderUseCase:
    def execute(self, input: CreateOrderInput) -> Order:
        logger.info("Creating order for customer %s", input.customer_id)
        ...
```

### 1.5 サブシステム別ログレベル（応用）

特定モジュールが冗長すぎるとき個別にレベルを上げる：

```python
# main.py の setup_logger() の後
logging.getLogger(f"{PROJECT_NAME}.infrastructure.persistence").setLevel(logging.WARNING)
```

実行時に必要なら env var で：

```python
# config.py
class Settings(BaseModel):
    log_level: str = "INFO"
    log_levels_per_module: dict[str, str] = Field(default_factory=dict)
```

### 1.6 禁止ロガーパターン

```python
# ❌ 悪い — ライブラリモジュール内のモジュールレベル basicConfig
import logging
logging.basicConfig(level=logging.DEBUG)  # 呼び出し元全部に漏れる

# ❌ 悪い — ロガー呼び出しに f-string（遅延フォーマットが効かない）
logger.info(f"Order {order.id} created")

# ✅ 良い — % フォーマット・ログレベル OFF 時にコストが遅延
logger.info("Order %s created", order.id)

# ❌ 悪い — 実行時エラーに裸 `print()`
print(f"Failed: {e}")

# ✅ 良い — logger.error はスタックフレーム・重要度・ファイル位置をキャプチャ
logger.error("Failed", exc_info=True)

# ❌ 悪い — ロガー出力に日本語（bat 実行で CP932 文字化け）
logger.info("注文を作成しました")

# ✅ 良い — 英語
logger.info("Order created")
```

---

## 2. テストポリシー

py-kit プロジェクトは**境界テスト**ポリシー：テストは意味ある境界（ユースケース・リポジトリ・API エンドポイント）の振る舞いを検証 — 個別メソッドはテストしない。

### 2.1 何をテストし、何をしないか

| テスト種別 | ポリシー | 理由 |
|---|---|---|
| ユースケーステスト | ✅ 常時 | ユースケースが価値の単位；ユーザーがやることをカバー |
| ドメインロジック（純粋関数・値オブジェクト） | ✅ 複雑なとき | 読んで検証困難なルールにテストを書く |
| リポジトリテスト（インフラ） | ✅ 実テスト DB（コンテナ内 Postgres）かインメモリ実装に対して | SQL / スキーマミスを捕える |
| HTTP エンドポイント（インターフェース） | ✅ FastAPI `TestClient` で | ルーティング / シリアライズミスを捕える |
| E2E（CLI/API エンドツーエンド） | ✅ クリティカルパスのみ | 保守コストが高い |
| 個別メソッドのユニットテスト | ❌ 書かない | 保守コスト > 価値（AI 支援開発で）；リファクタについてこない |
| getter/setter・dataclass フィールドのテスト | ❌ 書かない | 自明コードのテスト |
| サードパーティライブラリのテスト | ❌ 書かない | 自分のコードではない |

### 2.2 モックポリシー — 境界のみモック

テストは外部 I/O 境界のみモック：DB・HTTP・ファイルシステム・メッセージキュー・LLM API・OS API。ドメインロジックとアプリケーションサービスは実実装でテストする。

| テスト対象 | モック | 実物 |
|---|---|---|
| ユースケース | リポジトリ・支払いゲートウェイ・LLM クライアント | ドメインエンティティ・値オブジェクト |
| ドメインサービス | なし（純粋なので） | すべて |
| リポジトリ | データベース接続 / HTTP クライアント | SQL / シリアライズコード |
| HTTP エンドポイント | インメモリインフラで全ユースケース | ルーター・ミドルウェア・Pydantic |

`domain/repositories/` の Protocol が継ぎ目 — `tests/mocks/` でフェイク実装を作る。

### 2.3 テストフォルダ構造

`tests/` はソースパッケージをミラー、共有 fixture・mock は最上部。

```
tests/
├── conftest.py                   # 共有 fixture（pytest が自動ロード）
├── mocks/
│   ├── __init__.py
│   ├── mock_env.py               # env var モックヘルパー
│   ├── mock_externals.py         # 外部 API クライアントスタブ
│   └── in_memory_order_repository.py  # Protocol を実装するフェイクリポジトリ
├── domain/                       # {pkg}/domain/ をミラー
│   ├── entities/
│   │   └── test_order.py
│   └── value_objects/
│       └── test_money.py
├── application/                  # {pkg}/application/ をミラー
│   └── use_cases/
│       └── test_create_order.py
├── infrastructure/               # {pkg}/infrastructure/ をミラー
│   └── persistence/
│       └── test_postgres_order_repository.py
├── interface/                    # {pkg}/interface/ をミラー
│   └── api/
│       └── routers/
│           └── test_orders_router.py
└── e2e/                          # レイヤー跨ぎシナリオ
    └── test_create_order_e2e.py
```

### 2.4 テストファイル / 関数名

| 対象 | 規約 |
|---|---|
| テストファイル | `test_{module}.py` — ソースモジュール名をミラー |
| テスト関数 | `test_{behavior}` — 検証する振る舞いを表現（呼び出しではない） |
| テストクラス（グループ化が本当に有用なときだけ） | `Test{ClassName}` |

```python
# ✅ 良い — テスト対象の振る舞いを表現
def test_returns_none_when_not_found(): ...
def test_raises_refund_window_closed_after_30_days(): ...
def test_create_order_emits_order_placed_event(): ...

# ❌ 悪い — 呼び出しを表現・振る舞いではない
def test_find_by_id(): ...
def test_refund(): ...
def test_main(): ...
```

### 2.5 ユースケーステストテンプレート

```python
# tests/application/use_cases/test_create_order.py
import pytest

from {pkg}.application.use_cases.create_order import (
    CreateOrderUseCase,
    CreateOrderInput,
)
from {pkg}.domain.entities.order import Order
from {pkg}.domain.value_objects.customer_id import CustomerId
from tests.mocks.in_memory_order_repository import InMemoryOrderRepository
from tests.mocks.fake_payment_gateway import FakePaymentGateway


@pytest.fixture
def order_repo() -> InMemoryOrderRepository:
    return InMemoryOrderRepository()


@pytest.fixture
def payments() -> FakePaymentGateway:
    return FakePaymentGateway()


@pytest.fixture
def use_case(order_repo: InMemoryOrderRepository, payments: FakePaymentGateway) -> CreateOrderUseCase:
    return CreateOrderUseCase(order_repo, payments)


def test_saves_order_and_charges_customer(use_case: CreateOrderUseCase, order_repo: InMemoryOrderRepository, payments: FakePaymentGateway) -> None:
    input = CreateOrderInput(
        customer_id=CustomerId("cust-1"),
        line_items=[...],
    )

    order = use_case.execute(input)

    saved = order_repo.find_by_id(order.id)
    assert saved is not None
    assert saved.customer_id == input.customer_id
    assert payments.charged_amount(input.customer_id) == order.total
```

### 2.6 リポジトリテストテンプレート — 実 DB

リポジトリテストは実テスト DB（コンテナ内 Postgres・テンポラリ SQLite 等）に対して書く。モックすると SQL テストの意味がなくなる。

```python
# tests/infrastructure/persistence/test_postgres_order_repository.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from {pkg}.infrastructure.persistence.postgres_order_repository import PostgresOrderRepository

@pytest.fixture
def session() -> Session:
    engine = create_engine("postgresql://test:test@localhost:5433/test_db")
    with Session(engine) as s:
        yield s
        s.rollback()  # DB をクリーンに保つ


def test_find_by_id_returns_saved_order(session: Session) -> None:
    repo = PostgresOrderRepository(session)
    order = Order(id=OrderId("o-1"), ...)
    repo.save(order)
    session.commit()

    fetched = repo.find_by_id(OrderId("o-1"))

    assert fetched is not None
    assert fetched.id == order.id
```

### 2.7 HTTP エンドポイントテストテンプレート

```python
# tests/interface/api/routers/test_orders_router.py
from fastapi.testclient import TestClient

from {pkg}.main import build_app
from tests.mocks.fake_container import build_fake_container


def test_post_orders_returns_201_on_success() -> None:
    app = build_app(container=build_fake_container())
    client = TestClient(app)

    response = client.post("/orders", json={"customer_id": "cust-1", "line_items": [...]})

    assert response.status_code == 201
    assert response.json()["id"]
```

`build_fake_container()` が同じユースケースをインメモリインフラで配線するため、テストは DB を触らずに routing + serialization + business logic を実行する。

### 2.8 パラメタライズドテスト

閉集合入力には `@pytest.mark.parametrize`：

```python
@pytest.mark.parametrize(
    ("amount", "expected_tax"),
    [
        (100, 8),
        (500, 40),
        (10_000, 800),
    ],
)
def test_calculates_tax(amount: int, expected_tax: int) -> None:
    assert calculate_tax(amount) == expected_tax
```

### 2.9 fixture — スコープと共有

| スコープ | 用途 |
|---|---|
| `function`（デフォルト） | ほとんどの fixture — テストごとに新しい状態 |
| `module` | 1テストファイルで共有する高コストセットアップ（例：webdriver 起動） |
| `session` | 真にグローバルなセットアップ（例：テストコンテナを1回起動） |
| `class` | 稀 — クラス内のテストが状態共有する必要があるとき |

広く共有する fixture は**最上位** `conftest.py`。フォルダ固有の fixture はネスト `conftest.py`（pytest が自動検出）。

---

## 3. ソース ↔ テストのリンク

ソースファイル変更時、対応するテストファイルも更新する。これはプロジェクトレベルのルール（`.claude/rules/source-test-link.md` で強制）。

| ソース変更 | テストアクション |
|---|---|
| ユースケース / リポジトリに公開メソッド追加 | 新振る舞いを検証するテスト追加 |
| 公開メソッドのシグネチャ変更 | 影響テスト更新・呼び出し元が通ることを確認 |
| バグ修正 | 修正前に失敗・修正後に通るリグレッションテスト追加 |
| 振る舞い変更なしのリファクタ | 既存テストが通ることを確認・新規追加なし |
| コード削除 | 対応テストも削除 |

テストファイルパスは機械的：`{pkg}/domain/entities/order.py` → `tests/domain/entities/test_order.py`。

---

## 4. テスト実行

### 4.1 ローカル

```bash
pytest                    # 全テスト
pytest tests/application  # 1フォルダ
pytest -k create_order    # 名前部分一致
pytest -x                 # 最初の失敗で停止
pytest --lf               # 最後に失敗したテストだけ再実行
pytest -v                 # 詳細
```

### 4.2 カバレッジ付き

```bash
pytest --cov={package_name} --cov-report=term-missing
```

カバレッジ閾値（例：80%）は `pyproject.toml` で強制：

```toml
[tool.pytest.ini_options]
addopts = "--cov={package_name} --cov-fail-under=80"
```

> カバレッジは smell 検出器であって品質指標ではない。自明な getter の高カバレッジには
> 意味がない。ユースケースとドメインロジックの高カバレッジを狙う；インフラの
> カバレッジは現実的シナリオで全ブランチが動いているかで測る。

### 4.3 テスト検出

pytest は `tests/` 配下のテストを自動検出。`pyproject.toml` で設定：

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
python_classes = ["Test*"]
```

---

## 5. Definition of Done — テストチェックリスト

変更を「完了」とする前に：

- [ ] 影響を受けるすべてのユースケースに新規/変更振る舞いを検証するテストが少なくとも1つ（§ 2.1）
- [ ] バグ修正には古いコードで失敗するリグレッションテスト（§ 3）
- [ ] モックは外部 I/O 境界のみ（§ 2.2）
- [ ] テストファイルパスがソースパスをミラー（§ 2.3）
- [ ] テスト関数名が呼び出しではなく振る舞いを表現（§ 2.4）
- [ ] `pytest` が警告なしで通る
- [ ] 変更コードのカバレッジが意味ある（行だけでなくブランチも）
- [ ] ロガーが § 1 に従う（boot シーケンスを触ったなら）
- [ ] デバッグ用 `print()` がコードに残っていない（`logger.debug` で置換）
