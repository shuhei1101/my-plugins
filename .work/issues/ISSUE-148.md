# ISSUE-148: url-state.jp.md と launchers-windows.jp.md の英語ソースファイルが存在しない

**作成日**: 2026-06-02

## 問題

2 つの `.jp.md` ミラーファイルが存在するが、対応する英語ソース（`.md`）が存在しない。`_index.yaml` と `_injection_rules.yaml` はその存在しない英語ソースパスを参照しており、注入が無声でスキップされる。

存在する JP ミラー（孤立）:
- `plugins/dev-kit/references/next/frontend/url-state.jp.md` — 内容あり（URL クエリ state 全量）
- `plugins/dev-kit/references/python/scripts/launchers-windows.jp.md` — 内容あり（bat ランチャー全量）

存在しない英語ソース:
- `next/frontend/url-state.md` — `_index.yaml` と `_injection_rules.yaml` で参照
- `python/scripts/launchers-windows.md` — `_index.yaml` と `_injection_rules.yaml` で参照

規約上、`.jp.md` は `.md` の JP ミラーであり、英語ソースが source of truth。英語ソースが存在しない JP ミラーは孤立ファイルであり、注入フックも機能しない。

## 対応方針

JP ミラーの内容を英語に翻訳して英語ソース（`.md`）を新規作成し、JP ミラーを JP mirror warning comment つきで維持する。`_index.md` への追記も必要。

## 対象ファイル

- `plugins/dev-kit/references/next/frontend/url-state.md`: 新規作成（JP ミラーを英語化）
- `plugins/dev-kit/references/python/scripts/launchers-windows.md`: 新規作成（JP ミラーを英語化）
- `plugins/dev-kit/references/_index.md`: 2 ファイルの追記

## QA

### QA-1: どの案で進めるか

A) JP ミラー内容を英語化して新規 `.md` を作成、JP ミラーは維持 / B) JP ミラーファイルをリネームして英語ソース化し、改めて `.jp.md` を作成

**推奨**: A — ファイル名変更なしで済み、作業範囲が明確

**回答**: <!-- A / B -->

# ユーザー回答欄

## 意思

**回答**: <!-- 承認 / 却下 / 保留 -->
