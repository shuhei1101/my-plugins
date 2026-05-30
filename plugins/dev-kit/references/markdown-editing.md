# Markdown Editing — Frontmatter Placement

> If the file has no YAML frontmatter (`---` block), ignore this reference.

Japanese mirror: `references/markdown-editing.jp.md`

---

## Rule

In a Markdown file with a YAML frontmatter block, **nothing may appear before the opening `---`**.

```
✅ Correct
---
title: My Doc
---
<!-- warning comment or any content here -->

❌ Wrong — comment above the opening ---
<!-- This file is a Japanese mirror. ... -->
---
title: My Doc
---
```

**Why**: Most Markdown renderers (GitHub, Obsidian, etc.) only recognize the YAML block when `---`
is on the very first line. Anything above it causes the frontmatter to be rendered as body text.

## Fix

Move HTML comments and any other content to **immediately after the closing `---`**.
