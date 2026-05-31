# JP ミラーファイルヘッダー規約

## 概要

`.jp.md` ファイルの冒頭には、英語 HTML コメント形式のミラー説明のみを記載する。
日本語 blockquote による説明（`> このファイルは...`）は使用しない。

## 規約

### 採用形式（HTML コメント）

```markdown
<!-- This file is a Japanese mirror of {original}.md. When updating the English original, update this file too. -->
```

### 禁止形式（日本語 blockquote）

```markdown
> このファイルは `{original}.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `{original}.md` にも反映してください。
```

## 理由

- HTML コメントは英語で一行にまとまっており、ファイル冒頭として簡潔
- 日本語 blockquote はレンダリング時に本文として表示されてしまう
- 二重記述は冗長なため、HTML コメント形式に一本化する
