# PR202 — fix-pr179-merge-fallout

## 概要

PR179 を master へマージした際の取り違え修正に加え、追加スコープとして `dev-kit:yaml` スキル一式を削除する後始末 PR。

**含まれる変更**:

1. **PR179 merge fallout の修正**:
   `plugins/claude-kit/changelogs/v3.43.0.md` の内容が PR184 のもの（plugin-update スキル追加）になっていたのを、本来の PR179 内容（underscore rename + 並列 plugin 名整理）に書き戻し。merge 時の add/add コンフリクト解消で `git checkout --ours` を誤適用した結果。
2. **`dev-kit:yaml` スキル一式の削除（追加スコープ）**:
   YAML ファイル管理の規約（`index.yaml` / `settings.yaml` / `settings.yaml.sample` の三層パターン等）は dev-kit のスコープ外として整理。スキル本体・注入リファレンス・dispatch フック・プロンプト・該当する injection_rules パターンをすべて削除。
3. **master 取り込み**:
   PR179 merge 後に master が PR184/189/192/194/187/188/196/197/198/199/200/203/204 等で大幅進行していたため、`git merge master --no-edit` で取り込み済み。

なお、`dev-kit/_injection_rules.yaml` の PR194 日本語コメント翻訳が regressed したと当初疑ったが、PR194 のコミットメッセージに「dev-kit はコメント無しのため変更なし」と明記されていたため対応不要と確認した。

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | `claude-kit/changelogs/v3.43.0.md` の内容を PR179 本来のものに書き戻し | `plugins/claude-kit/changelogs/v3.43.0.md` |
| 済 | `git merge master --no-edit` で master を取り込み | 各種 |
| 済 | `dev-kit:yaml` スキル・リファレンス・フック・プロンプトを削除 | `plugins/dev-kit/skills/yaml/`<br>`plugins/dev-kit/references/yaml/`<br>`plugins/dev-kit/hooks/scripts/yaml_skill_dispatch.py`<br>`plugins/dev-kit/hooks/prompts/yaml-skill-dispatch.{md,jp.md}` |
| 済 | `hooks/hooks.json` から `yaml_skill_dispatch` 2 エントリ削除 | `plugins/dev-kit/hooks/hooks.json` |
| 済 | `_index.yaml` / `_index.jp.yaml` から `yaml/yaml.md` エントリ削除 | `plugins/dev-kit/references/_index.yaml`<br>`plugins/dev-kit/references/_index.jp.yaml` |
| 済 | `_injection_rules.yaml` から YAML 注入パターン 3 件削除 | `plugins/dev-kit/references/_injection_rules.yaml` |
| 済 | `CLAUDE.md` (+ `.jp.md`) から yaml スキル / hook / フォルダ言及削除、version history 表に v4.8.0 行追加 | `plugins/dev-kit/CLAUDE.md` (+ `.jp.md`) |
| 済 | `references/python/llm/prompts-authoring.{md,jp.md}` と `references/python/shared/secrets-and-env.{md,jp.md}` の `dev-kit:yaml` 言及削除 | 各ファイル |
| 済 | dev-kit バージョン bump 4.7.0 → 4.8.0、description から YAML 削除 | `plugins/dev-kit/.claude-plugin/plugin.json`<br>`.claude-plugin/marketplace.json` |
| 済 | v4.8.0 changelog 作成 | `plugins/dev-kit/changelogs/v4.8.0.md` |
| 済 | スモーク検証: dev-kit 注入フックが exit 0 | - |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/claude-kit/changelogs/v3.43.0.md` | 編集 | PR179 本来の changelog に書き戻し | merge 時の `--ours` 取り違え修正 |
| `plugins/dev-kit/skills/yaml/SKILL.md` (+ `.jp.md`) | 削除 | スキル本体 | - |
| `plugins/dev-kit/references/yaml/yaml.md` (+ `.jp.md`) | 削除 | 注入リファレンス | フォルダ自体も削除 |
| `plugins/dev-kit/hooks/scripts/yaml_skill_dispatch.py` | 削除 | dispatch フック | - |
| `plugins/dev-kit/hooks/prompts/yaml-skill-dispatch.md` (+ `.jp.md`) | 削除 | フックプロンプト | - |
| `plugins/dev-kit/hooks/hooks.json` | 編集 | `yaml_skill_dispatch.py` 参照削除（Edit / Write の両方） | - |
| `plugins/dev-kit/references/_index.yaml` (+ `_index.jp.yaml`) | 編集 | `yaml/yaml.md` エントリ削除 | - |
| `plugins/dev-kit/references/_injection_rules.yaml` | 編集 | YAML 注入パターン 3 件削除 | - |
| `plugins/dev-kit/CLAUDE.md` (+ `.jp.md`) | 編集 | yaml 言及削除 + v4.8.0 行追加 | - |
| `plugins/dev-kit/references/python/llm/prompts-authoring.md` (+ `.jp.md`) | 編集 | `dev-kit:yaml` 言及削除 | - |
| `plugins/dev-kit/references/python/shared/secrets-and-env.md` (+ `.jp.md`) | 編集 | `dev-kit:yaml` 言及削除 | - |
| `plugins/dev-kit/.claude-plugin/plugin.json` | 編集 | 4.7.0 → 4.8.0、description から YAML 削除 | - |
| `.claude-plugin/marketplace.json` | 編集 | dev-kit version + description 同期 | - |
| `plugins/dev-kit/changelogs/v4.8.0.md` | 新規 | PR202 YAML 削除 changelog | - |

## テスト

テストファイル変更なし。手動でスモーク確認:

| ファイル名 | 内容 | 補足 |
|---|---|---|
| - | `CLAUDE_PLUGIN_ROOT=plugins/dev-kit DEV_KIT_*=true python3 plugins/dev-kit/hooks/scripts/inject_references.py` がダミー stdin で exit 0 | YAML パターン削除後も注入フックが正常動作 |

## QA

未決定事項なし。

## 参考ドキュメント

- `plugins/dev-kit/CLAUDE.md`: yaml 削除後の dev-kit 構成
- `plugins/dev-kit/changelogs/v4.8.0.md`: 本 PR の dev-kit 側 changelog

## 関連PR

| PR番号 | 概要 |
|---|---|
| #PR179 | prefix-underscore-injection-config（merge fallout の原因となった PR） |
| #PR184 | claude-kit-plugin-update-skill（v3.43.0.md に内容が誤って複製された PR） |
| #PR194 | translate-injection-rules-comments-to-japanese（誤検出として除外） |
| #PR199 | dev-kit-references-yaml-subfolder（削除対象の `yaml/` サブフォルダを導入していた PR） |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |
