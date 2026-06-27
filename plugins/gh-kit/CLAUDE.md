# gh-kit ワークフロー設計

## モニター一覧（パイプライン順）

| #   | モニター名     | 起動スキル            | 監視ラベル          | 完了時の次ラベル                                                   | 入力          | 必須/任意                             |
| --- | -------------- | --------------------- | ------------------- | ------------------------------------------------------------------ | ------------- | ------------------------------------- |
| 1   | issue-triage   | gh-kit:issue-triage   | 確認:issue-triage   | 確認:issue-spec                                                    | Issue 番号    | 必須                                  |
| 2   | issue-spec     | gh-kit:issue-spec     | 確認:issue-spec     | 確認:issue-ui（画面あり）/ 確認:issue-arch（画面なし）             | 〃            | 〃                                    |
| 3   | issue-ui       | gh-kit:issue-ui       | 確認:issue-ui       | 確認:issue-arch                                                    | 〃            | 画面ありの場合のみ                    |
| 4   | issue-arch     | gh-kit:issue-arch     | 確認:issue-arch     | （ユーザー手動）確認:pr-plan                                       | 〃            | 実装系で必須                          |
| 5   | pr-plan        | gh-kit:pr-plan        | 確認:pr-plan        | 確認:pr-test                                                       | 〃            | 必須                                  |
| 6   | pr-test        | gh-kit:pr-test        | 確認:pr-test        | 確認:pr-impl                                                       | PR 番号       | 〃                                    |
| 7   | pr-impl        | gh-kit:pr-impl        | 確認:pr-impl        | 確認:pr-impl-review                                                | 〃            | 〃                                    |
| 8   | pr-impl-review | gh-kit:pr-impl-review | 確認:pr-impl-review | 確認:pr-doc-plan（合格時）/ 確認:pr-impl（差し戻し時）             | 〃            | 〃                                    |
| 9   | pr-doc-plan    | gh-kit:pr-doc-plan    | 確認:pr-doc-plan    | 確認:pr-doc（影響あり）/ 確認:pr-merge（影響なし）                 | 〃            | 必須（影響リスト確認のみ）            |
| 10  | pr-doc         | gh-kit:pr-doc         | 確認:pr-doc         | 確認:pr-doc-review                                                 | 〃            | ドキュメント影響あり時のみ            |
| 11  | pr-doc-review  | gh-kit:pr-doc-review  | 確認:pr-doc-review  | （ユーザー手動）確認:pr-merge（合格時）/ 確認:pr-doc（差し戻し時） | 〃            | 〃                                    |
| 12  | pr-merge       | gh-kit:pr-merge       | 確認:pr-merge       | 完了                                                               | 〃            | 必須                                  |
| 13  | reset          | gh-kit:reset          | 確認:reset          | 完了                                                               | Issue/PR 番号 | 不要化時のみ（ユーザー手動付与）      |

---

## 設計レベルとモニターの対応

| 設計レベル            | 担当モニター   | 決めること                                                          |
| --------------------- | -------------- | ------------------------------------------------------------------- |
| 管理                  | issue-triage   | タイトル・概要・背景・type/priority・分割判断                       |
| SA（システム要件）    | issue-spec     | 機能要件（エラー/バリ含む）・非機能要件・スコープ外                 |
| UI                    | issue-ui       | 画面構成・モック・画面遷移 **+ UI ライブラリ採用時は PoC まで実施** |
| SS（システム方式）    | issue-arch     | コンポーネント分割・採用ライブラリ・データフロー **+ ライブラリ選定で必要な場合は PoC 実施** |
| DD + 実装計画         | pr-plan        | worktree + Draft PR + 実装計画（コード変更一覧）+ テスト計画        |
| テスト                | pr-test        | テストコード作成（Red 状態）                                        |
| 実装                  | pr-impl        | 実装 → Green 化                                                     |
| 実装レビュー          | pr-impl-review | コード品質チェック                                                  |
| ドキュメント計画      | pr-doc-plan    | 実装結果を踏まえた詳細なドキュメント修正計画                        |
| ドキュメント実装      | pr-doc         | Wiki / CLAUDE.md / Rules の実コミット                               |
| ドキュメントレビュー  | pr-doc-review  | ドキュメント差分のレビュー                                          |
| マージ                | pr-merge       | マージ + コンフリクト解消 + worktree 削除                           |
| 中断リセット          | reset          | 不要化した Issue/PR の巻き戻し（追記 Wiki 削除・worktree 削除・クローズ） |

---

## issue本文の担当セクション

詳細は Wiki: **`gh-kit_規約_イシュー本文.md`**

担当モニター・サブセクション一覧・記入テンプレートはすべて Wiki に集約。


## PR本文の担当セクション

| セクション                | サブセクション                   | 必須or条件                         | 概要                                                                                           | 担当モニター                                         |
| ------------------------- | -------------------------------- | ---------------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| `## 紐づく Issue`         | -                                | 必須                               | 親 Issue 番号                                                                                  | pr-plan                                              |
| `## 実装計画`             | -                                | 必須                               | No / 完了 / 新規/変更 / レイヤー / 分類 / ファイル / 対象 / 概要 / 補足 の表（分類: クラス/メソッド/関数/コンポーネント/フック/型/DBカラム/マイグレーション/エンドポイント など。対象: クラス名・メソッド名・型名・カラム名など。概要: 何を追加/変更するかを 1〜2 文。完了は ⬜/✅、pr-impl が完了から ✅ に更新） | pr-plan が計画 / pr-impl がチェック                  |
| `## テスト計画`           | `### 単体テスト`                 | 実装系（ドキュメント系はスキップ） | 新規/変更/既存実行のテスト一覧 + 各行にチェックボックス（pr-impl で Green になったらチェック） | pr-plan が計画 / pr-test が追加 / pr-impl がチェック |
| 〃                        | `### 結合テスト`                 | 〃                                 | 〃                                                                                             | 〃                                                   |
| 〃                        | `### E2Eテスト`                  | 〃                                 | 〃                                                                                             | 〃                                                   |
| 〃                        | `### 外部疎通テスト`             | 起動環境系の最低限の確認が必要時   | 〃                                                                                             | 〃                                                   |
| `## ドキュメント変更計画` | -                                | ドキュメント影響あり時             | ページ / セクション / 変更内容 / 補足 / 完了 の 5 列表（同ページに複数変更あれば行を追加。pr-doc が変更完了するごとに「完了」列をチェック）  | pr-doc-plan が計画 / pr-doc がチェック               |


## rulesページの担当セクション
<!-- 'my-plugins\plugins\dev-kit\hooks\inject_rules\rules' -->

dev-kit のルール（言語/フレームワーク横断の規約。プロジェクトを跨いで使い回す）。Wiki と違ってプロジェクト固有情報は含まない。

> 担当モニターは全て `pr-doc-plan`（分類別スキル経由で並列処理）。

