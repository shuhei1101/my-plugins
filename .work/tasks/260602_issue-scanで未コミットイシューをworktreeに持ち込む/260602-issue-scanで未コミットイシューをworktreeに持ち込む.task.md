# issue-scanで未コミットイシューをworktreeに持ち込む

> ブランチ: fix/issue-scan-carry-uncommitted

## 概要

### 実施条件

即時実施可

### 背景

ユーザーはイシューファイルへの回答（`## 意思` / `## QA` の `**回答**:`）をマスターブランチで直接書き込む運用をしており、コミットせずに放置することが多い。

`work:issue-scan` は worktree を作成してスキャン結果をコミット・マージするが、worktree はマスターの**コミット済み状態**から分岐するため、未コミットのイシューファイルが worktree に引き継がれない。

### 目的

`issue-scan` が worktree を作成した後、マスターに未コミットの `.work/issues/` ファイルがあれば worktree にコピーし、スキャン結果と一緒にコミットする。

## 作業内容

| # | 作業 | 状態 |
|---|---|---|
| 1 | QA を記録する | 済 |
| 2 | `issue-scan/SKILL.md` Step 0 に未コミットコピー手順を追加 | - |
| 3 | `issue-scan/SKILL.jp.md` を同期 | - |
| 4 | `plugin.json` バージョンを bump | - |
| 5 | `work/CLAUDE.md` changelog を更新 | - |
| 6 | ノートを更新してファイナルコミット | - |

## QA

## テスト

| # | テスト項目 | 結果 |
|---|---|---|
| 1 | マスターに未コミットのイシューファイルがある状態で `issue-scan` を実行し、worktree コミットに未コミットファイルが含まれること | - |

## 変更内容

| # | ファイル | 変更内容 |
|---|---|---|
| 1 | `plugins/work/skills/issue-scan/SKILL.md` | Step 0 に未コミットファイルのコピー手順を追加 |
| 2 | `plugins/work/skills/issue-scan/SKILL.jp.md` | JP ミラー同期 |
| 3 | `plugins/work/.claude-plugin/plugin.json` | version bump |
| 4 | `plugins/work/CLAUDE.md` | changelog 追加 |

## 参考ドキュメント

- `.work/notes/ワークフロー・マージ/イシュー対応ワークフロー.md`

## 関連イシュー

## 関連ブランチ

## 次ブランチ候補
