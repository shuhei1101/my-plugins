# dev-kit — Development Conventions Toolkit

Unified plugin covering Python / HTML-CSS-JS / Next.js 16 App Router / YAML / Markdown conventions.
Reference auto-injection is opt-in per language via `settings.json` env vars.

## Skills

| Skill | Purpose |
|---|---|
| `dev-kit:py-script` | Single-file (or few-file) Python script scaffold |
| `dev-kit:py-project` | Full Python project scaffold (feature-folder layout, function-first) |
| `dev-kit:html-implement` | UI screen implementation workflow (FLOCSS + design tokens) |
| `dev-kit:html-logging` | Frontend logging setup |
| `dev-kit:html-mock` | UI mock generation |
| `dev-kit:html-debug-fab` | Floating debug button (FAB) with element picker |
| `dev-kit:next-implement` | Next.js implementation workflow |
| `dev-kit:next-plan` | Next.js planning document generator |
| `dev-kit:plugin-migrate` | Sync dev-kit-generated artifacts in the project (html-implement rules, html-debug-fab widget) to the installed dev-kit version (manual `/dev-kit:plugin-migrate` only) |

## Hooks

Hook scripts live under `hooks/scripts/` with a per-plugin `_common.py` for shared helpers.

| Hook | Trigger | Purpose |
|---|---|---|
| `scripts/inject_references.py` | PreToolUse(Edit/Write/MultiEdit/Read) | Reference auto-injection per language |
| `scripts/ts_check.py` | PostToolUse(Edit/Write/MultiEdit) | `tsc --noEmit --incremental` for `*.ts`/`*.tsx` |
| `scripts/_common.py` | — (library) | Stdin parsing / env truthy / once-per-session token / block reason emitter |

## Env toggles

All toggles live in `settings.json` `env` (or `~/.claude/settings.json`).
Truthy = `true`/`1`/`yes`/`on` (case-insensitive). Falsy = anything else.

**Bold** = default value (applied when the key is unset). Booleans list `true` / `false` only (`1` / `yes` / `on` are also accepted as truthy).

### Language opt-in (reference auto-injection)

| Variable | Description | Values |
|---|---|---|
| `${DEV_KIT_PYTHON}` | Truthy injects Python references when editing matched `*.py` etc. | - true<br>- **false** |
| `${DEV_KIT_HTML}` | Truthy injects HTML references when editing `*.html` / `*.css` / `*.js` | - true<br>- **false** |
| `${DEV_KIT_NEXT}` | Truthy injects Next.js references when editing `*.ts` / `*.tsx` etc. | - true<br>- **false** |
| `${DEV_KIT_MARKDOWN}` | Truthy injects Markdown references when editing `*.md` | - true<br>- **false** |

Default is **all off**. Opt into each language your project uses.

### Other toggles

| Variable | Description | Values |
|---|---|---|
| `${DEV_KIT_NEXT_TS_CHECK}` | Run `tsc --noEmit` on `*.ts` / `*.tsx` after edit | - **true**<br>- false |
| `${DEV_KIT_INJECTION_DISABLE}` | Kill switch — a truthy value disables all reference injection | - true<br>- **false** |
| `${DEV_KIT_INJECTION_TTL}` | TTL for the per-pattern / reference token cache; seconds (integer) | **3600** |
| `${DEV_KIT_INJECTION_LANG}` | Language for injected reference bodies (`jp` for Japanese) | - **en**<br>- jp |

## Reference structure

```
references/
├── python/      # Python conventions (47 files: architecture/, core/, fastapi/, llm/, etc.)
├── html/        # HTML/CSS/JS principles (principles.md, ui-design.md)
├── next/        # Next.js conventions (90 files: backend/, frontend/, testing/, etc.)
├── markdown/    # Markdown conventions (markdown-table.md, マークダウン編集.md)
├── _index.yaml   # path + lang + description per reference (merged from all langs)
├── _injection_rules.yaml   # pattern + lang + required/optional per rule
└── ...
```

