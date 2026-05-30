# claude-kit Plugin Developer Guide

## Authoring knowledge lives in `references/`, auto-injected

The authoring guides for each instruction-file type live in `references/` (`common.md`,
`skills.md`, `rules.md`, `hooks.md`, `claude-md.md`, `plugin-structure.md`, plus `glossary.md` /
`incidents.md` / `plugin-config.md`). The `claude-kit-references-injection` hook (`hooks/scripts/inject_references.py`)
injects the matching guide **in full body** when you edit the corresponding file (a `SKILL.md`, a
rule, a `CLAUDE.md`, a `hooks.json`, a `plugin.json`, …) — see `references/_injection_rules.yaml`
for the path→reference map.

- The creator skills (`skill-creator` / `rule-creator` / `hook-creator` / `claude-creator` /
  `plugin-creator`) are **thin wrappers** that defer to these references. Edit the target file
  directly; the guide is injected. The wrappers remain for explicit invocation and for callers
  for explicit invocation.
- **Do not load other skills in a Step 0** — reading skills at startup costs 2500 × N tokens. The
  injection mechanism replaces the old "Step 0: read background materials" pattern.

This injection structure is shared across all `*-kit` plugins (dev-kit / claude-kit) — see
the `kit-hooks-index-sync` rule. Attach it to a plugin with `/ref-inject:apply <plugin>`; never
hand-edit the mechanism per plugin (change the `ref-inject` templates and re-apply).

## Hooks

claude-kit ships a single hook: the `claude-kit-references-injection` hook
(`hooks/scripts/inject_references.py`, `PreToolUse(Edit | Write | MultiEdit | Read)`). There are
**no dispatch / check guards** — they were removed in favor of reference injection (creator-dispatch
in PR159; `j2-stamp-check` and the PostToolUse `jp-mirror-check` in PR161). JP-mirror sync is
enforced by the project's `*-jp-mirror-sync` rules.

> General guidance if you ever add a guard-style hook back: use `PreToolUse` (not `UserPromptSubmit`,
> which only scans the user's text); use a per-session flag (`/tmp/{hook}-{session_id}`) so it fires
> once per session; extract the logic into a script file, not an inline `-c` one-liner (inline python
> breaks on quote-nesting — incident `statusline-python-quote-nesting`). Hook scripts live under
> `hooks/scripts/` with a per-plugin `_common.py` for shared helpers (introduced in PR180).

## Environment Variables

| Variable | Values | Default | Description |
|---|---|---|---|---|
| `CLAUDE_KIT_INJECTION_DISABLE` | `true`/`1`/`yes`/`on` | (unset = ON) | Master kill switch — set to a truthy value to stop all reference injection |
| `CLAUDE_KIT_INJECTION_TTL` | integer (seconds) | `3600` | TTL for the per-session injection token (patterns and references) |
| `CLAUDE_KIT_INJECTION_LANG` | `en` / `jp` | `en` | Language for injected references (`jp` uses `index.jp.yaml` + `injection.jp.md.j2`) |
| `CLAUDE_KIT_JP_MIRROR` | `true` / `false` | `true` | When `false`, skip `.jp.md` mirror creation and write the main `.md` file in Japanese directly |

## Changelog

| # | Version | Summary |
|---|---|---|
| 1 | `3.47.0` | Add `references/jinja2/templates.md` — authoring rules for Jinja2 templates that emit Markdown; auto-injected on `**/hooks/templates/*.j2` edits |
| 2 | `3.46.0` | Add `references-edit-guard` PreToolUse hook — reminds to update `_index.yaml` / `_injection_rules.yaml` when editing `references/` |
| 3 | `3.44.0` | Add `CLAUDE_KIT_JP_MIRROR` env var — when `false`, skip `.jp.md` mirrors and write the main file in Japanese |
| 4 | `3.43.0` | Rename meta-YAML files under `references/` with `_` prefix; update plugin-name docs (PR179) |
| 5 | `3.42.0` | Add `CLAUDE_KIT_INJECTION_DISABLE` kill switch env var |
