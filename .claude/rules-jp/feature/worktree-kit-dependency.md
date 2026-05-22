---
paths:
  - "plugins/work-kit/skills/work-start/SKILL.md"
  - "plugins/worktree-kit/skills/work-add/SKILL.md"
  - "plugins/worktree-kit/skills/vscode-workspace-sync/SKILL.md"
---

> ⚠️ **日本語ミラー** — Claude には自動ロードされません。このファイルを更新する際は、必ず英語本体 `.claude/rules/feature/worktree-kit-dependency.md` も同時に更新してください。

# worktree-kit 依存関係ルール

## プラグイン構成

このプロジェクトでは work-kit と worktree-kit を分離して管理している。

| プラグイン | 責務 |
|---|---|
| `work-kit` | `.work/` フォルダ管理、PRライフサイクル（TODO/QA/index.yaml） |
| `worktree-kit` | git worktree の作成・削除・VS Code連携 |

## ファイル依存関係

`work-start` の Step 4 は `worktree-kit:work-add` に委譲している:

| 編集ファイル | 合わせて確認・更新 |
|---|---|
| `plugins/work-kit/skills/work-start/SKILL.md` | `plugins/worktree-kit/skills/work-add/SKILL.md` — インターフェース（PR番号・ブランチ引数）が一致しているか確認 |
| `plugins/worktree-kit/skills/work-add/SKILL.md` | `plugins/work-kit/skills/work-start/SKILL.md` — Step 4 の呼び出し形式と一致しているか確認 |
| `plugins/worktree-kit/skills/vscode-workspace-sync/SKILL.md` | ネームスペースが `worktree-kit:` であることを確認（旧 `work-kit:`） |

## インストール方針

- worktree を使わないプロジェクト → `work-kit` のみインストール
- worktree を使うプロジェクト → `work-kit` + `worktree-kit` の両方をインストール
- `work-start` は worktree-kit 未インストール時でも動作する（worktree 作成をスキップ）
