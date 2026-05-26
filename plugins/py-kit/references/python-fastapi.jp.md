<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# Python FastAPI 規約 — py-kit（日本語ミラー）

> このファイルは `python-fastapi.md` の日本語ミラーです。Claude Code には読み込まれません。

FastAPI プロジェクトの規約。`python-core.md` と `python-architecture.md` と合わせて読む。

---

## プロジェクト構成

```
{package_name}/
├── interface/
│   └── api/
│       ├── routers/         # リソースグループごとに1ファイル
│       │   ├── users.py
│       │   └── orders.py
│       ├── dependencies.py  # FastAPI Depends() ファクトリー
│       └── middleware.py    # CORS・認証・ロギングミドルウェア
├── application/             # ユースケース（FastAPI インポートなし）
├── domain/                  # エンティティ・Protocol・値オブジェクト
└── infrastructure/          # DB・外部 API アダプター
```

---

## エンドポイント設計

- リソースグループごとにルーターファイルを1つ作成（`users.py`・`orders.py`）
- ルート関数は薄く — ユースケースを呼び出し、レスポンスモデルを返すだけ
- ルート関数にビジネスロジックを入れない
- リクエストボディとレスポンスには Pydantic モデルを使う

```python
@router.post("/users", response_model=UserResponse, status_code=201)
async def create_user(body: CreateUserRequest, use_case: CreateUserUseCase = Depends(get_create_user)) -> UserResponse:
    return await use_case.execute(body)
```

---

## 依存性注入

FastAPI `Depends()` を使ってユースケースとリポジトリを注入する：

```python
def get_user_repository() -> UserRepository:
    return PostgresUserRepository(get_db_connection())

def get_create_user(repo: UserRepository = Depends(get_user_repository)) -> CreateUserUseCase:
    return CreateUserUseCase(repo)
```

ルート関数内でユースケースやリポジトリを直接インスタンス化しない。

---

## 共通ミドルウェア

- **CORS**：常に明示的に設定する — 本番環境でワイルドカード `*` は禁止
- **認証**：ミドルウェアではなく `Depends()` 関数として JWT 検証を実装する
- **ロギング**：リクエストメソッド・パス・ステータスコード・処理時間を INFO レベルでログに記録する
- **エラーハンドリング**：`@app.exception_handler` でドメイン例外 → HTTP ステータスへのマッピングを実装する

---

## 起動・シャットダウン

`lifespan` コンテキストマネージャーを使う（非推奨の `on_event` よりも推奨）：

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 起動時
    await db.connect()
    yield
    # シャットダウン時
    await db.disconnect()

app = FastAPI(lifespan=lifespan)
```

---

## 実行とデプロイ

ローカル開発（Windows）：`python-scripts.md` の FastAPI run.bat テンプレートを参照

本番環境：`uvicorn {package_name}.__main__:app --host 0.0.0.0 --port {PORT}` で実行
