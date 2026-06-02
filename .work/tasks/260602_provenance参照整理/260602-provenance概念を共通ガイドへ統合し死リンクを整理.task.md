# provenance 概念を共通ガイドへ統合し死リンクを整理

> ブランチ: `refactor/integrate-provenance-into-common-guide`

## 概要

`references/provenance.md` は実在しないのに、claude-kit の複数のリファレンス・スキルファイルから
参照されており、死リンク・循環参照・存在しない注入ルール記述を生んでいる（ISSUE-123）。
provenance（JP ミラー警告コメントのフォーマット／スタンプ手順）という概念を `共通ガイド.md` の
JP/EN ミラールールセクションに直接統合し、散在する `provenance.md` 参照を削除または共通ガイド参照へ
書き換える（案 B）。

### 実施条件

即時実施可。

## 作業内容

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | 未解決事項を `## QA` に記録する（QA は ISSUE-123 で B に確定済み、本ブランチに未決事項なし） |
| 2 | 済 | リポジトリ全体の provenance 参照を grep で洗い出し、実在しないことを確認 |
| 3 | 済 | `共通ガイド.md` の JP/EN ミラー節に警告コメント仕様を自己完結化（`(see provenance.md)` 死リンク除去） |
| 4 | 済 | `スキル.md` の 3 箇所（行 7 / 70 / 153）の provenance 記述を共通ガイド参照へ書き換え |
| 5 | 済 | creator 系 5 SKILL.md（claude/skill/rule/hook/plugin）の `references/provenance.md` 参照を書き換え |
| 6 | 済 | `claude-refactor` SKILL.md の 2 箇所（Step 4 / References）の provenance 参照を書き換え（grep で追加検出） |
| 7 | 済 | 上記すべての JP ミラー（.jp.md）を同期 |
| 8 | 済 | `_injection_rules.yaml` / `_index.yaml` に provenance 宣言が無いことを確認（孤立チェック） |
| 9 | 済 | 修正後に再 grep し `provenance.md` への死リンクが 0 件であることを確認 |
| 10 | 済 | `.work/notes/` の関連ノートを更新する |

## 変更内容

実装したファイル（テスト以外）。

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/claude-kit/references/common/共通ガイド.md` | 編集 | 警告コメント仕様を自己完結化、`(see provenance.md)` 死リンク除去 | +jp |
| 2 | `plugins/claude-kit/references/skill/スキル.md` | 編集 | 行 7/70/153 の provenance 記述を共通ガイド参照へ | +jp |
| 3 | `plugins/claude-kit/skills/claude-creator/SKILL.md` | 編集 | `references/provenance.md` 参照を共通ガイド参照へ | +jp |
| 4 | `plugins/claude-kit/skills/skill-creator/SKILL.md` | 編集 | 同上 | +jp |
| 5 | `plugins/claude-kit/skills/rule-creator/SKILL.md` | 編集 | 同上 | +jp |
| 6 | `plugins/claude-kit/skills/hook-creator/SKILL.md` | 編集 | 同上 | +jp |
| 7 | `plugins/claude-kit/skills/plugin-creator/SKILL.md` | 編集 | 同上 | +jp |
| 8 | `plugins/claude-kit/skills/claude-refactor/SKILL.md` | 編集 | Step 4 / References の provenance 列挙を整理 | +jp |
| 9 | `plugins/claude-kit/CLAUDE.md` | 編集 | Changelog に本リファクタを追記、version bump | +jp |
| 10 | `plugins/claude-kit/.claude-plugin/plugin.json` | 編集 | version 3.55.0 → 3.56.0 | - |

## テスト

| # | 確認内容 | 実測結果 | 判定 |
|---|---|---|---|
| 1 | `grep -rn "provenance" plugins/` で `provenance.md` への死リンクが 0 件 | (実装後に記録) | - |
| 2 | `_injection_rules.yaml` / `_index.yaml` に provenance 宣言が無い | NONE（着手前確認済み） | OK |

## 参考ドキュメント

- `.work/notes/スキル設計/ref-injectジェネレータ.md`: provenance 概念の経緯（PR161 で導入→PR165 で全廃）

## 関連イシュー

| # | ID | 概要 | resolution |
|---|---|---|---|
| 1 | ISSUE-123 | provenance.md が複数箇所から参照されているが実体が存在しない | resolved |

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | - | なし |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | - | なし | - |
