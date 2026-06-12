# post-merge-upgrade — マージ後自動 push & upgrade フック

## 概要

master へのマージ後に `git push`、marketplace upgrade、tmux セッションへの `/reload-plugins` 送信を自動実行する。フック（シン・ラッパー）とツール（コア処理）に分離している。

## 構成

| 役割 | ファイル |
|---|---|
| フック（シン・ラッパー） | `.claude/hooks/post-merge-upgrade.py` |
| コア処理 | `tools/post_merge_upgrade.py` |

## フックの条件チェック

stdin あり（フック起動）の場合のみ以下を確認してスキップ判定する:
- `tool_name` が `Bash` であること
- コマンドに `git merge` を含むこと
- `git merge origin/master`（master 取り込み）はスキップ
- 現在ブランチが `master` であること
- `CONFLICT` がレスポンスに含まれていないこと

## コア処理の流れ

1. `git.exe push origin master`（WSL では `git.exe` を使用）
2. `python tools/marketplace.py upgrade`
3. `python tools/reload_plugins.py`（tmux セッションに `/reload-plugins` 送信）

## 参考リンク

- `.claude/hooks/post-merge-upgrade.py`: フック（シン・ラッパー）
- `tools/post_merge_upgrade.py`: コア処理
