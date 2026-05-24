# PR95 — pr-handoff-sequential-deps

## 概要

pr-handoff スキルを直列依存対応に改修する。

現在の実装では、TODO.md の `## 次PR候補` に複数件あった場合は全件をそのまま別々のPRとして予約する。
しかし実際には、後続PRが先行PRのマージ後にしか着手できない（直列依存がある）ケースが頻繁にある。
例: PR10 がマージされた後でないと PR11 の実装が始められない。

このようなケースで全件を一度に予約すると、後続PRのワークツリーが古い master ベースで作られてしまい、
先行PR のマージ完了後に大量のリベース作業が発生する。

そこで:
- TODO.md の `## 次PR候補` テーブルに `実施条件` カラムを追加し、依存関係を明示できるようにする
- pr-handoff は実施条件を読み取り、即時着手可能な候補のみ予約する
- 依存候補は予約せず、予約された先行PRの TODO.md `## 次PR候補` に埋め込む（連鎖的に引き継ぐ）

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | QA.md に未決定事項を記録する | - `.work/tasks/.../PR95/QA.md` |
| - | TODO.md テンプレに `実施条件` カラムを追加 | - `plugins/work-kit/templates/TODO.md`<br>- `plugins/work-kit/templates/.work/tasks/yyyymmdd_xxx/PRXXX/TODO.md` |
| - | pr-handoff SKILL.md を直列依存対応に改修 | - `plugins/work-kit/skills/pr-handoff/SKILL.md`<br>- `plugins/work-kit/skills/pr-handoff/SKILL.jp.md` |
| - | work-start SKILL.md Step 7 のテンプレート言及を更新 | - `plugins/work-kit/skills/work-start/SKILL.md`<br>- `plugins/work-kit/skills/work-start/SKILL.jp.md` |
| - | work-kit プラグインのバージョン bump | - `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |
| - | changelog 追加 | - `plugins/work-kit/changelogs/` |
| - | ルール `work-kit-todo-template-sync.md` のチェックリストに実施条件カラムを反映 | - `.claude/rules/feature/work-kit-todo-template-sync.md` |

## 参考ドキュメント

- `.claude/rules/feature/work-kit-todo-template-sync.md`: TODO テンプレと SKILL.md の同期ルール
- `.claude/rules/feature/skill-jp-mirror-sync.md`: SKILL.jp.md 同期ルール

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| {次にやること} | {背景・目的} | {例: PR{N} がマージされたら / 即時実施可} |
</content>
</invoke>