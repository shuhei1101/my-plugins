# app/api/v1/{resource}/dbHelper.ts

リソース内で複数の `query.ts` / `db.ts` 関数から共通利用するヘルパー。

---

## 必須テンプレ

```ts
/** ページング計算 */
export const calculatePagination = ({ page, pageSize }: { page: number; pageSize: number }) => ({
  offset: (page - 1) * pageSize,
  limit: pageSize,
})

/** リソース全体に共通する WHERE 条件 */
export const buildResourceVisibilityCondition = (userId: string) => {
  // 例: 公開フラグ or 自分のリソース
  return or(eq(resources.isPublic, true), eq(resources.createdBy, userId))
}
```

---

## ルール

- **リソース内に閉じる共通処理だけ**を置く
- 複数リソース横断で使うものは **`app/(shared)/lib/`** に格上げ（`app/(shared)/lib/pagination.ts` 等）
- 純粋関数を優先（テストしやすい）
- DB 接続を取らない（受け取る側で扱う）

## 何を置くか

| 置く | 置かない |
|---|---|
| ページング計算 | 複数リソースで使う計算（→ `(shared)/lib/`） |
| リソース固有の WHERE ビルダ | 汎用 WHERE ビルダ |
| リソース固有のソート定義 | 共通ソート（→ `(shared)/lib/`） |
| 結果整形のための共通ロジック | データ取得そのもの（→ `query.ts`） |

## ファイルを作るかどうか

- 共通ヘルパーが **0 個** ならファイル不要
- **1 個** だけならまず `query.ts` 内に書いてみる
- **2 個以上** なら `dbHelper.ts` に切り出す

## 関連 references

- `query-ts.md`, `db-ts.md`
