# PR142 — add-j2-support-to-mark-generated

## 概要

`mark-generated` スキルに Jinja2 テンプレート（`.j2`）ファイルのサポートを追加する。
Step 3 の対応表に `.j2` を追加し、`hooks.json` に `.j2` ファイルを編集しようとしたときに一度ブロックして mark-generated スタンプの挿入を促す PreToolUse フックを追加する。

### 実施条件

即時実施可

### 関連PR

| PR番号 | 概要 |
|---|---|
| - | - |

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | - `.work/tasks/.../PR142/QA.md` |
| 済 | mark-generated SKILL.md Step 3 に `.j2` を追加 | - `plugins/claude-kit/skills/mark-generated/SKILL.md` |
| 済 | SKILL.jp.md も同期更新 | - `plugins/claude-kit/skills/mark-generated/SKILL.jp.md` |
| 済 | hooks.json に `.j2` 用 PreToolUse フックを追加 | - `plugins/claude-kit/hooks/hooks.json` |
| 済 | フックプロンプトを作成 | - `plugins/claude-kit/hooks/prompts/j2-stamp-check.md` |
| 済 | フックプロンプトの JP ミラーを作成 | - `plugins/claude-kit/hooks/prompts/j2-stamp-check.jp.md` |
| 済 | plugin.json / marketplace.json のバージョンを更新 | - `plugins/claude-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `.work/notes/generator-metadata.md`: mark-generated スキルの仕様ノート
- `plugins/claude-kit/hooks/hooks.json`: 既存フックの実装パターン（セッションフラグ型）

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |
