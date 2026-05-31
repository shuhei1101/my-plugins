# ブランチ文書ファイル名を日本語タイトル基準に変更

> 内部 ID: 244（index.yaml 採番用 — クロスリファレンス目的）

## 概要

ブランチ文書のファイル名を `{YYMMDD}-{branch-hyphenated}.md` から `{YYMMDD}-{日本語タイトル}.md` に変更する。
合わせて文書内にブランチ名行を追加し、`index.yaml` に `branch` フィールドを追加して PR 表記をブランチ表記に統一する。

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | QA を `## QA` に記録する |
| 2 | 済 | `.work/notes/` のノートを更新する |
| 3 | 済 | テンプレートファイルを `yymmdd-日本語タイトル.md` にリネームし、ブランチ名行を追加 |
| 4 | 済 | `setup-task.py` に `--ja-title` パラメータを追加し日本語タイトルをファイル名に使用 |
| 5 | 済 | `index-tool.py` に `--branch` パラメータを追加し PR 言語を修正 |
| 6 | 済 | `index.yaml` / `index.archive.yaml` テンプレートを修正（PR → ブランチ、branch フィールド追加） |
| 7 | 済 | `skills/start/SKILL.md` を更新（ファイル名説明・コマンド例・Step 2 に日本語タイトル収集を追加） |
| 8 | 済 | 関連スキル・フック・リファレンスの `{branch-hyphenated}.md` パス表記を全件更新 |
| 9 | 済 | JP ミラーも同様に更新 |
| 10 | 済 | `CLAUDE.md` の changelog に追記 |
| 11 | 済 | テンプレートから「内部 ID」見出し行を削除し、`setup-task.py` の `{N}` 置換を整理 |
| 12 | - | rules / CLAUDE.md を更新する |

## 変更内容

実装したファイル（テスト以外）。コミットに積まれる全ファイルを列挙する。

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/work/templates/.work/tasks/yymmdd_xxx/yymmdd-日本語タイトル.md` | 新規（リネーム） | ブランチ文書テンプレート。ブランチ名行を追加 | `yymmdd-branch-name.md` からリネーム |
| 2 | `plugins/work/scripts/setup-task.py` | 編集 | `--ja-title` パラメータ追加、`{日本語タイトル}` / `{branch-name}` プレースホルダー対応 | - |
| 3 | `plugins/work/scripts/index-tool.py` | 編集 | `--branch` パラメータ追加、PR 言語をブランチ用語に統一 | - |
| 4 | `plugins/work/templates/.work/tasks/index.yaml` | 編集 | PR 表記修正、branch フィールド追加、YYYYMMDD→YYMMDD 修正 | - |
| 5 | `plugins/work/templates/.work/tasks/index.archive.yaml` | 編集 | 同上 | - |
| 6 | `plugins/work/skills/start/SKILL.md` | 編集 | Step 2 に日本語タイトル収集追加、Step 3/6/7 をファイル名変更に合わせて更新 | - |
| 7 | `plugins/work/skills/start/SKILL.jp.md` | 編集 | 〃 | - |
| 8 | `plugins/work/skills/branch-reserve/SKILL.md` | 編集 | ブランチ文書パス表記を更新 | - |
| 9 | `plugins/work/skills/branch-reserve/SKILL.jp.md` | 編集 | 〃 | - |
| 10 | `plugins/work/skills/merge/SKILL.md` | 編集 | ブランチ文書パス表記を全件更新 | 3 箇所 |
| 11 | `plugins/work/skills/merge/SKILL.jp.md` | 編集 | 〃 | - |
| 12 | `plugins/work/skills/qa-review/SKILL.md` | 編集 | ブランチ文書パス表記を更新 | - |
| 13 | `plugins/work/skills/qa-review/SKILL.jp.md` | 編集 | 〃 | - |
| 14 | `plugins/work/hooks/prompts/user-prompt-submit.md` | 編集 | ブランチ文書パス表記を更新 | - |
| 15 | `plugins/work/hooks/prompts/user-prompt-submit.jp.md` | 編集 | 〃 | - |
| 16 | `plugins/work/references/work-dot-work-dir.md` | 編集 | ディレクトリ構成表とテキストのパス表記を更新 | - |
| 17 | `plugins/work/references/work-dot-work-dir.jp.md` | 編集 | 〃 | - |
| 18 | `plugins/work/references/work-start-skill-sync.md` | 編集 | PR 言語をブランチ用語に修正 | - |
| 19 | `plugins/work/references/work-start-skill-sync.jp.md` | 編集 | 〃 | - |
| 20 | `plugins/work/CLAUDE.md` | 編集 | Branch Document Structure のパス・changelog 追記 | - |
| 21 | `plugins/work/CLAUDE.jp.md` | 編集 | 〃 | - |

## テスト

手動テスト・動作確認の実施記録。

| # | 確認内容 | 実測結果 | 判定 |
|---|---|---|---|
| 1 | {何を確認したか} | {実際どうなったか} | OK |

## QA

このブランチのスコープの未決定事項を QA-XXX として記録する。決定後は本文の該当箇所に反映する。

## 参考ドキュメント

- `.work/notes/PR用語廃止・ブランチ用語統一.md`: PR 用語廃止・ブランチ用語統一の経緯と変更方針

## 関連イシュー

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | - | - |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | - | - | - |
