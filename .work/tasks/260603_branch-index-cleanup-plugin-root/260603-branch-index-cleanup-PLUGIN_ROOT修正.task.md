# branch-index-cleanup の {PLUGIN_ROOT} を ${CLAUDE_PLUGIN_ROOT} に修正

**ブランチ**: fix/branch-index-cleanup-plugin-root
**作成日**: 2026-06-03

## 作業内容

- [x] `plugins/work/skills/branch-index-cleanup/SKILL.md` 行 148 の `{PLUGIN_ROOT}` を `${CLAUDE_PLUGIN_ROOT}` に修正 済
- [x] `plugins/work/skills/branch-index-cleanup/SKILL.md` 行 167 の `{PLUGIN_ROOT}` の説明文を更新 済
- [x] `plugins/work/skills/branch-index-cleanup/SKILL.jp.md` の同箇所を EN に合わせて修正 済

## QA

（未解決の QA なし）

## テスト

- grep で `{PLUGIN_ROOT}` の全出現が 0 件になることを確認
- 他スキル（start/SKILL.md など）と同形式になっていることを確認

## 変更内容

SKILL.md 行 148: `python {PLUGIN_ROOT}/scripts/index-tool.py` → `python ${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py`
SKILL.md 行 167: `{PLUGIN_ROOT}` 説明文 → `${CLAUDE_PLUGIN_ROOT}` に更新
SKILL.jp.md 行 149, 168: 同上

## 関連イシュー

| イシュー | タイトル | ステータス |
|---|---|---|
| ISSUE-140 | branch-index-cleanup の {PLUGIN_ROOT} が ${CLAUDE_PLUGIN_ROOT} と不統一・未定義 | in_progress |

## 参考ドキュメント

- `.work/notes/バグ・不具合/branch-index-cleanup-plugin-root-fix.md`
