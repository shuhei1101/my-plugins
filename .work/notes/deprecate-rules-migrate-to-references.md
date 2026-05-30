---
created_at: 2026-05-30
updates:
  - 2026-05-30 — 初版作成（PR203）
related_specs: []
related_prs:
  - PR197
  - PR203
---

# deprecate-rules-migrate-to-references — .claude/rules/ 廃止とリファレンス移行

## 概要

`.claude/rules/` 配下のパス一致ルールファイル群を廃止し、
各プラグインの `references/` フォルダに統合する計画。

## 背景と決定経緯

PR197（plugin-work-rule-add-claude-md-check）でプラグインの整合性チェックを追加する際、
ルールファイルへの追記ではなくリファレンスファイルへの追記を選択した。
その理由: `.claude/rules/` はプロジェクトローカルのファイルであり、
プラグインの知識はプラグイン自身の `references/` に持つべきというアーキテクチャ方針から。

## 移行マッピング（仮）

| 現在のルールファイル | 移行先 |
|---|---|
| `core/plugin-work.md` | `plugins/claude-kit/references/plugin-structure.md` に統合済み（PR197） |
| `feature/claude-md-jp-mirror-sync.md` | `plugins/claude-kit/references/` |
| `feature/skill-jp-mirror-sync.md` | `plugins/claude-kit/references/` |
| `feature/hook-prompts-jp-mirror-sync.md` | `plugins/claude-kit/references/` |
| `feature/references-jp-mirror-sync.md` | `plugins/claude-kit/references/` |
| `feature/kit-hooks-index-sync.md` | `plugins/claude-kit/references/` |
| `feature/debug-fab-template-sync.md` | `plugins/dev-kit/references/` |
| `feature/incidents-glossary-jp-mirror-sync.md` | `plugins/work/references/` |
| `feature/work-kit-stop-prompt-sync.md` | `plugins/work/references/` |
| `feature/work-merge-skill-spec-sync.md` | `plugins/work/references/` |
| `feature/work-start-worktree-link.md` | `plugins/work/references/` |
| `feature/work-todo-template-sync.md` | `plugins/work/references/` |

## 移行方針

1. ルールファイルの内容（チェックリスト・概要・説明）を移行先リファレンスの適切なセクションに追記
2. 移行先に対応する injection_rules.yaml（`_injection_rules.yaml`）でリファレンス注入を設定
3. 元のルールファイルと `.claude/rules-jp/` の対応ファイルを削除
4. CLAUDE.md からルール参照を削除

## PR203 実施結果

### 移行完了

| 旧ルールファイル | 移行先 | 方法 |
|---|---|---|
| `core/plugin-work.md` | `claude-kit/references/plugin-structure.md` | PR197 で完了済み |
| `feature/claude-md-jp-mirror-sync.md` | `claude-kit/references/claude-md.md` | 追記 |
| `feature/skill-jp-mirror-sync.md` | `claude-kit/references/skills.md` | 追記 |
| `feature/hook-prompts-jp-mirror-sync.md` | `claude-kit/references/hooks.md` | 追記 |
| `feature/references-jp-mirror-sync.md` | `claude-kit/references/references-sync.md` | 新規ファイル |
| `feature/kit-hooks-index-sync.md` | `claude-kit/references/kit-hooks-sync.md` | 新規ファイル |
| `feature/debug-fab-template-sync.md` | `dev-kit/references/html/debug-fab-sync.md` | 新規ファイル |
| `feature/work-kit-stop-prompt-sync.md` | `work/references/work-stop-prompt-sync.md` | 新規ファイル |
| `feature/work-merge-skill-spec-sync.md` | `work/references/work-merge-skill-sync.md` | 新規ファイル |
| `feature/work-start-worktree-link.md` | `work/references/work-start-skill-sync.md` | 新規ファイル |
| `feature/work-todo-template-sync.md` | `work/references/work-todo-template-sync.md` | 新規ファイル |
| `feature/incidents-glossary-jp-mirror-sync.md` | （削除のみ） | 参照先ファイルが存在しないため移行不要 |

### work プラグインへの注入インフラ追加

`work/references/` 新設に伴い、以下を追加:
- `hooks/scripts/inject_references.py`（claude-kit から fork、WORK prefix で置換）
- `hooks/scripts/_common.py`（ENV_PREFIX: WORKSPACE → WORK に更新）
- `hooks/templates/injection.md.j2` / `injection.jp.md.j2`
- `hooks/hooks.json` に Edit/Write/MultiEdit/Read フックを追加
