# PR99 — merge-next-pr-list-with-status

## 概要

merge スキル Step 10 の「次PR提示」を 3 カテゴリに分けて表示する。
現状は `.work/tasks/` 内の進行中 PR を未分類で羅列するだけだが、
ユーザーが「いま着手できる PR」を一目で判別できるようにする。

3 カテゴリ:

- 🟢 **着手可能**: 予約済みでまだ作業されていない PR（`git log master..{branch} --oneline | wc -l` ≤ 1）
- 🟡 **進行中**: 他セッションで作業中の PR（コミット数 ≥ 2）
- 🔴 **条件あり・着手不可**: 今マージした PR の `## 次PR候補` のうち、実施条件が他候補依存になっているもの

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md は記録なし（未決定事項なし） | - `.work/tasks/20260524_merge-next-pr-list-with-status/PR99/QA.md` |
| 済 | merge SKILL.md / SKILL.jp.md の Step 10 を Step 10/11/12 に分割し 3 カテゴリ表示仕様に書き換え | - `plugins/work-kit/skills/merge/SKILL.md`<br>- `plugins/work-kit/skills/merge/SKILL.jp.md` |
| 済 | `plugins/work-kit/.claude-plugin/plugin.json` を 2.27.0 に bump | - `plugins/work-kit/.claude-plugin/plugin.json` |
| 済 | `.claude-plugin/marketplace.json` の work-kit を 2.27.0 に bump | - `.claude-plugin/marketplace.json` |
| 済 | `plugins/work-kit/changelogs/v2.27.0.md` を追加 | - `plugins/work-kit/changelogs/v2.27.0.md` |
| 済 | glossary に「着手可能 (🟢) / 進行中 (🟡) / 条件あり (🔴)」を追加 | - `.claude/rules/core/glossary.md` |

## 参考ドキュメント

- `plugins/work-kit/skills/merge/SKILL.md`: merge スキル本体（Step 10 が改修対象）
- `.claude/rules/core/glossary.md`: 「実施条件」「即時予約対象」「依存後続候補」の定義

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| {次にやること} | {背景・目的} | {即時実施可 / 他候補依存} |
