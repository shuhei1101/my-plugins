---
name: dev-kit:next-plan
description: |
  Next.js App Router のプロジェクト・機能・APIリソースの実装計画書を生成する。
  dev-kit Next.js references を読み込み、ファイルツリー・各ファイルの役割・規約ポイント・
  実装順序を含む構造化された計画書を出力する（実際のコードは書かない）。
  「設計を考えて」「何のファイルが必要か」「計画を立てて」「構成を教えて」
  「feature を追加したい」「API を追加したい」「新規プロジェクトを作りたい」
  または `/dev-kit:next-plan` の明示的な呼び出し時にトリガー。
  実装タスクには使用しない — 代わりに `dev-kit:next-implement` を使う。
---
<!-- This file is a Japanese mirror of SKILL.md. When updating the English original, update this file too. -->

# dev-kit:next-plan — 実装計画書ジェネレーター

dev-kit Next.js references を読み込み、新規プロジェクト・機能・APIリソースの
構造化された計画書を出力する（実際のコードは書かない）。

---

## 概要

このスキルは「X を作りたい」と「X の実装を開始する」の間のギャップを埋める。
関連する references を読み込み、ファイルが作成される前にユーザーがレビューできる計画書を出力する。

**このスキル1つでカバーするユースケース**:
1. **新規プロジェクト** — 完全な初期スキャフォールド（アプリ構造・認証・DB・共通ユーティリティ）
2. **新規フィーチャ** — CRUDフィーチャの追加（一覧/詳細/作成/編集画面 + Server Actions + API）
3. **新規APIリソース** — `app/api/v1/{resource}/` の追加（route / client / service / db / query / dbHelper）

---

## タスク

### ステップ 1: リクエストを理解する

#### 条件

- 常に — 最初に実行

#### 処理

1. ユーザーが作りたいものを特定:
   - **リソース/フィーチャ名**（例: `users`, `products`, `orders`）
   - **必要な操作**（list / view / create / edit / delete — またはその一部）
   - **必要なインターフェース**（画面のみ / APIのみ / 両方）
2. 以下のいずれかに分類:
   - `new-project` — ゼロから開始（既存のNext.jsプロジェクトなし）
   - `new-feature` — 既存プロジェクトへの完全なCRUDフィーチャ追加
   - `new-api` — APIリソースのみ追加（画面なし）
   - `new-screens` — 画面のみ追加（APIは既存）
3. 分類が曖昧な場合は、続行前にユーザーに確認する

→ ステップ 2 へ

#### 出力

- リソース名・必要な操作・インターフェースタイプ・分類が確定

---

### ステップ 2: references を読み込む

#### 条件

- Step 1 完了

#### 処理

`{plugin_root}/references/` から以下を読み込む（plugin_root はこのスキルファイルから2レベル上）:

**常に**:
- `frontend/feature-folder.md`
- `frontend/route-groups.md`
- `frontend/app-folder-overview.md`

**`new-feature` または `new-screens`**（必要な操作に基づく）:

| 操作 | Reference |
|---|---|
| 一覧画面 | `frontend/list-page-tsx.md`, `frontend/list-screen-tsx.md` |
| 詳細画面 | `frontend/view-page-tsx.md`, `frontend/view-screen-tsx.md` |
| 新規作成画面 | `frontend/edit-page-tsx.md`, `frontend/edit-screen-tsx.md` |
| 編集画面 | `frontend/edit-page-tsx.md`, `frontend/edit-screen-tsx.md` |
| フォーム処理 | `frontend/form-ts.md`, `frontend/use-form-pattern.md` |
| Server Actions | `backend/actions-ts.md`, `shared/error-action-handler.md` |

**`new-feature` または `new-api`**:
- `backend/api-folder-overview.md`
- `backend/route-ts.md`
- `backend/client-ts.md`
- `backend/service-ts.md`
- `backend/db-ts.md`
- `backend/query-ts.md`
- `backend/db-helper-ts.md`

**`new-project`**（上記すべて、さらに）:
- `shared/environment.md`
- `shared/error-classes.md`
- `shared/logger-impl.md`
- `backend/auth-setup.md`
- `backend/db-id.md`
- `backend/db-timestamps.md`
- `backend/db-relations.md`
- `frontend/endpoints.md`
- `frontend/query-client-setup.md`

→ ステップ 3 へ

