# PR58 — split-work-kit-worktree

## 概要

work-kit を2つのプラグインに分割する。
- `work-kit`: .work/ フォルダ管理（TODO/QA/specs/index.yaml）
- `worktree-kit`: git worktree 管理（作成・削除・VS Code連携）

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | QA.md に未決定事項を記録する | `.work/tasks/.../PR58/QA.md` |
| - | `.work/specs/` の仕様書を更新する | `.work/specs/plugin-split.md` |
| - | 分割境界線を確定する（QA-001解決待ち） | — |
| - | `worktree-kit` プラグインを新規作成する | `plugins/worktree-kit/` |
| - | worktree関連スキルをworktree-kitへ移動する | `skills/vscode-workspace-sync/` 等 |
| - | work-start からworktree操作を分離する（方針次第） | `skills/work-start/SKILL.md` |
| - | `plugin.json` を新規・更新する | `plugins/worktree-kit/.claude-plugin/plugin.json` |
| - | `marketplace.json` を更新する | `.claude-plugin/marketplace.json` |
| - | ルール・CLAUDE.md を整備する | — |

## 参考ドキュメント

- `.work/specs/plugin-split.md`: プラグイン分割仕様（作成予定）
