<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# Python アーキテクチャ規約 — py-kit（日本語ミラー）

> このファイルは `python-architecture.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `python-architecture.md` にも反映してください。

本格 Python プロジェクト向けのアーキテクチャパターンと設計原則。
`python-core.md` と合わせて読む。プロジェクト作業（新規・リファクタ・機能追加）では必須リファレンス。

---

## 1. SOLID 原則

### 1.1 S — 単一責任

各クラスには変更理由が**1つだけ**ある。サイズではなく変更の軸で分割する。

```python
# ❌ 悪い — 3つの変更理由（認証ロジック・メール書式・DBスキーマ）
class UserService:
    def authenticate(self, email: str, password: str) -> User: ...
    def send_welcome_email(self, user: User) -> None: ...
    def save(self, user: User) -> None: ...

# ✅ 良い — それぞれ理由が1つ
class AuthService:
    def authenticate(self, email: str, password: str) -> User: ...

class WelcomeEmailSender:
    def send(self, user: User) -> None: ...

class UserRepository(Protocol):
    def save(self, user: User) -> None: ...
```

**検出ヒューリスティック:**
- クラス名を説明するのに "and" が必要（`UserAndEmailService`）
- `git log` でメソッドが別の理由で変更されている
- 1つのメソッドだけが触るプライベートフィールドがある

### 1.2 O — 開放閉鎖

拡張に開き、修正に閉じる。コード追加で振る舞いを増やす — 既存クラスを編集しない。

```python
# ❌ 悪い — 形式追加のたびにこの関数を編集
def export(data: list[dict], fmt: str) -> bytes:
    if fmt == "csv":
        return _to_csv(data)
    elif fmt == "json":
        return _to_json(data)
    elif fmt == "parquet":     # 来スプリント追加
        return _to_parquet(data)
    raise ValueError(f"unknown format: {fmt}")

# ✅ 良い — 新形式 = 新クラス；既存コード編集なし
class ExportStrategy(Protocol):
    def export(self, data: list[dict]) -> bytes: ...

class CsvExporter:
    def export(self, data: list[dict]) -> bytes: ...

class JsonExporter:
    def export(self, data: list[dict]) -> bytes: ...

def export_with(strategy: ExportStrategy, data: list[dict]) -> bytes:
    return strategy.export(data)
```

OCP を厳格適用すべき場面：多くのモジュールから**読まれる**コード。やりすぎな場面：呼び出し元のない葉コード。

### 1.3 L — リスコフ置換

サブクラスは呼び出し元を壊さず基底クラスを置換できねばならない。以下は絶対禁止：

- 事後条件を弱める（基底が約束する以下しか返さない）
- 事前条件を強める（基底以上を呼び出し元に求める）
- 基底がドキュメント化していない例外を投げる

```python
# ❌ 悪い — サブクラスが raise・呼び出し元全部が壊れる
class FileRepository(Protocol):
    def save(self, content: bytes) -> None: ...

class ReadOnlyFileRepository:
    def save(self, content: bytes) -> None:
        raise NotImplementedError("read-only")  # LSP 違反

# ✅ 良い — Protocol を分割し、呼び出し元は必要なものだけ求める
class FileReader(Protocol):
    def read(self) -> bytes: ...

class FileWriter(Protocol):
    def write(self, content: bytes) -> None: ...

class ReadOnlyFile(FileReader):
    def read(self) -> bytes: ...

class ReadWriteFile(FileReader, FileWriter):
    def read(self) -> bytes: ...
    def write(self, content: bytes) -> None: ...
```

### 1.4 I — インターフェース分離

巨大な汎用インターフェース1つより、小さく専用な Protocol を多数。クライアントは使うものにだけ依存する。

```python
# ❌ 悪い — 使わなくても stat / list を受け入れる必要がある
class IStorage(Protocol):
    def read(self, path: str) -> bytes: ...
    def write(self, path: str, content: bytes) -> None: ...
    def delete(self, path: str) -> None: ...
    def list(self, prefix: str) -> list[str]: ...
    def stat(self, path: str) -> StorageStat: ...

# ✅ 良い — クライアントは必要最小限の Protocol に依存
class Readable(Protocol):
    def read(self, path: str) -> bytes: ...

class Writable(Protocol):
    def write(self, path: str, content: bytes) -> None: ...

class Listable(Protocol):
    def list(self, prefix: str) -> list[str]: ...

