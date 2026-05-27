<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# py-kit references インデックス（日本語ミラー）

> このファイルは `index.md` の日本語ミラーです。
> 注入フックは英語版 `index.md` を読みます。日本語版は人間が一覧確認するためのもの。

各 reference ファイルの 1 行説明。本文は同じディレクトリ配下の各ファイルを参照。
編集対象ファイルに対する自動注入ルール（star chart）は `injection_rules.yaml` 側にあります。

---

## core — 言語ルール

| Path | 説明 |
|---|---|
| `core/naming.md` | 命名規約。関数 snake_case、型エイリアス UpperCamel、ファイル/モジュール snake_case。feature フォルダ内の標準ファイル名（types/service/query/route/client/db）対応表 |
| `core/comments.md` | コメントルール。exported 関数/型に 1 行 docstring 必須、Pydantic/dataclass の設計上重要フィールドの description 必須、PR 番号付き変更履歴、TODO は issue 番号必須 |
| `core/type-hints.md` | 型ヒント本体。PEP 695 ジェネリクス、Self、@typing.override、Annotated、TYPE_CHECKING、type 文、NewType、assert_never、Literal+match |
| `core/decorators.md` | 推奨デコレータ（@dataclass / @final / @cache / @cached_property / @override / @contextmanager）と、横断関心事を吸収するハンドラーデコレータ（@catch_and_log / @catch_and_map / @with_retry / @with_timeout）、@overload の限定使用 |
| `core/language-rules.md` | 言語ルール。コメントは日本語、print/logger/bat は英語、文字列フォーマット f-string、import 順、例外階層（AppError 基底クラス） |
| `core/style.md` | スタイル設定。ruff/mypy/pyright の推奨設定、行長 100、ダブルクォート、セクションマーカー |

## architecture — アーキテクチャ

| Path | 説明 |
|---|---|
| `architecture/layout.md` | トップレベルレイアウト。必須は shared/ と main.py のみ、任意で features/integrations/runtime/server。feature フォルダ内の標準構成（types.py / service.py / query.py / route.py / client.py） |
| `architecture/ts-style.md` | TypeScript 風 Python の中心ドキュメント。type エイリアスで関数の型を定義 + Callable で DI、Protocol で構造的型付け、@dataclass/Pydantic/TypedDict の使い分け表 |
| `architecture/composition-root.md` | main.py の責務。build_handlers(settings) で関数を functools.partial で配線、Handlers dataclass で型安全に保持。FastAPI/CLI 等ライブラリ標準クラスはそのまま使う |
| `architecture/dependencies.md` | 依存方向ルール。features/server → integrations → shared の一方向。同層内相互参照は禁止。逆依存（DIP）は関数の型エイリアスで実現 |
| `architecture/design-principles.md` | 設計原則の優先順位。DRY > SOLID > 拡張性意識。関数ファーストでクラスは DTO とライブラリ要求のみ |
| `architecture/refactoring-judgement.md` | リファクタ判断基準。何回書いたら共通化、いつ抽象化、いつ設定外出し、いつファイル分割するか |

## shared — 横断インフラ

| Path | 説明 |
|---|---|
| `shared/logger.md` | JSON Lines 形式の logger 標準実装。get_logger(__name__)、構造化ログ、ログレベル運用 |
| `shared/settings.md` | pydantic_settings.BaseSettings 標準パターン。.env / .env.sample 運用、SecretStr、ネストした設定 |
| `shared/secrets-and-env.md` | シークレット / 環境 / 構造 / アセット / ランタイム状態の保管先の分離方針。.env / settings.yaml / コード / index.yaml / data/ の使い分け |
| `shared/errors.md` | 例外階層。AppError 基底クラス、ドメイン別サブクラス、HTTP エラーとのマッピング |
| `shared/types.md` | 共通型エイリアス。NewType と type 文の使い分け、識別子型（UserId 等）の標準 |
| `shared/constants.md` | constants.py の役割境界。PROJECT_ROOT, LOG_DIR 等の計算済みパス置き場。実行時可変値は settings へ |

## scripts — スクリプト

