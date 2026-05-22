# Hooks Design Guide

Reference for designing and creating prompt-injection hooks.
Targets hooks that inject a text prompt into Claude's context (not action hooks that run external processes).
Japanese mirror: `references/hooks.jp.md`

---

## Hook events

| Event | When it fires | Purpose |
|---|---|---|
| `UserPromptSubmit` | Every time the user submits a prompt | Rules or checklists to verify on every request |
| `Stop` | Every time Claude stops responding | Post-work checks, forced follow-up |
| `PreToolUse` | Before a tool is executed | Block or confirm dangerous operations |
| `PostToolUse` | After a tool is executed | Post-edit notifications or validation |
| `SessionStart` | At session start | Initial context injection |

---

## Prompt injection mechanism

| Hook | stdout format | Effect on Claude |
|---|---|---|
| `UserPromptSubmit` | Plain text | Injected as `<system-reminder>` |
| `Stop` | `{"decision":"block","reason":"<prompt>"}` | Claude continues with that instruction |
| `PreToolUse` | `{"decision":"block","reason":"<prompt>"}` | Blocks tool execution and injects instruction |

---

## When to use hooks

Migrate content from rules / CLAUDE.md to hooks when it has these properties:

- "Check every time a prompt is submitted", "verify on every request" → `UserPromptSubmit`
- "Do X every time Claude stops", "confirm after work is complete" → `Stop`
- "Confirm before running a tool" → `PreToolUse`
- "Notify after editing a file" → `PostToolUse`

---

## What NOT to put in hooks

- Content that only needs to be confirmed once — hooks fire every time
- Long-form prompts — `Stop` hook's `reason` is shown directly to the user; keep it brief
- Block-type hooks without loop prevention → always add loop guards

---

## Loop prevention

### Stop hook

Check `stop_hook_active` in stdin JSON to skip re-fires:

```python
d = json.loads(sys.stdin.read())
if d.get('stop_hook_active'):
    sys.exit(0)  # re-fire → skip
```

### PreToolUse hook (one-time token)

```python
session_id = d.get('session_id', 'default')
token = pathlib.Path(tempfile.gettempdir()) / f'my-guard-token-{session_id}'
if token.exists():
    token.unlink()   # consume token → pass through
    sys.exit(0)
token.touch()        # block + create token
```

---

## Placement

| Location | File | Shared |
|---|---|---|
| Plugin | `plugins/{name}/hooks/hooks.json` | ✅ Bundled with plugin |
| Project (team-shared) | `hooks` section of `.claude/settings.json` | ✅ Committed to git |
| Project (local only) | `hooks` section of `.claude/settings.local.json` | ❌ Add to `.gitignore` |

---

## Path variables

| Variable | Where usable | Meaning |
|---|---|---|
| `${CLAUDE_PLUGIN_ROOT}` | Plugin hooks.json only | Plugin installation root |
| `${CLAUDE_PROJECT_DIR}` | settings.json / settings.local.json | Project root |