class ReadWritable(Readable, Writable, Protocol):
    """両方必要なクライアント向けに小さい Protocol を合成。"""
```

### 1.5 D — 依存性逆転

上位モジュールは具体実装ではなく抽象に依存する。コンストラクタで注入する。

```python
# ❌ 悪い — ReportService が PostgresDatabase に固定される
class ReportService:
    def __init__(self) -> None:
        self.db = PostgresDatabase()

# ✅ 良い — Protocol に依存・具体クラスは注入
class ReportService:
    def __init__(self, repo: UserRepository) -> None:  # UserRepository は Protocol
        self._repo = repo
```

**検出ヒューリスティック:** 実 DB・HTTP・ファイルシステムなしにテスト不可なら、DIP 違反。修正は Protocol 抽出＋テストでフェイク注入。

---

## 2. DRY 原則 — 慎重に

抽出は**安定した名前付き概念**が裏にあるときだけ。似た3行は、名前のない抽象化より良い。

| 重複種別 | 抽出時期 | 抽出先 |
|---|---|---|
| 3箇所以上の同じリテラル値 | ほぼ常に | `constants.py` の定数 |
| 同じビジネスルールが2通りに書かれている | 常に | ドメイン意味のある名前の関数 |
| 複数機能を跨ぐ同じクラス構造 | 概念に名前がついたとき（`Repository`・`Aggregate`・`EventHandler`） | 基底クラスかジェネリック |
| 同じ設定キー | 常に | ドキュメント化された設定ファイル / 環境変数 |
| 異なるドメインで似て見えるコード | **絶対に NO** | 偶然の類似 |

```python
# ❌ 悪い — 偽 DRY："process_with_logging" はドメイン概念ではない
def process_user(u: User) -> None: ...
def process_order(o: Order) -> None: ...
def process_with_logging(item: Any) -> None:  # 過剰抽象化
    logger.info("processing %s", item)
    ...

# ✅ 良い — 「X をロギング付き処理」という概念は存在しないので重複を残す
def process_user(u: User) -> None:
    logger.info("processing user %s", u.id)
    ...

def process_order(o: Order) -> None:
    logger.info("processing order %s", o.id)
    ...
```

迷ったら**3つ目**まで待ってから抽出する。

---

## 3. レイヤードアーキテクチャ — 純DDD

py-kit の標準レイアウトは**純粋なドメイン駆動設計**：domain が中心、application
がユースケースを調整、infrastructure が外部関心を実装、interface が外部世界と
ユースケースを翻訳。

### 3.1 依存方向（硬性ルール）

```
interface ──┐
            ├─► application ──► domain
infrastructure ──┘                ▲
                                  │
infrastructure は domain で定義された Protocol を実装する
```

| レイヤー | importしてよい | importしてはいけない |
|---|---|---|
| `domain/` | stdlib・`typing`・`pydantic`（境界モデルのみ） | application・infrastructure・interface・外部SDK |
| `application/` | domain・stdlib | infrastructure・interface・外部SDK |
| `infrastructure/` | domain（Protocol 実装）・application（稀）・stdlib・サードパーティ SDK | interface |
| `interface/` | application・domain（読み取り — 型アノテーション等） | infrastructure |

ルール違反はリファクタ債務 — `if TYPE_CHECKING` での回避はしない。

### 3.2 レイヤーの役割

| レイヤー | 責務 | モジュール例 |
|---|---|---|
| `interface/` | 外部（HTTP・CLI・GUI）→ ユースケース呼び出しに翻訳。結果も翻訳して返す。ビジネスロジックなし。 | `interface/cli/main.py`・`interface/api/routers/users.py` |
| `application/` | ユースケース調整：ユースケース入力を受け、ドメインサービスとリポジトリを正しい順序で呼び、ユースケース出力を返す。 | `application/use_cases/create_order.py` |
| `domain/` | 純粋なビジネスルール。エンティティ・値オブジェクト・ドメインサービス・リポジトリと外部サービスの Protocol 定義。 | `domain/entities/order.py`・`domain/repositories/order_repository.py` |
| `infrastructure/` | domain Protocol の具体実装。DB クライアント・HTTP アダプタ・ファイル I/O・メッセージキュー。 | `infrastructure/persistence/postgres_order_repository.py`・`infrastructure/external_apis/stripe_client.py` |

### 3.3 境界ルール — domain に Protocol・infrastructure に実装

外部サービスに触れるコードは必ず：

1. **Protocol** を `domain/repositories/` か `domain/services/` に定義
2. **具体実装** を `infrastructure/` に置く
3. composition root で**配線**（§ 5）

```python
# domain/repositories/order_repository.py — 外部ライブラリの import 禁止
from typing import Protocol
from {pkg}.domain.entities.order import Order

