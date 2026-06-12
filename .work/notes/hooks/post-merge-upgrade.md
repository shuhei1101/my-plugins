# post-merge-upgrade — マージ後自動 push & upgrade フック

## 概要

master へのマージ後に `git push`、marketplace upgrade、tmux セッションへの `/reload-plugins` 送信を自動実行するフック。TTY 直接実行にも対応。

## 動作モード

- フック起動（stdin あり）: PostToolUse として動作。`git merge` コマンドが対象で、master ブランチかつコンフリクトなしの場合のみ本処理を実行
- 直接実行（TTY / stdin なし）: フックチェックをスキップして本処理を直接実行

## 処理の流れ

1. `git.exe push origin master`（WSL では `git.exe` を使用）
2. `python tools/marketplace.py upgrade`
3. `python tools/reload_plugins.py`（tmux セッションに `/reload-plugins` 送信）

## 参考リンク

- `.claude/hooks/post-merge-upgrade.py`: スクリプト本体
