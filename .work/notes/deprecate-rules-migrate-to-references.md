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
