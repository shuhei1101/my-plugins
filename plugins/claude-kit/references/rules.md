# Rules Design Guide

Reference for designing, creating, and evaluating `.claude/rules/<name>.md` files.
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
- **Effect**: When any one file is edited, Claude has full context of the entire relationship

### ② Context rule (trigger-load type)

Automatically loads relevant knowledge, specs, or guidelines when working in a specific area.

- Set `paths:` to the files that, when touched, should trigger loading this rule
- Example: touching `config/` → config spec rule is loaded
- Example: touching `src/` → coding convention rule is loaded

---

## Use-case-driven `paths:` design

**Start from "when should this be read?"**

1. **Identify the use case** — in what kind of work is this rule useful?
2. **Identify the trigger file/folder** — what file is always touched during that work?
3. **Set that file in `paths:`** — the rule loads every time it is touched

**Example — context rule for a config spec**:
- Use case: when editing a config file, load the corresponding spec
- Trigger: editing something in `config/`
- Set `config/**` in `paths:` → spec rule loads every time a config file is touched

**Example — always-on rule**:
- Use case: a rule that must be followed during any work (e.g. coding conventions)
- Trigger: touching any source code
- Set a broad pattern like `src/**` or `**/*.ts` in `paths:`

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
| `## Rule Maintenance` | How to update the rule itself when files are added/removed/renamed | Recommended |

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

## Related Files

| File path | Role |
|---|---|
| `src/models/**/*.py` | Implementation |
| `tests/test_models.py` | Tests |
| `docs/specs/models.md` | Specification |

## When Editing

- [ ] Implementation and tests are consistent
- [ ] New files added to this domain → updated `paths:` and Related Files?

## Rule Maintenance

- **Added a new file** → add to `paths:` and Related Files
- **Deleted or renamed a file** → remove/update in `paths:` and Related Files
```

---

## Single-folder content: rules vs subfolder CLAUDE.md

| Priority | Choice |
|---|---|
| **See all active rules in one place** (auditability) | `.claude/rules/<name>.md` |
| **Keep rules co-located with the code** (proximity) | Subfolder `CLAUDE.md` |

Cross-path linking always belongs in `.claude/rules/`.
