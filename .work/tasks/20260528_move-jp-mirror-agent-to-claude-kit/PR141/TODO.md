# PR141 — move-jp-mirror-agent-to-claude-kit

## 概要

PR133 で work-kit に追加した `jp-mirror-translator` エージェントを claude-kit に移動する。
また、PR137 で作成した `agent-jp-mirror-sync` ルール（不要と判明）と `.claude/rules/feature/_overview.md`（不要）を削除する。
さらに、claude-kit の creator skills（skill-creator / rule-creator / hook-creator / claude-creator）で JP ミラーを生成する際に `jp-mirror-translator` エージェントを使うよう変更する。

### 実施条件

即時実施可

### 関連PR

| PR番号 | 概要 |
|---|---|
| #133 | jp-mirror-translator エージェントを work-kit に追加（このPRで claude-kit へ移動） |
| #137 | agent-jp-mirror-sync ルールを追加（このPRで削除） |

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | `.work/tasks/.../PR141/QA.md` |
| 済 | `.work/notes/` のノートを更新する | `.work/notes/jp-mirror-policy.md` |
| 済 | `jp-mirror-translator` エージェントを work-kit → claude-kit に移動 | `plugins/work-kit/agents/` → `plugins/claude-kit/agents/` |
| 済 | work-kit の `plugin.json` から agents エントリを削除 | `plugins/work-kit/.claude-plugin/plugin.json` |
| 済 | claude-kit の `plugin.json` に agents エントリを追加 | `plugins/claude-kit/.claude-plugin/plugin.json` |
| 済 | `agent-jp-mirror-sync.md`（英語版・JP ミラー）を削除 | `.claude/rules/feature/agent-jp-mirror-sync.md`, `.claude/rules-jp/feature/agent-jp-mirror-sync.md` |
| 済 | `.claude/rules/feature/_overview.md` を削除 | `.claude/rules/feature/_overview.md` |
| 済 | creator skills の JP ミラー生成ステップを `jp-mirror-translator` 使用に変更 | `plugins/claude-kit/skills/skill-creator/SKILL.md`, `plugins/claude-kit/skills/rule-creator/SKILL.md`, `plugins/claude-kit/skills/hook-creator/SKILL.md`, `plugins/claude-kit/skills/claude-creator/SKILL.md` |
| 済 | 各 SKILL.jp.md（JP ミラー）を更新 | 上記の対応 `.jp.md` |
| 済 | marketplace.json のバージョンを更新 | `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `.work/notes/jp-mirror-policy.md`: JP ミラーポリシーのメモ
- `plugins/work-kit/agents/jp-mirror-translator.md`: 移動対象のエージェント定義

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |
