# dev-kit _index.yaml JP mirror 誤登録修正

**日付**: 2026-06-03
**ブランチ**: fix/dev-kit-index-jp-mirror-misentry
**関連イシュー**: ISSUE-136

---

## 概要

`plugins/dev-kit/references/.ref-inject/_index.yaml` に JP mirror ファイル `next/testing/E2Eテスト.jp.md` が誤登録されていた問題を修正した。

## 問題の詳細

`_index.yaml` の行 391–393 に以下のエントリが存在していた:

```yaml
- path: next/testing/E2Eテスト.jp.md
  lang: next
  description: JP mirror of E2Eテスト.md
```

`_index.yaml` は ref-inject フックが参照するリファレンス一覧で、EN ファイルのパスのみを登録する規約がある。JP mirror ファイルのパスをここに登録するのは規約違反で、注入フックに JP mirror が誤って候補として扱われる可能性があった。

## 対応

- `_index.yaml` から `E2Eテスト.jp.md` の 3 行エントリを削除
- `_index.yaml` に他の `.jp.md` エントリがないことを確認（当該 1 件のみだった）
- `_index.jp.yaml` の構造を確認: EN ファイルパスに日本語 description を付与する形式で、JP mirror ファイル自体のパスは登録しない構造であることを確認。追加対応不要。
- YAML 検証: `python3 -c "import yaml; yaml.safe_load(open(...))"` で OK

## 原因

`E2Eテスト.jp.md` 追加時に誤って `_index.yaml` に記入した可能性がある。
