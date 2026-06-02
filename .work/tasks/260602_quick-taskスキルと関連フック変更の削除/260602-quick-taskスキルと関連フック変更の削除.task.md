# quick-taskスキルと関連フック変更の削除

> ブランチ: refactor/remove-quick-task

## 概要

### 実施条件

即時実施可

### 背景

`work:quick-task` スキルは最近追加されたが、不要になったため削除する。
スキル本体と、追加時に変更されたフック・プラグイン設定をすべて削除し、追加前の状態に戻す。

## 作業内容

| No | 状態 | タスク |
|----|------|--------|
| 1 | 済 | `plugins/work/skills/quick-task/` ディレクトリを削除 |
| 2 | 済 | `user-prompt-submit.md/jp.md` から quick-task 振り分けロジックを削除 |
| 3 | 済 | `plugins/work/CLAUDE.md/jp.md` から quick-task 言及を削除 |
| 4 | 済 | `plugins/work/.claude-plugin/plugin.json` から quick-task エントリを削除 |
| 5 | 済 | `.claude-plugin/marketplace.json` から quick-task エントリを削除 |
| 6 | 済 | QA を記録する |

## 変更内容

| No | ファイル | 変更内容 |
|----|----------|----------|
| 1 | `plugins/work/skills/quick-task/SKILL.md` | 削除 |
| 2 | `plugins/work/skills/quick-task/SKILL.jp.md` | 〃 |
| 3 | `plugins/work/hooks/prompts/user-prompt-submit.md` | Step 3 を quick-task前（work:start のみ）に戻す |
| 4 | `plugins/work/hooks/prompts/user-prompt-submit.jp.md` | 〃 |
| 5 | `plugins/work/CLAUDE.md` | Lifecycle・Skills表・Changelogから quick-task 言及を削除; v2.70.0 エントリ追加 |
| 6 | `plugins/work/CLAUDE.jp.md` | 〃 |
| 7 | `plugins/work/.claude-plugin/plugin.json` | バージョン 2.70.0 にbump、descriptionを更新 |
| 8 | `.claude-plugin/marketplace.json` | work バージョンを 2.70.0 に更新 |

## テスト

| No | 確認項目 | 結果 |
|----|----------|------|
| — | — | — |

## QA

（なし）

## 参考ドキュメント

- `.work/notes/スキル設計/work-kitスキル群.md`

## 関連ブランチ

（なし）

## 次ブランチ候補

（なし）
