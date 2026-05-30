# Next.js App Router — E2E Tests (Playwright)

> **Stack**: Playwright + Page Object Model + Fixtures。画面単位フォルダで構造化。

---

## セットアップ

```bash
pnpm add -D @playwright/test
pnpm playwright install --with-deps
```

```ts
// playwright.config.ts
import { defineConfig, devices } from "@playwright/test"

export default defineConfig({
  testDir: "./tests/e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ["list"],
    ["html", { open: "never" }],
  ],
  use: {
    baseURL: "http://localhost:3000",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
    { name: "webkit", use: { ...devices["Desktop Safari"] } },
    { name: "mobile-chrome", use: { ...devices["Pixel 7"] } },
  ],
  webServer: {
    command: "pnpm dev",
    url: "http://localhost:3000",
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
})
```

---

## フォルダ構成（再掲）

```
tests/
├── e2e/
│   ├── resources/             # 画面単位
│   │   ├── list.spec.ts
│   │   ├── create.spec.ts
│   │   ├── view.spec.ts
│   │   ├── edit.spec.ts
│   │   └── delete.spec.ts
│   ├── auth/
│   │   ├── login.spec.ts
│   │   └── signup.spec.ts
│   └── usecases/              # 複数画面横断
│       └── register-and-edit-flow.spec.ts
├── pages/                     # Page Object Model
│   ├── ResourceListPage.ts
│   ├── ResourceEditPage.ts
│   └── LoginPage.ts
├── fixtures/                  # データ生成
├── helpers/                   # 共通ヘルパー
└── global-setup.ts            # 全テスト前のセットアップ
```

---

## Page Object Model

```ts
// tests/pages/ResourceListPage.ts
import { Page, expect } from "@playwright/test"

export class ResourceListPage {
  constructor(public page: Page) {}

  async goto() {
    await this.page.goto("/resources")
    await expect(this.page).toHaveTitle(/リソース/)
  }

  async search(text: string) {
    await this.page.getByPlaceholder("名前で検索").fill(text)
  }

  async expectCount(count: number) {
    await expect(this.page.getByTestId("resource-card")).toHaveCount(count)
  }

  async openByName(name: string) {
    await this.page.getByRole("link", { name }).click()
  }

  async clickNew() {
    await this.page.getByRole("link", { name: "新規作成" }).click()
  }
}
```

```ts
// tests/pages/ResourceEditPage.ts
import { Page, expect } from "@playwright/test"

export class ResourceEditPage {
  constructor(public page: Page) {}

  async gotoNew() {
    await this.page.goto("/resources/new")
  }

  async gotoEdit(id: string) {
    await this.page.goto(`/resources/${id}/edit`)
  }

  async fillName(name: string) {
    await this.page.getByLabel("名前").fill(name)
  }

  async addTag(tag: string) {
    await this.page.getByPlaceholder("タグを追加...").fill(tag)
    await this.page.getByPlaceholder("タグを追加...").press("Enter")
  }

  async save() {
    await this.page.getByRole("button", { name: "保存" }).click()
    await expect(this.page.getByText("保存しました")).toBeVisible()
  }

  async delete() {
    await this.page.getByRole("button", { name: "削除" }).click()
    await this.page.getByRole("button", { name: "削除する" }).click()
  }
}
```

ロケータは role / label / placeholder ベース（a11y フレンドリー）。`data-testid` は最後の手段。

---

## ユースケース別テスト

```ts
// tests/e2e/resources/create.spec.ts
import { test, expect } from "@playwright/test"
import { ResourceListPage } from "@/tests/pages/ResourceListPage"
import { ResourceEditPage } from "@/tests/pages/ResourceEditPage"
import { loginAsTestUser, cleanResources } from "@/tests/helpers"

test.describe("リソース新規作成", () => {
  test.beforeEach(async ({ page }) => {
    await loginAsTestUser(page)
    await cleanResources()
  })

  test("一覧から新規作成 → 詳細遷移", async ({ page }) => {
    const list = new ResourceListPage(page)
    const edit = new ResourceEditPage(page)

    await list.goto()
    await list.expectCount(0)

    await list.clickNew()
    await edit.fillName("マイリソース")
    await edit.addTag("テスト")
    await edit.save()

    // 詳細画面に遷移している
    await expect(page).toHaveURL(/\/resources\/[a-f0-9-]+$/)
    await expect(page.getByRole("heading", { name: "マイリソース" })).toBeVisible()
  })

  test("名前未入力でエラーが表示される", async ({ page }) => {
    const edit = new ResourceEditPage(page)
    await edit.gotoNew()
    await edit.save()           // 名前空のまま保存

    await expect(page.getByText("リソース名は必須です")).toBeVisible()
  })
})
```

---

## 横断ユースケース

