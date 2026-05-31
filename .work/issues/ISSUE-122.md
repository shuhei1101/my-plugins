# ISSUE-122: incidents.md が _index.md に記載されているが実体が存在しない

**作成日**: 2026-05-31

## 問題
`references/_index.md` の「同期・保守」セクション行64に以下の記載がある。

```
| 3 | [incidents.md](incidents.md) | `.claude/rules/incidents.md` のフォーマットガイド。2 層構造（索引 + 詳細ファイル） |
```

しかし `references/` 配下のどこにも `incidents.md` は存在せず、`_index.yaml`（注入インデックス）にも登録されていない。リンクも実体ファイルも両方存在しない完全な死リンク。

## 修正案

**案 A**: `incidents.md` を実際に作成し、`.claude/rules/incidents.md` のフォーマットガイドとして記述する。作成後は `_index.yaml` にも `path` エントリを追加し、必要であれば `_injection_rules.yaml` にもパターンを追加する。

**案 B**: ガイドが不要になった場合は `_index.md` から当該行を削除する。

## 水平展開
`_index.md`（人間向けインデックス）と `_index.yaml`（注入システム向けインデックス）は別管理されており、今後も同様の乖離が生じやすい。両インデックスの整合チェックをチームの定期メンテナンス項目に加えることを推奨する。
