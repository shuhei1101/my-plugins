---
description: Auto-loaded when editing any SKILL.md — enforces JP mirror update in the same commit
globs:
  - "plugins/**/skills/**/SKILL.md"
---

# SKILL.md JP Mirror Sync Rules

`SKILL.md` を編集したら、**必ず同じコミットで `SKILL.jp.md` も更新する**。

## Required sync targets

| 編集したファイル | 必ず同時に更新するファイル |
|---|---|
| `plugins/{name}/skills/{skill}/SKILL.md` | `plugins/{name}/skills/{skill}/SKILL.jp.md` |

## What to update in SKILL.jp.md

- 追加したセクション → 対応する日本語セクションを追加する
- 変更した文言 → 対応箇所を日本語でも変更する
- 削除したセクション → 対応する日本語セクションも削除する

## Checklist before committing

- [ ] `SKILL.md` の変更内容が `SKILL.jp.md` に日本語で反映されている
- [ ] `SKILL.jp.md` のセクション構成が `SKILL.md` と一致している
- [ ] `SKILL.jp.md` の冒頭に JP ミラー警告コメント（`<!-- This file is a Japanese mirror... -->`）が含まれている

## JP ミラー警告コメント

すべての JP ミラーファイル（`*.jp.md`）には、ファイル冒頭に以下のような警告コメントが必須:

```
<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
```

JP ミラーを作成・編集する際は、このコメントが残っていることを必ず確認すること。

## Why

`SKILL.jp.md` はユーザーが内容を確認するための日本語リファレンス。
片方だけ更新すると内容が乖離し、意図と異なる動作をしているように見える原因になる。