class OrderRepository(Protocol):
    def find_by_id(self, order_id: OrderId) -> Order | None: ...
    def save(self, order: Order) -> None: ...

# infrastructure/persistence/postgres_order_repository.py — 具体実装
import psycopg
from {pkg}.domain.entities.order import Order
from {pkg}.domain.repositories.order_repository import OrderRepository

class PostgresOrderRepository:
    def __init__(self, conn: psycopg.Connection) -> None:
        self._conn = conn

    def find_by_id(self, order_id: OrderId) -> Order | None: ...
    def save(self, order: Order) -> None: ...
```

これにより：

- ビジネスロジック層はどの外部サービスを使うかを知らない
- ビジネスロジックを触らずに外部サービスを差し替えられる
- テストは実インフラ抜きでフェイクを注入できる

### 3.4 アーキテクチャ品質チェックリスト

- [ ] `domain/` は stdlib・内部モジュール・`typing`・（任意で）Pydantic のみ import — 外部 SDK なし
- [ ] `application/` は `domain/` と stdlib のみ import — infrastructure import なし
- [ ] すべての Protocol は `domain/` に定義；実装は `infrastructure/` に存在
- [ ] `domain/` および `application/` 内で外部ライブラリの具体クラスをインスタンス化しない
- [ ] すべての境界で依存性注入 — コンストラクタが具体クラスではなく Protocol を受け取る
- [ ] composition root（`main.py` または `container.py`）が唯一の具体クラス組み立て場所

---

## 4. ハードコード禁止

設定値をソースコードに直接埋め込まない。`.env`・設定ファイル・`constants.py`（計算済みパスのみ）に置く。

### 4.1 何がハードコードか

| 値種別 | 置き場所 |
|---|---|
| URL・エンドポイント | `.env` → `config.py` |
| ポート | `.env` → `config.py` |
| ファイルパス | `constants.py`（`__file__` 由来なら）or `.env`（絶対パスなら） |
| 認証情報・APIキー | `.env`（コミット禁止） |
| リトライ・タイムアウト値 | `.env` か `config.py` |
| フィーチャーフラグ | `.env` か設定ファイル |
| マジックナンバー | 意味のある名前のモジュール定数 |
| ユーザー向けエラーメッセージ | 設定ファイル / テンプレートファイル |

### 4.2 例

```python
# ❌ 悪い — 全部ハードコード
class ApiClient:
    def fetch(self, path: str) -> dict:
        return httpx.get(
            f"https://api.example.com{path}",     # URL ハードコード
            timeout=30.0,                          # timeout ハードコード
            headers={"X-Api-Key": "sk-abc123"},   # 認証情報ハードコード
        ).json()

# ✅ 良い — 外部化
# constants.py
PROJECT_ROOT: Path = Path(__file__).parent.parent
LOG_DIR: Path = PROJECT_ROOT / "log"

# config.py
class Settings(BaseModel):
    api_base_url: str
    api_timeout: float = 30.0
    api_key: SecretStr

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            api_base_url=os.environ["API_BASE_URL"],
            api_timeout=float(os.environ.get("API_TIMEOUT", "30.0")),
            api_key=SecretStr(os.environ["API_KEY"]),
        )

# api_client.py
class ApiClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def fetch(self, path: str) -> dict:
        return httpx.get(
            f"{self._settings.api_base_url}{path}",
            timeout=self._settings.api_timeout,
            headers={"X-Api-Key": self._settings.api_key.get_secret_value()},
        ).json()
