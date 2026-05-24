# PR89 — stop-hook-prompt-by-ref

## 概要

Stop フックの `reason` に全文を埋め込んでいたため、会話セッションに長い指示が差し込まれ見づらかった。
スクリプトが出力するのは「このファイルを読んで従って」の1行参照に変更し、Claude が自分でファイルを読む方式にする。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | QA.md に未決定事項を記録する | `.work/tasks/20260524_stop-hook-prompt-by-ref/PR89/QA.md` |
| 済 | stop.py をファイル参照1行出力に変更 | `plugins/work-kit/hooks/scripts/stop.py` |
| 済 | hook-creator SKILL.md に Stop フック1行参照ルールを追加 | `plugins/claude-kit/skills/hook-creator/SKILL.md` |
| 済 | hook-creator SKILL.jp.md を同期更新 | `plugins/claude-kit/skills/hook-creator/SKILL.jp.md` |
| 済 | work-kit バージョン bump | `plugins/work-kit/.claude-plugin/plugin.json` / `.claude-plugin/marketplace.json` |
| 済 | claude-kit バージョン bump | `plugins/claude-kit/.claude-plugin/plugin.json` / `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- なし

## 次PR候補

| タイトル | 概要 |
|---|---|
| - | - |
