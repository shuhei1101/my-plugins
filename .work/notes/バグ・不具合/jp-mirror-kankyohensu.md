# 環境変数.jp.md 欠落バグ (ISSUE-124)

## 概要

`plugins/claude-kit/references/common/環境変数.md` が行 8 で JP ミラーファイル（`references/common/環境変数.jp.md`）
の存在を宣言していたが、実ファイルが作成されていなかった。

## 経緯

- 2026-05-31: ISSUE-124 として記録
- コミット `cd990b7d`（fix: ISSUE-062/065）で `環境変数.jp.md` を含む JP ミラー 7 件を一括作成し、
  master に取り込み済み
- 2026-06-02: ブランチ `fix/jp-mirror-kankyohensu` でイシュークローズ処理を実施

## 修正内容

`plugins/claude-kit/references/common/環境変数.jp.md` を新規作成。
冒頭の警告コメント・全セクション（設定・読み取り・実例・規約・パス変数 vs 環境変数）を翻訳。

## 教訓

新規リファレンスファイルを追加する際、JP ミラーの作成を忘れないよう注意が必要。
`共通ガイド.md` の JP/EN ミラールールに従い、`環境変数.md` を追加した時点で同時に `環境変数.jp.md` を作成すべきだった。
