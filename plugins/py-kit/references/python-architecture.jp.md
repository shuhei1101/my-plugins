<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# Python アーキテクチャ規約 — py-kit（日本語ミラー）

> このファイルは `python-architecture.md` の日本語ミラーです。Claude Code には読み込まれません。

本格 Python プロジェクト向けのアーキテクチャパターンと設計原則。

---

## SOLID 原則

### S — 単一責任原則

各クラスには変更理由が1つだけある。変更の軸で分割する（サイズではなく）。

```python
# 悪い例: UserService が認証・メール・DB を担当
# 良い例: AuthService・EmailService・UserRepository — それぞれ1つの理由でのみ変更される
```

### O — 開放・閉鎖原則

拡張に対して開いており、修正に対して閉じている。既存クラスを編集せず、コードを追加して振る舞いを拡張する。

```python
# 悪い例: 新しい型が増えるたびに肥大化する if/elif チェーン
# 良い例: Strategy パターン — 新しい振る舞い = Protocol を実装する新しいクラス
class ExportStrategy(Protocol):
    def export(self, data: list[dict]) -> bytes: ...
```

### L — リスコフ置換原則

サブクラスは呼び出し元を壊すことなく基底クラスを置換できなければならない。サブクラスで事後条件を弱めたり事前条件を強めたりしない。

### I — インターフェース分離原則

大きな汎用インターフェース1つより、小さな専用プロトコル多数。クライアントは使うものにだけ依存する。

```python
# 悪い例: class IStorage(Protocol): read() / write() / delete() / list() / stat()
# 良い例: class Readable(Protocol): read() / class Writable(Protocol): write()
#         合成: class ReadWritable(Readable, Writable, Protocol): ...
```

### D — 依存性逆転原則

上位モジュールは具体実装ではなく抽象に依存する。コンストラクタで依存性を注入する。

```python
# 悪い例: class ReportService: def __init__(self): self.db = PostgresDatabase()
# 良い例:
class ReportService:
    def __init__(self, repo: UserRepository) -> None:  # UserRepository は Protocol
        self._repo = repo
```

---

## DRY 原則

**安定した名前のある概念**が背後にある場合のみ重複を排除する。似た3行は、時期尚早な抽象化より良い。

- 値の重複 → 定数
- 同じ概念のロジック重複 → 関数
- 複数機能にわたるクラス構造の重複 → 基底クラスまたはジェネリック
- 設定の重複 → 設定ファイル / 環境変数

コードが似て見えるだけで全く異なるドメイン間で DRY を適用しない。

---

## レイヤードアーキテクチャ

コードをレイヤーに分けて構造化する。フォルダ名は自由 — プロジェクトに合ったものを使う。重要な制約は**依存の方向**：上位レイヤーは抽象に依存し、下位レイヤーが実装を提供する。

### レイヤーの役割

| レイヤー | 責務 |
|---|---|
| エントリーポイント / インターフェース | CLI 引数パース・HTTP ルーティング・GUI イベント・bat ランチャー。ビジネスロジックなし。 |
| ビジネスロジック | コアルールとユースケースの調整。Protocol インターフェース経由でのみ外部を呼び出す。 |
| 外部境界 | Protocol の具体実装：DB クライアント・外部 API アダプター・ファイル I/O・メッセージキュー。 |

### 外部境界の分離

外部サービス（HTTP API・DB・ファイルシステム・MQ）に触れるコードは必ず外部境界レイヤーに置き、ビジネスロジック層に定義した `Protocol` 経由でのみアクセスする。

### アーキテクチャ品質チェックリスト

- [ ] ビジネスロジック層は stdlib・内部モジュール・Protocol のみをインポート — 外部ライブラリは禁止
- [ ] 全外部サービス呼び出しは Protocol インターフェース経由
- [ ] ビジネスロジック層で外部ライブラリの具体クラスをインスタンス化しない
- [ ] 全箇所で依存性注入 — コンストラクタは具体クラスではなく Protocol を受け取る

---

## ハードコード禁止

設定値をソースコードに直接埋め込まない。

**ハードコード（悪い例）:**

```python
BASE_URL = "https://api.example.com"  # ビジネスロジック内
TIMEOUT = 30
OUTPUT_DIR = "/tmp/output"
```

**外部化（良い例）:**

```python
# constants.py — プロジェクト全体の計算済みパスのみ
PROJECT_ROOT = Path(__file__).parent.parent
LOG_DIR = PROJECT_ROOT / "log"

# config.py — 起動時に環境変数 / 設定ファイルから読み込む
BASE_URL: str = os.environ["API_BASE_URL"]
TIMEOUT: int = int(os.environ.get("API_TIMEOUT", "30"))
```

**ルール:**
- URL・ポート・ファイルパス・認証情報・閾値・フィーチャーフラグは全て `.env` / 設定ファイルに書く
- `.env.sample` で全必要変数をドキュメント化する
- `constants.py` は `__file__` から派生した計算済みパスのみ（マジックナンバー・文字列は禁止）

---

## 拡張性重視の設計

デフォルトで将来の変更に備えて設計する。実装をロックインしない。

### 依存性注入

常にコンストラクタで依存性を注入する。クラスボディ内で具体クラスをインスタンス化しない。

### Strategy パターン

交換可能なアルゴリズムを Protocol の後ろに隠す。

### Factory パターン

オブジェクト生成ロジックを集約する。構築が複雑または条件付きの場合に Factory 関数やクラスを使う。

### Decorator パターン

元のクラスを変更せず、横断的な振る舞い（ロギング・キャッシュ・リトライ）を追加する。

---

## Pydantic の適用境界

実行時バリデーションが必要なシステム境界では型ヒントだけでなく Pydantic モデルを使う。

**Pydantic を使う場面:**
- 外部 API のリクエストボディ・レスポンス
- LLM の入力・出力（Instructor 経由）
- 設定ファイル読み込み（YAML / JSON）
- ファイル間で受け渡すデータ（CSV / JSONL レコード）
- ユーザー入力のパース
- スレッド / プロセス間のイベントデータ

**`typing` だけで十分な場面:**
- 内部ロジックの関数引数 / 戻り値の型ヒント
- 単一関数内に留まる `dict` / `list` 式

---

## プロジェクトフォルダ構成

```
{package-name}/
├── {package_name}/
│   ├── interface/           # CLI・GUI・HTTP ハンドラー
│   ├── application/         # ユースケース
│   ├── domain/
│   │   ├── entities/
│   │   ├── value_objects/
│   │   ├── repositories/    # Protocol 定義
│   │   └── services/        # ドメインサービス
│   ├── infrastructure/      # 具体実装
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
│   └── {feature}/
│       └── test_{feature}.py
├── setup/
│   └── setup_venv.bat
├── {mode}.bat
├── activate.bat
├── .env.sample
├── .gitignore
├── README.md
└── pyproject.toml
```
