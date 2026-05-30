# dev-kit リファレンス インデックス

`references/` 配下のリファレンスドキュメント一覧。技術スタック別に分類。

---

## Markdown

| # | ファイル | 内容 |
|---|---|---|
| 1 | [markdown/markdown-table.md](markdown/markdown-table.md) | Markdown テーブル書式規約。`#` 列必須・〃（繰り返し記号）の使い方 |
| 2 | [markdown/markdown-editing.md](markdown/markdown-editing.md) | Markdown フロントマター配置ルール。`---` の前に何も書かない |

---

## HTML / CSS / JS

Vanilla HTML + CSS + JS プロジェクトの設計方針。

| # | ファイル | 内容 |
|---|---|---|
| 1 | [html/principles.md](html/principles.md) | HTML/CSS/JS 開発原則。DRY/集中化・FLOCSS レイヤー・デザイントークン・JS 規約 |
| 2 | [html/ui-design.md](html/ui-design.md) | UX パターンと共通部品優先ルール。画面を書く前に shared リソースを読む |
| 3 | [html/debug-fab-sync.md](html/debug-fab-sync.md) | debug-fab テンプレート同期ルール。uidev.js / uidev.css 変更時の SKILL.md 更新 |
| 4 | [html/css-js-link.md](html/css-js-link.md) | CSS クラス ↔ JS DOM アクセス連動ルール。FLOCSS クラス定義と DOM アクセスの同期 |
| 5 | [html/common-component-first.md](html/common-component-first.md) | 共通部品優先ルール。新規 UI 追加前に shared 定数・ルート・コンポーネント CSS/JS を読む |

---

## Python

### コア言語規約

| # | ファイル | 内容 |
|---|---|---|
| 1 | [python/core/naming.md](python/core/naming.md) | 命名規約。snake_case 関数・UpperCamel 型エイリアス・標準ファイル名 |
| 2 | [python/core/comments.md](python/core/comments.md) | コメント規約。exported に 1 行 docstring・PR 番号付き変更履歴・TODO にはイシュー番号 |
| 3 | [python/core/type-hints.md](python/core/type-hints.md) | 型ヒント規約。PEP 695 generics・Self・@override・Annotated・type 文 |
| 4 | [python/core/decorators.md](python/core/decorators.md) | 推奨デコレータ。@dataclass / @final / @cache / @override / @contextmanager ほか |
| 5 | [python/core/language-rules.md](python/core/language-rules.md) | 言語規則。コメントは日本語・f-string・import 順・例外クラス階層 |
| 6 | [python/core/style.md](python/core/style.md) | スタイル設定。ruff/mypy/pyright 推奨設定・行長 100・ダブルクォート |

### アーキテクチャ

| # | ファイル | 内容 |
|---|---|---|
| 1 | [python/architecture/layout.md](python/architecture/layout.md) | トップレベルレイアウト。shared/ と main.py が必須・feature/integrations/server はオプション |
| 2 | [python/architecture/ts-style.md](python/architecture/ts-style.md) | TypeScript スタイル Python。関数型エイリアス DI・Protocol 構造的型付け |
| 3 | [python/architecture/composition-root.md](python/architecture/composition-root.md) | main.py の責務。build_handlers() で DI・Handlers dataclass |
| 4 | [python/architecture/dependencies.md](python/architecture/dependencies.md) | 依存方向ルール。features/server → integrations → shared の一方向 |
| 5 | [python/architecture/design-principles.md](python/architecture/design-principles.md) | 設計原則の優先順位。DRY > SOLID > 拡張性意識。関数ファースト |
| 6 | [python/architecture/refactoring-judgement.md](python/architecture/refactoring-judgement.md) | リファクタリング判断基準。抽出・抽象化・外部化・ファイル分割の閾値 |

### 共有モジュール

