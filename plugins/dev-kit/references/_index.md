# dev-kit リファレンス インデックス

`references/` 配下のリファレンスドキュメント一覧。技術スタック別に分類。

---

## Markdown

| # | ファイル | 内容 |
|---|---|---|
| 1 | [markdown/マークダウンテーブル.md](markdown/マークダウンテーブル.md) | Markdown テーブル書式規約。`#` 列必須・〃（繰り返し記号）の使い方 |
| 2 | [markdown/マークダウン編集.md](markdown/マークダウン編集.md) | Markdown フロントマター配置ルール。`---` の前に何も書かない |

---

## HTML / CSS / JS

Vanilla HTML + CSS + JS プロジェクトの設計方針。

| # | ファイル | 内容 |
|---|---|---|
| 1 | [html/基本方針.md](html/基本方針.md) | HTML/CSS/JS 開発原則。DRY/集中化・FLOCSS レイヤー・デザイントークン・JS 規約 |
| 2 | [html/UIデザイン.md](html/UIデザイン.md) | UX パターンと共通部品優先ルール。画面を書く前に shared リソースを読む |
| 3 | [html/デバッグFAB同期.md](html/デバッグFAB同期.md) | debug-fab テンプレート同期ルール。uidev.js / uidev.css 変更時の SKILL.md 更新 |
| 4 | [html/CSS-JSリンク.md](html/CSS-JSリンク.md) | CSS クラス ↔ JS DOM アクセス連動ルール。FLOCSS クラス定義と DOM アクセスの同期 |
| 5 | [html/コンポーネントファースト.md](html/コンポーネントファースト.md) | 共通部品優先ルール。新規 UI 追加前に shared 定数・ルート・コンポーネント CSS/JS を読む |

---

## Python

### コア言語規約

| # | ファイル | 内容 |
|---|---|---|
| 1 | [python/core/命名規則.md](python/core/命名規則.md) | 命名規約。snake_case 関数・UpperCamel 型エイリアス・標準ファイル名 |
| 2 | [python/core/コメント.md](python/core/コメント.md) | コメント規約。exported に 1 行 docstring・PR 番号付き変更履歴・TODO にはイシュー番号 |
| 3 | [python/core/型ヒント.md](python/core/型ヒント.md) | 型ヒント規約。PEP 695 generics・Self・@override・Annotated・type 文 |
| 4 | [python/core/デコレーター.md](python/core/デコレーター.md) | 推奨デコレータ。@dataclass / @final / @cache / @override / @contextmanager ほか |
| 5 | [python/core/言語ルール.md](python/core/言語ルール.md) | 言語規則。コメントは日本語・f-string・import 順・例外クラス階層 |
| 6 | [python/core/スタイル.md](python/core/スタイル.md) | スタイル設定。ruff/mypy/pyright 推奨設定・行長 100・ダブルクォート |

### アーキテクチャ

| # | ファイル | 内容 |
|---|---|---|
| 1 | [python/architecture/レイアウト.md](python/architecture/レイアウト.md) | トップレベルレイアウト。shared/ と main.py が必須・feature/integrations/server はオプション |
| 2 | [python/architecture/TypeScriptスタイル適用.md](python/architecture/TypeScriptスタイル適用.md) | TypeScript スタイル Python。関数型エイリアス DI・Protocol 構造的型付け |
| 3 | [python/architecture/コンポジションルート.md](python/architecture/コンポジションルート.md) | main.py の責務。build_handlers() で DI・Handlers dataclass |
| 4 | [python/architecture/依存パッケージ管理.md](python/architecture/依存パッケージ管理.md) | 依存方向ルール。features/server → integrations → shared の一方向 |
| 5 | [python/architecture/design-基本方針.md](python/architecture/design-基本方針.md) | 設計原則の優先順位。DRY > SOLID > 拡張性意識。関数ファースト |
| 6 | [python/architecture/リファクタリング判断.md](python/architecture/リファクタリング判断.md) | リファクタリング判断基準。抽出・抽象化・外部化・ファイル分割の閾値 |

### 共有モジュール

| # | ファイル | 内容 |
|---|---|---|
| 1 | [python/shared/ロガー.md](python/shared/ロガー.md) | 標準 JSON Lines ロガー。get_logger(__name__)・構造化ログ・ログレベルポリシー |
| 2 | [python/shared/設定.md](python/shared/設定.md) | pydantic_settings.BaseSettings 標準パターン。.env /.env.sample・SecretStr |
| 3 | [python/shared/シークレットと環境変数.md](python/shared/シークレットと環境変数.md) | シークレット / 環境変数 / 構造 / アセット / ランタイム状態の分離 |
| 4 | [python/shared/エラー定義.md](python/shared/エラー定義.md) | 例外クラス階層。AppError 基底クラス・ドメイン例外・HTTP マッピング |
| 5 | [python/shared/型定義.md](python/shared/型定義.md) | 共通型エイリアス。NewType と type 文の使い分け・識別子型（UserId 等） |
| 6 | [python/shared/定数.md](python/shared/定数.md) | constants.py の役割境界。PROJECT_ROOT / LOG_DIR 等の事前計算パス |

### スクリプト

| # | ファイル | 内容 |
|---|---|---|
| 1 | [python/scripts/Pythonスクリプト.md](python/scripts/Pythonスクリプト.md) | 単一ファイル Python スクリプト構造。docstring・argparse・main() -> int |
| 2 | [python/scripts/ランチャー-Unix.md](python/scripts/ランチャー-Unix.md) | UNIX シェルスクリプト。set -euo pipefail・tee でログ・.venv アクティベーション |
| 3 | [python/scripts/Tkinter.md](python/scripts/Tkinter.md) | tkinter GUI 規約。標準スタイル・設定ダイアログ・青アクセントカラー |

### 並行処理

| # | ファイル | 内容 |
|---|---|---|
| 1 | [python/concurrency/非同期処理.md](python/concurrency/非同期処理.md) | asyncio 規約。TaskGroup・asyncio.timeout・同期/非同期境界 |
| 2 | [python/concurrency/並列処理.md](python/concurrency/並列処理.md) | 並列処理。multiprocessing / threading / subinterpreters の選び方 |

### パッケージング

| # | ファイル | 内容 |
|---|---|---|
| 1 | [python/packaging/pyproject設定.md](python/packaging/pyproject設定.md) | pyproject.toml サンプル全量。[project] / [tool.ruff] / [tool.mypy] など |
| 2 | [python/packaging/依存パッケージ管理.md](python/packaging/依存パッケージ管理.md) | 依存管理。uv 標準・optional-dependencies.dev 必須・.venv 統一 |
| 3 | [python/packaging/配布設定.md](python/packaging/配布設定.md) | 配布。wheel/sdist・PyPI publish・entry_points で CLI 公開 |
| 4 | [python/packaging/Pythonバージョン.md](python/packaging/Pythonバージョン.md) | Python バージョンポリシー。最新を使う・3.12 以降の機能表 |

### パフォーマンス

| # | ファイル | 内容 |
|---|---|---|
| 1 | [python/performance/パフォーマンスチートシート.md](python/performance/パフォーマンスチートシート.md) | パフォーマンスチートシート。プロファイラ選択・ホットパスチェックリスト |

### LLM 統合

| # | ファイル | 内容 |
|---|---|---|
| 1 | [python/llm/プロバイダー.md](python/llm/プロバイダー.md) | LLM プロバイダ実装。Claude/OpenAI/Gemini を関数として抽象化・ベンダー例外のラップ |
| 2 | [python/llm/Instructor.md](python/llm/Instructor.md) | Instructor + Pydantic による構造化出力。タスク固有クライアント関数の作り方 |
| 3 | [python/llm/プロンプト執筆.md](python/llm/プロンプト執筆.md) | プロンプトファイルの作成と組み立て。prompts/ ルート・H3 パーツ・static vs dynamic |
| 4 | [python/llm/プロンプトローダー.md](python/llm/プロンプトローダー.md) | プロンプトローダー実装。index_loader / builder / types 配置・Jinja2 StrictUndefined |
| 5 | [python/llm/コストとキャッシュ.md](python/llm/コストとキャッシュ.md) | コスト管理。プロンプトキャッシュ設計・cache_control・Batch API・streaming |
| 6 | [python/llm/例外とリトライ.md](python/llm/例外とリトライ.md) | LLM 例外クラス階層。rate-limit / server / auth / timeout・リトライ戦略 |

### FastAPI

| # | ファイル | 内容 |
|---|---|---|
| 1 | [python/fastapi/アプリケーション.md](python/fastapi/アプリケーション.md) | FastAPI アプリ構成。build_app パターン・lifespan・middleware・CORS |
| 2 | [python/fastapi/ルート定義.md](python/fastapi/ルート定義.md) | ルーター実装。Annotated[Type, Depends]・ルート関数はシン・ビジネスロジックは service.py |
| 3 | [python/fastapi/スキーマ.md](python/fastapi/スキーマ.md) | I/O Pydantic スキーマ。Field 制約・to_domain / from_domain メソッド |
| 4 | [python/fastapi/認証とエラー.md](python/fastapi/認証とエラー.md) | Depends による認証・SecretStr 処理・exception_handler によるエラー処理 |
| 5 | [python/fastapi/ヘルスチェック.md](python/fastapi/ヘルスチェック.md) | ヘルスチェック。/healthz で 200 を返すだけのシンプルな実装 |

### テスト

| # | ファイル | 内容 |
|---|---|---|
| 1 | [python/testing/テスト戦略.md](python/testing/テスト戦略.md) | テストポリシー。ユニットテストなし・結合テスト + スモークテストのみ |
| 2 | [python/testing/pytest.md](python/testing/pytest.md) | pytest 規約。conftest.py・fixtures・parametrize・pytest-asyncio・tests/ レイアウト |
| 3 | [python/testing/モック.md](python/testing/モック.md) | 結合テスト用モックパターン。LLM モック・HTTP モック・時刻モック |

---

## Next.js

### バックエンド (API ルート)

| # | ファイル | 内容 |
|---|---|---|
| 1 | [next/backend/APIフォルダ概要.md](next/backend/APIフォルダ概要.md) | app/api/v1/{resource}/ の 6 ファイル責務分離・呼び出し階層 |
| 2 | [next/backend/ルート-ts.md](next/backend/ルート-ts.md) | route.ts — HTTP ハンドラ。withRouteErrorHandling・getAuthContext・Zod パース |
| 3 | [next/backend/サービス-ts.md](next/backend/サービス-ts.md) | service.ts — ビジネスロジック + トランザクション境界 |
| 4 | [next/backend/DB-ts.md](next/backend/DB-ts.md) | db.ts — 書き込み専用（INSERT/UPDATE/DELETE）。楽観的ロック |
| 5 | [next/backend/クエリ-ts.md](next/backend/クエリ-ts.md) | query.ts — 読み取り専用（SELECT）。フィルタ Zod スキーマ + fetchXxx 関数 |
| 6 | [next/backend/クライアント-ts.md](next/backend/クライアント-ts.md) | client.ts — クライアント側 fetch ヘルパー。AppError.fromResponse でラップ |
| 7 | [next/backend/DBヘルパー-ts.md](next/backend/DBヘルパー-ts.md) | dbHelper.ts — リソース内共通ヘルパー（ページング計算等） |
| 8 | [next/backend/アクション-ts.md](next/backend/アクション-ts.md) | actions.ts — Server Action 群。ActionResult<T>・revalidateTag + cacheLife |

### バックエンド (認証・DB)

| # | ファイル | 内容 |
|---|---|---|
| 1 | [next/backend/認証コンテキスト.md](next/backend/認証コンテキスト.md) | getAuthContext() — route/Server Action/Server Component の統一エントリポイント |
| 2 | [next/backend/認証セットアップ.md](next/backend/認証セットアップ.md) | lib/auth.ts — Better Auth セットアップ。drizzleAdapter・socialProviders |
| 3 | [next/backend/認証スキーマ.md](next/backend/認証スキーマ.md) | drizzle/schema.ts の認証テーブル。Better Auth 公式 schema 厳守 |
| 4 | [next/backend/認証アクション.md](next/backend/認証アクション.md) | loginAction / signupAction / signOutAction。Better Auth API + Zod + redirect |
| 5 | [next/backend/認証クライアント.md](next/backend/認証クライアント.md) | クライアント側 createAuthClient + useSession |
| 6 | [next/backend/DB-ID設計.md](next/backend/DB-ID設計.md) | 主キー設計。マスター = integer()・データ = uuid()・認証 = text |
| 7 | [next/backend/DBタイムスタンプ.md](next/backend/DBタイムスタンプ.md) | 共通カラム timestamps（createdAt/updatedAt）と auditFields |
| 8 | [next/backend/DBエナム.md](next/backend/DBエナム.md) | pgEnum 定義。命名 camelCase 単数・Enum 接尾辞なし |
| 9 | [next/backend/DBリレーション.md](next/backend/DBリレーション.md) | 外部キー + relations() + index 設計。onDelete の選び方 |
| 10 | [next/backend/DBトランザクション.md](next/backend/DBトランザクション.md) | Drizzle トランザクション規約。service.ts が境界・Promise.all 禁止 |
| 11 | [next/backend/DB楽観的ロック.md](next/backend/DB楽観的ロック.md) | 楽観的ロック（updatedAt 比較）。VersionConflictError |
| 12 | [next/backend/DB変更履歴.md](next/backend/DB変更履歴.md) | ハードデリート + history テーブルパターン |
| 13 | [next/backend/DBマイグレーション.md](next/backend/DBマイグレーション.md) | drizzle-kit マイグレーション運用。production 自動適用 NG |
| 14 | [next/backend/Drizzleスタイル.md](next/backend/Drizzleスタイル.md) | SQL Builder vs Relational Queries の使い分け |

