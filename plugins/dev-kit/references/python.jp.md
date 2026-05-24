<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# Python — dev-kit 共通リファレンス（日本語ミラー）

> このファイルは `python.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `python.md` にも反映してください。

全 dev-kit Python スキルがこのドキュメントを参照する。スキルファイル内に内容を重複して書かない。

---

## 命名規則

| 対象 | 規約 | 例 |
|---|---|---|
| モジュール / ファイル | `snake_case` | `user_repository.py` |
| クラス | `PascalCase` | `UserRepository` |
| 関数 / メソッド | `snake_case` | `find_by_id()` |
| 変数 | `snake_case` | `user_id` |
| 定数 | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| プライベート | 先頭に `_` | `_internal_cache` |
| Protocol / インターフェース | `{Name}able`（推奨）・`I{Name}`・`Base{Name}` — プロジェクト内で1パターンに統一 | `Convertable`・`IConverter`・`BaseConverter` |
| 実装クラス | `{実装名}_{name}.py` | `ffmpeg_converter.py` |

---

## コメントルール

**なぜ**を書く。**何をするか**は書かない（コードを読めばわかる）。

- 良い例：`# CP932 で bat ファイルをパースする — 日本語 UTF-8 バイトがリードバイトとして誤認され後続文字が消える`
- 悪い例：`# setup_logger を呼ぶ`

1行の短いコメントのみ。複数段落・シグネチャを言い換えるだけの docstring は禁止。

例外：スクリプトのモジュールレベル docstring（簡易スクリプトセクション参照）。

---

## 型ヒント

関数の引数・戻り値・クラスフィールドの全箇所に付ける。裸の `Any` は禁止。

```python
from typing import Literal, Optional, Protocol, TypeVar
from collections.abc import Sequence

def process(items: Sequence[str], mode: Literal["fast", "slow"]) -> list[str]: ...
```

構造的インターフェースには `Protocol` を使う（新規コードでは `ABC` より推奨）：

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Convertable(Protocol):
    def convert(self, source: str) -> str: ...
```

共有デフォルト実装が必要な場合のみ `ABC` を使う。

---

## SOLID 原則

### S — 単一責任原則（Single Responsibility）

クラスの変更理由は1つだけ。変更の軸ごとに分割する（サイズではなく）。

```python
# 悪い例：UserService が認証・メール・DB 操作を担当
# 良い例：AuthService / EmailService / UserRepository — それぞれ1つの変更理由を持つ
```

### O — 開放閉鎖原則（Open / Closed）

拡張に対して開いている、修正に対して閉じている。既存コードを書き換えず、コードを追加して機能を増やす。

```python
# 悪い例：新しい種別が増えるたびに成長する if/elif チェーン
# 良い例：Strategy パターン — 新しい動作 = Protocol を実装する新しいクラス
class ExportStrategy(Protocol):
    def export(self, data: list[dict]) -> bytes: ...

class CsvExporter:
    def export(self, data: list[dict]) -> bytes: ...

class JsonExporter:
    def export(self, data: list[dict]) -> bytes: ...
```

### L — リスコフの置換原則（Liskov Substitution）

サブクラスは基底クラスの代わりに使えなければならない。事後条件を弱めたり前提条件を強めたりしない。

```python
# 悪い例：SquareRepository.find_all() が NotImplementedError を raise する
# 良い例：すべてのサブクラスが Protocol の契約を完全に実装する
```

### I — インターフェース分離原則（Interface Segregation）

1つの大きな汎用インターフェースより、小さく目的を絞ったインターフェースを複数作る。クライアントは使うものだけに依存する。

```python
# 悪い例：class IStorage(Protocol): def read() / write() / delete() / list() / stat()
# 良い例：class Readable(Protocol): def read() / class Writable(Protocol): def write()
#          組み合わせ：class ReadWritable(Readable, Writable, Protocol): ...
```

### D — 依存性逆転原則（Dependency Inversion）

高レベルモジュールは具象実装ではなく抽象に依存する。依存はコンストラクタ経由でインジェクトする。

```python
# 悪い例
class ReportService:
    def __init__(self) -> None:
        self.db = PostgresDatabase()  # 具象をハードコード

# 良い例
class ReportService:
    def __init__(self, repo: UserRepository) -> None:  # UserRepository は Protocol
        self._repo = repo
