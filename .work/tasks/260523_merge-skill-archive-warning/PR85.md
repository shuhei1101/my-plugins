# PR85 — merge-skill-archive-warning

## 概要

merge スキルのステップ5（JP）/ Step 6（EN）に、`index.archive.yaml` のコミット漏れを防ぐ警告注意事項を追加する。
マージ前に必ず `index.archive.yaml` がコミット済みであることを確認させるための明示的なチェックポイントを設ける。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | `.work/tasks/.../PR85/QA.md` |
| 済 | SKILL.jp.md ステップ5に `index.archive.yaml` コミット確認の警告を追加 | `plugins/work-kit/skills/merge/SKILL.jp.md` |
| 済 | SKILL.md Step 6 に同内容の警告を追加（EN版） | `plugins/work-kit/skills/merge/SKILL.md` |
| 済 | plugin.json / marketplace.json バージョンをバンプ | `plugins/work-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `plugins/work-kit/skills/merge/SKILL.jp.md`: 修正対象

## 次PR候補

| タイトル | 概要 |
|---|---|
| {次にやること} | {背景・目的} |

## QA

なし
