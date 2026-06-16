# issue-resolve-auto 並列数を環境変数化

> ブランチ: `feat/issue-resolve-auto-parallel-env`

## 概要

`work:issue-resolve-auto` スキルは現状サブエージェントの並列実行数を 5 件に固定している。
イシューの規模や端末の能力に応じて並列数を変えたいケースがあるため、環境変数 `WORK_ISSUE_RESOLVE_PARALLEL` で上書きできるようにする。

あわせてスキル冒頭に「最初に環境変数を読み込む書き方」のセクションを追加し、
今後同様の用途で参照できるリファレンスとして残す。

### 実施条件

即時実施可

## 作業内容

| No | 完了 | 作業内容 |
|---|---|---|
| 1 | - | スキル冒頭に環境変数読み込みセクションを追加（`!`echo` バッククォート構文） |
| 2 | - | Step 1 / Step 5 の固定値「5」を環境変数参照に置き換える |
| 3 | - | `marketplace.json` / `plugin.json` の version bump |

## 変更内容

| No | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/work/skills/issue-resolve-auto/SKILL.md` | 編集 | 環境変数読み込みセクション追加 + 並列数を `WORK_ISSUE_RESOLVE_PARALLEL`（既定 5）参照に変更 | |
| 2 | `plugins/work/.claude-plugin/plugin.json` | 編集 | version bump | |
| 3 | `.claude-plugin/marketplace.json` | 編集 | work エントリの version bump | |

## テスト

| No | 確認内容 | 実測結果 | 判定 |
|---|---|---|---|
| 1 | スキル本文を読み環境変数参照が固定値「5」から差し替わっていること | - | - |

## 参考リンク

- `plugins/work/skills/issue-resolve-auto/SKILL.md`: 編集対象スキル
- `plugins/work/skills/issue-review/SKILL.md`: 既存の環境変数参照例（`${WORK_COMMIT_LANG}` 等）
