# claude-kitスキル名プレフィックス監査

> ブランチ: `fix/claude-kit-skill-name-prefix-audit`

## 概要

`plugins/claude-kit/skills/` 配下の全10スキルで `name` フィールドにプラグインプレフィックスが付いておらず、命名規則に違反している。`fix/skill-name-prefix-unification` ブランチ（ISSUE-032・033）で dev-kit・work・ref-inject を修正したのと同じポリシーに従い、claude-kit の全スキルにも `claude-kit:` プレフィックスを付与する。

**前ブランチで確立したポリシー**: SKILL.md の `name` フィールドは `{plugin}:{skill}` 形式でなければならない（`.work/notes/環境・設定・ポリシー/スキル名プレフィックスポリシー.md` 参照）。

対象スキル（全て `claude-kit:` プレフィックスなし）:
- `claude-creator`, `claude-refactor`, `config`, `env-sync`, `hook-creator`, `plugin-creator`, `plugin-migrate`, `rule-creator`, `skill-creator`, `statusline-setup`

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | 未解決事項を `## QA` に記録する |
| 2 | 済 | `claude-creator` SKILL.md / SKILL.jp.md の `name` を `claude-kit:claude-creator` に変更 |
| 3 | 済 | `claude-refactor` SKILL.md / SKILL.jp.md の `name` を `claude-kit:claude-refactor` に変更 |
| 4 | 済 | `config` SKILL.md / SKILL.jp.md の `name` を `claude-kit:config` に変更 |
| 5 | 済 | `env-sync` SKILL.md / SKILL.jp.md の `name` を `claude-kit:env-sync` に変更 |
| 6 | 済 | `hook-creator` SKILL.md / SKILL.jp.md の `name` を `claude-kit:hook-creator` に変更 |
| 7 | 済 | `plugin-creator` SKILL.md / SKILL.jp.md の `name` を `claude-kit:plugin-creator` に変更 |
| 8 | 済 | `plugin-migrate` SKILL.md / SKILL.jp.md の `name` を `claude-kit:plugin-migrate` に変更 |
| 9 | 済 | `rule-creator` SKILL.md / SKILL.jp.md の `name` を `claude-kit:rule-creator` に変更 |
| 10 | 済 | `skill-creator` SKILL.md / SKILL.jp.md の `name` を `claude-kit:skill-creator` に変更 |
| 11 | 済 | `statusline-setup` SKILL.md / SKILL.jp.md の `name` を `claude-kit:statusline-setup` に変更 |
| 12 | 済 | `.work/notes/` の関連ノートを更新する |

## 変更内容

実装したファイル（テスト以外）。コミットに積まれる全ファイルを列挙する。

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/claude-kit/skills/claude-creator/SKILL.md` | 編集 | `name` に `claude-kit:` プレフィックス付与 | |
| 2 | `plugins/claude-kit/skills/claude-creator/SKILL.jp.md` | 編集 | 〃 | |
| 3 | `plugins/claude-kit/skills/claude-refactor/SKILL.md` | 編集 | 〃 | |
| 4 | `plugins/claude-kit/skills/claude-refactor/SKILL.jp.md` | 編集 | 〃 | |
| 5 | `plugins/claude-kit/skills/config/SKILL.md` | 編集 | 〃 | |
| 6 | `plugins/claude-kit/skills/config/SKILL.jp.md` | 編集 | 〃 | |
| 7 | `plugins/claude-kit/skills/env-sync/SKILL.md` | 編集 | 〃 | |
| 8 | `plugins/claude-kit/skills/env-sync/SKILL.jp.md` | 編集 | 〃 | |
| 9 | `plugins/claude-kit/skills/hook-creator/SKILL.md` | 編集 | 〃 | |
| 10 | `plugins/claude-kit/skills/hook-creator/SKILL.jp.md` | 編集 | 〃 | |
| 11 | `plugins/claude-kit/skills/plugin-creator/SKILL.md` | 編集 | 〃 | |
| 12 | `plugins/claude-kit/skills/plugin-creator/SKILL.jp.md` | 編集 | 〃 | |
| 13 | `plugins/claude-kit/skills/plugin-migrate/SKILL.md` | 編集 | 〃 | |
| 14 | `plugins/claude-kit/skills/plugin-migrate/SKILL.jp.md` | 編集 | 〃 | |
| 15 | `plugins/claude-kit/skills/rule-creator/SKILL.md` | 編集 | 〃 | |
| 16 | `plugins/claude-kit/skills/rule-creator/SKILL.jp.md` | 編集 | 〃 | |
| 17 | `plugins/claude-kit/skills/skill-creator/SKILL.md` | 編集 | 〃 | |
| 18 | `plugins/claude-kit/skills/skill-creator/SKILL.jp.md` | 編集 | 〃 | |
| 19 | `plugins/claude-kit/skills/statusline-setup/SKILL.md` | 編集 | 〃 | |
| 20 | `plugins/claude-kit/skills/statusline-setup/SKILL.jp.md` | 編集 | 〃 | |

## テスト

手動テスト・動作確認の実施記録。

| # | 確認内容 | 実測結果 | 判定 |
|---|---|---|---|
| 1 | 全スキルの `name` フィールドが `claude-kit:{skill}` 形式になっている | 10スキル全て `claude-kit:` プレフィックス付与を確認 | OK |

## QA

（なし）

## 参考ドキュメント

- `.work/notes/環境・設定・ポリシー/スキル名プレフィックスポリシー.md`: スキル name フィールドのプレフィックス命名規則

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | `fix/skill-name-prefix-unification` | dev-kit・work・ref-inject のスキル名プレフィックス統一（先行ブランチ） |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | 全プラグイン横断スキル名監査 | my-plugins 全プラグインのスキル name フィールドを一括チェックし、命名規則違反を洗い出す | 即時実施可 |
