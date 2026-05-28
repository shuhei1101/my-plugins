# Rules Authoring Guide

How to design, create, and evaluate `.claude/rules/<name>.md` files (path-scoped rules).
A rule groups related files into a domain and loads automatically when Claude **reads** a file
matching its `paths:` pattern. This guide is self-contained: when injected (because you are editing
a rule file), follow it to author the rule directly. Read `common.md` alongside it.
Japanese mirror: `references/rules.jp.md`

---

## When rules load

Loads when Claude **reads** a file matching the `paths:` pattern.

- ✅ Reading a file → loads
- ✅ Editing a file (Claude reads before editing) → loads
- ❌ Shell-only commands (`mv`, `rm`, etc.) without reading → does not load
- ❌ Working without accessing a matching file → does not load

---

## Two types of rules

### ① Link rule (file-coupling type)

Bundles related files so that editing one forces the author to check the others.

- List all related files in `paths:`
- Example: abstract class + interface + child class + parent class in one rule
- Example: config file + spec doc + test cases + implementation code bundled together
- **Effect**: when any one file is edited, Claude has full context of the entire relationship

### ② Context rule (trigger-load type)

Automatically loads relevant knowledge, specs, or guidelines when working in a specific area.

- Set `paths:` to the files that, when touched, should trigger loading this rule
- Example: touching `config/` → config spec rule is loaded
- Example: touching `src/` → coding convention rule is loaded

---

## Authoring workflow

### Step 1 — Check existing coverage

Glob `.claude/rules/**/*.md`, read each `paths:`, and test whether the target files already match
an existing rule. If covered, **extend that rule** instead of creating a new file.

### Step 2 — Gather domain information

Identify:
- **Domain name** — kebab-case (e.g. `models`, `voice`, `assets-bgm`)
- **Files in this domain**, in three categories: config/schema (YAML/JSON/constants), source code, docs (specs/architecture)
- **One-line description** — what the domain does and why these files must stay in sync

### Step 3 — Validate that a rule is the right type

| If the files are… | Verdict |
|---|---|
| Spread across multiple different folders | ✅ Rule — correct for cross-path linking |
| All within a single folder | ✅ Rule (auditability) or subfolder `CLAUDE.md` (co-location) — ask which the user prefers |
| About a workflow or procedure | ⚠️ `.claude/skills/` may fit better |
| A mix | ⚠️ Split: rule for cross-path; user's choice for folder-local |

Cross-path linking always belongs in `.claude/rules/`.

### Step 4 — Check for similar existing rules

Glob and read overviews + `paths:`. On overlap: **merge** into the existing rule, or **keep separate**
only with a clear boundary (different update triggers / ownership).

### Step 5 — Write the JP mirror first, then translate

Author `.claude/rules-jp/<name>.md` in Japanese first, then produce `.claude/rules/<name>.md`
(by hand or via the `jp-mirror-translator` agent). Stamp both (see `common.md`).

> ⚠️ Do **not** place the JP mirror inside `.claude/rules/` — use `.claude/rules-jp/`. The rules
> directory is scanned recursively and would auto-load the mirror.

Always include a `## Rule Maintenance` section so Claude updates the rule itself when files in the
domain are added, removed, or renamed.

---

## Use-case-oriented `paths:` design

**Start from "when should this be read?"**

1. **Identify the use case** — in what kind of work is this rule useful?
2. **Identify the trigger file/folder** — what file is always touched during that work?
3. **Set that file in `paths:`** — the rule loads every time it is touched

**Example — context rule for a config spec**: editing `config/` should load the spec →
set `config/**` in `paths:`.

**Example — always-on rule** (e.g. coding conventions): touching any source code →
set a broad pattern like `src/**` or `**/*.ts`.

> For by-name folder patterns, prefix with `**/` (e.g. `**/tools/**/*.py`) so they match in
> monorepo subprojects, not just the project root.

---

## Consolidation and separation criteria

- **Consolidate**: rules covering the same domain with duplicated content → merge into one
- **Separate**: one rule covering unrelated domains → split by domain
  - A `paths:` spanning unrelated directories causes unnecessary context load on every touch
  - Principle: 1 domain = 1 rule file

---

## Folder structure criteria

### Required folders

| Folder | Role | What goes here |
|---|---|---|
| `core/` | Project-wide foundational rules | Coding conventions, workflow, environment setup, general dev process |
| `feature/` | Feature-specific domain knowledge | Rules per feature, specs, design decisions (1 feature = 1 file) |

### Optional folders (codebase-dependent)

| Folder | When to add |
|---|---|
| `ui/` | Frontend exists: `components/`, `pages/`, `views/`, etc. |
| `api/` | Many backend API rules / `routes/` or `handlers/` directories |
| `infra/` | Many Docker / CI/CD / deployment rules |

---

## Required sections for rule files

| Section | Content | Required |
|---|---|---|
| Frontmatter `paths:` | Glob patterns that trigger the rule | **Required** |
| `## Overview` | Description of what this rule governs | Required |
| `## Related Files` | File paths and their roles | Recommended |
| `## When Editing` | Checklist of what to verify on any edit in this domain | Recommended |
| `## Rule Maintenance` | How to update the rule itself when files are added/removed/renamed | **Recommended** |

---

## Structure example

```markdown
---
paths:
  - "src/models/**/*.py"
  - "tests/test_models.py"
  - "docs/specs/models.md"
---

## Overview

Rule linking implementation, tests, and specs for the models domain.
When editing any file in this domain, check all the others too.

## Related Files

| File path | Role |
|---|---|
| `src/models/**/*.py` | Implementation |
| `tests/test_models.py` | Tests |
| `docs/specs/models.md` | Specification |
| `.claude/rules/models.md` | This rule |

## When Editing

- [ ] Implementation and tests are consistent
- [ ] New fields are covered by tests
- [ ] Spec reflects current behavior
- [ ] New files added to this domain → updated `paths:` and Related Files?

## Rule Maintenance

- **Added a new file** → add it to `paths:` and Related Files
- **Deleted or renamed a file** → remove/update it in `paths:` and Related Files
- **Domain responsibilities changed** → update the Overview
```

---

## Single-folder content: rule vs subfolder CLAUDE.md

| Priority | Choice |
|---|---|
| **See all active rules in one place** (auditability) | `.claude/rules/<name>.md` |
| **Keep rules co-located with the code** (proximity) | Subfolder `CLAUDE.md` |

Cross-path linking always belongs in `.claude/rules/`.
