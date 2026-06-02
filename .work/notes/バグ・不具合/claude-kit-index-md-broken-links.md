# claude-kit _index.md リンク修正 (ISSUE-125)

**日付**: 2026-06-02
**ブランチ**: fix/claude-kit-index-md-links

## 問題

`plugins/claude-kit/references/_index.md`（人間向けナビゲーション文書）内の全リンクがファイル名のみで記述されており、実際のサブディレクトリパスを含まないため、GitHub 等のリンクレンダラーで全リンクが 404 になっていた。

v3.48.0 で `references/` をロールベースのサブフォルダ（`common/`、`skill/`、`hook/`、`claude-md/`、`plugin/`）に再編成した際に `_index.md` のリンクが更新されなかったことが原因。

## 修正内容

| カテゴリ | 変更 |
|---|---|
| リンクパス修正 | 全 14 リンクを `ファイル名.md` → `サブディレクトリ/ファイル名.md` に修正 |
| jinja2 パス修正 | `jinja2/テンプレート注意点.md` → `hook/jinja2/テンプレート注意点.md` |
| 未掲載追加 | `common/環境変数記法.md`、`hook/jinja2/執筆ガイド.md`、`plugin/バージョン同期.md` を追加 |
| 死リンク削除 | 存在しない `incidents.md` の行を削除 |

## 結果

- 全 17 リンクが実在するファイルを指すことを確認
- `_index.yaml` 登録済み全 17 件が `_index.md` に掲載されていることを確認
- 死リンクゼロ

## 教訓

`references/` 再編成（ディレクトリ構造変更）を行う際は `_index.md` のリンクも同時に更新する。`_index.yaml`（システム向け）と `_index.md`（人間向け）の二重管理が乖離の根本原因。
