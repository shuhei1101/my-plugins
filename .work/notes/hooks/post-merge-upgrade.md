# post-merge-upgrade — マージ後自動 push & upgrade フック

## 概要

master へのマージ後に `git push`、marketplace upgrade、tmux セッションへの `/reload-plugins` 送信を自動実行する。フック（シン・ラッパー）とツール（コア処理）に分離している。

## 構成

| 役割 | ファイル |
|---|---|
| フック（条件チェック＋呼び出し） | `.claude/hooks/post-merge-upgrade.py` |
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

## reload の自セッション遅延実行

実行者自身のセッションはターン処理中で send-keys を取りこぼすため、即時送信しない:

1. `reload_plugins.py` が自セッション（`$TMUX` + `tmux display-message`）を検出したら、送信せず保留トークン `~/.claude/tokens/work/reload-pending/<tmux_session>` を書く
2. work プラグインの Stop フック `reload_deferred.py` がターン終了時にトークンを消費し、3 秒遅延のバックグラウンドプロセスで自セッションへ send-keys する
3. トークンがなければ Stop フックは何もしない

## 既知の課題

- フックの merge 検出正規表現が `git merge` のみで、`git -C <path> merge` 形式にマッチしない（pre-merge-version-check も同様）
- ~~cmd_upgrade()のuninstallコマンドに`--scope`を指定していなかったため、localスコープのプラグインのアンインストールが失敗していた~~ → fix/cmd-upgrade-scope で修正済み

## 参考リンク

- `.claude/hooks/post-merge-upgrade.py`: フック（シン・ラッパー）
- `tools/post_merge_upgrade.py`: コア処理（pushスキル廃止、MCPツールおよびフックが直接呼び出す）
- `tools/reload_plugins.py`: reload 送信（自セッションは保留トークン化）
- `plugins/work/hooks/reload_deferred.py`: Stop フック（保留分の遅延送信）
