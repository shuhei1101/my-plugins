<!-- This file is a Japanese mirror of unit.md. When updating the English original, update this file too. -->
# Next.js App Router — Unit & Component Tests

> **Stack**: Vitest + Testing Library + MSW（任意）。

---

## セットアップ

```bash
pnpm add -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom @vitejs/plugin-react
```

```ts
// vitest.config.ts
import { defineConfig } from "vitest/config"
import react from "@vitejs/plugin-react"
import path from "path"

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: { "@": path.resolve(__dirname, ".") },
  },
  test: {
    environment: "jsdom",
    setupFiles: ["./tests/setup.ts"],
    globals: true,
    coverage: {
      provider: "v8",
      reporter: ["text", "html"],
      include: ["app/**/*.{ts,tsx}"],
      exclude: ["**/*.test.{ts,tsx}", "**/page.tsx", "**/layout.tsx"],
    },
  },
})
```

```ts
// tests/setup.ts
import "@testing-library/jest-dom/vitest"
```

---

## Schema テスト

```ts
// tests/unit/schema/resource-form.test.ts
import { describe, it, expect } from "vitest"
import { ResourceFormSchema } from "@/app/(authenticated)/resources/form"

describe("ResourceFormSchema", () => {
  it("有効な値をパースできる", () => {
    const result = ResourceFormSchema.safeParse({
      name: "テスト",
      tags: ["a"],
      iconId: 1,
      iconColor: "#000",
      categoryId: null,
      isPublic: false,
    })
    expect(result.success).toBe(true)
  })

  it("名前が空だとエラー", () => {
    const result = ResourceFormSchema.safeParse({ name: "", tags: [], iconId: 1, iconColor: "#000", categoryId: null, isPublic: false })
    expect(result.success).toBe(false)
    if (!result.success) expect(result.error.issues[0].path).toEqual(["name"])
  })

  it("タグが 10 件を超えるとエラー", () => {
    const result = ResourceFormSchema.safeParse({
      name: "x",
      tags: Array(11).fill("t"),
      iconId: 1,
      iconColor: "#000",
      categoryId: null,
      isPublic: false,
    })
    expect(result.success).toBe(false)
  })
})
```

---

## Pure function テスト

```ts
// tests/unit/utils/format.test.ts
import { describe, it, expect } from "vitest"
import { formatDate } from "@/app/(shared)/lib/format"

describe("formatDate", () => {
  it("ISO 文字列を日本語表記に変換", () => {
    expect(formatDate("2026-05-27T00:00:00Z")).toBe("2026年5月27日")
  })
})
```

---

## Component テスト

shadcn/ui ベースのコンポーネントを Testing Library で:

```tsx
// tests/components/TagInput.test.tsx
import { describe, it, expect, vi } from "vitest"
import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { TagInput } from "@/app/(shared)/components/TagInput"

describe("TagInput", () => {
  it("Enter でタグを追加できる", async () => {
    const onChange = vi.fn()
    render(<TagInput value={[]} onChange={onChange} />)

    const input = screen.getByRole("textbox")
    await userEvent.type(input, "新規{Enter}")

    expect(onChange).toHaveBeenCalledWith(["新規"])
  })

  it("IME 入力中の Enter は無視", async () => {
    const onChange = vi.fn()
    render(<TagInput value={[]} onChange={onChange} />)

    const input = screen.getByRole("textbox")
    await userEvent.type(input, "あ", { skipClick: true })
    // composition start を発火
    input.dispatchEvent(new CompositionEvent("compositionstart"))
    await userEvent.type(input, "{Enter}")

    expect(onChange).not.toHaveBeenCalled()
  })

  it("バッジクリックで削除", async () => {
    const onChange = vi.fn()
    render(<TagInput value={["既存"]} onChange={onChange} />)

    await userEvent.click(screen.getByRole("button"))
    expect(onChange).toHaveBeenCalledWith([])
  })
})
```

---

## Hook テスト

