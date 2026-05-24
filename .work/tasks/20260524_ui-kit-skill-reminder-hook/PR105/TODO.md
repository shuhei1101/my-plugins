# PR105 — ui-kit-skill-reminder-hook

## 概要

ui-kit プラグインに UserPromptSubmit フックを追加する。
HTML/CSS/JS の実装・編集が要求されたとき `implement` と `logging` スキルの起動を自動リマインドし、
モック作成が要求された場合はさらに `mock` スキルも案内する。
フックは hooks.json のインライン Python でキーワード検出し、"Read and follow" 形式で単一 MD ファイルへ誘導する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | hooks/hooks.json を作成（インライン Python + "Read and follow" 形式） | `plugins/ui-kit/hooks/hooks.json` |
| 済 | hooks/prompts/ui-skill-reminder.md を作成（単一ファイル・状況別案内） | `plugins/ui-kit/hooks/prompts/ui-skill-reminder.md` |
| 済 | plugin.json バージョンを 1.3.4 → 1.4.0 にバンプ | `plugins/ui-kit/.claude-plugin/plugin.json` |
| 済 | marketplace.json の ui-kit バージョンを更新 | `.claude-plugin/marketplace.json` |
| 済 | changelogs/v1.4.0.md を作成 | `plugins/ui-kit/changelogs/v1.4.0.md` |

## 参考ドキュメント

- `plugins/work-kit/hooks/hooks.json`: `${CLAUDE_PLUGIN_ROOT}` パス変数の使い方

## 次PR候補

| タイトル | 概要 |
|---|---|
| hook-creator SKILL.md 改善 | UserPromptSubmit を "Read and follow" 形式に統一・Plugin/Project パターン統合・編集例追加 |
