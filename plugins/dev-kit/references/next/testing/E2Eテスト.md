# Next.js App Router — E2E Tests (Playwright)

> **Stack**: Playwright + Page Object Model + Fixtures。ユースケース駆動設計で構造化。

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
  testDir: "./e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ["list"],
    ["html", { open: "never", outputFolder: "e2e/reports" }],
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

## フォルダ構成

```
e2e/
├── scenarios/              # ユースケース単位（ドメイン分類）
│   ├── auth/
│   │   ├── login.spec.ts
│   │   └── signup.spec.ts
│   ├── checkout/
│   │   ├── apply-coupon.spec.ts
│   │   └── complete-purchase.spec.ts
│   └── account/
│       └── update-profile.spec.ts
├── pages/                  # Page Object Model
│   ├── LoginPage.ts
│   ├── CartPage.ts
│   └── DashboardPage.ts
├── fixtures/               # テスト前提条件・共通前処理
│   ├── auth.ts
│   └── test.ts
├── utils/                  # ドメイン別共通処理
│   ├── db.ts
│   ├── mail.ts
│   └── factories.ts
├── data/                   # 固定テストデータ
│   ├── users.ts
│   ├── products.ts
│   └── coupons.ts
├── snapshots/              # visual regression 用比較画像
├── reports/                # CI レポート出力先
├── global.setup.ts         # 認証 state 生成・DB 初期化
├── global.teardown.ts      # テスト後の後片付け
└── playwright.config.ts
```

---

## 各フォルダの責務

### scenarios/（中核）

ユーザーの行動単位でテストを配置する。技術的な分類（画面名）ではなくドメイン分類。

```
scenarios/auth/login.spec.ts
scenarios/checkout/apply-coupon.spec.ts
```

spec ファイルのみを置く。UI 操作の詳細は pages/ に委譲する。

### pages/（Page Object）

UI 操作の抽象化レイヤー。メソッドは「操作単位」に留め、業務ロジックは持たせない。

### fixtures/（テスト前提条件）

ログイン済み状態などの共通前処理。storageState 生成や API 準備を集約してspecをスリムにする。

### utils/（共通処理）

DB 操作・メール取得・外部サービス（Stripe 等）連携・テストデータ生成（factory）。
`helper.ts` 乱立は避け、責務ごとにファイルを分割する。

### data/（固定データ）

テスト用の固定値（ユーザー・商品・クーポンなど）。動的生成は `utils/factories.ts` へ。

```ts
// e2e/data/users.ts
export const TEST_USER = {
  email: "test@example.com",
  password: "password",
}
```

### global.setup.ts / global.teardown.ts

- setup：認証 state 生成・DB 初期化
- teardown：後片付け・データ削除

---

## 設計原則

1. **ユースケース中心** — 「ページ」ではなく「行動」で scenarios/ を分ける
2. **Page Object は薄く** — UI 操作のみ。業務フローを持たせない
3. **fixtures でテストを短くする** — login 処理の重複を排除
4. **utils はドメイン別に整理** — helper 地獄を防ぐ
5. **data は固定値専用** — 動的生成は factory へ

---

## 理想のテストイメージ

```ts
// e2e/scenarios/checkout/apply-coupon.spec.ts
import { test, expect } from "@playwright/test"
import { LoginPage } from "@/e2e/pages/LoginPage"
import { CartPage } from "@/e2e/pages/CartPage"
import { TEST_USER } from "@/e2e/data/users"

test("ユーザーがクーポンを適用して購入できる", async ({ page }) => {
  const loginPage = new LoginPage(page)
  const cartPage = new CartPage(page)

  await loginPage.login(TEST_USER.email, TEST_USER.password)
  await cartPage.applyCoupon("DISCOUNT10")
  await expect(page).toHaveURL("/checkout/complete")
})
```

テストが「読める仕様書」になる。

---

## Page Object Model

