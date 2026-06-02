# ISSUE-034: `work:branch-show` と `work:qa-review` の `description` にトリガー条件が不十分

**作成日**: 2026-05-31

## 概要

`work:branch-show` と `work:qa-review` の `description` frontmatter が、同じプラグイン内の他スキルと比べて著しくトリガー条件が薄く、自動起動の発話条件が記述されていない。

## 背景

skill 参照ガイド（`claude-kit/references/skill/スキル.md`）は「Trigger when the user says X」という形式で具体的なトリガーフレーズを列挙することを要求している。同プラグインの `branch-reserve` や `issue-create` は複数の日本語・英語トリガーフレーズを持つ。

## 現状

**`plugins/work/skills/branch-show/SKILL.md`**:

```yaml
description: Present next branch candidates in 3 categories (ready to start / in progress elsewhere / has conditions).
```

トリガーフレーズが一切ない 1 行の説明文のみ。ユーザーがどう発話するとこのスキルが発動するかが不明。

**`plugins/work/skills/qa-review/SKILL.md`**:

```yaml
description: |
  When /work:qa-review is invoked.
  Or when the user says "review QA", "check QA items", or "answer the QA".
```

英語フレーズが 3 つだけで、日本語トリガーフレーズがない。同プラグインの他スキル（`start`、`merge`、`branch-reserve`、`issue-create` など）はすべて日本語フレーズを複数含んでいる。

## 期待される状態

`branch-show` と `qa-review` の両方が、日英のトリガーフレーズを伴った「いつこのスキルが起動すべきか」を明示する形式の `description` を持ち、同プラグインの他スキルと同等の自動起動性を備えている。

## 対応案

`branch-show` に Trigger フレーズ（日本語・英語）を追加し、単なる説明文から起動条件を明示した形式に変える。

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

## 横展開

`work` プラグイン全体のスキルを一覧し、トリガーフレーズが日英混在または英語のみになっているものを把握すると良い。同様のパターンは `setup` スキル（"Manual invocation only" とだけあり日本語フレーズなし）にも見られる。

---

# ユーザー回答欄

> 回答方法: 各 `**回答**:` 行で不要な選択肢を消し、1 つだけ残す（`{回答を入力}` は自由記入）。
> AI は選択肢・推奨と、候補を並べた `**回答**:` 行まで用意する。

## 意思

このイシューに対応するか。

**回答**: 対応する

## QA

### QA-1: description ポリシーの矛盾 — トリガーフレーズを追加するか削除するか

**背景**: 実装作業中に、現行 master には `docs/skill-description-policy`（2026-05-31 マージ）によって「description は短い一行説明のみ・トリガーフレーズ不要」という逆方針が `claude-kit/references/skill/スキル.md` および `.work/notes/スキル設計/skill-template-standards.md` に記録されていることが判明した。このイシューの `## 対応案`（トリガーフレーズを追加する）と現行ポリシーが直接矛盾する。

また、イシューの `## 背景` に記載の「`スキル.md` はトリガーフレーズを列挙することを要求している」という前提は、当時の旧ポリシーに基づくものであり、現在は無効になっている。

| # | 案 | 内容 |
|---|---|---|
| A | 現行ポリシー（トリガーフレーズ不要）を優先し、このイシューをクローズ（wontfix） | `branch-show` と `qa-wizard` の description は現状のまま（一行説明のみ）が正しく、このイシューは時代遅れなのでクローズする |
| B | このイシューの `## 対応案` を優先し、トリガーフレーズを追加する | 現行ポリシーノートを上書きしてトリガーフレーズを追加する方向に戻す（ただし現行の `スキル.md` 参照ガイドとの矛盾が残る） |
| C | description ポリシー自体を改めて検討し、その結果次第でこのイシューを閉じるか別イシューとして切り出す | |

**推奨**: A（現行ポリシーを優先してクローズ）— `docs/skill-description-policy` はユーザー判断でマージされており、ポリシー逆行は避けるべき。このイシューは旧ポリシー時代のスキャン結果であり、新ポリシー適用後は不要。

**回答**: A / B / C