| # | ファイル | 内容 |
|---|---|---|
| 1 | [python/shared/logger.md](python/shared/logger.md) | 標準 JSON Lines ロガー。get_logger(__name__)・構造化ログ・ログレベルポリシー |
| 2 | [python/shared/settings.md](python/shared/settings.md) | pydantic_settings.BaseSettings 標準パターン。.env /.env.sample・SecretStr |
| 3 | [python/shared/secrets-and-env.md](python/shared/secrets-and-env.md) | シークレット / 環境変数 / 構造 / アセット / ランタイム状態の分離 |
| 4 | [python/shared/errors.md](python/shared/errors.md) | 例外クラス階層。AppError 基底クラス・ドメイン例外・HTTP マッピング |
| 5 | [python/shared/types.md](python/shared/types.md) | 共通型エイリアス。NewType と type 文の使い分け・識別子型（UserId 等） |
| 6 | [python/shared/constants.md](python/shared/constants.md) | constants.py の役割境界。PROJECT_ROOT / LOG_DIR 等の事前計算パス |

### スクリプト

| # | ファイル | 内容 |
|---|---|---|
| 1 | [python/scripts/python-script.md](python/scripts/python-script.md) | 単一ファイル Python スクリプト構造。docstring・argparse・main() -> int |
| 2 | [python/scripts/launchers-unix.md](python/scripts/launchers-unix.md) | UNIX シェルスクリプト。set -euo pipefail・tee でログ・.venv アクティベーション |
| 3 | [python/scripts/tkinter.md](python/scripts/tkinter.md) | tkinter GUI 規約。標準スタイル・設定ダイアログ・青アクセントカラー |

### 並行処理

| # | ファイル | 内容 |
|---|---|---|
| 1 | [python/concurrency/async.md](python/concurrency/async.md) | asyncio 規約。TaskGroup・asyncio.timeout・同期/非同期境界 |
| 2 | [python/concurrency/parallelism.md](python/concurrency/parallelism.md) | 並列処理。multiprocessing / threading / subinterpreters の選び方 |

### パッケージング

| # | ファイル | 内容 |
|---|---|---|
| 1 | [python/packaging/pyproject.md](python/packaging/pyproject.md) | pyproject.toml サンプル全量。[project] / [tool.ruff] / [tool.mypy] など |
| 2 | [python/packaging/dependencies.md](python/packaging/dependencies.md) | 依存管理。uv 標準・optional-dependencies.dev 必須・.venv 統一 |
| 3 | [python/packaging/distribution.md](python/packaging/distribution.md) | 配布。wheel/sdist・PyPI publish・entry_points で CLI 公開 |
| 4 | [python/packaging/python-versions.md](python/packaging/python-versions.md) | Python バージョンポリシー。最新を使う・3.12 以降の機能表 |

### パフォーマンス

| # | ファイル | 内容 |
|---|---|---|
| 1 | [python/performance/cheatsheet.md](python/performance/cheatsheet.md) | パフォーマンスチートシート。プロファイラ選択・ホットパスチェックリスト |

### LLM 統合

| # | ファイル | 内容 |
|---|---|---|
| 1 | [python/llm/providers.md](python/llm/providers.md) | LLM プロバイダ実装。Claude/OpenAI/Gemini を関数として抽象化・ベンダー例外のラップ |
| 2 | [python/llm/instructor.md](python/llm/instructor.md) | Instructor + Pydantic による構造化出力。タスク固有クライアント関数の作り方 |
| 3 | [python/llm/prompts-authoring.md](python/llm/prompts-authoring.md) | プロンプトファイルの作成と組み立て。prompts/ ルート・H3 パーツ・static vs dynamic |
| 4 | [python/llm/prompts-loader.md](python/llm/prompts-loader.md) | プロンプトローダー実装。index_loader / builder / types 配置・Jinja2 StrictUndefined |
| 5 | [python/llm/cost-cache.md](python/llm/cost-cache.md) | コスト管理。プロンプトキャッシュ設計・cache_control・Batch API・streaming |
| 6 | [python/llm/exceptions-retry.md](python/llm/exceptions-retry.md) | LLM 例外クラス階層。rate-limit / server / auth / timeout・リトライ戦略 |

### FastAPI

