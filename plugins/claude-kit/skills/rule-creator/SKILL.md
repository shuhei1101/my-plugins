---
name: rule-creator
description: |
  Create a new path-scoped rule under .claude/rules/ using the step-based structure.
  Trigger when the user says "新しいルール作って", "ルールを新規作成", "make a rule for X", or "create a rule for".
---

# rule-creator — Path-Scoped Rule Creator (thin wrapper)

Authoring guidance for rules now lives in this plugin's references and is **auto-injected** by the
`claude-kit-references-injection` hook whenever you edit a file under `.claude/rules/`. This skill is
a thin wrapper, kept for explicit invocation and for callers (e.g. `notes-to-claude`).

## What to do

1. Follow `references/rules.md` + `references/common.md` (in this plugin). They are injected
   automatically when you write the rule file; if not, read them directly. Together they cover:
   when rules load, the two rule types (link / context), use-case-oriented `paths:` design,
   consolidation/separation criteria, folder structure, required sections, and the structure example.
2. Create `.claude/rules-jp/<name>.md` first, then produce the English `.claude/rules/<name>.md`.
   Do **not** put the JP mirror inside `.claude/rules/` (it would auto-load).
3. Stamp each file per `references/provenance.md` — it is auto-injected when you write the file, so
   write the stamp directly (no skill call needed).