```

### 4.3 `.env.sample` は仕様書

`.env.sample` はプロジェクトが読むすべての環境変数をドキュメント化する。git 管理対象（`.env` は対象外）。

```bash
# .env.sample — アプリが読むすべてのキー・プレースホルダー値・コメント付き
# 外部 API のベース URL
API_BASE_URL=https://api.example.com
# 外部 API のタイムアウト（秒）
API_TIMEOUT=30.0
# 外部 API の認証キー（コミット禁止）
API_KEY=sk-replace-me
```

CI チェック：`.env.sample` をロード・パースし、各キーがコードベースのどこかで消費されていることを検証するテスト。

### 4.4 `constants.py` — 計算済みパスのみ

`constants.py` は import 時に計算されるパスだけのためにある。ビジネス定数・マジックナンバー・設定可能値は置かない。

```python
# ✅ 良い
PROJECT_ROOT: Path = Path(__file__).parent.parent
LOG_DIR: Path = PROJECT_ROOT / "log"
TEMPLATE_DIR: Path = PROJECT_ROOT / "templates"

# ❌ 悪い — これらは設定可能値・計算済みではない
MAX_RETRY = 3
API_BASE_URL = "https://api.example.com"
DEFAULT_LANGUAGE = "ja"
```

---

## 5. Composition Root と依存性注入

### 5.1 Composition Root とは

唯一の場所：

- すべての具体クラスをインスタンス化
- すべての依存を配線
- Settings をロード

通常 `main.py`（CLI）か `container.py`（FastAPI サービス）。他のすべてのファイルはコンストラクタ経由で依存を受け取る。

### 5.2 最小 Composition Root

```python
# main.py
def build_container() -> Container:
    settings = Settings.from_env()
    logger = setup_logger(LOG_DIR)

    # infrastructure
    db_conn = psycopg.connect(settings.database_url)
    order_repo = PostgresOrderRepository(db_conn)
    stripe_client = StripeClient(settings.stripe_api_key)

    # application
    create_order = CreateOrderUseCase(order_repo, stripe_client)
    cancel_order = CancelOrderUseCase(order_repo, stripe_client)

    return Container(
        create_order=create_order,
        cancel_order=cancel_order,
        logger=logger,
    )

def main() -> None:
    container = build_container()
    # container をエントリポイントに渡す
    ...

if __name__ == "__main__":
    main()
```

### 5.3 コンストラクタ注入 — 必須

クラスが必要とする協調者は `__init__` で渡す。絶対 NG：

```python
# ❌ 悪い — ボディ内で具体クラスをインスタンス化
class CreateOrderUseCase:
    def __init__(self) -> None:
        self._repo = PostgresOrderRepository(...)
        self._payments = StripeClient(...)

# ❌ 悪い — グローバルシングルトン参照
class CreateOrderUseCase:
    def execute(self, ...) -> Order:
        repo = ServiceLocator.get(OrderRepository)
        ...
```

```python
# ✅ 良い — 協調者は注入
class CreateOrderUseCase:
    def __init__(
        self,
        order_repo: OrderRepository,
        payments: PaymentGateway,
    ) -> None:
        self._order_repo = order_repo
        self._payments = payments

    def execute(self, input: CreateOrderInput) -> Order:
        ...
```

### 5.4 Container クラス（大規模プロジェクト向け・任意）

ユースケースが20+ ある場合、`Container` dataclass でまとめる：

```python
@dataclass(frozen=True)
class Container:
    create_order: CreateOrderUseCase
    cancel_order: CancelOrderUseCase
    fulfill_order: FulfillOrderUseCase
    logger: logging.Logger
```

FastAPI には `app.state` 経由、CLI には main 関数経由で渡す。

重い DI フレームワーク（`dependency-injector`・`injector`）は手動配線で本当に手に余るまで避ける。明示的な `main.py` 配線がデフォルト。

---

## 6. デザインパターン

### 6.1 Strategy

交換可能なアルゴリズムを Protocol の後ろに隠す。使う場面：

- 複数アルゴリズムで同じ結果を出す
- 実行時に選択（設定・ユーザー入力・プラグイン選択）
- 将来新アルゴリズムが追加される可能性

```python
class SortStrategy(Protocol):
    def sort(self, items: list[int]) -> list[int]: ...

class QuickSort:
    def sort(self, items: list[int]) -> list[int]: ...

class MergeSort:
    def sort(self, items: list[int]) -> list[int]: ...

# 呼び出し元が選ぶ
def process(items: list[int], strategy: SortStrategy) -> list[int]:
    return strategy.sort(items)
```

Strategy は**呼び出し元**にアルゴリズム制御を渡す — いつでも strategy を入れ替えられる。

### 6.2 Template Method

基底クラスでアルゴリズムの骨格を定義し、サブクラスは**変わる部分**だけオーバーライドする。使う場面：

- 全体フローが固定（バリデーション → 変換 → 永続化 → 通知）
- 特定ステップだけ具体型ごとに異なる
- 順序強制をサブクラスではなくフレームワークに任せたい

```python
from abc import ABC, abstractmethod

