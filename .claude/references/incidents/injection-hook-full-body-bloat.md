# Auto-injection hook injected full reference bodies, bloating context

## What happened

The py-kit / next-kit references auto-injection hook (`inject_references.py`,
PreToolUse) rendered the **full body** of every matched reference file into the
`decision: block` reason. Because the hook also fires on `Read`, every file
operation that matched an `injection_rules.yaml` pattern pulled large reference
bodies into Claude's context. During an exploration phase (reading many `.py`
files), this repeated per file and bloated the context badly.

## How it was diagnosed

The user noticed the context filling up while reading source files and asked to
review the hook. Investigation showed the Jinja2 template rendered `{{ ref.body }}`
for the Required section.

## Wrong first move

AI initially proposed **removing the `Read` matcher** from `hooks.json` to stop
the firing. The user corrected this: the `Read` matcher is intentional (it lets
`issue-scan` and other read paths receive reference guidance). The trigger was
not the problem — the **volume of injected content** was.

## Fix (PR147)

1. Inject **pointers only** (path + description), never file bodies. Claude reads
   the bodies itself via `Read` on demand.
2. Removed the body read in `inject_references.py` `_read_ref()` and `{{ ref.body }}`
   from all four templates; also dropped the redundant Summary section.
3. Kept the `Read` matcher.

## Second lesson: `${CLAUDE_PLUGIN_ROOT}` is not expanded in injected text

Switching to pointers exposed a path-resolution bug: the template first emitted
`references/{{ ref.path }}` (relative). That path resolves against the **edited
project's** cwd, not the plugin cache, so Claude could not `Read` it.

`${CLAUDE_PLUGIN_ROOT}` is expanded **only inside hooks.json** (see
`claude-kit/references/hooks.md`), not inside the reason text a hook prints.
Therefore the hook script must compute and emit an **absolute path** itself
(`(refs_dir / rel_path).as_posix()`), consistent with the 1行参照パターン
(absolute path in hook reason/stdout).

## Takeaways

- Auto-injection hooks should inject **pointers, not full file bodies** — full
  bodies multiply context cost on every matching operation.
- When a hook points Claude at a plugin file to `Read`, emit an **absolute path**.
  `${CLAUDE_PLUGIN_ROOT}` works in hooks.json args only, never in injected text.
- When an injection hook bloats context, reduce **what** is injected before
  removing the **trigger** — the trigger may serve other consumers (issue-scan).
