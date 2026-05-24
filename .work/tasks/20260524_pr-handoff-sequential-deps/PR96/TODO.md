# PR96 — merge-step10-handoff-sync

## 概要

PR95 で `pr-handoff` スキルが「直列依存対応」になり、候補を「即時予約対象」と「依存後続候補」に分類して扱うようになった。
しかし `merge` スキル Step10 の文言は古いままで「全候補を予約する」と書かれており、
実際の pr-handoff の動作と乖離している。merge SKILL を pr-handoff の新挙動に追従させる。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する（未決定事項なし） | - `.work/tasks/.../PR96/QA.md` |
| 済 | merge SKILL.md Step10 を pr-handoff 直列依存対応に追従 | - `plugins/work-kit/skills/merge/SKILL.md` |
| 済 | merge SKILL.jp.md Step10 を pr-handoff 直列依存対応に追従 | - `plugins/work-kit/skills/merge/SKILL.jp.md` |
| 済 | plugin.json / marketplace.json のバージョン bump（PATCH） | - `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `plugins/work-kit/skills/pr-handoff/SKILL.md`: PR95 で直列依存対応になった現行の pr-handoff 仕様
- PR95 コミット `d6fe951`: pr-handoff 直列依存対応の本体実装

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| {次にやること} | {背景・目的} | {例: 即時実施可 / 「{他候補タイトル}」が完了したら} |
