# PR55 — fix-debug-fab-copy-return

## 概要

debug-fab スキルで、要素選択モード中にコピーボタンを押したとき、モーダルに戻らずトップ画面へ直接遷移するよう挙動を修正する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | - `.work/tasks/.../PR55/QA.md` |
| 済 | `.work/specs/` の仕様書を更新する | - `.work/specs/ui-kit.md` |
| 済 | SKILL.md の要素選択コピー後の遷移を「モーダルへ戻る」→「トップ画面へ戻る」に修正 | - `plugins/ui-kit/skills/debug-fab/SKILL.md` |
| 済 | SKILL.jp.md も同様に修正 | - `plugins/ui-kit/skills/debug-fab/SKILL.jp.md` |

## 参考ドキュメント

- `.work/specs/ui-kit.md`: ui-kit スキル仕様

## QA

なし
