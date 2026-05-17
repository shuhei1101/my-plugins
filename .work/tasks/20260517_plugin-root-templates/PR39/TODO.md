# PR39 — plugin-root-templates TODO

## 概要

work-start スキルのテンプレート参照を `${CLAUDE_PLUGIN_ROOT}/templates/` へ移行。
`yyyymmdd_xxx/PRXXX/` という存在しないパスを参照しているバグを修正する。

## 仕様参照

- `.work/specs/plugin-root-templates.md`

## タスク

| Done | Task |
|------|------|
| 済 | `plugins/work-kit/templates/TODO.md` テンプレートファイル作成 |
| 済 | `plugins/work-kit/templates/QA.md` テンプレートファイル作成 |
| 済 | `plugins/work-kit/templates/spec.md` テンプレートファイル作成 |
| 済 | `SKILL.md` Step 5 のテンプレートパスを `${CLAUDE_PLUGIN_ROOT}/templates/` に修正 |
| 済 | `SKILL.md` Step 6 のテンプレートパスを `${CLAUDE_PLUGIN_ROOT}/templates/` に修正 |
| 済 | `SKILL.jp.md` 同様に修正 |
| 済 | `plugin.json` / `marketplace.json` バージョンバンプ |
| | `merge` スキル Step 3: index.archive.yaml を master 直接ではなく PR ブランチにコミットするよう修正 |
