<!-- This file is a Japanese mirror. When updating the English original (glossary.md), update this file too. -->
# Glossary（用語集）

このマーケットプレイスリポジトリ固有の用語。常時ロードされるため基準は高い — 現行で使われ、
名前から非自明で、繰り返し参照される用語のみ。

英語オリジナル: `.claude/rules/glossary.md`

> 採用基準とフォーマット: `plugins/work/references/conversation/用語集.md`。

---

## ルールシステム

| Term | Description |
|---|---|
| incidents | 作業プロセスのミスを再発防止のため記録する常時ロードのログ。2 層構造: 1 行要約のインデックス（`.claude/rules/incidents.md`）と詳細ファイル（`.claude/references/incidents/{slug}.md` + `.jp.md`）。記録対象は操作・判断の誤りのみで、コードのバグは対象外。 |
| glossary | 常時ロードのプロジェクト用語ファイル（`.claude/rules/glossary.md`）。毎セッションでコンテキストを消費するため簡潔に保つ。 |
| JP ミラー (jp-mirror) | `.md` に対する `.jp.md`（または `.yaml` に対する `.jp.yaml`）の対訳。英語ファイルが source of truth かつ常時ロードで、JP ミラーは人間参照用で自動ロードされない。規約: ソースを編集してからミラーを同期する。警告コメントは YAML frontmatter の閉じ `---` の後に置き、開き `---` の前には決して置かない。 |

## プラグインの仕組み

| Term | Description |
|---|---|
| ref-inject | リファレンス自動注入の仕組み（`ref-inject` プラグインと、それが配布する `*-kit` フック）。Write/Edit/Read がマッチすると、フックは `required` リファレンスを**本文全量**、`optional` を**パス + 説明のみ**で注入する。セッション単位の二層 TTL トークン（`patterns` + `references` の名前空間）で抑制し、TTL が切れるまで同じ本文を再注入しない。 |

## work プラグイン

| Term | Description |
|---|---|
| イシューテンプレート (issue template) | イシューファイルの形式・ライフサイクル・`_index.yaml` スキーマは `plugins/work/references/work-dir/イシュー.md` に定義される。テンプレート構造を変更する場合はこのファイルを編集する — 個別イシューファイルの編集ではない。 |
