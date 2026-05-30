---
paths:
  - "plugins/workspace/skills/work-start/SKILL.md"
  - "plugins/workspace/skills/work-add/SKILL.md"
  - "plugins/workspace/skills/vscode-workspace-sync/SKILL.md"
---

> ⚠️ **日本語ミラー** — Claude には自動ロードされません。このファイルを更新する際は、必ず英語本体 `.claude/rules/feature/work-start-worktree-link.md` も同時に更新してください。

# work-start ↔ worktree スキル リンクルール

## 概要

PR163 で worktree-kit プラグインを workspace に統合した。worktree 関連の 2 スキル
（`work-add` / `vscode-workspace-sync`）は workspace 配下にある。
`work-start` の Step 4 は `workspace:work-add` に委譲しているため、両者のインターフェースを揃える必要がある。

## ファイル依存関係

| 編集ファイル | 合わせて確認・更新 |
|---|---|
| `plugins/workspace/skills/work-start/SKILL.md` | `plugins/workspace/skills/work-add/SKILL.md` — インターフェース（PR番号・ブランチ引数）が一致しているか確認 |
| `plugins/workspace/skills/work-add/SKILL.md` | `plugins/workspace/skills/work-start/SKILL.md` — Step 4 の呼び出し形式と一致しているか確認 |
| `plugins/workspace/skills/vscode-workspace-sync/SKILL.md` | ネームスペースが `workspace:` であることを確認 |

## ワークツリー利用の切り替え

- worktree 利用は環境変数 `WORK_KIT_USE_WORKTREE` で切り替える（デフォルト有効）
- `false` / `0` / `no` / `off` を設定すると `work-start` はワークツリー作成をスキップし、`.work/` 管理のみで動作する
- この判定は `work-start` の Step 4 が行う

## ルールメンテナンス

- worktree 関連スキルを追加・削除・リネームした → `paths:` と依存表を更新する
- env var の意味を変えた → 概要と `work-start` Step 4 の記述を揃える
