---
paths:
  - "**/frontend/**/*.ts"
  - "**/tsconfig*.json"
  - "**/eslint.config.*"
  - "**/package.json"
  - "**/vitest.config.*"
  - "**/playwright.config.*"
---

# tsc 運用（バニラ TS + FastAPI）

ブラウザに出すのは `tsc` が生成した `.js`。バンドラは使わない（`html/core/ビルドレス原則.md`）。`.ts` を著作し、`tsc` がトランスパイル 1 段だけ挟む。

## 出力レイアウト（同階層 emit）

生成 `.js` は `.ts` と同じ階層に出す。`screen.ts` → 同じフォルダに `screen.js`。importmap・Jinja2 の `<script>` 参照は生成 `.js` を指す（importmap の配線が最小で済む）。

理由: 画面はフォルダで分割され 1 フォルダのファイル数が少ないため、同階層に `.js` が並んでも散らからない。`src/` → `static/` のような出力集約は HTML/importmap 側の付け替えが増えるので採らない。

## 設定ファイル（repo ルート）

| ファイル | 役割 |
| --- | --- |
| `tsconfig.json` | 型チェック用。`noEmit`。`frontend/**/*.ts`（移行期は `.js` も）を include |
| `tsconfig.build.json` | 生成用。`tsconfig.json` を継承し `noEmit:false` + 同階層 emit。include は `frontend/**/*.ts` のみ |
| `eslint.config.mjs` | flat config。`typescript-eslint` で `.ts` を lint。Next/React 設定は使わない |
| `package.json` | dev ツールの devDependencies と scripts（`type: module`） |

importmap の別名（`shared/`）は `tsconfig.json` の `paths` で `./frontend/shared/*` に解決する。

## scripts

| script | 中身 | 用途 |
| --- | --- | --- |
| `dev` | `tsc -p tsconfig.build.json --watch` | 開発中。保存ごとに変更分だけ再生成（数百 ms） |
| `build` | `tsc -p tsconfig.build.json` | 全 `.ts` を一括生成 |
| `typecheck` | `tsc -p tsconfig.json --noEmit` | CI / pre-commit。型崩れ検知 |
| `lint` | `eslint frontend` | flat config |
| `test` | `vitest run` / `playwright test` | テスト |
| `gen-types` | `openapi-typescript` | API 型を `shared/api/schema.d.ts` に生成（コミットする） |

開発フローは `npm run dev`（tsc --watch）を裏で回しつつ FastAPI を起動。`.ts` を保存すると `.js` が再生成され、ブラウザを再読込すれば反映される。

## 生成 .js は gitignore

著作は `.ts`、`.js` は生成物。フロントエンドの生成 `.js` はコミットしない（`.gitignore`）。例外は手書きで維持する `shared/vendor/`（外部依存の vendoring）と openapi 生成型 `shared/api/schema.d.ts`（コミットする）。

```
# 生成物（.ts から tsc が出力）
frontend/**/*.js
!frontend/shared/vendor/**
```

## 移行期の扱い

既存の手書き `.js`（108 ファイル）は順次 `.ts` に変換する。変換時はその `.js` を `git rm` し `.ts` を追加する（生成 `.js` は gitignore 済みなので追跡から外れる）。変換が終わるまで `tsconfig.json` は `.ts` と `.js` の両方を include して型チェックを切らさない。

## 型崩れ検知

`type` や API 型を 1 か所変えると、参照箇所が `tsc` で全部赤くなる。CI / pre-commit で `npm run typecheck` を回し、リファクタの変更漏れをコンパイル段階で捕まえる。
