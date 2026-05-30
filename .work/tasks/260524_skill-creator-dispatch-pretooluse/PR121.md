# PR121 — skill-creator-dispatch-pretooluse

## 概要

claude-kit の skill-creator-dispatch フックが UserPromptSubmit のみで実装されており、ユーザーが曖昧なプロンプトを送った場合に Claude が直接 SKILL.md を編集してもフックが発火しない問題を修正する。PreToolUse フック（dev-kit と同じブロック型）を追加し、4プラグイン（claude-kit/dev-kit/ui-kit/work-kit）すべてで直接 SKILL.md 編集をブロックする。

### 実施条件

即時実施可

### 関連PR

| PR番号 | 概要 |
|---|---|
| #113 | disable-model-invocation フラグ整理（creator-dispatch 関連） |
| #115 | フックパターン一括変更（claude-kit 漏れの原因PR） |

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | `.work/tasks/20260524_skill-creator-dispatch-pretooluse/PR121/QA.md` |
| 済 | `.work/notes/` のノートを更新する | `.work/notes/claude-kit-creator-skill-hook.md` |
| 済 | claude-kit: PreToolUse SKILL.md ブロックフックを hooks.json に追加 | `plugins/claude-kit/hooks/hooks.json` |
| 済 | claude-kit: skill-creator-dispatch.md を PreToolUse 向けに更新 | `plugins/claude-kit/hooks/prompts/skill-creator-dispatch.md` |
| 済 | claude-kit: skill-creator-dispatch.jp.md を更新 | `plugins/claude-kit/hooks/prompts/skill-creator-dispatch.jp.md` |
| 済 | dev-kit: hooks.json の PreToolUse に SKILL.md ブロックを追加 | `plugins/dev-kit/hooks/hooks.json` |
| 済 | dev-kit: skill-creator-dispatch.md を新規作成 | `plugins/dev-kit/hooks/prompts/skill-creator-dispatch.md` |
| 済 | dev-kit: skill-creator-dispatch.jp.md を新規作成 | `plugins/dev-kit/hooks/prompts/skill-creator-dispatch.jp.md` |
| 済 | ui-kit: hooks.json に PreToolUse セクションを新規追加 | `plugins/ui-kit/hooks/hooks.json` |
| 済 | ui-kit: skill-creator-dispatch.md を新規作成 | `plugins/ui-kit/hooks/prompts/skill-creator-dispatch.md` |
| 済 | ui-kit: skill-creator-dispatch.jp.md を新規作成 | `plugins/ui-kit/hooks/prompts/skill-creator-dispatch.jp.md` |
| 済 | work-kit: hooks.json に Edit/Write PreToolUse を追加 | `plugins/work-kit/hooks/hooks.json` |
| 済 | work-kit: skill-creator-dispatch.md を新規作成 | `plugins/work-kit/hooks/prompts/skill-creator-dispatch.md` |
| 済 | work-kit: skill-creator-dispatch.jp.md を新規作成 | `plugins/work-kit/hooks/prompts/skill-creator-dispatch.jp.md` |
| 済 | 各プラグイン plugin.json / marketplace.json バージョンバンプ | `plugins/*/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |
| 済 | incidents に今回修正した問題を記録する | `.claude/rules/core/incidents.md` |

## 参考ドキュメント

- `plugins/dev-kit/hooks/hooks.json`: PreToolUse ブロック型の実装例（python-skill-dispatch / yaml-skill-dispatch）

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| ui-kit-skill-reminder-jp-mirror | ui-kit の `ui-skill-reminder.md` に `.jp.md` ミラーが存在しない。hook-prompts-jp-mirror-sync ルール違反。作成して補完する | 即時実施可 |

## QA

なし