```tsx
// tests/unit/hooks/useDebouncedValue.test.tsx
import { describe, it, expect } from "vitest"
import { renderHook, waitFor } from "@testing-library/react"
import { useDebouncedValue } from "@/app/(shared)/hooks/useDebouncedValue"

describe("useDebouncedValue", () => {
  it("debounce 後に値が更新される", async () => {
    const { result, rerender } = renderHook(({ v }) => useDebouncedValue(v, 100), {
      initialProps: { v: "a" },
    })

    expect(result.current).toBe("a")
    rerender({ v: "b" })
    expect(result.current).toBe("a")          // まだ更新されない
    await waitFor(() => expect(result.current).toBe("b"), { timeout: 200 })
  })
})
```

---

## service.ts の integration テスト

DB（または testcontainers）を使う:

```ts
// tests/unit/service/resource.test.ts
import { describe, it, expect, beforeEach } from "vitest"
import { registerResource, editResource } from "@/app/api/v1/resources/service"
import { db } from "@/drizzle/db"
import { resources } from "@/drizzle/schema"

const TEST_USER = "00000000-0000-0000-0000-000000000001"

describe("resource service", () => {
  beforeEach(async () => {
    await db.delete(resources)
  })

  it("登録できる", async () => {
    const { id } = await registerResource({ db, userId: TEST_USER, form: {
      name: "テスト",
      tags: [],
      iconId: 1,
      iconColor: "#000",
      categoryId: null,
      isPublic: false,
    }})
    expect(id).toBeDefined()

    const row = await db.query.resources.findFirst({ where: (r, { eq }) => eq(r.id, id) })
    expect(row?.name).toBe("テスト")
  })

  it("楽観的ロック競合で更新失敗", async () => {
    // 古い updatedAt を渡すと VersionConflictError
    await expect(editResource({
      db, userId: TEST_USER, id: "...", form: {...}, updatedAt: "2020-01-01T00:00:00Z",
    })).rejects.toThrow("他のユーザーによって更新されています")
  })
})
```

DB は **test 用に別 schema / branch** を使う（dev / prod と分離）。Drizzle の transaction で rollback する手もあり:

```ts
beforeEach(async () => {
  // 各テストでロールバックする方式（Vitest concurrent と相性悪い）
})
```

testcontainers を使うとさらに分離が綺麗:

```ts
// testcontainers セットアップ（複雑なら避ける）
import { PostgreSqlContainer } from "@testcontainers/postgresql"
```

---

## MSW（任意）

クライアント側で API モックする場合:

```ts
// tests/helpers/server.ts
import { setupServer } from "msw/node"
import { http, HttpResponse } from "msw"

export const server = setupServer(
  http.get("/api/v1/resources", () => HttpResponse.json({ data: [], meta: { totalRecords: 0, page: 1, pageSize: 20 } })),
  http.post("/api/v1/resources", () => HttpResponse.json({ data: { id: "abc" } }, { status: 201 })),
)
```

```ts
// tests/setup.ts
import { server } from "./helpers/server"

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

詳細: `devtools/mock.md`

---

## テスト命名

- `describe("対象")` でグルーピング
- `it("○○できる")` `it("○○のときエラー")` で振る舞いを記述
- 否定形は `it("○○できない")` `it("○○のとき何もしない")`

---

## アンチパターン

- 実装の詳細を test に書く（refactor 耐性なし）→ 振る舞いをテスト
- 1 テストで多くを検証 → 1 つの振る舞いに集中
- mock しすぎて意味のない test → integration を増やす
- `screen.getByTestId("xxx")` を多用 → `getByRole` / `getByText` で a11y 親和的に
- `await sleep(1000)` → `waitFor` / `findBy*` に

---

## Constraints

- Vitest を使う（Jest との互換性高、`describe / it / expect`）
- Component は `@testing-library/react` + `userEvent`
- セレクタは `getByRole` / `getByText` / `getByLabelText` 優先（テストID 多用しない）
- service.ts は実 DB or testcontainers でテスト
- Schema は 100% カバー
- 非同期は `waitFor` / `findBy*`（hardcoded sleep 禁止）
- 各テストは独立（grobal state を残さない）
- カバレッジ計測は `vitest run --coverage`
