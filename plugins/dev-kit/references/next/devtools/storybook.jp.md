<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# Next.js App Router — Storybook

> **目的**: shadcn/ui 拡張コンポーネントのカタログを可視化し、デザイン確認・テスト・ドキュメント化を一元化。
> **Stack**: Storybook 8.x + `@storybook/nextjs-vite` + Vitest 統合。

---

## セットアップ

```bash
pnpm dlx storybook@latest init
# Next.js プロジェクトとして自動セットアップ
```

```bash
pnpm storybook            # 開発サーバー
pnpm build-storybook      # 静的ビルド
```

設定:

```ts
// .storybook/main.ts
import type { StorybookConfig } from "@storybook/nextjs-vite"

const config: StorybookConfig = {
  stories: ["../app/**/*.stories.@(ts|tsx|mdx)", "../stories/**/*.stories.@(ts|tsx|mdx)"],
  addons: [
    "@storybook/addon-essentials",
    "@storybook/addon-interactions",
    "@storybook/addon-a11y",
    "@storybook/addon-themes",
    "@chromatic-com/storybook",
  ],
  framework: { name: "@storybook/nextjs-vite", options: {} },
  staticDirs: ["../public"],
}

export default config
```

```ts
// .storybook/preview.ts
import type { Preview } from "@storybook/react"
import "../app/globals.css"             // Tailwind / shadcn の global style
import { ThemeProvider } from "next-themes"

const preview: Preview = {
  parameters: {
    layout: "centered",
    backgrounds: {
      default: "light",
      values: [
        { name: "light", value: "#ffffff" },
        { name: "dark", value: "#0a0a0a" },
      ],
    },
  },
  decorators: [
    (Story) => (
      <ThemeProvider attribute="class" defaultTheme="light">
        <Story />
      </ThemeProvider>
    ),
  ],
}

export default preview
```

---

## Story の書き方

```tsx
// app/(shared)/components/PageHeader.stories.tsx
import type { Meta, StoryObj } from "@storybook/react"
import { PageHeader } from "./PageHeader"
import { Button } from "./ui/button"

const meta: Meta<typeof PageHeader> = {
  title: "Shared / PageHeader",
  component: PageHeader,
}

export default meta

type Story = StoryObj<typeof PageHeader>

export const Default: Story = {
  args: {
    title: "リソース一覧",
  },
}

export const WithActions: Story = {
  args: {
    title: "リソース一覧",
    description: "登録されたリソースを一覧表示します。",
    actions: <Button>新規作成</Button>,
  },
}

export const TitleOnly: Story = {
  args: {
    title: "シンプルタイトル",
  },
}
```

---

## 配置規約

- 共通コンポーネント（`app/(shared)/components/`）の `.stories.tsx` を **同じディレクトリ** に置く
- フィーチャ固有のコンポーネントは story 不要（E2E でカバー）
- 状態のあるコンポーネント（Dialog 等）は `play` 関数で操作

---

## Interaction tests（play 関数）

```tsx
// app/(shared)/components/TagInput.stories.tsx
import { expect, userEvent, within } from "@storybook/test"

export const TypeAndConfirm: Story = {
  args: { value: [], onChange: fn() },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement)
    const input = canvas.getByPlaceholderText("タグを追加...")
    await userEvent.type(input, "新規{Enter}")
    expect(input).toHaveValue("")
  },
}
```

Vitest と統合して CI で自動実行できる。

---

## アクセシビリティチェック

`addon-a11y` を入れると、各 Story で axe-core によるチェックが走り、違反が UI に表示される。

```ts
parameters: {
  a11y: {
    config: { rules: [{ id: "color-contrast", enabled: true }] },
  },
}
```

---

## ダーク・ライトテーマ

`addon-themes` で全 Story にテーマ切替トグルを追加:

```ts
// .storybook/preview.ts
import { withThemeByClassName } from "@storybook/addon-themes"

const preview: Preview = {
  decorators: [
    withThemeByClassName({
      themes: { light: "", dark: "dark" },
      defaultTheme: "light",
    }),
  ],
}
```

---

## Chromatic（視覚回帰）

`@chromatic-com/storybook` で各 Story を Chromatic にアップ → 視覚回帰テスト:

```bash
pnpm dlx chromatic --project-token=xxx
```

PR ごとに「以前の見た目との diff」が表示される。

---

## Story 命名規約

```
title: "{Category} / {ComponentName}"
```

| Category | 用途 |
|---|---|
| `Shared` | `app/(shared)/components/` のカスタム |
| `Shared / UI` | `app/(shared)/components/ui/` の shadcn コピー（必要なら） |
| `Patterns` | パターン例（List 画面風、Edit 画面風） |
| `Forms` | フォーム例 |
| `Pages` | ページ全体のスタブ（任意） |

```ts
const meta: Meta<typeof Button> = {
  title: "Shared / UI / Button",
  component: Button,
}
```

---

## CI で Storybook をビルド・テスト

```bash
pnpm build-storybook --quiet
pnpm test-storybook                 # play 関数を CI で実行
```

---

## アンチパターン

- 全コンポーネントに story → メンテ負荷増。`shared/` の再利用コンポーネントだけに絞る
- story が古くなる → コンポーネント変更時に同 PR で更新
- 過度に状態を持つ巨大 story → 小さい variant を複数に分割
- props 全部に control を付ける → 主要なものだけで OK

---

## Constraints

- 対象は `app/(shared)/components/` の再利用コンポーネント
- ファイル名は `*.stories.tsx`、同ディレクトリに配置
- story title は `{Category} / {ComponentName}`
- a11y / dark / interaction addon を入れる
- 主要 variant を `Default` + 数個のバリエーションで網羅
- インタラクションは `play` 関数で確認
- フィーチャ固有のコンポーネントは story 不要（E2E でカバー）
- 視覚回帰が必要なら Chromatic（任意）