class ReportGenerator(ABC):
    """Template Method：レポート生成アルゴリズムを定義。
    サブクラスは _load と _format だけオーバーライド・フロー固定。"""

    def generate(self, source: str) -> bytes:
        raw = self._load(source)
        validated = self._validate(raw)
        formatted = self._format(validated)
        return self._render(formatted)

    @abstractmethod
    def _load(self, source: str) -> dict: ...

    def _validate(self, data: dict) -> dict:
        """デフォルト実装 — 厳密化が必要ならサブクラスでオーバーライド。"""
        if not data:
            raise EmptyReportSourceError(source)
        return data

    @abstractmethod
    def _format(self, data: dict) -> dict: ...

    def _render(self, data: dict) -> bytes:
        """デフォルト実装 — JSON。CSV/PDF 等はオーバーライド。"""
        return json.dumps(data).encode("utf-8")


class SalesReportGenerator(ReportGenerator):
    def _load(self, source: str) -> dict:
        return self._sales_repo.fetch(source)

    def _format(self, data: dict) -> dict:
        return {"total": sum(row["amount"] for row in data["rows"])}


class CsvSalesReportGenerator(SalesReportGenerator):
    def _render(self, data: dict) -> bytes:
        return to_csv(data).encode("utf-8")
```

#### Template Method vs Strategy — どちらを選ぶか

| 観点 | Template Method | Strategy |
|---|---|---|
| アルゴリズムフローを誰が制御するか | 基底クラス（固定） | 呼び出し元（自由） |
| 変化点はどこに住むか | サブクラスでの特定ステップオーバーライド | Protocol 実装クラスで分離 |
| 結合度 | 強い — サブクラスは基底を継承 | 緩い — strategy は合成される |
| 使う場面 | フロー不変・ステップが変わる | アルゴリズム自体が変わる・フローは付随 |
| リスク | サブクラスが事後条件を弱めると LSP 違反 | 特になし |

**Template Method を選ぶ場面：** "フレームワークがこの順序でステップを実行する；スキップ・順序入れ替え不可；穴を埋めるだけ" を強制したいとき。

**Strategy を選ぶ場面：** 変化点がアルゴリズムそのもの・呼び出し元が自由に strategy を入れ替えたいとき。

### 6.3 Factory

オブジェクト生成ロジックを集中。使う場面：

- 構築が複雑・条件分岐がある
- どの具体クラスが返るか呼び出し元が知る必要なし

```python
def create_exporter(fmt: Literal["csv", "json", "parquet"]) -> ExportStrategy:
    match fmt:
        case "csv":     return CsvExporter()
        case "json":    return JsonExporter()
        case "parquet": return ParquetExporter()
```

構築が複雑（任意の協調者多数）な場合は builder スタイルの Factory クラス。

### 6.4 Decorator

横断的振る舞い（ロギング・キャッシュ・リトライ・メトリクス）を元クラスを変えずに追加。使う場面：

- 横断関心が複数の無関係なクラスに適用される
- 振る舞いを合成したい（ロギング + キャッシュ + リトライ）

```python
class LoggingRepository:
    """Decorator：別の UserRepository をラップ・各呼び出しでログ追加。"""

    def __init__(self, inner: UserRepository, logger: logging.Logger) -> None:
        self._inner = inner
        self._logger = logger

    def find_by_id(self, user_id: UserId) -> User | None:
        self._logger.debug("find_by_id %s", user_id)
        result = self._inner.find_by_id(user_id)
        self._logger.debug("find_by_id %s -> %s", user_id, "hit" if result else "miss")
        return result

    def save(self, user: User) -> None:
        self._logger.debug("save %s", user.id)
        self._inner.save(user)