```ts
// e2e/pages/CartPage.ts
import { Page, expect } from "@playwright/test"

export class CartPage {
  constructor(public page: Page) {}

  async goto() {
    await this.page.goto("/cart")
  }

  async addItem(productId: string) {
    await this.page.getByTestId(`add-to-cart-${productId}`).click()
  }

  async applyCoupon(code: string) {
    await this.page.getByPlaceholder("クーポンコード").fill(code)
    await this.page.getByRole("button", { name: "適用" }).click()
    await expect(this.page.getByText("クーポンが適用されました")).toBeVisible()
  }

  async checkout() {
    await this.page.getByRole("button", { name: "購入する" }).click()
  }
}
```

```ts
// e2e/pages/LoginPage.ts
import { Page } from "@playwright/test"

export class LoginPage {
  constructor(public page: Page) {}

  async login(email: string, password: string) {
    await this.page.goto("/login")
    await this.page.getByLabel("メール").fill(email)
    await this.page.getByLabel("パスワード").fill(password)
    await this.page.getByRole("button", { name: "ログイン" }).click()
    await this.page.waitForURL("/home")
  }
}
```

ロケータは role / label / placeholder ベース（a11y フレンドリー）。`data-testid` は最後の手段。

---

## fixtures でログインをスリム化

```ts
// e2e/fixtures/auth.ts
import { test as base } from "@playwright/test"
import { LoginPage } from "@/e2e/pages/LoginPage"
import { TEST_USER } from "@/e2e/data/users"

export const test = base.extend<{ loggedIn: void }>({
  loggedIn: async ({ page }, use) => {
    const loginPage = new LoginPage(page)
    await loginPage.login(TEST_USER.email, TEST_USER.password)
    await use()
  },
})
```

```ts
// e2e/scenarios/checkout/apply-coupon.spec.ts（fixtures 利用版）
import { test } from "@/e2e/fixtures/auth"
import { expect } from "@playwright/test"

test("クーポンを適用して購入できる", async ({ page, loggedIn }) => {
  await page.goto("/cart")
  await page.getByPlaceholder("クーポンコード").fill("DISCOUNT10")
  await page.getByRole("button", { name: "適用" }).click()
  await expect(page).toHaveURL("/checkout/complete")
})
```

---

## Storage State で高速化

```ts
// e2e/global.setup.ts
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
  await ctx.storageState({ path: "e2e/.auth/user.json" })
  await browser.close()
}
```

```ts
// playwright.config.ts に
projects: [
  {
    name: "chromium",
    use: { ...devices["Desktop Chrome"], storageState: "e2e/.auth/user.json" },
  },
],
globalSetup: "./e2e/global.setup.ts",
globalTeardown: "./e2e/global.teardown.ts",
```

各 test がログイン処理を繰り返さず高速化。

---

## DB シード（utils/）

```ts
// e2e/utils/db.ts
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
pnpm playwright test --debug e2e/scenarios/auth/login.spec.ts

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
await expect(page).toHaveScreenshot("cart-page.png", { maxDiffPixels: 100 })
```

スクショは `e2e/snapshots/` に保存。Playwright が初回で生成し、次回以降は diff 比較。

---

## アクセシビリティテスト

```bash
pnpm add -D @axe-core/playwright
```

```ts
import AxeBuilder from "@axe-core/playwright"

test("カートページは a11y 違反なし", async ({ page }) => {
  await page.goto("/cart")
  const results = await new AxeBuilder({ page }).analyze()
  expect(results.violations).toEqual([])
})
```

---

## Constraints

- `e2e/scenarios/` にユースケース単位でスペックを配置（画面名でなくドメイン分類）
- Page Object は UI 操作の抽象化のみ。業務フローを持たせない
- ロケータは `getByRole` / `getByLabel` / `getByText` 優先（`testid` は最後の手段）
- ログインは storage state で高速化
- DB シードは `utils/db.ts` に集約
- `utils/` は `helper.ts` 乱立を避けドメイン別にファイルを分割
- `data/` は固定値のみ。動的生成は `utils/factories.ts` へ
- 視覚回帰・a11y は必要に応じて
- `trace: "on-first-retry"` で失敗デバッグを容易に
- 並列実行を前提に test 間で state を共有しない
- CUJ（クリティカルパス）は必ず E2E でカバー
