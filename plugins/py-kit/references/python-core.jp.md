<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# Python コア規約 — py-kit（日本語ミラー）

> このファイルは `python-core.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `python-core.md` にも反映してください。

すべての Python タスクで必須となるベースライン。Python コードを書く・編集する前に
通しで読むこと。セクションを飛ばすと規約を破るコードが量産される。

---

## 1. 命名規則

### 1.1 命名テーブル

コードベース内のすべての名前は、以下のいずれかのパターンに従う。例外なし。

| 対象 | 規約 | 良い例 | 悪い例 |
|---|---|---|---|
| モジュール / ファイル | `snake_case` | `user_repository.py` | `UserRepository.py`、`user-repo.py` |
| パッケージディレクトリ | `snake_case` | `external_apis/` | `ExternalApis/`、`external-apis/` |
| クラス | `PascalCase` | `UserRepository`、`OrderId` | `user_repository`、`orderID` |
| 例外クラス | `PascalCase` + `Error` 接尾辞 | `OrderNotFoundError` | `OrderNotFoundException`、`OrderNotFound` |
| 関数 / メソッド | `snake_case`・動詞始まり | `find_by_id()`、`save()` | `findById()`、`Save()`、`user()` |
| 変数 / 引数 | `snake_case`・名詞始まり | `user_id`、`order_total` | `userId`、`OrderTotal` |
| モジュール定数 | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` | `MaxRetryCount`、`max_retry_count` |
| プライベート（モジュール/クラス） | 先頭 `_` | `_internal_cache`、`_build_query()` | `internalCache`、`__build_query` |
| 名前マングリング | 先頭 `__`（末尾なし） | クラス内 `__id` | 本当に必要な場面でだけ使う |
| Protocol / インターフェース | プロジェクト内で**1スタイルに統一**: `{Name}able`・`I{Name}`・`Base{Name}` | `Convertable`・`IConverter`・`BaseConverter` | 1プロジェクト内で複数スタイルを混用 |
| 型エイリアス | `PascalCase` | `UserId = NewType("UserId", str)` | `user_id_t`、`t_user_id` |
| TypeVar | 大文字1文字 or `PascalCase`+`T` 接尾辞 | `T`、`K`、`V`、`EntityT` | `entity_t`、`tEntity` |
| テストファイル | `test_{module}.py`（ソース構造をミラー） | `tests/users/test_user_repository.py` | `user_repo_test.py`、`UserRepoTests.py` |
| テスト関数 | `test_{behavior}` | `test_returns_none_when_not_found()` | `test_1()`、`testReturnsNone()` |
| Fixture（pytest） | `snake_case` | `def user_repo() -> UserRepository:` | `def UserRepo():` |

### 1.2 動詞始まり / 名詞始まり

関数名は動詞で始める。変数・属性は名詞で始める。

```python
# ✅ 良い
def fetch_user(user_id: UserId) -> User: ...
def is_valid(value: str) -> bool: ...
def has_permission(user: User, perm: Permission) -> bool: ...

current_user: User = ...
order_count: int = 0

# ❌ 悪い — 関数が名詞始まり、変数が動詞始まり
def user(user_id: UserId) -> User: ...        # 「何をするか」が見えない
def validity(value: str) -> bool: ...
fetch: User = ...                             # 「何」ではなく「するか」
```

### 1.3 Protocol / インターフェースの命名スタイル — 1つに統一

プロジェクト全体で**1スタイル**に統一する。混用しない。

| スタイル | パターン | 例 |
|---|---|---|
| 形容詞型 | `{Name}able` | `Convertable`、`Readable`、`Cacheable` |
| Hungarian-I | `I{Name}` | `IConverter`、`IReader`、`ICache` |
| Base 接頭型 | `Base{Name}` | `BaseConverter`、`BaseReader`、`BaseCache` |