```

Decorator は合成可能：`RetryRepository(LoggingRepository(PostgresUserRepository(conn)))`。

### 6.5 Observer（控えめに使う）

複数 observer に通知。以下のときだけ使う：

- 関連のない複数のサブシステムが同じイベントに反応する必要
- publisher が listener を知らないべき

ほとんどの Python アプリでは直接呼び出し（または `asyncio.Queue` / `asyncio.Event`）で十分。Observer は間接化のコストに見合うときだけ。

---

## 7. Pydantic の適用境界

実行時バリデーションが必要なシステム境界では Pydantic モデル（型ヒントだけでない）を使う。

### 7.1 Pydantic を使う場面

| 用途 | Pydantic？ |
|---|---|
| 外部 HTTP リクエストボディ・レスポンス | ✅ Yes |
| Instructor 経由の LLM 入出力 | ✅ Yes |
| 設定ファイル読み込み（YAML/JSON/`.env`） | ✅ Yes |
| プロセス・スレッド間のシリアライズ済みデータ | ✅ Yes |
| CSV/JSONL レコード（1行=1モデル） | ✅ Yes |
| ユーザー入力パース（CLI 引数・フォーム） | ✅ Yes |
| 既に上流でバリデート済みの内部関数引数 | ❌ No — 型ヒントで十分 |
| 1関数内に留まる dict/list 式 | ❌ No |
| 純粋な dataclass 用途（バリデーションなし） | ❌ `@dataclass` を使う |

### 7.2 境界パターン

境界でバリデート・型付きオブジェクトを内側へ・出力境界で raw 型に戻す。

```python
# interface/api/routers/orders.py — 入力境界
class CreateOrderRequest(BaseModel):
    customer_id: str
    line_items: list[LineItem]

@router.post("/orders")
async def create_order(body: CreateOrderRequest, container: Container = Depends(...)) -> dict:
    input = CreateOrderInput(customer_id=CustomerId(body.customer_id), line_items=body.line_items)
    order = container.create_order.execute(input)
    return CreateOrderResponse.from_domain(order).model_dump()
```

### 7.3 Pydantic v2 パターン

```python
from pydantic import BaseModel, Field, model_validator

class Settings(BaseModel):
    api_base_url: str = Field(..., min_length=1)
    api_timeout: float = Field(default=30.0, ge=0.1, le=600.0)
    feature_flags: dict[str, bool] = Field(default_factory=dict)

    @model_validator(mode="after")
    def check_timeout_consistency(self) -> "Settings":
        # フィールド間バリデーション
        return self
```

新規コードでは `BaseModel` を `pydantic.dataclasses.dataclass` より優先 — ツールサポートが良い。

---

## 8. プロジェクトフォルダ構成 — 純DDD（標準）

py-kit の標準レイアウトは**純粋なドメイン駆動設計**。フォルダ役割は固定 — 各フォルダ内のファイル名だけプロジェクト依存。

```
{project_name}/
├── pyproject.toml
├── README.md
├── .env.sample
├── .gitignore
├── activate.bat                  # Windows のみ
├── {mode}.bat                    # Windows のみ — 実行モード別エントリ
├── setup/
│   └── setup_venv.bat            # Windows のみ
├── {package_name}/
│   ├── __init__.py
│   ├── __main__.py               # `python -m {package_name}` のエントリ
│   ├── main.py                   # composition root（§ 5）
│   ├── config.py                 # Settings モデル + from_env ローダー
│   ├── constants.py              # 計算済みパスのみ（マジック値禁止）
│   ├── logger.py                 # setup_logger() — python-testing.md 参照
│   ├── exceptions.py             # 横断的例外基底クラス
│   ├── interface/                # 外部 ↔ ユースケースの翻訳
│   │   ├── __init__.py
│   │   ├── cli/                  # CLI エントリ（あれば）
│   │   │   └── main.py
│   │   └── api/                  # HTTP ルート（FastAPI の場合 — python-fastapi.md 参照）
│   │       ├── __init__.py
│   │       ├── routers/
│   │       │   ├── orders.py
│   │       │   └── users.py
│   │       ├── dependencies.py
│   │       └── middleware.py
│   ├── application/              # ユースケース調整
│   │   ├── __init__.py
│   │   └── use_cases/
│   │       ├── create_order.py
│   │       ├── cancel_order.py
│   │       └── list_orders.py
│   ├── domain/                   # 純粋なビジネスルール — 外部依存禁止
│   │   ├── __init__.py
│   │   ├── entities/
│   │   │   ├── order.py
│   │   │   ├── customer.py
│   │   │   └── line_item.py
│   │   ├── value_objects/
│   │   │   ├── order_id.py       # NewType("OrderId", str) または BaseModel
│   │   │   ├── money.py
│   │   │   └── address.py
│   │   ├── repositories/         # Protocol 定義のみ
│   │   │   ├── order_repository.py
│   │   │   ├── customer_repository.py
│   │   │   └── payment_gateway.py
│   │   ├── services/             # ドメインサービス（複数エンティティ跨ぐロジック）
│   │   │   └── order_pricing_service.py
│   │   └── events/               # ドメインイベント（任意）
│   │       └── order_placed.py
│   └── infrastructure/           # 具体実装
│       ├── __init__.py
│       ├── persistence/          # DB / ファイルリポジトリ
│       │   ├── postgres_order_repository.py
│       │   ├── in_memory_order_repository.py
│       │   └── postgres_customer_repository.py
│       ├── external_apis/        # サードパーティ HTTP/SDK アダプタ
│       │   ├── stripe_payment_gateway.py
│       │   └── sendgrid_email_sender.py
│       └── messaging/            # メッセージキュー（任意）
│           └── sqs_event_publisher.py
├── tests/
│   ├── conftest.py
│   ├── mocks/
│   │   ├── mock_env.py
│   │   └── mock_externals.py
│   ├── domain/                   # ソース domain/ をミラー
│   │   └── entities/
│   │       └── test_order.py
│   ├── application/
│   │   └── use_cases/
│   │       └── test_create_order.py
│   ├── infrastructure/
│   │   └── persistence/
│   │       └── test_postgres_order_repository.py
│   └── e2e/                      # エンドツーエンド（CLI/API）
│       └── test_create_order_e2e.py
└── log/                          # 実行時生成 — `.gitkeep` で空保持・git ignore
    └── .gitkeep
