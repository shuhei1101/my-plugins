---
paths:
  - "**/tests/e2e/**/*.spec.ts"
  - "**/tests/pages/**/*.ts"
  - "**/playwright.config.ts"
---
<!-- This file is a Japanese mirror of E2Eテスト.md. When updating the English original, update this file too. -->
# Next.js App Router — E2E Tests (Playwright)

> **Stack**: Playwright + Page Object Model。`tests/` 共通構造に準拠（テスト戦略.md）。

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
    ["html", { open: "never", outputFolder: "tests/e2e/reports" }],
  ],
  use: {
    baseURL: "http://localhost:3000",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"], storageState: "tests/e2e/.auth/user.json" },
    },
    {
      name: "webkit",
      use: { ...devices["Desktop Safari"], storageState: "tests/e2e/.auth/user.json" },
    },
    {
      name: "mobile-chrome",
      use: { ...devices["Pixel 7"], storageState: "tests/e2e/.auth/user.json" },
    },
  ],
  globalSetup: "./tests/e2e/global.setup.ts",
  globalTeardown: "./tests/e2e/global.teardown.ts",
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
tests/
├── e2e/                        # E2E spec files（画面・ドメイン単位フォルダ）
│   ├── auth/
│   │   ├── login.spec.ts
│   │   └── signup.spec.ts
│   ├── checkout/
│   │   ├── apply-coupon.spec.ts
│   │   └── complete-purchase.spec.ts
│   ├── account/
│   │   └── update-profile.spec.ts
│   ├── usecases/               # 横断ユースケース
│   │   └── register-and-purchase.spec.ts
│   ├── .auth/                  # Storage State（.gitignore 対象）
│   ├── reports/                # CI レポート出力先
│   ├── snapshots/              # visual regression 用比較画像
│   ├── global.setup.ts         # 認証 state 生成・DB 初期化
│   └── global.teardown.ts      # テスト後の後片付け
├── pages/                      # Page Object Model（E2E 専用）
│   ├── LoginPage.ts
│   ├── CartPage.ts
│   └── DashboardPage.ts
├── fixtures/                   # テストデータ Factory（→ フィクスチャー.md）
│   ├── user.ts
│   ├── resource.ts
│   └── index.ts
└── helpers/                    # 共通操作（→ テスト戦略.md）
    ├── auth.ts                 # ログイン済み状態を作る
    ├── db.ts                   # DB シード・クリーンアップ
    └── server.ts               # MSW handlers
```

---

## 各フォルダの責務

### tests/e2e/（スペックのみ）

画面・ドメイン単位でフォルダを切り、その下にユースケース別ファイルを置く。
ロケータや DB 操作は持たせない。

```
tests/e2e/checkout/
├── apply-coupon.spec.ts
└── complete-purchase.spec.ts
```

### tests/pages/（Page Object）

UI 操作の抽象化レイヤー。メソッドは「操作単位」に留め、業務ロジックは持たせない。

### tests/fixtures/（テストデータ）

固定値・Factory 関数を集約。詳細は `フィクスチャー.md` を参照。

### tests/helpers/（共通操作）

ログイン済み状態作成（`auth.ts`）・DB シード（`db.ts`）・MSW（`server.ts`）。
`helper.ts` 乱立は避け、責務ごとにファイルを分割する。

### tests/e2e/global.setup.ts / global.teardown.ts

- setup：Storage State 生成・DB 初期化
- teardown：後片付け・データ削除

---

## 設計原則

1. **画面・ドメイン単位フォルダ** — `tests/e2e/{screen}/` でフォルダを切る
2. **Page Object は薄く** — UI 操作のみ。業務フローを持たせない
3. **helpers でテストを短くする** — login 処理の重複を排除
4. **fixtures はドメイン別に整理** — helper 地獄を防ぐ
5. **tests/fixtures は固定値専用** — 動的生成は Factory へ

---

## 理想のテストイメージ

```ts
// tests/e2e/checkout/apply-coupon.spec.ts
import { test, expect } from "@playwright/test"
import { LoginPage } from "@/tests/pages/LoginPage"
import { CartPage } from "@/tests/pages/CartPage"
import { TEST_USER } from "@/tests/fixtures/user"

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
// tests/pages/CartPage.ts
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
// tests/pages/LoginPage.ts
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

## helpers でログインをスリム化

```ts
// tests/helpers/auth.ts
import { Page } from "@playwright/test"

export const loginAsTestUser = async (page: Page) => {
  await page.context().addCookies([
    { name: "session_token", value: TEST_SESSION_TOKEN, domain: "localhost", path: "/" },
  ])
}
```

```ts
// tests/e2e/checkout/apply-coupon.spec.ts（helpers 利用版）
import { test, expect } from "@playwright/test"
import { loginAsTestUser } from "@/tests/helpers/auth"

test("クーポンを適用して購入できる", async ({ page }) => {
  await loginAsTestUser(page)
  await page.goto("/cart")
  await page.getByPlaceholder("クーポンコード").fill("DISCOUNT10")
  await page.getByRole("button", { name: "適用" }).click()
  await expect(page).toHaveURL("/checkout/complete")
})
```

---

## Storage State で高速化

```ts
// tests/e2e/global.setup.ts
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
  await ctx.storageState({ path: "tests/e2e/.auth/user.json" })
  await browser.close()
}
```

各 test がログイン処理を繰り返さず高速化。`.auth/` は `.gitignore` に追加する。

---

## DB シード（helpers/）

```ts
// tests/helpers/db.ts
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
pnpm playwright test --debug tests/e2e/auth/login.spec.ts

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

スクショは `tests/e2e/snapshots/` に保存。Playwright が初回で生成し、次回以降は diff 比較。

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

- `tests/e2e/` に画面・ドメイン単位でスペックを配置
- Page Object は `tests/pages/` に集約（UI 操作の抽象化のみ）
- テストデータは `tests/fixtures/` に Factory パターンで集約（`フィクスチャー.md`）
- 共通操作（ログイン・シード等）は `tests/helpers/` に
- ロケータは `getByRole` / `getByLabel` / `getByText` 優先（`testid` は最後の手段）
- Storage State でログインを高速化（`tests/e2e/.auth/user.json`）
- `trace: "on-first-retry"` で失敗デバッグを容易に
- 並列実行を前提に test 間で state を共有しない
- CUJ（クリティカルパス）は必ず E2E でカバー
- 視覚回帰・a11y は必要に応じて
