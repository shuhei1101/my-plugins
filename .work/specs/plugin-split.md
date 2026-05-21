# Plugin Split Spec — work-kit / worktree-kit

## 目的

work-kit の責務が「.work/ フォルダ管理」と「git worktree 管理」の2つに混在しているため、
プラグインとして分割し責務を明確にする。

**動機**: worktree を使わないプロジェクトでは work-kit だけインストールして運用できるようにする。
worktree-kit は必要なプロジェクトにのみ追加インストールする。

---

## 分割方針（QA-001 決定済み — 広い解釈 B）

### work-kit（既存プラグイン — 縮小）

**責務**: `.work/` フォルダ構造の管理、PRライフサイクルの管理

| コンポーネント | 内容 |
|---|---|
| skills | work-start, merge, setup, update |
| hooks | master-commit-guard, stop, user-prompt-submit |
| scripts | index-tool.py, setup-task.py, trim-index.py |
| templates | .work/ 以下のテンプレート群 |

**work-start の変更**:
- Step 4（`git worktree add`）を worktree-kit に委譲
- worktree-kit がインストールされていない場合は worktree 作成をスキップし、その旨をユーザーに通知
- ワークツリーなしでも .work/ フォルダ管理・TODO/QA は動作する

### worktree-kit（新規プラグイン）

**責務**: git worktree の作成・削除・外部ツール連携

| コンポーネント | 内容 |
|---|---|
| skills | work-add（worktree作成）, vscode-workspace-sync（work-kit から移動） |
| hooks | hooks.json（minimal 構成） |

**work-add スキル**:
- `work-start` から呼び出される: `/worktree-kit:work-add PR{N} {type}/{title}`
- `git worktree add -b PR{N}/{type}/{title} ../repo-wt-PR{N}` を実行
- 単独でも呼び出し可能

---

## ファイル変更一覧

| 操作 | ファイル |
|---|---|
| 新規作成 | `plugins/worktree-kit/.claude-plugin/plugin.json` |
| 新規作成 | `plugins/worktree-kit/skills/work-add/SKILL.md` |
| 新規作成 | `plugins/worktree-kit/skills/work-add/SKILL.jp.md` |
| 移動（コピー後編集） | `plugins/work-kit/skills/vscode-workspace-sync/` → `plugins/worktree-kit/skills/vscode-workspace-sync/` |
| 削除 | `plugins/work-kit/skills/vscode-workspace-sync/` |
| 更新 | `plugins/work-kit/skills/work-start/SKILL.md` — Step 4 を worktree-kit に委譲 |
| 更新 | `plugins/work-kit/skills/work-start/SKILL.jp.md` |
| 更新 | `plugins/work-kit/.claude-plugin/plugin.json` — version bump |
| 更新 | `.claude-plugin/marketplace.json` — worktree-kit を追加 |

---

## 関連ファイル

- `plugins/work-kit/` — 既存プラグイン
- `plugins/worktree-kit/` — 新規作成（このPRで作成）
- `.claude-plugin/marketplace.json` — カタログに worktree-kit を追加
