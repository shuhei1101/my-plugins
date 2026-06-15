# scripts-branch-guard — work プラグイン scripts 共通の保護ブランチ実行ガード

## 概要

work プラグインの状態書き換え系 Python スクリプト
(`index-tool.py` / `issue-tool.py` / `trim-index.py`) が、cwd の git ブランチが
`master` / `main` / `develop` のときに自分自身を拒否する仕組み。

PreToolUse `Edit|Write` matcher の `protected-branch-guard.py` だけでは
MCP 経由 (Bash matcher) の subprocess 書き込みを止められないため、スクリプト側に
ガードを置いて多重防御する。

## 仕組み

- 共通ヘルパー `plugins/work/scripts/_branch_guard.py` に
  `assert_not_protected_branch(script_label)` を実装
- 各スクリプトは `main()` の先頭でこれを呼ぶ
- cwd で `git branch --show-current` を実行し、結果が
  `{master, main, develop}` に含まれていたら stderr に日本語メッセージを出して
  `sys.exit(1)`
- git 不在・リポジトリ外 (`returncode != 0` or 空出力) はガードしない (素通り)

## 適用範囲

| No | スクリプト | ガード |
|---|---|---|
| 1 | `scripts/index/index-tool.py` | ✅ |
| 2 | `scripts/index/trim-index.py` | ✅ |
| 3 | `scripts/issue/issue-tool.py` | ✅ |
| 4 | `scripts/worktree/worktree-tool.py` | ❌ master から worktree を切る入口 |

## 経路別の効果

| No | 経路 | cwd | ガード結果 |
|---|---|---|---|
| 1 | master セッション + MCP ツール呼出 | `CLAUDE_PROJECT_DIR` = main repo | exit 1, `CommandResult.success=False` |
| 2 | worktree セッション + MCP ツール呼出 | `CLAUDE_PROJECT_DIR` = worktree path | 通過 |
| 3 | master 上で CLI 直叩き | カレント | exit 1 |
| 4 | worktree 上で CLI 直叩き | カレント | 通過 |

## 既知の影響

`/work:start` の step 2 は master セッションから `index_add` を呼ぶ前提のため、
このガード適用後は失敗する。`/work:start` 側の改修（worktree_create を先行させて
subsequent subprocess を worktree cwd で動かす経路を整える、もしくは subcommand 別
ホワイトリスト方式に切替）は別タスクで対応する。

## 参考リンク

- `plugins/work/scripts/_branch_guard.py`: ガード本体
- `plugins/work/hooks/protected-branch-guard.py`: PreToolUse `Edit|Write` 側の既存ガード（同じ思想の Hook 版）
- `plugins/work/mcp/server.py`: `_run_script` の cwd 渡し（`CLAUDE_PROJECT_DIR`）
