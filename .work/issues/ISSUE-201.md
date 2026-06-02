# ISSUE-201: dev-kit の _index.yaml / _index.jp.yaml に標準ヘッダーコメントが欠落

**作成日**: 2026-06-03

# ユーザー回答欄

## 意思

- [x] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`plugins/dev-kit/references/.ref-inject/_index.yaml` と `_index.jp.yaml` の両ファイルに、他プラグイン（claude-kit・work）および `ref-inject` テンプレートが持つ標準ヘッダーコメントが欠落している。

他プラグインの `_index.yaml` 冒頭には以下のようなヘッダーがある：

```yaml
# {plugin} reference index (English; parsed by inject_references.py).
# Each entry maps a reference file to a one-line description.
#   path        : path relative to this references/ directory
#   description : shown in the injected pointer (and as the section heading)
# Keep this in sync with _index.jp.yaml and _injection_rules.yaml.
```

dev-kit のファイルはコメントが一切なく、`references:` から直接始まっている。このヘッダーは「inject_references.py がパースする」「同期させること」を明示する維持管理上重要な説明コメント。

## 対応方針

`ref-inject` テンプレートと同じ形式のヘッダーを両ファイル先頭に追加する（`_index.yaml` は英語5行、`_index.jp.yaml` は日本語3行）。

## 対象ファイル

- `plugins/dev-kit/references/.ref-inject/_index.yaml`: 先頭にヘッダーコメントを追加
- `plugins/dev-kit/references/.ref-inject/_index.jp.yaml`: 先頭にヘッダーコメントを追加
