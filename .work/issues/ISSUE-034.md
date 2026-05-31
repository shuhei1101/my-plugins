# ISSUE-034: `work:branch-show` と `work:qa-review` の `description` にトリガー条件が不十分

**作成日**: 2026-05-31

## 問題

`work:branch-show` と `work:qa-review` の `description` frontmatter が、同じプラグイン内の他スキルと比べて著しくトリガー条件が薄い。skill 参照ガイド（`claude-kit/references/skill/スキル.md`）は「Trigger when the user says X」という形式で具体的なトリガーフレーズを列挙することを要求しているが、以下の2スキルはそれを満たしていない。

**`plugins/work/skills/branch-show/SKILL.md`**（現状）:

```yaml
description: Present next branch candidates in 3 categories (ready to start / in progress elsewhere / has conditions).
```

トリガーフレーズが一切ない1行の説明文のみ。自動起動の条件が全く記述されておらず、ユーザーがどう発話するとこのスキルが発動するかが不明。同プラグインの `branch-reserve` や `issue-create` が複数の日本語・英語トリガーフレーズを持つのと比べて大きく見劣りする。

**`plugins/work/skills/qa-review/SKILL.md`**（現状）:

```yaml
description: |
  When /work:qa-review is invoked.
  Or when the user says "review QA", "check QA items", or "answer the QA".
```

英語フレーズが3つだけで、日本語トリガーフレーズがない。同プラグインの他スキル（`start`、`merge`、`branch-reserve`、`issue-create` など）はすべて日本語フレーズを複数含んでいる。

## 修正案

`branch-show` に Trigger フレーズ（日本語・英語）を追加し、単なる説明文から「いつこのスキルが起動すべきか」を明示した形式に変える。

```yaml
# branch-show 修正例
description: |
  Present next branch candidates in 3 categories (ready to start / in progress elsewhere / has conditions).
  Trigger when the user says "次にやることを教えて", "次のブランチを確認して", "どのブランチを選べばいい",
  "show next branches", "what can I work on next", or invokes `/work:branch-show` explicitly.
```

`qa-review` に日本語トリガーフレーズを追加する。

```yaml
# qa-review 修正例
description: |
  When /work:qa-review is invoked.
  Or when the user says "review QA", "check QA items", "answer the QA",
  "QA を確認して", "QA に回答して", "QA の決定事項を埋めて".
```

## 水平展開

`work` プラグイン全体のスキルを一覧し、トリガーフレーズが日英混在または英語のみになっているものを把握すると良い。同様のパターンは `setup` スキル（"Manual invocation only" とだけあり日本語フレーズなし）にも見られる。
