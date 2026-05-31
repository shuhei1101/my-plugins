# ISSUE-066: JP ミラー標準ヘッダーコメントが欠落しているファイル（10 件）

**作成日**: 2026-05-31

## 問題

JP ミラーファイルには先頭に以下の標準ヘッダーコメントを付与する規約がある:

```
<!-- This file is a Japanese mirror of {source}.md. When updating the English original, update this file too. -->
```

以下の 10 ファイルにはこのコメントが存在しない（または旧形式 `<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->` のままで `of {source}.md` が欠けている）。

| No | ファイル | 現状のヘッダー |
|---|---|---|
| 1 | `plugins/claude-kit/hooks/prompts/references-edit-guard.jp.md` | `<!-- This file is a Japanese mirror. ... -->` (ソース名なし) |
| 2 | `plugins/claude-kit/references/hook/jinja2/テンプレート注意点.jp.md` | ヘッダーコメントなし |
| 3 | `plugins/claude-kit/references/plugin/セットアップウィザード.jp.md` | `<!-- This file is a Japanese mirror. ... -->` (ソース名なし) |
| 4 | `plugins/claude-kit/references/plugin/バージョン同期.jp.md` | `> 英語オリジナル: ...` (Markdown blockquote 形式、コメントなし) |
| 5 | `plugins/dev-kit/hooks/prompts/references-edit-guard.jp.md` | `<!-- This file is a Japanese mirror. ... -->` (ソース名なし) |
| 6 | `plugins/dev-kit/skills/plugin-config/SKILL.jp.md` | ヘッダーコメントなし (YAML frontmatter から始まる) |
| 7 | `plugins/ref-inject/templates/hooks/prompts/references-edit-guard.jp.md` | `<!-- This file is a Japanese mirror. ... -->` (ソース名なし) |
| 8 | `plugins/work/CLAUDE.jp.md` | ヘッダーコメントなし（直接 `#` 見出しから始まる） |
| 9 | `plugins/work/skills/issue-scan/SKILL.jp.md` | ヘッダーコメントなし (YAML frontmatter から始まる) |
| 10 | `plugins/work/skills/plugin-config/SKILL.jp.md` | ヘッダーコメントなし (YAML frontmatter から始まる) |

なお、SKILL.md の JP ミラーでは YAML frontmatter の直後（frontmatter 終了行 `---` の次）にヘッダーコメントを挿入する必要がある（`SKILL.jp.md` の他のファイルはこの形式を採っている）。

## 修正案

各ファイルに標準形式のヘッダーコメントを追加する:

```
<!-- This file is a Japanese mirror of {source-filename}.md. When updating the English original, update this file too. -->
```

YAML frontmatter がある SKILL ファイルの場合は frontmatter の直後の行に挿入する（`2b8048a9` コミットで行われた一括適用のパターンを参照）。

`バージョン同期.jp.md` の `> 英語オリジナル:` 形式は Markdown 出力として混入するため、HTML コメント形式に修正する。

## 水平展開

`2b8048a9` コミット（全 211 ファイル一括適用）以降に追加されたファイルでヘッダーが漏れているケース。新規 JP ミラー作成時のテンプレートにヘッダーコメントを必須項目として含めることで再発を防止できる。
