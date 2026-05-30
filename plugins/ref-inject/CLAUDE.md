# ref-inject Plugin Developer Guide

`ref-inject` **attaches the reference auto-injection mechanism to a plugin** (the `*-kit`
style used by `py-kit` / `next-kit`): a `PreToolUse` hook that matches the edited file path
against `injection_rules.yaml` and injects the relevant references. The target plugin can be
new or existing — `/ref-inject:apply` only contributes the **injection part**.

It does **not** centralize a shared runtime (that approach was rejected — see
`premature-cross-plugin-centralization`). Instead it copies **independent files** from
`templates/`, automating the copy-paste that the incident log blessed as the cheaper path.

There is **no generator script**. `/ref-inject:apply` has Claude read each template and write
the destination file itself, substituting placeholders as it goes — so the structure stays in
context and can be adapted per plugin.

### Scope (what this plugin does NOT own)

The `apply` skill is scoped to the **injection machinery only**. Plugin-level concerns belong
to `plugin-creator`, not here:

- It does not create/edit the target plugin's `plugin.json`
- It does not create/own the target plugin's root `CLAUDE.md`
- It does not touch `marketplace.json`

---

## Structure

```
ref-inject/
├── .claude-plugin/plugin.json
├── CLAUDE.md / CLAUDE.jp.md
├── skills/apply/SKILL.md (+ .jp.md)    # /ref-inject:apply — Claude reads templates & writes them into the target plugin
└── templates/                           # the injection files copied into a target plugin (injection part only)
    ├── hooks/
    │   ├── scripts/
    │   │   ├── inject_references.py      # PreToolUse: match path → inject references (the reusable injection script)
    │   │   └── _common.py                # Shared helpers for hook scripts (stdin, env truthy, once-per-session, block reason)
    │   ├── hooks.json
    │   └── templates/injection.md.j2 (+ .jp.md.j2)
    └── references/
        ├── index.yaml (+ index.jp.yaml)
        ├── injection_rules.yaml
        ├── CLAUDE.md (+ CLAUDE.jp.md)
        └── example/getting-started.md
```

There are no `plugin.json` / root-`CLAUDE.md` templates — those are plugin-level (owned by
`plugin-creator`), not part of the injection mechanism.

---

## Placeholders

The `apply` skill has Claude substitute these in every text template while writing it out
(derived from the target plugin's directory name):

| Placeholder | Replaced with | Example |
|---|---|---|
| `__PLUGIN_NAME__` | plugin name (kebab) | `vue-kit` |
| `__ENV_PREFIX__` | name upper-cased, non-alnum → `_` | `VUE_KIT` |
| `__LOG_TAG__` | `{name}-references-injection` | `vue-kit-references-injection` |
| `__DEFAULT_TTL__` | default TTL seconds | `3600` |

Paths mirror the template — no relocation.

---

## Injection design (baked into the hook)

- `required` references → **full body** injected (first time this session); `optional` → **path + description only**
- Token: `~/.claude/tokens/{plugin}/{session_id}.yaml`, a **two-tier** YAML map with two namespaces — `patterns` and `references` — each keyed entry has `expires_at` (epoch, = injection time + TTL). Skip while `now < expires_at`; re-inject once `now >= expires_at`. Because the expiry is baked in at injection time, changing the TTL env var does not retroactively affect already-written entries.
  - **`patterns`** throttle whether a matched pattern's reference-set is re-injected at all (a still-fresh pattern is skipped entirely)
  - **`references`** throttle whether a `required` reference's **body** is injected. If a reference was already injected this session via any pattern (still fresh), it is shown by **path only** — so a reference bound to multiple patterns is never re-injected as full body
- TTL: default `3600`s, overridable via `settings.json` `env` → `{PREFIX}_INJECTION_TTL` (shared by both tiers)
- Cleanup: every hook fire scans all `{session_id}.yaml`, drops expired entries from both namespaces, deletes emptied files (and purges stale top-level keys from the old single-tier schema)
- Language: `{PREFIX}_INJECTION_LANG=jp` switches descriptions/template to Japanese

No `PreCompact` hook: after `/compact` the reference body is dropped from context, but the
token simply re-injects once its TTL elapses — a dedicated compact-refresh hook was judged
unnecessary overhead (PR156).

The reference-tier cache (PR160) extends the original single-tier (pattern-only) token (PR156/157):
it solves the case where the same reference is bound to multiple patterns, so editing files that
match different patterns no longer re-injects the shared document body. This whole scheme replaces
the old per-pattern empty-file token (PR150/151) and the pointer-only injection (PR147) — `required`
bodies are back because the TTL token throttles re-injection.

---

## Usage

`/ref-inject:apply` against a target plugin (new or existing). Then fill `references/` with
real docs and bind them in `injection_rules.yaml`.

To change the **mechanism** for all consumers, edit `templates/` here, then re-apply the
changed templates to each consumer's `hooks/` (the references stay as-is — only the
hook/template files come from `ref-inject`).

---

## Related Plugins

| Plugin | Relationship |
|---|---|
| `py-kit` / `next-kit` | Reference-injection consumers; to be migrated onto ref-inject's templates |
| `claude-kit` | Source of `plugin-creator` (owns plugin-level files) and the common hook policy |
