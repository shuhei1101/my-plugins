# Next.js App Router — Testing Strategy

> **方針**: ユースケース志向 + 画面単位のフォルダ構造。共通化と保守性を重視し、ベタ書きを避ける。
> **Stack**: Vitest（Unit）+ Playwright（E2E）+ Testing Library + MSW（任意）。

---

## テストレベル

| Level | Tool | 目的 | 比率目安 |
|---|---|---|---|
| **Unit** | Vitest | 純粋関数・スキーマ・小さい util | 多 |
| **Component** | Vitest + Testing Library | コンポーネントの描画・インタラクション | 中 |
| **Integration** | Vitest | service / db / API の組み合わせ（実 DB or testcontainers） | 中 |
| **E2E** | Playwright | ブラウザでの全機能フロー | 少（クリティカルパスのみ） |

E2E ですべてカバーするのではなく、ユニットで網羅・E2E で重要フローを確認するピラミッド構造。

---

## フォルダ構成（PR135 で標準化）

```
packages/web/
├── tests/
│   ├── unit/                       # 単体テスト
│   │   ├── schema/
│   │   │   └── resource-form.test.ts
│   │   ├── service/
│   │   │   └── resource.test.ts
│   │   └── utils/
│   ├── components/                 # コンポーネントテスト
│   │   ├── TagInput.test.tsx
│   │   └── PageHeader.test.tsx
│   ├── e2e/                        # E2E（画面単位フォルダ）
│   │   ├── resources/
│   │   │   ├── list.spec.ts
│   │   │   ├── create.spec.ts
│   │   │   ├── view.spec.ts
│   │   │   ├── edit.spec.ts
│   │   │   └── delete.spec.ts
│   │   ├── auth/
│   │   │   ├── login.spec.ts
│   │   │   └── signup.spec.ts
│   │   └── usecases/               # 横断ユースケース
│   │       └── register-and-edit.spec.ts
│   ├── pages/                      # Page Object Model
│   │   ├── ResourceListPage.ts
│   │   ├── ResourceEditPage.ts
│   │   └── LoginPage.ts
│   ├── fixtures/                   # テストデータ Factory
│   │   ├── resource.ts
│   │   ├── user.ts
│   │   └── index.ts
│   └── helpers/
│       ├── db.ts                   # テスト用 DB ヘルパー
│       ├── auth.ts                 # ログイン済み状態を作る
│       └── server.ts               # MSW handlers
├── vitest.config.ts
└── playwright.config.ts
```

**画面単位でテストフォルダ**を切り、その下にユースケース別ファイル。Page Object Model でロケータと操作を共通化、Fixtures でデータ生成を共通化。

---

## 設計原則

### 1. 画面単位フォルダ + ユースケース別ファイル

```
tests/e2e/resources/
├── list.spec.ts      # 一覧画面の操作（検索・ソート・ページング）
├── create.spec.ts    # 新規作成フロー
├── view.spec.ts      # 詳細閲覧
├── edit.spec.ts      # 編集フロー
└── delete.spec.ts    # 削除フロー
```

### 2. Page Object Model

ロケータと操作を 1 ファイルにまとめ、テストは「何を確認するか」に集中:

```ts
// tests/pages/ResourceListPage.ts
import { Page } from "@playwright/test"

export class ResourceListPage {
  constructor(private page: Page) {}

  async goto() { await this.page.goto("/resources") }

  async search(text: string) {
    await this.page.getByPlaceholder("名前で検索").fill(text)
  }

  async filterByTag(tag: string) { /* ... */ }

  async clickCard(name: string) {
    await this.page.getByRole("link", { name }).click()
  }

  async expectEmptyState() {
    await this.page.getByText("該当するリソースがありません").waitFor()
  }
}
```

テスト本体:

```ts
// tests/e2e/resources/list.spec.ts
import { test, expect } from "@playwright/test"
import { ResourceListPage } from "@/tests/pages/ResourceListPage"
import { loginAsTestUser } from "@/tests/helpers/auth"
import { seedResources } from "@/tests/fixtures/resource"

test.describe("リソース一覧", () => {
  test.beforeEach(async ({ page }) => {
    await loginAsTestUser(page)
    await seedResources(5)
  })

  test("一覧に 5 件表示される", async ({ page }) => {
    const listPage = new ResourceListPage(page)
    await listPage.goto()
    await expect(page.getByRole("link")).toHaveCount(5)
  })

  test("検索で絞り込める", async ({ page }) => {
    const listPage = new ResourceListPage(page)
    await listPage.goto()
    await listPage.search("テスト")
    await expect(page.getByRole("link")).toHaveCount(1)
  })
})
```

### 3. Fixtures（テストデータ Factory）

```ts
// tests/fixtures/resource.ts
import { db } from "@/drizzle/db"
import { resources, ResourceInsert } from "@/drizzle/schema"

export const createResourceFixture = (overrides?: Partial<ResourceInsert>): ResourceInsert => ({
  name: "テストリソース",
  isPublic: false,
  categoryId: null,
  ...overrides,
})

export const seedResources = async (count: number) => {
  const records = Array.from({ length: count }).map((_, i) =>
    createResourceFixture({ name: `テストリソース ${i + 1}` })
  )
  await db.insert(resources).values(records)
}

export const clearResources = async () => {
  await db.delete(resources)
}
```

### 4. ヘルパーで共通化

```ts
// tests/helpers/auth.ts
import { Page } from "@playwright/test"

export const loginAsTestUser = async (page: Page) => {
  await page.context().addCookies([
    { name: "session_token", value: TEST_SESSION_TOKEN, domain: "localhost", path: "/" },
  ])
}
```

---

## カバレッジ目標

| Type | 目標 |
|---|---|
| **クリティカルパス（CUJ）** | 100% E2E カバー |
| **Zod schema** | 100% Unit |
| **service.ts**（業務ロジック） | 80%+ Integration |
| **db.ts / query.ts** | 60%+ Integration（複雑なクエリのみ） |
| **共通コンポーネント** | 60%+ Component |
| **画面コンポーネント** | E2E でカバー（個別 Component test は最小限） |

---

## CUJ（Critical User Journey）の定義

ユーザーが価値を得るための一連のフロー:

1. **新規登録 → ログイン**
2. **リソース作成 → 一覧表示 → 詳細閲覧 → 編集 → 削除**
3. **検索・フィルタ・ソート**
4. **権限ガード（権限なしユーザーが編集 URL に直アクセス → 弾かれる）**
5. **エラーハンドリング（ネットワーク失敗時の UI）**

これらは E2E で必ずカバー。

---

## 実行コマンド

```bash
# Unit / Component
pnpm vitest                    # watch
pnpm vitest run                # 1 回
pnpm vitest run --coverage     # カバレッジ

# E2E
pnpm playwright test                          # 全部
pnpm playwright test tests/e2e/resources      # 画面単位
pnpm playwright test --ui                     # GUI で対話実行
pnpm playwright codegen http://localhost:3000  # ロケータ自動生成
```

---

## CI 統合

```yaml
# .github/workflows/test.yml（参考）
- run: pnpm vitest run --coverage
- run: pnpm playwright install --with-deps
- run: pnpm playwright test
```

詳細: `devops/deploy.md`（CI を書く場合）。PR135 では CI は不採用。

---

## テストの保守性

- **テスト名は「何を確認するか」** を明確に（`"検索で絞り込める"` ◎、`"テスト 1"` ✗）
- **`describe` で画面・機能を分け**、`test.beforeEach` で前提条件を共通化
- **Page Object** にセレクタを集約 — UI 変更時の修正箇所が 1 つに
- **Fixtures** でデータを共通化 — DB シードを宣言的に
- **flaky test を直す** — wait をハードコードせず `waitFor` を使う
- **DB は test 間でリセット**（`beforeEach` で truncate or rollback）
- **mock は最小限** — 本物の DB / API を使うのが理想（testcontainers 等）

---

## アンチパターン

- 1 テストに 100 行のセレクタ・操作をベタ書き → Page Object に切り出す
- 大量の `sleep(1000)` → `waitFor` / `expect.toBeVisible()` に
- 同じセットアップを各 test で繰り返す → `beforeEach`
- E2E でユニットレベルのことをテスト → unit に降ろす
- mock しすぎて実装の振る舞いをテストできていない → integration に切り替え

---

## Constraints

- フォルダ構成は `tests/{unit,components,e2e,pages,fixtures,helpers}/`
- E2E は **画面単位フォルダ + ユースケース別ファイル**（PR135）
- セレクタは Page Object に集約
- データ生成は Fixtures Factory に集約
- 共通操作（ログイン・シード等）は helpers に
- E2E はクリティカルパスを優先、ユニットで網羅
- カバレッジは Schema 100%, service 80%, db 60%, components 60% を目標
- flaky test 禁止（必ず `waitFor` / `expect.toXxx`）
- CI はオプション（PR135 では不採用、必要になったら追加）
