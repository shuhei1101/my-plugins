# Incident: Design-phase QA included implementation detail (creep)

## Date

2026-05-27 — PR138 (review-py-kit-plugin)

## What happened

While drafting the design QA for py-kit (PR138), AI included **detailed step-by-step implementation logic** in QA-D-6 and QA-D-7 — for example, "the hook should (1) read tool_input.file_path, (2) load index.yaml, (3) iterate injection_rules, (4) collect required/optional refs, (5) render with Jinja2, (6) return decision: block …" — even though the PR's scope was to **decide policy only** and to defer implementation to a separate PR.

The user pointed this out sharply: 「こんなの書かなくていい」「フックは hook-creator スキルで普通に Python スクリプト流せるから自明」「実装は別フェーズで予約だけしておいて」.

## Root cause

AI conflated two distinct PR scopes:

1. **Policy / design PR**: decide *what to build* and *why*
2. **Implementation PR**: decide *how to build it*

When the user explicitly partitioned the work into two PRs (PR138 = policy, next PR = implementation), AI should have stopped at "what / why" in the QA and left "how" to the implementation PR. Instead, AI tried to be helpful by writing the implementation strategy in advance, creating noise that conflicted with the scope decision.

## Lesson

When a PR is explicitly scoped to **policy / design only** (with implementation deferred to a follow-up PR), the QA content must stop at:

- **What** the artifact will do
- **Why** it is needed
- **Where** it will be placed (path / file structure)
- **References to data shapes** (e.g. "use the existing index.yaml schema") when essential for the policy decision

The QA must NOT include:

- Step-by-step implementation logic
- Specific function signatures or pseudocode of the implementation
- Decisions about libraries / techniques that belong to the implementation PR

If implementation detail feels relevant during the policy QA, it is usually a sign that:

- The policy decision is not yet stable (resolve the policy first), OR
- The detail belongs as a brief data-shape contract (acceptable, e.g. YAML schema), OR
- The detail is just AI being over-helpful (cut it)

## Fix applied (PR138)

- Removed the detailed Python pseudocode from QA-D-6 and QA-D-7
- Replaced with: "implementation deferred to the next PR (`add-py-kit-references-injection-hook`)"
- Reserved two follow-up PRs in TODO.md `## 次PR候補` (rebuild-py-kit-references → add-py-kit-references-injection-hook)

## Detection signal for future sessions

If you (AI) are drafting QA content and find yourself writing:

- `# 1. ... # 2. ... # 3. ...` step lists describing how a thing works
- Pseudocode that includes specific stdlib calls or library APIs
- "The hook does X, then Y, then Z"

…and the PR description says "実装は別 PR" / "policy only" / "design only" — **stop and delete the detail**. Move it to the follow-up PR's planning notes if it has lasting value, or simply discard.
