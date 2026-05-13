---
name: claude-rule
description: Gateway for all Claude Code questions and configuration. Apply when the user asks anything about Claude Code (context, status line, hooks, MCP, memory, rules, skills, how things work), or wants to create/edit CLAUDE.md, SKILL.md, .claude/rules/ files, or set up Claude Code in a project. Trigger phrases include "ルールを作る", "スキルを作る", "CLAUDE.md を作る", "クロードのコンテキストって", "ステータスラインって", "フックってどう使うの", "rule-market", "install rules".
---

# claude-rule — Claude Code Gateway

Entry point for all Claude Code questions, documentation, and configuration work.
Contains authoring conventions and dispatches to specialized skills based on what the user needs.

---

## Step 0: Read Official Docs First

<steps>

For **any** Claude Code task or question — configuration, questions about behavior, creating files,
or anything else — always check the official docs before answering or taking action.
Official Claude Code documentation: **https://code.claude.com/docs/**

Key pages by task:

| Task | Doc |
|---|---|
| Creating a skill | https://code.claude.com/docs/en/skills |
| Path-scoped rules / memory | https://code.claude.com/docs/en/memory |
| Building a plugin | https://code.claude.com/docs/en/plugins |
| Configuring hooks | https://code.claude.com/docs/en/hooks |
| MCP servers | https://code.claude.com/docs/en/mcp |

When creating a **skill**, also load the `skill-creator` skill so its latest conventions apply.
Check if it is installed: look for `/skill-creator:skill-creator` in the available skill list.
If not installed: `/plugin install skill-creator@claude-plugins-official`

</steps>

---

## Dispatch Guide

<dispatch_guide>

Identify what the user needs, then route accordingly:

| Need | Action |
|---|---|
| Question about Claude Code ("how does X work?") | Read official docs → answer from docs |
| Install proven, reusable rules | `/claude-rule:rule-market` |
| Create a new project-specific rule | Check rule-market first; if no match → `/claude-rule:rules-creator` |
| Create / update a skill | Load `skill-creator` (install if missing), then follow it |
| Edit existing CLAUDE.md / SKILL.md / rules | Apply conventions in this skill directly |
| Configure hooks | Read hooks docs; edit `.claude/settings.json` directly |
| Set up Claude Code for a new project | Run rule-market, create CLAUDE.md, see placement below |

**When to use rule-market vs rules-creator:**
Run `/claude-rule:rule-market list` first. If the needed rule is already in the library,
install it. Only create a custom rule from scratch (rules-creator) when no market match exists.

</dispatch_guide>

---

## Core Authoring Rule

<hard_rules>

- **Write all Claude-read files in English.** CLAUDE.md, SKILL.md, and `.claude/rules/*.md`
  are auto-loaded as directives. Japanese causes translation overhead and ambiguity.
- **Every English file must have a paired Japanese mirror.** The mirror is for the human author.
- **Never put Japanese content inside the authoritative English file.**
- **Never update one side without updating the other.**

</hard_rules>

---

## Mirror File Placement

<policy>

**Exact-filename auto-load** (`CLAUDE.md`, `SKILL.md`): Claude matches by exact filename.
Co-locate the JP mirror as `<basename>.jp.md` in the same directory.

| Auto-loaded (English) | Human mirror (Japanese) |
|---|---|
| `CLAUDE.md` | `CLAUDE.jp.md` |
| `SKILL.md` | `SKILL.jp.md` |

**Recursive directory scan** (`.claude/rules/`): Claude loads every `.md` file it finds,
regardless of suffix. A `.jp.md` inside `.claude/rules/` would be auto-loaded.
Use a **parallel directory** to isolate mirrors:

| Auto-loaded (English) | Human mirror (Japanese) |
|---|---|
| `.claude/rules/<name>.md` | `.claude/rules-jp/<name>.md` |

`.claude/rules-jp/` is not scanned by Claude Code — no configuration needed to exclude it.

</policy>

---

## Edit Workflow

<steps>

1. Update the **JP mirror first** — lock intent in Japanese.
2. Translate and update the **English authoritative file**.
3. Commit both files together. Single-side commits are forbidden.

</steps>

---

## XML Tags for Structural Clarity

<policy>