Each rule in `_injection_rules.yaml` carries `lang: python|html|next|markdown`. The hook skips rules whose
`lang` is not enabled in env. The TTL token at `~/.claude/tokens/dev-kit/{session_id}.yaml`
prevents duplicate injection.

## Changelog


| Version | Date | Summary |
|---|---|---|
| 4.14.0 | 2026-06-02 | Remove the interactive `dev-kit:plugin-config` skill; reformat the env-toggle tables to the unified 3-column layout (Variable / Description / Values, default in **bold**) |
| 4.13.0 | 2026-06-01 | Remove `dev-kit:setup-wizard` skill and `SessionStart` hook (`setup_check.py`) |
| 4.11.1 | 2026-05-31 | Remove branch-check step (master/main guard) from `plugin-migrate` — redundant with the work harness UserPromptSubmit hook |
| 4.11.0 | 2026-05-31 | Add `dev-kit:plugin-config` skill — interactively configures 6 env toggles (`DEV_KIT_PYTHON/HTML/NEXT/MARKDOWN` opt-in + `DEV_KIT_NEXT_TS_CHECK/MARKDOWN_CHECK` default-on) via numbered-list loop (PR229) |
| 4.10.0 | 2026-05-31 | Remove `markdown_frontmatter_check.py` hook; rule is already enforced via `references/markdown/マークダウン編集.md` auto-injection on `**/*.md` (PR228) |
| 4.9.0 | 2026-05-31 | Add `references-edit-guard` PreToolUse hook (via ref-inject v1.7.0) that reminds to update `_index.yaml` / `_injection_rules.yaml` **before** editing or creating files under `references/` (PR206) |
| 4.8.0 | 2026-05-31 | Remove `dev-kit:yaml` skill, `references/yaml/`, and the `yaml_skill_dispatch.py` hook (+ prompts); drop `**/index.yaml` / `**/settings.yaml(.sample)` injection patterns; the YAML conventions are out of scope for dev-kit (PR202) |
| 4.7.0 | 2026-05-31 | Add Markdown frontmatter placement check hook and reference; move `マークダウン編集.md` into `markdown/` subfolder; wire into `_injection_rules.yaml` alongside `markdown-table.md`; add `${DEV_KIT_MARKDOWN}` opt-in support (PR198) |
| 4.6.0 | 2026-05-30 | Move `yaml.md` / `yaml.jp.md` into `yaml/` subfolder to match `html/`, `next/`, `python/`, `markdown/` structure; register `yaml/yaml.md` in `_index.yaml` and add `**/index.yaml` / `**/settings.yaml(.sample)` injection rules (PR199) |
| 4.5.0 | 2026-05-30 | Move `css-js-link.md` / `common-component-first.md` from `templates/html/rules/` to `references/html/`; wire them into `_injection_rules.yaml` html patterns; remove static-copy steps from `html-implement` (Step 7) and `plugin-migrate` (Step 2) (PR200) |
| 4.4.0 | 2026-05-30 | Add `markdown/` reference subfolder with Markdown table conventions (`#` column rule, `〃` ditto mark for repeated values); injected on `**/*.md` edits (PR196) |
| 4.3.0 | 2026-05-30 | Add `dev-kit:plugin-migrate` skill — inspects/fixes dev-kit-generated artifacts (static templates + convention-following source files) against the current dev-kit version. Self-contained: no dependency on any other plugin; refuses to run on master/main; never commits on its own (PR182) |
| 4.2.0 | 2026-05-30 | Rename meta-YAML files in `references/` with `_` prefix: `index.yaml` / `index.jp.yaml` / `injection_rules.yaml` → `_index.yaml` / `_index.jp.yaml` / `_injection_rules.yaml` (PR179) |
| 4.1.0 | 2026-05-30 | Move hook scripts under `hooks/scripts/` with shared `_common.py`; behavior unchanged (PR180) |
| 4.0.0 | 2026-05-30 | Merge `py-kit` / `html-kit` / `next-kit` into `dev-kit`; opt-in language toggles via `${DEV_KIT_PYTHON}` / `${DEV_KIT_HTML}` / `${DEV_KIT_NEXT}` (PR166) |
