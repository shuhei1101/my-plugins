# PR47 — improve-merge-skill

## 概要

work-kit:merge スキルの改善。セッションで PR が特定済みの場合はスクリプトをスキップ、
index アーカイブをスクリプト不要の直接操作に変更、マージ先を派生元ブランチに統一、
チェックリスト表記を修正する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | `.work/tasks/20260517_improve-merge-skill/PR47/QA.md` |
| 済 | ステップ1: セッションで PR が特定済みの場合はステップ2へ進む分岐を追加 | `plugins/work-kit/skills/merge/SKILL.md`, `SKILL.jp.md` |
| 済 | ステップ3: スクリプト依存を廃止し index.yaml を直接操作に変更 | `plugins/work-kit/skills/merge/SKILL.md`, `SKILL.jp.md` |
| 済 | ステップ4: 「メインブランチ」を「派生元ブランチ」に変更 | `plugins/work-kit/skills/merge/SKILL.md`, `SKILL.jp.md` |
| 済 | チェックリストの index.archive.yaml 項目を「PRブランチに同梱」表記に修正 | `plugins/work-kit/skills/merge/SKILL.md`, `SKILL.jp.md` |
| 済 | バージョンを 2.15.2 → 2.16.0 に bump | `plugins/work-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `plugins/work-kit/skills/merge/SKILL.md`: マージスキル定義
