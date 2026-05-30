<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# Route Groups — `(name)/`

URL に含まれないフォルダ単位の整理。本プロジェクトは **3 つに統一**。

---

## 採用する Route Group

| Group | 用途 |
|---|---|
| `(authenticated)` | 認証必須エリア。メイン画面群がここに入る |
| `(auth)` | 認証画面（login / signup / reset-password 等） |
| `(shared)` | 共通コンポーネント・hook・provider・schema・logger・endpoints |

---

## `(authenticated)/`

```
app/(authenticated)/
├── layout.tsx          # 認証ガード + AppShell
├── home/
├── resources/
├── settings/
└── ...
```

`layout.tsx` でセッションをチェックし、未認証なら `/login` に redirect:

```tsx
// app/(authenticated)/layout.tsx
import { redirect } from "next/navigation"
import { getOptionalAuthContext } from "@/app/(shared)/auth"
import { LOGIN_URL } from "@/app/(shared)/endpoints"
import { AppShell } from "@/app/(shared)/components/AppShell"

export default async function Layout({ children }: { children: React.ReactNode }) {
  const ctx = await getOptionalAuthContext()
  if (!ctx) redirect(LOGIN_URL)
  return <AppShell>{children}</AppShell>
}
```

軽量な認証チェックは `proxy.ts` でも行う（`backend/proxy.md`）。

---

## `(auth)/`

```
app/(auth)/
├── login/
│   ├── page.tsx
│   └── LoginScreen.tsx
├── signup/
│   ├── page.tsx
│   └── SignupScreen.tsx
└── reset-password/
    └── page.tsx
```

既にログイン済みのユーザーがアクセスしたら `/home` に redirect する:

```tsx
// app/(auth)/login/page.tsx
import { redirect } from "next/navigation"
import { getOptionalAuthContext } from "@/app/(shared)/auth"
import { HOME_URL } from "@/app/(shared)/endpoints"
import { LoginScreen } from "./LoginScreen"

export default async function Page() {
  const ctx = await getOptionalAuthContext()
  if (ctx) redirect(HOME_URL)
  return <LoginScreen />
}
```

---

## `(shared)/`

```
app/(shared)/
├── components/         # 共通 UI コンポーネント
│   └── ui/             # shadcn/ui copy
├── hooks/              # 複数フィーチャで使う hook のみ
├── providers/          # Theme, Query, Toaster, ConfirmDialog
├── auth/               # getAuthContext, provider, client
├── theme/              # next-themes 設定
├── endpoints.ts        # URL 定数
├── logger.ts           # JSON Lines ロガー
├── schema.ts           # Zod 共通プリミティブ
├── errors/             # AppError, handler 等
├── actions/            # 共通 Server Action
└── lib/
    └── utils.ts        # cn() 等
```

ここに置くもの:
- **複数フィーチャ** で使う UI / hook / 関数
- 認証・ロガー・エラー処理・URL 定数

ここに置かないもの:
- 単一フィーチャ専用のもの（→ `app/(authenticated)/{feature}/` 配下）

---

## ルール

- 3 つの Route Group 以外を作らない（増やすときは PR で議論）
- フィーチャは **`(authenticated)/{feature}/`** 配下
- `(authenticated)/layout.tsx` で認証ガード
- `(shared)/` の中身は **複数フィーチャで使うもの限定**

## 関連 references

- `frontend/app-folder-overview.md`
- `frontend/feature-folder.md` — フィーチャフォルダの中身
- `backend/auth-context.md` — getAuthContext
- `backend/proxy.md` — proxy.ts での認証ガード

## 禁止

- Route Group を増やす（`(admin)` `(dashboard)` `(public)` 等）
- 単一フィーチャ専用のものを `(shared)/` に置く
- アンダースコア prefix（`_components/` 等）— PR135 で廃止
