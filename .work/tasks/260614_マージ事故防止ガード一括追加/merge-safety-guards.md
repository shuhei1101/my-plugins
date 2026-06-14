# マージ事故防止ガード一括追加

## 目的

ISSUE-361 のマージ事故（2849 ファイル誤削除）を踏まえ、確認プロンプトを増やさずに自動で守る系のガードを一括追加する。

## 作業内容

| No | 作業 | 完了 |
| --- | --- | --- |
| 1 | `skills/merge/SKILL.md` のコンフリクト自動解消方針を「停止して報告」に書き換え | 未 |
| 2 | `agents/issue-resolver.md` にコンフリクト時の自動解消禁止を明記 | 未 |
| 3 | `skills/issue-resolve-auto/SKILL.md` のサブエージェント呼び出し時の指示にも明記 | 未 |
| 4 | `delete-guard.py` を拡張して `.gitignore` / `.gitattributes` も対象に | 未 |
| 5 | 新規 `dangerous-git-guard.py` 追加（`worktree remove --force` / `git rm` 重要ファイル / `git checkout --` 重要ファイル を block） | 未 |
| 6 | 新規 `post-commit-deletion-check.py`（Stop hook）追加（直近コミットで N 件超削除なら警告） | 未 |
| 7 | `worktree-tool.py` の `cmd_create` で `origin/<current_branch>` を fetch して base ref に使う | 未 |
| 8 | バージョンアップ（plugin.json / marketplace.json） | 未 |

## 仕様

Phase 1: プロンプト矯正 — マージスキルとサブエージェント側のコンフリクト解消ポリシーを「自動解消禁止／停止して報告」に変える。
Phase 2: 静かなガード — 確認プロンプトを挟まず、危険コマンドは完全 block、削除検知は警告コンテキスト注入のみ。
Phase 3: base ref 修正 — worktree 作成時に `origin/<parent_branch>` を fetch してから base にする。古い HEAD からの分岐を防ぐ。

## 参考ドキュメント
