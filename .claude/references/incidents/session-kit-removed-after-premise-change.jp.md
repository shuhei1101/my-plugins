<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# session-kit を作ったが前提が変わって削除（PR155）

## 何が起きたか

`session-kit` は PR150 で新設、PR151 でピボットし、py-kit/next-kit の reference **注入トークン**の寿命を管理していた: 毎 `UserPromptSubmit` でセッションのトークンを削除して reference を**会話ターンごとに再注入**させ（長いセッションで注入内容が埋もれて忘れられるのを防ぐ）、古いトークンを 1 日 TTL で掃除していた。

PR155 でユーザーが「これって結局いらなくなったんじゃないの。削除でよくね」と質問。調査の結果、session-kit へのハード依存は無い（消費側は自分のトークンを作って存在チェックするだけ、session-kit が外部から削除）ため削除は安全と確認。ユーザーは削除（方針 A）を選択し、py-kit/next-kit は once-per-session 注入にフォールバックした。

## 根本原因

session-kit の価値は**ターンごとの再注入**で、これは注入内容が重く、長い会話で埋もれて忘れられる場合にのみ意味がある。しかし PR147 で注入は既に **path + description のポインタのみ**（本文なし）に変わっていた。ポインタのみになった時点で、それを毎ターン再注入する限界価値は、専用のプラグイン横断プラグイン＋ `~/.claude/tokens/` の寿命規約に見合わなくなっていた。

インフラ（session-kit）が、それを正当化していた前提（本文全量注入）より長生きした。前提は PR147 で消えたが、依存インフラは PR155 まで見直されなかった。

## 教訓

**ある最適化の前提が変わったら、そのために作ったインフラがまだ正当かを見直す。** 具体的には、PR147（本文全量 → ポインタ注入）の時点で session-kit を見直すべきだった（軽量ポインタではターンごとの鮮度の価値は大きく下がるため）。実際には session-kit は数 PR の間そのまま残った。

また、限界的な UX 最適化のために専用プラグイン＋プラグイン横断のパス/トークン規約を持つのは高コスト。これは [[premature-cross-plugin-centralization]]（プラグイン横断の仕組みを早すぎる段階で作らない）と同系統だが角度が違う — ここでは作成時点では正当だったが、*別の*変更（PR147）が前提を崩したことで初めてお荷物になった。

## 関連

- [[premature-cross-plugin-centralization]] — 同系統（プラグイン横断インフラの作りすぎ）
- [[injection-hook-full-body-bloat]] — PR147、session-kit の前提を崩した変更
- 削除したプラグイン: `plugins/session-kit/`（PR155）
