# PR186 — rename-workspace-to-work

## 概要

PR172 で `work-kit` → `workspace` にリネームしたプラグインを、ユーザーの要望で `work` という新しい名前に変更する。
あわせてスキル名 `work-start` → `start`、`work-add` → `worktree-create`、環境変数 `WORKSPACE_*` → `WORK_*` に変更する。

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA を記録する | - |
| 済 | プラグインフォルダをリネーム `plugins/workspace/` → `plugins/work/` | - |
| 済 | `plugin.json` の name を `work` に変更 | `plugins/work/.claude-plugin/plugin.json` |
| 済 | `marketplace.json` の name・source を更新 | `.claude-plugin/marketplace.json` |
| 済 | `skills/work-start/` → `skills/start/` にフォルダリネーム | - |
| 済 | `skills/work-add/` → `skills/worktree-create/` にフォルダリネーム | - |
| 済 | 全スキル内の `workspace:work-start` → `work:start` に一括置換 | plugins/work/ 以下の全 SKILL.md |
| 済 | 全スキル内の `workspace:work-add` → `work:worktree-create` に一括置換 | plugins/work/ 以下の全 SKILL.md |
| 済 | 全スキル内の `workspace:` → `work:` に一括置換（他スキル分） | plugins/work/ 以下の全 SKILL.md |
| 済 | `WORKSPACE_*` → `WORK_*` に env 変数を変更 | hooks/scripts/*.py, hooks/hooks.json |
| 済 | ルールファイルのリネーム `workspace-*.md` → `work-*.md` | `.claude/rules/feature/` |
| 済 | ルールファイル内の `workspace:` 参照を `work:` に更新 | 上記ルールファイル |
| 済 | claude-kit references の `workspace` 参照を `work` に更新 | `plugins/claude-kit/references/` |
| 済 | glossary の `workspace` 参照を更新 | `.claude/rules/core/glossary.md` |
| 済 | `plugin.json` バージョンバンプ | `plugins/work/.claude-plugin/plugin.json` |
| 済 | JP ミラーを更新 | 変更した SKILL.md に対応する SKILL.jp.md |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/work/` (全ファイル) | リネーム/編集 | `plugins/workspace/` からフォルダリネーム | スキルフォルダ含む |
| `plugins/work/.claude-plugin/plugin.json` | 編集 | name を work に変更、v2.45.0 | |
| `plugins/work/skills/start/` | リネーム | `skills/work-start/` → `skills/start/` | SKILL.md/jp.md 内容も更新 |
| `plugins/work/skills/worktree-create/` | リネーム | `skills/work-add/` → `skills/worktree-create/` | SKILL.md/jp.md 内容も更新 |
| `plugins/work/hooks/hooks.json` | 編集 | `WORKSPACE_*` → `WORK_*` | |
| `plugins/work/hooks/scripts/*.py` | 編集 | `WORKSPACE_*` → `WORK_*` | 3ファイル |
| `plugins/work/hooks/prompts/*.md` | 編集 | `workspace:` → `work:`、`WORKSPACE_*` → `WORK_*` | 6ファイル |
| `plugins/work/templates/.work/CLAUDE.md` | 編集 | `workspace:` → `work:` | jp.md も更新 |
| `.claude-plugin/marketplace.json` | 編集 | name/source を work に更新、v2.45.0 | |
| `.claude/rules/feature/work-merge-skill-spec-sync.md` | リネーム | `workspace-merge-skill-spec-sync.md` → `work-...` | |
| `.claude/rules/feature/work-todo-template-sync.md` | リネーム | `workspace-todo-template-sync.md` → `work-...` | |
| `.claude/rules/core/glossary.md` | 編集 | `workspace:` → `work:`、`WORKSPACE_*` → `WORK_*`、歴史エントリ更新 | |
| `plugins/claude-kit/references/plugin-structure.md` | 編集 | `/workspace:work-start` → `/work:start` | jp.md も更新 |
| `.work/CLAUDE.md` | 編集 | `/work-kit:work-start` → `/work:start` | |

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| （なし） | - | - | - |

## QA

特になし。

## 参考ドキュメント

- `.claude/rules/core/glossary.md`: `WORKSPACE_*` 環境変数と workspace スキル群の定義

## 関連PR

| PR番号 | 概要 |
|---|---|
| #172 | work-kit → workspace リネーム（今回はこれを別名 work に変更） |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |
