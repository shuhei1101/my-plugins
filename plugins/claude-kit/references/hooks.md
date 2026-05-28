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

## Reference auto-injection pattern (j2 template)

A `PreToolUse(Edit|Write|MultiEdit|Read)` hook that injects the conventions /
documentation relevant to the file Claude is about to touch. Canonical
implementation: py-kit / next-kit (`hooks/inject_references.py` +
`hooks/templates/injection.md.j2` + `references/injection_rules.yaml`).

### How it works

1. On Edit/Write/MultiEdit/Read, read the target path from stdin (`tool_input.file_path`).
2. Match it against glob patterns in `injection_rules.yaml` → collect the
   `required` / `optional` reference files for that path.
3. Render a Jinja2 template and emit it in the `decision: block` reason. Claude
   reads/follows the guidance, then retries the tool call.
4. Including `Read` lets read-only passes (e.g. code scans) receive guidance too.

### Caution 1 — inject pointers, not full bodies

Do **not** render the full body of each reference into the reason. The hook
fires on **every** matching file operation, so full-body injection re-injects
the entire content each time and bloats the context fast. Inject only
**path + a one-line description**, and let Claude `Read` the files it actually
needs. (Incident: `injection-hook-full-body-bloat`.)

### Caution 2 — use absolute paths for the injected pointers

`${CLAUDE_PLUGIN_ROOT}` is expanded **only inside hooks.json**, never in the
reason text a hook prints. A relative path like `references/foo.md` resolves
against the *edited project's* cwd (not the plugin cache) and fails. The hook
script must compute and emit an **absolute path** itself, e.g.:

```python
abs_path = (refs_dir / rel_path).as_posix()   # refs_dir derived from CLAUDE_PLUGIN_ROOT
```

### Caution 3 — block once per file per session

Use a session + file-hash token so the same file is injected only once per
session (otherwise every edit of that file re-injects):

```python
file_hash = hashlib.sha1(file_path.encode('utf-8')).hexdigest()[:12]
token = pathlib.Path(tempfile.gettempdir()) / f'my-injection-{session_id}-{file_hash}'
if token.exists():
    sys.exit(0)        # already injected this file this session → skip
token.touch()          # first time → inject (do NOT consume the token)
```

> Unlike the confirm-each-time token (which is *consumed* on retry), this token
> is left in place so the file is never re-injected within the same session.

> ⚠️ **Limitation — context resets.** This token assumes "injected once ⇒ still in
> context." But `/compact` wipes/summarizes the context while the **`session_id`
> stays the same**, so the token survives and the reference is never re-injected
> even though Claude lost it. Pair the token with a **session marker** (provided by
> the `session-kit` plugin at `/tmp/claude-session-ctx-gen-{session_id}`, bumped on
> `PreCompact`): re-inject when the marker is newer than the token. Fall back to
> plain once-per-session when the marker is absent (session-kit not installed).
> (`/clear` needs no marker — it changes the `session_id`, so a fresh session
> re-injects naturally.) session-kit also GCs stale tokens/markers (1-day TTL) on
> `SessionStart` so `/tmp` does not accumulate them.

```python
marker = pathlib.Path(tempfile.gettempdir()) / f'claude-session-ctx-gen-{session_id}'
if token.exists():
    reset_after = marker.exists() and marker.stat().st_mtime_ns > token.stat().st_mtime_ns
    if not reset_after:
        sys.exit(0)    # injected and no reset since → skip
token.touch()          # first time, or context reset since last injection → (re)inject
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
