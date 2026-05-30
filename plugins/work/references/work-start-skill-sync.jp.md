<!-- This file is a Japanese mirror of work-start-skill-sync.md. When updating the English original, update this file too. -->
# work-start ↔ worktree-create スキルリンク

`work-start` の Step 4 は `worktree-create` に委譲するため、インターフェースを常に整合させること。
`vscode-workspace-sync` も work-start に隣接し、`work:` 名前空間を使用する。
英語原文: `references/work-start-skill-sync.md`

---

## ファイルの依存関係

| 編集したファイル | 確認・更新が必要なファイル |
|---|---|
| `plugins/work/skills/start/SKILL.md` | `plugins/work/skills/worktree-create/SKILL.md` — インターフェース（PR番号・ブランチ引数）が Step 4 と一致しているか確認 |
| `plugins/work/skills/worktree-create/SKILL.md` | `plugins/work/skills/start/SKILL.md` — Step 4 の呼び出し形式と一致しているか確認 |
| `plugins/work/skills/vscode-workspace-sync/SKILL.md` | 名前空間が `work:` であることを確認 |

## ワークツリー使用の切り替え

- ワークツリーの使用は `WORK_USE_WORKTREE` 環境変数で制御する（デフォルトは有効）
- `false` / `0` / `no` / `off` に設定すると `work-start` はワークツリー作成をスキップする
- このチェックは `work-start` の Step 4 で行われる

## コミット前チェックリスト

- [ ] `work-start` の Step 4 の呼び出し形式が `worktree-create` の SKILL.md インターフェースと一致している
- [ ] インターフェースが変わる場合、3 つのスキルの SKILL.md を同じコミットで更新している
