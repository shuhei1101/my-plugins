<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->

---
description: plugins/*/references/**/*.md を編集したら paired *.jp.md も同コミットで更新する
globs:
  - "plugins/**/references/**/*.md"
---

# References JP ミラー同期ルール

`plugins/*/references/**/*.md` を編集したら、**必ず同じコミットで `*.jp.md` も更新する**。

## 同期対象

| 編集したファイル | 必ず同時に更新するファイル |
|---|---|
| `plugins/{name}/references/**/{topic}.md` | `plugins/{name}/references/**/{topic}.jp.md` |

## JP ミラーで更新すること

- 追加したセクション → 対応する日本語セクションを追加する
- 変更した文言 → 対応箇所を日本語でも変更する
- 削除したセクション → 対応する日本語セクションも削除する

## コミット前チェックリスト

- [ ] `*.md` の変更内容が `*.jp.md` に日本語で反映されている
- [ ] `*.jp.md` のセクション構成が英語版 `*.md` と一致している
- [ ] `*.jp.md` の冒頭に JP ミラー警告コメント（`<!-- This file is a Japanese mirror... -->`）が含まれている

## JP ミラー警告コメント

すべての JP ミラーファイル（`*.jp.md`）には、ファイル冒頭に以下のような警告コメントが必須:

```
<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
```

手書きで JP ミラーを作成・編集する際は、このコメントが残っていることを必ず確認すること。

## 理由

`*.jp.md` はユーザーがリファレンスドキュメントの内容を日本語で確認するためのリファレンス。
リファレンスはフック自動注入 (ref-inject) によって Claude のコンテキストへ注入される規約・仕様のため、
片方だけ更新すると内容が乖離し、意図が JP ミラーから正しく読み取れなくなる。
