<!-- This file is a Japanese mirror of zustand-pattern.md. When updating the English original, update this file too. -->
# Zustand — クロスルート state パターン

頻繁更新 / selector が必要な共有 state。Context で不十分なときに使う。

---

## 必須テンプレ

```ts
// app/(shared)/stores/useAppStore.ts
'use client'

import { create } from "zustand"

type AppStore = {
  unreadCount: number
  setUnreadCount: (n: number) => void
  reset: () => void
}

export const useAppStore = create<AppStore>((set) => ({
  unreadCount: 0,
  setUnreadCount: (n) => set({ unreadCount: n }),
  reset: () => set({ unreadCount: 0 }),
}))
```

---

## 使い方（selector 推奨）

```tsx
'use client'
import { useAppStore } from "@/app/(shared)/stores/useAppStore"

// 全体を取る（再 render 多い）
const store = useAppStore()

// selector で部分購読（推奨）
const unread = useAppStore((s) => s.unreadCount)
const setUnread = useAppStore((s) => s.setUnreadCount)
```

`selector` を使うと、その値が変わった時だけ再 render される。

---

## いつ Zustand を使う

- 頻繁な更新で **Context だと全 consumer が re-render** する
- **React tree 外** からも参照したい（middleware・analytics 等）
- **selector で部分購読** したい

---

## 使わないケース

| 状態 | 適切なツール |
|---|---|
| サーバーデータ | TanStack Query |
| URL state | URL クエリ |
| フォーム値 | react-hook-form |
| 1 コンポーネント内のみ | useState |

---

## persist（永続化）

```ts
import { persist } from "zustand/middleware"

export const usePreferencesStore = create<Preferences>()(
  persist(
    (set) => ({
      density: "comfortable",
      setDensity: (d) => set({ density: d }),
    }),
    { name: "preferences-storage" }
  )
)
```

`localStorage` に保存されるので、リロード後も値を保持。

---

## 既存 store の例（参考）

- `useConfirmDialogStore` — 確認ダイアログ（`frontend/confirm-dialog.md`）
- `useAppStore` — 通知未読数等（プロジェクトに応じて）

---

## ルール

- 配置は **`app/(shared)/stores/use{Name}Store.ts`** または `app/(shared)/hooks/`
- selector で部分購読（パフォーマンス）
- persist が必要なら `zustand/middleware` の `persist`
- 関連 state は **1 つの store** にまとめる（複数 store は connection 必要時のみ）

## 関連 references

- `frontend/state-decision.md`
- `frontend/context-pattern.md` — Context 代替候補
- `frontend/confirm-dialog.md` — 実装例

## 禁止

- サーバーデータ / フォーム値 を Zustand に入れる
- selector なしで全体取得（不必要 re-render）
- 1 機能 1 store の細かい分割（過剰）
- 状態が小さい / 更新少ない場合に使う（→ Context で十分）
