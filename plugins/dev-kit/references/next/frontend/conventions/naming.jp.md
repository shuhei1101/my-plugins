<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# Next.js App Router — Naming Conventions

## File and folder naming

| Target | Convention | Example |
|---|---|---|
| Folder | kebab-case | `resources/`, `family-members/` |
| Hook folder | `hooks/`（複数形、アンダースコアなし） | `hooks/` |
| Component folder | `components/`（複数形、アンダースコアなし） | `components/` |
| Page file | `page.tsx`（Next.js 規約） | `page.tsx` |
| Layout file | `layout.tsx` | `layout.tsx` |
| Loading file | `loading.tsx` | `loading.tsx` |
| Error file | `error.tsx`, `global-error.tsx` | `error.tsx` |
| Not-found file | `not-found.tsx` | `not-found.tsx` |
| Template file | `template.tsx` | `template.tsx` |
| Proxy file | `proxy.ts`（Next.js 16: 旧 middleware.ts） | `proxy.ts` |
| List screen file | PascalCase + `ListScreen` 接尾辞 | `ResourceListScreen.tsx` |
| New screen file | PascalCase + `NewScreen` 接尾辞 | `ResourceNewScreen.tsx` |
| View screen file | PascalCase + `ViewScreen` 接尾辞 | `ResourceViewScreen.tsx` |
| Edit screen file | PascalCase + `EditScreen` 接尾辞 | `ResourceEditScreen.tsx` |
| Layout component | PascalCase + `Layout` 接尾辞 | `ResourceEditLayout.tsx` |
| Sub-component | PascalCase | `ResourceCard.tsx` |
| Hook file | camelCase + `use` プレフィックス | `useResource.ts` |
| Form schema file | `form.ts`（小文字固定） | `form.ts` |
| Util / config / endpoints | camelCase | `endpoints.ts`, `logger.ts`, `utils.ts` |
| Dynamic segment | `[id]`, `[slug]`, `[childId]` | `[id]/` |
| Route Group | `(name)` 小文字 | `(authenticated)`, `(auth)`, `(shared)` |

### アンダースコアプレフィックスの廃止（PR135）

旧 `_components/` `_hooks/` の `_` プレフィックスは **不要** と判断（→ 廃止）。`components/` `hooks/` で十分。
- Next.js Private Folder（`_` prefix）は route 化を回避するための機能だが、`components/` `hooks/` はそもそも route ファイル名と衝突しない
- 視覚的にもシンプル、フックトリガーパターンとしても扱いやすい

---

## Per-record View / Edit 規約

各レコードは **`[id]/page.tsx` が View**、**`[id]/edit/page.tsx` が Edit**:

| URL | Screen file | Path |
|---|---|---|
| `/{feature}/[id]` | `{Feature}ViewScreen.tsx` | `[id]/` |
| `/{feature}/[id]/edit` | `{Feature}EditScreen.tsx` | `[id]/edit/` |

権限ガードは `proxy.ts` で行う（`backend/proxy.md` 参照）。

---

## Screen / Layout / Card

| 接尾辞 | 役割 | When to use |
|---|---|---|
| `ListScreen` | 一覧画面 | `/{feature}/page.tsx` から render |
| `NewScreen` | 新規作成画面 | `/{feature}/new/page.tsx` から render |
| `ViewScreen` | 読み取り画面 | `/{feature}/[id]/page.tsx` から render |
| `EditScreen` | 編集画面 | `/{feature}/[id]/edit/page.tsx` から render |
| `Layout` | Screen 内で使う再利用シェル | header + content + actions の構成体 |
| `Card` | 一覧内の 1 アイテム | `*ListScreen.tsx` の中で使用 |
| `Item` | フィードの 1 エントリ | infinite-scroll feed 内 |
| `Settings` | edit フォームのタブ | `*EditScreen.tsx` 内のタブパネル |
| `Dialog` / `Sheet` | shadcn/ui のモーダル系 | `dialog.md` 参照 |
| `Form` | フォーム部分コンポーネント | 入力グループの再利用ブロック |
| `Provider` | Context Provider | `app/(shared)/providers/` 配下 |
| `Wrapper` | スタイリングシェル with `children` | `ScreenWrapper` 等 |

