# E2Eテスト設計方針 — ユースケース駆動設計

dev-kit の Next.js E2E テストリファレンスで採用する設計方針。

---

## 概要

E2E テストは「画面単位フォルダ」ではなく「ユースケース駆動設計」で構成する。
テストが読める仕様書になることを最優先とし、CIで壊れにくい構造を目指す。

---

## ディレクトリ構成

```
e2e/
├── scenarios/    # ユースケース単位（ドメイン分類）
├── pages/        # Page Object Model
├── fixtures/     # テスト前提条件・共通前処理
├── utils/        # ドメイン別共通処理（db/mail/factories）
├── data/         # 固定テストデータ
├── snapshots/    # visual regression 用
├── reports/      # CI レポート
├── global.setup.ts
├── global.teardown.ts
└── playwright.config.ts
```

## 設計原則

1. **ユースケース中心** — 「ページ」ではなく「行動」で scenarios/ を分ける
2. **Page Object は薄く** — UI 操作のみ。業務フローを持たせない
3. **fixtures でテストを短くする** — login 処理の重複を排除
4. **utils はドメイン別に整理** — helper 地獄を防ぐ
5. **data は固定値専用** — 動的生成は factory へ

## 旧構成との対応

| 旧 | 新 | 変更点 |
|---|---|---|
| `tests/e2e/resources/` | `e2e/scenarios/{domain}/` | 画面名 → ユースケース名 |
| `tests/helpers/` | `e2e/utils/` | 責務ごとにファイル分割 |
| `tests/fixtures/` | `e2e/fixtures/` + `e2e/data/` | 前処理と固定値を分離 |
| `tests/global-setup.ts` | `e2e/global.setup.ts` + `e2e/global.teardown.ts` | teardown を追加 |

---

## 変更履歴

| # | 日付 | 概要 |
|---|---|---|
| 1 | 2026-06-01 | 初版作成（ユースケース駆動設計への更新） |
