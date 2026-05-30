<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# `<ScreenWrapper>` — Screen の必須外殻

全 Screen コンポーネント（`*ListScreen.tsx` / `*ViewScreen.tsx` / `*EditScreen.tsx` 等）の最外殻。

---

## 実装

```tsx
// app/(shared)/components/ScreenWrapper.tsx
import { cn } from "@/app/(shared)/lib/utils"

type Props = {
  children: React.ReactNode
  /** 全体に半透明オーバーレイを被せる */
  isLoading?: boolean
  className?: string
}

/** 全 Screen の最外殻 */
export const ScreenWrapper = ({ children, isLoading, className }: Props) => (
  <div className={cn("relative max-w-screen-xl mx-auto p-4 md:p-6", className)}>
    {isLoading && (
      <div className="absolute inset-0 z-10 bg-background/60 backdrop-blur-sm" />
    )}
    {children}
  </div>
)
```

---

## 使い方

```tsx
'use client'
import { ScreenWrapper } from "@/app/(shared)/components/ScreenWrapper"

export const ResourceListScreen = () => (
  <ScreenWrapper>
    {/* 画面の中身 */}
  </ScreenWrapper>
)
```

mutation 実行中のオーバーレイ:

```tsx
<ScreenWrapper isLoading={isPending}>
  ...
</ScreenWrapper>
```

---

## ルール

- **全 Screen で必須**（List / View / Edit / New 等）
- `relative` + `max-w-screen-xl` で responsive な最大幅
- `isLoading` 時は半透明オーバーレイで操作不能化
- `className` で個別画面が padding 等を上書き可能

## なぜ必要

- 画面ごとに max-w / padding を書き直さないため
- mutation 中の disable UI を統一
- 画面の z-index 階層の基準

## 関連 references

- `frontend/components-catalog.md`
- `frontend/list-screen-tsx.md`, `frontend/view-screen-tsx.md`, `frontend/edit-screen-tsx.md`

## 禁止

- Screen で `<ScreenWrapper>` なし（直接 `<div>` で書く）
- `<ScreenWrapper>` を多重 wrap
- isLoading を mutation でない箇所で使う（Skeleton や loading.tsx を使う）
