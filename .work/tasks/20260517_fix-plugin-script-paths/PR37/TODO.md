# PR37 — fix-plugin-script-paths

## 概要

スキル内のスクリプト参照パスが `plugins/work-kit/scripts/` というリポジトリ相対パスになっており、
`my-plugins` 以外のプロジェクトでは動作しない問題を修正する。
`${CLAUDE_PLUGIN_ROOT}/scripts/` を使うことでプラグインキャッシュ内のスクリプトを参照できるようにする。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | work-start のスクリプトパスを ${CLAUDE_PLUGIN_ROOT}/scripts/ に変更 | - `plugins/work-kit/skills/work-start/SKILL.md`<br>- `plugins/work-kit/skills/work-start/SKILL.jp.md` |
| 済 | merge のスクリプトパスを ${CLAUDE_PLUGIN_ROOT}/scripts/ に変更 | - `plugins/work-kit/skills/merge/SKILL.md`<br>- `plugins/work-kit/skills/merge/SKILL.jp.md` |
| 済 | plugin.json と marketplace.json のバージョンを bump | - `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |
| - | plugin-work ルールに ${CLAUDE_PLUGIN_ROOT}/scripts/ パス規約を追記 | - `.claude/rules/plugin-work.md`<br>- `.claude/rules-jp/plugin-work.md` |

## 参考ドキュメント

- なし