| 分類     | ファイルパス（rules/ 以下）                      | 概要                                                                         |
| -------- | ------------------------------------------------ | ---------------------------------------------------------------------------- |
| claude   | claude/Claude Code Tool活用.md                   | Write 前に空ファイル作成・Task 系ツール活用など Claude Code の基本ツール作法 |
| 〃       | claude/Claude_Json.md                            | settings.json 等 JSON ファイルでのコメント擬似記法・キー間空行ルール         |
| 〃       | claude/Claude共通.md                             | SKILL/ルール/CLAUDE.md 執筆時の簡潔・無冗長の共通方針                        |
| 〃       | claude/claudeプラグイン.md                       | プラグイン内テンプレートフォルダの規約と展開方法                             |
| 〃       | claude/mcp.md                                    | MCP サーバー作成ルール（FastMCP・stdio・構成）                               |
| 〃       | claude/skills活用.md                             | AgentSkills（SKILL.md）の動的コンテキスト注入・公式仕様                      |
| 〃       | claude/サブエージェント.md                       | スキル内ステップをサブエージェントに委譲する判断基準とマーカー               |
| 〃       | claude/フック.md                                 | フックスクリプト/プロンプトの配置と書き方・ワンタイムトークン                |
| 〃       | claude/ルール記載.md                             | ユーザ配下ルール記載時の汎用性・プロジェクト特化禁止                         |
| dev      | dev/yaml-sot.md                                  | 新規ドメインは index.yaml+settings.yaml の 2 段構成で SoT 化                 |
| 〃       | dev/コーディング全般.md                          | 例外を握りつぶさない・無闇なフォールバック禁止など言語横断のコーディング規約 |
| html     | html/components/カスタムエレメント.md            | Light DOM の自律カスタム要素・connectedCallback・属性駆動                    |
| 〃       | html/components/先読みカタログ.md                | 画面実装前に共通層を先読みして再利用する原則                                 |
| 〃       | html/components/共通シェル.md                    | ヘッダー・サイドバー等の app-shell 共通シェル方針                            |
| 〃       | html/core/iframe禁止.md                          | フロントエンドで iframe を使わない                                           |
| 〃       | html/core/ビルドレス原則.md                      | バンドラを使わずネイティブ ESM と素 CSS を配信（tsc 1 段のみ可）             |
| 〃       | html/css/コメント.md                             | CSS セレクタごとに直上コメントを書く・/* */ のみ使う                         |
| 〃       | html/css/トークン.md                             | デザイントークンを :root に集約・3 ティア・ライト固定                        |
| 〃       | html/css/ネスト.md                               | CSS Nesting 利用可・&__title 連結禁止・フル記述                              |
| 〃       | html/css/レイヤー構成.md                         | @layer 順序固定・全 CSS をレイヤーへ・utilities で !important 禁止           |
| 〃       | html/html/コメント.md                            | HTML のセクション/属性/hidden/Jinja ブロックへのコメント規約                 |
| 〃       | html/html/ネイティブ要素.md                      | dialog/details 等のネイティブ要素を第一選択する                              |
| 〃       | html/js/api層.md                                 | api 層 fetch ラッパーに通信集約・openapi 型のみ生成                          |
| 〃       | html/js/websocket.md                             | WsClient extends EventTarget・指数バックオフ・URL 定数化                     |
| 〃       | html/js/エンドポイント.md                        | URL 文字列をハードコードせず定数集約・使う範囲で配置先決定                   |
| 〃       | html/js/バニラTS方針.md                          | 関数指向で書く・クラスは Custom Element のみ・ライブラリ追加禁止             |
| 〃       | html/js/モジュール解決.md                        | import maps でモジュール解決・bare specifier・生成 .js を参照                |
| 〃       | html/js/レイヤー分離.md                          | UI/State/API の 3 層分離・下方向のみ依存                                     |
| 〃       | html/js/状態管理.md                              | リアクティブ強制せず手続き的更新可・URL クエリ反映推奨                       |
| 〃       | html/layout/レイアウトパターン.md                | サイドバー+メインの標準骨格・PC 固定                                         |
| 〃       | html/layout/画面テンプレート.md                  | 一覧/詳細/設定の画面型ごとの構成要点                                         |
| 〃       | html/mock/indexモック.md                         | モック index.html は各モック画面へのリンク集                                 |
| 〃       | html/mock/モックテーマ.md                        | モックテーマ画面の役割・デザイン方向性決め                                   |
| 〃       | html/mock/モック画面ルール.md                    | mocks/ 配下に FastAPI+HTML で疎結合にモック配置                              |
| 〃       | html/naming/cssクラス.md                         | CSS クラス命名（c-/l- 等のハンガリアン禁止・BEM 風連結）                     |
| 〃       | html/naming/カスタムエレメント.md                | app- 接頭辞+kebab・is 属性禁止（Safari 非対応）                              |
| 〃       | html/naming/ファイル名.md                        | kebab-case 統一・概念区切りはフォルダで分ける                                |
| 〃       | html/pages/_shared.md                            | pages/{domain}/_shared はドメイン内共通部品置き場                            |
| 〃       | html/pages/index-html.md                         | 各画面 index.html は _layout 継承・ブロック使い分け規約                      |
| 〃       | html/pages/screen-css.md                         | 画面固有 CSS も @layer 内・トークン参照・画面ローカル変数                    |
| 〃       | html/pages/screen-ts.md                          | screen.ts の作法（init 即時起動・getElementById・XSS エスケープ）            |
| 〃       | html/pages/画面の作り方.md                       | pages/{domain}/{screen}/ 配下のファイル構成と役割                            |
| 〃       | html/shared/components.md                        | shared/components の配置と共通スタイル方針                                   |
| 〃       | html/shared/core.md                              | shared/core に環境/定数/ルート値を集約・DOM/通信は持たない                   |
| 〃       | html/shared/css.md                               | shared/css は基盤スタイル置き場・layers.css がエントリ                       |
| 〃       | html/shared/fmt.md                               | fmt.ts に整形関数集約・純関数・DOM 不可                                      |
| 〃       | html/shared/lib.md                               | shared/lib は DOM 非依存の汎用ユーティリティ集約場所                         |
| 〃       | html/shared/logger.md                            | logger.ts でログ集約・console 直書き禁止                                     |
| 〃       | html/shared/vendor.md                            | 外部依存は vendoring で固定・CDN 依存禁止                                    |
| 〃       | html/testing/e2eテスト.md                        | Playwright E2E 規約（モック・ロケータ優先・直列実行）                        |
| 〃       | html/testing/テスト戦略.md                       | vitest+playwright の 2 層・ピラミッド構造                                    |
| 〃       | html/testing/ユニットテスト.md                   | vitest+jsdom で純 ESM をテスト・配置と対象選定                               |
| 〃       | html/tooling/tsc運用.md                          | tsc で ts→js 同階層 emit・バンドラ不使用                                    |
| 〃       | html/typescript/コメント.md                      | TS コメント規約（@param 等不要・export 直上に JSDoc）                        |
| 〃       | html/typescript/型システム.md                    | 汎用 TS の型方針（any 回避・union literal・関数型エイリアス）                |
| 〃       | html/typescript/関数とオブジェクト引数.md        | 依存は引数注入・2 引数以上はオブジェクトで受ける                             |
| 〃       | html/フォルダ構成.md                             | frontend/ 配下の shared+pages ディレクトリツリー定義                         |
| 〃       | html/モバイル対応.md                             | @media (max-width:768px) 単一で screen.css 末尾に追記する方式                |
| 〃       | html/共通化の判断.md                             | 部品の置き場所判断（使う範囲が最も狭い階層を選ぶ）                           |
| markdown | markdown/マークダウンテーブル.md                 | Markdown テーブル活用・No カラム付与基準                                     |
| 〃       | markdown/マークダウン編集.md                     | フロントマター配置・--- 区切り線の使用制限                                   |
| 〃       | markdown/マーメイド.md                           | mermaid でフローチャート作成（LR/TD 使い分け）                               |
| next     | next/backend/APIフォルダ概要.md                  | app/api/v{N}/{resource}/ の 6 ファイル責務分離（CQRS）                       |
| 〃       | next/backend/DB Enum.md                          | drizzle/schema.ts の pgEnum 運用・値削除回避                                 |
| 〃       | next/backend/DB-ID設計.md                        | 主キーは gen_random_uuid()・独自 ID 避ける                                   |
| 〃       | next/backend/DB-ts.md                            | api/db.ts は書き込み専用・1 関数 1 SQL・DatabaseError 包む                   |
| 〃       | next/backend/DBタイムスタンプ.md                 | createdAt/updatedAt を ISO 文字列共通カラムで持つ                            |
| 〃       | next/backend/DBヘルパー-ts.md                    | api/dbHelper.ts はリソース内共通の純粋関数                                   |
| 〃       | next/backend/DBマイグレーション.md               | drizzle-kit の追加/削除運用・破壊的変更手順                                  |
| 〃       | next/backend/DBリレーション.md                   | drizzle の relations/index/外部キー方針                                      |
| 〃       | next/backend/DB変更履歴.md                       | ソフトデリート禁止・履歴テーブル退避+ハードデリート                          |
| 〃       | next/backend/DB楽観的ロック.md                   | updatedAt 比較による VersionConflictError 検知パターン                       |
| 〃       | next/backend/Drizzleスタイル.md                  | SQL Builder 標準・Relational Query 限定使用・sql.raw 禁止                    |
| 〃       | next/backend/アクション-ts.md                    | Server Action 規約（use server/ActionResult/Zod/getAuthContext）             |
| 〃       | next/backend/ウェブフック.md                     | Webhook 受信パターン（配置・署名検証）                                       |
| 〃       | next/backend/キャッシュ.md                       | Next.js 16 の cacheComponents/use cache/cacheLife/cacheTag                   |
| 〃       | next/backend/クエリ-ts.md                        | api/query.ts は読み取り専用・Zod フィルタ・Promise.all 活用                  |
| 〃       | next/backend/クライアント-ts.md                  | api/client.ts の型 import・URL 定数経由・data unwrap                         |
| 〃       | next/backend/サービス-ts.md                      | api/service.ts がトランザクション境界・AppError 派生扱い                     |
| 〃       | next/backend/プロキシ.md                         | proxy.ts（旧 middleware）の認証ガード・matcher 設定                          |
| 〃       | next/backend/ルート-ts.md                        | route.ts は withRouteErrorHandling+認証+Zod+service 呼び                     |
| 〃       | next/backend/レートリミット.md                   | Upstash Ratelimit で proxy.ts と route.ts で二重適用                         |
| 〃       | next/backend/ローカルYAML開発DB.md               | dev 用 YAML データストアと本番 Drizzle 実装の差し替え                        |
| 〃       | next/backend/冪等性.md                           | Idempotency-Key ヘッダで二重実行防止対象を限定                               |
| 〃       | next/backend/認証アクション.md                   | auth.ts Server Action（Better Auth 経由の signIn/Up/Out）                    |
| 〃       | next/backend/認証クライアント.md                 | クライアント useSession（Better Auth）配置と利用                             |
| 〃       | next/backend/認証コンテキスト.md                 | getAuthContext() 統一エントリ・3 関数でセッション取得                        |
| 〃       | next/backend/認証スキーマ.md                     | Better Auth が要求する user/session/account/verification 定義                |
| 〃       | next/backend/認証セットアップ.md                 | lib/auth.ts の Better Auth 初期化・cookieCache・期限                         |
| 〃       | next/devops/デプロイ.md                          | Vercel を標準とするデプロイ先選定マトリクス                                  |
| 〃       | next/devtools/Storybook.md                       | shadcn 拡張の Storybook 構成・Vitest 統合                                    |
| 〃       | next/devtools/モック.md                          | MSW で fetch を intercept・dev/test 両用                                     |
| 〃       | next/devtools/リントとフォーマット.md            | ESLint/Prettier/tsconfig 設定（Next.js 16）                                  |
| 〃       | next/frontend/404-tsx.md                         | not-found.tsx は Server Component・戻るリンク必須                            |
| 〃       | next/frontend/IDルーティング.md                  | [id]/page.tsx が View 本体・edit/ との共通化方針                             |
| 〃       | next/frontend/PWA.md                             | manifest.ts・Apple 対応の PWA 設定                                           |
| 〃       | next/frontend/SEO.md                             | Metadata API・sitemap/robots/manifest・構造化データ                          |
| 〃       | next/frontend/Zustandパターン.md                 | Context で不十分な時の Zustand・配置・selector                               |
| 〃       | next/frontend/appフォルダ概要.md                 | app/ 配下の全体構成（Route Group 3 つ・API 配下）                            |
| 〃       | next/frontend/conventions/コメント規約.md        | Next.js App Router のコメントスタイル（JSX/Drizzle/Zod）                     |
| 〃       | next/frontend/conventions/ルートファイル規約.md  | page/layout/loading 等各 route segment の役割と配置                          |
| 〃       | next/frontend/conventions/命名規約.md            | フォルダ/ファイル/フック等の命名規則                                         |
| 〃       | next/frontend/conventions/型規約.md              | 型定義の置き場所マッピング                                                   |
| 〃       | next/frontend/url-state.md                       | URL クエリにスクリーン state を置く原則・読み書き方法                        |
| 〃       | next/frontend/useActionState.md                  | Server Action 呼び出しの hook 選択（useTransition 他）                       |
| 〃       | next/frontend/useFormパターン.md                 | use{Feature}Form.ts の構成・defaultValues と values 使い分け                 |
| 〃       | next/frontend/useMutationパターン.md             | useMutation 採用条件・楽観更新の許可リスト                                   |
| 〃       | next/frontend/useQueryパターン.md                | useQuery の戻り値/queryKey/initialData 規約                                  |
| 〃       | next/frontend/useUrlStateパターン.md             | use{Feature}UrlState.ts の nuqs 採用ルール                                   |
| 〃       | next/frontend/アセット.md                        | next/image の remotePatterns・priority・sizes 規約                           |
| 〃       | next/frontend/エラー-tsx.md                      | error.tsx/global-error.tsx の作法・reset() 設置                              |
| 〃       | next/frontend/エンドポイント.md                  | app/(shared)/endpoints.ts で URL 全集約・ハードコード禁止                    |
| 〃       | next/frontend/クエリクライアントセットアップ.md  | TanStack Query の QueryProvider 設定（staleTime 等）                         |
| 〃       | next/frontend/コンテキストパターン.md            | React Context の使い所と運用ルール                                           |
| 〃       | next/frontend/コンポーネントカタログ.md          | (shared)/components/ の自前ラッパー一覧                                      |
| 〃       | next/frontend/スクリーンラッパー.md              | <ScreenWrapper> の責務と isLoading オーバーレイ                              |
| 〃       | next/frontend/ストリーミング.md                  | Suspense 境界と streaming・Skeleton フォールバック                           |
| 〃       | next/frontend/タグ入力.md                        | <TagInput> の IME 対応・onBlur 確定                                          |
| 〃       | next/frontend/ダイアログ.md                      | Dialog/AlertDialog/Sheet 等の suffix 選択                                    |
| 〃       | next/frontend/フィーチャーフォルダ.md            | app/(authenticated)/{feature}/ 配下の標準構成                                |
| 〃       | next/frontend/フォーム-ts.md                     | {feature}/form.ts に Zod schema と型を集約                                   |
| 〃       | next/frontend/フォームコンポーネント.md          | shadcn <Form>+RHF+Zod 標準組み合わせ                                         |
| 〃       | next/frontend/ページヘッダー.md                  | <PageHeader> の props・h1 利用・1 Screen 1 つ                                |
| 〃       | next/frontend/ルートグループ.md                  | (authenticated)/(auth)/(shared) の 3 グループ運用                            |
| 〃       | next/frontend/ローディングボタン.md              | <LoadingButton> で mutation ボタンを統一                                     |
| 〃       | next/frontend/一覧スクリーン-tsx.md              | ListScreen.tsx は use client+URL state+initial                               |
| 〃       | next/frontend/一覧ページ-tsx.md                  | 一覧 page.tsx は Zod パース+SEO metadata                                     |
| 〃       | next/frontend/必須マーク.md                      | <RequiredMark/> を必須フィールドにのみ付与                                   |
| 〃       | next/frontend/状態管理判断基準.md                | サーバー/URL/Context/Zustand/useState の決定フロー                           |
| 〃       | next/frontend/確認ダイアログ.md                  | useConfirmDialog() で window.confirm 代替                                    |
| 〃       | next/frontend/空状態.md                          | <EmptyState> で length 0 時の白画面防止                                      |
| 〃       | next/frontend/編集スクリーン-tsx.md              | EditScreen/NewScreen は shadcn Form+useTransition+Server Action              |
| 〃       | next/frontend/編集ページ-tsx.md                  | edit/page.tsx の notFound/redirect/canEdit 分岐                              |
| 〃       | next/frontend/自動保存.md                        | useAutosave hook で debounce 保存と古い結果無視                              |
| 〃       | next/frontend/自動保存インジケーター.md          | <AutosaveIndicator> の 4 状態と表示規約                                      |
| 〃       | next/frontend/詳細スクリーン-tsx.md              | ViewScreen.tsx は use client・読み取り専用・canEdit                          |
| 〃       | next/frontend/詳細ページ-tsx.md                  | [id]/page.tsx が View 本体・notFound・generateMetadata                       |
| 〃       | next/shared/エラーアクションハンドラー.md        | handleActionError で Server Action 例外を ActionResult 化                    |
| 〃       | next/shared/エラークライアントハンドラー.md      | handleAppError でクライアント側エラーを UX 変換                              |
| 〃       | next/shared/エラークラス.md                      | AppError 階層・fromResponse で API 失敗復元                                  |
| 〃       | next/shared/エラールートハンドラー.md            | withRouteErrorHandling で route.ts エラーを構造化 JSON へ                    |
| 〃       | next/shared/セキュリティ.md                      | セキュリティヘッダ・CSP nonce・CSRF 対策                                     |
| 〃       | next/shared/ロガータグ.md                        | logger.create("tag") タグ命名規約（layer:name 形式）                         |
| 〃       | next/shared/ロガー実装.md                        | logger.ts の JSON Lines 出力・level 運用・本番クランプ                       |
| 〃       | next/shared/環境変数.md                          | 環境変数は秘密のみ・構造化設定は YAML に分離                                 |
| 〃       | next/testing/E2Eテスト.md                        | Playwright 設定・storageState・webServer 自動起動                            |
| 〃       | next/testing/テスト戦略.md                       | Vitest+Playwright のピラミッド構造・各 Level ツール表                        |
| 〃       | next/testing/フィクスチャー.md                   | tests/fixtures の 4 点セット（build/seed/seeds/clean）                       |
| 〃       | next/testing/ユニットテスト.md                   | Vitest+Testing Library のユニット/コンポーネントテスト                       |
| python   | python/architecture/TypeScriptスタイル適用.md    | 関数ファースト+型エイリアス+DTO+Protocol で書く中心ドキュメント              |
| 〃       | python/architecture/コンポジションルート.md      | main.py で関数依存を組み立てる composition root                              |
| 〃       | python/architecture/リファクタリング判断.md      | DRY 化のトリガー（2 回目検討/3 回目必須）と粒度                              |
| 〃       | python/architecture/レイアウト.md                | 機能フォルダ型レイアウトのトップレベル構成                                   |
| 〃       | python/architecture/依存関係管理.md              | features→integrations→shared の依存方向ルール                              |
| 〃       | python/architecture/設計原則.md                  | DRY 最重視・SOLID 重視・YAGNI 不強制の優先順位                               |
| 〃       | python/concurrency/並列処理.md                   | GIL 前提・CPU/IO 分岐の並列処理判断フロー                                    |
| 〃       | python/concurrency/非同期処理.md                 | asyncio 規約（TaskGroup/timeout/to_thread）                                  |
| 〃       | python/core/コメント.md                          | Python 固有コメントルール（docstring 濃度マトリクス）                        |
| 〃       | python/core/スタイル.md                          | ruff/mypy/pyright/pytest ツール構成と設定                                    |
| 〃       | python/core/デコレーター.md                      | 推奨デコレータ表とハンドラーデコレータ用法                                   |
| 〃       | python/core/命名規則.md                          | モジュール/関数/型/Protocol 等の命名規約表                                   |
| 〃       | python/core/型ヒント.md                          | Python 3.12+ の PEP 695 必須・annotations import                             |
| 〃       | python/core/言語ルール.md                        | コメント/識別子/出力文字列の使用言語使い分け表                               |
| 〃       | python/fastapi/アプリケーション.md               | server/app.py の build_fastapi+lifespan 構成                                 |
| 〃       | python/fastapi/スキーマ.md                       | リクエスト/レスポンス Pydantic・to_domain/from_domain                        |
| 〃       | python/fastapi/ヘルスチェック.md                 | /healthz は生存判定のみ・liveness/readiness の分け方                         |
| 〃       | python/fastapi/ルート定義.md                     | ルーターは薄く 4 責務のみ・features に配置                                   |
| 〃       | python/fastapi/認証とエラー.md                   | Bearer/APIKey/Scope 認証パターンと例外ハンドラ                               |
| 〃       | python/llm/Instructor.md                         | Instructor で LLM 出力を Pydantic モデル化                                   |
| 〃       | python/llm/コストとキャッシュ.md                 | LLM トークン管理・用途別 max_tokens 目安                                     |
| 〃       | python/llm/プロバイダー.md                       | make_{provider}_chat ファクトリで関数注入抽象化                              |
| 〃       | python/llm/プロンプトローダー.md                 | prompts/index.yaml を読み Jinja2 で結合する実装                              |
| 〃       | python/llm/プロンプト執筆.md                     | プロンプトをファイル化・部品分割・index.yaml 組み立て                        |
| 〃       | python/llm/例外とリトライ.md                     | LlmError ベース例外分類とリトライ可否マトリクス                              |
| 〃       | python/packaging/Pythonバージョン.md             | 3.12+ を最低ライン・3.13 新機能の採用判断                                    |
| 〃       | python/packaging/pyproject設定.md                | pyproject.toml 標準テンプレート（project メタデータ）                        |
| 〃       | python/packaging/依存パッケージ管理.md           | uv 標準・コマンド早見表                                                      |
| 〃       | python/packaging/配布設定.md                     | uv build/publish・SemVer・CLI エントリポイント                               |
| 〃       | python/performance/パフォーマンスチートシート.md | 計測ツール早見表・最適化前に計測する原則                                     |
| 〃       | python/scripts/Pythonスクリプト.md               | scripts/ サブフォルダ配置・docstring 必須要素                                |
| 〃       | python/scripts/Tkinter.md                        | tkinter GUI 設計指針・テーマ統一・モーダル作法                               |
| 〃       | python/scripts/launchers-windows.md              | Windows .bat ランチャーの標準テンプレート                                    |
| 〃       | python/scripts/ランチャー-Unix.md                | UNIX 系 .sh ランチャーの標準テンプレート                                     |
| 〃       | python/shared/エラー定義.md                      | shared/errors.py の AppError 単一階層                                        |
| 〃       | python/shared/シークレットと環境変数.md          | .env/settings.yaml/コードでの値分離方針                                      |
| 〃       | python/shared/ロガー.md                          | JSON Lines 構造化ログ実装・get_logger 運用                                   |
| 〃       | python/shared/型定義.md                          | shared/types.py に横断的型のみ・引き上げ基準                                 |
| 〃       | python/shared/定数.md                            | shared/constants.py に計算済み不変値だけ置く                                 |
| 〃       | python/shared/設定.md                            | pydantic-settings で .env/環境変数を型安全に読む                             |
| 〃       | python/testing/pytest.md                         | pytest 規約（命名・fixture・conftest 階層）                                  |
| 〃       | python/testing/テスト戦略.md                     | 単体テスト書かない方針・結合+外部疎通の 2 種類のみ                           |
| 〃       | python/testing/モック.md                         | 関数型エイリアス DI 前提の Mock パターン早見表                               |


