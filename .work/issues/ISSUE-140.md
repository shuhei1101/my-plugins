# ISSUE-140: branch-index-cleanup の {PLUGIN_ROOT} が ${CLAUDE_PLUGIN_ROOT} と不統一・未定義

**作成日**: 2026-06-02

# ユーザー回答欄

> 各 `**回答**:` 行で不要な選択肢を消して 1 つだけ残す。

## 意思

このイシューに対応するか。

**回答**: 対応する / 対応しない / 様子見

---

## 概要

`plugins/work/skills/branch-index-cleanup/SKILL.md` の Step 3 で `index-tool.py` を呼ぶコマンドが `{PLUGIN_ROOT}` というプレースホルダーを使っているが、他のすべてのスキルは `${CLAUDE_PLUGIN_ROOT}` というシェル変数を使っている。`{PLUGIN_ROOT}` はシェル変数でもなくプレースホルダーでもあいまいで、そのまま実行すると `{PLUGIN_ROOT}` という文字列パスとして解釈されコマンドが失敗する。

## 背景

incidents No.24 (`claude-plugin-root-unset-manual-steps`) が示す通り、`${CLAUDE_PLUGIN_ROOT}` は Claude Code のプラグイン実行コンテキストで自動設定されるシェル変数。スキル本文でスクリプトパスを参照するときは `${CLAUDE_PLUGIN_ROOT}` を使うのが全スキルを通じた規約。

## 現状

`plugins/work/skills/branch-index-cleanup/SKILL.md`:
- 行 148: `python {PLUGIN_ROOT}/scripts/index-tool.py add .work/tasks/index.yaml \`
- 行 167: `- `{PLUGIN_ROOT}` refers to the workspace plugin root path`

他のスキル（merge, start, issue-resolve など）はすべて `python "${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py"` の形式を使っている。

## 期待される状態

- `{PLUGIN_ROOT}` を `"${CLAUDE_PLUGIN_ROOT}"` に修正する
- Notes の説明文も削除または「`${CLAUDE_PLUGIN_ROOT}` はプラグインルートパスを指すシェル変数」に更新する

## 対応案

`plugins/work/skills/branch-index-cleanup/SKILL.md` 行 148 の `{PLUGIN_ROOT}` を `"${CLAUDE_PLUGIN_ROOT}"` に置換し、行 167 の `{PLUGIN_ROOT}` の説明も合わせて修正する。

## 横展開

同様の間違いが他スキルに波及していないか確認済み（他スキルはすべて `${CLAUDE_PLUGIN_ROOT}` を使用）。本件は branch-index-cleanup のみ。
