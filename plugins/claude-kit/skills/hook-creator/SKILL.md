---
name: hook-creator
description: |
  Create a prompt-injection hook — a hook that injects a text prompt into Claude's context at a specific event.
  Trigger when the user says "I want to give Claude instructions at a specific moment", "inject a prompt on hook",
  "create a hook that tells Claude to do X when Y happens", "hook でプロンプトを差し込みたい",
  "特定のタイミングで AI に指示を出したい", or invoked explicitly as `/claude-kit:hook-creator`.
---

# hook-creator — Prompt-Injection Hook Creator (thin wrapper)

Authoring guidance for hooks now lives in this plugin's references and is **auto-injected** by the
`claude-kit-references-injection` hook whenever you edit a `hooks.json`, a `.claude/settings.json`,
or a `hooks/prompts/*.md`. This skill is a thin wrapper, kept for explicit invocation and for callers.

## What to do

1. Follow `references/hooks.md` + `references/common.md` (in this plugin). They are injected
   automatically when you write the hook config; if not, read them directly. Together they cover:
   hook events and the event mapping, the injection mechanism, when to use hooks, loop prevention
   (`stop_hook_active` / one-time token / session-flag), ready-to-use `hooks.json` snippets,
   prompt-file placement, and path variables.
2. For reference auto-injection hooks specifically, do **not** hand-build — use `/ref-inject:apply <plugin>`.
3. Create the prompt file (+ `.jp.md` mirror for plugin hooks), wire `hooks.json` / `settings.json`,
   and add a loop guard for `Stop` / `PreToolUse` block-type hooks.
4. Stamp each generated file per `references/provenance.md` — it is auto-injected when you write the
   file, so write the stamp directly (no skill call needed).
