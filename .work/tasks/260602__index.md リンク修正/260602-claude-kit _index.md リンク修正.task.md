# claude-kit _index.md リンク修正

**ブランチ**: fix/claude-kit-index-md-links
**作成日**: 2026-06-02
**種別**: fix

## 概要

`plugins/claude-kit/references/_index.md`（人間向けナビゲーション文書）内の全リンクがファイル名のみで記述されており、実際のサブディレクトリパスを含まないため GitHub 等のリンクレンダラーで全リンクが 404 になる。また `_index.yaml` に登録済みのリファレンスが一部未掲載で、死リンク行も存在する。

## 作業内容

| # | 内容 | 状態 |
|---|---|---|
| 1 | `_index.md` 内の全リンクを正確な相対パス（`common/共通ガイド.md`、`hook/フック.md` 等）に修正する | 済 |
| 2 | `_index.yaml` に登録済みだが `_index.md` に未掲載のリファレンス行を追加する（`hook/jinja2/執筆ガイド.md`、`plugin/バージョン同期.md`、`common/環境変数記法.md`） | 済 |
| 3 | 存在しない `incidents.md` の死リンク行を削除する | 済 |

## テスト

- [x] `_index.md` 内の全リンク先が実ファイルシステム上に存在する（17/17 確認済み）
- [x] `_index.yaml` 登録済みの全リファレンスが `_index.md` に掲載されている（17/17 確認済み）
- [x] 死リンクがゼロである

## 関連イシュー

| イシュー | タイトル |
|---|---|
| ISSUE-125 | _index.md の全リンクがサブディレクトリパスを省略していて無効 |

## 参考ドキュメント

- `.work/notes/バグ・不具合/claude-kit-index-md-broken-links.md`
