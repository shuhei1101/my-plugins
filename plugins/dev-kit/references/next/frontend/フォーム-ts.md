<!-- This file is a Japanese mirror of フォーム-ts.md. When updating the English original, update this file too. -->
# app/(authenticated)/{feature}/form.ts — Zod schema + Type

フォーム用の Zod スキーマと型。**new と edit で共用**するためフィーチャ直下に置く（PR135）。

---

## 必須テンプレ

```ts
// app/(authenticated)/resources/form.ts
import { z } from "zod"
import { IconIdSchema, IconColorSchema } from "@/app/(shared)/schema"

/** リソース登録/編集フォームスキーマ */
export const ResourceFormSchema = z.object({
  name: z.string()
    .nonempty({ error: "リソース名は必須です。" })
    .min(1)
    .max(20, { error: "リソース名は 20 文字以下で入力してください。" }),
  iconId: IconIdSchema,
  iconColor: IconColorSchema,
  /** タグ（最大 10 件） */
  tags: z.array(z.string()).max(10),
  /** カテゴリ ID（null は未分類） */
  categoryId: z.number().nullable(),
  isPublic: z.boolean(),
})

/** リソース登録/編集フォーム型（推論） */
export type ResourceFormType = z.infer<typeof ResourceFormSchema>

/** new 画面用デフォルト値 */
export const defaultResourceForm: ResourceFormType = {
  name: "",
  iconId: 1,
  iconColor: "#3B82F6",
  tags: [],
  categoryId: null,
  isPublic: false,
}
```

---

## 共通プリミティブ

`app/(shared)/schema.ts` に複数フィーチャで使うスキーマを集約:

```ts
// app/(shared)/schema.ts
import { z } from "zod"

/** ID — 半角英数字 + アンダースコア */
export const IdSchema = z.string().regex(/^[a-zA-Z0-9_]+$/, {
  message: "半角英数字とアンダースコアのみ使用可能です",
})

/** 表示 ID — 5〜20 文字 */
export const DisplayIdSchema = IdSchema.min(5).max(20)

/** アイコン ID */
export const IconIdSchema = z.number({ error: "アイコンは必須です。" })

/** アイコンカラー */
export const IconColorSchema = z.string({ error: "アイコンカラーは必須です。" })
```

---

## Schema 拡張

```ts
export const PremiumResourceFormSchema = ResourceFormSchema.extend({
  planId: z.string(),
})
export type PremiumResourceFormType = z.infer<typeof PremiumResourceFormSchema>
```

---

## クロスフィールドバリデーション

```ts
export const ResourceFormSchema = z.object({
  // ...
  ageFrom: z.number().nullable(),
  ageTo: z.number().nullable(),
})
.refine((data) => {
  if (data.ageFrom == null || data.ageTo == null) return true
  return data.ageFrom < data.ageTo
}, {
  message: "開始年齢は終了年齢より小さい必要があります",
  path: ["ageFrom"],
})
```

`path: ["fieldName"]` で shadcn `<FormMessage>` が該当フィールド下に表示。

---

## エラーメッセージ

- **日本語、ユーザー向け文言**
- 必須は `nonempty({ error: "..." })`
- 長さは `.max(N, { error: "..." })`
- カスタムは `.refine(check, { message, path })`

---

## ルール

- 配置は **`{feature}/form.ts`** （PR135、`[id]/edit/` 配下から移動）
- 型は **`z.infer<>`** で導出（手書き禁止）
- `defaultResourceForm` を export（new 画面で利用）
- 共通プリミティブは `app/(shared)/schema.ts` に集約
- エラーメッセージは日本語
- ファイル種別の Schema 名: `{Feature}FormSchema`
- 型名: `{Feature}FormType`

## 関連 references

- `frontend/フォームコンポーネント.md` — shadcn `<Form>` でのバインド
- `frontend/編集スクリーン-tsx.md` — フォーム送信
- `backend/アクション-ts.md` — Server Action 側でも同じ schema を `.parse`
- `frontend/conventions/型定義.md` — 型導出全般

## 禁止

- `form.ts` を `[id]/edit/` 配下に置く（PR135 でフィーチャ直下に移動）
- 型を手書きする（必ず `z.infer<>`）
- エラーメッセージを英語で書く
- 同じ schema を `route.ts` と `actions.ts` で別定義
- 単一フィーチャ固有のものを `app/(shared)/schema.ts` に置く
