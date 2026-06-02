# ISSUE-193: claude-kit/CLAUDE.md changelog テーブルの行番号「2」が3回重複

**作成日**: 2026-06-02

## 問題

`plugins/claude-kit/CLAUDE.md`（および `CLAUDE.jp.md`）の `## Changelog` テーブルで、行番号（第 1 列）が `1, 2, 2, 2, 3, 4, 5, ...` となっており、番号 `2` が `3.55.0`・`3.54.0`・`3.53.0` の 3 行に重複している。

## 対応方針

行番号列は単純な 1 始まりの連番のため、`1, 2, 3, 4, 5, 6, ...` に振り直す。JP ミラーも同期する。

## 対象ファイル

- `plugins/claude-kit/CLAUDE.md`: changelog の行番号列を連番に修正
- `plugins/claude-kit/CLAUDE.jp.md`: 同上

# ユーザー回答欄

## 意思

**回答**: <!-- 承認 / 却下 / 保留 -->
