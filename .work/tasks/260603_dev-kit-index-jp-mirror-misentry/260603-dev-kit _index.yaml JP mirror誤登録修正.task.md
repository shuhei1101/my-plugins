# dev-kit _index.yaml JP mirror誤登録修正

**ブランチ**: fix/dev-kit-index-jp-mirror-misentry
**作成日**: 2026-06-03
**種別**: fix

---

## 概要

`plugins/dev-kit/references/.ref-inject/_index.yaml` に JP mirror ファイル `next/testing/E2Eテスト.jp.md` が誤登録されている問題を修正する。EN ファイルのみを登録する規約に違反するエントリを削除し、`_index.jp.yaml` に移動する。

---

## 作業内容

| # | 内容 | 状態 |
|---|------|------|
| 1 | `_index.yaml` の `E2Eテスト.jp.md` エントリ（3行）を削除 | 未 |
| 2 | `_index.yaml` の他 `.jp.md` 誤登録チェック | 未 |
| 3 | `_index.jp.yaml` に JP mirror エントリが欠けていれば追加 | 未 |
| 4 | `_index.yaml` が有効な YAML としてパースできることを検証 | 未 |

---

## テスト

- `python -c "import yaml; yaml.safe_load(open(...))"` による YAML パース検証

---

## 関連イシュー

| イシュー ID | タイトル | 関係 |
|-------------|----------|------|
| ISSUE-136 | dev-kit: _index.yaml に JP mirror ファイル（E2Eテスト.jp.md）が誤登録 | 対応 |

---

## 参考ドキュメント

| ドキュメント | 説明 |
|-------------|------|