> 推奨：純粋な Protocol（共有実装なし）には **`{Name}able` スタイル**、ABC で共有
> 実装を持つ場合は **`Base{Name}` スタイル**。プロジェクトの `CLAUDE.md` に
> 選んだスタイルを明記する。

### 1.4 実装クラスの命名

Protocol の実装クラスは、実装技術を接頭辞にする：

```python
# domain/repositories/user_repository.py
class UserRepository(Protocol):
    def find_by_id(self, user_id: UserId) -> Optional[User]: ...

# infrastructure/persistence/postgres_user_repository.py
class PostgresUserRepository:
    def find_by_id(self, user_id: UserId) -> Optional[User]: ...

# infrastructure/persistence/in_memory_user_repository.py
class InMemoryUserRepository:
    def find_by_id(self, user_id: UserId) -> Optional[User]: ...
```

ファイル名はクラス名に従う：`postgres_user_repository.py`（`user_repository_postgres.py` ではない）。

### 1.5 真偽値の命名

真偽値変数・属性・関数は状態動詞で始める：`is_`・`has_`・`can_`・`should_`・`was_`・`will_`。

```python
# ✅ 良い
is_active: bool = True
has_permission: bool = False
def can_edit(user: User, post: Post) -> bool: ...
def should_retry(error: Exception) -> bool: ...

# ❌ 悪い
active: bool = True              # 状態か命令か曖昧
permission: bool = False         # 名詞・真偽ではない
def edit_check(...): ...         # 動作始まり・状態始まりではない
```

### 1.6 コレクションの命名

コレクション変数は複数形にする。

```python
# ✅ 良い
users: list[User] = []
user_ids: set[UserId] = set()
user_by_id: dict[UserId, User] = {}

# ❌ 悪い
user_list: list[User] = []       # 型接尾辞は冗長（アノテーションが list だと言っている）
ids: set[UserId] = set()         # 何の id か曖昧
user_map: dict[...] = {}         # キーが何か曖昧
```

dict は `{value}_by_{key}` を `{key}_to_{value}` や `{key}_{value}_map` より好む。

---

## 2. コメントルール

### 2.1 何にコメントするか・何にしないか

コメントは**なぜ**を書く。**何**は書かない（コードがすでに言っている）。

| コメント種別 | 必須？ | 補足 |
|---|---|---|
| スクリプトエントリのモジュール docstring | ✅ 必須（スクリプトのみ — `python-scripts.md` 参照） | 最低3行：name — purpose、usage 行 |
| ライブラリモジュールのモジュール docstring | ⚠️ 任意（モジュール目的が非自明な場合のみ） | 1行以内 |
| クラス docstring | ⚠️ 任意（クラスに微妙な不変条件がある場合のみ必須） | 1行・シグネチャ再記述禁止 |
| 関数 / メソッド docstring | ⚠️ 任意（隠れた制約・副作用・非自明な返り値があるとき必須） | 1行・`:param:`/`:returns:` ブロック禁止 |
| 非自明な制約・回避策のインラインコメント | ✅ 必須（その制約があるなら） | 1行・`# ` で開始 |
| 変更履歴コメント | ✅ 必須（特定PRで非自明な決定があったとき） | `# PR{N}: {何をなぜ}` |
| コードを言い換えるコメント | ❌ 禁止 | コードが仕様 |
| アノテーションにある型情報の説明 | ❌ 禁止 | 型ヒントが仕様 |

### 2.2 良い例 / 悪い例

```python
# ✅ 良い — 隠れた制約を説明
# CP932 で bat ファイルがパースされる — 日本語UTF-8バイトがリードバイトとして誤認され後続文字を飲み込む
bat_text.encode("ascii", errors="strict")

# ✅ 良い — 特定バグへの回避策を説明
# vendored anthropic SDK 0.34 は空 delta で StreamError を投げる — スキップする
if not chunk.delta:
    continue

# ✅ 良い — コードから自明でないビジネス意図を説明
# 返金期限は注文日ではなく**発送日**から30日（法的要件）
if (today - order.shipped_at).days > 30:
    raise RefundWindowClosedError()

# ❌ 悪い — コードを言い換え
# is_open を True にする
self.is_open = True

# ❌ 悪い — 型アノテーションを言い換え
# user_id は文字列
user_id: str = "..."

# ❌ 悪い — 関数名を言い換え
# この関数は合計を計算する
def calculate_total(items: list[Item]) -> int: ...

# ❌ 悪い — 価値を生まない長い docstring
def find_by_id(user_id: UserId) -> Optional[User]:
    """
    Find a user by id.

    :param user_id: The id of the user to find.
    :returns: The user if found, None otherwise.
    """
```

