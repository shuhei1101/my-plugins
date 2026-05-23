# PR78 — merge-step7-next-pr-suggestion

## 概要

merge スキルの Step 7（完了報告）で、マージした PR の TODO.md に記載された「次PR候補」セクションの内容をユーザーに提示するよう更新する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | SKILL.md Step 7 を更新（次PR候補を提示する処理を追加） | - `plugins/work-kit/skills/merge/SKILL.md` |
| 済 | SKILL.jp.md Step 7 を更新（日本語版） | - `plugins/work-kit/skills/merge/SKILL.jp.md` |
| 済 | plugin.json と marketplace.json のバージョンを bump | - `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `plugins/work-kit/skills/merge/SKILL.md`: merge スキル本体
- `plugins/work-kit/templates/.work/tasks/yyyymmdd_xxx/PRXXX/TODO.md`: TODO テンプレート（次PR候補セクション含む）

## 次PR候補

| タイトル | 概要 |
|---|---|
| {次にやること} | {背景・目的} |