## wikiページの担当セクション

> 担当モニターは全て `pr-doc-plan`（分類別スキル経由で並列処理）。
> ここに載せるのは**全プロジェクトで共通で使うページ**のみ。my-plugins 固有のページ（テンプレート_ライブラリ選定論点.md など）はここには載せない。

| 分類             | ページ名                                 | 概要                                                         |
| ---------------- | ---------------------------------------- | ------------------------------------------------------------ |
| コード設計図     | クラス図_{モジュール名}.md               | クラス構成と関係（Mermaid classDiagram）                     |
| 〃               | シーケンス図_{機能名}.md                 | 処理の呼び出し順（Mermaid sequenceDiagram）                  |
| 〃               | 状態遷移図_{コンポーネント名}.md         | 状態を持つ要素の遷移（Mermaid stateDiagram）                 |
| 〃               | ER図.md                                  | DB スキーマ（Mermaid erDiagram）                             |
| 〃               | 画面遷移図_{機能名}.md                   | UI 画面間の遷移                                              |
| 〃               | アーキテクチャ図.md                      | システム全体構成（C4 / Mermaid）                             |
| 〃               | データフロー図_{機能名}.md               | データの流れ                                                 |
| 〃               | フローチャート_{機能名}.md               | エンドポイント/機能ごとの条件分岐フロー（Mermaid flowchart） |
| プロジェクト管理 | ラベル定義一覧.md                        | constants.sh のラベルと運用ルール                            |
| 〃               | ディレクトリ構成図.md                    | プラグイン全体のフォルダ階層                                 |
| 〃               | 命名規則.md                              | **プロジェクト固有**の命名規則のみ（ラベル名・スキル名など。一般的な言語規約は rules 側） |
| 運用・規約       | イシュードキュメント.md                  | Issue 本文テンプレート                                       |
| 〃               | PRドキュメント.md                        | PR 本文テンプレート                                          |
| 〃               | セットアップ手順.md                      | プラグインインストール手順                                   |
| Claude ハーネス  | スキル一覧.md                            | プラグイン内の全 SKILL.md の一覧と役割                       |
| 〃               | カスタムサブエージェント一覧.md          | agents/*.md の一覧と役割                                     |
| 〃               | フック一覧.md                            | session-start / PreToolUse などの設定一覧                    |
| 〃               | 動的注入対応表.md                        | 編集対象パス → 注入される Wiki ページの対応                  |
| 〃               | プラグイン構成.md                        | hooks / skills / agents / scripts の役割と関係               |
| 実装リファレンス | APIエンドポイント一覧.md                 | エンドポイントのパス・メソッド・パラメータ・レスポンス一覧   |
| 〃               | エラーコード・例外定義一覧.md            | エラーコード・例外クラスとその発生条件・ハンドリング方針     |
| 〃               | データモデル一覧.md                      | アプリケーション層の**データ構造の一覧**（リクエスト/レスポンス DTO・ドメインオブジェクト・型定義 など）。クラス図とは別軸でデータ型をプロジェクト横断で俯瞰する用（DB スキーマは `ER図.md` 参照） |
| 〃               | 外部ライブラリ一覧.md                    | 採用済みライブラリのインデックス（名前・バージョン・用途・`外部ライブラリ_{lib名}.md` へのリンク） |
| 〃               | 外部ライブラリ_{lib名}.md                    | このプロジェクトで使うメソッドとそのパラメータを公式ドキュメントから抜粋（インストール手順・バージョン明記）。書き方規約は `gh-kit_規約_外部ライブラリ.md` |
| 〃               | 外部API一覧.md                       | 採用済み外部 API のインデックス（名前・バージョン・用途・`外部API_{API名}.md` へのリンク）                                          |
| 〃               | 外部API_{API名}.md                       | このプロジェクトで使うエンドポイントを公式ドキュメントから抜粋（認証セットアップ・レートリミット・課金・リクエスト/レスポンス）。書き方規約は `gh-kit_規約_外部API.md` |
| テスト           | テスト実行方法.md                        | **プロジェクト固有**のテスト起動コマンドと前提条件（戦略自体は rules 側） |
| 〃               | テスト一覧.md                            | 既存テスト（種別 × 対象モジュール）の一覧と網羅状況          |
| 開発環境         | 開発環境セットアップ.md                  | ローカル開発環境の構築手順（依存ツール・初期化スクリプト）   |

## ワークフロー全体の流れ

```
[Issue]
  起票 → triage（整理・現状調査）
       → spec（要件定義）
       → ui（画面ありの場合のみ）  ※ UI ライブラリ採用なら PoC まで実施
       → arch（システム方式設計） ※ ライブラリ選定で PoC が必要なら PoC まで実施
                                  … ここまで Issue 上で確定
                                  ※ ドキュメント関連は Issue には書かない
  ↓ ユーザーが OK したら 確認:pr-plan を手動付与

[PR]
  pr-plan: Draft PR 作成 + PR 本文骨組み
         + 実装設計を分かる範囲で骨組み記述
         + 不明点は PR コメントで質問
         ↻ ユーザー回答 → 本文の実装設計を埋める → 確定したコメントは削除
  ↓
  pr-test → pr-impl → pr-impl-review → pr-doc-plan → pr-doc → pr-doc-review → pr-merge

[中断クローズ]
  reset（任意・ユーザー手動）: 不要化した Issue/PR を巻き戻してクローズ
```

- Issue は「**何を作るか**」まで。ドキュメント影響は Issue には書かない
- PR は「**どう作るか**」と「**実装結果**」「**ドキュメント更新**」を担当
- 確定したコメントは削除して履歴をクリーンに保つ

---

## 設計原則

### モニター vs カスタムサブエージェントの判断軸

**ユーザーとのやり取りが発生するなら「モニター」、発生しないなら「カスタムサブエージェント」**

| 場面                                             | 採用             | 理由                                               |
| ------------------------------------------------ | ---------------- | -------------------------------------------------- |
| ユーザーへ質問してコメント返信を待つ             | モニター         | スキルが長時間待機せず、ラベル付け替えで再開できる |
| 複数の観点・候補を並列に深堀りして結果を統合する | サブエージェント | 内部処理で完結、Agent ツールで並列起動できる       |

### 領域別の処理（フロント/バック/DB）

`issue-arch` の領域別検討は**カスタムサブエージェントで並列処理**する。
モニター数を爆発させないため、領域分割はモニターではなくサブエージェントで行う。

---

## モニター詳細

### 1. issue-triage

**モニター条件**:
- Issue に `確認:issue-triage` ラベルが付与された
- Assignee にユーザが設定されていない

**モニターの役割**:
起票直後の Issue を整える。**「分かっていることだけを整理する」**フェーズで、仕様・実装方針の決定は後の issue-spec 以降に任せる。

- 本文の整文・整形（入力の誤字脱字・改行整理・文言修正）を行う
- **後続フェーズ全てのセクション骨組み**（spec/ui/arch が後で埋めるセクション。PoC 結果は arch/ui が必要時に埋める）を本文に作っておく
- 本文に欠けているセクションがあれば、**ユーザーが書いた情報の範囲内で**テンプレートに沿って埋める
- 内容を表すタイトルに更新する
- `type:*` ラベル・優先度ラベルを付与する
- **現状調査**: 以下を実施して「現状」セクションに記録する
  - Issue が言及する領域のコードベース・既存実装・関連ファイルを Read で確認
  - 実行可能なテスト（E2E・結合・単体）があれば**実際に走らせる**
  - 報告された問題が**再現するかを確認**する
  - 再現結果（ログ・スクリーンショット・テスト出力）を本文に貼る
  - **関連 Issue / PR を検索**してリンクとして本文に貼る
    - 2 つのカスタムサブエージェント（`related-issue-finder` と `related-pr-finder`）を**並列起動**して効率化
    - 検索対象: 同領域・同キーワード・同エラーメッセージ・関連ファイル名（open/closed/merged 全部対象）
    - 過去の対応で**バグった可能性のある PR** も探す（同じファイル・同じ機能を直近で触っている merged PR）
    - 見つけた関連 Issue/PR は `## 現状` に **「関連 Issue/PR」** 小見出しでリンク列挙
    - 完全重複 Issue なら、ユーザーに通知して当 Issue をクローズする提案も出す

**フロー**:

1. Issue 本文を整形・整文する（音声入力の誤字脱字・改行整理。ユーザー入力の範囲内）
2. 後続フェーズ（spec/ui/arch）のセクション骨組みを本文に作成（`## PoC 結果` 骨組みも置く — 必要時に arch/ui が埋める）
3. 内容を表すタイトルに更新
4. `type:*` ラベル・優先度ラベルを付与
5. **現状調査（全てサブエージェント並列起動）**:
   - 5a. **領域別コードベース調査**: Issue が言及する領域ごとにサブエージェントを起動（関連カスタムサブエージェントがあれば優先、なければ汎用 Agent でOK）→ コードベース・既存実装・関連ファイルの所在と要点を返してもらう。各サブエージェントには関連 Wiki（該当領域の `クラス図_{モジュール名}` / `シーケンス図_{機能名}` / `APIエンドポイント一覧` / `ER図` / **`
`**（アプリ層 DTO・ドメインオブジェクト・型定義）など）を**注入**し、既存のデータ構造との関連も把握させる
   - 5b. **テスト再現調査**: 「E2E で試せそう」「結合で試せそう」「単体で試せそう」のテスト種別ごとにサブエージェントを起動（各サブエージェントに Wiki の `テスト戦略`・`テスト実行方法`・`テスト一覧` ページを注入）→ 該当テストを実行 → 再現結果を返してもらう
   - 5c. `related-issue-finder` と `related-pr-finder` をサブエージェントとして並列起動
6. 調査結果（再現ログ・スクリーンショット・関連 Issue/PR リンク）を本文の `## 現状` に記録
7. **分岐判定**:
   - 完全重複 Issue が見つかった → クローズ提案コメント → `assignee=ユーザー` 待機 → ユーザー合意で Issue クローズ＆終了
   - スコープが大きすぎる → 子 Issue 分割提案コメント → `assignee=ユーザー` 待機 → ユーザー合意で子 Issue 作成＆親 Issue クローズ＆終了
   - それ以外 → 次へ
8. 完了報告コメントを投稿し `assignee=ユーザー` で待機
9. **ユーザー応答ループ**:
   - ユーザーが assignee を外した（`フェーズ終了` なし）→ 最新コメントの追記内容を確認:
     - **修正指示のみ**（議論完了）→ 本文反映 → そのコメント全体を削除 → 8 に戻る
     - **質問・追加議論を含む** → 同コメントに `🤖 Generated by issue-triage` + 区切り線で返信を追記 → 必要に応じて本文も部分反映 → 8 に戻る（コメントは議論続行のため残す）
   - ユーザーが `フェーズ終了` 付与（=承認） → 次へ
10. **ラベル更新**（前提条件: 自分宛コメントが全て本文反映済み（未反映あればユーザー確認後に自分宛のみ一括 Resolve））:
    - 上記条件を満たさなければ「本文反映 → 一括 Resolve」を先に実行
    - 満たしたら `確認:issue-triage` 除去 + `フェーズ終了` 除去 + `確認:issue-spec` を付与（フロー終了）

**現状調査のユースケース例**:
- バグ報告: 実際に動かしてみたら問題が再現しない → ユーザー環境の問題（キャッシュ・古いバージョンなど）だと判明
- パフォーマンス劣化: 該当処理を実測して数値を記録 → spec フェーズで目標値設定の材料になる
- 機能追加要望: 既存機能で似たことができないか試す → 重複実装を未然に防げる
- エラー発生報告: ログを確認して発生条件を絞り込む → spec フェーズの再現手順が明確になる
- Issue のスコープが大きすぎる場合は子 Issue の分割を提案し、ユーザーの合意が得られれば親 Issue はクローズする

**担当セクション**（自身で記入）:
- `## 概要`（ユーザー入力の範囲内）
- `## 背景`（ユーザー入力の範囲内）
- `## 現状`
  - `### 関連実装コード`
  - `### 関連テスト`
  - `### 関連 Issue/PR`
  - `### 関連ドキュメント`
  - `### 既存テスト実行結果`（テスト実行可能時のみ）
  - `### 再現手順`（バグ報告の場合のみ）

**担当セクション詳細**:

| サブセクション           | 入力値                                                | 概要                                                                                         | 参照 Wiki                                                |
| ------------------------ | ----------------------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| `## 概要`                | ユーザーが起票時に書いた目的文                        | Issue が解決したい問題・実現したい状態を 1〜3 行で整形（ユーザー入力範囲内）                 | -                                                        |
| `## 背景`                | ユーザーが起票時に書いた経緯文                        | 起票に至った背景・きっかけ・問題の発生状況を整形                                             | -                                                        |
| `### 関連実装コード`     | Issue が言及する領域のコードベース調査                | **No / ファイル / メソッド / 概要 / 補足** の表                                              | クラス図_*.md / シーケンス図_*.md / データモデル一覧.md  |
| `### 関連テスト`         | 関連テストの調査                                      | **No / 分類 / ファイル / メソッド / 概要 / 補足** の表（分類は 単体/結合/E2E/外部疎通など）  | テスト一覧.md                                            |
| `### 関連 Issue/PR`      | `related-issue-finder` / `related-pr-finder` の戻り値 | **No / 番号 / 状況 / 概要 / 補足** の表（状況は open/closed/merged など、番号は Issue#xx / PR#xx） | -                                                  |
| `### 関連ドキュメント`   | Wiki インデックス・CLAUDE.md / Rules を調査           | **No / 分類 / ページ / 概要 / 補足** の表（分類は Wiki / CLAUDE.md / Rules / agents など）    | -                                                        |
| `### 既存テスト実行結果` | 関連テスト実行結果（テスト実行可能時のみ）            | **No / 分類 / ファイル / メソッド / 概要 / 結果 / 補足** の表（分類は 単体/結合/E2E/外部疎通、メソッド全実行は `-`、結果は ✅/❌） | テスト実行方法.md    |
| `### 再現手順`           | バグ報告の場合のみ・実際に再現を試した結果            | 番号付き箇条書きで再現手順 + 末尾に再現結果（ログ/スクリーンショット）。再現しなかった場合もその旨記録 | -                                                |

**骨組みだけ作るセクション**（後続が記入）:
- `## システム要件（SA）` → issue-spec
- `## UI 設計` → issue-ui
- `## PoC 結果` → issue-arch または issue-ui（ライブラリ選定で PoC 実施時のみ）
- `## システム方式設計（SS）` → issue-arch

**禁止事項**:
- モデルが持っている知識で**仕様や実装方針を推測して書き加えない**（ハルシネーション防止）
- 「こうあるべき」「こうした方がいい」は spec / arch / pr-plan で決めるので、ここでは書かない
- 調査せずに想像で書いた内容は後続フェーズのコンテキストを汚染するので絶対 NG

**ユーザーとのコメントのやり取り**:

| 起点     | 発生条件                                                  | 議論内容                              | 終了条件                                 | 備考                          |
| -------- | --------------------------------------------------------- | ------------------------------------- | ---------------------------------------- | ----------------------------- |
| AI       | Issue のスコープが大きすぎる場合                          | 子 Issue 分割提案                     | ユーザーが分割案に合意 → 分割実行        | 親 Issue は分割後にクローズ   |
| ユーザー | triage 結果（タイトル/概要/背景/現状の整理）に修正リクエスト | 該当箇所の文言・整理内容を修正        | 修正反映で完了                           | ユーザー入力範囲内の修正のみ  |

**カスタムサブエージェント**:

| エージェント         | 入力                   | 出力                                                |
| -------------------- | ---------------------- | --------------------------------------------------- |
| related-issue-finder | Issue 本文・キーワード | 関連 Issue リスト（open/closed、リンク + 一言概要） |
| related-pr-finder    | 〃                     | 関連 PR リスト（merged 含む、リンク + 一言概要）    |

**ラベル更新**（フェーズ完了時=ユーザー `フェーズ終了` 付与後）:
- Issue: 除去 `確認:issue-triage` + `フェーズ終了` / 付与 `確認:issue-spec`
- PR: なし


### 2. issue-spec

**モニター条件**:
- Issue に `確認:issue-spec` ラベルが付与された
- Assignee にユーザが設定されていない

システム要件（SA）を確定する。完了後は画面ありなら `確認:issue-ui`、画面なしなら `確認:issue-arch` を付与する。

- 機能要件・非機能要件・スコープ外を Issue 本文に整理（エラーハンドリング・バリデーションは機能要件のカテゴリに含める）
- 要件で曖昧な点があればユーザーに質問するコメントを投稿（1質問 = 1コメント）
- 完了後は画面ありなら `確認:issue-ui`、画面なしなら `確認:issue-arch` を付与

**担当セクション**:
- `## システム要件（SA）`
  - `### 機能要件`
  - `### 非機能要件`
  - `### スコープ外`

**担当セクション詳細**:

| サブセクション   | 入力値                                | 概要                                                                                                                                                       | 参照 Wiki                                       |
| ---------------- | ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| `### 機能要件`   | 概要・背景・現状・ユーザー対話        | **No / カテゴリ / 要件 / 補足** の表。カテゴリは 編集機能/閲覧機能/バリデーション/エラー表示/状態表示/**レスポンシブ対応** など。エラーハンドリング・レスポンシブ対応の有無もここに含める | APIエンドポイント一覧.md / 画面遷移図_*.md      |
| `### 非機能要件` | ユーザー要望・既存システムの SLA      | **No / カテゴリ / 要件 / 補足** の表。カテゴリは 性能/セキュリティ/運用 など。当てはまるものがある時のみ書く                                               | -                                               |
| `### スコープ外` | 機能要件・関連 Issue・ユーザー対話    | **No / 項目 / 理由 / 補足** の表。「今回はやらないこと」を明示。将来やるなら別 Issue 起票候補にリンクを貼る                                                | -                                               |

**ユーザーとのコメントのやり取り**:

| 起点     | 発生条件                                                     | 議論内容                                              | 終了条件                                              | 備考                |
| -------- | ------------------------------------------------------------ | ----------------------------------------------------- | ----------------------------------------------------- | ------------------- |
| AI       | 要件で曖昧な点がある場合                                     | 機能要件・非機能要件の確認質問（1質問1コメント）      | ユーザー回答 → 本文の `## システム要件（SA）` に反映 | 1 質問 = 1 コメント |
| ユーザー | 本文の `## システム要件（SA）` に対して追加・修正要望        | 該当要件項目の追加・修正                              | 該当箇所を更新                                        | -                   |

**カスタムサブエージェント**: なし

**フロー**:

1. 機能要件・非機能要件・スコープ外を本文 `## システム要件（SA）` に整理（issue-triage が骨組み済）
2. 曖昧な点があれば 1質問1コメントで投稿し、ユーザー回答を本文に反映
3. 完了報告コメント投稿 + `assignee=ユーザー` で待機
4. **ユーザー応答ループ**:
   - フィードバックコメント + assignee 外す → 反映して 3 に戻る
   - `フェーズ終了` ラベル付与 → 次へ
5. **ラベル更新**（前提条件: 自分宛コメントが全て本文反映済み（未反映あればユーザー確認後に自分宛のみ一括 Resolve））:
   - 上記条件を満たさなければ「本文反映 → 一括 Resolve」を先に実行
   - 満たしたら `確認:issue-spec` 除去 + `フェーズ終了` 除去 + `確認:issue-ui`（画面あり）または `確認:issue-arch`（画面なし）を付与（フロー終了）

**ラベル更新**（フェーズ完了時=ユーザー `フェーズ終了` 付与後）:
- Issue: 除去 `確認:issue-spec` + `フェーズ終了` / 付与 `確認:issue-ui`（画面あり）または `確認:issue-arch`（画面なし）
- PR: なし


### 3. issue-ui（任意）

**モニター条件**:
- Issue に `確認:issue-ui` ラベルが付与された
- Assignee にユーザが設定されていない

UI 設計を行う。**UI ライブラリ採用時に必要なら PoC まで実施（issue-arch の PoC 機能と同じ手順）**。

- 画面構成・画面遷移を提案
- 必要に応じてモック画面を作成
  - 一画面につき 1コメントで各案のモック URL を貼る
- UI ライブラリ採用検討で PoC が必要な場合は **issue-arch のフロー（PoC 要否判定カテゴリ A〜E / PoC worktree 運用ルール）を参照して同手順で実施** → 採用ライブラリを `## PoC 結果` に記録
- ユーザー確認後、SS 設計に進む

**担当セクション**:
- `## UI 設計`
  - `### 画面構成`
  - `### 画面遷移`
  - `### モック`
- `## PoC 結果`（UI ライブラリ採用時に PoC を実施した場合のみ）
  - `### 検証したライブラリ`
  - `### 動作確認結果`
  - `### 追記した Wiki`

**担当セクション詳細**:

| サブセクション | 入力値                          | 概要                                                                                                            | 参照 Wiki                |
| -------------- | ------------------------------- | --------------------------------------------------------------------------------------------------------------- | ------------------------ |
| `### 画面構成` | 機能要件・既存画面              | **No / 要素 / 種類 / 位置 / 説明 / 表示条件 / 必須 / 制限 / 初期値 / データソース / アクション / 補足** の表（要素: ボタン・入力欄・ラベル・テーブル等／種類: button/input/table 等／位置: ヘッダー/フッター/フォーム本体/サイドバー 等／**データソース: `エンティティ.フィールド` 形式（DB 論理名 or データモデル名）。例: `ユーザ.名前` / `タスク.編集日付`**／**アクション: 日本語のドメイン記述で。例: 「クリックで詳細画面へ遷移」「クリックで保存」（API パスやコードは書かない）**／**表に書き切れない複雑なロジックは `※1` `※2` … の印を該当セルに入れ、表の直下に `※1: 〜` 形式で詳細を記述**／該当しない列は `-`） | 画面遷移図_*.md / データモデル一覧.md |
| `### 画面遷移` | 機能要件・既存画面遷移          | Mermaid `flowchart LR` で図示。トリガー（ボタンクリック等）も明示                                               | 画面遷移図_*.md          |
| `### モック`   | 画面構成・画面遷移              | **No / 画面 / URL / 補足** の表（デプロイ済みモック画面の URL、画像添付ある場合は補足に記載）                   | -                        |

**ユーザーとのコメントのやり取り**:

| 起点     | 発生条件                                                 | 議論内容                          | 終了条件                                             | 備考                            |
| -------- | -------------------------------------------------------- | --------------------------------- | ---------------------------------------------------- | ------------------------------- |
| AI       | 画面構成・モック案を提示する場合                         | 画面要素・遷移・モック URL の選定 | ユーザーが構成案に合意 → 本文の `## UI 設計` に反映  | モックは別途デプロイ URL を貼る |
| ユーザー | 画面に対する追加・修正要望（要素追加・遷移変更など）     | モック更新と該当箇所の調整        | モック更新 → 本文の `## UI 設計` に反映              | -                               |

**カスタムサブエージェント**: なし

**フロー**:

1. **既存画面・関連 UI コードの調査（サブエージェント並列起動）**:
   - 既存画面・共通コンポーネント・画面遷移などフロント領域の調査が必要なら、プロジェクト配下のフロント領域カスタムサブエージェント定義があれば優先的に並列起動（なければ汎用 Agent）
   - 各サブエージェントには Wiki の `画面遷移図`・関連 `画面遷移図_{機能名}` などを**注入**
   - 各サブエージェントは担当領域だけ調査し、要点を返す
2. 画面構成・画面遷移を提案（1 の調査結果を踏まえる）
3. 必要に応じて（新規画面もしくは大きく画面要素を変える場合 等）モック画面を作成し、1画面=1コメントでモック URL を共有
4. ユーザー合意後、本文 `## UI 設計`（`### 画面構成` / `### 画面遷移` / `### モック`）に記録
5. 完了報告コメント投稿 + `assignee=ユーザー` で待機
6. **ユーザー応答ループ**:
   - フィードバックコメント + assignee 外す → モック更新・本文反映して 5 に戻る
   - `フェーズ終了` ラベル付与 → 次へ
7. **ラベル更新**（前提条件: 自分宛コメントが全て本文反映済み（未反映あればユーザー確認後に自分宛のみ一括 Resolve））:
   - 上記条件を満たさなければ「本文反映 → 一括 Resolve」を先に実行
   - 満たしたら `確認:issue-ui` 除去 + `フェーズ終了` 除去 + `確認:issue-arch` を付与（フロー終了）

**ラベル更新**（フェーズ完了時=ユーザー `フェーズ終了` 付与後）:
- Issue: 除去 `確認:issue-ui` + `フェーズ終了` / 付与 `確認:issue-arch`
- PR: なし


### 4. issue-arch

**モニター条件**:
- Issue に `確認:issue-arch` ラベルが付与された
- Assignee にユーザが設定されていない

システム方式設計（SS）を行う。コンポーネント分割・採用ライブラリ・データフローを決定する。**ライブラリ選定で必要な場合は PoC まで実施**する。

- 実装範囲を判定し、必要な領域分のサブエージェントを並列起動
- 各領域の検討結果を統合してコメントに投稿（1論点 = 1コメント）
- ライブラリ選定論点は library-finder / library-researcher を使う
- 採用候補が**未経験のライブラリ**で PoC が必要と判断したら（後述「PoC 要否判定カテゴリ」A〜E に該当）、PoC まで本フェーズ内で完結させる
- ユーザーが各論点を確認した後、ユーザー自身が `確認:pr-plan` ラベルを手動付与する（その時点で実装計画フェーズに進む）

#### PoC 要否判定カテゴリ

| カテゴリ | 該当する例 |
| -------- | ---------- |
| A. ライブラリ選定型 | 複数候補（例: Faster-Whisper vs whisper.cpp）の比較が必要 |
| B. 動作確認型 | 採用方針は決まっているが API 仕様の確認が必要（例: Stripe 定期課金フロー） |
| C. パフォーマンス検証型 | 非機能要件で性能数値目標があり計測が必要 |
| D. 統合検証型 | 既存システムへの結合が読めない（例: 認証層変更） |
| E. 手順検証型 | 本番ぶっつけが怖い（例: DB マイグレーション） |

- 該当なし → PoC スキップ、通常のライブラリ選定論点として進める
- 該当あり → 候補/対象をユーザーと合意して PoC 実行

#### PoC worktree 運用ルール（実行する場合のみ）

- 命名: `poc/{issue#}-{lib-name}`（例: `poc/123-langchain`）
- リモート push なし（ローカル限定）
- 検証中の動作確認・所感はコメントで議論（決定後にコメント全消し）
- 採用決定後: 全 PoC worktree とローカルブランチを削除
- 大規模 PoC（複数ファイル）の場合のみ pr-plan まで一時保持し、本文にその旨を注記

**担当セクション**:
- `## システム方式設計（SS）`
  - `### 採用ライブラリ`
  - `### コンポーネント分割`
  - `### データフロー`
- `## PoC 結果`（ライブラリ選定で PoC を実施した場合のみ）
  - `### 検証したライブラリ`
  - `### 動作確認結果`
  - `### 追記した Wiki`

**担当セクション詳細**:

| サブセクション           | 入力値                                                               | 概要                                                                                                                            | 参照 Wiki                               |
| ------------------------ | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| `### 採用ライブラリ`     | 本フェーズの PoC 結論・既存使用ライブラリ・library-finder の調査結果 | **No / ライブラリ / バージョン / 用途 / 補足** の表。新規採用は補足に選定理由                                                                | 外部ライブラリ一覧.md                   |
| `### コンポーネント分割` | 機能要件・領域別サブエージェントの調査結果                           | **No / 新規/変更 / レイヤー / コンポーネント / 役割 / 補足** の表（レイヤーは フロント/バック/DB、新規/変更は 新規/変更/削除）              | アーキテクチャ図.md                     |
| `### データフロー`       | コンポーネント分割・API エンドポイント                               | Mermaid `sequenceDiagram` または `flowchart` で図示                                                                                          | データフロー図_*.md                     |
| `### 検証したライブラリ` | ユーザーが採用決定したライブラリ                                     | **No / ライブラリ / バージョン / ライセンス / 用途 / 補足** の表。採用決定した 1 ライブラリのみ記載、非決定の候補はコメントで議論し決定後に削除 | 外部ライブラリ一覧.md                   |
| `### 動作確認結果`       | 採用決定ライブラリの PoC 実行結果                                    | **No / ライブラリ / 検証項目 / 結果 / 補足** の表（成功条件・所要時間・所感など）+ 表後に最小再現コード（10〜30行程度）。非決定案の検証履歴は残さない | -                          |
| `### 追記した Wiki`      | このフェーズで新規作成・追記した Wiki ページ                         | **No / ページ / 内容 / 補足** の表（reset モニターが巻き戻し時に遡って削除するための履歴）                                                  | 外部ライブラリ一覧.md / 外部ライブラリ_*.md |

**ユーザーとのコメントのやり取り**:

| 起点     | 発生条件                                                         | 議論内容                          | 終了条件                                                          | 備考                                                                                       |
| -------- | ---------------------------------------------------------------- | --------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| AI       | ライブラリ選定論点が見つかった場合                               | 候補ライブラリの比較と推奨        | ユーザーが採用候補を選択 → 本文の `### 採用ライブラリ` に反映     | library-finder / library-researcher の結果を整形                                           |
| AI       | 候補ライブラリの動作検証結果を共有する場合（PoC 実施時）         | 候補ごとの動作結果・所感を共有し採用判断を仰ぐ | ユーザーが採用ライブラリを決定 → 本文の `## PoC 結果` に反映      | 候補ごとに 1 コメント                                                                      |
| AI       | 設計論点（コンポーネント分割・データフローなど）が見つかった場合 | 複数案比較 + 推奨                    | ユーザーが案を選択 → 本文の `## システム方式設計（SS）` に反映    | design-points-finder / design-reviewer の結果を整形（テンプレート_設計レビュー論点.md）    |
| ユーザー | 別の案・観点の追加要望                                           | 該当案を追加検討                  | 追加検討結果 → 本文の `## システム方式設計（SS）` に反映          | -                                                                                          |

**カスタムサブエージェント**:

| エージェント | 入力 | 出力 |
| ------------ | ---- | ---- |
| design-points-finder | Issue + 関連コード + 領域別アーキ調査結果 | **ライブラリ以外**の設計判断ポイントを列挙（例: キャッシュ戦略・エラー処理方針・スキーマ分割・データフロー設計）。タイトルだけ、深掘りはしない |
| design-reviewer | 1 設計論点 + 関連コード | 複数案比較 + 推奨（`テンプレート_設計レビュー論点.md` 形式） |
| library-finder | 処理目的 + 既存スタック | ライブラリ候補3〜5個 |
| library-researcher | 1ライブラリ | 観点別スコア + コード例 |

**使い分け**:
- **library-***：ライブラリ採用判断（候補列挙 → 各候補深掘り → 必要なら PoC で実コード検証）
- **design-***：ライブラリに関係しない設計判断（キャッシュ戦略・エラー処理方針など）
- 両者は観点が独立しており重複しない。論点提示時は 1 論点 = 1 コメントで並列に出す

**フロー**:

1. **領域別アーキ調査（サブエージェント並列起動）**:
   - 実装範囲を判定し、必要な領域分のサブエージェント（フロント/バック/DB など）を並列起動
   - **プロジェクト配下の領域別カスタムサブエージェント定義があれば優先利用**
   - 各サブエージェントには関連 Wiki（`アーキテクチャ図`・`ER図`・`APIエンドポイント一覧`・該当領域の `クラス図_{モジュール名}` / `シーケンス図_{機能名}` など）を**注入**
   - 各サブエージェントは担当領域だけ調査・設計案を返す
2. **論点抽出（2系統を並列起動）**:
   - 2a. **設計論点**（ライブラリ以外）: `design-points-finder` を起動 → 論点リスト（例: キャッシュ戦略・エラー処理方針・スキーマ分割など）を取得
   - 2b. **ライブラリ選定論点**: `library-finder` を起動 → 候補ライブラリリスト（3〜5 個）を取得
3. **論点ごとに深掘り（並列起動）**:
   - 3a. 設計論点ごとに `design-reviewer` を並列起動 → 複数案比較 + 推奨を取得（`テンプレート_設計レビュー論点.md` 形式）
   - 3b. ライブラリ候補ごとに `library-researcher` を並列起動 → 観点別スコア + コード例を取得
   - プロジェクト配下のカスタムサブエージェント定義があれば優先利用
4. **PoC 要否判定（ライブラリ系のみ対象）**: 採用候補が未経験で PoC が必要か判定（前述「PoC 要否判定カテゴリ」A〜E に該当するか）
   - **不要** → 5 に進む
   - **必要** → 以下の PoC サブステップを実施:
     - 4a. 候補ライブラリ・検証観点をコメントで提示しユーザー合意
     - 4b. 候補ライブラリごとに PoC 専用 worktree（`poc/{issue#}-{lib-name}`、リモート push なし）を作成
     - 4c. サブエージェント並列起動で各候補を独立検証（Wiki `外部ライブラリ一覧` を注入。担当 worktree で最小 PoC コードを書いて動作確認）
     - 4d. 各候補の動作結果・所感をコメントで投稿（議論用、決定後に削除）し採用判断を仰ぐ
     - 4e. ユーザー採用決定 → 採用案を本文 `## PoC 結果`（`### 検証したライブラリ` / `### 動作確認結果`）に記録
     - 4f. **Wiki 反映**: `外部ライブラリ一覧.md` に行追加・`外部ライブラリ_{lib名}.md` を新規作成または更新（書き方規約は Wiki `gh-kit_規約_外部ライブラリ.md` 参照: 概要 / 現在のバージョン情報 / インストール / 使用するメソッドとパラメータ）→ 追記/新規作成した URL を `### 追記した Wiki` に記録
     - 4g. PoC worktree とローカルブランチを**全て削除**（大規模 PoC で pr-plan に引き継ぐ場合のみ採用案の worktree を保持し、本文に注記）
5. 設計論点・ライブラリ論点を **1論点 = 1コメント** で並列に投稿、ユーザー選択を本文 `## システム方式設計（SS）`（`### 採用ライブラリ` / `### コンポーネント分割` / `### データフロー`）に反映
6. 完了報告コメント投稿 + `assignee=ユーザー` で待機
7. **ユーザー応答ループ**:
   - フィードバックコメント + assignee 外す → 反映して 6 に戻る
   - `フェーズ終了` ラベル付与 → 次へ
8. **ラベル更新**（前提条件: 自分宛コメントが全て本文反映済み（未反映あればユーザー確認後に自分宛のみ一括 Resolve）・PoC 実施時は非決定案の worktree が全て削除済み）:
   - 上記条件を満たさなければ「本文反映 → 一括 Resolve → worktree 削除」を先に実行
   - 満たしたら `確認:issue-arch` 除去 + `フェーズ終了` 除去（次ラベルは付与しない — **ユーザー手動で `確認:pr-plan` を付与**）（フロー終了）

**ラベル更新**（フェーズ完了時=ユーザー `フェーズ終了` 付与後）:
- Issue: 除去 `確認:issue-arch` + `フェーズ終了` / 付与 なし（ユーザー手動で `確認:pr-plan` を付与）
- PR: なし


### 5. pr-plan

**モニター条件**:
- Issue に `確認:pr-plan` ラベルが付与された
- Assignee にユーザが設定されていない

Draft PR を作成し、実装計画（コード変更一覧）とテスト計画を立てる。

- worktree を作成し、PR 本文テンプレートに沿った空コミットを push
- `gh pr create --draft` で Draft PR を作成
- **PR 本文の後続フェーズ（pr-test/pr-impl/pr-doc-plan/pr-doc）のセクション骨組みを作っておく**（pr-impl-review/pr-doc-review は本文書き込みなし）
- Issue の SS で決まった各コンポーネントについて、`## 実装計画` 表に**分かる範囲で骨組み**として行を書く（クラス・メソッド・型・DB カラムを 1 表で管理）
- 不明点は PR コメントでユーザーに質問し、やり取りしながら少しずつ埋めていく
- テスト計画は、実装計画の各行をどこでカバーするかも明示する（すべてのコード変更がテストされるようにする）

**担当セクション（PR 本文）**:
- `## 紐づく Issue`
- `## 実装計画`（コード変更一覧 + 完了状態を 1 表にまとめる。クラス・メソッド・型・DB カラムなどを全て分類列で区別）
- `## テスト計画`
  - `### 単体テスト`
  - `### 結合テスト`
  - `### E2Eテスト`
  - `### 外部疎通テスト`（任意）

**担当セクション詳細**:

| サブセクション                          | 入力値                                                                       | 概要                                                                                                                  | 参照 Wiki                                       |
| --------------------------------------- | ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| `## 実装計画`                           | issue-arch のコンポーネント分割・データフロー・既存クラス・サブエージェント調査 | **No / 完了 / 新規/変更 / レイヤー / 分類 / ファイル / 対象 / 概要 / 補足** の表。コード・型・DB カラム・マイグレーションなど全てを 1 表にまとめる。分類は クラス/メソッド/関数/コンポーネント/フック/型/DBカラム/マイグレーション/エンドポイント など。対象は クラス名・メソッド名・型名・カラム名などシンボル名。概要は「何を受け取って何を返すか」「どんな変更か」を 1〜2 文。完了は ⬜/✅ で pr-impl が更新 | クラス図_*.md / 命名規則.md / データモデル一覧.md / ER図.md |
| `## テスト計画` > `### 単体テスト`      | 実装計画                                                                     | 単体テストの追加/変更/既存実行を **チェックボックス付き** で列挙                                                      | テスト戦略.md / テスト一覧.md |
| `## テスト計画` > `### 結合テスト`      | コンポーネント分割・データフロー                                             | 結合テストの追加/変更/既存実行をチェックボックス付きで列挙                                                            | テスト戦略.md / テスト一覧.md / シーケンス図_*.md |
| `## テスト計画` > `### E2Eテスト`       | 機能要件・画面遷移                                                           | E2E テストの追加/変更/既存実行をチェックボックス付きで列挙                                                            | テスト戦略.md / テスト一覧.md / 画面遷移図_*.md / APIエンドポイント一覧.md |
| `## テスト計画` > `### 外部疎通テスト` | 起動環境系の最低限動作確認                                                   | 外部疎通テストの追加/変更/既存実行をチェックボックス付きで列挙（任意）                                                | テスト戦略.md / テスト実行方法.md / 開発環境セットアップ.md |

**ユーザーとのコメントのやり取り**:

| 起点     | 発生条件                                                  | 議論内容                                   | 終了条件                                                        | 備考                              |
| -------- | --------------------------------------------------------- | ------------------------------------------ | --------------------------------------------------------------- | --------------------------------- |
| AI       | 実装計画で不明点がある場合                                | クラス・メソッド・型・DB カラムなどの確認質問 | ユーザー回答 → 本文の `## 実装計画` に反映                      | 1 質問 = 1 コメント               |
| AI       | 実装タスクの粒度・順序を相談する場合                      | タスク分解の妥当性                         | ユーザーが計画に合意 → 本文の `## 実装計画` に反映              | -                                 |
| AI       | テスト計画で観点の選別が必要な場合                        | テスト観点の複数案提示                        | ユーザーが観点を選択 → 本文の `## テスト計画` に反映            | 単体/結合/E2E ごとに別コメント    |
| ユーザー | 実装計画・テスト計画への修正要望                          | 該当箇所の修正                             | 該当箇所を更新                                                  | -                                 |

**カスタムサブエージェント**: なし

**フロー**:

1. worktree を作成し、PR 本文テンプレートに沿った空コミットを push → `gh pr create --draft` で Draft PR 作成
2. PR 本文の後続フェーズ全て（pr-test / pr-impl / pr-doc-plan / pr-doc）のセクション骨組みを作成
3. **実装計画のためのコードベース調査（サブエージェント並列起動）**:
   - 実装計画（コード変更一覧）を埋めるため、関連コードベース・既存実装の調査が必要なら、プロジェクト配下の領域別カスタムサブエージェント定義があれば優先的に並列起動（なければ汎用 Agent）
   - 各サブエージェントには関連 Wiki（該当領域の `クラス図_{モジュール名}` / `シーケンス図_{機能名}` / `APIエンドポイント一覧` / `ER図` / `データモデル一覧` など）を**注入**
   - 各サブエージェントは担当領域だけ調査し、既存シグネチャ・データモデル・呼び出し関係を返す
4. Issue の SS + 3 の調査結果から、本文 `## 実装計画` 表に **分かる範囲で骨組み行を記述**（クラス・メソッド・型・DB カラム・マイグレーションなどを 1 表に集約）
5. 不明点があれば 1質問1コメントで PR に投稿
6. **実装計画レビュー（ユーザー確認）**:
   - 完了報告コメント投稿 + `assignee=ユーザー` で待機
   - フィードバックコメント + assignee 外す → 該当箇所を更新 → 6 を繰り返し
   - **実装計画に対して `フェーズ終了` ではなく中間合意コメント**（例: 「実装計画 OK、テスト計画に進んで」）を受領 → 次へ
7. **テスト計画作成（テスト種別ごとにサブエージェント並列起動）**:
   - **単体テスト**: 1 サブエージェント起動 → Wiki `テスト戦略`・`テスト実行方法`・`テスト一覧` を注入 → 単体テストの新規/変更/既存実行を列挙
   - **結合テスト**: 1 サブエージェント起動 → 同様の Wiki + `シーケンス図` を注入 → 結合テストの新規/変更/既存実行を列挙
   - **E2E テスト**: 1 サブエージェント起動 → 同様の Wiki + `画面遷移図`・`APIエンドポイント一覧` を注入 → E2E テストの新規/変更/既存実行を列挙
   - **外部疎通テスト**（任意）: 起動環境系の最低限の確認テスト → サブエージェント起動 → Wiki `開発環境セットアップ`・`テスト実行方法` を注入 → 外部疎通テストの新規/変更/既存実行を列挙
   - プロジェクト配下のテスト系カスタムサブエージェント定義があれば優先利用
   - 各サブエージェントの戻り値を本文 `## テスト計画` の対応サブセクション（`### 単体テスト` / `### 結合テスト` / `### E2Eテスト` / `### 外部疎通テスト`）に統合
8. **テスト計画レビュー（ユーザー確認）**:
   - 完了報告コメント投稿 + `assignee=ユーザー` で待機
9. **ユーザー応答ループ**:
    - フィードバックコメント + assignee 外す → 本文の `## 実装計画` / `## テスト計画` を更新 → 8 に戻る
    - `フェーズ終了` ラベル付与 → 次へ
10. **ラベル更新**（前提条件: 自分宛コメントが全て本文反映済み（未反映あればユーザー確認後に自分宛のみ一括 Resolve））:
    - 上記条件を満たさなければ「本文反映 → 一括 Resolve」を先に実行
    - 満たしたら Issue から `確認:pr-plan` + `フェーズ終了` 除去 / PR に `確認:pr-test` を付与（フロー終了）

**ラベル更新**（フェーズ完了時=ユーザー `フェーズ終了` 付与後）:
- Issue: 除去 `確認:pr-plan` + `フェーズ終了` / 付与 なし
- PR: 除去 なし / 付与 `確認:pr-test`


### 6. pr-test

**モニター条件**:
- PR に `確認:pr-test` ラベルが付与された
- Assignee にユーザが設定されていない

選択されたテスト観点でテストコードを作成する（実装はまだ）。

- 既存テストの規約に沿ってテストコードを書く（Red 状態で push）
- E2E / 結合 / 単体 を必要なレイヤーで配置
- ユーザーが「重複してる」「他の観点も追加して」とフィードバックしたら反映

**担当セクション（PR 本文）**:
- `## テスト計画`（pr-plan が骨組み済みの各サブセクションを更新）

**担当セクション詳細**:

| サブセクション                                            | 入力値                       | 概要                                                                                                       | 参照 Wiki                              |
| --------------------------------------------------------- | ---------------------------- | ---------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| `## テスト計画`（pr-plan が骨組み済の各サブセクション）   | pr-plan で立てた計画         | 計画通りにテストコードを Red 状態で作成し、各チェックボックスの行にテストファイル名を確定記入              | テスト実行方法.md / テスト戦略.md      |

**ユーザーとのコメントのやり取り**:

| 起点     | 発生条件                                                                             | 議論内容                                | 終了条件                                                   | 備考 |
| -------- | ------------------------------------------------------------------------------------ | --------------------------------------- | ---------------------------------------------------------- | ---- |
| AI       | 追加観点を提案する場合                                                               | 既存テストとの差分を提示し追加観点を提案 | ユーザー合意 → テスト追加・本文の `## テスト計画` を更新   | -    |
| ユーザー | ユーザーから「テストが重複してる」「他の観点も追加して」のフィードバックがあった場合 | テストの追加・削除・差し替え            | ユーザーがテスト構成に合意 → 本文の `## テスト計画` を更新 | -    |

**カスタムサブエージェント**: なし

**フロー**:

1. PR 本文 `## テスト計画`（pr-plan が作成済み）の各サブセクション（`### 単体テスト` / `### 結合テスト` / `### E2Eテスト` / `### 外部疎通テスト`）を読み込む
2. 計画通りにテストコードを Red 状態で作成（既存テストの規約に沿う）
3. テスト失敗が想定通り（Red）であることを確認
4. 本文の各テスト行にテストファイル名を確定記入（チェックボックスはまだ付けない、Green は pr-impl で確認するため）
5. 完了報告コメント投稿 + `assignee=ユーザー` で待機
6. **ユーザー応答ループ**（テスト実装に対するフィードバック）:
   - フィードバックコメント + assignee 外す → テスト追加/削除/差し替え + 本文反映 → 5 に戻る
   - 計画自体の見直しが必要な場合はラベルを `確認:pr-plan` に戻して終了
   - `フェーズ終了` ラベル付与 → 次へ
7. **ラベル更新**（前提条件: 自分宛コメントが全て本文反映済み（未反映あればユーザー確認後に自分宛のみ一括 Resolve））:
   - 上記条件を満たさなければ「本文反映 → 一括 Resolve」を先に実行
   - 満たしたら PR から `確認:pr-test` + `フェーズ終了` 除去 / PR に `確認:pr-impl` を付与（フロー終了）

**ラベル更新**（フェーズ完了時=ユーザー `フェーズ終了` 付与後）:
- Issue: なし
- PR: 除去 `確認:pr-test` + `フェーズ終了` / 付与 `確認:pr-impl`


### 7. pr-impl

**モニター条件**:
- PR に `確認:pr-impl` ラベルが付与された
- Assignee にユーザが設定されていない

実装する（TDD）。**ユーザーとのやり取りはなし**。計画通りに実装してテストが Green になったら自動で次のレビューフェーズへ進める。

- worktree に復帰し、fetch/reset で最新化
- pr-plan の実装計画通りに実装
- テスト走らせて Green を確認
- `gh pr ready` で Draft を解除 → 自動で `確認:pr-impl-review` に進む

**担当セクション（PR 本文）**:
- `## 実装計画` のチェックボックスを完了したタスクから順にチェック
- `## テスト計画` の各テスト一覧のチェックボックスを Green になったものから順にチェック

**担当セクション詳細**:

| サブセクション                              | 入力値                       | 概要                                                                                                          | 参照 Wiki |
| ------------------------------------------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------- | --------- |
| `## 実装計画`（チェックボックス更新）       | pr-plan の実装計画           | 完了したタスクから順にチェックを入れる（本文の追記はせず、既存項目のチェック更新のみ）                        | -         |
| `## テスト計画`（チェックボックス更新）     | pr-test の追加テスト         | Green になったテストから順にチェックを入れる                                                                  | -         |

**ユーザーとのコメントのやり取り**: なし（実装に専念。設計レベルで困った場合のみラベルを `確認:pr-plan` に戻して引き継ぎ）

**カスタムサブエージェント**: なし

**フロー**:

1. worktree に復帰し、fetch/reset で最新化
2. **周辺コード調査が必要なケース（サブエージェント並列起動）**:
   - 実装中に周辺コード・既存実装の調査が必要になった場合、プロジェクト配下の領域別カスタムサブエージェント定義があれば優先的に並列起動（なければ汎用 Agent）
   - 各サブエージェントには関連 Wiki（該当領域の `クラス図_{モジュール名}` / `シーケンス図_{機能名}` / `APIエンドポイント一覧` / `エラーコード・例外定義一覧` / `データモデル一覧` など）を**注入**
   - 各サブエージェントは担当領域だけ調査し、要点を返す
3. 実装計画を順に消化（タスク完了ごとに本文 `## 実装計画` のチェックボックスをチェック）
4. テスト実行 → Green を確認、本文 `## テスト計画` の各テスト一覧のチェックボックスをチェック
5. `gh pr ready` で Draft 解除
6. **判定**:
   - **全タスク完了 + 全テスト Green** → 7 へ
   - **設計レベルの判断に迷う**（メソッドシグネチャ変更などが必要） → ラベルを `確認:pr-plan` に戻して終了（pr-plan に引き継ぎ）
   - **テスト失敗が解消できない** → ラベルを `確認:pr-plan` に戻して終了（テスト計画/実装計画の見直しを依頼）
7. **ラベル更新**（前提条件: 全タスク・全テストのチェックボックスが揃っている）:
   - PR から `確認:pr-impl` を除去 / PR に `確認:pr-impl-review` を付与（フロー終了、**`フェーズ終了` ラベル不要・自動遷移**）

**ラベル更新**（実装完了時、ユーザー承認不要）:
- Issue: なし
- PR: 除去 `確認:pr-impl` / 付与 `確認:pr-impl-review`


### 8. pr-impl-review

**モニター条件**:
- PR に `確認:pr-impl-review` ラベルが付与された
- Assignee にユーザが設定されていない

実装コードの品質をレビューする。**最初は AI 同士（pr-impl-review と pr-impl）で指摘→修正のラリーを回し、出尽くしたら最後にユーザーに質問する**。

- バグ・可読性・保守性の観点で diff をレビュー（動作確認はテストで担保するためパフォーマンスチェックは行わない）
- 指摘があれば `確認:pr-impl` に差し戻し → pr-impl が修正 → 再び `確認:pr-impl-review` に戻ってくる（**AI 間ループ**）
- 指摘が出尽くしたら最後に **質問点をまとめてユーザーに投げる**（`assignee=ユーザー`）

**担当セクション（PR 本文）**:
- なし（レビューはコメント中心、承認状況は GitHub の Approval 機能で見える）

**担当セクション詳細**: なし

**ユーザーとのコメントのやり取り**:

| 起点     | 発生条件                                                  | 議論内容                                                          | 終了条件                                          | 備考                                                                                       |
| -------- | --------------------------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| AI       | AI 間ループで結論が出ない箇所がある（設計判断要・代替案複数 など） | 質問点をまとめてユーザーに投げる                                  | ユーザー回答 → 反映 → AI 間ループに戻る           | **AI 間ループが先・ユーザー対話は最後**                                                    |
| AI       | 全レビュー指摘解消後の最終承認依頼                        | （議論なし、GitHub Approval のみ）                                | Approval → `フェーズ終了` 付与 → 次フェーズへ     | GitHub Approval のみ                                                                       |
| ユーザー | AI 指摘への反論・根拠説明                                 | 指摘の妥当性議論                                                  | AI 合意なら指摘取り下げ                           | -                                                                                          |
| ユーザー | AI が見落とした観点の追加指摘                             | 追加指摘箇所の修正                                                | ラベルを `確認:pr-impl` に戻して修正依頼          | -                                                                                          |

**カスタムサブエージェント**: なし

**フロー**:

1. **レビュー観点ごとの周辺コード・規約調査（サブエージェント並列起動）**:
   - diff の周辺コード・既存規約・命名規則の調査が必要なら、プロジェクト配下の領域別カスタムサブエージェント定義があれば優先的に並列起動（なければ汎用 Agent）
   - 各サブエージェントには **Issue 本文 + PR 本文** + 関連 Wiki（`命名規則`・該当領域の `クラス図_{モジュール名}` / `シーケンス図_{機能名}` / `エラーコード・例外定義一覧` / `データモデル一覧` など）を**注入**（Issue で決まった要件・設計意図を踏まえてレビューさせるため）
   - 各サブエージェントは担当領域だけ調査し、既存規約との整合性・類似実装との差分・要件との乖離を返す
2. diff をバグ・可読性・保守性の観点でレビュー（パフォーマンスチェックは行わない、1 の調査結果を踏まえる）
3. **指摘振り分け（AI 間ループ vs ユーザー質問）**:
   - **AI で判断可能な指摘**（規約違反・明確なバグ・既存パターンとの乖離 など）→ インラインコメント投稿 → ラベル `確認:pr-impl` に戻して再実装依頼 → pr-impl 完了で `確認:pr-impl-review` に戻ってきたら 1 に戻る（**AI 間ループ**）
   - **判断に迷う指摘**（複数の妥当な案があり設計判断要 など）→ 質問点として一時保留
4. **AI 間ループ収束判定**:
   - 全指摘が解消 → 5 へ
   - まだ指摘ある → 3 のループ継続
5. **ユーザー質問フェーズ**（AI 間で結論が出なかった質問点がある場合のみ）:
   - 保留していた質問点をまとめて投稿 → `assignee=ユーザー` で待機
   - ユーザー応答ループ:
     - フィードバックコメント + assignee 外す → 反映して 1 に戻る（再レビュー）
     - `フェーズ終了` 付与 → 次へ
6. **質問なし or ユーザー承認済み**: そのまま次へ
7. **ラベル更新**（前提条件: 自分宛コメントが全て本文反映済み（未反映あればユーザー確認後に自分宛のみ一括 Resolve））:
   - 上記条件を満たさなければ「本文反映 → 一括 Resolve」を先に実行
   - 満たしたら PR から `確認:pr-impl-review` + `フェーズ終了` 除去 / PR に `確認:pr-doc-plan` を付与（フロー終了）

**ラベル更新**（フェーズ完了時=ユーザー `フェーズ終了` 付与後 or 質問なしで AI 間ループ完了後）:
- Issue: なし
- PR: 除去 `確認:pr-impl-review` + `フェーズ終了` / 付与 `確認:pr-doc-plan`


### 9. pr-doc-plan

**モニター条件**:
- PR に `確認:pr-doc-plan` ラベルが付与された
- Assignee にユーザが設定されていない

実装結果を踏まえ、ドキュメント修正の詳細計画を 2 段構えのサブエージェントで立てる。
**さらに AI 改善計画**（これまでの Resolve 済みコメントから「コンテキスト不足が原因の指摘」を抽出してドキュメント改善計画に反映）も同時に行う。

- 1段目: `doc-finder` を 1 体起動 → Issue 本文 + PR 本文 + **Issue/PR の Resolve 済みコメント全件** を注入 → 修正対象ドキュメントの一覧を返す
  - 修正対象には「実装結果に直接由来するもの」と「AI 改善由来（レビュー指摘の原因が情報不足）」の両方が含まれる
- 2段目: 1段目の結果のドキュメントごとに `doc-page-planner` を並列起動 → Issue 本文 + PR 本文 + 該当ドキュメント本体 を注入 → そのページの記載ルールを守りつつ「どのセクションに何を追加/変更/新規作成するか」を返す
- 親（pr-doc-plan）は全結果を統合して PR 本文 `## ドキュメント変更計画` に反映
- AI 改善由来の項目もユーザー対話で取捨選択。ユーザーが採用したものだけ最終的に表に残す（不採用はコメントで議論しつつ本文には書かない）
- 影響リストが空（採用された項目が 0）なら `確認:pr-merge` に付け替えて pr-doc/pr-doc-review をスキップ
- 影響ありなら計画を本文に書き、ユーザーと合意したうえで `確認:pr-doc` に付け替える

**ドキュメント一覧の置き場所**:
- rules の一覧 / Wiki ページの一覧は **Wiki 側**に配置
- `doc-finder` が Wiki からインデックスを参照して候補を絞る

**担当セクション（PR 本文）**:
- `## ドキュメント変更計画`（ページ × セクション × 変更内容 × 補足 × 完了 の表。同じページに複数変更がある場合は行を追加）

**担当セクション詳細**:

| サブセクション           | 入力値                                                                            | 概要                                                                                                                                                                          | 参照 Wiki                              |
| ------------------------ | --------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| `## ドキュメント変更計画` | 実装内容・`doc-finder` の戻り値・`doc-page-planner` の戻り値                      | **ページ / セクション / 変更内容 / 補足 / 完了** の 5 列表で記載。同じページに変更が複数あれば行を追加して独立化。pr-doc が変更完了するごとに「完了」列のチェックボックスを順次チェック | （`doc-finder` が Wiki インデックス参照） |

**ユーザーとのコメントのやり取り**:

| 起点     | 発生条件                                                  | 議論内容                                       | 終了条件                                                       | 備考                                                  |
| -------- | --------------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------------------- | ----------------------------------------------------- |
| AI       | 修正計画の確認をユーザーに依頼する場合                    | ページ / セクション / 変更内容 / 補足 の妥当性 | ユーザーが計画に合意 → 本文の `## ドキュメント変更計画` に反映 | `doc-finder` → `doc-page-planner` 2段サブエージェント並列の結果を統合 |
| ユーザー | 「ここは不要」「このページも追加して」フィードバック      | 計画の追加・削除・変更                         | 計画を更新 → 本文の `## ドキュメント変更計画` に反映           | -                                                     |

**カスタムサブエージェント**:

| エージェント       | 入力                                          | 出力                                                                                       |
| ------------------ | --------------------------------------------- | ------------------------------------------------------------------------------------------ |
| doc-finder         | Issue 本文 + PR 本文 + Issue/PR の Resolve 済みコメント全件 + Wiki インデックス | 修正対象ドキュメント一覧（Wiki ページ / CLAUDE.md / Rules / `agents/*.md`）。実装直接由来・AI 改善由来の両方を含む |
| doc-page-planner   | Issue 本文 + PR 本文 + 該当ドキュメント本体   | そのページの記載ルールに準拠した「どのセクションに何を追加/変更/新規作成するか」の詳細計画 |

**使い分け**:
- **doc-finder**: 修正対象を**列挙**（1 体起動、まずは候補出し）
- **doc-page-planner**: 各ページについて**深掘り**（ドキュメント数だけ並列起動、ページごとの記載ルールを守る）
- 2 段構えにする理由: ドキュメントごとに記載ルール（テンプレート構造・記法・順序など）が異なるため、1 体に全部任せると個別ルールを守れない

**フロー**:

1. **doc-finder を 1 体起動**:
   - Issue 本文 + PR 本文 + **Issue/PR の Resolve 済みコメント全件**（AI 改善計画の素材）+ Wiki のドキュメントインデックスを注入
   - 修正対象ドキュメントの一覧（ファイルパス + 修正理由の概要）を返してもらう
   - 修正理由には「実装結果に直接由来」と「AI 改善由来（レビューコメントから抽出した情報不足の補強）」の両方を含める
2. **doc-page-planner を該当ドキュメント数だけ並列起動**:
   - 各サブエージェントに Issue 本文 + PR 本文 + 該当ドキュメント本体 を注入
   - そのページの記載ルールを守りつつ「どのセクションに何を追加/変更/新規作成するか」の詳細計画を返してもらう
   - プロジェクト配下のページ別カスタムサブエージェント定義があれば優先利用
3. **プロジェクト配下のカスタムサブエージェント定義（`agents/*.md`）の保守判定**:
   - 実装で「新規ファイル/ディレクトリが増えた」「既存ファイルが削除/移動された」「主要モジュールのインターフェースが変わった」場合、それを参照しているカスタムサブエージェント定義（特に "ファイル" 表・参照パス一覧など）も古い情報を指したままになる
   - 該当する `agents/*.md` を洗い出し、更新が必要なものを **`## ドキュメント変更計画` の表に行追加**（Wiki ページや CLAUDE.md と同列で計画に乗せ、2 の doc-page-planner で詳細化）
4. 本文 `## ドキュメント変更計画` に **ページ / セクション / 変更内容 / 補足 / 完了** の 5 列表で記入（同ページに複数変更あれば行を追加）
5. 完了報告コメント投稿 + `assignee=ユーザー` で待機
6. **ユーザー応答ループ**:
   - フィードバックコメント + assignee 外す → 反映して 5 に戻る
   - `フェーズ終了` ラベル付与 → 次へ
7. **分岐**（いずれも前提条件: 自分宛コメントが全て本文反映済み（未反映あればユーザー確認後に自分宛のみ一括 Resolve）。満たさなければ「本文反映 → 一括 Resolve」を先に実行）:
   - 影響あり（計画あり）→ **ラベル更新**: PR から `確認:pr-doc-plan` + `フェーズ終了` 除去 / PR に `確認:pr-doc` を付与（フロー終了）
   - 影響なし（計画が空）→ **ラベル更新**: PR から `確認:pr-doc-plan` + `フェーズ終了` 除去 / PR に `確認:pr-merge` を付与（pr-doc / pr-doc-review をスキップしてフロー終了）

**ラベル更新**（フェーズ完了時=ユーザー `フェーズ終了` 付与後）:
- Issue: なし
- PR: 除去 `確認:pr-doc-plan` + `フェーズ終了` / 付与 `確認:pr-doc`（影響あり）または `確認:pr-merge`（影響なし）


### 10. pr-doc

**モニター条件**:
- PR に `確認:pr-doc` ラベルが付与された
- Assignee にユーザが設定されていない

ドキュメント変更計画に沿って、Wiki / CLAUDE.md / Rules を実際に修正する。

- **修正対象ページごとに `doc-page-editor` サブエージェントを並列起動**
- 各サブエージェントには「Issue 本文 + PR 本文 + 該当ドキュメント本体 + pr-doc-plan が立てた該当ページの修正計画」を注入
- 各サブエージェントは自分の担当ページだけ編集してコミット（ページの記載ルールに準拠）
- 新規ページ追加時は、対応するインデックスページ（`外部ライブラリ一覧.md` など）も該当サブエージェントが自身で更新
- 親（pr-doc）は各サブエージェントの完了を待って push まで担当
- Wiki ページは Wiki リポジトリに push（必要なら新規ページ作成）

**担当セクション（PR 本文）**:
- `## ドキュメント変更計画` 表の「完了」列のチェックボックスを更新完了した変更から順にチェック

**担当セクション詳細**:

| サブセクション                                  | 入力値                | 概要                                                                                       | 参照 Wiki |
| ----------------------------------------------- | --------------------- | ------------------------------------------------------------------------------------------ | --------- |
| `## ドキュメント変更計画`（「完了」列のチェックボックス更新） | pr-doc-plan の計画    | 更新完了した変更行から順に「完了」列のチェックボックスを更新   | -         |

**ユーザーとのコメントのやり取り**: なし（修正に専念。計画外の問題が出た場合のみラベルを `確認:pr-doc-plan` に戻して引き継ぎ）

**カスタムサブエージェント**:

| エージェント     | 入力                                                                                              | 出力                                                       |
| ---------------- | ------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| doc-page-editor  | Issue 本文 + PR 本文 + 該当ドキュメント本体 + pr-doc-plan が立てた該当ページの修正計画            | 該当ページの修正コミット（ページ記載ルールに準拠した編集） |

プロジェクト配下のページ別カスタムサブエージェント定義があれば優先利用。

**フロー**:

1. **修正対象ページごとに `doc-page-editor` を並列起動**
   - 各サブエージェントに「Issue 本文 + PR 本文 + 該当ドキュメント本体 + 該当ページの修正計画」を注入
   - 各サブエージェントは自分の担当ページだけ編集してコミット（ページ記載ルールに準拠）
2. 新規ページ追加時は、対応するインデックスページも該当 `doc-page-editor` が更新（例: 新規 `外部ライブラリ_xxx.md` 追加なら `外部ライブラリ一覧.md` にも行追加）
3. **プロジェクト配下のカスタムサブエージェント定義（`agents/*.md`）の更新**:
   - pr-doc-plan で `## ドキュメント変更計画` 表に含めた `agents/*.md` を計画に沿って更新（参照ファイル一覧・"ファイル" 表・参照パスなど）
   - 計画外でも、コミット中に「このサブエージェントの参照は古い」と気づいたら追加修正対象として取り込む（その場合は pr-doc-plan に戻すか判断）
4. 親（pr-doc）は各 `doc-page-editor` の完了を待って push（Wiki ページは Wiki リポジトリに push）
5. 本文 `## ドキュメント変更計画` 表の「完了」列のチェックボックスを更新完了した変更から順にチェック
6. **判定**:
   - 全変更（「完了」列が全て ✅）→ 7 へ
   - 計画外の問題が出た → ラベルを `確認:pr-doc-plan` に戻して終了（pr-doc-plan に引き継ぎ）
7. **ラベル更新**（前提条件: 全変更のチェックボックスが ✅）:
   - PR から `確認:pr-doc` を除去 / PR に `確認:pr-doc-review` を付与（フロー終了、**`フェーズ終了` ラベル不要・自動遷移**）

**ラベル更新**（修正完了時、ユーザー承認不要）:
- Issue: なし
- PR: 除去 `確認:pr-doc` / 付与 `確認:pr-doc-review`


### 11. pr-doc-review

**モニター条件**:
- PR に `確認:pr-doc-review` ラベルが付与された
- Assignee にユーザが設定されていない

ドキュメント差分をレビューする。**最初は AI 同士（pr-doc-review と pr-doc）で指摘→修正のラリーを回し、出尽くしたら最後にユーザーに質問する**。

- 計画整合性・既存ドキュメント整合性・記述正確性の観点で diff をレビュー
- 指摘があれば `確認:pr-doc` に差し戻し → pr-doc が修正 → 再び `確認:pr-doc-review` に戻ってくる（AI 間ループ）
- 指摘が出尽くしたら最後に質問点をまとめてユーザーに投げる（`assignee=ユーザー`）

**担当セクション（PR 本文）**: なし（レビューはコメント中心、承認状況は GitHub の Approval 機能で見える）

**担当セクション詳細**: なし

**ユーザーとのコメントのやり取り**:

| No  | 起点     | 発生条件                                                          | 議論内容                                | 終了条件                                          | 備考                                       |
| --- | -------- | ----------------------------------------------------------------- | --------------------------------------- | ------------------------------------------------- | ------------------------------------------ |
| 1   | AI       | AI 間ループで結論が出ない箇所がある（記述スタイル・解釈判断要 など） | 質問点をまとめてユーザーに投げる        | ユーザー回答 → 反映 → AI 間ループに戻る           | AI 間ループが先・ユーザー対話は最後        |
| 2   | AI       | 全レビュー指摘解消後の最終承認依頼                                | （議論なし、GitHub Approval のみ）      | Approval → `フェーズ終了` 付与 → 次フェーズへ     | GitHub Approval のみ                       |
| 3   | ユーザー | AI 指摘への反論・根拠説明                                         | 指摘の妥当性議論                        | AI 合意なら取り下げ                               | -                                          |
| 4   | ユーザー | AI が見落とした観点の追加指摘                                     | 追加指摘箇所の修正                      | ラベルを `確認:pr-doc` に戻して修正依頼           | -                                          |

**カスタムサブエージェント**: なし

**フロー**:

1. **既存ドキュメント構造の調査（サブエージェント並列起動）**:
   - ドキュメント差分の整合性チェックにあたり、既存 Wiki / CLAUDE.md / Rules の構造・命名・関連ページの調査が必要なら、プロジェクト配下のカスタムサブエージェント定義（領域別／ドキュメント領域）があれば優先的に並列起動（なければ汎用 Agent）
   - 各サブエージェントには **Issue 本文 + PR 本文** + Wiki の `命名規則`・該当領域の関連ページを注入
   - 各サブエージェントは担当領域だけ調査し、既存ドキュメントとの整合性・重複可能性を返す
2. ドキュメント差分を計画整合性・既存ドキュメント整合性・記述正確性の観点でレビュー（1 の調査結果を踏まえる）
3. **指摘振り分け（AI 間ループ vs ユーザー質問）**:
   - AI で判断可能な指摘（記述ルール違反・整合性ずれ など）→ インラインコメント投稿 → ラベル `確認:pr-doc` に戻して再修正依頼 → pr-doc 完了で `確認:pr-doc-review` に戻ってきたら 1 に戻る（AI 間ループ）
   - 判断に迷う指摘（記述スタイル・複数の妥当な書き方など）→ 質問点として一時保留
4. **AI 間ループ収束判定**:
   - 全指摘が解消 → 5 へ
   - まだ指摘ある → 3 のループ継続
5. **ユーザー質問フェーズ**（AI 間で結論が出なかった質問点がある場合のみ）:
   - 保留していた質問点をまとめて投稿 → `assignee=ユーザー` で待機
   - ユーザー応答ループ:
     - フィードバックコメント + assignee 外す → 反映して 1 に戻る（再レビュー）
     - `フェーズ終了` 付与 → 次へ
6. **質問なし or ユーザー承認済み**: そのまま次へ
7. **ラベル更新**（前提条件: 自分宛コメントが全て本文反映済み（未反映あればユーザー確認後に自分宛のみ一括 Resolve））:
   - 上記条件を満たさなければ「本文反映 → 一括 Resolve」を先に実行
   - 満たしたら PR から `確認:pr-doc-review` + `フェーズ終了` 除去 / PR に付与なし（**ユーザー手動で `確認:pr-merge` 付与**）（フロー終了）

**ラベル更新**（フェーズ完了時=ユーザー `フェーズ終了` 付与後 or 質問なしで AI 間ループ完了後）:
- Issue: なし
- PR: 除去 `確認:pr-doc-review` + `フェーズ終了` / 付与 なし（ユーザー手動で `確認:pr-merge` 付与）


### 12. pr-merge

**モニター条件**:
- PR に `確認:pr-merge` ラベルが付与された
- Assignee にユーザが設定されていない

PR を base ブランチへマージする。コンフリクト解消もこのモニターの責務。

- master を取り込む → コンフリクトがあればユーザーに相談しながら解消
- `gh pr merge --squash --delete-branch` で squash マージ + リモートブランチ削除
- ローカルの worktree を削除

**担当セクション（PR 本文）**:
- 本文の追記はなし（マージで PR がクローズされるため）
- コンフリクト解消があった場合のみ、コメントに解消内容を記録

**担当セクション詳細**: なし

**ユーザーとのコメントのやり取り**:

| 起点     | 発生条件                                          | 議論内容                            | 終了条件                                          | 備考                                  |
| -------- | ------------------------------------------------- | ----------------------------------- | ------------------------------------------------- | ------------------------------------- |
| AI       | master 取り込み時にコンフリクト発生               | どちらの変更を残すかの相談          | ユーザー判断 → コンフリクト解消してマージ続行     | どちらの変更を残すかをユーザー判断    |

**カスタムサブエージェント**: なし

**フロー**:

1. worktree に復帰し master を取り込み
2. コンフリクトがあればユーザーに相談コメント（`assignee=ユーザー`）→ ユーザー判断で解消
3. `gh pr merge --squash --delete-branch` で squash マージ + リモートブランチ削除
4. ローカルの worktree を削除
5. **ラベル更新**: PR から `確認:pr-merge` 除去（マージで PR 自体がクローズ、`フェーズ終了` ラベルもクローズで実質無効化）（フロー終了）

※ pr-merge は最終段階のため、他フェーズと異なり「完了報告 → `フェーズ終了` 待ち」のユーザー応答ループは行わない（マージしたら終了）。

**ラベル更新**（マージ実行時）:
- Issue: なし（マージで自動クローズ）
- PR: 除去 `確認:pr-merge`（マージで PR 自体がクローズ、`フェーズ終了` ラベルもクローズで実質無効化）


### 13. reset

**モニター条件**:
- Issue/PR に `確認:reset` ラベルが付与された（ユーザー手動）
- Assignee にユーザが設定されていない

途中で不要になった Issue/PR を**巻き戻して初期化**する。これまでに作成した Wiki ページ・worktree などをすべて元に戻したうえで Issue/PR をクローズする。

**担当セクション**: なし（リセット作業のみ）

**担当セクション詳細**: なし

**ユーザーとのコメントのやり取り**:

| 起点     | 発生条件                                                          | 議論内容                                                  | 終了条件                                       | 備考                                       |
| -------- | ----------------------------------------------------------------- | --------------------------------------------------------- | ---------------------------------------------- | ------------------------------------------ |
| AI       | 巻き戻し対象（Wiki/worktree など）が複数あり判断が必要            | 削除して良いか、残すか、別 Issue に移譲するかをユーザー確認 | ユーザー判断                                   | -                                          |
| ユーザー | 「クローズする前にこれだけ残しておいて」のような追加指示           | 残すべき情報・別 Issue 移譲先を指示                       | 該当処理を実行                                 | -                                          |

**カスタムサブエージェント**: なし

**フロー**:

1. Issue/PR の本文を読み、各セクションから **「追記した Wiki」「PoC worktree」「Draft PR worktree」「子 Issue」** などの巻き戻し対象を全て洗い出す
2. 巻き戻し対象一覧をコメントで投稿し `assignee=ユーザー` で待機
3. ユーザー応答ループ:
   - 「全部削除でOK」「これは残す」「これは別 Issue に移譲」などの指示を受ける
   - `フェーズ終了` 付与 → 次へ
4. **巻き戻し実行**:
   - 削除対象の Wiki ページを削除（`外部ライブラリ一覧.md` などインデックスからも該当行を削除）
   - 削除対象の worktree（PoC・Draft PR とも）とローカルブランチを削除
   - リモートブランチが残っていれば削除
   - PR が存在する場合は `gh pr close --delete-branch`
   - Issue を `gh issue close --reason "not planned"` でクローズ
5. **ラベル更新**（前提条件: 自分宛コメントが処理済み（未反映あればユーザー確認後に自分宛のみ一括 Resolve）・巻き戻し対象が全て処理済み）:
   - 上記条件を満たさなければ「巻き戻し → コメント Resolve」を先に実行
   - 満たしたら `確認:reset` 除去 + `フェーズ終了` 除去（Issue/PR 自体はクローズ済み）（フロー終了）

**ラベル更新**（フェーズ完了時=ユーザー `フェーズ終了` 付与後）:
- Issue/PR: 除去 `確認:reset` + `フェーズ終了`（Issue/PR 自体はクローズ済み）


---

## 運用ルール

### assignee による状態管理

各モニターは「**監視ラベル付き AND assignee にユーザが入っていない**」Issue/PR を拾う。
assignee がボールの所在を示す。

| アクター | アクション               | assignee 操作                                    |
| -------- | ------------------------ | ------------------------------------------------ |
| AI       | コメントしてボールを渡す | `=ユーザー` を付ける                             |
| ユーザー | コメント等で返信         | **ユーザを外す**（モニターが再度拾えるように） |

スキル側は「最後のコメント著者が AI なら初回、ユーザーなら返信ターン」で分岐する。


### フェーズ終了ラベル（共通）

**`フェーズ終了`** ラベルを 1 つだけ用意し、全モニター共通で使う。

#### 役割

各モニターが本文・コメント整理を終え `assignee=ユーザー` で待機している状態で、ユーザーが「このフェーズの内容で OK」と判断したら **`フェーズ終了` ラベルを付与**する。

#### モニターの動き

| 検知ラベル状態                              | モニターの動き                                                                                              |
| ------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `確認:{自身}` のみ                          | 初回起動 → 仕事をして `assignee=ユーザー` で待機                                                            |
| `確認:{自身}` + ユーザー起点フィードバックコメント（**自身宛のみ**） | 該当箇所を本文反映 → `assignee=ユーザー` で待機（Resolve はフェーズ終了時に自分宛コメントのみ一括）             |
| `確認:{自身}` + `フェーズ終了`              | **フェーズ完了とみなす** → `確認:{自身}` 除去 + `フェーズ終了` 除去 + 次の `確認:{次モニター}` を付与で終了 |

#### 使い分け

| ユーザー操作              | 意味                                                                                |
| ------------------------- | ----------------------------------------------------------------------------------- |
| assignee を外す のみ      | 「フィードバックを返したので AI で続きの作業をして」（ループ継続）                  |
| `フェーズ終了` を付与     | 「このフェーズはこれで完了、次フェーズへ進めて OK」（ループ抜け、次フェーズへ遷移） |

`フェーズ終了` ラベルは次フェーズに進む直前にモニターが自分で除去するので、常にどこかの 1 つの Issue/PR にしか付かない想定。

#### フェーズ移行の前提条件（必須）

`確認:{自身}` + `フェーズ終了` を検知して次フェーズへ移行する前に、以下を順に実施:

1. **自分宛のコメント**を全件精査（コメント返信ルールの「精査対象」参照）
   - 自身が投稿したコメント
   - ユーザー → 自身宛のコメント
   - 他モニター宛のコメントは無視（そのモニターのフェーズ終了時に処理される）
2. **自分宛の未反映コメントがあるか確認**:
   - 全て本文反映済み → 自分宛コメントを一括 Resolve（`gh api graphql` の `minimizeComment` mutation で `RESOLVED`）→ 3 へ
   - 未反映あり → ユーザーに「これは反映してよいですか？反映不要ですか？」と質問コメント → `assignee=ユーザー` で待機 → ユーザー回答後に 1 から再判定
3. 本文の担当セクションが最新の確定版か最終確認 → 必要なら更新
4. `確認:{自身}` + `フェーズ終了` を除去 → 次の `確認:{次モニター}` を付与

「コメントは議論の経過であり、確定情報は本文に書く」原則の徹底のため。
Resolve されたコメントは後の pr-doc-plan で AI 改善計画の素材として参照される。


### コメント返信ルール（共通）

詳細は Wiki: **`gh-kit_共通_コメント返信.md`**

要点:
- 議論完了コメントは Resolve（minimizeComment mutation）で隠す。削除はしない
- 返信は同一コメントに `---` 区切りで追記。先頭に `@送信者 → @宛先` を必ず明記（AI は `🤖` 接頭辞）
- ユーザーコメントは 5 分類（質問 / 明確な指示 / 不明確な指示 / 妥当性に疑問 / 議論）で対応パターンが異なる
- コメントは個別 Resolve しない。`フェーズ終了` 付与時に自分宛コメントのみ一括 Resolve
- 「自分宛」判定は各コメント先頭の `@{宛先}` を見る


### 本文構造ルール（Issue/PR 共通）

本文はテンプレート構造にして、各モニターが担当セクションだけ上書きする。

#### Issue 本文テンプレート

詳細は Wiki: **`gh-kit_規約_イシュー本文.md`**

issue-triage が起票直後に全セクションの骨組みを作成し、後続モニター（issue-spec / issue-ui / issue-arch）が担当セクションだけ上書きする。担当一覧・テンプレート・記入例は Wiki 参照。

#### PR 本文テンプレート

pr-plan が起票直後に骨組みを作成し、後続モニターが自分の担当セクションだけ上書き更新する。

記入例（題材: ユーザープロフィール編集画面追加 — Issue #42 への対応 PR）

```markdown
## 紐づく Issue
<!-- pr-plan が記入 -->

- #42 ユーザープロフィール編集画面を追加する

## 実装計画
<!-- pr-plan が計画・pr-impl が完了したものから「完了」列を ✅ に更新 -->
<!-- コード・型・DB カラムなど全変更を 1 表にまとめる -->

| No | 完了 | 新規/変更 | レイヤー | 分類           | ファイル                                  | 対象                              | 概要                                                              | 補足                       |
| -- | ---- | --------- | -------- | -------------- | ----------------------------------------- | --------------------------------- | ----------------------------------------------------------------- | -------------------------- |
| 1  | ⬜   | 変更      | DB       | マイグレーション | `migrations/20260627_add_user_bio.sql`    | `users.bio`                       | 自己紹介用 `VARCHAR(500) NULL` カラムを `users` に追加              | -                          |
| 2  | ⬜   | 新規      | バック   | 型             | `types/user.ts`                           | `UpdateUserRequest`               | プロフィール更新リクエスト（氏名・自己紹介・任意アバター）         | -                          |
| 3  | ⬜   | 〃        | 〃       | 〃             | 〃                                        | `UpdateUserResponse`              | 更新後の `User` をラップしたレスポンス                            | -                          |
| 4  | ⬜   | 〃        | 〃       | メソッド       | `services/user_service.ts`                | `UserService.updateProfile()`     | ID と更新データを受け取り更新後の `User` を返す                   | 既存クラスへ追加 / バリデーション含む |
| 5  | ⬜   | 〃        | 〃       | エンドポイント | `api/users/[id].ts`                       | `PUT /api/users/{id}`             | `UpdateUserRequest` を受け取り `UpdateUserResponse` を返す        | 認可チェック含む           |
| 6  | ⬜   | 〃        | フロント | コンポーネント | `pages/profile/ProfileEditScreen.tsx`     | `ProfileEditScreen`               | プロフィール編集画面を描画                                        | -                          |
| 7  | ⬜   | 〃        | 〃       | 〃             | `components/AvatarCropModal.tsx`          | `AvatarCropModal`                 | 画像ソースとコールバックを受け取りトリミング UI を提供            | -                          |
| 8  | ⬜   | 〃        | 〃       | フック         | `hooks/useUpdateProfile.ts`               | `useUpdateProfile`                | API 呼び出しと送信中状態を管理                                    | -                          |

## テスト計画
<!-- pr-plan が骨組み・pr-test が中身を記入・pr-impl が「完了」列を ✅ に更新 -->

### 単体テスト

| No | 完了 | 種別     | ファイル                                | メソッド                              | 概要                          | 補足              |
| -- | ---- | -------- | --------------------------------------- | ------------------------------------- | ----------------------------- | ----------------- |
| 1  | ⬜   | 新規     | `tests/services/test_user_service.py`   | `test_update_profile_success`         | 正常系                        | -                 |
| 2  | ⬜   | 〃       | 〃                                      | `test_update_profile_validation`      | バリデーション失敗系          | 500字超 / 5MB超   |
| 3  | ⬜   | 〃       | 〃                                      | `test_update_profile_authorization`   | 他ユーザー更新拒否            | -                 |
| 4  | ⬜   | 既存実行 | 〃                                      | `test_get_user`                       | 既存テスト pass 維持確認      | -                 |

### 結合テスト

| No | 完了 | 種別 | ファイル                       | メソッド                       | 概要              | 補足                          |
| -- | ---- | ---- | ------------------------------ | ------------------------------ | ----------------- | ----------------------------- |
| 1  | ⬜   | 新規 | `tests/api/test_users.py`      | `test_put_users_id_e2e`        | API → DB 統合     | テスト DB に対し実 PUT を投げる |

### E2Eテスト

| No | 完了 | 種別     | ファイル                                 | メソッド | 概要                                  | 補足 |
| -- | ---- | -------- | ---------------------------------------- | -------- | ------------------------------------- | ---- |
| 1  | ⬜   | 新規     | `tests/e2e/profile_edit.spec.ts`         | -        | プロフィール編集フルフロー            | ※1   |
| 2  | ⬜   | 既存実行 | `tests/e2e/profile_view.spec.ts`         | -        | 表示画面に回帰がないこと              | -    |

※1: ログイン → `/profile/view` → 編集ボタン → 各項目編集（氏名・自己紹介・画像）→ 保存 → 詳細画面で反映確認

### 外部疎通テスト

| No | 完了 | 種別     | ファイル                                       | メソッド                              | 概要                                                              | 補足                                          |
| -- | ---- | -------- | ---------------------------------------------- | ------------------------------------- | ----------------------------------------------------------------- | --------------------------------------------- |
| 1  | ⬜   | 新規     | `tests/external/test_avatar_storage_live.py`   | `test_upload_avatar_live`             | アバター画像保存用の外部ストレージ（S3 互換）への実 PUT 疎通      | 課金発生・手動実行のみ・env キーなければ skip |
| 2  | ⬜   | 既存実行 | `tests/external/test_mail_notifier_live.py`    | `test_send_profile_updated_mail_live` | プロフィール更新通知メールの外部メール送信サービスへの実送信疎通  | 〃                                            |

## ドキュメント変更計画
<!-- pr-doc-plan が記入、ドキュメント影響あり時のみ・pr-doc が「完了」列を ✅ に更新 -->
<!-- 完了状態は ⬜ 未完 / ✅ 完了 の絵文字で表現（表内チェックボックスはレンダリングされないため） -->

| No | 完了 | ページ                              | セクション         | 変更内容                                  | 補足                          |
| -- | ---- | ----------------------------------- | ------------------ | ----------------------------------------- | ----------------------------- |
| 1  | ⬜   | `クラス図_user.md`                  | `### UserService`  | `updateProfile()` メソッド追記            | 要件由来                      |
| 2  | ⬜   | `APIエンドポイント一覧.md`          | -                  | `PUT /api/users/{id}` 行追加              | 要件由来                      |
| 3  | ⬜   | `データモデル一覧.md`               | `### User`         | `bio` フィールド追記                      | 要件由来                      |
| 4  | ⬜   | `外部ライブラリ_react-image-crop.md`    | -                  | 新規ページ作成                            | 採用ライブラリの使い方        |
| 5  | ⬜   | `外部ライブラリ一覧.md`             | -                  | `外部ライブラリ_react-image-crop.md` 行追加   | 要件由来                      |
| 6  | ⬜   | `CLAUDE.md`                         | `### pr-impl`      | TDD 手順の明示を追記                      | AI改善由来（CMT-003 で指摘）  |
```

| 役割                           | 場所         |
| ------------------------------ | ------------ |
| 議論の経緯（論点・質問・回答） | コメント履歴 |
| 確定した内容（最新版のみ）     | 本文         |
