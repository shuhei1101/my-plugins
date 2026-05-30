# PR181 — remove-conversation-to-claude

## 概要

`conversation-to-claude` スキル本体と、これに連動して維持していた以下のプロジェクトファイルを削除する。
- `.claude/rules/core/glossary.md`
- `.claude/rules/core/incidents.md`
- `.claude/references/incidents/`（インシデント詳細ファイル群）

`conversation-to-claude` を使わなくなったため、関連する merge ステップ・env トグル・依存ルール・claude-kit 内の参照も併せて削除する。

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | `conversation-to-claude` スキル本体・`PreCompact` フックを削除 | `plugins/claude-kit/skills/conversation-to-claude/`, `plugins/claude-kit/hooks/prompts/pre-compact.md`(+jp), `plugins/claude-kit/hooks/hooks.json` |
| 済 | claude-kit 内の `conversation-to-claude` 参照を除去 | `plugins/claude-kit/CLAUDE.md`(+jp), `skills/{skill,rule,claude}-creator/SKILL.md`(+jp), `references/glossary.md`(+jp) |
| 済 | merge スキルから旧 Step 4（c2c）を削除し Step 5〜13 を Step 4〜12 に繰り上げ | `plugins/workspace/skills/merge/SKILL.md`(+jp) |
| 済 | workspace:config から `WORK_KIT_MERGE_CONV2CLAUDE` 選択肢を削除 | `plugins/workspace/skills/config/SKILL.md`(+jp) |
| 済 | notes-to-claude から c2c 参照を除去 | `plugins/workspace/skills/notes-to-claude/SKILL.md`(+jp) |
| 済 | プロジェクトの glossary / incidents を削除 | `.claude/rules/core/glossary.md`(+jp), `.claude/rules/core/incidents.md`(+jp), `.claude/references/incidents/` |
| 済 | `.claude/rules/core/_overview.md` から glossary / incidents 行を削除 | `.claude/rules/core/_overview.md` |
| 済 | `claude-kit-skill-dependencies` ルールを削除 | `.claude/rules/feature/claude-kit-skill-dependencies.md`(+jp) |
| 済 | claude-kit / workspace のバージョンを bump し marketplace.json を更新 | `plugins/claude-kit/.claude-plugin/plugin.json`, `plugins/workspace/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |
| 済 | master 取り込み・再 bump（claude-kit 3.39.0 / workspace 2.45.0）、タスクドキュメントを新形式に移行 | 本ドキュメント |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/claude-kit/skills/conversation-to-claude/` | 削除 | スキル本体（SKILL.md / SKILL.jp.md） | - |
| `plugins/claude-kit/hooks/prompts/pre-compact.md`(+jp) | 削除 | c2c を呼び出す PreCompact 指示プロンプト | - |
| `plugins/claude-kit/hooks/hooks.json` | 編集 | `PreCompact` エントリを削除 | 残るは `PreToolUse` 注入のみ |
| `plugins/claude-kit/CLAUDE.md`(+jp) | 編集 | c2c 言及を削除、フック数の記載を更新 | - |
| `plugins/claude-kit/skills/{skill,rule,claude}-creator/SKILL.md`(+jp) | 編集 | 「呼び出し元」注記から c2c を除去 | - |
| `plugins/claude-kit/references/glossary.md`(+jp) | 編集 | 用語追記タイミング節を c2c 非依存に書き換え | - |
| `plugins/claude-kit/.claude-plugin/plugin.json` | 編集 | 3.38.0 → 3.39.0 | - |
| `plugins/workspace/skills/merge/SKILL.md`(+jp) | 編集 | Step 4 c2c を削除しステップ番号を 13→12 に繰り上げ | master 取り込み後に再適用 |
| `plugins/workspace/skills/config/SKILL.md`(+jp) | 編集 | `WORK_KIT_MERGE_CONV2CLAUDE` を管理対象から外す（8→7 トグル） | - |
| `plugins/workspace/skills/notes-to-claude/SKILL.md`(+jp) | 編集 | 関連スキル一覧・説明から c2c を除去 | - |
| `plugins/workspace/.claude-plugin/plugin.json` | 編集 | 2.43.0 → 2.45.0（master 2.44.0 と衝突回避のため再 bump） | - |
| `.claude-plugin/marketplace.json` | 編集 | claude-kit / workspace のバージョン同期 | - |
| `.claude/rules/core/glossary.md`(+jp) | 削除 | プロジェクトの glossary | - |
| `.claude/rules/core/incidents.md`(+jp) | 削除 | プロジェクトの incidents インデックス | - |
| `.claude/references/incidents/` | 削除 | インシデント詳細ファイル群（en/jp 計 80 ファイル前後） | - |
| `.claude/rules/feature/claude-kit-skill-dependencies.md`(+jp) | 削除 | c2c 中心の依存ルール | - |
| `.claude/rules/core/_overview.md` | 編集 | `plugin-work.md` のみを残す | - |
| `.work/tasks/index.yaml` | 編集 | PR181 エントリ追加 | - |
| `.work/tasks/20260530_remove-conversation-to-claude/PR181-chore-remove-conversation-to-claude.md` | 新規 | 本 PR ドキュメント（新形式） | TODO.md + QA.md を統合 |

## テスト

なし（削除中心のため）

## QA

（未決定事項なし）

## 参考ドキュメント

- なし

## 関連PR

| PR番号 | 概要 |
|---|---|
| #PR168 | task doc 構造を単一ファイル化（本 PR で新形式に追従） |
| #PR171 | claude-kit テンプレ刷新・changelogs/ 廃止方針（本 PR の changelogs/ 新規ファイルを取り下げ） |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |
