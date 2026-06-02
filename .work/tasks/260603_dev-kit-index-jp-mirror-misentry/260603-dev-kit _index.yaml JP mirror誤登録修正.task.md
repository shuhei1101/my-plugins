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
| 1 | `_index.yaml` の `E2Eテスト.jp.md` エントリ（3行）を削除 | 済 |
| 2 | `_index.yaml` の他 `.jp.md` 誤登録チェック | 済 |
| 3 | `_index.jp.yaml` に JP mirror エントリが欠けていれば追加 | 済 |
| 4 | `_index.yaml` が有効な YAML としてパースできることを検証 | 済 |

---

## テスト

- `python3 -c "import yaml; yaml.safe_load(open(...))"` による YAML パース検証: **OK**
- `_index.yaml` 内の `.jp.md` エントリ grep チェック: **0 件（該当なし）**

---

## 関連イシュー

| イシュー ID | タイトル | 関係 |
|-------------|----------|------|
| ISSUE-136 | dev-kit: _index.yaml に JP mirror ファイル（E2Eテスト.jp.md）が誤登録 | 対応 |

---

## 参考ドキュメント

| ドキュメント | 説明 |
|-------------|------|
| [dev-kit-index-jp-mirror-misentry.md](../../../.work/notes/バグ・不具合/dev-kit-index-jp-mirror-misentry.md) | 誤登録の詳細と対応メモ |

