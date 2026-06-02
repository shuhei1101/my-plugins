# ISSUE-172: next-implement / next-plan が英語名の reference パスを参照しているが実ファイルは日本語名

**作成日**: 2026-06-02

## 問題

`dev-kit:next-implement` および `dev-kit:next-plan` が Step 2 の「配置先確認」や `References` セクションで英語名の reference ファイルパスを多数列挙しているが、`references/next/frontend/` および `references/next/backend/` の実ファイルはすべて日本語名である。これらの英語名パスはどこにも存在しない。

### next-implement/SKILL.md（主なマッピング）

| SKILL.md 記載パス（存在しない） | 実際のファイル名 |
|---|---|
| `frontend/feature-folder.md` | `next/frontend/フィーチャーフォルダ.md` |
| `frontend/route-groups.md` | `next/frontend/ルートグループ.md` |
| `frontend/id-routing.md` | `next/frontend/IDルーティング.md` |
| `frontend/list-page-tsx.md` | `next/frontend/一覧ページ-tsx.md` |
| `frontend/view-page-tsx.md` | `next/frontend/詳細ページ-tsx.md` |
| `frontend/edit-page-tsx.md` | `next/frontend/編集ページ-tsx.md` |
| `frontend/form-ts.md` | `next/frontend/フォーム-ts.md` |
| `backend/actions-ts.md` | `next/backend/アクション-ts.md` |
| `backend/route-ts.md` | `next/backend/ルート-ts.md` |
| `backend/client-ts.md` | `next/backend/クライアント-ts.md` |
| `backend/service-ts.md` | `next/backend/サービス-ts.md` |
| `backend/db-ts.md` | `next/backend/DB-ts.md` |
| `backend/query-ts.md` | `next/backend/クエリ-ts.md` |
| `references/CLAUDE.md` | `references/_index.md` |

### next-plan/SKILL.md

同様に `frontend/app-folder-overview.md`（実: `next/frontend/appフォルダ概要.md`）等が誤っている。

## 対応方針

英語名パスを日本語名パスに全件修正し、`references/CLAUDE.md` の参照を `references/_index.md` に変更する。英語版・JP ミラー両方を更新する。

## 対象ファイル

- `plugins/dev-kit/skills/next-implement/SKILL.md`: マッピングテーブル・References セクションのパスを全件修正
- `plugins/dev-kit/skills/next-implement/SKILL.jp.md`: 同上
- `plugins/dev-kit/skills/next-plan/SKILL.md`: references リスト・References セクションのパスを全件修正
- `plugins/dev-kit/skills/next-plan/SKILL.jp.md`: 同上

## QA

### QA-1: 修正方針の選択

A) 英語名パスを日本語名パスに全件書き換え / B) 英語名エイリアスファイルを別途追加して両立

**推奨**: A — スキル本文のパスが実ファイルと1対1で対応するのがシンプル

**回答**: <!-- A / B -->

# ユーザー回答欄

## 意思

**回答**: <!-- 承認 / 却下 / 保留 -->
