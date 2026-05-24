---
created_at: 2026-05-23
updates:
  - 2026-05-23 — 初版作成（PR86: archive フロー修正）
  - 2026-05-23 — ステップ番号を更新（PR92: master 適合確認 Step3 挿入により繰り下げ）
related_specs: []
related_prs:
  - PR85
  - PR86
  - PR92
---

# work-kit:merge フロー — index archive の設計

## 概要

work-kit:merge スキルが `index.yaml` の完了エントリを `index.archive.yaml` に移動するフロー。
`index.yaml` は gitignore 済みでメインリポジトリにのみ存在するため、archive 実行前に `completed: true` を明示的にセットする必要がある。

## index.yaml / index.archive.yaml の性質

| ファイル | git 管理 | 存在場所 |
|---|---|---|
| `index.yaml` | gitignore（非追跡） | メインリポジトリのみ |
| `index.archive.yaml` | 追跡済み | メインリポジトリ・worktree 双方に存在 |

worktree を作成しても `index.yaml` はコピーされない。
archive コマンドはメインリポジトリの `index.yaml` を読み、worktree の `index.archive.yaml` に書き込む。

## 正しい merge フロー（Step 5〜7）

> PR92 で Step3（master 適合確認）が追加されたため、以下のステップ番号が繰り下がった。

```
Step 5: completed: true をセット（メインリポジトリで実行）
  python index-tool.py set-completed .work/tasks/index.yaml --id {N}

Step 6: archive をメインリポジトリで実行、書き込み先は worktree
  python index-tool.py archive \
    .work/tasks/index.yaml \
    ../$(basename $(pwd))-wt-PR{N}/.work/tasks/index.archive.yaml

  → worktree の index.archive.yaml に PR エントリが移動する
  → worktree でコミット（PR ブランチに含める）
    git -C ../$(basename $(pwd))-wt-PR{N} add .work/tasks/index.archive.yaml
    git -C ../$(basename $(pwd))-wt-PR{N} commit -m "chore: archive PR{N} #PR{N}"

Step 7: --no-ff マージ（index.archive.yaml が PR ブランチ経由で master に入る）
  git merge --no-ff -m "{type}: {title} #PR{N}" PR{N}/{type}/{title}
```

## なぜ Step 5 が必要か

archive コマンドは `completed: true` のエントリのみを移動する。
merge 前の時点では `completed` は `false` のままなので、archive を実行しても 0 件になる。
Step 5 で明示的に `completed: true` にセットすることで archive が機能する。

## index-tool.py の set-completed コマンド仕様

```
python index-tool.py set-completed [index_yaml] --id N
```

- `index_yaml`: `index.yaml` のパス（デフォルト: `.work/tasks/index.yaml`）
- `--id N`: 完了にする PR 番号
- 対象エントリの `completed: false` を `completed: true` に更新して上書き保存
- 対象が見つからない場合はエラー終了