| # | ファイル | 内容 |
|---|---|---|
| 1 | [python/fastapi/app.md](python/fastapi/app.md) | FastAPI アプリ構成。build_app パターン・lifespan・middleware・CORS |
| 2 | [python/fastapi/routes.md](python/fastapi/routes.md) | ルーター実装。Annotated[Type, Depends]・ルート関数はシン・ビジネスロジックは service.py |
| 3 | [python/fastapi/schemas.md](python/fastapi/schemas.md) | I/O Pydantic スキーマ。Field 制約・to_domain / from_domain メソッド |
| 4 | [python/fastapi/auth-and-errors.md](python/fastapi/auth-and-errors.md) | Depends による認証・SecretStr 処理・exception_handler によるエラー処理 |
| 5 | [python/fastapi/health.md](python/fastapi/health.md) | ヘルスチェック。/healthz で 200 を返すだけのシンプルな実装 |

### テスト

| # | ファイル | 内容 |
|---|---|---|
| 1 | [python/testing/strategy.md](python/testing/strategy.md) | テストポリシー。ユニットテストなし・結合テスト + スモークテストのみ |
| 2 | [python/testing/pytest.md](python/testing/pytest.md) | pytest 規約。conftest.py・fixtures・parametrize・pytest-asyncio・tests/ レイアウト |
| 3 | [python/testing/mocks.md](python/testing/mocks.md) | 結合テスト用モックパターン。LLM モック・HTTP モック・時刻モック |

---

## Next.js

### バックエンド (API ルート)

| # | ファイル | 内容 |
|---|---|---|
| 1 | [next/backend/api-folder-overview.md](next/backend/api-folder-overview.md) | app/api/v1/{resource}/ の 6 ファイル責務分離・呼び出し階層 |
| 2 | [next/backend/route-ts.md](next/backend/route-ts.md) | route.ts — HTTP ハンドラ。withRouteErrorHandling・getAuthContext・Zod パース |
| 3 | [next/backend/service-ts.md](next/backend/service-ts.md) | service.ts — ビジネスロジック + トランザクション境界 |
| 4 | [next/backend/db-ts.md](next/backend/db-ts.md) | db.ts — 書き込み専用（INSERT/UPDATE/DELETE）。楽観的ロック |
| 5 | [next/backend/query-ts.md](next/backend/query-ts.md) | query.ts — 読み取り専用（SELECT）。フィルタ Zod スキーマ + fetchXxx 関数 |
| 6 | [next/backend/client-ts.md](next/backend/client-ts.md) | client.ts — クライアント側 fetch ヘルパー。AppError.fromResponse でラップ |
| 7 | [next/backend/db-helper-ts.md](next/backend/db-helper-ts.md) | dbHelper.ts — リソース内共通ヘルパー（ページング計算等） |
| 8 | [next/backend/actions-ts.md](next/backend/actions-ts.md) | actions.ts — Server Action 群。ActionResult<T>・revalidateTag + cacheLife |

### バックエンド (認証・DB)

| # | ファイル | 内容 |
|---|---|---|
| 1 | [next/backend/auth-context.md](next/backend/auth-context.md) | getAuthContext() — route/Server Action/Server Component の統一エントリポイント |
| 2 | [next/backend/auth-setup.md](next/backend/auth-setup.md) | lib/auth.ts — Better Auth セットアップ。drizzleAdapter・socialProviders |
| 3 | [next/backend/auth-schema.md](next/backend/auth-schema.md) | drizzle/schema.ts の認証テーブル。Better Auth 公式 schema 厳守 |
| 4 | [next/backend/auth-actions.md](next/backend/auth-actions.md) | loginAction / signupAction / signOutAction。Better Auth API + Zod + redirect |
| 5 | [next/backend/auth-client.md](next/backend/auth-client.md) | クライアント側 createAuthClient + useSession |
| 6 | [next/backend/db-id.md](next/backend/db-id.md) | 主キー設計。マスター = integer()・データ = uuid()・認証 = text |
| 7 | [next/backend/db-timestamps.md](next/backend/db-timestamps.md) | 共通カラム timestamps（createdAt/updatedAt）と auditFields |
| 8 | [next/backend/db-enum.md](next/backend/db-enum.md) | pgEnum 定義。命名 camelCase 単数・Enum 接尾辞なし |
| 9 | [next/backend/db-relations.md](next/backend/db-relations.md) | 外部キー + relations() + index 設計。onDelete の選び方 |
| 10 | [next/backend/db-transaction.md](next/backend/db-transaction.md) | Drizzle トランザクション規約。service.ts が境界・Promise.all 禁止 |
| 11 | [next/backend/db-optimistic-lock.md](next/backend/db-optimistic-lock.md) | 楽観的ロック（updatedAt 比較）。VersionConflictError |
| 12 | [next/backend/db-history.md](next/backend/db-history.md) | ハードデリート + history テーブルパターン |
| 13 | [next/backend/db-migration.md](next/backend/db-migration.md) | drizzle-kit マイグレーション運用。production 自動適用 NG |
| 14 | [next/backend/drizzle-style.md](next/backend/drizzle-style.md) | SQL Builder vs Relational Queries の使い分け |

