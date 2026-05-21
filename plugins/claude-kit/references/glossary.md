# glossary — Project Glossary Format

Documents the structure and usage of `.claude/rules/glossary.md`, which stores
project-specific terminology so Claude doesn't misinterpret or ask about the same
terms repeatedly.

---

## File Structure

```
.claude/rules/
└── glossary.md     # Always loaded — keep short
```

Unlike `incidents`, glossary has no separate detail files. All content lives in the
single rule file, organized by category.

---

## glossary.md Format

```markdown
# Glossary

## {Category}

| Term | Definition |
|---|---|
| {term} | {1–2 sentence definition} |
```

### Category guidelines

Group terms by domain. Examples:

- `## Architecture` — system components, layers, design patterns
- `## Workflow` — process names, phases, commands
- `## Files & Paths` — key filenames, directory roles
- `## People & Teams` — roles, team names, stakeholders

Add new categories as needed. Keep category names broad enough to hold multiple terms.

---

## Writing discipline

glossary.md is **always loaded** as a system prompt — every line costs context window.

- Definitions: 1–2 sentences only. If you need more, the term probably belongs in a
  spec document, not the glossary.
- When in doubt, don't add. Only record terms a reader would genuinely misunderstand.
- Never duplicate content already in CLAUDE.md or a rule file.

---

## When Claude adds terms

The `conversation-to-claude` skill detects new terms in Step 1 and proposes them to
the user in the glossary block of the proposal. After the user approves, Claude:

1. Reads the existing glossary to avoid duplicates
2. Uses the inferred definition from conversation context
3. Places the term under the most appropriate existing category (or creates one)
4. Writes conservatively — if unsure whether a term qualifies, skip it
