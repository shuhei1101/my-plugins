---
paths:
  - "**/*.css"
  - "**/*.js"
  - "**/*.html"
---

# CSS Class ↔ JS DOM Access Linkage

Keeps FLOCSS class definitions in CSS and DOM access in JS / HTML in sync.

This rule auto-loads whenever you read or edit a `.css`, `.js`, or `.html` file in the project.

---

## Triggers

| When you change... | Also check... |
|---|---|
| A `.c-*`, `.p-*`, `.l-*`, `.u-*` class definition in CSS (add / remove / rename) | All `*.js` and `*.html` files that reference that class via `querySelector`, `getElementsByClassName`, `classList.add/remove`, `className`, or HTML `class="..."` |
| A `querySelector(".c-...")` / `getElementsByClassName(...)` / `classList.*` call in JS (add / remove / rename selector) | The corresponding CSS file — does the class exist? Is the BEM substructure correct? |
| A `class="..."` attribute in HTML (add / remove / rename) | The corresponding CSS file for definitions AND any JS file that queries that class |

## What to verify

1. **Existence**: every class referenced in JS / HTML has a matching definition in CSS (or is intentionally a placeholder).
2. **Layer correctness**:
   - `l-*` selectors target layout containers
   - `c-*` selectors target reusable components
   - `p-*` selectors target project-specific composites
   - `u-*` selectors target utilities (single-purpose, do not combine inside JS logic)
3. **BEM substructure**: `.c-button__icon` exists only if `.c-button` exists; `--modifier` makes sense for the block.
4. **No dead classes**: classes defined in CSS but not referenced anywhere in JS / HTML should be flagged as candidates for removal.
5. **No magic strings**: JS selectors that recur across multiple files should be hoisted to a shared `SELECTORS` constant module.

## What NOT to do

- Do not autofix renames blindly — propose the change and confirm with the user. Class renames can break CSS theme overrides, tests, and external integrations.
- Do not consider framework / library / vendor classes (e.g. `swiper-*`, `gridjs-*`) as in-scope. The rule applies to project-defined FLOCSS classes only.

---

## Rule maintenance

If the FLOCSS prefix set changes (e.g. introducing a new `t-*` Theme layer) or the linkage logic
evolves (new patterns like `data-component="..."`), update this rule file before relying on it.
The rule is meant to be the single source of truth for the linkage convention.
