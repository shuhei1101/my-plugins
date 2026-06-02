# PR109 — pr-show-skill

## 概要

merge スキルの Step 12（予約済みPR状況表示）を `pr-show` という独立スキルとして切り出す。
merge 完了後以外にも「今どのPRが予約されているか確認したい」という場面で直接呼び出せるようにする。
merge SKILL.md の Step 12 は `pr-show` への委譲（呼び出し）に書き換える。

### 実施条件

即時実施可

### 関連PR

| PR番号 | 概要 |
|---|---|
| #107 | merge スキルの Step 12 テーブル形式追加（pr-show の元となったステップ） |

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| x | QA.md に未決定事項を記録する（未決定事項なし） | `.work/tasks/20260524_pr-show-skill/PR109/QA.md` |
| x | merge SKILL.md の Step 12 内容を確認する（英語版） | `plugins/work-kit/skills/merge/SKILL.md` |
| x | `pr-show` スキルの SKILL.jp.md を作成する | `plugins/work-kit/skills/pr-show/SKILL.jp.md` |
| x | `pr-show` スキルの SKILL.md を作成する | `plugins/work-kit/skills/pr-show/SKILL.md` |
| x | merge SKILL.md の Step 12 を pr-show への委譲に書き換える | `plugins/work-kit/skills/merge/SKILL.md` |
| x | merge SKILL.jp.md の Step 12 を同様に書き換える | `plugins/work-kit/skills/merge/SKILL.jp.md` |
| x | work-kit plugin.json / marketplace.json のバージョンをバンプする | `plugins/work-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |
| x | ルール・CLAUDE.md を整備する（glossary に pr-show エントリ追加） | `.claude/rules/core/glossary.md` |

## 参考ドキュメント

- `plugins/work-kit/skills/merge/SKILL.md:Step 12`: 元の実装（英語版）
- `plugins/work-kit/skills/merge/SKILL.jp.md:366-428`: 元の実装（日本語版）
- `.work/notes/work-kit-skills.md`: work-kit スキル群の設計メモ

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |

## QA

なし
