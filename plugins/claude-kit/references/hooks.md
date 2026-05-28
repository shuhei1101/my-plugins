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

### Caution 3 — de-dupe injection with a per-pattern token

Without de-duplication, every matching file operation re-injects. Use a token
keyed by the **matched rule's pattern** (not the file path) so all files matching
the same pattern share it, and inject only the references of patterns whose token
does not yet exist:

```python
token_dir = pathlib.Path.home() / '.claude' / 'tokens' / 'my-kit'   # one subfolder per plugin
required, optional, new_tokens = [], [], []
for rule in matched_rules:
    pat_hash = hashlib.sha1(rule['pattern'].encode('utf-8')).hexdigest()[:12]
    token = token_dir / f'{session_id}-{pat_hash}'
    if token.exists():
        continue                      # this pattern already injected → skip its refs
    new_tokens.append(token)
    required += rule.get('required', [])
    optional += rule.get('optional', [])
if not required and not optional:
    sys.exit(0)                       # nothing new to inject
token_dir.mkdir(parents=True, exist_ok=True)
for token in new_tokens:
    token.touch()                     # mark these patterns injected (do NOT consume)
```

> Store tokens under `~/.claude/tokens/{plugin}/` (one subfolder per plugin) to keep
> them out of the project tree and namespaced per plugin.

> Per-pattern (vs per-file) means: once a pattern's references are injected via
> any matching file, other files matching the same pattern skip them. A file that
> matches an *additional* pattern injects only that pattern's references.

> ⚠️ **Limitation — once-per-session scope.** The token lives for the whole session,
> so each pattern injects once-per-session: references inject the first time a
> matching file is touched and not again that session. `/clear` changes the
> `session_id`, so a fresh session re-injects naturally; `/compact` does **not**
> change it, so guidance summarized away by `/compact` is not re-injected. Tokens
> are empty marker files and accumulate under `~/.claude/tokens/{plugin}/` with no
> automatic cleanup. (A `session-kit` companion plugin once reset tokens per turn and
> GC'd them, but it was removed in PR155 — per-turn refresh wasn't worth a dedicated
> cross-plugin plugin for pointer-only injection.)

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