### バックエンド (インフラ)

| # | ファイル | 内容 |
|---|---|---|
| 1 | [next/backend/proxy.md](next/backend/proxy.md) | proxy.ts — 認証ガード・A/B testing・ヘッダ書き換え |
| 2 | [next/backend/caching.md](next/backend/caching.md) | Next.js 16 キャッシュ API。"use cache" + cacheLife/cacheTag・revalidateTag |
| 3 | [next/backend/webhooks.md](next/backend/webhooks.md) | Webhook 受信。署名検証（raw body）・idempotency |
| 4 | [next/backend/jobs.md](next/backend/jobs.md) | バックグラウンドジョブ / Cron。Vercel Cron・after()・Inngest / QStash |
| 5 | [next/backend/realtime.md](next/backend/realtime.md) | リアルタイム機能。SSE 第一選択・Pusher・Supabase Realtime |
| 6 | [next/backend/rate-limit.md](next/backend/rate-limit.md) | Upstash Ratelimit によるレート制限。proxy.ts と route.ts で 2 段階 |
| 7 | [next/backend/idempotency.md](next/backend/idempotency.md) | Idempotency-Key ヘッダ。DB 保存で二重実行防止 |

### フロントエンド (画面構成)

| # | ファイル | 内容 |
|---|---|---|
| 1 | [next/frontend/app-folder-overview.md](next/frontend/app-folder-overview.md) | app/ フォルダ全体図。Route Group (authenticated)/(auth)/(shared) |
| 2 | [next/frontend/route-groups.md](next/frontend/route-groups.md) | Route Groups の役割と認証ガード layout.tsx |
| 3 | [next/frontend/feature-folder.md](next/frontend/feature-folder.md) | app/(authenticated)/{feature}/ フォルダ構成 |
| 4 | [next/frontend/id-routing.md](next/frontend/id-routing.md) | [id]/ ルーティング。[id]/page.tsx を View 画面そのものに |
| 5 | [next/frontend/list-page-tsx.md](next/frontend/list-page-tsx.md) | page.tsx — 一覧 Server Component。query.ts から取得し Client Screen に渡す |
| 6 | [next/frontend/list-screen-tsx.md](next/frontend/list-screen-tsx.md) | ListScreen — 一覧 Client Component。URL state + TanStack Query |
| 7 | [next/frontend/view-page-tsx.md](next/frontend/view-page-tsx.md) | [id]/page.tsx — View Server Component。notFound() + generateMetadata |
| 8 | [next/frontend/view-screen-tsx.md](next/frontend/view-screen-tsx.md) | ViewScreen — View Client Component。canEdit でボタン出し分け |
| 9 | [next/frontend/edit-page-tsx.md](next/frontend/edit-page-tsx.md) | [id]/edit/page.tsx — Edit Server Component。権限ガード |
| 10 | [next/frontend/edit-screen-tsx.md](next/frontend/edit-screen-tsx.md) | EditScreen / NewScreen — shadcn Form + RHF + Zod + Server Action |

### フロントエンド (コンポーネント)

