# branch-index-cleanup SKILL.md の {PLUGIN_ROOT} 修正

## 概要

`plugins/work/skills/branch-index-cleanup/SKILL.md` の Step 3 (Class C) コマンドと Notes セクションで
`{PLUGIN_ROOT}` というプレースホルダーが使われていたため、実行時にシェル変数展開が行われず
コマンドが失敗する問題があった。全スキル共通の規約 `${CLAUDE_PLUGIN_ROOT}` に統一した。

## 修正内容

- `SKILL.md` 行 148: `python {PLUGIN_ROOT}/scripts/index-tool.py` → `python ${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py`
- `SKILL.md` 行 167: `{PLUGIN_ROOT}` 説明 → `${CLAUDE_PLUGIN_ROOT}` はプラグインルートパスを指すシェル変数
- `SKILL.jp.md` 行 149, 168: 同上（JP ミラー）

## 変更履歴

| 日付 | 変更 |
|---|---|
| 2026-06-03 | 初版 — ISSUE-140 対応 |
