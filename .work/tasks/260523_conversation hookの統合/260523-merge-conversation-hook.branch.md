# PR84 — merge-conversation-hook

## 概要

work-kit:merge スキルにおいて、マージ実行前に claude-kit プラグインがインストールされているか確認し、インストール済みの場合は `conversation-to-claude` スキルを実行してからマージするフローを追加する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | `.work/tasks/20260523_merge-conversation-hook/PR84/QA.md` |
| 済 | `.work/specs/` の仕様書を確認・更新する | `.work/specs/` |
| 済 | merge SKILL.md に Step 3 を追加（claude-kit 検出 → conversation-to-claude 実行） | `plugins/work-kit/skills/merge/SKILL.md` |
| 済 | plugin.json と marketplace.json のバージョンをバンプする | `plugins/work-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |
| 済 | SKILL.jp.md を SKILL.md に同期する | `plugins/work-kit/skills/merge/SKILL.jp.md` |
| 済 | claude-kit 検出方法をbashからスキル一覧チェックに変更する | `plugins/work-kit/skills/merge/SKILL.md`, `SKILL.jp.md` |

## 参考ドキュメント

- `plugins/work-kit/skills/merge/SKILL.md`: 現行のマージフロー定義
- `plugins/claude-kit/skills/conversation-to-claude/SKILL.md`: 実行対象スキル

## 次PR候補

| タイトル | 概要 |
|---|---|
| {次にやること} | {背景・目的} |

## QA

なし
