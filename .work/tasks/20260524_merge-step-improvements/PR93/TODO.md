# PR93 — merge-step-improvements

## 概要

work-kit:merge スキルに2つの改善を加える:

**1. Step 10 に pr-handoff 自動呼び出しを追加**
- 現在の Step 10 は「次PR候補」をユーザーに提示するだけ
- TODO.md に次PR候補がある場合、自動で `/work-kit:pr-handoff` を呼び出して PR を予約する
- 候補がない場合はスキップ

**2. conversation-to-claude をワークツリーで実行**
- 現在の Step 3 は master の cwd で `conversation-to-claude` を呼ぶ
- 結果として `.claude/rules/`・`.claude/references/` への書き込みが master 行きになり、PR の `--no-ff` マージに同梱されない
- ワークツリーに `cd` してから呼び出すよう変更し、変更を PR ブランチに同梱する

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | merge SKILL.jp.md の Step 3 を「ワークツリーで conversation-to-claude を実行」に変更 | - `plugins/work-kit/skills/merge/SKILL.jp.md` |
| - | merge SKILL.md の Step 3 を同様に変更 | - `plugins/work-kit/skills/merge/SKILL.md` |
| - | merge SKILL.jp.md の Step 10 に pr-handoff 自動呼び出しを追記 | - `plugins/work-kit/skills/merge/SKILL.jp.md` |
| - | merge SKILL.md の Step 10 に同様に追記 | - `plugins/work-kit/skills/merge/SKILL.md` |
| - | plugin.json / marketplace.json のバージョンを bump | - `plugins/work-kit/.claude-plugin/plugin.json` / `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- 既存スキル: `plugins/work-kit/skills/pr-handoff/SKILL.md`
- 既存スキル: `plugins/claude-kit/skills/conversation-to-claude/SKILL.md`

## 次PR候補

| タイトル | 概要 |
|---|---|
| {次にやること} | {背景・目的} |