| Path | 説明 |
|---|---|
| `scripts/python-script.md` | 単一ファイル Python スクリプトの構造。docstring、argparse、main() 返り値 int、セクションマーカー |
| `scripts/launchers-windows.md` | Windows 用 bat ランチャー。chcp 65001、setlocal、PowerShell 時刻、log/ ディレクトリ出力。**bat 内に日本語を書かない**（絶対） |
| `scripts/launchers-unix.md` | UNIX 用 shell スクリプト。set -euo pipefail、tee でログ、.venv activate |
| `scripts/tkinter.md` | tkinter GUI 規約。標準スタイル、設定ダイアログ、アクセントカラー（blue） |

## testing — テスト

| Path | 説明 |
|---|---|
| `testing/strategy.md` | テスト方針。単体テストは書かない、結合テスト + スモークテストのみ。スモークは外部接続用でユーザー手動実行限定（AI 自動実行禁止） |
| `testing/pytest.md` | pytest 規約。conftest.py、fixtures、parametrize、pytest-asyncio、tests/ レイアウト |
| `testing/mocks.md` | 結合テストの Mock パターン。LLM Mock、HTTP Mock、時刻 Mock、関数の型エイリアスを利用した注入差し替え |

## concurrency — 並行性

| Path | 説明 |
|---|---|
| `concurrency/async.md` | asyncio 規約。TaskGroup、asyncio.timeout、sync/async 境界、async generator/context manager |
| `concurrency/parallelism.md` | 並列処理。multiprocessing / threading / subinterpreter の使い分け、GIL、CPU bound vs IO bound |

## packaging — パッケージング

| Path | 説明 |
|---|---|
| `packaging/pyproject.md` | pyproject.toml 完全サンプル。[project] / [tool.ruff] / [tool.mypy] / [tool.pyright] / [tool.pytest] |
| `packaging/dependencies.md` | 依存管理。uv 標準、optional-dependencies.dev 必須、.venv 統一、lock ファイル運用 |
| `packaging/distribution.md` | 配布。wheel/sdist、PyPI publish、entry_points で CLI 公開 |
| `packaging/python-versions.md` | Python バージョン方針。極力高いバージョンを採用、3.12 以降の機能対応表 |

## performance — パフォーマンス

| Path | 説明 |
|---|---|
| `performance/cheatsheet.md` | パフォーマンスチート集。プロファイラ（cProfile / snakeviz / line_profiler / py-spy / scalene / memray）の使い分け、ホットパスのチェックリスト |

## llm — LLM

| Path | 説明 |
|---|---|
| `llm/providers.md` | LLM プロバイダ実装。Claude / OpenAI / Gemini を関数で抽象化、vendor 例外をドメイン例外にラップ、token usage ログ |
| `llm/instructor.md` | Instructor + Pydantic で構造化出力。task-specific クライアント関数の作り方 |
| `llm/prompts-authoring.md` | プロンプトファイルの書き方と組み立て。プロジェクトルート直下 prompts/、H3 セクション単位で部品化、static (.md) と dynamic (.j2)、index.yaml で SoT 管理、includes で組み立て |
| `llm/prompts-loader.md` | プロンプトのローダー実装。src/{pkg}/integrations/llm/prompts/ 配下に index_loader / builder / types を置く、Jinja2 + StrictUndefined、build_prompt / build_bundle |
| `llm/cost-cache.md` | コスト管理。プロンプトキャッシュの設計考え方（上から積む / 固定値は上 / 動的値は下）、Anthropic cache_control、OpenAI 自動キャッシュ、max_tokens、Batch API、ストリーミング |
| `llm/exceptions-retry.md` | LLM 例外階層。rate-limit / server / bad-request / auth / timeout / content-filter、リトライ戦略、Retry-After 尊重 |

## fastapi — FastAPI

| Path | 説明 |
|---|---|
| `fastapi/app.md` | FastAPI アプリ構成。build_app パターン、lifespan、middleware、CORS |
| `fastapi/routes.md` | ルーター実装。Annotated[Type, Depends/Path/Query]、route 関数は thin、service.py に処理本体 |
| `fastapi/schemas.md` | 入出力 Pydantic スキーマ。Field 制約、to_domain/from_domain メソッドで feature 内 DTO と分離 |
| `fastapi/auth-and-errors.md` | 認証 Depends + SecretStr の取り扱い + exception_handler によるエラーハンドリング |
| `fastapi/health.md` | ヘルスチェック。/healthz で 200 を返すだけのシンプル実装 |
