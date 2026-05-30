# *-kit References Injection Sync

`dev-kit` and `claude-kit` share the same reference auto-injection structure. When changing the
shared structure in one kit, **update the other kit in the same commit**.
Japanese mirror: `references/kit-hooks-sync.jp.md`

---

## Shared structure

Both kits share identical injection infrastructure:

| File | Role |
|---|---|
| `plugins/*-kit/hooks/scripts/inject_references.py` | Hook body (same logic, only env var names and log tag differ) |
| `plugins/*-kit/hooks/scripts/_common.py` | Common helpers (same functions, only ENV_PREFIX differs) |
| `plugins/*-kit/hooks/hooks.json` | PreToolUse registration (same format) |
| `plugins/*-kit/hooks/templates/injection.md.j2` | Injection template EN (only plugin name differs) |
| `plugins/*-kit/hooks/templates/injection.jp.md.j2` | Injection template JP |
| `plugins/*-kit/references/_index.yaml` | Reference list (EN); `references:` array of path + description |
| `plugins/*-kit/references/_index.jp.yaml` | Reference list JP mirror |
| `plugins/*-kit/references/_injection_rules.yaml` | pattern → required/optional mapping |
| `plugins/*-kit/references/CLAUDE.md` | Index-style landing: "read _index.yaml" |
| `plugins/*-kit/references/CLAUDE.jp.md` | JP mirror of CLAUDE.md |

The structure (format, parse spec, template variables, YAML schema) must stay in sync across both
kits — the hook parser assumes they match.

## When editing the shared structure

When changing the injection mechanism in **either** kit:

- [ ] `inject_references.py` function / variable / env-var conventions (`{PLUGIN}_INJECTION_*`) match across kits
- [ ] `hooks.json` matcher / command structure matches across kits
- [ ] Template variables (`file_path`, `required`, `optional`, `ref.path`, `ref.description`, `ref.body`) and Jinja2 control syntax match
- [ ] `_index.yaml` YAML schema (`references:` array, `path` + `description` key names) matches
- [ ] `_injection_rules.yaml` YAML schema (`rules:` array, `pattern` + `required` + `optional` key names) matches
- [ ] `references/CLAUDE.md` (+ jp) management sections match

**Content-only changes** (adding a reference entry, adding a pattern) do not require cross-kit updates.
But if key names, types, or naming conventions change — that counts as a structural change.

## Prohibitions

- Changing `inject_references.py` in one kit without updating the other (breaks or diverges the hook)
- Renaming `_injection_rules.yaml` keys in only one kit
- Adding a convenience feature to one kit's injection hook without updating the other
