# claude-kit Plugin Developer Guide

## Authoring knowledge lives in `references/`, auto-injected

The authoring guides for each instruction-file type live in `references/` (`common.md`,
`skills.md`, `rules.md`, `hooks.md`, `claude-md.md`, `plugin-structure.md`). The
`claude-kit-references-injection` hook (`hooks/inject_references.py`) injects the matching guide
**in full body** when you edit the corresponding file (a `SKILL.md`, a rule, a `CLAUDE.md`, a
`hooks.json`, a `plugin.json`, …) — see `references/injection_rules.yaml` for the path→reference
map.

- The creator skills (`skill-creator` / `rule-creator` / `hook-creator` / `claude-creator` /
  `plugin-creator`) are **thin wrappers** that defer to these references. Edit the target file
  directly; the guide is injected. The wrappers remain for explicit invocation and for callers
  (e.g. `notes-to-claude`).
- **Do not load other skills in a Step 0** — reading skills at startup costs 2500 × N tokens. The
  injection mechanism replaces the old "Step 0: read background materials" pattern.

This injection structure is shared across all `*-kit` plugins (py-kit / next-kit / claude-kit) — see
the `kit-hooks-index-sync` rule. Attach it to a plugin with `/ref-inject:apply <plugin>`; never
hand-edit the mechanism per plugin (change the `ref-inject` templates and re-apply).

## Hooks

claude-kit ships a single hook: the `claude-kit-references-injection` hook
(`hooks/inject_references.py`, `PreToolUse(Edit | Write | MultiEdit | Read)`). There are
**no dispatch / check guards** — they were removed in favor of reference injection (creator-dispatch
in PR159; `j2-stamp-check` and the PostToolUse `jp-mirror-check` in PR161). JP-mirror sync is
enforced by the project's `*-jp-mirror-sync` rules.

> General guidance if you ever add a guard-style hook back: use `PreToolUse` (not `UserPromptSubmit`,
> which only scans the user's text); use a per-session flag (`/tmp/{hook}-{session_id}`) so it fires
> once per session; extract the logic into a script file, not an inline `-c` one-liner (inline python
> breaks on quote-nesting — incident `statusline-python-quote-nesting`).
