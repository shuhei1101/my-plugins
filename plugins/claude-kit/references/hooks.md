# Hooks Authoring Guide

How to design and create **prompt-injection hooks** — hooks that inject a text prompt into Claude's
context when an event fires (not action hooks that run external processes for their side effects).
This guide is self-contained: when injected (because you are editing `hooks.json`, a project
`settings.json`, or a `hooks/prompts/*.md`), follow it to author the hook directly.
Japanese mirror: `references/hooks.jp.md`

---

## Hook events

| Event | When it fires | Purpose |
|---|---|---|
| `UserPromptSubmit` | Every time the user submits a prompt | Rules/checklists to verify on every request |
| `Stop` | Every time Claude stops responding | Post-work checks, forced follow-up |
| `PreToolUse` | Before a tool is executed | Block or confirm dangerous operations; inject context |
| `PostToolUse` | After a tool is executed | Post-edit notifications or validation |
| `SessionStart` | At session start | Initial context injection |
| `PreCompact` | Before context is compacted | Re-inject content that compaction would drop |

### Event mapping (from the user's description)

| User's description | Event |
|---|---|
| "every time the user submits" / "before Claude processes" | `UserPromptSubmit` |
| "when Claude finishes" / "after each response" / "on stop" | `Stop` |
| "before a tool runs" / "before Bash" | `PreToolUse` |
| "after a tool runs" / "after file edit" | `PostToolUse` |
| "at session start" | `SessionStart` |

---

## Prompt injection mechanism

| Hook | stdout format | Effect on Claude |
|---|---|---|
| `UserPromptSubmit` | Plain text (file content) | Injected as `<system-reminder>` before Claude processes the prompt |
| `Stop` | `{"decision":"block","reason":"<content>"}` | Claude continues and follows the instruction |
| `PreToolUse` | `{"decision":"block","reason":"<content>"}` | Blocks the tool and injects the instruction |

The hook reads the prompt file at runtime and embeds its content directly — the prompt file is the
source of truth for the instruction text.

---

## When to use hooks (and what not to put in them)

Migrate content from rules / CLAUDE.md to a hook when it has these properties:

- "Check every time a prompt is submitted" → `UserPromptSubmit`
- "Do X every time Claude stops" → `Stop`
- "Confirm before running a tool" → `PreToolUse`
- "Notify after editing a file" → `PostToolUse`

Do **not** put in hooks:
- Content that only needs to be confirmed once — hooks fire every time
- Long-form prompts in a `Stop` hook's `reason` (it is shown to the user) — keep it brief
- Block-type hooks without loop prevention — always add a loop guard (below)

---

## Authoring workflow

1. **Pick the event** from the mapping above.
2. **Decide placement**:

   | Placement | File | Shared |
   |---|---|---|
   | Plugin | `plugins/{name}/hooks/hooks.json` | ✅ Bundled with plugin |
   | Project (team) | `hooks` section of `.claude/settings.json` | ✅ Committed to git |
   | Project (local only) | `hooks` section of `.claude/settings.local.json` | ❌ Add to `.gitignore` |

3. **Create the prompt file** with the instruction text:
   - Plugin: `plugins/{name}/hooks/prompts/{event-name}.md` (+ `.jp.md` mirror)
   - Project: `.claude/hooks/{event-name}.md`
4. **Wire it in `hooks.json` / `settings.json`** using a snippet below.
5. **Add loop prevention** for `Stop` / `PreToolUse` block-type hooks.
6. Tell the user to restart Claude Code, then trigger the event to verify the `<system-reminder>` appears.

---

## Ready-to-use snippets

> Use `${CLAUDE_PLUGIN_ROOT}` in plugin `hooks/hooks.json`; use `${CLAUDE_PROJECT_DIR}` in project
> `settings.json`. `${CLAUDE_PLUGIN_ROOT}` is expanded **only in hooks.json**, never in the injected
> reason text.

