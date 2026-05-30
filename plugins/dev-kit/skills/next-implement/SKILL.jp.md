---
name: implement
description: |
  Next.js App Router でページ・コンポーネント・hook・API ルート・Server Action を新規作成・編集するとき。
  ユーザーが「画面を作って」「コンポーネントを実装して」「API を追加して」「Server Action を書いて」「Next.js の規約に従って」と言ったとき、または `/dev-kit:next-implement` を明示的に呼び出したとき。
---
<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# implement — Next.js 実装規約ガイド

Next.js App Router のページ・コンポーネント・hook・API ルート・Server Action を実装する。Next.js 16 + shadcn/ui + Tailwind + Drizzle + TanStack Query 前提。

---

## 概要

Next.js 実装作業を始めるときに呼ぶスキル。

References は **1 ファイル = 1 ユースケース** で分割されている（PR135、QA-073）。編集対象のファイル種別に対応する reference だけを読む。

**前提スタック**:
- Next.js 16 (App Router, proxy.ts, Cache Components, Async Request APIs)
- React 19.2 (View Transitions, useEffectEvent, React Compiler)
- shadcn/ui + Tailwind
- Drizzle ORM
- TanStack Query + Server Actions（mutation の第一選択）
- Better Auth
- sonner / lucide-react / date-fns

---

## タスク

### ステップ 1: 対象ファイルを特定し、対応する reference を読む

#### 条件

- 必ず最初に実行

#### 処理

1. 編集対象のファイル種別を特定（`*.tsx`, `route.ts`, `query.ts`, `actions.ts` 等）
2. `references/CLAUDE.md` の「ファイル種別 → reference マッピング」を参照
3. 該当する reference を 1〜数個読む（**1 ファイルに 1 ユースケース** で分割済み）

主要マッピング:

| 編集対象 | Read |
|---|---|
| `app/(authenticated)/{feature}/page.tsx` (list) | `frontend/list-page-tsx.md` |
| `{Feature}ListScreen.tsx` | `frontend/list-screen-tsx.md` |
| `[id]/page.tsx` (view) | `frontend/view-page-tsx.md` |
| `{Feature}ViewScreen.tsx` | `frontend/view-screen-tsx.md` |
| `[id]/edit/page.tsx`, `new/page.tsx` | `frontend/edit-page-tsx.md` |
| `*EditScreen.tsx`, `*NewScreen.tsx` | `frontend/edit-screen-tsx.md` |
| `form.ts` | `frontend/form-ts.md` |
| `actions.ts` | `backend/actions-ts.md` |
| `route.ts` | `backend/route-ts.md` |
| `client.ts` | `backend/client-ts.md` |
| `service.ts` | `backend/service-ts.md` |
| `db.ts` | `backend/db-ts.md` |
| `query.ts` | `backend/query-ts.md` |
| `drizzle/schema.ts` | `backend/db-id.md` + `db-timestamps.md` + `db-relations.md` 等 |
| `hooks/use{Feature}.ts` | `frontend/use-query-pattern.md` |
| `hooks/use{Feature}Form.ts` | `frontend/use-form-pattern.md` |
| `hooks/use{Feature}UrlState.ts` | `frontend/use-url-state-pattern.md` |
| `proxy.ts` | `backend/proxy.md` |
| `error.tsx` | `frontend/error-tsx.md` |
| `not-found.tsx` | `frontend/not-found-tsx.md` |

全マッピングは `references/CLAUDE.md` 参照。

→ ステップ 2 へ

#### 出力

- 編集対象に対応する reference の読み込み完了

---

### ステップ 2: フォルダと配置を確認

#### 条件

- ステップ 1 完了

#### 処理

1. `frontend/feature-folder.md`、`frontend/route-groups.md`、`frontend/id-routing.md` で配置先を確認
2. 命名規約は `frontend/conventions/naming.md`
3. `page.tsx` は **Server Component を第一選択**（async function）、`*Screen.tsx` は `'use client'`
4. Route Group は **`(authenticated)` / `(auth)` / `(shared)`** に統一
5. API ルートは **`app/api/v1/`** 配下（バージョニング）
6. `[id]/page.tsx` は **View 画面そのもの**（PR135、`view/` サブルート廃止）
7. `form.ts` `actions.ts` は **フィーチャ直下**
8. `components/` `hooks/` （アンダースコアなし、PR135 で変更）

→ ステップ 3 へ

#### 出力

- 配置パスを確認

---

### ステップ 3: 対応 reference に従って実装

#### 条件

- ステップ 2 完了

#### 処理

1. 該当 reference の必須テンプレに従って実装
2. ルール・禁止事項を厳守
3. 関連 reference（コメント・型・命名 等）を必要に応じて参照

主要原則:

- **mutation は Server Action 第一選択**（HTTP API は外部公開・複雑処理のみ）
- フォームは **shadcn `<Form>` + RHF + Zod**
- **削除のみ確認ダイアログ**（登録・更新は不要、QA-027）
- **エラーは AppError 派生** を投げ、handler 経由でレスポンス / toast
- **ログは `logger.create("tag")`**（`console.log` 禁止）
- **URL は `RESOURCE_URL.*` 経由**（hard-code 禁止）
- **CQRS 分離**: query.ts = SELECT 全集約 / db.ts = INSERT・UPDATE・DELETE / service.ts = トランザクション境界
- **ハードデリート + 履歴テーブル** パターン
- **楽観的ロックは `updatedAt`**（必要なら `version` 列）
- **主キー**: マスター = integer、データ = UUID

→ 完了

#### 出力

- 規約準拠の実装が完了

---

## 参考資料

- `references/CLAUDE.md` — 全 reference のファイル種別マッピング（インデックス）
- `references/frontend/` — フロントエンド規約
- `references/backend/` — バックエンド規約
- `references/shared/` — 共通
- `references/testing/` — テスト戦略
- `references/devtools/` — lint / storybook / mock
- `references/devops/` — deploy
