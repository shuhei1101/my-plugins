# PR124 — fix-skill-creator-dispatch-dedup

## 概要

PR121 で dev-kit/ui-kit/work-kit に追加した `skill-creator-dispatch` の PreToolUse フックを削除し、claude-kit に集約する。
各プラグインが同一内容の hooks エントリと prompts ファイルを持つ重複状態を解消する。

### 実施条件

即時実施可

### 関連PR

| PR番号 | 概要 |
|---|---|
| #PR121 | skill-creator-dispatch を PreToolUse ブロック型に移行して4プラグインに追加（本PRで一部を削除） |

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | `.work/tasks/20260525_fix-skill-creator-dispatch-dedup/PR124/QA.md` |
| 済 | `.work/notes/` のノートを更新する | `.work/notes/hook-creator-dispatch.md` |
| 済 | dev-kit/hooks.json から skill-creator-dispatch PreToolUse エントリを削除 | `plugins/dev-kit/hooks/hooks.json` |
| 済 | ui-kit/hooks.json から skill-creator-dispatch PreToolUse エントリを削除 | `plugins/ui-kit/hooks/hooks.json` |
| 済 | work-kit/hooks.json から skill-creator-dispatch PreToolUse エントリを削除 | `plugins/work-kit/hooks/hooks.json` |
| 済 | dev-kit の skill-creator-dispatch プロンプトファイルを削除 | `plugins/dev-kit/hooks/prompts/skill-creator-dispatch.md` `plugins/dev-kit/hooks/prompts/skill-creator-dispatch.jp.md` |
| 済 | ui-kit の skill-creator-dispatch プロンプトファイルを削除 | `plugins/ui-kit/hooks/prompts/skill-creator-dispatch.md` `plugins/ui-kit/hooks/prompts/skill-creator-dispatch.jp.md` |
| 済 | work-kit の skill-creator-dispatch プロンプトファイルを削除 | `plugins/work-kit/hooks/prompts/skill-creator-dispatch.md` `plugins/work-kit/hooks/prompts/skill-creator-dispatch.jp.md` |
| 済 | 各プラグインの plugin.json バージョンバンプ | `plugins/dev-kit/.claude-plugin/plugin.json` `plugins/ui-kit/.claude-plugin/plugin.json` `plugins/work-kit/.claude-plugin/plugin.json` |
| 済 | marketplace.json バージョンバンプ | `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `.work/notes/claude-kit-creator-skill-hook.md`: creator-dispatch フック設計メモ

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| claude-kit-pretooluse-pattern-extend | claude-kit の PreToolUse パターンを SKILL.jp.md / rules/*.md / CLAUDE.md にも拡張 | 即時実施可 |
| pretooluse-file-edit-intercept-research | PreToolUse でファイル編集を検知する仕組みの設計調査・実装 | 即時実施可 |

## QA

なし
