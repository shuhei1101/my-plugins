# dev-kit — Development Conventions Toolkit

Unified plugin covering Python / HTML-CSS-JS / Next.js 16 App Router / YAML conventions.
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
| `dev-kit:yaml` | YAML standards |

## Hooks

Hook scripts live under `hooks/scripts/` with a per-plugin `_common.py` for shared helpers.

| Hook | Trigger | Purpose |
|---|---|---|
| `scripts/inject_references.py` | PreToolUse(Edit/Write/MultiEdit/Read) | Reference auto-injection per language |
| `scripts/ts_check.py` | PostToolUse(Edit/Write/MultiEdit) | `tsc --noEmit --incremental` for `*.ts`/`*.tsx` |
| `scripts/yaml_skill_dispatch.py` | PreToolUse(Edit/Write) | Remind user to invoke `dev-kit:yaml` when editing YAML |
| `scripts/_common.py` | — (library) | Stdin parsing / env truthy / once-per-session token / block reason emitter |

## Env toggles

All toggles live in `settings.json` `env` (or `~/.claude/settings.json`).
Truthy = `true`/`1`/`yes`/`on` (case-insensitive). Falsy = anything else.

### Language opt-in (reference auto-injection)

| Env var | Default | Effect |
|---|---|---|
| `DEV_KIT_PYTHON` | (off) | Inject Python references when editing matched `*.py` etc. |
| `DEV_KIT_HTML` | (off) | Inject HTML references when editing `*.html`/`*.css`/`*.js` |
| `DEV_KIT_NEXT` | (off) | Inject Next.js references when editing `*.ts`/`*.tsx` etc. |

Default is **all off**. Opt into each language your project uses.

### Other toggles

| Env var | Default | Effect |
|---|---|---|
| `DEV_KIT_NEXT_TS_CHECK` | on | `tsc --noEmit` on `*.ts`/`*.tsx` after edit |
| `DEV_KIT_INJECTION_DISABLE` | off | **Truthy** disables all reference injection (kill switch) |
| `DEV_KIT_INJECTION_TTL` | 3600 (sec) | TTL for the per-pattern/reference token cache |
| `DEV_KIT_INJECTION_LANG` | `en` | Set to `jp` for Japanese reference bodies |

## Reference structure

```
references/
├── python/      # Python conventions (47 files: architecture/, core/, fastapi/, llm/, etc.)
├── html/        # HTML/CSS/JS principles (principles.md, ui-design.md)
├── next/        # Next.js conventions (90 files: backend/, frontend/, testing/, etc.)
├── yaml.md      # YAML standards
├── index.yaml   # path + lang + description per reference (merged from python/html/next)
├── injection_rules.yaml   # pattern + lang + required/optional per rule
└── ...
```

Each rule in `injection_rules.yaml` carries `lang: python|html|next`. The hook skips rules whose
`lang` is not enabled in env. The TTL token at `~/.claude/tokens/dev-kit/{session_id}.yaml`
prevents duplicate injection.
