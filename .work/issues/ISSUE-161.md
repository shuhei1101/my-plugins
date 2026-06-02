# ISSUE-161: イシュー.md Lifecycle 記述が旧 reject ブランチモデルのまま（JP ミラーと乖離）

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [ ] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`plugins/work/references/work-dir/イシュー.md` の Lifecycle セクションが v2.68.0 で廃止されたシェアドブランチモデルの記述のままになっており、JP ミラーと乖離している。

英語オリジナルは「`wontfix` クローズを shared `chore/rejected-issues` ブランチで行う」と記述しているが、v2.68.0 以降の実装は「使い捨ての 1 イシュー専用ブランチ `chore/reject-ISSUE-{N}` を切って master へ即マージ」する方式に変更されており、JP ミラーはすでに新方式を反映している。

## 対応方針

EN オリジナルの該当行を、JP ミラーの記述（使い捨て per-issue ブランチ方式）に合わせて修正する。

## 対象ファイル

- `plugins/work/references/work-dir/イシュー.md`: Lifecycle セクションの reject ブランチ記述を現行方式に修正