---

## Hook naming

| Pattern | Purpose | Example |
|---|---|---|
| `use{Feature}` | 単体読み取り | `useResource` |
| `use{Feature}List` | 一覧読み取り | `useResourceList` |
| `use{Feature}View` | View 専用フィールドがある場合 | `useResourceView` |
| `use{Feature}Form` | フォーム state + 初期ロード | `useResourceForm` |
| `useRegister{Feature}` | 作成 mutation | `useRegisterResource` |
| `useUpdate{Feature}` | 更新 mutation | `useUpdateResource` |
| `useDelete{Feature}` | 削除 mutation | `useDeleteResource` |
| `use{Feature}UrlState` | URL クエリ state | `useResourceListUrlState` |

ルール:
- 1 hook = 1 file、ファイル名 = export 名
- 必ず `use` で始める（React のルール）
- 1 動詞（Register / Update / Delete）= 1 ファイル

---

## Zod schema naming

| Pattern | Example | Notes |
|---|---|---|
| `{Feature}FormSchema` | `ResourceFormSchema` | Zod object |
| `{Feature}FormType` | `ResourceFormType` | `z.infer<>` で導出 |
| `{Feature}FilterSchema` | `ResourceFilterSchema` | フィルタ用 Zod |
| `{Feature}Filter` (type) | `ResourceFilter` | 同上の型 |
| `{Feature}RequestSchema` | `PostResourceRequestSchema` | API リクエストボディ用（`route.ts` 内） |
| `{Feature}Request` (type) | `PostResourceRequest` | 同上の型 |

新規コードは `Schema`（`Scheme` ではない）を使う。既存コードの `Scheme` は触る際にリネーム。

---

## Server Action naming

```ts
// app/(authenticated)/resources/actions.ts
'use server'

export async function createResource(input: ResourceFormType) { /* ... */ }
export async function updateResource(id: string, input: ResourceFormType) { /* ... */ }
export async function deleteResource(id: string) { /* ... */ }
```

- ファイル: `actions.ts`（フィーチャ直下、または `app/(shared)/actions/` 配下）
- 関数名は動詞 + 名詞（`createResource`, `updateResource`, `deleteResource`）
- 詳細: `backend/server-actions.md`

---

## URL constant naming

詳細は `frontend/endpoints.md`。サマリ:

```ts
// 単発の URL
export const HOME_URL = `/home`

// フィーチャグループ（オブジェクト）
export const RESOURCE_URL = {
  list: `/resources`,
  new:  `/resources/new`,
  view: (id: string) => `/resources/${id}`,         // [id]/page.tsx が View
  edit: (id: string) => `/resources/${id}/edit`,
}

// API はバージョン付き
export const RESOURCE_API_URL = {
  list:   `/api/v1/resources`,
  detail: (id: string) => `/api/v1/resources/${id}`,
}
```

---

## Constraints

- アンダースコアプレフィックスは使わない（旧 `_hooks/` `_components/` から PR135 で変更）
- `form.ts` はフィーチャ直下に置く（new と edit で共用）
- Screen 接尾辞: `ListScreen` / `NewScreen` / `ViewScreen` / `EditScreen` を使い分ける
- 単に `Screen` という接尾辞は使わない
- `index.tsx` は feature folder に置かない（役割名のファイル名を付ける）
- 動的 segment は `[id]`、ネスト時は `[childId]` のように区別
- Route Group は `(authenticated)` `(auth)` `(shared)` の 3 つ
- Proxy ファイルは `proxy.ts`（旧 `middleware.ts` から Next.js 16 でリネーム）