| # | ファイル | 内容 |
|---|---|---|
| 1 | [next/frontend/form-ts.md](next/frontend/form-ts.md) | form.ts — Zod schema + Type。new/edit で共用・エラー文言は日本語 |
| 2 | [next/frontend/form-component.md](next/frontend/form-component.md) | shadcn Form + FormField + FormItem の組み合わせ。入力タイプ別パターン |
| 3 | [next/frontend/dialog.md](next/frontend/dialog.md) | Dialog / AlertDialog / Sheet / Drawer / Popover パターン |
| 4 | [next/frontend/components-catalog.md](next/frontend/components-catalog.md) | app/(shared)/components/ カタログ。新規作成前に確認 |
| 5 | [next/frontend/screen-wrapper.md](next/frontend/screen-wrapper.md) | ScreenWrapper — 全 Screen の最外殻。max-w-screen-xl + padding + isLoading |
| 6 | [next/frontend/page-header.md](next/frontend/page-header.md) | PageHeader — title + description + actions。1 画面 1 つ |
| 7 | [next/frontend/loading-button.md](next/frontend/loading-button.md) | LoadingButton — 非同期 onClick 用。Loader2 spinner + disable |
| 8 | [next/frontend/tag-input.md](next/frontend/tag-input.md) | TagInput — IME 対応タグ入力。Enter で確定・IME 入力中の Enter 無視 |
| 9 | [next/frontend/empty-state.md](next/frontend/empty-state.md) | EmptyState — 空状態 UI。message + description + action |
| 10 | [next/frontend/required-mark.md](next/frontend/required-mark.md) | RequiredMark — FormLabel 内の赤い * |
| 11 | [next/frontend/confirm-dialog.md](next/frontend/confirm-dialog.md) | useConfirmDialog() — await confirm({...}) で Promise boolean |
| 12 | [next/frontend/autosave.md](next/frontend/autosave.md) | フォーム自動保存パターン。debounce + Server Action + 楽観 UI + localStorage draft |
| 13 | [next/frontend/autosave-indicator.md](next/frontend/autosave-indicator.md) | AutosaveIndicator — idle/saving/saved/error 状態表示 |
| 14 | [next/frontend/error-tsx.md](next/frontend/error-tsx.md) | error.tsx / global-error.tsx — エラーバウンダリ。digest + reset() |
| 15 | [next/frontend/not-found-tsx.md](next/frontend/not-found-tsx.md) | not-found.tsx — 404 ページ。notFound() で自動表示 |

### フロントエンド (状態・フック)

| # | ファイル | 内容 |
|---|---|---|
| 1 | [next/frontend/use-query-pattern.md](next/frontend/use-query-pattern.md) | use{Feature}(s).ts — TanStack Query 読み取り。queryKey 設計・SSR hydrate |
| 2 | [next/frontend/use-mutation-pattern.md](next/frontend/use-mutation-pattern.md) | use{Verb}{Feature}.ts — useMutation。楽観更新 / 並列 / キャンセル時のみ |
| 3 | [next/frontend/use-form-pattern.md](next/frontend/use-form-pattern.md) | use{Feature}Form.ts — react-hook-form 内包。formState.isDirty |
| 4 | [next/frontend/use-url-state-pattern.md](next/frontend/use-url-state-pattern.md) | use{Feature}UrlState.ts — URL クエリ ↔ state。nuqs 推奨 |
| 5 | [next/frontend/use-action-state.md](next/frontend/use-action-state.md) | React 19 Hook 群 (useTransition/useActionState/useFormStatus/useOptimistic) の使い分け |
| 6 | [next/frontend/state-decision.md](next/frontend/state-decision.md) | 状態の置き場所決定フロー。TanStack Query → URL → Context/Zustand → useState → RHF |
| 7 | [next/frontend/query-client-setup.md](next/frontend/query-client-setup.md) | QueryProvider.tsx — staleTime 0・refetchOnWindowFocus false |
| 8 | [next/frontend/context-pattern.md](next/frontend/context-pattern.md) | React Context — 共有 UI state パターン。AppShellProvider への追加 |
| 9 | [next/frontend/zustand-pattern.md](next/frontend/zustand-pattern.md) | Zustand — クロスルート state。selector 部分購読・persist |
| 10 | [next/frontend/endpoints.md](next/frontend/endpoints.md) | endpoints.ts — URL 定数管理。RESOURCE_URL + API_URL |

### フロントエンド (規約・SEO・アセット)

