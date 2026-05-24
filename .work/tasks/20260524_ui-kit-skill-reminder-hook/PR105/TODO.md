# PR105 — ui-kit-skill-reminder-hook

## 概要

ui-kit プラグインに UserPromptSubmit フックを追加する。
HTML/CSS/JS の実装・編集が要求されたとき `implement` と `logging` スキルの起動を自動リマインドし、
モック作成が要求された場合はさらに `mock` スキルも案内する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| x | hooks/hooks.json を作成 | `plugins/ui-kit/hooks/hooks.json` |
| x | hooks/scripts/user-prompt-submit.py を作成 | `plugins/ui-kit/hooks/scripts/user-prompt-submit.py` |
| x | hooks/prompts/base.md を作成（implement + logging リマインダー） | `plugins/ui-kit/hooks/prompts/base.md` |
| x | hooks/prompts/with-mock.md を作成（implement + logging + mock リマインダー） | `plugins/ui-kit/hooks/prompts/with-mock.md` |
| x | plugin.json バージョンを 1.3.4 → 1.4.0 にバンプ | `plugins/ui-kit/.claude-plugin/plugin.json` |
| x | marketplace.json の ui-kit バージョンを更新 | `.claude-plugin/marketplace.json` |
| x | changelogs/v1.4.0.md を作成 | `plugins/ui-kit/changelogs/v1.4.0.md` |

## 参考ドキュメント

- `plugins/work-kit/hooks/hooks.json`: フック構成の参考（`${CLAUDE_PLUGIN_ROOT}` パス変数の使い方）
- `plugins/work-kit/hooks/scripts/user-prompt-submit.py`: スクリプト構成の参考

## 次PR候補

| タイトル | 概要 |
|---|---|
| {次にやること} | {背景・目的} |
