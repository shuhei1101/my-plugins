<!-- This file is a Japanese mirror of work-merge-skill-sync.md. When updating the English original, update this file too. -->
# マージスキル ↔ マージフローノート同期

マージフローの現在仕様はノート `.work/notes/work-kitスキル群.md` に記載されている。
マージ `SKILL.md` でステップを追加・削除・並べ替えしたら、同じ変更でそのノートのマージフロー
記述も更新し、ノートが実際の挙動を反映し続けるようにする。
英語原文: `references/work-merge-skill-sync.md`

---

## ファイルの依存関係

| 変更 | 確認・更新が必要なファイル |
|---|---|
| `plugins/work/skills/merge/SKILL.md` のステップ追加・削除・並べ替え | `.work/notes/work-kitスキル群.md` — マージフロー記述が現在のステップを反映しているか |
| `plugins/work/skills/merge/SKILL.jp.md` の更新 | `SKILL.md` も同じコミットで更新（JP ミラー） |

## コミット前チェックリスト

- [ ] `.work/notes/work-kitスキル群.md` が*現在の*マージフローを記述している（古いステップ番号が残っていない）
- [ ] `SKILL.md` と `SKILL.jp.md` が同じコミットで更新されている
