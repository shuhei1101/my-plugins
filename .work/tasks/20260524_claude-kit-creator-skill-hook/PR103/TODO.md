# PR103 — claude-kit-creator-skill-hook

## 概要

CLAUDE.md・スキル（SKILL.md）・ルール・フックのいずれかを編集・作成しようとしたとき、対応するクリエイタースキルを使うよう Claude Code に促す UserPromptSubmit フックを claude-kit に追加する。現在は `.claude/rules/feature/creator-skill-dispatch.md` でルールとして記述しているが、ルールは「常時読み込み」かつ「Claude が守るかどうかに依存」するため、フックで自動プロンプトインジェクションする方が確実。

### 実施条件

即時実施可

### 関連PR

| PR番号 | 概要 |
|---|---|
| - | - |

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | QA.md に未決定事項を記録する | - `.work/tasks/.../PR103/QA.md` |
| - | `.work/notes/` のノートを更新する | - `.work/notes/claude-kit-creator-skill-hook.md` |
| - | `/claude-kit:hook-creator` を使って UserPromptSubmit フックを作成 | - `plugins/claude-kit/hooks/creator-skill-dispatch/` |
| - | plugin.json / marketplace.json のバージョンバンプ | - `plugins/claude-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `.claude/rules/feature/creator-skill-dispatch.md`: 現在のルールベース実装（フックに移行する対象）
- `.work/notes/claude-kit-creator-skill-hook.md`: 設計メモ・検知パターン

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| {次にやること} | {背景・目的} | {例: 即時実施可 / 「{他候補タイトル}」が完了したら} |
