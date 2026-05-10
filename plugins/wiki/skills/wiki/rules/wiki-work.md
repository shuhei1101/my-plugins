---
paths:
  - "wiki/**/*.md"
---

# Wiki / Document Work

## Master Document Principle

One fact, one document. Before editing any wiki file, check whether the same content exists elsewhere. If it does, link instead of duplicating.

## Folder layout

- All wiki files live at the same level under `wiki/`. **No subfolders.**
- `wiki/home.md` is the navigation hub. Every doc must be linked from it.

## Adding / removing docs

- Creating a new wiki doc → add a link in `wiki/home.md` (in the appropriate section).
- Deleting a wiki doc → remove its link from `wiki/home.md` and any cross-references.

## Editing a wiki doc

Before writing, grep the keyword across `wiki/` to check for duplicates. If a duplicate exists, apply the Master Document Principle: link from non-master docs to the master; never copy the content.

```markdown
For details, see [Master Doc — Section](wiki/master.md#section)
```

## Last-Updated tracking

After every document update (not initial creation), append or update at the bottom:

```markdown
**Last updated**: YYYY-MM-DD — {one-line description of what changed}
```

## What NOT to do

- Do not create subdirectories inside `wiki/`
- Do not write the same fact in multiple documents
- Do not add a new document without also updating `home.md`
