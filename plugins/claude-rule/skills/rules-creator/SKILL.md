---
name: rules-creator
description: >
  Scaffold a new path-scoped rule under `.claude/rules/`. Use when: user explicitly asks to
  create a new custom rule that is NOT in the rule-market library; the claude-rule gateway
  dispatches here after rule-market found no match; user says "/rules-creator", "make a rule
  for X", "create a path-scoped rule", "ルールを新規作成", "新しいルール作って", or describes
  a new coding/workflow constraint they want Claude to follow in a specific folder.
  ALWAYS check rule-market first (run `/claude-rule:rule-market list`) before using this skill —
  if a market rule covers the need, install it instead of creating from scratch.
disable-model-invocation: false
---

# rules-creator — Scaffold a New Path-Scoped Rule

Use this when the user needs a new `.claude/rules/<name>.md` that is not in the rule-market
library. Walks the four steps required by the `claude-rule` authoring conventions.

---

## Pre-check: Rule Market First

<policy>

Before creating anything, run `/claude-rule:rule-market list`.
If a market rule covers the need → install it, do not proceed with this skill.
Only continue if no market rule matches.

</policy>

---

## Procedure

### Step 1: Ask the user three questions

Use `AskUserQuestion` for:

1. **Rule name** — the `<name>` part of `<name>.md` (e.g. `api-conventions` / `tts` / `db-schema`).
2. **Target paths** — the glob patterns for the `paths:` frontmatter
   (e.g. `src/api/**/*.ts`, `frontend/components/**/*.tsx`). Multiple allowed.
3. **One-line description** — what this rule governs and why it exists
   (e.g. "Always check OpenAPI spec before editing any API route handler").

If the user gives only a topic (e.g. "make a rule for the database layer"), propose paths
and a one-liner yourself, then confirm.

---

### Step 2: Check for duplicates

`Glob` `.claude/rules/*.md` and look for an existing rule covering the same area.

- If one exists, offer to append to it instead of creating a new file.
- If fully new, continue.

---

### Step 3: Write the JP mirror (`.claude/rules-jp/<name>.md`)

<steps>

Use this template:

```markdown
---
paths:
  - "<path-pattern>"
---

# <Area> ルール（日本語ミラー）

> **このファイルは人間向けの日本語ミラーで Claude には読み込まれません**
> （`.claude/rules-jp/` は公式 rules ディレクトリ外）。本体は `.claude/rules/<name>.md`。

## なぜ必要か

<What goes wrong if this rule isn't followed — 1–3 lines>

## ルール

<when_to_apply>
このルールが適用される条件
</when_to_apply>

- ✅ やる: <positive 1>
- ✅ やる: <positive 2>
- ❌ やらない: <prohibition 1>

## 参照ドキュメント

- <relative link to related spec / design doc>

## 編集ルール

- このファイルを編集したら、必ず `.claude/rules/<name>.md` 側も同期する
```

**When writing the JP mirror:**
- Pair "do" and "don't" entries for concreteness — easier to translate later.
- Do not stack meta-notes preemptively (write affirmative rules, not "absolutely forbidden" notes).

</steps>

---

### Step 4: Translate to the English authoritative file (`.claude/rules/<name>.md`)

<steps>

Translate the JP mirror line-by-line. Apply these conventions:

- Mirror the structure exactly (headings, lists, tables).
- Apply XML tags to semantic sections: `<when_to_apply>`, `<hard_rules>`, `<steps>`, `<policy>`,
  `<checklist>`, `<references>` as appropriate.
- "やる/やらない" → "Do: ..." / "Don't: ..." pairs.
- Replace the closing sync note with:
  "Always sync `.claude/rules-jp/<name>.md` when you edit this file."
- Remove the "このファイルは人間向け..." disclaimer (it belongs only in the JP mirror).

</steps>

---

### Step 5: Update `CLAUDE.md`

<steps>

If the project has a `Folder-scoped rules` table in `CLAUDE.md`, append a row:

```markdown
| `<name>.md` | `<path-pattern>` — <one-line summary> |
```

If `CLAUDE.md` has no such table, skip this step — don't restructure the entire file.

</steps>

---

### Step 6: Explain verification

Tell the user:

1. Open a file matching the target path in a new Claude Code session.
2. Confirm the response contains `<system-reminder> Contents of .claude/rules/<name>.md`.
3. If the rule is not loaded, revisit the `paths:` glob:
   - `**/*.py` — recursive, all `.py` files ✓
   - `*.py` — not recursive (root only) ✗
   - `**/*` — matches everything ✓

---

### Step 7: Commit

<checklist>

Commit these four files together — never a partial commit:
- `.claude/rules/<name>.md` (English authoritative)
- `.claude/rules-jp/<name>.md` (Japanese mirror)
- `CLAUDE.md` (if updated)
- `CLAUDE.jp.md` (if `CLAUDE.md` was updated)

```
docs(rules): <name>.md 新規追加 (<path-pattern>)
```

</checklist>

---

## Don'ts

<hard_rules>

- Do not write `.claude/rules/<name>.md` in Japanese — Claude reads it directly as directives.
- Do not place the JP mirror inside `.claude/rules/` — it would be auto-loaded by Claude's scan.
  Always isolate it in `.claude/rules-jp/`.
- Do not ship the English file without the JP mirror.
- Do not skip the `CLAUDE.md` table update if the table exists.

</hard_rules>

---

## Related

- `/claude-rule:rule-market` — install proven rules from the library (check here first)
- `/claude-rule:claude-rule` — full authoring conventions (bilingual convention, XML tags, placement)
