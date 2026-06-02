# pretooluse-read-block-cancels-tool

Japanese mirror: `.claude/references/incidents/pretooluse-read-block-cancels-tool.jp.md`

## What happened

`inject_references.py` returned `{"decision": "block", "reason": "..."}` for all four tool names
(`Edit`, `Write`, `MultiEdit`, and `Read`). For `Edit`/`Write`/`MultiEdit` this is intentional —
the hook cancels the call, injects reference context, and Claude retries with the context available.

For `Read` the same output had an unintended side-effect: the Read was cancelled and Claude
never received the file contents. Claude then fell back to `Bash` + `sed` to read the file.

## Root cause

`decision: "block"` is the hook output format for events like `UserPromptSubmit`, `Stop`, and
`PostToolUse`. When used in a `PreToolUse` hook it also works (legacy support), but the semantics
are "cancel the tool call" — which is correct for Edit/Write but wrong for Read.

The `PreToolUse`-specific format for injecting context **without cancelling** is:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "additionalContext": "..."
  }
}
```

## Prevention

In a `PreToolUse` hook script, branch on `tool_name`:

```python
if tool_name == "Read":
    sys.stdout.buffer.write(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "additionalContext": reason,
        }
    }, ensure_ascii=False).encode("utf-8"))
else:
    sys.stdout.buffer.write(
        json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False).encode("utf-8")
    )
```

The `additionalContext` field is shown to Claude as a `system-reminder` alongside the tool result,
so the reference content is injected AND the file content is also delivered.
