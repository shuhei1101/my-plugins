# PR87 — merge-skill-no-auto-merge

## 概要

merge SKILL.md に「絶対に勝手にマージしない」強化禁止文を追記する。
過去にユーザーがマージを許可した履歴があっても、毎回必ず明示的な指示を待つこと。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | `.work/tasks/20260524_merge-skill-no-auto-merge/PR87/QA.md` |
| 済 | merge SKILL.md に絶対マージ禁止の強化文を追記する | `plugins/work-kit/skills/merge/SKILL.md` |
| 済 | バージョンを bump する | `plugins/work-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |
| 済 | incidents.md に事故記録を追記する | `.claude/rules/core/incidents.md` |
| 済 | stop.md のマージ提案文に PR 番号を含める | `plugins/work-kit/hooks/prompts/stop.md` |
| 済 | SKILL.jp.md を SKILL.md の変更内容に合わせて更新する | `plugins/work-kit/skills/merge/SKILL.jp.md` |
| 済 | JP ミラー更新漏れを防ぐルールを追加する | `.claude/rules/feature/skill-jp-mirror-sync.md` |
| 済 | 編集対象に応じてクリエイタースキルを先に読む強制ルールを追加する | `.claude/rules/feature/creator-skill-dispatch.md` |

## 参考ドキュメント

- `plugins/work-kit/skills/merge/SKILL.md`: 修正対象のマージスキル定義

## 次PR候補

| タイトル | 概要 |
|---|---|
| - | - |
