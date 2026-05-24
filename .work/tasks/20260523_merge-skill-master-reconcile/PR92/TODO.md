# PR92 — merge-skill-master-reconcile

## 概要

merge スキルの Step2（TODO確認）と Step3（conversation-to-claude）の間に、master との差分確認・適合ステップを追加する。
PR ブランチが長期間続いた場合などに master 側で変更が入っていても、その背景を考慮したうえで PR 側の変更と適合させてからマージできるようにする。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | `.work/tasks/20260523_merge-skill-master-reconcile/PR92/QA.md` |
| 済 | SKILL.md に新 Step3（master 適合確認）を追加し、既存ステップ番号を繰り下げる | `plugins/work-kit/skills/merge/SKILL.md` |
| 済 | SKILL.jp.md に同内容を反映する（JP ミラー） | `plugins/work-kit/skills/merge/SKILL.jp.md` |
| 済 | 概要セクション（冒頭サマリ行）を更新する | `plugins/work-kit/skills/merge/SKILL.md`, `SKILL.jp.md` |
| 済 | plugin.json・marketplace.json のバージョンを bump する | `plugins/work-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |
| 済 | ルール・CLAUDE.md を整備する | — |
| 済 | Step3: 「停止してユーザーに確認」を廃止し、Claude が自律判断で完結するよう変更 | `SKILL.md`, `SKILL.jp.md` |
| 済 | Step3: 重複検出を「ファイル直接一致のみ」から「間接依存（呼び出し元・import 元も含む）」の文脈判断に変更 | `SKILL.md`, `SKILL.jp.md` |
| 済 | Step3: 判断軸に影響範囲・インターフェース変更・意図の方向性を追加 | `SKILL.md`, `SKILL.jp.md` |

## 参考ドキュメント

- `plugins/work-kit/skills/merge/SKILL.md`: 現行マージスキル定義

## 次PR候補

| タイトル | 概要 |
|---|---|
| — | — |
