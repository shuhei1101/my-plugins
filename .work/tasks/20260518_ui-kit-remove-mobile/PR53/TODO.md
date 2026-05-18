# PR53 — ui-kit-remove-mobile

## 概要

ui-kit スキル・リファレンスからモバイル対応・レスポンシブ関連の記述を全て削除する。
PC 版のみをターゲットとし、スマホでも PC 表示で使う方針。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | - `.work/tasks/.../PR53/QA.md` |
| 済 | ui-design.jp.md からモバイル・レスポンシブ記述を削除 | - `plugins/ui-kit/references/ui-design.jp.md` |
| 済 | ui-design.md からモバイル・レスポンシブ記述を削除 | - `plugins/ui-kit/references/ui-design.md` |
| 済 | principles.jp.md からブレイクポイント・レスポンシブ記述を削除 | - `plugins/ui-kit/references/principles.jp.md` |
| 済 | principles.md からブレイクポイント・レスポンシブ記述を削除 | - `plugins/ui-kit/references/principles.md` |
| 済 | mock/SKILL.jp.md からモバイル記述を削除 | - `plugins/ui-kit/skills/mock/SKILL.jp.md` |
| 済 | mock/SKILL.md からモバイル記述を削除 | - `plugins/ui-kit/skills/mock/SKILL.md` |
| 済 | implement/SKILL.jp.md からブレイクポイント記述を削除 | - `plugins/ui-kit/skills/implement/SKILL.jp.md` |
| 済 | implement/SKILL.md からブレイクポイント記述を削除 | - `plugins/ui-kit/skills/implement/SKILL.md` |
| 済 | mock-skeleton.html からレスポンシブ CSS を削除 | - `plugins/ui-kit/skills/mock/templates/mock-skeleton.html` |
| 済 | plugin.json と marketplace.json のバージョンを bump | - `plugins/ui-kit/.claude-plugin/plugin.json` |
| 済 | `.work/specs/` の仕様書を更新する | - `.work/specs/ui-kit.md` |
| - | debug-fab: clipboard コピーに textarea フォールバックを追加(SSH/HTTP 対応) | - `plugins/ui-kit/skills/debug-fab/templates/uidev.js` |

## 参考ドキュメント

- `.work/specs/ui-kit.md`: ui-kit 設計方針
