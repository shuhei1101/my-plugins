# PR195 — git-guard-allow-merge-master

## 概要

`git merge master` / `git merge main`（masterブランチの内容を現在のブランチへ取り込む）はガード不要な操作にもかかわらず、git-guardがブロックしていた。
現在のブランチをmasterへマージする操作（`git merge <feature>`をmaster上で実行）のみをブロックし、masterを現在のブランチへ取り込む操作は許可するよう修正する。

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA を `## QA` に記録 | - |
| 済 | `.work/notes/` のノートを更新 | - `.work/notes/integrate-guard-kit-into-workspace.md` |
| 済 | `git merge master/main/origin/master/origin/main` のみ許可するよう正規表現を修正 | - `plugins/work/hooks/scripts/git-guard.py` |
| 済 | プロンプト内容の更新（不要と判断 — ブロック時のみ表示のため） | - |
| 済 | バージョンバンプ | - `plugins/work/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json`<br>- `plugins/work/changelogs/v2.46.1.md` |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/work/hooks/scripts/git-guard.py` | 編集 | `_SAFE_MERGE` 正規表現を追加し `git merge (origin/)?(master\|main)` を除外 | - |
| `plugins/work/.claude-plugin/plugin.json` | 編集 | バージョン 2.46.0 → 2.46.1 | - |
| `.claude-plugin/marketplace.json` | 編集 | work バージョン 2.46.0 → 2.46.1 | - |
| `plugins/work/changelogs/v2.46.1.md` | 新規 | v2.46.1 変更内容を記録 | - |

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| - | - | テストなし | - |

## QA

QAなし

## 参考ドキュメント

- `.work/notes/integrate-guard-kit-into-workspace.md`: git-guard の workspace(→work) 統合経緯

## 関連PR

| PR番号 | 概要 |
|---|---|
| #186 | git-guard を guard-kit から work-kit へ統合 |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |
