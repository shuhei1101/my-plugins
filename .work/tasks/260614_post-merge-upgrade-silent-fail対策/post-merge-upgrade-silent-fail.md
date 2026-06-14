# post-merge-upgrade のサイレント失敗を恒久対策

## 背景

master へのマージ後、`PostToolUse:Bash` フックで `post-merge-upgrade.py` → `tools/post_merge_upgrade.py` が走り、push + marketplace upgrade + reload-plugins を実行する設計。
ところが push が失敗しても `subprocess.run(check=False)` で握り潰され、会話にも何も出ないため「フックが動いていない」ように見える。
今回のマージ後に master が origin/master より 12 コミット先行していたのが具体例。

## 作業内容

| No | 作業 | 完了 |
| --- | --- | --- |
| 1 | `tools/post_merge_upgrade.py` の各 `subprocess.run` を `capture_output=True` 化し、`returncode != 0` で stdout に内訳を出す（push / upgrade / reload を個別に） | 未 |
| 2 | WSL から `git.exe` を呼ぶときは `cwd` を Windows パス（`/mnt/c/...` → `C:/...`）に変換 | 未 |
| 3 | `.claude/hooks/post-merge-upgrade.py` で `tools/post_merge_upgrade.py` の stdout を取得し、`hookSpecificOutput.additionalContext` で会話に注入（成功・失敗どちらも） | 未 |
| 4 | 動作確認: 手動で `post_merge_upgrade.py` を起動して push が走り、結果が stdout に出ることを検証 | 未 |

## 仕様

- push 失敗時の終了コードは `0`（フックが errno でクラッシュしないように）。失敗内容は stdout のメッセージで会話に流す
- WSL パス変換は `sys.platform == "linux"` かつ cwd が `/mnt/{letter}/...` 形式のときだけ適用
- 既存の「サブステップ間のスリープ 2 秒」「マーケットプレイス upgrade」「reload-plugins」のフローは維持

## 参考ドキュメント
