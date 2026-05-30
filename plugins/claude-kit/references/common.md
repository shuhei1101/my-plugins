# Claude Configuration Common Guide

Shared reference for all creator skills and `claude-refactor`.
Japanese mirror: `references/common.jp.md`

For type-specific details, read the dedicated reference:
- Rules: `references/rules.md`
- Skills: `references/skills.md`
- Hooks: `references/hooks.md`
- CLAUDE.md: `references/claude-md.md`

---

## File type summary

| File type | When read | What to write |
|---|---|---|
| `CLAUDE.md` (root) | Every session start — always | Project-wide conventions and workflow. **Keep as thin as possible** |
| `CLAUDE.md` (subfolder) | When Claude accesses that folder | Folder description and local conventions (co-location preferred) |
| `.claude/rules/<name>.md` | When a file matching `paths:` is read | Cross-path links and missed-update prevention |
| `.claude/skills/<name>/SKILL.md` | When invoked | Multi-step workflows and procedures |
| `.claude/hooks/` + `settings.json` | On specific event (automatic) | Auto-checks, notifications, prompt injection |
| `.claude/references/<name>.md` | On-demand, when Claude needs it | Detailed explanations and reference material not needed every session |

---

## File type decision criteria

| Content nature | Best file type | Reason |
|---|---|---|
| Cross-path file sync link spanning multiple different folders | **rule** | Path-matched auto-load only when target files are edited |
| Single-folder file listing or local conventions | rule or subfolder CLAUDE.md | rule for visibility, CLAUDE.md for co-location |
| Short workflow or constraints needed project-wide at all times | **CLAUDE.md (root)** | Always loaded at session start |
| Multi-step workflow with user confirmation and branching | **skill** | On-demand invocation; does not pollute context |
| Repeated auto-check or notification triggered by events | **hook** | Auto-fires on event; injects into Claude's context |
| 1–2 line simple instruction or caution | CLAUDE.md or rule | Not complex enough to warrant a skill |
| Reference material or detailed explanation needed only sometimes | `.claude/references/` | CLAUDE.md lists path only; loaded on demand |

---

## Artifact proliferation guard

**Always-loaded context consumes the context window on every session or file read.**

- `CLAUDE.md` (root) is loaded **every** session start
- Rules with broad `paths:` patterns auto-load **every time** a matching file is opened

Adding more of these costs tokens on all work, not just the relevant task. Before creating any new artifact, apply the following checks:

### New artifact vs merge into existing — decision criteria

| Question | If YES → |
|---|---|
| Does an existing rule or skill already cover this domain? | Merge into it — do not create a new file |
| Is the content needed every session, or only during specific tasks? | If only sometimes → use `.claude/references/` not CLAUDE.md |
| Would the rule's `paths:` match nearly all files in the project? | Narrow the pattern, or move to CLAUDE.md |
| Is this a one-time observation or temporary note? | Do not persist it |

### Anti-proliferation checklist

- [ ] Checked whether an existing artifact can absorb this content first?
- [ ] For CLAUDE.md additions: is this truly needed every session?
- [ ] For rules: is `paths:` as narrow as possible?
- [ ] Not writing detail-only content to CLAUDE.md that belongs in `.claude/references/`?

---

## JP/EN mirror rules

Every file requires a corresponding JP mirror:

| English file (read by Claude) | JP mirror (human reference only) |
|---|---|
| `.claude/rules/<name>.md` | `.claude/rules-jp/<name>.md` |
| `.claude/skills/<name>/SKILL.md` | `.claude/skills/<name>/SKILL.jp.md` |
| `CLAUDE.md` (any folder) | `CLAUDE.jp.md` in the same folder |
| `.claude/references/<name>.md` | `.claude/references/<name>.jp.md` |

**Workflow — write the JP mirror first, then the English original.** Author the `.jp.md`
in Japanese, then produce the English version from it. In this repo the English original is
the file Claude actually loads, so the two must never drift. Every JP mirror must start with
the warning comment `<!-- This file is a Japanese mirror. ... -->` (see `provenance.md`).

> The repo bundles a `jp-mirror-translator` agent (`subagent_type: "claude-kit:jp-mirror-translator"`):
> pass a `.md` path to generate/update its `.jp.md`, or a `.jp.md` path to update the English original.
> Useful when authoring both sides, but writing them by hand is equally valid.