Use XML-style tags inside Claude instruction files to delimit semantic sections.
Claude is trained on XML-structured content and resolves tagged sections more reliably than
plain Markdown prose.

**Use XML tags in:** `CLAUDE.md`, `SKILL.md`, `.claude/rules/*.md`
**Do not use in:** JP mirrors, YAML/JSON data files, general project documentation

**Recommended tags:**

| Tag | Use for |
|---|---|
| `<when_to_apply>` | Activation condition / scope |
| `<hard_rules>` | Non-negotiable constraints |
| `<steps>` | Sequential procedure |
| `<policy>` | Behavioral rules / guidelines |
| `<checklist>` | Completion criteria |
| `<dispatch_guide>` | Decision table routing to sub-skills |
| `<references>` | Links to wikis / docs |

Keep Markdown headers for human readability; wrap the section body with the matching tag:

```markdown
## Before writing code

<steps>
1. Confirm the spec exists...
2. Check open issues...
</steps>
```

</policy>

---

## CLAUDE.md vs `.claude/rules/` Placement

<policy>

| Instruction type | Where |
|---|---|
| Applies every session, any file | `CLAUDE.md` |
| Project meta-workflow (worktree, commit, server) | `CLAUDE.md` |
| Applies only while editing a specific folder | `.claude/rules/<name>.md` with `paths:` |
| "Which specs govern this folder" reference list | `.claude/rules/<name>.md` with `paths:` |

Keep `CLAUDE.md` under ~200 lines. Prefer path-scoped rules for domain-specific content.

Path-scoped frontmatter:
```markdown
---
paths:
  - "src/api/**/*.ts"
---
```

A rule without `paths:` is loaded every session — same scope as CLAUDE.md.

</policy>

---

## Two Patterns for Path-Scoped Rules

<policy>

1. **Process / convention rules** — how to work in a folder (coding standards, checklists).
   Self-contained.
2. **Source ↔ documentation linking rules** — list the spec docs or reference materials governing
   a folder. When Claude edits source under that path, the rule injects "relevant specs are X, Y, Z".

</policy>

---

## Meta-rule: Editing a Rule File

<steps>

1. Check whether docs referenced in the rule still match the current content.
2. Update the `.claude/rules-jp/<same-name>.md` mirror.
3. Commit EN original + JP mirror in the same commit.

</steps>

---

## Cross-Platform Script Policy

<policy>

Rules and skills in this plugin must work on both Linux/Mac (Bash) and Windows (PowerShell).

**Shell commands** — always provide both versions, Bash first:

```bash
# Bash (Linux / Mac)
find ~/.claude -name "sync_rules.py" -path "*target*" 2>/dev/null | head -1
```
```powershell
# PowerShell (Windows)
Get-ChildItem ~/.claude -Recurse -Filter "sync_rules.py" | Where-Object { $_.FullName -like "*target*" } | Select-Object -First 1 -ExpandProperty FullName
```

**Python scripts** — use Python for complex logic; it runs on both platforms without changes.
- Invoke as `python script.py` (use `python3` if Python 3 is not the default)
- Use `pathlib.Path` for file paths — never hardcode `/` or `\` separators
- Write comments and docstrings in **Japanese** (scripts are for humans, not for Claude)

**Quick reference — Bash / PowerShell equivalents:**

| Operation | Bash | PowerShell |
|---|---|---|
| Find file by name | `find ~ -name "file.py" 2>/dev/null` | `Get-ChildItem ~ -Recurse -Filter "file.py" -ErrorAction SilentlyContinue` |
| Home directory | `~` | `~` (also `$HOME` or `$env:USERPROFILE`) |
| Run Python | `python script.py` | `python script.py` |
| Path separator | `/` | `/` or `\` (both work in pwsh) |

</policy>

---

## File Summary

| File | Language | Auto-loaded? | Purpose |
|---|---|---|---|
| `CLAUDE.md` | English | Yes | Project-level instructions |
| `CLAUDE.jp.md` | Japanese | No | Human reference |
| `SKILL.md` | English | Yes | Skill definition |
| `SKILL.jp.md` | Japanese | No | Human reference |
| `.claude/rules/<name>.md` | English | Yes (path match or always) | Scoped or always-on rule |
| `.claude/rules-jp/<name>.md` | Japanese | No | Human reference for the rule |
