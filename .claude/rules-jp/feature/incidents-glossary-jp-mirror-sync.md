<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->

---
description: incidents.md / glossary.md を編集したら rules-jp の JP ミラーも同コミットで更新する
paths:
  - .claude/rules/core/incidents.md
  - .claude/rules/core/glossary.md
  - .claude/rules-jp/core/incidents.md
  - .claude/rules-jp/core/glossary.md
---

# Incidents / Glossary JP ミラー同期ルール

`incidents.md` または `glossary.md` を編集したら、**必ず同じコミットで `rules-jp/` の JP ミラーも更新する**。

## 同期対象

| 編集したファイル | 必ず同時に更新するファイル |
|---|---|
| `.claude/rules/core/incidents.md` | `.claude/rules-jp/core/incidents.md` |
| `.claude/rules/core/glossary.md` | `.claude/rules-jp/core/glossary.md` |

## JP ミラーで更新すること

- 追加したエントリ → 対応する日本語エントリを JP ミラーにも追加する
- 変更した内容 → 対応箇所を JP ミラーでも変更する
- 削除したエントリ → JP ミラーからも削除する

## コミット前チェックリスト

- [ ] 英語版の変更内容が JP ミラーに反映されている
- [ ] JP ミラーのエントリ数が英語版と一致している
- [ ] JP ミラーの冒頭に警告コメント（`> ⚠️ **日本語ミラー**...`）が残っている

## 理由

`rules-jp/` の JP ミラーはユーザーが日本語で内容を確認するためのリファレンス。
片方だけ更新すると内容が乖離し、インシデントや用語の記録が JP 版から正しく読み取れなくなる。
