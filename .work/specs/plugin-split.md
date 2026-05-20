# Plugin Split Spec — work-kit / worktree-kit

## 目的

work-kit の責務が「.work/ フォルダ管理」と「git worktree 管理」の2つに混在しているため、
プラグインとして分割し責務を明確にする。

---

## 分割方針

### work-kit（既存プラグイン — 縮小）

**責務**: `.work/` フォルダ構造の管理、PRライフサイクルの管理

| コンポーネント | 内容 |
|---|---|
| skills | work-start, merge, setup, update |
| hooks | master-commit-guard, stop, user-prompt-submit |
| scripts | index-tool.py, setup-task.py, trim-index.py |
| templates | .work/ 以下のテンプレート群 |

### worktree-kit（新規プラグイン）

**責務**: git worktree の作成・削除・外部ツール連携

| コンポーネント | 内容 |
|---|---|
| skills | vscode-workspace-sync（work-kit から移動） |
| その他 | 方針次第で追加（→ QA-001参照） |

---

## 未決定事項

- QA-001: work-start 内の `git worktree add` を worktree-kit へ切り出すか（狭い / 広い解釈）

---

## 関連ファイル

- `plugins/work-kit/` — 既存プラグイン
- `plugins/worktree-kit/` — 新規作成（このPRで作成）
- `.claude-plugin/marketplace.json` — カタログに worktree-kit を追加
