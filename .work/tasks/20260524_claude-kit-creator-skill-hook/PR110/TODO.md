# PR110 — remove-redundant-creator-rules

## 概要

PR103 で claude-kit に UserPromptSubmit creator-dispatch フックを追加したことにより、プロジェクト内のルール・CLAUDE.md に記述していた「クリエイタースキルを使え」という指示が冗長になった。フックによる自動注入に移行したため、重複するテキストを削除する。

### 実施条件

即時実施可（PR103 マージ済み）

### 関連PR

| PR番号 | 概要 |
|---|---|
| #103 | creator-dispatch フック追加（このPRの前提） |

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | - `.work/tasks/.../PR110/QA.md` |
| 済 | `.work/notes/` のノートを更新する | - `.work/notes/claude-kit-creator-skill-hook.md` |
| 済 | `plugin-work.md` の "Skills to Use When Creating New Content" セクションを削除 | - `.claude/rules/core/plugin-work.md` |
| 済 | `CLAUDE.md` の "Plugin Creation & Update Rules" セクションを削除 | - `CLAUDE.md` |

## 参考ドキュメント

- `.work/notes/claude-kit-creator-skill-hook.md`: creator-dispatch フック設計メモ

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| {次にやること} | {背景・目的} | {例: 即時実施可 / 「{他候補タイトル}」が完了したら} |
