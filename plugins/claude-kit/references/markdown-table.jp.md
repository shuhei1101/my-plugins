<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# Markdown テーブル規約

英語正本: `references/markdown-table.md`

---

## セルの繰り返し値

同じ列で連続した行が同じ値を持つ場合、値は**最初の行にのみ**書き、以降の行はセルを空白にする。

**例 — ファイル名 + 変更内容:**

| ファイル | 変更内容 |
|---|---|
| `foo.md` | セクション A を追加 |
|  | セクション B の誤字を修正 |
| `bar.md` | 非推奨の注記を削除 |

**アンチパターン — 繰り返してはいけない:**

| ファイル | 変更内容 |
|---|---|
| `foo.md` | セクション A を追加 |
| `foo.md` | セクション B の誤字を修正 |

このルールは値が複数行にまたがる列全般に適用する: ファイル名、コンポーネント名、カテゴリ名など。
