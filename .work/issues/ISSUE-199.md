# ISSUE-199: キットフック同期.md が参照する references/CLAUDE.md パスが実在しない（実パスは .ref-inject/CLAUDE.md）

**作成日**: 2026-06-03

# ユーザー回答欄

## 意思

- [x] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`plugins/claude-kit/references/hook/キットフック同期.md` の構造テーブルとチェックリストが `plugins/*-kit/references/CLAUDE.md` / `CLAUDE.jp.md` を参照しているが、この場所にファイルは存在しない。

実際に存在するのは `plugins/claude-kit/references/.ref-inject/CLAUDE.md`（`.ref-inject/` サブフォルダ内）であり、`dev-kit` には対応ファイル自体が存在しない。

```
# キットフック同期.md が記述する期待構造（現状と不一致）
plugins/*-kit/references/CLAUDE.md      ← 存在しない

# 実際の状況
plugins/claude-kit/references/.ref-inject/CLAUDE.md   ← 存在
plugins/dev-kit/references/.ref-inject/CLAUDE.md      ← 存在しない
```

キットフック同期.md はオーサリングガイドとして auto-inject される文書であり、記述パスが誤っていると同期チェック時に開発者が正しいファイルを参照できない。

## 対応方針

`キットフック同期.md`（と JP ミラー）のテーブル・チェックリストのパスを `.ref-inject/CLAUDE.md` に修正する。dev-kit に `references/.ref-inject/CLAUDE.md` が不足している場合は claude-kit を参考に作成する（任意）。

## 対象ファイル

- `plugins/claude-kit/references/hook/キットフック同期.md`: パスを `.ref-inject/CLAUDE.md` に修正
- `plugins/claude-kit/references/hook/キットフック同期.jp.md`: JP ミラー同期
