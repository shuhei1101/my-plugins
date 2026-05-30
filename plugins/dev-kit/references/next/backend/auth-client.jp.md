<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# app/(shared)/auth/client.ts — クライアント側 useSession

ブラウザから Better Auth のセッションを参照・操作する hook。

---

## 必須テンプレ

```ts
// app/(shared)/auth/client.ts
'use client'

import { createAuthClient } from "better-auth/react"

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL,
})

// React hook を export
export const useSession = authClient.useSession
```

---

## コンポーネントでの使い方

```tsx
'use client'
import { useSession } from "@/app/(shared)/auth/client"

export const UserAvatar = () => {
  const { data: session, isPending } = useSession()
  if (isPending) return <Skeleton className="h-8 w-8 rounded-full" />
  if (!session) return null
  return (
    <Avatar>
      <AvatarImage src={session.user.image ?? undefined} />
      <AvatarFallback>{session.user.name?.[0]}</AvatarFallback>
    </Avatar>
  )
}
```

---

## クライアントから直接認証操作

「クライアントで完結したい」場合（一般的には Server Action 推奨だが、SPA 的なフローならクライアント側 sign in / sign out も可）:

```tsx
'use client'
import { authClient } from "@/app/(shared)/auth/client"
import { useRouter } from "next/navigation"
import { HOME_URL, LOGIN_URL } from "@/app/(shared)/endpoints"

const router = useRouter()

await authClient.signIn.email({ email, password })
router.push(HOME_URL)

await authClient.signOut()
router.push(LOGIN_URL)
```

ただし Server Action での処理が推奨（プログレッシブエンハンスメント・CSRF 対策が楽）。詳細: `auth-actions.md`

---

## ルール

- 配置は **`app/(shared)/auth/client.ts`**（ファイル冒頭 `'use client'`）
- `baseURL` は `NEXT_PUBLIC_APP_URL` 経由
- Server 側からは絶対に import しない（クライアント専用）
- `useSession` でセッション購読 → リアクティブに更新される
- `isPending` で loading 状態を扱う

## 関連 references

- `auth-context.md` — Server 側の `getAuthContext()`
- `auth-setup.md` — Better Auth 全体設定
- `auth-actions.md` — Server Action（推奨）

## 禁止

- Server Component からこのファイルを import
- セッショントークンを手動取得（`useSession` 経由）
- localStorage への session 保存