### バックエンド (インフラ)

| # | ファイル | 内容 |
|---|---|---|
| 1 | [next/backend/プロキシ.md](next/backend/プロキシ.md) | proxy.ts — 認証ガード・A/B testing・ヘッダ書き換え |
| 2 | [next/backend/キャッシュ.md](next/backend/キャッシュ.md) | Next.js 16 キャッシュ API。"use cache" + cacheLife/cacheTag・revalidateTag |
| 3 | [next/backend/ウェブフック.md](next/backend/ウェブフック.md) | Webhook 受信。署名検証（raw body）・idempotency |
| 4 | [next/backend/ジョブ.md](next/backend/ジョブ.md) | バックグラウンドジョブ / Cron。Vercel Cron・after()・Inngest / QStash |
| 5 | [next/backend/リアルタイム.md](next/backend/リアルタイム.md) | リアルタイム機能。SSE 第一選択・Pusher・Supabase Realtime |
| 6 | [next/backend/レートリミット.md](next/backend/レートリミット.md) | Upstash Ratelimit によるレート制限。proxy.ts と route.ts で 2 段階 |
| 7 | [next/backend/冪等性.md](next/backend/冪等性.md) | Idempotency-Key ヘッダ。DB 保存で二重実行防止 |

### フロントエンド (画面構成)

| # | ファイル | 内容 |
|---|---|---|
| 1 | [next/frontend/appフォルダ概要.md](next/frontend/appフォルダ概要.md) | app/ フォルダ全体図。Route Group (authenticated)/(auth)/(shared) |
| 2 | [next/frontend/ルートグループ.md](next/frontend/ルートグループ.md) | Route Groups の役割と認証ガード layout.tsx |
| 3 | [next/frontend/フィーチャーフォルダ.md](next/frontend/フィーチャーフォルダ.md) | app/(authenticated)/{feature}/ フォルダ構成 |
| 4 | [next/frontend/IDルーティング.md](next/frontend/IDルーティング.md) | [id]/ ルーティング。[id]/page.tsx を View 画面そのものに |
| 5 | [next/frontend/一覧ページ-tsx.md](next/frontend/一覧ページ-tsx.md) | page.tsx — 一覧 Server Component。query.ts から取得し Client Screen に渡す |
| 6 | [next/frontend/一覧スクリーン-tsx.md](next/frontend/一覧スクリーン-tsx.md) | ListScreen — 一覧 Client Component。URL state + TanStack Query |
| 7 | [next/frontend/詳細ページ-tsx.md](next/frontend/詳細ページ-tsx.md) | [id]/page.tsx — View Server Component。notFound() + generateMetadata |
| 8 | [next/frontend/詳細スクリーン-tsx.md](next/frontend/詳細スクリーン-tsx.md) | ViewScreen — View Client Component。canEdit でボタン出し分け |
| 9 | [next/frontend/編集ページ-tsx.md](next/frontend/編集ページ-tsx.md) | [id]/edit/page.tsx — Edit Server Component。権限ガード |
| 10 | [next/frontend/編集スクリーン-tsx.md](next/frontend/編集スクリーン-tsx.md) | EditScreen / NewScreen — shadcn Form + RHF + Zod + Server Action |

### フロントエンド (コンポーネント)

