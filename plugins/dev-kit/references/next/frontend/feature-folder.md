# app/(authenticated)/{feature}/ — フィーチャ単位フォルダ

1 つのリソース（resources, posts, members 等）に対応するフォルダ構成。

---

## 必須構成

```
app/(authenticated)/{feature}/
├── page.tsx                       # Server Component: 一覧（List）
├── {Feature}ListScreen.tsx        # Client Component: インタラクション
├── form.ts                        # Zod schema + Type（new と edit で共用）
├── actions.ts                     # Server Action 群（'use server'）
├── components/                    # フィーチャ内共有コンポーネント
├── hooks/                         # フィーチャ内共有 hook
├── new/
│   ├── page.tsx
│   └── {Feature}NewScreen.tsx
└── [id]/
    ├── page.tsx                   # View 画面（読み取りデフォルト）
    ├── {Feature}ViewScreen.tsx
    ├── components/                # view/edit 共通
    ├── hooks/                     # view/edit 共通
    └── edit/
        ├── page.tsx
        ├── {Feature}EditScreen.tsx
        ├── components/            # edit 専用
        └── hooks/                 # edit 専用
```

---

## ファイル種別と対応 reference

| ファイル | 詳細 reference |
|---|---|
| `page.tsx`（list / new / view / edit） | `frontend/list-page-tsx.md`, `view-page-tsx.md`, `edit-page-tsx.md` |
| `{Feature}ListScreen.tsx` | `frontend/list-screen-tsx.md` |
| `{Feature}NewScreen.tsx` / `{Feature}EditScreen.tsx` | `frontend/edit-screen-tsx.md` |
| `{Feature}ViewScreen.tsx` | `frontend/view-screen-tsx.md` |
| `form.ts` | `frontend/form-ts.md` |
| `actions.ts` | `backend/actions-ts.md` |
| `components/*.tsx` | フィーチャ固有のコンポーネント、規約は `frontend/components-catalog.md` 参照 |
| `hooks/use*.ts` | `frontend/use-query-pattern.md`, `use-form-pattern.md`, `use-url-state-pattern.md` |

---

## 完全な例 — resources

```
app/(authenticated)/resources/
├── page.tsx                       # 一覧 Server Component
├── ResourceListScreen.tsx         # 一覧 Client Component
├── form.ts                        # Zod schema (new/edit 共通)
├── actions.ts                     # registerResourceAction, updateResourceAction, deleteResourceAction
├── components/
│   └── ResourceCard.tsx
├── hooks/
│   ├── useResourceList.ts
│   └── useResourceListUrlState.ts
├── new/
│   ├── page.tsx
│   └── ResourceNewScreen.tsx
└── [id]/
    ├── page.tsx                   # View Server Component
    ├── ResourceViewScreen.tsx     # View Client Component
    ├── components/
    │   └── ResourceHeader.tsx     # view/edit 共通
    ├── hooks/
    │   └── useResource.ts         # view/edit 共通
    └── edit/
        ├── page.tsx
        ├── ResourceEditScreen.tsx
        ├── components/
        │   ├── ResourceEditLayout.tsx
        │   └── BasicSettings.tsx
        └── hooks/
            └── useResourceForm.ts
```

---

## `form.ts` の配置

PR135 で **フィーチャ直下**に変更（旧 `[id]/edit/form.ts` から）。new と edit で共有可能。

```ts
// app/(authenticated)/resources/form.ts
export const ResourceFormSchema = z.object({ /* ... */ })
export type ResourceFormType = z.infer<typeof ResourceFormSchema>
```

詳細: `frontend/form-ts.md`

---

## `actions.ts` の配置

フィーチャ直下。`'use server'` で開始。

```ts
// app/(authenticated)/resources/actions.ts
'use server'

export async function registerResourceAction(...) { /* ... */ }
export async function updateResourceAction(...) { /* ... */ }
export async function deleteResourceAction(...) { /* ... */ }
```

詳細: `backend/actions-ts.md`

---

## `components/` `hooks/` の配置

| Scope | Location |
|---|---|
| フィーチャ全体で共用 | `{feature}/components/`, `{feature}/hooks/` |
| `[id]/` 配下（view/edit 共用） | `{feature}/[id]/components/`, `{feature}/[id]/hooks/` |
| `[id]/edit/` 専用 | `{feature}/[id]/edit/components/`, `{feature}/[id]/edit/hooks/` |
| 複数フィーチャ共通 | `app/(shared)/components/`, `app/(shared)/hooks/` |

**アンダースコア prefix は使わない**（PR135 で廃止）。

---

## ルール

- フィーチャ名は **kebab-case 複数形**（`resources/`, `family-members/`）
- `form.ts` `actions.ts` はフィーチャ直下
- `[id]/page.tsx` は **View 画面**（PR135 で view/ サブルート廃止）
- 編集は `[id]/edit/`、新規は `new/`
- `components/` `hooks/` フォルダ名（アンダースコアなし）
- Screen 接尾辞: `ListScreen` / `NewScreen` / `ViewScreen` / `EditScreen`

## 関連 references

- `frontend/route-groups.md` — Route Group 全体
- `frontend/id-routing.md` — `[id]/` のルーティング詳細
- `frontend/conventions/naming.md` — 命名規約
- `frontend/conventions/server-vs-client.md` — Server / Client 境界
- `backend/actions-ts.md` — Server Action
- `frontend/form-ts.md` — Zod schema

## 禁止

- アンダースコア prefix（`_components/` `_hooks/`）
- `form.ts` を `[id]/edit/` 配下に置く（フィーチャ直下に統一）
- `view/` サブルートを作る（`[id]/page.tsx` を View 本体に）
- 単一画面のコンポーネントを `app/(shared)/components/` に置く
