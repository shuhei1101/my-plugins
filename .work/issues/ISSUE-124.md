---
decision: pending
status: not_started
branches: []
instruction: ""
---

# ISSUE-124: 環境変数.md が JP ミラーを宣言しているが 環境変数.jp.md が存在しない

**作成日**: 2026-05-31

## 問題
`references/common/環境変数.md` の行8に以下の宣言がある。

```
Japanese mirror: `references/common/環境変数.jp.md`
```

しかし `references/common/環境変数.jp.md` は存在しない。他の全リファレンスファイル（`共通ガイド.md`、`AskUserQuestion制約.md`、`サブエージェント.md` 等）には対応する `.jp.md` が存在しており、`環境変数.md` だけが抜けている。

`リファレンス同期.md` と `共通ガイド.md` の JP/EN ミラールールによれば、すべてのリファレンスファイルには対応する JP ミラーが必要である。

## 修正案

`references/common/環境変数.jp.md` を作成する。先頭には所定の警告コメントを付け、内容は `環境変数.md` を日本語に翻訳したものとする。`jp-mirror-translator` エージェント（`subagent_type: "claude-kit:jp-mirror-translator"`）を使用して生成可能。

## 水平展開
新規リファレンスファイルを追加した際の JP ミラー作成が漏れるパターン。他の新規追加ファイルでも同様の漏れが発生しやすいため、プラグイン更新時のチェックリストに「全 `.md` に対応する `.jp.md` が存在するか確認」を加えることを推奨する。