| # | ファイル | 内容 |
|---|---|---|
| 1 | [next/frontend/フォーム-ts.md](next/frontend/フォーム-ts.md) | form.ts — Zod schema + Type。new/edit で共用・エラー文言は日本語 |
| 2 | [next/frontend/フォームコンポーネント.md](next/frontend/フォームコンポーネント.md) | shadcn Form + FormField + FormItem の組み合わせ。入力タイプ別パターン |
| 3 | [next/frontend/ダイアログ.md](next/frontend/ダイアログ.md) | Dialog / AlertDialog / Sheet / Drawer / Popover パターン |
| 4 | [next/frontend/コンポーネントカタログ.md](next/frontend/コンポーネントカタログ.md) | app/(shared)/components/ カタログ。新規作成前に確認 |
| 5 | [next/frontend/スクリーンラッパー.md](next/frontend/スクリーンラッパー.md) | ScreenWrapper — 全 Screen の最外殻。max-w-screen-xl + padding + isLoading |
| 6 | [next/frontend/ページヘッダー.md](next/frontend/ページヘッダー.md) | PageHeader — title + description + actions。1 画面 1 つ |
| 7 | [next/frontend/ローディングボタン.md](next/frontend/ローディングボタン.md) | LoadingButton — 非同期 onClick 用。Loader2 spinner + disable |
| 8 | [next/frontend/タグ入力.md](next/frontend/タグ入力.md) | TagInput — IME 対応タグ入力。Enter で確定・IME 入力中の Enter 無視 |
| 9 | [next/frontend/空状態.md](next/frontend/空状態.md) | EmptyState — 空状態 UI。message + description + action |
| 10 | [next/frontend/必須マーク.md](next/frontend/必須マーク.md) | RequiredMark — FormLabel 内の赤い * |
| 11 | [next/frontend/確認ダイアログ.md](next/frontend/確認ダイアログ.md) | useConfirmDialog() — await confirm({...}) で Promise boolean |
| 12 | [next/frontend/自動保存.md](next/frontend/自動保存.md) | フォーム自動保存パターン。debounce + Server Action + 楽観 UI + localStorage draft |
| 13 | [next/frontend/自動保存インジケーター.md](next/frontend/自動保存インジケーター.md) | AutosaveIndicator — idle/saving/saved/error 状態表示 |
| 14 | [next/frontend/エラー-tsx.md](next/frontend/エラー-tsx.md) | error.tsx / global-error.tsx — エラーバウンダリ。digest + reset() |
| 15 | [next/frontend/404-tsx.md](next/frontend/404-tsx.md) | not-found.tsx — 404 ページ。notFound() で自動表示 |

### フロントエンド (状態・フック)

| # | ファイル | 内容 |
|---|---|---|
| 1 | [next/frontend/useQueryパターン.md](next/frontend/useQueryパターン.md) | use{Feature}(s).ts — TanStack Query 読み取り。queryKey 設計・SSR hydrate |
| 2 | [next/frontend/useMutationパターン.md](next/frontend/useMutationパターン.md) | use{Verb}{Feature}.ts — useMutation。楽観更新 / 並列 / キャンセル時のみ |
| 3 | [next/frontend/useFormパターン.md](next/frontend/useFormパターン.md) | use{Feature}Form.ts — react-hook-form 内包。formState.isDirty |
| 4 | [next/frontend/useUrlStateパターン.md](next/frontend/useUrlStateパターン.md) | use{Feature}UrlState.ts — URL クエリ ↔ state。nuqs 推奨 |
| 5 | [next/frontend/useActionState.md](next/frontend/useActionState.md) | React 19 Hook 群 (useTransition/useActionState/useFormStatus/useOptimistic) の使い分け |
| 6 | [next/frontend/状態管理判断基準.md](next/frontend/状態管理判断基準.md) | 状態の置き場所決定フロー。TanStack Query → URL → Context/Zustand → useState → RHF |
| 7 | [next/frontend/クエリクライアントセットアップ.md](next/frontend/クエリクライアントセットアップ.md) | QueryProvider.tsx — staleTime 0・refetchOnWindowFocus false |
| 8 | [next/frontend/コンテキストパターン.md](next/frontend/コンテキストパターン.md) | React Context — 共有 UI state パターン。AppShellProvider への追加 |
| 9 | [next/frontend/Zustandパターン.md](next/frontend/Zustandパターン.md) | Zustand — クロスルート state。selector 部分購読・persist |
| 10 | [next/frontend/エンドポイント.md](next/frontend/エンドポイント.md) | endpoints.ts — URL 定数管理。RESOURCE_URL + API_URL |

### フロントエンド (規約・SEO・アセット)