### 2.3 docstring ルール

docstring が必要な場合は1行・1物理行に書く：

```python
# ✅ 良い — 1行・意図のみ
def find_by_id(user_id: UserId) -> Optional[User]:
    """Return the user or None if not found. Hits the read replica, not primary."""
    ...

# ✅ 良い — 1行・振る舞いのみ
def refund(order: Order) -> RefundReceipt:
    """Issue a refund. Raises RefundWindowClosedError after 30 days from ship date."""
    ...
```

複数段落 docstring・`:param:`/`:returns:`/`Args:`/`Returns:` ブロック・RST/Sphinx
マークアップは禁止。構造化された説明が必要なら、それは：

- 関数の責務過多のサイン（分割せよ）、または
- 意図はクラス docstring か モジュール冒頭ノートに書くべき内容

### 2.4 変更履歴コメント

特定 PR で非自明な変更があった場合、PR 番号と理由を1行で残す：

```python
# ✅ 良い
# PR142: 後方互換のため order_date を残す — 新規コードは shipped_at を読む
order_date: datetime
shipped_at: datetime

# PR98: logger.py が constants から PROJECT_ROOT を読むので config.load() より前にインポート
import constants  # noqa: E402

# ❌ 悪い — PR番号なし・理由なし
# legacy フィールド
order_date: datetime
```

変更履歴コメントは古びる — 周辺コードがリライトされたらコメントも削除する。

### 2.5 セクションマーカーコメント（スクリプトのみ）

単一ファイルスクリプトでは、import・定数・ヘルパー・main をセクションマーカーで区切る。
正確な書式は `python-scripts.md` 参照。

### 2.6 禁止コメントパターン

- 担当者・Issue リンクなしの `# TODO:` — 直接修正するか、Issue を立ててリンク：`# TODO(#142): retry を追加`
- 文脈なしの `# XXX:` / `# FIXME:` — 無意味；直すか先送り理由を書く
- コメントアウトされたコードブロック — 削除する；git に履歴がある
- 関数ボディ内の ASCII アート区切り線 — コードブロックはすでに視覚的に区切られている

---

## 3. 型ヒント

### 3.1 網羅 — 全箇所適用

すべての公開シンボルに完全アノテーションを付ける。内部ヘルパーは推奨だが必須ではない。

| 位置 | 必須？ |
|---|---|
| 関数引数 | ✅ 常時 |
| 関数戻り値 | ✅ 常時 — 手続きの `-> None` も含む |
| クラス属性（宣言） | ✅ 常時 |
| `dataclass` / Pydantic フィールド | ✅ 常時 |
| `__init__` パラメータ | ✅ 常時 |
| RHS から型が推論できるローカル変数 | ⚠️ 任意 |
| 型が非自明なローカル変数 | ✅ 必須（例: `x: dict[str, list[int]] = {}`） |
| Lambda | ⚠️ 任意（1式以上なら `def` を使う） |

```python
# ✅ 良い — 全公開シンボルにアノテーション
def fetch_user(user_id: UserId) -> Optional[User]:
    cache: dict[UserId, User] = {}  # 非自明な型・アノテーションを付ける
    user = cache.get(user_id)       # 推論可能・アノテーション不要
    return user

# ❌ 悪い — 戻り値アノテーション欠落
def fetch_user(user_id: UserId):
    ...

# ❌ 悪い — 引数アノテーション欠落
def fetch_user(user_id):
    ...
```

