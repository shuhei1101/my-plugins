# Incident: Duplicate Guard Hooks Added to Non-claude-kit Plugins

## Date
2026-05-25

## Summary
`skill-creator-dispatch` PreToolUse hook was added to all 4 plugins (claude-kit, dev-kit, ui-kit, work-kit) in PR121, but claude-kit already guards SKILL.md globally — the copies in dev-kit/ui-kit/work-kit were redundant duplicates. Removed in PR124.

## What Happened
- PR121 added `skill-creator-dispatch` as a `PreToolUse` block hook to 4 plugins to prevent Claude from directly editing `SKILL.md` without going through `skill-creator`.
- The hook code, flag name (`skill-creator-dispatch-{sid}`), and prompt file content were identical across all 4 plugins.
- Since claude-kit hooks apply globally (they are installed once and fire for all sessions regardless of which plugin's files are being edited), the 3 additional copies in dev-kit/ui-kit/work-kit were dead weight.

## Why It Happened
The lesson from PR121 was "PreToolUse block is more effective than UserPromptSubmit for guarding files." This was correct, but the fix over-generalized: instead of adding the hook only to claude-kit, it was added to all plugins in a cargo-cult manner.

## Fix
PR124 removed:
- `skill-creator-dispatch` entries from `PreToolUse` in `dev-kit/hooks/hooks.json`, `ui-kit/hooks/hooks.json`, `work-kit/hooks/hooks.json`
- `plugins/{dev-kit,ui-kit,work-kit}/hooks/prompts/skill-creator-dispatch.md` (and `.jp.md`)

## Prevention
When adding a **global guard hook** (one that should fire regardless of which plugin's files are being edited), add it **only to claude-kit**. claude-kit is the central toolkit plugin — its hooks run globally.

Add plugin-specific hooks only when:
- The hook should fire only for files within that plugin's scope (e.g., dev-kit hooking on `.py` / `.yaml` files)
- The behavior differs per plugin

Before adding a new hook to a non-claude-kit plugin, ask: "Does claude-kit already do this?"
