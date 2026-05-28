# session-kit built then removed after its premise changed (PR155)

## What happened

`session-kit` was created in PR150 and pivoted in PR151 to manage the lifetime of py-kit/next-kit's reference **injection tokens**: it deleted the session's tokens on every `UserPromptSubmit` so references would **re-inject each conversation turn** (keeping injected guidance fresh in long sessions), and GC'd stale tokens (1-day TTL).

In PR155 the user asked "didn't this end up being unnecessary? can we just delete it?" Investigation confirmed: nothing hard-depends on session-kit (consumers create/check their own tokens; session-kit deletes them externally), so removal is safe. The user chose to delete it (option A); py-kit/next-kit fall back to once-per-session injection.

## Root cause

session-kit's value was **per-turn re-injection** — worth it only if the injected content is heavy enough to get buried and forgotten in a long conversation. But PR147 had already changed injection to **path + description pointers only** (no full bodies). Once injection was pointer-only, the marginal value of re-injecting those pointers every turn no longer justified a dedicated cross-plugin plugin plus the `~/.claude/tokens/` lifetime convention.

The infrastructure (session-kit) outlived the premise (heavy full-body injection) that justified it. The premise was removed in PR147, but the dependent infrastructure was not revisited until PR155.

## Lesson

**When the premise of an optimization changes, revisit whether the infrastructure built for it is still justified.** Concretely: PR147 (full-body → pointer injection) should have triggered a review of session-kit, since per-turn freshness matters far less for lightweight pointers. Instead session-kit lived on for several PRs.

Also: a whole separate plugin + cross-plugin path/token convention is a heavy price for a marginal UX optimization. This echoes [[premature-cross-plugin-centralization]] (don't build cross-plugin machinery prematurely) but from a different angle — here the machinery was justified at creation time and only became dead weight once a *different* change (PR147) undercut its premise.

## Related

- [[premature-cross-plugin-centralization]] — same family (over-built cross-plugin infra)
- [[injection-hook-full-body-bloat]] — PR147, the change that undercut session-kit's premise
- Removed plugin: `plugins/session-kit/` (PR155)