| # | ファイル | 内容 |
|---|---|---|
| 1 | [next/frontend/conventions/naming.md](next/frontend/conventions/naming.md) | 命名規約。フォルダ kebab-case・Screen PascalCase・hook は use prefix |
| 2 | [next/frontend/conventions/comments.md](next/frontend/conventions/comments.md) | コメント規約。日本語・exported に 1 行 JSDoc |
| 3 | [next/frontend/conventions/types.md](next/frontend/conventions/types.md) | 型定義。z.infer<>・import type・Drizzle $inferSelect/$inferInsert |
| 4 | [next/frontend/conventions/route-files.md](next/frontend/conventions/route-files.md) | App Router 標準ファイル (page/layout/loading/error/route/proxy) の役割 |
| 5 | [next/frontend/conventions/server-vs-client.md](next/frontend/conventions/server-vs-client.md) | Server Component と Client Component の境界。'use client' は深い葉に |
| 6 | [next/frontend/seo.md](next/frontend/seo.md) | Metadata API。generateMetadata・sitemap.ts・robots.ts・JSON-LD |
| 7 | [next/frontend/assets.md](next/frontend/assets.md) | next/image + next/font。Next.js 16 破壊的変更・priority・placeholder=blur |
| 8 | [next/frontend/pwa.md](next/frontend/pwa.md) | PWA / Service Worker / Push 通知。manifest.ts・serwist・VAPID |
| 9 | [next/frontend/streaming.md](next/frontend/streaming.md) | Streaming / Suspense / Cache Components (PPR)。"use cache" + View Transitions |

### 共有インフラ

| # | ファイル | 内容 |
|---|---|---|
| 1 | [next/shared/environment.md](next/shared/environment.md) | 環境変数 (.env) + YAML 設定の使い分け。t3-env で型安全 env |
| 2 | [next/shared/security.md](next/shared/security.md) | セキュリティヘッダ (CSP/HSTS)・CSRF・XSS・SQL Injection・入力 Zod |
| 3 | [next/shared/error-classes.md](next/shared/error-classes.md) | エラークラス階層。AppError → ClientValueError / VersionConflictError など |
| 4 | [next/shared/error-route-handler.md](next/shared/error-route-handler.md) | withRouteErrorHandling — route.ts 用エラー JSON 変換 |
| 5 | [next/shared/error-action-handler.md](next/shared/error-action-handler.md) | handleActionError — Server Action 内 try/catch → ActionResult<T> |
| 6 | [next/shared/error-client-handler.md](next/shared/error-client-handler.md) | handleAppError — クライアント側エラー処理。認証エラーで /login 遷移 |
| 7 | [next/shared/logger-impl.md](next/shared/logger-impl.md) | logger.ts — JSON Lines ロガー実装。production はクライアント warn 以上強制 |
| 8 | [next/shared/logger-tags.md](next/shared/logger-tags.md) | Logger Component tag 命名規約。{layer}:{name} 形式 |

### テスト

| # | ファイル | 内容 |
|---|---|---|
| 1 | [next/testing/strategy.md](next/testing/strategy.md) | テスト戦略全体。Vitest (Unit/Component) + Playwright (E2E) + MSW |
| 2 | [next/testing/unit.md](next/testing/unit.md) | Unit / Component test (Vitest)。Schema test・Component test (Testing Library) |
| 3 | [next/testing/e2e.md](next/testing/e2e.md) | E2E test (Playwright)。Page Object Model・Storage State 認証・Chromatic |
| 4 | [next/testing/fixtures.md](next/testing/fixtures.md) | テストデータ Factory パターン。build*/seed*/clean*・nanoid で一意命名 |

### DevOps / DevTools

| # | ファイル | 内容 |
|---|---|---|
| 1 | [next/devops/deploy.md](next/devops/deploy.md) | デプロイ。Vercel 第一選択・self-host (Docker + Nginx)・DB は Supabase/Neon |
| 2 | [next/devtools/storybook.md](next/devtools/storybook.md) | Storybook 8.x + @storybook/nextjs-vite。addon-a11y・Chromatic 視覚回帰 |
| 3 | [next/devtools/mock.md](next/devtools/mock.md) | MSW セットアップ。mocks/handlers.ts 集約・dev は Service Worker |
| 4 | [next/devtools/lint-and-format.md](next/devtools/lint-and-format.md) | ESLint v9 Flat Config + Prettier。prettier-plugin-tailwindcss・lint-staged |
