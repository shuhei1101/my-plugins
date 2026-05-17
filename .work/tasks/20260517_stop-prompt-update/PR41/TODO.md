# PR41 — stop-prompt-update

## 概要

stop hook プロンプトに、QA確認とスペック確認のチェック項目を追加する。
現状は TODO.md の完了確認とマージ提案のみだが、以下も確認するよう拡張する:
- 現在のセッションで対応している PR の QA 表が全部回答済みか
- 今回作業した内容がスペック（仕様書）に書き起こされているか
- 全部揃っていれば `/work-kit:merge` の実行を提案する

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | stop.jp.md を更新（QA確認・スペック確認チェックを追加） | - `plugins/work-kit/hooks/prompts/stop.jp.md` |
| 済 | stop.md を更新（JP ミラーの内容を英語で反映） | - `plugins/work-kit/hooks/prompts/stop.md` |
| 済 | plugin.json と marketplace.json のバージョンを bump | - `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |

## 作業内容（追加）

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | タスクフォルダ・TODO・QA作成スクリプトを実装 | - `plugins/work-kit/scripts/setup-task.py` |
| 済 | work-start Step 5 をスクリプト呼び出しに変更 | - `plugins/work-kit/skills/work-start/SKILL.jp.md`<br>- `plugins/work-kit/skills/work-start/SKILL.md` |
| 済 | work-start Step 5 と Step 6 の間に「TODO記載」ステップを追加 | - `plugins/work-kit/skills/work-start/SKILL.jp.md`<br>- `plugins/work-kit/skills/work-start/SKILL.md` |
| 済 | plugin.json と marketplace.json のバージョンを bump | - `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |

## 作業内容（追加2）

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | setup-task.py に `--task-dir` 引数を追加（既存タスクフォルダ指定） | - `plugins/work-kit/scripts/setup-task.py` |
| 済 | work-start に「タスクフォルダ判定」ステップを追加（Step 5として挿入） | - `plugins/work-kit/skills/work-start/SKILL.jp.md`<br>- `plugins/work-kit/skills/work-start/SKILL.md` |
| 済 | plugin.json と marketplace.json のバージョンを bump | - `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `.work/specs/work-kit-stop-hook.md`: stop hook のチェック仕様
