# PR186 — rename-workspace-to-work

## 概要

PR172 で `work-kit` → `workspace` にリネームしたプラグインを、ユーザーの要望で `work` という新しい名前に変更する。
あわせてスキル名 `work-start` → `start`、`work-add` → `worktree-create`、環境変数 `WORKSPACE_*` → `WORK_*` に変更する。

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | QA を記録する | - |
| - | プラグインフォルダをリネーム `plugins/workspace/` → `plugins/work/` | - |
| - | `plugin.json` の name を `work` に変更 | `plugins/work/.claude-plugin/plugin.json` |
| - | `marketplace.json` の name・source を更新 | `.claude-plugin/marketplace.json` |
| - | `skills/work-start/` → `skills/start/` にフォルダリネーム | - |
| - | `skills/work-add/` → `skills/worktree-create/` にフォルダリネーム | - |
| - | 全スキル内の `workspace:work-start` → `work:start` に一括置換 | plugins/work/ 以下の全 SKILL.md |
| - | 全スキル内の `workspace:work-add` → `work:worktree-create` に一括置換 | plugins/work/ 以下の全 SKILL.md |
| - | 全スキル内の `workspace:` → `work:` に一括置換（他スキル分） | plugins/work/ 以下の全 SKILL.md |
| - | `WORKSPACE_*` → `WORK_*` に env 変数を変更 | hooks/scripts/*.py, hooks/hooks.json |
| - | ルールファイルのリネーム `workspace-*.md` → `work-*.md` | `.claude/rules/feature/` |
| - | ルールファイル内の `workspace:` 参照を `work:` に更新 | 上記ルールファイル |
| - | claude-kit references の `workspace` 参照を `work` に更新 | `plugins/claude-kit/references/` |
| - | glossary の `workspace` 参照を更新 | `.claude/rules/core/glossary.md` |
| - | `plugin.json` バージョンバンプ | `plugins/work/.claude-plugin/plugin.json` |
| - | JP ミラーを更新 | 変更した SKILL.md に対応する SKILL.jp.md |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| （実装後に記入） | - | - | - |

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
