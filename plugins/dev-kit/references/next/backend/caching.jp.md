<!-- This file is a Japanese mirror of caching.md. When updating the English original, update this file too. -->
# Next.js App Router — Caching

> **Next.js 16 のキャッシュ API**: `cacheLife`, `cacheTag`, `revalidateTag`（cacheLife プロファイル必須化）, `updateTag`（新）, `refresh`（新）, `"use cache"` ディレクティブ。

---

## キャッシュ階層

| 層 | 説明 |
|---|---|
| **Request Memoization** | 同一リクエスト内の `fetch` を自動メモ化 |
| **Data Cache** | `fetch` / `"use cache"` 関数のレスポンスキャッシュ（プロセス間共有） |
| **Full Route Cache** | プリレンダ HTML / RSC payload |
| **Router Cache** | クライアント側のキャッシュ（戻る・進む） |

Next.js 16 では Cache Components（`cacheComponents: true`）が PPR の標準動作になり、レンダリング戦略が大きく変わる。

---

## Cache Components / PPR

`next.config.ts`:

```ts
import type { NextConfig } from "next"
const nextConfig: NextConfig = {
  cacheComponents: true,
}
export default nextConfig
```

有効化すると:
- 静的にレンダリング可能な部分はビルド時 / ISR でプリレンダ
- 動的な部分（`cookies()` `headers()`、`<Suspense>` 内）はリクエスト時レンダ
- ユーザーは静的部分を即座に受け取り、動的部分はストリーム

---

## "use cache" ディレクティブ

```ts
// app/api/v1/categories/query.ts
import { cacheLife, cacheTag } from "next/cache"

export async function getCategories() {
  "use cache"
  cacheLife("max")
  cacheTag("categories")

  return await db.select().from(categories)
}
```

- ファイル全体、関数、コンポーネントのいずれかに付けられる
- 関数の戻り値がキャッシュされる（同じ引数なら次回はキャッシュヒット）

---

## cacheLife プロファイル

`cacheLife()` には組み込みプロファイルを渡せる:

| プロファイル | stale | revalidate | expire |
|---|---|---|---|
| `default` | 5 min | 15 min | 1 year |
| `seconds` | 0 | 1 sec | 1 sec |
| `minutes` | 1 min | 1 min | 1 hour |
| `hours` | 5 min | 1 hour | 1 day |
| `days` | 5 min | 1 day | 1 week |
| `weeks` | 5 min | 1 week | 1 month |
| `max` | 5 min | 1 month | 1 year |

カスタム:

```ts
"use cache"
cacheLife({ stale: 60, revalidate: 60 * 5, expire: 60 * 60 })
```

---

## cacheTag

```ts
"use cache"
cacheTag("resources")
cacheTag(`resource:${id}`)
```

複数タグを付けられる。invalidate 時にタグでターゲット指定。

---

## revalidateTag — stale-while-revalidate

```ts
import { revalidateTag } from "next/cache"

// Server Action 内
revalidateTag("resources", "max")
```

**Next.js 16 で第 2 引数（cacheLife プロファイル）必須化**。指定がないと TypeScript エラー。

挙動: タグ付きキャッシュを stale としてマーク → 次の閲覧者はバックグラウンドで再生成しつつ古いデータを見る。

用途: 多少の遅延が許される更新（ブログ、プロダクトカタログ、ドキュメント）。

---

## updateTag — read-your-writes（新、Next.js 16）

```ts
import { updateTag } from "next/cache"

// Server Action 内
export async function updateProfileAction(input) {
  await updateProfile(input)
  updateTag(`user:${userId}`)        // 即時 expire + refresh
}
```

挙動: タグ付きキャッシュを **即時 expire**、同じリクエスト内で再フェッチ。ユーザーは変更後即座に反映を見る。

用途: フォーム保存、設定変更、楽観 UI を補強したい場合。

---

## refresh — client router 更新（新、Next.js 16）

```ts
import { refresh } from "next/cache"

// Server Action 内
export async function actionWithRefresh() {
  await someUpdate()
  refresh()                          // client router の RSC payload を更新
}
```

`router.refresh()` のサーバー版。Server Action 完了時にクライアントルーターが再フェッチする。

---

## Server Action でのパターン