### UserPromptSubmit — inject on every prompt

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python",
            "args": [
              "-c",
              "import sys,pathlib; p=pathlib.Path(sys.argv[1]); sys.stdout.buffer.write(p.read_bytes()) if p.exists() else None",
              "${CLAUDE_PLUGIN_ROOT}/hooks/prompts/user-prompt-submit.md"
            ]
          }
        ]
      }
    ]
  }
}
```

**Keyword filtering** (inject only when the prompt matches): replace the `-c` string with:

```
import sys,json,pathlib; d=json.loads(sys.stdin.read()); p=d.get('prompt','').lower(); q=pathlib.Path(sys.argv[1]); sys.stdout.buffer.write(q.read_bytes()) if q.exists() and any(k in p for k in ['html','css','js']) else None
```

### Stop — inject a prompt and make Claude continue (loop-safe)

The `stop_hook_active` guard prevents infinite loops.

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python",
            "args": [
              "-c",
              "import sys,json,pathlib; d=json.loads(sys.stdin.read()); sys.exit(0) if d.get('stop_hook_active') else None; p=pathlib.Path(sys.argv[1]); sys.stdout.buffer.write(json.dumps({'decision':'block','reason':p.read_text('utf-8')},ensure_ascii=False).encode('utf-8')) if p.exists() else None",
              "${CLAUDE_PLUGIN_ROOT}/hooks/prompts/stop.md"
            ]
          }
        ]
      }
    ]
  }
}
```

### PreToolUse — unconditional block

`matcher` targets specific tools. Blocks **every** matching call.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python",
            "args": [
              "-c",
              "import sys,json,pathlib; p=pathlib.Path(sys.argv[1]); sys.stdout.buffer.write(json.dumps({'decision':'block','reason':p.read_text('utf-8')},ensure_ascii=False).encode('utf-8')) if p.exists() else sys.exit(0)",
              "${CLAUDE_PLUGIN_ROOT}/hooks/prompts/pre-tool-use.md"
            ]
          }
        ]
      }
    ]
  }
}
```

### PreToolUse — conditional block with one-time token (loop-safe)

"Require confirmation each time, but let through once after confirming." Without a guard, Claude's
retry after approval hits the hook again → infinite loop. The token breaks the cycle.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python",
            "args": [
              "-c",
              "import sys,json,pathlib,re,tempfile; d=json.loads(sys.stdin.read()); cmd=d.get('tool_input',{}).get('command',''); sys.exit(0) if not re.search(r'\\bgit\\s+(push|merge)\\b',cmd) else None; token=pathlib.Path(tempfile.gettempdir())/f'my-guard-token-{d.get(\"session_id\",\"default\")}'; token.unlink() or sys.exit(0) if token.exists() else None; token.touch(); p=pathlib.Path(sys.argv[1]); sys.stdout.buffer.write(json.dumps({'decision':'block','reason':p.read_text('utf-8')},ensure_ascii=False).encode('utf-8')) if p.exists() else sys.exit(0)",
              "${CLAUDE_PLUGIN_ROOT}/hooks/prompts/pre-tool-use.md"
            ]
          }
        ]
      }
    ]
  }
}
```

> ⚠️ Use a unique token filename per hook; shared names cause cross-hook interference.
> ✅ Include `session_id` in the token name so parallel sessions cannot consume each other's token.
>
> Quote-nesting caution: inside a `-c "..."` one-liner, use single quotes internally (`d.get('x')`),
> never nested double quotes — they break the outer shell string. For anything non-trivial, extract
> the logic into a `hooks/*.py` script instead of an inline `-c` one-liner.

---

## Loop prevention

| Hook | Problem | Fix |
|---|---|---|
| `Stop` | Claude continues → stops → hook fires → loop | `stop_hook_active` flag — skip on re-fire |
| `PreToolUse` | Claude retries → hook blocks again → loop | One-time token — allow exactly one retry per block |

```python
# Stop: skip on re-fire
d = json.loads(sys.stdin.read())
if d.get('stop_hook_active'):
    sys.exit(0)
```

