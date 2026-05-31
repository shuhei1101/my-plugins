# JPミラーヘッダーコメント規約 — 標準形式と配置ルール

すべての `.jp.md` ファイルの先頭に付与する標準ヘッダーコメントの形式と配置ルール。

## 標準形式

```
<!-- This file is a Japanese mirror of {source-filename}.md. When updating the English original, update this file too. -->
```

`{source-filename}` は対応する英語オリジナルファイル名（拡張子 `.md` を含む）。

## 配置ルール

| ファイル種別 | 配置位置 |
|---|---|
| YAML frontmatter がないファイル | ファイルの先頭行（1行目） |
| YAML frontmatter があるファイル（SKILL.jp.md など） | frontmatter 終了行 `---` の直後の行 |

YAML frontmatter がある場合、frontmatter の前には何も置いてはならない（Markdown フロントマター配置ルール）。

## よくある誤りと正しい形式

| 誤り | 正しい形式 |
|---|---|
| `<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->` | `<!-- This file is a Japanese mirror of {source}.md. When updating the English original, update this file too. -->` |
| `<!-- This file is a Japanese mirror. When updating the English original (SKILL.md), update this file too. -->` | 〃 |
| `> 英語オリジナル: \`references/...\`` | 〃 |

## 一括適用の参考

コミット `2b8048a9` で全211ファイルに一括適用済み。それ以降に作成されるJPミラーファイルには作成時に必ず含める。

## 変更履歴

| No | 日付 | 内容 |
|---|---|---|
| 1 | 2026-05-31 | ISSUE-066 対応で9ファイルのヘッダーコメントを追加・修正（ブランチ: fix/jp-mirror-header-comment） |
