---
paths:
  - "plugins/work-kit/templates/TODO.md"
  - "plugins/work-kit/templates/.work/tasks/yyyymmdd_xxx/PRXXX/TODO.md"
  - "plugins/work-kit/skills/work-start/SKILL.md"
---

> ⚠️ **Japanese mirror** — Claude には読み込まれません。このファイルを更新する際は、必ず英語オリジナル `.claude/rules/work-kit-todo-template-sync.md` も同時に更新してください。

# work-kit TODO テンプレート同期ルール

## 概要

work-kit の TODO.md テンプレートと work-start スキルの Step 7 を同期させるルール。

TODO.md テンプレートのセクション構成と、work-start SKILL.md の Step 7（TODO記入手順）が乖離すると、
生成された TODO.md の実態とスキルのガイドが食い違う。どちらか一方を変更したら必ず他方も更新すること。

## 関連ファイル

| ファイルパス | 役割 |
|---|---|
| `plugins/work-kit/templates/TODO.md` | work-kit インストール時の参照テンプレート |
| `plugins/work-kit/templates/.work/tasks/yyyymmdd_xxx/PRXXX/TODO.md` | `.work/` フォルダ内の example テンプレート |
| `plugins/work-kit/skills/work-start/SKILL.md` | TODO.md の記入手順を定義するスキル（Step 7） |

## 編集時のチェックリスト

いずれかのファイルを編集したら、他のファイルも必ず確認する:

- [ ] `templates/TODO.md` のセクション構成が `SKILL.md` Step 7 の記入手順と一致しているか
- [ ] `templates/.work/.../TODO.md`（example）が `templates/TODO.md` と同じセクション構成か
- [ ] 新しいセクションを追加した場合、SKILL.md Step 7 にそのセクションの記入指示があるか
- [ ] セクションを削除・改名した場合、SKILL.md Step 7 の該当記述も削除・更新したか
- [ ] **新しいテンプレートファイルを追加した場合**、このルールの `paths:` と関連ファイル一覧を更新したか

## ルールのメンテナンス

このドメインでファイル操作を行ったとき:
- **テンプレートファイルを追加** → `paths:` と関連ファイル一覧に追記
- **テンプレートファイルを削除・改名** → `paths:` と関連ファイル一覧を更新
- **SKILL.md の構造が大きく変わった** → 概要セクションを更新
