# claude-kit Plugin Developer Guide

## Authoring knowledge lives in `references/`, auto-injected

The authoring guides for each instruction-file type live in `references/` (`common.md`,
`skills.md`, `rules.md`, `hooks.md`, `claude-md.md`, `plugin-structure.md`, plus `glossary.md` /
`incidents.md`). The `claude-kit-references-injection` hook (`hooks/scripts/inject_references.py`)
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

## Skills

| Skill | Purpose |
|---|---|
| `claude-kit:claude-creator` | Create `CLAUDE.md` files |
| `claude-kit:claude-refactor` | Refactor existing `CLAUDE.md` files |
| `claude-kit:rule-creator` | Create path-scoped rules |
| `claude-kit:skill-creator` | Create skills |
| `claude-kit:hook-creator` | Create prompt-injection hooks |
| `claude-kit:plugin-creator` | Create or update plugins |
| `claude-kit:plugin-migrate` | Sync plugin-level artifacts to the current claude-kit conventions |
| `claude-kit:jp-mirror-sync` | Sync JP mirror files (`.jp.md`) from English originals |
| `claude-kit:env-sync` | Sync env var declarations across plugin files |
| `claude-kit:statusline-setup` | Configure the Claude Code status line |
| `claude-kit:plugin-config` | Interactively configure claude-kit env variables (JP mirror, injection language, TTL) |

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

**Bold** = default value (applied when the key is unset). Booleans list `true` / `false` only (`1` / `yes` / `on` are also accepted as truthy).

| Variable | Description | Values |
|---|---|---|
| `${CLAUDE_KIT_INJECTION_DISABLE}` | Master kill switch — a truthy value stops all reference injection | - true<br>- **false** |
| `${CLAUDE_KIT_INJECTION_TTL}` | TTL for the per-session injection token (patterns and references); seconds (integer) | **3600** |
| `${CLAUDE_KIT_INJECTION_LANG}` | Language for injected references (`jp` uses `index.jp.yaml` + `injection.jp.md.j2`) | - **en**<br>- jp |
| `${CLAUDE_KIT_JP_MIRROR}` | When `false`, skip `.jp.md` mirror creation and write the main `.md` file in Japanese directly | - **true**<br>- false |

## Changelog

| # | Version | Summary |
|---|---|---|
| 1 | `3.56.0` | Remove the dead `provenance.md` concept — integrate the JP-mirror warning-comment format into `共通ガイド.md`'s JP/EN mirror section; rewrite all `provenance.md` references in `スキル.md`, the 5 creator skills, and `claude-refactor` to point there |
| 2 | `3.55.0` | Restore `claude-kit:plugin-config` skill (renamed from `config`); restore `プラグイン設定.md` authoring reference and `plugin-config` mandate in `プラグイン構造.md`; add to injection rules for SKILL.md and plugin.json patterns |
| 2 | `3.54.0` | Remove the interactive `work:plugin-config` / `dev-kit:plugin-config` skills and the `プラグイン設定.md` (config-skill) authoring reference; drop the `plugin-config` mandate from `plugin-creator` / `プラグイン構造.md`; redefine the env-table format in `プラグインCLAUDE-md.md` to the unified 3-column layout (Variable / Description / Values, default in **bold**) and reformat the `## Environment Variables` tables |
| 2 | `3.53.0` | Remove `claude-kit:config` skill |
| 3 | `3.52.0` | Add `claude-kit:jp-mirror-sync` skill (moved from `utils` plugin); remove `utils` plugin from marketplace |
| 4 | `3.51.0` | Remove `claude-kit:setup-wizard` skill and `SessionStart` hook (`setup_check.py`) |
| 5 | `3.49.1` | Remove branch-check step (master/main guard) from `plugin-migrate` — redundant with the work harness UserPromptSubmit hook |
| 6 | `3.48.0` | Reorganize `references/` into role-based subfolders (`common/`, `skill/`, `hook/`, `claude-md/`, `plugin/`); add `plugin/バージョン同期.md`; inject version-sync reminder on `plugins/*/CLAUDE.md` edits |
| 7 | `3.47.0` | Add `references/jinja2/templates.md` — authoring rules for Jinja2 templates that emit Markdown; auto-injected on `**/hooks/templates/*.j2` edits |
| 8 | `3.46.0` | Add `references-edit-guard` PreToolUse hook — reminds to update `_index.yaml` / `_injection_rules.yaml` when editing `references/` |
| 9 | `3.44.0` | Add `${CLAUDE_KIT_JP_MIRROR}` env var — when `false`, skip `.jp.md` mirrors and write the main file in Japanese |
| 10 | `3.43.0` | Rename meta-YAML files under `references/` with `_` prefix; update plugin-name docs (PR179) |
| 11 | `3.42.0` | Add `${CLAUDE_KIT_INJECTION_DISABLE}` kill switch env var |