### 3.2 裸の `Any` 禁止 — 絞り込む

`Any` は型チェックを無効化する。避けられない境界（未型データのパース）でのみ使い、即座に絞り込む。

```python
# ❌ 悪い
def process(data: Any) -> Any: ...

# ✅ 良い — エントリポイントで TypedDict / dataclass / Pydantic で絞り込む
class RawOrder(TypedDict):
    id: str
    amount: int

def process(data: RawOrder) -> OrderId: ...

# ✅ 許容 — Any が避けられない境界パース
def parse_json(raw: str) -> Any:
    return json.loads(raw)

def to_order(raw: Any) -> Order:  # 即座に絞り込む
    return Order.model_validate(raw)
```

### 3.3 Protocol vs ABC

ドメインコードの構造的インターフェースには `Protocol`。サブクラスでデフォルト実装を共有したい場合のみ `ABC`。

```python
# ✅ Protocol — 構造的型・継承不要
from typing import Protocol, runtime_checkable

@runtime_checkable
class Convertable(Protocol):
    def convert(self, source: str) -> str: ...

# ✅ ABC — デフォルト実装が必要なとき
from abc import ABC, abstractmethod

class BaseConverter(ABC):
    def convert(self, source: str) -> str:
        validated = self._validate(source)
        return self._convert(validated)

    def _validate(self, source: str) -> str:
        return source.strip()  # デフォルト実装

    @abstractmethod
    def _convert(self, source: str) -> str: ...
```

Protocol への `@runtime_checkable` は `isinstance()` 実行時チェックを有効化 — プラグイン的オブジェクトを受ける場面で便利。

### 3.4 モダンジェネリクス（Python 3.12+）と旧記法（3.11）

Python 3.12+ では新ジェネリクス構文：

```python
# Python 3.12+
def first[T](items: list[T]) -> T | None: ...

class Repository[EntityT]:
    def find(self, id: str) -> EntityT | None: ...
```

3.11 や広いライブラリ互換が必要な場合は `TypeVar`：

```python
# Python 3.11 / ライブラリコード
from typing import TypeVar

T = TypeVar("T")
EntityT = TypeVar("EntityT", bound="Entity")

def first(items: list[T]) -> T | None: ...

class Repository(Generic[EntityT]):
    def find(self, id: str) -> EntityT | None: ...
```

### 3.5 `Optional[T]` vs `T | None`

`T | None`（PEP 604）を `Optional[T]` より好む。両方有効・プロジェクト内で1つに揃える。

```python
# ✅ 推奨
def find(id: UserId) -> User | None: ...

# ✅ 許容
def find(id: UserId) -> Optional[User]: ...
```

### 3.6 閉じた集合には `Literal`

引数が固定の文字列・整数集合に制限されるなら `Literal`。

```python
# ✅ 良い — 型チェッカーが閉集合を強制
def export(fmt: Literal["csv", "json", "parquet"]) -> bytes: ...

# ❌ 悪い — 任意の文字列を受け、実行時チェックに遅延
def export(fmt: str) -> bytes:
    if fmt not in ("csv", "json", "parquet"):
        raise ValueError(...)
```

5 種類超や振る舞いを足すときは `Enum` を使う。

### 3.7 識別子には `NewType`

プリミティブ型の識別子は `NewType` でラップして型レベルで取り違えを防ぐ：

```python
from typing import NewType

UserId = NewType("UserId", str)
OrderId = NewType("OrderId", str)

def find_user(user_id: UserId) -> User: ...

# ✅ 呼び出し側は明示的に UserId を構築
find_user(UserId("abc"))

# ❌ 型チェッカーはこれを拒否（両方とも内部は str だが）
find_user(OrderId("abc"))
```

### 3.8 境界の構造化 dict には `TypedDict`

dict としてデータが境界を越える場面（関数内 JSON ペイロードなど）で shape をドキュメント化：

