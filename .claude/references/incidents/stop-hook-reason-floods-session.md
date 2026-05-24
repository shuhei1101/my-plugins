# Stop Hook reason Floods Session

## What happened

The Stop hook's `stop.py` script read the full contents of `stop.md` and embedded them in the `reason` field. Every time Claude finished a response, this multi-line instruction block was injected into the conversation session and displayed to the user — noisy, intrusive, and harder to read.

## Root cause

The hook output pattern was `{"decision":"block","reason":"<full file contents>"}`. The `reason` text is injected directly into the conversation session and is visible to the user on every Stop event.

## Fix

Change the `reason` to a single-line file reference: `"Read and follow: /path/to/stop.md"`. Claude reads the actual instructions from that file itself. This keeps the `reason` to one line while still delivering the full instruction set.

**Before:**
```python
response = {"decision": "block", "reason": prompt_path.read_text("utf-8")}
```

**After:**
```python
reason = f"Read and follow: {prompt_path}"
response = {"decision": "block", "reason": reason}
```

The dedicated `stop.py` script was also removed entirely; the inline python in `hooks.json` is sufficient for this simple pattern.

## Rule

- **Stop hook `reason` must be exactly 1 line** — use the file-reference pattern
- Full instruction text goes in the prompt file; the script outputs only the file path reference
- This pattern is documented in `hook-creator/SKILL.md` Step 4 Notes
