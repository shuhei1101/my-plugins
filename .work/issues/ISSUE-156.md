# ISSUE-156: 薄ラッパー3本が存在しない notes-to-claude スキルを呼び出し元例として参照している

**作成日**: 2026-06-02

## 問題

`claude-creator`、`rule-creator`、`skill-creator` の SKILL.md が「explicit invocation and for callers (e.g. `notes-to-claude`)」と記述しているが、`notes-to-claude` というスキルはリポジトリ内のどこにも存在しない。

リポジトリ内には `.work/tasks/260524_notes-to-claudeスキル追加/` というタスクフォルダが存在し、「`work-kit:notes-to-claude` スキルを作成」と記載されている。つまり `work-kit` プラグイン向けとして計画されたが未実装、または別プラグインへ帰属する予定のスキルを、`claude-kit` の thin wrapper スキルが参照している状態。

## 対応方針

`notes-to-claude` の実装・廃止が決まるまで、参照例を削除するか「e.g. orchestrator skills」のような汎称に差し替える。JP ミラーも同期する。

## 対象ファイル

- `plugins/claude-kit/skills/claude-creator/SKILL.md`: `notes-to-claude` 参照を削除または汎称に差し替え
- `plugins/claude-kit/skills/rule-creator/SKILL.md`: 同上
- `plugins/claude-kit/skills/skill-creator/SKILL.md`: 同上
- 各 `SKILL.jp.md`: JP ミラー同期

# ユーザー回答欄

## 意思

**回答**: <!-- 承認 / 却下 / 保留 -->
