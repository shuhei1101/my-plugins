<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# 「ベストプラ網羅型」references がフック自動 inject 前提で分割やり直しになった

**日付**: 2026-05-28
**PR**: PR135 (review-next-kit-plugin)

## 背景

PR135 で `next-kit` references を Next.js コミュニティのベストプラクティスと照合してレビュー。72 件の QA 判断を反映後、AI は shadcn/ui・Server Actions・テスト・セキュリティ等をカバーした 46 ファイルの references を仕上げた。

ユーザーが成果物を点検したところ、具体的なファイル (`backend/api-routes.md` の 50〜60 行目、`backend/auth.md` の 11〜22 行目) を指摘して構造を拒否:

- `api-routes.md` は 6 種類のファイル種別 (`route.ts` / `client.ts` / `service.ts` / `db.ts` / `query.ts` / `dbHelper.ts`) を 1 ファイルに詰めていた。ユーザーが `query.ts` だけ書きたいときに、他 5 種類の情報まで読み込まれる
- `auth.md` の大半が「プロバイダ選定の比較表」(Better Auth / Auth.js / Lucia / Clerk / Supabase Auth)。決定済みの後では比較表はノイズで、フック自動 inject には役立たない
- ユーザー曰く: 「次の PR でフックを作る前提で、ファイル名・パスでヒットしたらその reference だけ inject する形にしたい。だから 1 ファイル = 1 ユースケースに分割して、比較・選定・トレードオフは完全削除して」

結果: QA-073 を起票し、references を全面再分割 — **46 → 90 ファイル**、ファイル名はフックトリガーキーワード (`query-ts.md` / `route-ts.md` / `list-screen-tsx.md` 等) と一致させた。

## 根本原因

AI は「**ベストプラクティスの網羅**」を最適化していた (「SEO は? テストは? PWA は? a11y は?」)。「**読まれる場面**」(誰が・いつ・どれだけの周辺コンテキストを必要としているか) を最適化していなかった。

フック注入の世界では、価値の単位は「**1 ファイル編集**」。それと無関係なものは全てトークンの無駄。

「比較・選定・トレードオフ」セクションは特に質が悪い: それらは *判断* のために存在するが、判断が記録された後、比較表は実装者にとってもう価値がない。AI がデフォルトで「網羅的」なドキュメントを書こうとしただけで残っていた。

## 教訓

フックで（または何らかの自動 inject 機構で）読み込まれる references を書くとき:

1. **トリガーを想像する**: どのファイル編集でこの reference が読み込まれるか?
2. **1 ファイル = 1 トリガー = 1 ユースケース**。2 つのファイル種別が共通の内容を持つなら、共通部分は構造的なもの (`api-folder-overview.md` のような薄いファイル) として独立させるか、または両方にコピペして短く保つ
3. **比較・選定・トレードオフセクションは削除**。判断は commit message / `.work/notes/` または 1 行記述に残す — フックで毎回 inject される比較表として残してはいけない
4. **ファイル名はトリガーキーワードと一致**: `query.ts` 編集 → `query-ts.md`、`EditScreen.tsx` 編集 → `edit-screen-tsx.md`、`proxy.ts` 編集 → `proxy.md`。これで `injection_rules.yaml` での 1:1 マッピングが簡単になる

## 再発防止

- kit 系 plugin の references を設計するとき、**`injection_rules.yaml` のパターン(トリガーマップ)から始める** — 内容の目次から始めない
- AI の plan / QA フェーズに以下のチェックを加える: 「この 1 ファイルがフックで自動 inject されたとき、編集者の現在のファイルに無関係な内容も一緒に注入されないか? もし含まれるなら、分割せよ」

## 関連

- PR135 のコミット `02a5b0e` (backend 分割)、`fac94c5` (frontend 分割)、`ef44fe6` (shared/error 分割 + 最終整合)
- `premature-cross-plugin-centralization.md` (PR140 — 反対の間違い: 早すぎる共通化)
- `markdown-for-code-consumed-config.md` (PR140 — コードで消費される設定ファイルを人間用に設計した)
