# References designed for "best-practice coverage" had to be re-split for hook auto-injection

**Date**: 2026-05-28
**PR**: PR135 (review-next-kit-plugin)

## Background

PR135 reviewed `next-kit` references against Next.js community best practices. After 72 QA decisions were applied, AI produced 46 references covering shadcn/ui, Server Actions, testing, security, etc.

When the user inspected the result, they pointed at concrete files (`backend/api-routes.md` lines 50–60, `backend/auth.md` lines 11–22) and rejected the structure:

- `api-routes.md` packed 6 different file kinds (`route.ts` / `client.ts` / `service.ts` / `db.ts` / `query.ts` / `dbHelper.ts`) into one document. When the user only wants to write `query.ts`, the other 5 kinds of info get pulled in too.
- `auth.md` consisted mostly of "provider selection tables" comparing Better Auth / Auth.js / Lucia / Clerk / Supabase Auth. Once the decision is made, comparison tables are noise — and they cannot help a hook that auto-injects context.
- The user said: "次の PR でフックを作る前提で、ファイル名・パスでヒットしたらその reference だけ inject する形にしたい。だから 1 ファイル = 1 ユースケースに分割して、比較・選定・トレードオフは完全削除して。"

Result: QA-073 was opened and the entire references tree was re-split — **46 → 90 files**, with file names matching hook trigger keywords (`query-ts.md` / `route-ts.md` / `list-screen-tsx.md` / etc.).

## Root cause

AI optimized for **best-practice coverage** ("did we cover SEO? testing? PWA? a11y?"). It did not optimize for the **reading context** — who reads this, when, and how much surrounding context they need.

For a hook-injection world, the unit of value is *"a single file edit"*. Anything not relevant to that single file is wasted tokens.

The "比較・選定・トレードオフ" sections were especially bad: they exist to make a *decision*, but once the decision is recorded, the comparison is over and no longer useful to anyone *implementing* in the codebase. They survived only because AI defaulted to writing "thorough" docs.

## Lesson

When writing references that will be loaded by a hook (or any auto-injection mechanism):

1. **Imagine the trigger**: which file edit will cause this reference to load?
2. **One file = one trigger = one use case**. If two different file types share content, that means the shared content is structural (`api-folder-overview.md`) and gets its own thin file, OR it should be replicated and kept short.
3. **Delete comparison / selection / trade-off sections**. Record the decision in `commit message` / `.work/notes/` or as a one-liner — never as a comparison table that a hook would inject every time someone edits a file.
4. **File names should match the trigger keyword**: `query.ts` edit → `query-ts.md`; `EditScreen.tsx` edit → `edit-screen-tsx.md`; `proxy.ts` edit → `proxy.md`. This makes 1:1 mapping in `injection_rules.yaml` trivial.

## Recurrence prevention

- When designing references for a kit-style plugin, **start from `injection_rules.yaml` patterns** (the trigger map), not from a content TOC.
- Add a check in the AI's plan / QA phase: "Could a hook auto-inject this file usefully? If a single file would inject content irrelevant to the editor's current file, split it."

## Related

- PR135 commits `02a5b0e` (backend split), `fac94c5` (frontend split), `ef44fe6` (shared/error split + finalize)
- See also `premature-cross-plugin-centralization.md` (PR140 — opposite mistake: centralizing too early)
- See also `markdown-for-code-consumed-config.md` (PR140 — designing config files for humans when they are consumed by code)