```

---

## DRY 原則

重複を排除するのは、その背後に**安定した名前のついた概念**がある場合のみ。似たような3行コードは、早まった抽象化より良い。

- 重複する値 → 定数
- 同じ概念の重複ロジック → 関数
- 機能をまたぐクラス構造の重複 → 基底クラスまたはジェネリクス
- 重複する設定 → 設定ファイル / 環境変数

全くドメインが違うコードが「見た目が似ているだけ」で DRY にするのは禁止。

---

## レイヤー構造

コードをレイヤーに分割する。フォルダ名は指定しない — プロジェクトに合った形で自由に構成する。制約は**依存の方向**だけ：高レベルレイヤーは抽象に依存し、低レベルレイヤーが実装を提供する。

### 各レイヤーの役割

| レイヤー | 責務 |
|---|---|
| エントリーポイント / インターフェース | CLI 引数パース・HTTP ルーティング・GUI イベント・bat ランチャー。ビジネスロジックは書かない。 |
| ビジネスロジック | コアルールとユースケースのオーケストレーション。外部サービスへは Protocol インターフェース経由でのみ呼び出す。 |
| 外部境界 | そのインターフェースの具象実装：DB クライアント・外部 API アダプター・ファイル I/O・メッセージキュー。 |

### 外部境界の分離

外部サービス（HTTP API・データベース・ファイルシステム・メッセージキュー）に触れるコードは必ず外部境界レイヤーに置き、ビジネスロジックレイヤーで定義した `Protocol` 経由でのみアクセスする。

```python
# ビジネスロジック層に定義 — 外部ライブラリのインポートなし
class OrderRepository(Protocol):
    def find_by_id(self, order_id: str) -> Optional[Order]: ...
    def save(self, order: Order) -> None: ...

# 外部境界層で実装
class PostgresOrderRepository:
    def __init__(self, conn: Connection) -> None:
        self._conn = conn
    def find_by_id(self, order_id: str) -> Optional[Order]: ...
    def save(self, order: Order) -> None: ...
```

これにより：
- ビジネスロジック層はどの外部サービスを使っているかを知らない
- ビジネスロジックを変更せずに外部サービスを差し替えられる
- テストではフェイク実装をインジェクトして実インフラにアクセスしない

### アーキテクチャ品質チェックリスト

- [ ] ビジネスロジック層は stdlib・内部モジュール・Protocol のみインポートしている
- [ ] 全外部サービス呼び出しは Protocol インターフェース経由
- [ ] 外部ライブラリの具象クラスをビジネスロジック層内でインスタンス化していない
- [ ] 依存性注入を全箇所で使用している — コンストラクタは Protocol を受け取り、具象クラスは受け取らない

---

## ハードコード禁止

設定値をソースコードに直接埋め込まない。

**ハードコード（悪い例）：**

```python
BASE_URL = "https://api.example.com"  # ビジネスロジック内
TIMEOUT = 30
MAX_RETRY = 3
OUTPUT_DIR = "/tmp/output"
```

**外部化（良い例）：**

```python
# constants.py — __file__ から導出するプロジェクト全体のパスのみ
PROJECT_ROOT = Path(__file__).parent.parent
LOG_DIR = PROJECT_ROOT / "log"

# config.py — 起動時に環境変数 / 設定ファイルから読み込む
BASE_URL: str = os.environ["API_BASE_URL"]
TIMEOUT: int = int(os.environ.get("API_TIMEOUT", "30"))
```

**ルール：**
- URL・ポート・ファイルパス・認証情報・しきい値・フィーチャーフラグはすべて `.env` / 設定ファイルに書く
- 必要な全環境変数を `.env.sample` に記載する
- `constants.py` は `__file__` から導出するパスのみ — マジックナンバーや文字列は書かない
- コミット前にビジネスロジック内のベタ書き文字列リテラルとマジックナンバーを検索して確認する

---

## 拡張性重視の設計

将来の変更を前提として設計する。実装をロックインしない。

### 依存性注入（DI）

依存は必ずコンストラクタ経由でインジェクトする。クラス本体内で具象クラスをインスタンス化しない。

```python
# 悪い例
class OrderService:
    def __init__(self) -> None:
        self._repo = SqlOrderRepository()  # 具象をハードコード

# 良い例
class OrderService:
    def __init__(self, repo: OrderRepository) -> None:  # Protocol
        self._repo = repo
```

### Strategy パターン

交換可能なアルゴリズムを Protocol の後ろにカプセル化する。

```python
class SortStrategy(Protocol):
    def sort(self, items: list[int]) -> list[int]: ...

class QuickSort:
    def sort(self, items: list[int]) -> list[int]: ...

class MergeSort:
    def sort(self, items: list[int]) -> list[int]: ...
