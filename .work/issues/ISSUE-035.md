# ISSUE-035: 複数プラグインの `plugin-config` スキルで `description` トリガーフレーズが重複している

**作成日**: 2026-05-31

## 概要

`dev-kit:plugin-config`、`work:plugin-config`、`claude-kit:config` の 3 スキルが、`description` frontmatter に同一または極めて類似したトリガーフレーズを使っており、Claude がどのスキルを呼ぶべきか判断できない。

## 背景

skill 参照ガイド（`claude-kit/references/skill/スキル.md`）は「Vague descriptions cause false positives.（曖昧な説明は誤トリガーを引き起こす）」と明記している。汎用フレーズを複数スキルで使い回すことはこれに該当する。

## 現状

| No | スキル | 重複しているトリガーフレーズ |
|---|---|---|
| 1 | `plugins/dev-kit/skills/plugin-config/SKILL.md` | `"設定を変えたい"`, `"env を設定したい"`, `"トグルを切り替えたい"` |
| 2 | `plugins/work/skills/plugin-config/SKILL.md` | `"設定を変えたい"`, `"env を設定したい"`, `"トグルを切り替えたい"` |
| 3 | `plugins/claude-kit/skills/config/SKILL.md` | `"設定を変えたい"`, `"env を設定したい"`, `"トグルを切り替えたい"` |

ユーザーが「設定を変えたい」と言うと、どのプラグインの設定を変えたいのか区別がつかず、意図しない config スキルが誤起動するリスクがある。

## 期待される状態

各 `plugin-config` 系スキルの `description` がプラグイン固有の文脈（管理する env 変数名など）を含み、汎用フレーズへの依存が解消されて、Claude が文脈から正しいスキルを選択できる。

## 対応案

各スキルの description に、そのプラグイン固有の文脈を示すフレーズを追加し、汎用フレーズへの依存を減らす。または汎用フレーズを削除してプラグイン固有の語句のみに絞る。

```yaml
# dev-kit:plugin-config — 修正例
description: |
  When /dev-kit:plugin-config is invoked.
  Or when the user says "dev-kit の設定を変えたい", "Python/HTML/Next.js の注入を切り替えたい",
  "TypeScript チェックを無効にしたい", "言語を有効にしたい", "Markdown チェックを無効にしたい".

# work:plugin-config — 修正例
description: |
  When /work:plugin-config is invoked.
  Or when the user says "work の設定を変えたい", "worktree の作成をオフにしたい",
  "ブランチ強制注入を無効にしたい", "workspace config して".

# claude-kit:config — 修正例
description: |
  When /claude-kit:config is invoked.
  Or when the user says "claude-kit の設定を変えたい", "JP ミラーを無効にしたい", "注入言語を変えたい".
```

各スキルのトリガーフレーズをプラグイン固有の操作名（管理している env 変数名など）を含む表現に変更することで、Claude が文脈から正しいスキルを選択できるようにする。

## 横展開

同様の重複トリガー問題は他のプラグイン間でも発生しやすい。特に `plugin-migrate` のトリガーフレーズが 3 プラグイン間で重複していないか確認することを推奨する。

---

# ユーザー回答欄

> 回答方法: 各 `**回答**:` 行で不要な選択肢を消し、1 つだけ残す（`{回答を入力}` は自由記入）。
> AI は選択肢・推奨と、候補を並べた `**回答**:` 行まで用意する。

## 意思

このイシューに対応するか。

**回答**: 対応する
