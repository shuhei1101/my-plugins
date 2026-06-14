# メインリポジトリでの git add をブロックするフック追加

> ブランチ: `feat/git-add-guard`

## 概要

メインリポジトリ（master/main/develop ブランチ）上での `git add` をフックで検出・ブロックし、ワークツリーでの作業を強制する。
現在は `master-commit-guard` がコミットをブロックしているが、その前段階の `git add` も許すべきでないという考えに基づく。

### 実施条件

即時実施可

## 作業内容

| No | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | `master-commit-guard.py` に `git add` 検出ロジックを追加 |
| 2 | - | `.work/notes/` の関連ノートを更新する |

## 変更内容

| No | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/work/hooks/master-commit-guard.py` | 編集 | `git add` コマンドをメインブランチ上で検出してブロック | コミットガードと同居 |

## テスト

| No | 確認内容 | 実測結果 | 判定 |
|---|---|---|---|
| 1 | メインリポジトリで `git add` を実行するとブロックされる | block JSON 出力を確認 | 合格 |
| 2 | ワークツリー内では `git add` が通過する | exit 0 で通過を確認 | 合格 |
| 3 | `git add` 以外のコマンドは従来通り動作する | スクリプトの分岐構造から確認 | 合格 |

## QA

なし

## 参考リンク

- `plugins/work/hooks/master-commit-guard.py`: 既存のコミットガード実装