```

### Factory パターン

オブジェクト生成ロジックを一箇所に集約する。構築が複雑または条件分岐を伴う場合に factory 関数またはクラスを使う。

```python
def create_exporter(fmt: Literal["csv", "json"]) -> ExportStrategy:
    match fmt:
        case "csv": return CsvExporter()
        case "json": return JsonExporter()
```

### Decorator パターン

元のクラスを変更せずに横断的な関心事（ロギング・キャッシュ・リトライ）を追加する。

```python
class LoggingRepository:
    def __init__(self, inner: UserRepository, logger: Logger) -> None:
        self._inner = inner
        self._logger = logger

    def find_by_id(self, user_id: UserId) -> Optional[User]:
        self._logger.debug("find_by_id %s", user_id)
        return self._inner.find_by_id(user_id)
```

---

## Pydantic の境界

実行時バリデーションが重要なシステム境界では、型ヒントだけでなく Pydantic モデルを使う。

**Pydantic を使う箇所：**
- 外部 API へのリクエスト・レスポンス
- LLM への入力と出力（Instructor 経由）
- 設定ファイルの読み込み（YAML / JSON）
- ファイル間で受け渡すデータ（CSV / JSONL のレコード）
- ユーザー入力のパース
- スレッド / プロセス間で受け渡すイベントデータ

**型ヒントのみで十分な箇所：**
- 単一関数内で完結する内部ロジックの引数・戻り値
- 関数内に閉じた `dict` / `list` の型表現

---

## ロガー仕様

すべてのプロジェクトに `{package_name}/logger.py` と `setup_logger()` 関数を含める：

- `constants.py` に `LOG_DIR = PROJECT_ROOT / "log"` を定義する
- `setup_logger()` 内で `LOG_DIR.mkdir(parents=True, exist_ok=True)` を呼ぶ
- ログファイル名：`LOG_DIR / f"{datetime.now():%Y%m%d_%H%M%S}_{package_name}.log"` — 毎回新規ファイル
- `StreamHandler(sys.stdout)` と `FileHandler(..., encoding="utf-8")` の両方をアタッチする
- フォーマット：`[%(asctime)s] %(levelname)s %(name)s %(filename)s:%(lineno)d - %(message)s`
- ハンドラーの重複追加を防ぐ：`if logger.handlers: return logger`
- サブモジュール：`get_logger(__name__)` でロガーを取得する

`setup_logger()` は `main.py` / `__main__.py` の起動直後に呼ぶ。

---

## テスト方針

| テスト種別 | 方針 |
|---|---|
| 単体テスト（個々のメソッド・関数） | 書かない — AI 支援開発ではメンテコストが価値を上回る |
| モジュール間結合テスト | モジュール間の連携が非自明な場合に作成 |
| ユースケーステスト | ユースケース単位で作成。外部 I/O 境界のみモック |
| E2E テスト | CLI エントリーポイントと HTTP API エンドポイントがある場合に作成 |

pytest を使用。`tests/` はソースフォルダ構成をミラーリングする。再利用可能なモックは `tests/mocks/` にまとめる。

ソースファイルとテストファイルは連携している — ソースが変更されたときは必ず対応するテストを確認・更新する。

---

## プロジェクトフォルダ構成

```
{パッケージ名}/
├── {package_name}/
│   ├── interface/           # CLI / GUI / HTTP ハンドラー
│   ├── application/         # ユースケース
│   ├── domain/
│   │   ├── entities/
│   │   ├── value_objects/
│   │   ├── repositories/    # Protocol 定義
│   │   └── services/        # ドメインサービス
│   ├── infrastructure/      # 具象実装
│   ├── __init__.py
│   ├── __main__.py
│   ├── config.py
│   ├── main.py
│   ├── logger.py
│   ├── exceptions.py
│   └── constants.py
├── tests/
│   ├── mocks/
│   │   ├── mock_env.py
│   │   └── mock_externals.py
│   ├── conftest.py
│   └── {機能名}/
│       └── test_{機能名}.py
├── setup/
│   └── setup_venv.bat
├── {モード}.bat
├── activate.bat
├── .env.sample
├── .gitignore
├── README.md
└── pyproject.toml
```

---

## 簡易スクリプト構造

`pyproject.toml` などのフルプロジェクト構成が不要な単一ファイルスクリプト向け：

**ファイルヘッダー（必須）：**

```python
"""
{スクリプト名} — {何をするかの1行説明}

Usage:
  python {スクリプト名}.py [options] {positional_args}
"""
```

**コード構成テンプレート：**

```python
"""...(ヘッダー)..."""

# ── 標準ライブラリ ──────────────────────────────────────────
import argparse
from pathlib import Path
from typing import Optional

# ── サードパーティ ──────────────────────────────────────────
import some_lib  # pip install some_lib

# ── 定数 ────────────────────────────────────────────────────
SOME_CONSTANT: str = "value"

# ── プライベート関数 ─────────────────────────────────────────
def _helper(value: str) -> str:
    return value.strip()

# ── メイン処理 ──────────────────────────────────────────────
def main(args: argparse.Namespace) -> None:
    ...

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    return parser.parse_args()

if __name__ == "__main__":
    main(parse_args())
```

フルパッケージとの違い：`logger.py`・`config.py`・テスト・bat ファイル・setup スクリプト・`pyproject.toml` は生成しない。必要なパッケージは `# pip install {package}` でインラインコメント。

---

## bat ランチャーテンプレート

> **Windows 限定。** bat ファイルとこのセクションのルールは Linux / macOS 環境には適用しない。
> Linux / macOS では シェルスクリプトや `Makefile` を使う。

```bat
@echo off
chcp 65001 > nul
setlocal

set "LOG_DIR=%~dp0log"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMddHHmmss"') do set "TS=%%I"
set "BAT_LOG=%LOG_DIR%\%TS%_run_bat.log"

echo [%date% %time%] Starting >> "%BAT_LOG%"
echo [%date% %time%] CWD: %cd% >> "%BAT_LOG%"

if exist "%~dp0venv\Scripts\activate.bat" (
    call "%~dp0venv\Scripts\activate.bat" >> "%BAT_LOG%" 2>&1
)

python -m {package_name} %* >> "%BAT_LOG%" 2>&1
set "EXITCODE=%ERRORLEVEL%"

if %EXITCODE% neq 0 (
    echo [ERROR] Exit code %EXITCODE%. See: %BAT_LOG%
    pause
)

endlocal & exit /b %EXITCODE%
```

**ルール：**
- タイムスタンプ付きログファイル名は必須 — 固定名は禁止
- bat ファイルの内容はすべて ASCII のみ — 日本語は cmd.exe の CP932 パースでエラーになる
- タイムスタンプには PowerShell `Get-Date` を使う — `wmic` は Windows 11 24H2 以降で削除済み

コンソールとログへの同時出力（長時間コマンド）：

```bat
long_command.exe 2>&1 | powershell -NoProfile -Command "[Console]::InputEncoding=[System.Text.Encoding]::UTF8; $input | ForEach-Object { Write-Host $_; Add-Content -LiteralPath '%BAT_LOG%' -Value $_ -Encoding utf8 }"
```

---

## FastAPI run.bat テンプレート

> **Windows 限定。** 上記「bat ランチャーテンプレート」の注記を参照。

```bat
@echo off
chcp 65001 > nul
setlocal

set "LOG_DIR=%~dp0log"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMddHHmmss"') do set "TS=%%I"
set "BAT_LOG=%LOG_DIR%\%TS%_run.log"

if not "%1"=="" set "PORT=%1"

echo [%date% %time%] Starting. PORT=%PORT% >> "%BAT_LOG%"

if exist "%~dp0.venv\Scripts\activate.bat" (
    call "%~dp0.venv\Scripts\activate.bat" >> "%BAT_LOG%" 2>&1
)

python -m {package_name} >> "%BAT_LOG%" 2>&1
set "EXITCODE=%ERRORLEVEL%"

if %EXITCODE% neq 0 (
    echo [ERROR] Exit code %EXITCODE%. See: %BAT_LOG%
    pause
)

endlocal & exit /b %EXITCODE%
```

ポートの運用：メインリポジトリ用の固定ポートを予約し、worktree テスト起動では固定ポート + 1 以上を使う。

---

## GUI（tkinter）

- 実行ボタン：青色
- 設定ボタンを配置 → クリックでモーダル設定画面を開く
- 設定画面：全設定項目を GUI から変更可能。変更内容は `.env` ファイルに保存
- 再起動が必要な設定：赤字で「再起動後に適用されます」と表示
- レイアウト：プロジェクトごとに3案提示 → ユーザーが選択

---

## 言語ルール

- **英語のみ**：すべての `print()` 文とロガー出力（bat ファイルが CP932 でパースされ日本語が文字化けする）
- **日本語 OK**：コードコメント・`.env.sample` のコメント・GUI の表示文字列
