# Markdown Editing — Frontmatter Placement

> If the file has no YAML frontmatter (`---` block), ignore this reference.

In a Markdown file with YAML frontmatter, **nothing may appear before the opening `---`** —
not HTML comments, not blank lines, nothing. Most renderers only recognize the YAML block when
`---` is on the very first line; anything above it causes the frontmatter to render as body text.

If you need a warning comment (e.g. a JP mirror notice), place it **immediately after the
closing `---`**, not before the opening one.
