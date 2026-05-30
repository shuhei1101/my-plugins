<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# app/ — フォルダ全体図

Next.js App Router プロジェクトの `app/` 配下の構成。**モノレポ前提**で通常は `packages/web/app/`。

---

## トップレベル

```
packages/web/app/
├── (authenticated)/   # 認証必須エリア — メイン画面群
├── (auth)/            # 認証画面（login / signup / reset-password）
├── (shared)/          # 共通コンポーネント・hook・provider・schema
├── api/v1/            # バージョニング済み API ルート
├── error/             # エラーページ（unauthorized 等）
├── layout.tsx         # ルートレイアウト
├── error.tsx          # ルートエラーバウンダリ
├── global-error.tsx   # ルート layout 自体のエラー
├── not-found.tsx      # 404
└── loading.tsx        # ルート suspense fallback
```

プロジェクト直下:

```
packages/web/
├── proxy.ts           # Next.js 16: 旧 middleware.ts
├── drizzle/           # DB スキーマ
├── tests/             # E2E / Unit テスト
├── config/
│   └── settings.yaml  # YAML 構造化設定
└── stories/           # Storybook 用（任意）
```

---

## 関連 references（より詳細）

| Topic | Read |
|---|---|
| Route Group の命名 | `frontend/route-groups.md` |
| フィーチャ単位フォルダ | `frontend/feature-folder.md` |
| `[id]/` のルーティング | `frontend/id-routing.md` |
| ルートファイル種別（page / layout / error / loading 等） | `frontend/conventions/route-files.md` |
| Server / Client Component の境界 | `frontend/conventions/server-vs-client.md` |
| API ルート構成 | `backend/api-folder-overview.md` |
| proxy.ts | `backend/proxy.md` |

---

## ルール

- モノレポ前提（`packages/web/` 配下）
- Route Group は **`(authenticated)` `(auth)` `(shared)`** の 3 つに統一
- API ルートは **`/api/v1/`** 配下（バージョニング）
- `proxy.ts` はプロジェクト直下（Next.js 16 で `middleware.ts` から rename）
- 共通要素は `app/(shared)/` 配下