```ts
// tests/e2e/usecases/register-and-edit-flow.spec.ts
import { test, expect } from "@playwright/test"

test("新規作成 → 編集 → 削除のフル CRUD", async ({ page }) => {
  await loginAsTestUser(page)

  // 1. 新規作成
  await page.goto("/resources/new")
  await page.getByLabel("名前").fill("CRUD テスト")
  await page.getByRole("button", { name: "保存" }).click()

  const url = page.url()
  const id = url.split("/").pop()
  expect(id).toBeTruthy()

  // 2. 編集
  await page.goto(`/resources/${id}/edit`)
  await page.getByLabel("名前").fill("CRUD 編集後")
  await page.getByRole("button", { name: "保存" }).click()
  await expect(page.getByText("更新しました")).toBeVisible()

  // 3. View 確認
  await page.goto(`/resources/${id}`)
  await expect(page.getByRole("heading", { name: "CRUD 編集後" })).toBeVisible()

  // 4. 削除
  await page.getByRole("button", { name: "編集" }).click()
  await page.getByRole("button", { name: "削除" }).click()
  await page.getByRole("button", { name: "削除する" }).click()
  await expect(page.getByText("削除しました")).toBeVisible()
  await expect(page).toHaveURL("/resources")
})
```

---

## helpers

```ts
// tests/helpers/auth.ts
import { Page, BrowserContext } from "@playwright/test"

const TEST_USER = { email: "test@example.com", password: "test1234" }

export const loginAsTestUser = async (page: Page) => {
  // Storage State 戦略：事前にログイン済み state を保存しておく
  // ここでは UI 経由で簡易ログイン
  await page.goto("/login")
  await page.getByLabel("メール").fill(TEST_USER.email)
  await page.getByLabel("パスワード").fill(TEST_USER.password)
  await page.getByRole("button", { name: "ログイン" }).click()
  await page.waitForURL("/home")
}

export const cleanResources = async () => {
  // テスト用 API or DB 直接で削除
  await fetch("http://localhost:3000/api/v1/test/clean-resources", { method: "POST" })
}
```

### Storage State で高速化

```ts
// global-setup.ts
import { chromium, FullConfig } from "@playwright/test"

export default async (config: FullConfig) => {
  const browser = await chromium.launch()
  const ctx = await browser.newContext()
  const page = await ctx.newPage()
  await page.goto("http://localhost:3000/login")
  await page.getByLabel("メール").fill("test@example.com")
  await page.getByLabel("パスワード").fill("test1234")
  await page.getByRole("button", { name: "ログイン" }).click()
  await page.waitForURL("/home")
  await ctx.storageState({ path: "tests/.auth/user.json" })
  await browser.close()
}
```

```ts
// playwright.config.ts に
projects: [
  {
    name: "chromium",
    use: { ...devices["Desktop Chrome"], storageState: "tests/.auth/user.json" },
  },
],
globalSetup: "./tests/global-setup.ts",
```

各 test がログイン処理を繰り返さず高速化。

---

## DB シード

```ts
// tests/fixtures/resource.ts
import { db } from "@/drizzle/db"
import { resources } from "@/drizzle/schema"

export const seedResource = async (overrides?: Partial<typeof resources.$inferInsert>) => {
  const [row] = await db.insert(resources).values({
    name: "テスト",
    isPublic: false,
    ...overrides,
  }).returning()
  return row
}

export const cleanResources = async () => {
  await db.delete(resources)
}
```

DB を直接シード → API 経由よりも高速・確実。

---

## 失敗時のデバッグ

```bash
# UI モードで対話実行
pnpm playwright test --ui

# デバッグ（DevTools 起動）
pnpm playwright test --debug tests/e2e/resources/list.spec.ts

# Trace を見る
pnpm playwright show-trace test-results/.../trace.zip
```

`trace: "on-first-retry"` で失敗時に自動取得。

---

## 並列・分離

- `fullyParallel: true` でファイル単位の並列
- DB 状態を共有するテストは `test.serial` で直列化
- ユーザーごとに別 storageState を持つこともできる

---

## 視覚回帰テスト

```ts
await expect(page).toHaveScreenshot("resource-list.png", { maxDiffPixels: 100 })
```

Playwright が初回でスクショ保存、次回以降は diff 比較。UI 変更時に意図しないリグレッションを検知。

---

## アクセシビリティテスト

```bash
pnpm add -D @axe-core/playwright
```

```ts
import AxeBuilder from "@axe-core/playwright"

test("ListScreen は a11y 違反なし", async ({ page }) => {
  await page.goto("/resources")
  const results = await new AxeBuilder({ page }).analyze()
  expect(results.violations).toEqual([])
})
```

a11y を CI で検証できる（QA-065 では a11y は不要としたが、テストでチェックするのは無害）。

---

## Constraints

- 画面単位フォルダ + ユースケース別ファイル
- セレクタは Page Object に集約
- ロケータは `getByRole` / `getByLabel` / `getByText` 優先（`testid` は最後の手段）
- ログインは storage state で高速化
- DB シードは fixtures で集約
- 視覚回帰・a11y は必要に応じて
- `trace: "on-first-retry"` で失敗デバッグを容易に
- 並列実行を前提に test 間で state を共有しない
- CUJ（クリティカルパス）は必ず E2E でカバー
