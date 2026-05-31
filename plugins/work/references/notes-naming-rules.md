# Notes Naming and Index Rules

Naming conventions for `.work/notes/` files and `_index.md` management.
Japanese mirror: `references/notes-naming-rules.jp.md`

> For what to write inside a note and the fixed template, see `notes-content-rules.md`.
> A note is a **current spec sheet** — present state only, no history in the body.

---

## File naming

Use **Japanese** for file names and H1 titles. Technical identifiers (tool names, command names, code symbols) stay in their original form.

| | Example |
|---|---|
| File name | `ノートインデックス同期ルール.md` |
| H1 title | `# ノートインデックス同期ルール — _index.md 自動更新促進の設計メモ` |

Mixed names (Japanese + English identifier) are acceptable when the topic itself is primarily an English term:  
`TypeScript型チェックフック.md`, `PR用語廃止・ブランチ用語統一.md`

---

## _index.md management

`_index.md` catalogs all notes under `.work/notes/`. Always update it in the **same commit** as the note change.

| Action | Required change to `_index.md` |
|---|---|
| Create a new note | Add an entry in the appropriate category section |
| Rename a note | Update the file link and title in the entry |
| Delete a note | Remove the entry |

**Before creating a new note, read `_index.md`** to check for duplicates and find the right category.
