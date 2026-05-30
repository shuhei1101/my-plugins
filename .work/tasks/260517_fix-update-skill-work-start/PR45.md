# PR45 — fix-update-skill-work-start

## 概要

work-kit:update スキルがステップ1完了後に直接コミットしようとするバグを修正する。
ステップ1とステップ2の間に work-start スキルを実行するステップを追加することで、
必ずPRブランチ上で作業が行われるようにする。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | - `.work/tasks/20260517_fix-update-skill-work-start/PR45/QA.md` |
| 済 | `.work/specs/` の仕様書を更新する | - `.work/specs/work-kit-update-skill.md` |
| 済 | SKILL.jp.md のステップ1とステップ2の間に work-start 実行ステップを追加 | - `plugins/work-kit/skills/update/SKILL.jp.md` |
| 済 | SKILL.md に同じステップを追加（英語） | - `plugins/work-kit/skills/update/SKILL.md` |
| 済 | plugin.json と marketplace.json のバージョンを bump する | - `plugins/work-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `plugins/work-kit/skills/update/SKILL.jp.md`: 修正対象のスキル定義（日本語）
- `plugins/work-kit/skills/update/SKILL.md`: 修正対象のスキル定義（英語）

## QA

なし
