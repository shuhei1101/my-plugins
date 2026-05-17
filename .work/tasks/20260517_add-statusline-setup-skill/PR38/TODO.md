# PR38 — add-statusline-setup-skill

## 概要

claude-kit プラグインに `statusline-setup` スキルを追加する。
ユーザーの `~/.claude/settings.json` の `statusLine` キーを、
現在の設定済み値（モデル名・コンテキスト使用率・レート制限を表示するPythonコマンド）に書き換えるスクリプトを実行するだけのスキル。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | SKILL.jp.md を作成 | - `plugins/claude-kit/skills/statusline-setup/SKILL.jp.md` |
| - | SKILL.md を作成（JP mirrorから翻訳） | - `plugins/claude-kit/skills/statusline-setup/SKILL.md` |
| - | 適用スクリプトを作成 | - `plugins/claude-kit/scripts/apply-statusline.py` |
| - | marketplace.json に statusline-setup を追記 | - `.claude-plugin/marketplace.json` |
| - | plugin.json のバージョンを更新 | - `plugins/claude-kit/.claude-plugin/plugin.json` |

## 参考ドキュメント

- `~/.claude/settings.json`: 現在の statusLine 設定値（実装の参考）
