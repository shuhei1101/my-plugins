# PR40 — fix-py-kit-plugin-root-path

## 概要

py-kit の `py-project` と `py-new-project` の SKILL.md に、`{plugin_root}` がスキルディレクトリの2階層上であることの説明が欠けており、Claudeがパスを誤解釈してエラーになる問題を修正する。

`py-script/SKILL.md` にはすでに説明が存在する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | py-project SKILL.md に plugin_root の説明を追加 | - `plugins/py-kit/skills/py-project/SKILL.md` |
| 済 | py-project SKILL.jp.md を更新 | - `plugins/py-kit/skills/py-project/SKILL.jp.md` |
| 済 | py-new-project SKILL.md に plugin_root の説明を追加 | - `plugins/py-kit/skills/py-new-project/SKILL.md` |
| 済 | py-new-project SKILL.jp.md を更新 | - `plugins/py-kit/skills/py-new-project/SKILL.jp.md` |
| 済 | plugin.json のバージョンをバンプ | - `plugins/py-kit/.claude-plugin/plugin.json` |
| 済 | marketplace.json を更新 | - `.claude-plugin/marketplace.json` |

## 参考ドキュメント

なし

## QA

なし