#### 出力

- 関連するすべての references が読み込まれた状態

---

### ステップ 3: ファイル構造を設計する

#### 条件

- Step 2 完了

#### 処理

読み込んだ references とユーザーのリクエストに基づいて:

1. 作成が必要なファイルの完全なリストを決定
2. 各ファイルについて記録:
   - 完全パス（`feature-folder.md` と `route-groups.md` に従う）
   - 役割 / 責務
   - 対応する reference から抜き出した主要な規約
3. ディレクトリツリーを構築

従うべき標準パス:

| ファイル種別 | パスパターン |
|---|---|
| 一覧ページ | `app/(authenticated)/{feature}/page.tsx` |
| 詳細ページ | `app/(authenticated)/{feature}/[id]/page.tsx` |
| 新規作成ページ | `app/(authenticated)/{feature}/new/page.tsx` |
| 編集ページ | `app/(authenticated)/{feature}/[id]/edit/page.tsx` |
| 一覧スクリーン | `app/(authenticated)/{feature}/{Feature}ListScreen.tsx` |
| 詳細スクリーン | `app/(authenticated)/{feature}/{Feature}ViewScreen.tsx` |
| 新規作成スクリーン | `app/(authenticated)/{feature}/{Feature}NewScreen.tsx` |
| 編集スクリーン | `app/(authenticated)/{feature}/{Feature}EditScreen.tsx` |
| フォームスキーマ | `app/(authenticated)/{feature}/form.ts` |
| Server Actions | `app/(authenticated)/{feature}/actions.ts` |
| APIルート | `app/api/v1/{resource}/route.ts` |
| APIクライアント | `app/api/v1/{resource}/client.ts` |
| サービス | `app/api/v1/{resource}/service.ts` |
| DB更新 | `app/api/v1/{resource}/db.ts` |
| DBクエリ | `app/api/v1/{resource}/query.ts` |
| DBヘルパー | `app/api/v1/{resource}/dbHelper.ts` |
| DBスキーマ | `drizzle/schema.ts`（既存を拡張） |

→ ステップ 4 へ

#### 出力

- パス・役割・規約が記録されたファイルの完全なリスト

---

### ステップ 4: 計画書を出力する

#### 条件

- Step 3 完了

#### 処理

以下の構造化された計画書をMarkdownで出力する:

```markdown
# 実装計画: {作るもの}

**Type**: {new-project | new-feature | new-api | new-screens}
**Created**: {YYYY-MM-DD}
**Resource**: `{リソース名}`
**Operations**: {必要な操作のリスト}

## ディレクトリツリー

\`\`\`
{├── / └── / │ を使ったディレクトリツリー}
\`\`\`

## ファイル一覧

| ファイル | 役割 | 参照 reference |
|---|---|---|
| {パス} | {役割} | `{referenceファイル}` |
...

## 各ファイルの実装ポイント

### `{file1}`

- **役割**: {1行での役割説明}
- **規約ポイント**:
  - {referenceから抜き出した主要な規約}
  - ...

### `{file2}`
...

## 実装順序（推奨）

1. DBスキーマ (`drizzle/schema.ts`) — 先にデータ構造を確定
2. API層 (query → db → dbHelper → service → route → client)
3. Server Actions (`actions.ts`) — フロント↔バック橋渡し
4. 画面 (page.tsx → Screen → form.ts) — 上位から下位へ

## 次のステップ

- この計画を確認後、`/dev-kit:next-implement` で実装を開始
- 各ファイル編集時にnext-references-injectionフックが自動でreferenceを注入
```

→ 完了

#### 出力

- 構造化された計画書が会話に出力された状態

#### 注意事項

##### 禁止事項

- このスキルでソースファイルを作成・編集してはならない — 計画のみ
- `/dev-kit:next-implement` を自動的に呼び出してはならない — ユーザーが計画をレビューしてから

---

## 参照

- `references/CLAUDE.md` — すべてのreferenceのファイル種別マッピング（インデックス）
- `references/injection_rules.yaml` — ファイルパスパターン → referenceマッピング
- `references/frontend/feature-folder.md` — フィーチャフォルダレイアウトと命名
- `references/frontend/route-groups.md` — `(authenticated)` / `(auth)` / `(shared)` ルートグループ
- `references/frontend/app-folder-overview.md` — アプリディレクトリ全体の構造