```ts
'use server'

import { revalidateTag, updateTag, refresh } from "next/cache"

// 一覧用キャッシュ全部 + 単体キャッシュを invalidate
export async function updateResourceAction(id: string, input: FormType) {
  await editResource({ ... })

  // ユーザーは更新即時に反映を見たい → updateTag
  updateTag(`resource:${id}`)

  // 一覧は他のユーザーには遅延 OK → revalidateTag
  revalidateTag("resources", "max")

  // RSC payload も更新
  refresh()
}
```

---

## fetch() のキャッシュ

`fetch()` の `next` オプション:

```ts
// 永続キャッシュ（次回ビルドまで）
await fetch(url, { cache: "force-cache" })

// 毎回フレッシュ
await fetch(url, { cache: "no-store" })

// タグ付き
await fetch(url, { next: { tags: ["resources"] } })

// 時間ベースの revalidation
await fetch(url, { next: { revalidate: 60 } })
```

`cacheComponents: true` 環境では `"use cache"` + `cacheLife` を優先（より型安全）。

---

## Cache の決定フロー

```
データはユーザーごとに違う?
  ├─ Yes → キャッシュしない（cookies()/headers() を呼べば動的）
  └─ No → 次へ

データはどれくらい古くてもいい?
  ├─ 即時 → cacheLife("seconds") or キャッシュなし
  ├─ 数分 → cacheLife("minutes")
  ├─ 数時間 → cacheLife("hours")
  ├─ 数日 → cacheLife("days")
  └─ 1ヶ月+ → cacheLife("max")

mutation 後に即時反映必要?
  ├─ Yes → updateTag() + refresh()
  └─ No → revalidateTag(tag, "max")
```

---

## マスター系データのキャッシュ

カテゴリ・アイコン等の頻繁に変わらないマスタは長めにキャッシュ:

```ts
// app/api/v1/categories/query.ts
import { cacheLife, cacheTag } from "next/cache"

export async function getCategories() {
  "use cache"
  cacheLife("max")
  cacheTag("categories")
  return await db.select().from(categories).orderBy(asc(categories.sortOrder))
}
```

管理画面でカテゴリ追加したら:

```ts
revalidateTag("categories", "max")
```

---

## クライアント側キャッシュ（Router Cache）

クライアント側のナビゲーションキャッシュ。`router.prefetch()` で前もって取得:

```tsx
import Link from "next/link"

<Link href={RESOURCE_URL.view(id)} prefetch={true}>{name}</Link>
```

`prefetch={false}` で抑止可。Next.js 16 では prefetch 戦略が改善されレイアウト重複を排除。

---

## Anti-patterns

- `revalidateTag` を引数 1 つで呼ぶ（Next.js 16 では型エラー）→ 第 2 引数の cacheLife プロファイル必須
- `force-dynamic` で全部動的化 → PPR の恩恵を失う
- ユーザーごとに違うデータをキャッシュする → 別ユーザーに漏洩
- `cookies()` `headers()` を不必要に呼ぶ → ページ全体が動的化
- 重い計算結果をキャッシュしない → 毎回計算
- mutation 後に invalidate を忘れる → 古いデータを見せ続ける

---

## TanStack Query との関係

クライアント側キャッシュは TanStack Query が担当。Server / Server Action 側は Next.js キャッシュ。

```
ブラウザ
  └─ TanStack Query キャッシュ（useQuery）
       └─ HTTP リクエスト → /api/v1/resources
                                  └─ Next.js Router Cache
                                       └─ Server Component / route.ts
                                            └─ Next.js Data Cache（"use cache"）
                                                 └─ DB
```

両者は独立して動作。Server Action 後の同期は `updateTag` / `revalidateTag` + `queryClient.invalidateQueries`。

---

## Constraints

- `revalidateTag` は第 2 引数（cacheLife プロファイル）必須（Next.js 16）
- mutation の同期反映には `updateTag` + `refresh`
- 多少遅延が許される更新には `revalidateTag(tag, "max")`
- `"use cache"` 関数は引数で変動するなら自動的にバリアントごとにキャッシュ
- ユーザー固有データはキャッシュしない（`cookies()` 呼出で自動的に動的化）
- マスター系・カテゴリ系は `cacheLife("max")` + タグ管理
- Cache Components（`cacheComponents: true`）採用は段階的に
- `unstable_cache` は廃止、`"use cache"` に統一