```

### 8.1 レイヤーフォルダのルール

| フォルダ | 入れるもの | 入れないもの |
|---|---|---|
| `domain/entities/` | エンティティクラス（識別子を持つ可変オブジェクト） | DB 行クラス・DTO・JSON dict |
| `domain/value_objects/` | 値オブジェクトクラス（不変・値等価） | 識別子を持つもの |
| `domain/repositories/` | 永続化の Protocol 定義 | 具体リポジトリクラス |
| `domain/services/` | 複数エンティティ跨ぐドメインサービス | ユースケース（`application/`） |
| `application/use_cases/` | 1ユースケース = 1クラス | ドメインロジック・インフラコード |
| `infrastructure/persistence/` | 具体リポジトリ実装 | Protocol 定義 |
| `infrastructure/external_apis/` | サードパーティ HTTP/SDK アダプタ | ビジネスロジック |
| `interface/` | ルートハンドラ・CLI パーサ・GUI イベント | ビジネスロジック |

### 8.2 ファイル毎クラスルール

公開クラスごとに1ファイル。ファイル名は `snake_case` のクラス名：

| クラス | ファイル |
|---|---|
| `Order` | `domain/entities/order.py` |
| `OrderRepository`（Protocol） | `domain/repositories/order_repository.py` |
| `PostgresOrderRepository` | `infrastructure/persistence/postgres_order_repository.py` |
| `CreateOrderUseCase` | `application/use_cases/create_order.py` |

1箇所だけで使われるプライベートヘルパー・小 dataclass は呼び出し元と同居可。

### 8.3 テストミラールール

`tests/` はソースフォルダ構造をミラー。`{pkg}/domain/entities/order.py` のテストは `tests/domain/entities/test_order.py`。

レイヤー跨ぎの E2E テストは `tests/e2e/`。

---

## 9. Definition of Done — アーキテクチャチェックリスト

アーキテクチャ変更を「完了」とする前に確認：

- [ ] すべての Protocol が `domain/` に定義；`infrastructure/` に Protocol なし
- [ ] `domain/` ファイルが外部 SDK を import しない
- [ ] `application/` ファイルが `infrastructure/` から import しない
- [ ] 各ユースケースが単一 `execute()` メソッドのクラス
- [ ] すべての依存がコンストラクタを通る（service-locator なし・グローバルシングルトンなし）
- [ ] composition root（`main.py` か `container.py`）が唯一の具体クラスインスタンス化場所
- [ ] URL・認証情報・パスのハードコードなし — `.env` か `constants.py`（§ 4）
- [ ] `.env.sample` がアプリの読むすべてのキーをコメント付きで列挙
- [ ] Pydantic モデルがすべてのシステム境界を守っている（§ 7）
- [ ] フォルダレイアウトが § 8 に従う
- [ ] 新パターン追加時、適切なものか確認済み — § 6（Strategy vs Template Method vs Decorator）
