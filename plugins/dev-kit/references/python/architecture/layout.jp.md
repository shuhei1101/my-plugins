<!-- This file is a Japanese mirror of layout.md. When updating the English original, update this file too. -->
# トップレベルレイアウト + feature 内構造

> このファイルは `layout.md` の日本語ミラーです。

dev-kit Python の標準は **機能フォルダ型レイアウト**。純 DDD（domain / application / infrastructure / interface）は廃止。

---

## トップレベル構成

```
src/{pkg}/
├── __init__.py
├── __main__.py
├── main.py                       # composition root（必須）
├── shared/                       # 横断インフラ（必須）
├── features/                     # ビジネス機能（任意）
├── integrations/                 # 外部サービス連携（任意）
├── runtime/                      # 実行時インフラ（任意）
└── server/                       # HTTP/WS サーバ（任意）
```

### 必須

| パス | 役割 |
|---|---|
| `__init__.py` | パッケージマーカー |
| `main.py` | composition root（関数を `functools.partial` で配線） |
| `shared/` | logger / settings / errors / types / constants / utils |

### 任意（プロジェクトで使う場合のみ作る）

| パス | 役割 | 例 |
|---|---|---|
| `__main__.py` | `python -m {pkg}` で起動するエントリポイント | CLI ツール |
| `features/` | ビジネス機能 | `features/chat/`, `features/auto_tweet/` |
| `integrations/` | 外部サービス連携 | `integrations/llm/`, `integrations/tts/` |
| `runtime/` | 実行時インフラ（queue / workflow / state） | 必要に応じて |
| `server/` | HTTP/WS サーバ | FastAPI 使う場合 |

---

## feature フォルダ内の構造

```
{pkg}/features/{feature}/
├── __init__.py             # 公開 API（必須）
├── types.py                # 型定義（DTO + 型エイリアス + Protocol）
├── query.py                # 読み取り関数（find / list / get / search）
├── service.py              # ビジネスロジック関数（create / update / delete / 複合操作）
├── route.py                # HTTP ハンドラ（feature が Web に公開される場合のみ）
├── client.py               # 外部 API 呼び出し関数（主に integrations 配下で使う）
├── db.py                   # 永続化（DB 使う場合のみ。新方針では基本不要）
├── prompts/                # プロンプトファイル（LLM feature のみ）
└── _helpers.py             # feature 内部のみのヘルパー
```

### 小さい feature の最小構成

```
{pkg}/features/chat/
├── __init__.py
├── types.py
└── service.py
```

「全部置く」ではなく「**この名前を使うときはこの役割**」という標準。
小さい feature では `types.py` + `service.py` だけでも OK。

### サブフィーチャ

機能が大きくなったら同じ構造でサブフォルダを切る:

```
{pkg}/features/chat/
├── __init__.py
├── types.py
├── service.py
└── personal/               # サブフィーチャ
    ├── __init__.py
    ├── types.py
    └── service.py
```

---

## shared/ の中身

```
{pkg}/shared/
├── __init__.py
├── logger.py               # JSONL logger
├── settings.py             # Pydantic Settings
├── errors.py               # 例外階層
├── types.py                # 共通型エイリアス
├── constants.py            # 計算済みパス（PROJECT_ROOT, LOG_DIR）
└── utils.py                # 業務横断ヘルパー
```

`core/` フォルダは作らない（shared/ に統合）。
ライブラリ的な機能（logger / settings / errors）と業務横断ヘルパー（utils）を 1 フォルダにまとめる。

詳細は各 `shared/{xxx}.md`。

---

## integrations/ の中身

```
{pkg}/integrations/
├── __init__.py
└── llm/                    # サービス種別ごとにサブフォルダ
    ├── __init__.py
    ├── types.py            # 関数の型エイリアス（AsyncChatFn 等）と DTO
    ├── openai_client.py    # 各ベンダー実装
    ├── claude_client.py
    └── mock_client.py      # テスト用 Mock
```

`integrations/` は **外部サービスとの境界**。
- 関数の型エイリアス（`AsyncChatFn` 等）を `types.py` に定義
- 各プロバイダ実装を別ファイルで提供
- テスト用 Mock も同じフォルダに置く

> プロンプトファイルは **プロジェクトルート直下の `prompts/`** に置く（`llm/prompts-authoring.md` 参照）。
> `integrations/llm/` 配下にはローダーや provider 実装だけを置く。

---

## server/ の中身（FastAPI 使う場合）

```
{pkg}/server/
├── __init__.py
├── app.py                  # build_fastapi(settings) -> FastAPI
├── lifespan.py             # startup / shutdown
├── middleware.py           # CORS / 認証 / ログ
├── routes/                 # ルーター
│   ├── __init__.py
│   ├── chat.py             # /chat 系
│   └── health.py           # /healthz
└── ws/                     # WebSocket
    └── chat.py
```

`features/{feature}/route.py` に置く方式と `server/routes/{feature}.py` に置く方式の使い分け:

| 方式 | 推奨ケース |
|---|---|
| `features/{feature}/route.py` | feature 単位で完結。route + service が密結合 |
| `server/routes/{feature}.py` | route と service を完全分離したい。複数 feature を 1 route でまとめる |

新規プロジェクトでは **`features/{feature}/route.py`** を基本にする（feature 内で完結する）。
サーバ起動時に `server/app.py` から `include_router` で集約する。

---

## runtime/ の中身（任意・大規模プロジェクトで使う）

```
{pkg}/runtime/
├── __init__.py
├── queue.py                # メッセージキュー
├── workflow.py             # ステートマシン / ワークフロー
└── state.py                # ランタイム状態（接続プール、セッション等）
```

---

## tests/ の構造

```
tests/
├── __init__.py
├── conftest.py             # 共通 fixtures
├── features/               # features/ をミラー
│   ├── chat/
│   │   └── test_chat.py    # 結合テスト
│   └── ...
├── server/                 # server/ をミラー
│   └── test_routes_chat.py
└── smoke/                  # スモークテスト（ユーザー手動実行のみ）
    └── test_llm.py
```

詳細は `testing/strategy.md`。

---

## 単一ファイルスクリプトの場合

`pyproject.toml` を作らない簡易スクリプト:

```
project/
├── script.py
├── log/                    # 実行ログ出力先
└── run.bat                 # ランチャー
```

詳細は `scripts/python-script.md`。

---

## 関連ファイル

- `architecture/ts-style.md` — feature 内で使う型エイリアス + 関数のスタイル
- `architecture/composition-root.md` — main.py の責務
- `architecture/dependencies.md` — 依存方向
- `core/naming.md` — feature 内ファイル名の標準
