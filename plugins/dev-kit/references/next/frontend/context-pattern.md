# React Context — 共有 state パターン

複数のルート / コンポーネントで共有する UI state を Context で持つ。

---

## 必須テンプレ

```tsx
'use client'

import { createContext, useContext, useState, type ReactNode } from "react"

type AppShellValue = {
  sidebarOpen: boolean
  toggleSidebar: () => void
}

const AppShellContext = createContext<AppShellValue | null>(null)

export const AppShellProvider = ({ children }: { children: ReactNode }) => {
  const [sidebarOpen, setOpen] = useState(false)
  return (
    <AppShellContext.Provider value={{ sidebarOpen, toggleSidebar: () => setOpen((v) => !v) }}>
      {children}
    </AppShellContext.Provider>
  )
}

export const useAppShell = () => {
  const ctx = useContext(AppShellContext)
  if (!ctx) throw new Error("useAppShell must be used within AppShellProvider")
  return ctx
}
```

---

## 既存 Context（重複させない）

| Context | File | 用途 |
|---|---|---|
| `ThemeProvider` | next-themes | ライト/ダーク |
| `QueryProvider` | TanStack | server state |
| `ToasterProvider` | sonner | toast |
| `ConfirmDialogProvider` | shadcn AlertDialog | 確認ダイアログ |
| `AppShellContext` | 自前 | サイドメニュー開閉等 |

---

## いつ Context を作る

- **複数のルート/コンポーネント** で共有
- サーバーデータ / URL state / フォーム state では不適切
- prop drilling が **3+ レベル**

---

## Context vs Zustand

| 特徴 | Context | Zustand |
|---|---|---|
| 設定の簡単さ | ✓ | △ |
| 更新時の再 render | 全 consumer | selector 範囲のみ |
| React tree 外からの参照 | ✗ | ✓ |
| 大規模 / 高頻度更新 | △ | ✓ |

迷ったら Context、頻繁更新 / selector が要るなら Zustand。

---

## ルール

- 1 つの Context = 1 つの責務
- Provider は **`app/(shared)/providers/`** 配下
- カスタム hook（`use{Name}`）経由でアクセス
- `null` チェックを hook 内で（外から `useContext` を直接呼ばない）
- 更新頻度が高いなら **Zustand に切り替え** 検討

## 関連 references

- `frontend/state-decision.md`
- `frontend/zustand-pattern.md`
- `frontend/components-catalog.md` — 既存 provider 一覧

## 禁止

- Context を **複数 Provider boundary** で多重定義（1 つにまとめる）
- フォーム state を Context に入れる
- サーバーデータを Context に入れる
- `useContext` を直接呼ぶ（必ず `use{Name}` カスタム hook 経由）
- null チェックなしに `ctx.field` を参照
