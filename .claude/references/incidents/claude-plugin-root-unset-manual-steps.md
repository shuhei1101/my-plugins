# claude-plugin-root-unset-manual-steps

Japanese mirror: `claude-plugin-root-unset-manual-steps.jp.md`

## What happened

While executing `work:merge` steps manually (the skill has `disable-model-invocation: true`),
the index-tool command was copied verbatim from the skill definition:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py" list-active .work/tasks/index.yaml
```

This failed with:

```
python: can't open file '/scripts/index-tool.py': [Errno 2] No such file or directory
```

`${CLAUDE_PLUGIN_ROOT}` expanded to an empty string, so the path became `/scripts/index-tool.py`.

## Why it happened

`CLAUDE_PLUGIN_ROOT` is injected by the Claude Code skill runner when a skill executes normally.
When steps are run manually via the Bash tool — as required for skills with
`disable-model-invocation: true` — the env var is absent from the shell environment.

## Prevention

Before executing any skill step that references `${CLAUDE_PLUGIN_ROOT}`, locate the script
with `find`:

```bash
find /path/to/repo -path "*/scripts/index-tool.py" | head -1
```

Then substitute the literal path:

```bash
python plugins/work/scripts/index-tool.py list-active .work/tasks/index.yaml
```