```python
from typing import TypedDict, NotRequired

class WebhookPayload(TypedDict):
    event: Literal["order.created", "order.shipped"]
    order_id: str
    timestamp: int
    note: NotRequired[str]   # オプションフィールド
```

バリデーションが効く外部 API 境界では Pydantic を選ぶ。`python-architecture.md` § Pydantic Boundaries 参照。

### 3.9 型専用 import

実行時の循環 import を避けるため `from typing import TYPE_CHECKING` を使う：

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.entities.user import User

def fetch(user_id: UserId) -> User: ...
```

`from __future__ import annotations` でアノテーションが遅延（文字列化）される — Python <3.13 で上記パターンに必須。

---

## 4. import とモジュールレイアウト

### 4.1 import 順序

```python
# 1. Future
from __future__ import annotations

# 2. stdlib
import argparse
from pathlib import Path
from typing import Optional, Protocol

# 3. サードパーティ
import httpx
from pydantic import BaseModel

# 4. ローカル（絶対 import を推奨）
from {package_name}.domain.entities.user import User
from {package_name}.domain.repositories.user_repository import UserRepository
```

内部モジュールには絶対 import。相対 import（`from .user import User`）は密結合な兄弟モジュール間のみ — レイヤー横断では禁止。

### 4.2 ワイルドカード import 禁止

```python
# ❌ 悪い — 名前空間を汚す・型チェックを壊す
from {package_name}.domain import *

# ✅ 良い
from {package_name}.domain.entities.user import User
from {package_name}.domain.entities.order import Order
```

### 4.3 未使用 import 禁止

コミット前に未使用 import を削除する。ruff / flake8 を `F401` で fail させる設定にする。

---

## 5. エラー処理

### 5.1 ドメインごとに独自例外クラス

ドメイン固有の例外クラスを定義する。ビジネスエラーに組み込み例外を投げない。

```python
# ✅ 良い — ドメイン例外
class OrderNotFoundError(Exception):
    def __init__(self, order_id: OrderId) -> None:
        super().__init__(f"Order not found: {order_id}")
        self.order_id = order_id

raise OrderNotFoundError(order_id)

# ❌ 悪い — ビジネスエラーに組み込み例外
raise ValueError(f"Order {order_id} not found")
```

### 5.2 例外の層化 — 境界で包む

インフラ境界で低レベル例外をキャッチし、ドメイン例外として再 raise する：

```python
# infrastructure/persistence/postgres_order_repository.py
class PostgresOrderRepository:
    def find_by_id(self, order_id: OrderId) -> Order:
        try:
            row = self._conn.execute("SELECT ... WHERE id = ?", (order_id,)).fetchone()
        except psycopg.OperationalError as e:
            raise RepositoryUnavailableError(str(e)) from e
        if row is None:
            raise OrderNotFoundError(order_id)
        return Order.from_row(row)
```

アプリケーション層は `psycopg.OperationalError` を見るべきではない — ドメインまたはリポジトリ例外のみ。

### 5.3 `raise ... from ...` を必ず

元例外を `from` で保持する：

```python
# ✅ 良い
try:
    ...
except KeyError as e:
    raise ConfigKeyMissingError(str(e)) from e

# ❌ 悪い — 元のトレースバックが消える
except KeyError as e:
    raise ConfigKeyMissingError(str(e))
```

### 5.4 `except:` 裸禁止 — 具体的に

```python
# ❌ 悪い — KeyboardInterrupt・SystemExit・全部キャッチ
try: ...
except: ...

# ❌ 悪い — 範囲が広すぎる
try: ...
except Exception: ...

# ✅ 良い — 具体的
try: ...
except (httpx.ConnectError, httpx.TimeoutException) as e:
    ...
