# References JP Mirror Sync

When editing `plugins/*/references/**/*.md`, **the paired `*.jp.md` must also be updated in the same commit**.
Japanese mirror: `references/common/references-sync.jp.md`

---

## Required sync targets

| Edited file | Must also update |
|---|---|
| `plugins/{name}/references/**/{topic}.md` | `plugins/{name}/references/**/{topic}.jp.md` |

## What to update in *.jp.md

- Added section → add the corresponding Japanese section
- Changed wording → apply the change in Japanese too
- Deleted section → delete the corresponding Japanese section too

## Checklist before committing

- [ ] Changes in `*.md` are reflected in `*.jp.md` in Japanese
- [ ] Section structure in `*.jp.md` matches the English `*.md`
- [ ] The JP mirror warning comment (`<!-- This file is a Japanese mirror of {source}.md ... -->`) is present at the top of every `*.jp.md`

## JP mirror warning comment

All JP mirror files (`*.jp.md`) must have the following warning comment at the top:

```
<!-- This file is a Japanese mirror of {source}.md. When updating the English original, update this file too. -->
```

## Why

`*.jp.md` files are the Japanese reference for users to review content.
References are injected into Claude's context by the ref-inject auto-injection hook, so if only
one side is updated the content drifts and the intent cannot be read correctly from the JP mirror.