| # | ファイル | 内容 |
|---|---|---|
| 1 | [next/frontend/conventions/命名規則.md](next/frontend/conventions/命名規則.md) | 命名規約。フォルダ kebab-case・Screen PascalCase・hook は use prefix |
| 2 | [next/frontend/conventions/コメント.md](next/frontend/conventions/コメント.md) | コメント規約。日本語・exported に 1 行 JSDoc |
| 3 | [next/frontend/conventions/型定義.md](next/frontend/conventions/型定義.md) | 型定義。z.infer<>・import type・Drizzle $inferSelect/$inferInsert |
| 4 | [next/frontend/conventions/ルートファイル規約.md](next/frontend/conventions/ルートファイル規約.md) | App Router 標準ファイル (page/layout/loading/error/route/proxy) の役割 |
| 5 | [next/frontend/conventions/サーバーvsクライアント.md](next/frontend/conventions/サーバーvsクライアント.md) | Server Component と Client Component の境界。'use client' は深い葉に |
| 6 | [next/frontend/SEO.md](next/frontend/SEO.md) | Metadata API。generateMetadata・sitemap.ts・robots.ts・JSON-LD |
| 7 | [next/frontend/アセット.md](next/frontend/アセット.md) | next/image + next/font。Next.js 16 破壊的変更・priority・placeholder=blur |
| 8 | [next/frontend/PWA.md](next/frontend/PWA.md) | PWA / Service Worker / Push 通知。manifest.ts・serwist・VAPID |
| 9 | [next/frontend/ストリーミング.md](next/frontend/ストリーミング.md) | Streaming / Suspense / Cache Components (PPR)。"use cache" + View Transitions |

### 共有インフラ

| # | ファイル | 内容 |
|---|---|---|
| 1 | [next/shared/環境変数.md](next/shared/環境変数.md) | 環境変数 (.env) + YAML 設定の使い分け。t3-env で型安全 env |
| 2 | [next/shared/セキュリティ.md](next/shared/セキュリティ.md) | セキュリティヘッダ (CSP/HSTS)・CSRF・XSS・SQL Injection・入力 Zod |
| 3 | [next/shared/エラークラス.md](next/shared/エラークラス.md) | エラークラス階層。AppError → ClientValueError / VersionConflictError など |
| 4 | [next/shared/エラールートハンドラー.md](next/shared/エラールートハンドラー.md) | withRouteErrorHandling — route.ts 用エラー JSON 変換 |
| 5 | [next/shared/エラーアクションハンドラー.md](next/shared/エラーアクションハンドラー.md) | handleActionError — Server Action 内 try/catch → ActionResult<T> |
| 6 | [next/shared/エラークライアントハンドラー.md](next/shared/エラークライアントハンドラー.md) | handleAppError — クライアント側エラー処理。認証エラーで /login 遷移 |
| 7 | [next/shared/ロガー実装.md](next/shared/ロガー実装.md) | logger.ts — JSON Lines ロガー実装。production はクライアント warn 以上強制 |
| 8 | [next/shared/ロガータグ.md](next/shared/ロガータグ.md) | Logger Component tag 命名規約。{layer}:{name} 形式 |

### テスト

| # | ファイル | 内容 |
|---|---|---|
| 1 | [next/testing/テスト戦略.md](next/testing/テスト戦略.md) | テスト戦略全体。Vitest (Unit/Component) + Playwright (E2E) + MSW |
| 2 | [next/testing/ユニットテスト.md](next/testing/ユニットテスト.md) | Unit / Component test (Vitest)。Schema test・Component test (Testing Library) |
| 3 | [next/testing/E2Eテスト.md](next/testing/E2Eテスト.md) | E2E test (Playwright)。Page Object Model・Storage State 認証・Chromatic |
| 4 | [next/testing/フィクスチャー.md](next/testing/フィクスチャー.md) | テストデータ Factory パターン。build*/seed*/clean*・nanoid で一意命名 |

### DevOps / DevTools

| # | ファイル | 内容 |
|---|---|---|
| 1 | [next/devops/デプロイ.md](next/devops/デプロイ.md) | デプロイ。Vercel 第一選択・self-host (Docker + Nginx)・DB は Supabase/Neon |
| 2 | [next/devtools/Storybook.md](next/devtools/Storybook.md) | Storybook 8.x + @storybook/nextjs-vite。addon-a11y・Chromatic 視覚回帰 |
| 3 | [next/devtools/モック.md](next/devtools/モック.md) | MSW セットアップ。mocks/handlers.ts 集約・dev は Service Worker |
| 4 | [next/devtools/リントとフォーマット.md](next/devtools/リントとフォーマット.md) | ESLint v9 Flat Config + Prettier。prettier-plugin-tailwindcss・lint-staged |
