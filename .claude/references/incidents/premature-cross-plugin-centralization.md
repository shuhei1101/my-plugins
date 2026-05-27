# Premature cross-plugin centralization (PR140)

## What happened

While building py-kit v2.0.0, AI proactively created a separate `refs-inject-kit` plugin to centralize injection rules across py-kit, next-kit, and future reference-bearing plugins. The design used `${plugin-name}/path/to/ref.md` placeholder syntax and required a path-resolution layer in the hook (`~/.claude/plugins/cache/*/{plugin}/*/references/` lookup, env-var override for development).

The user reviewed the implementation and rejected it as "too complex": "py-kit や他のキットに普通に直接書いた方が良さそうやな / フックとか絶対そっちの方が楽". The entire `refs-inject-kit` plugin (5 commits, ~700 LOC) was reverted; py-kit was restored to owning its own hook, templates, and `injection_rules.yaml`.

## Root cause

The abstraction was driven by "future N plugins will need this" reasoning, but:

- At the time of extraction, only py-kit existed as a consumer; next-kit was speculative
- The placeholder syntax + cross-plugin path resolution added a non-trivial layer (glob over `~/.claude/plugins/cache/`, version selection, env var fallbacks)
- Each plugin owning its own hook is ~50 lines of duplication, which is far less cost than the centralization machinery

## Lesson

**Do not centralize across plugins just because "we might want it" later.** The threshold is:

- **2 plugins** with the same hook: maybe extract, but copy-paste is still fine
- **3+ plugins** with truly identical hooks: now extraction starts to pay off
- **Cross-plugin placeholder syntax / path resolution / version selection**: only when truly unavoidable

For PR140, the right pattern was: keep `inject_references.py` + `templates/` + `injection_rules.yaml` in py-kit. When next-kit gets the same need, copy them. Extract only after the third consumer or the third drift incident, whichever comes first.

## Related

- [[premature-abstraction]] / YAGNI principle
- Reverted plugin: `plugins/refs-inject-kit/` (PR140 commits 98f9617 → a09627b → 237c41a revert)
