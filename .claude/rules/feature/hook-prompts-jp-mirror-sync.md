---
description: Auto-loaded when editing any hook prompt file — enforces JP mirror update in the same commit
globs:
  - "plugins/**/hooks/prompts/*.md"
---

# Hook Prompts JP Mirror Sync Rules

`plugins/**/hooks/prompts/*.md` を編集したら、**必ず同じコミットで `*.jp.md` も更新する**。

## Required sync targets

| 編集したファイル | 必ず同時に更新するファイル |
|---|---|
| `plugins/{name}/hooks/prompts/{prompt}.md` | `plugins/{name}/hooks/prompts/{prompt}.jp.md` |

## What to update in *.jp.md

- 追加したセクション → 対応する日本語セクションを追加する
- 変更した文言 → 対応箇所を日本語でも変更する
- 削除したセクション → 対応する日本語セクションも削除する

## Checklist before committing

- [ ] `*.md` の変更内容が `*.jp.md` に日本語で反映されている
- [ ] `*.jp.md` のセクション構成が英語版 `*.md` と一致している
- [ ] `*.jp.md` の冒頭に JP ミラー警告コメント（`<!-- This file is a Japanese mirror... -->`）が含まれている

## JP ミラー警告コメント

すべての JP ミラーファイル（`*.jp.md`）には、ファイル冒頭に以下のような警告コメントが必須:

```
<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
```

JP ミラーを作成・編集する際は、このコメントが残っていることを必ず確認すること。

## Why

`*.jp.md` はユーザーがフックプロンプトの内容を確認するための日本語リファレンス。
フックプロンプトはフック実行時に Claude のコンテキストへ注入される指示文であるため、
片方だけ更新すると内容が乖離し、意図がミラーから読み取れなくなる。
