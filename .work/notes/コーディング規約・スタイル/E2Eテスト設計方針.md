# E2Eテスト設計方針 — tests/e2e/ 統一構造

dev-kit の Next.js E2E テストリファレンスで採用するディレクトリ設計方針。

---

## 概要

E2E テストは `tests/` 共通構造に準拠し、`tests/e2e/` 以下に spec ファイルを配置する。
ユニットテスト（`tests/unit/`）・コンポーネントテスト（`tests/components/`）・
fixtures（`tests/fixtures/`）・helpers（`tests/helpers/`）との一貫性を最優先とする。

---

## ディレクトリ構成

```
tests/
├── e2e/                  # E2E spec files（画面・ドメイン単位フォルダ）
│   ├── auth/
│   ├── checkout/
│   ├── usecases/         # 横断ユースケース
│   ├── .auth/            # Storage State（.gitignore）
│   ├── global.setup.ts
│   └── global.teardown.ts
├── pages/                # Page Object Model
├── fixtures/             # テストデータ Factory
└── helpers/              # 共通操作（auth, db, server）
```

## 設計原則

1. **tests/ 統一** — unit / components / e2e / pages / fixtures / helpers を同じ `tests/` 下に置く
2. **画面・ドメイン単位フォルダ** — `tests/e2e/{screen}/` でスペックを整理
3. **Page Object は薄く** — UI 操作のみ。業務フローを持たせない
4. **helpers で共通化** — login 処理・DB シードは helpers に集約
5. **fixtures は固定値専用** — 動的生成は Factory（`フィクスチャー.md`）

## 変更履歴

| # | 日付 | 概要 |
|---|---|---|
| 1 | 2026-06-01 | 初版：ユースケース駆動設計（`e2e/scenarios/`）として作成 |
| 2 | 2026-06-01 | 方針変更：`tests/e2e/` 統一構造へ（テスト戦略.md との整合性優先） |
