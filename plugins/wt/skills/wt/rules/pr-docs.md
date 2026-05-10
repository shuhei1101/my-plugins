---
paths:
  - "docs/PR/**/*.md"
  - "docs/PR/index.yaml"
---

# PR Document Rules

## When to create a PR doc

Create `docs/PR/PR{N}.md` before or during every PR — never after the merge. For planning PRs (no implementation, only design/roadmap), create the doc first and set `planning: true` in index.yaml.

## Required sections

```markdown
# PR{N} — {short title}

## Overview

{1–3 lines: what this PR does and why.}

## Scope

### Includes
- {item}

### Excludes
- {item}

## Changed Files

- `path/to/file` — one-line reason
```

Optional sections (add when needed): `Background`, `Prerequisites`, `Implementation Log`, `Decisions`, `Open Issues`.

## index.yaml — mandatory update

Every time you create or significantly update `docs/PR/PR{N}.md`, add or update the entry in `docs/PR/index.yaml`.

**Fields:**

| Field | Rule |
|---|---|
| `id` | PR number (int) |
| `title` | Exact h1 text from PR{N}.md |
| `type` | `feat` / `fix` / `docs` / `refactor` / `chore` / `test` |
| `tags` | Free-form list |
| `planning` | `true` if this PR contains no implementation — only planning or design docs |
| `summary` | One line (≤120 chars) describing the PR without opening the file |
| `children` | List of child PR numbers when this planning PR defines sub-PRs |
| `parent` | Parent PR number when this PR was defined by a planning PR |

**Minimal example:**

```yaml
  - id: 42
    title: 'PR42 — Add user authentication'
    type: feat
    tags: [auth, api]
    planning: false
    summary: 'JWT-based auth with refresh token rotation'
```
