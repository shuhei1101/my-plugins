# PR20 — fix-work-start-step8

## 概要

work-start ステップ8の内容を修正する。
不要な禁止事項を削除し、QA有無による実装開始の分岐を追加。
コミット粒度に関する補足も追加する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | ステップ8の禁止事項から「承認なしに実装開始しない」「コミット前に報告しない」を削除 | - `plugins/work-kit/skills/work-start/SKILL.jp.md`<br>- `plugins/work-kit/skills/work-start/SKILL.md` |
| 済 | 「ユーザーの承認を待つ」をQA有無で分岐させる（QA あり→確認、QA なし→即実装開始） | - `plugins/work-kit/skills/work-start/SKILL.jp.md`<br>- `plugins/work-kit/skills/work-start/SKILL.md` |
| 済 | コミットは意味のある単位で切る旨を補足に追加 | - `plugins/work-kit/skills/work-start/SKILL.jp.md`<br>- `plugins/work-kit/skills/work-start/SKILL.md` |
| 済 | work-kit バージョンを 2.6.6 → 2.6.7 に bump | - `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- なし

## QA

なし
