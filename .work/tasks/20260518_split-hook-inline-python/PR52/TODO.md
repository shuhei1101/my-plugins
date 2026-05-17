# PR52 — split-hook-inline-python

## 概要

`plugin-structure` スキル観点のレビューで挙がった次の 2 点を解消する:

1. `guard-kit` / `work-kit` の `hooks.json` に詰め込まれたインライン Python ワンライナーを
   `hooks/scripts/*.py` に切り出し、各スクリプト冒頭に「何のフックか」を説明するコメントを付与する
   （JSON にコメントは書けないため、Python ファイル側にドキュメントを置く）
2. `work-kit/skills/setup/SKILL.md`（と `.jp.md`）の `${CLAUDE_SKILL_DIR}` 参照を
   標準の `${CLAUDE_PLUGIN_ROOT}` に置き換える

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | QA.md に未決定事項を記録する | - `.work/tasks/20260518_split-hook-inline-python/PR52/QA.md` |
| - | guard-kit: `git-guard.py` を切り出してコメント付与 | - `plugins/guard-kit/hooks/scripts/git-guard.py`<br>- `plugins/guard-kit/hooks/hooks.json` |
| - | work-kit: `master-commit-guard.py` を切り出してコメント付与 | - `plugins/work-kit/hooks/scripts/master-commit-guard.py`<br>- `plugins/work-kit/hooks/hooks.json` |
| - | work-kit: `user-prompt-submit.py` を切り出してコメント付与 | - `plugins/work-kit/hooks/scripts/user-prompt-submit.py` |
| - | work-kit: `stop.py` を切り出してコメント付与 | - `plugins/work-kit/hooks/scripts/stop.py` |
| - | setup skill の `${CLAUDE_SKILL_DIR}` を `${CLAUDE_PLUGIN_ROOT}` に統一 | - `plugins/work-kit/skills/setup/SKILL.md`<br>- `plugins/work-kit/skills/setup/SKILL.jp.md` |
| - | spec を更新（guard-kit / work-kit-stop-hook） | - `.work/specs/guard-kit.md`<br>- `.work/specs/work-kit-stop-hook.md` |
| - | guard-kit / work-kit の `plugin.json` バージョン bump | - `plugins/guard-kit/.claude-plugin/plugin.json`<br>- `plugins/work-kit/.claude-plugin/plugin.json` |
| - | `marketplace.json` のバージョンを揃える | - `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `.work/specs/guard-kit.md`: guard-kit のフック仕様
- `.work/specs/work-kit-stop-hook.md`: work-kit stop フックの仕様
