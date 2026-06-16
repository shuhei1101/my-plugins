# delete-guard: .claude/worktrees/ 配下の削除を許可

> ブランチ: `fix/delete-guard-worktrees-allow`

## 概要

`delete-guard.py` は `.claude` ディレクトリ配下への `rm`/`rmdir` をブロックするが、
`.claude/worktrees/<branch>` のシンボリックリンク削除もブロックされてしまう問題を修正する。

`.claude/worktrees/` 配下はワークツリーの後片付けで削除する必要があるため、
このパスのみ削除ガードの対象外にする。

### 実施条件

即時実施可

## 作業内容

| No | 完了 | 作業内容 |
|---|---|---|
| 1 | - | `delete-guard.py` に `.claude/worktrees/<branch>` を例外として追加 |
| 2 | - | `.work/notes/` の関連ノートを更新する |

## 変更内容

| No | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/work/hooks/delete-guard.py` | 編集 | `.claude/worktrees/` 配下の削除を許可する例外ロジックを追加 | |

## テスト

| No | 確認内容 | 実測結果 | 判定 |
|---|---|---|---|
| 1 | `.claude/worktrees/test-branch` の `rm -rf` がブロックされないこと | (未実施) | - |
| 2 | `.claude/settings.json` など worktrees 以外の `.claude` 削除は引き続きブロックされること | (未実施) | - |

## QA

なし

## 参考リンク

- `plugins/work/hooks/delete-guard.py`: 削除ガード本体
