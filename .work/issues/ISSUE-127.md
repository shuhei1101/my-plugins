---
decision: pending
status: not_started
branches: []
instruction: ""
---

# ISSUE-127: jinja2/テンプレート注意点.md と jinja2/執筆ガイド.md の内容が大幅に重複

**作成日**: 2026-05-31

## 問題
同一ディレクトリ（`references/hook/jinja2/`）の 2 ファイルが、`trim_blocks=True` と `lstrip_blocks=True` 環境下での Jinja2 Markdown 出力の落とし穴について、ほぼ同じ内容を異なる切り口で記述している。

| No | テンプレート注意点.md | 執筆ガイド.md |
|---|---|---|
| 1 | Rule 1: `{% %}` タグが次の改行を食う | Pitfall 3: 条件ブロック直後の blank line 欠落（同概念） |
| 2 | Rule 2: 連続タグ + `---` で setext 見出し化 | Pitfall 1: ブロックタグ直上の `---` で setext 化（同概念） |
| 3 | Rule 3: `}}` が Handlebars パーサに誤解釈される | Pitfall 2: ATX 見出し内の `{{ expr }}` が誤解釈される（同概念） |
| 4 | General authoring guidance（4 ポイント、固有） | — |
| 5 | — | Pitfall 4: インデント付きブロックタグの indentation 消失（固有） |

3 つの主要ルール/落とし穴が実質的に重複しており、両ファイルを読んだ Claude がどちらを正とすべきか判断しにくい。また `_injection_rules.yaml` では `**/hooks/templates/*.j2`（全プラグイン）に `テンプレート注意点.md` が required、`plugins/*-kit/hooks/templates/*.j2`（kit 限定）に追加で `執筆ガイド.md` が required と設定されており、*-kit のテンプレート編集時には両方が同一セッションに注入されコンテキストが冗長になる。

## 修正案

**案 A（統合）**: 2 ファイルを 1 ファイルにマージする。固有コンテンツ（Pitfall 4 のインデント問題、General authoring guidance の 4 ポイント）を統合した上で、`_injection_rules.yaml` の `テンプレート注意点.md` エントリを存続させ、`執筆ガイド.md` エントリを削除する。

**案 B（役割分離の明確化）**: `執筆ガイド.md` を *-kit フック専用の「既知バグ記録」として位置づけ、一般的なルールは `テンプレート注意点.md` のみに記述する。重複している Rules 1–3 / Pitfalls 1–3 を `テンプレート注意点.md` から `執筆ガイド.md` へ参照リンクのみにとどめ、内容の重複を解消する。

## 水平展開
同一ディレクトリに「知識の階層化を意図した」複数ドキュメントが実際にはほぼ同一内容になるパターン。新規リファレンスを追加する前に `_index.yaml` の既存ドキュメント説明と内容を突き合わせて重複確認するステップを設けることを推奨する。