```

唯一の正当な `except Exception:` は、長時間ループの最上位で予期せぬエラー後もループを継続させる場合。

---

## 6. 言語ルール

### 6.1 print・ロガー出力 — 英語のみ

すべての `print()` とロガー出力は英語。理由：bat ランチャーは `cmd.exe`（日本語 Windows では CP932）で動き、非ASCII出力がログファイルとコンソールを壊す。

```python
# ✅ 良い
print("Starting batch job")
logger.info("Order %s shipped to %s", order_id, address.zip)

# ❌ 悪い
print("バッチ処理を開始します")
logger.info("注文 %s を発送しました", order_id)
```

### 6.2 日本語可・不可

| 場所 | 日本語OK？ | 補足 |
|---|---|---|
| `print()` / ロガー出力 | ❌ NG | CP932 で壊れる |
| コードコメント | ✅ OK | 共有コードベースでは英語推奨 |
| `.env.sample` コメント | ✅ OK | 人間が読む（bat ではない） |
| GUI 表示文字列（tkinter等） | ✅ OK | Python の stdout で動く（bat ではない） |
| 例外メッセージ | ⚠️ 英語推奨 | ログに流れる・CP932 で壊れる可能性 |
| docstring | ✅ OK | ツールは UTF-8 で読む |
| pytest テスト名・メッセージ | ⚠️ 英語推奨 | テスト出力が CI ログに流れる可能性 |

### 6.3 文字列フォーマット

| 用途 | 選択 |
|---|---|
| コード内インライン補間 | f-string: `f"User {user.id} created"` |
| ロガー呼び出し | `%`-style: `logger.info("User %s created", user.id)` — ログレベルOFF時にフォーマットコストを遅延 |
| ユーザー向けテンプレート（複数行・パラメータ化） | `string.Template` か Jinja2 テンプレートをファイルからロード |

```python
# ✅ 良い — インラインは f-string
msg = f"Order {order.id} totalled {order.total}"

# ✅ 良い — ロガーは %（遅延フォーマット）
logger.info("Order %s totalled %s", order.id, order.total)

# ❌ 悪い — ロガーの f-string（ログレベルでフィルタされてもフォーマットが走る）
logger.info(f"Order {order.id} totalled {order.total}")
```

### 6.4 ユーザー向け文字列ハードコード禁止 — 設定可能化

ユーザー向け文字列（エンドユーザーに表示するエラーメッセージ・メールテンプレート等）は設定ファイルかテンプレートファイル — ソースに入れない。`python-architecture.md` § No Hardcoding 参照。

---

## 7. コードスタイル クイックリファレンス

| 観点 | ルール |
|---|---|
| 行長 | 100文字（プロジェクトで 88 や 120 に上書き可、pyproject.toml に明記） |
| インデント | スペース4 — タブ禁止 |
| クォート | ダブルクォート — シングルは dict キーなど一貫性が出るときのみ |
| 末尾カンマ | 複数行のコレクション・引数リストでは必須 |
| 空行 | トップレベル def 間2行・メソッド間1行 |
| Walrus 演算子（`:=`） | 可読性が明らかに上がるときのみ — 副作用と条件の混在は避ける |
| match 文 | tagged union・閉集合に使う — 長い `if/elif` より好む |

ruff で強制：

```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM", "TCH"]
```

---

## 8. Definition of Done — コアチェックリスト

Python ファイルを「完了」とする前に確認：

- [ ] すべての名前が § 1（命名規則）に従っている
- [ ] コードを言い換えるコメントがない；非自明な「なぜ」コメントが付いている（§ 2）
- [ ] すべての公開シンボルに型アノテーション（§ 3.1） — 裸 `Any` なし（§ 3.2）
- [ ] import が § 4 に従っている（順序・ワイルドカードなし・未使用なし）
- [ ] エラーはドメイン例外クラス＋`raise ... from ...`（§ 5）
- [ ] すべての `print()` / ロガー出力が英語（§ 6.1）
- [ ] インラインは f-string・ロガーは `%`（§ 6.3）
- [ ] ユーザー向け文字列のハードコードなし（§ 6.4）
- [ ] ruff（またはプロジェクトの linter）が通る