```python
# PreToolUse: one-time token (stop_hook_active does not exist here)
session_id = d.get('session_id', 'default')
token = pathlib.Path(tempfile.gettempdir()) / f'my-guard-token-{session_id}'
if token.exists():
    token.unlink()   # consume → allow this execution
    sys.exit(0)
token.touch()        # no token → block + create
```

### Session-flag block (block first edit, pass after)

A variant used by dispatch hooks: touch the flag on the first block and **return 0 on subsequent
calls** in the same session (do not consume). Use it for "remind once per session, then stop nagging"
hooks keyed by `f'{rule-name}-{session_id}'`.

---

## Reference auto-injection hooks — use `ref-inject`

A `PreToolUse(Edit | Write | MultiEdit | Read)` hook that injects the conventions/docs relevant to
the file Claude is about to touch. **Do not hand-build this** — use the `ref-inject` plugin:

```
/ref-inject:apply <target-plugin>
```

It copies the injection hook (`hooks/scripts/inject_references.py` + `hooks/hooks.json`), the Jinja2 templates,
and a `references/` skeleton, substituting per-plugin placeholders. Then you fill `references/_index.yaml`
(path + description), bind edit-path patterns in `references/_injection_rules.yaml`, and write the
reference docs (1 reference = 1 use case). Canonical adopters: `dev-kit`, `claude-kit`.

### Injection design (what the generated hook does)

1. On Edit/Write/MultiEdit/Read, match the target path against `_injection_rules.yaml` glob patterns.
2. Inject each matched `required` reference **in full body**, each `optional` as **path + description only**.
3. De-dupe with a **per-pattern TTL token** at `~/.claude/tokens/{plugin}/{session_id}.yaml` — a
   YAML map keyed by the matched pattern, each entry holding `expires_at` (= injection time + TTL).
   Skip while `now < expires_at`; re-inject once it elapses (TTL default 3600s, override via
   `{PREFIX}_INJECTION_TTL`). Every fire cleans expired entries and deletes emptied token files.
4. `${CLAUDE_PLUGIN_ROOT}` is **not** expanded in injected reason text — the script emits absolute paths itself.

> History: an earlier design injected pointers only (path+description, no bodies) to avoid context
> bloat (incident `injection-hook-full-body-bloat`), and used per-pattern empty marker files with no
> cleanup. The current design restores full bodies for `required` because the TTL token throttles
> re-injection to once per TTL window. There is **no `PreCompact` refresh hook** — after `/compact`
> the body re-injects once the TTL elapses.

---

## Placement and path variables

| Variable | Where usable | Meaning |
|---|---|---|
| `${CLAUDE_PLUGIN_ROOT}` | Plugin hooks.json only | Plugin installation root |
| `${CLAUDE_PROJECT_DIR}` | settings.json / settings.local.json | Project root |
| `${CLAUDE_PLUGIN_DATA}` | Plugin hooks.json only | Plugin persistent data directory |

> ⚠️ `${CLAUDE_PLUGIN_ROOT}` only works when installed as a plugin. In project `settings.json` it does
> nothing — use `${CLAUDE_PROJECT_DIR}` instead.

---

## Environment variables

To make a hook configurable, read environment variables set in `settings.json`'s `env` block via
`os.environ` (e.g. the `*-kit` injection hooks read `{PREFIX}_INJECTION_TTL` / `{PREFIX}_INJECTION_LANG`).
Full guide — set/read, scopes, defaults, conventions — in **`environment.md`** (injected alongside this
guide when you edit `hooks.json` / `settings.json`).

---

## JP Mirror Sync (Hook Prompts)

When editing `plugins/**/hooks/prompts/*.md`, **update the paired `*.jp.md` in the same commit**.

| Edited file | Must also update |
|---|---|
| `plugins/{name}/hooks/prompts/{prompt}.md` | `plugins/{name}/hooks/prompts/{prompt}.jp.md` |

### Checklist before committing

- [ ] Changes in `*.md` are reflected in `*.jp.md` in Japanese
- [ ] Section structure in `*.jp.md` matches the English `*.md`
- [ ] `*.jp.md` has the JP mirror warning comment at the top (`<!-- This file is a Japanese mirror... -->`)
