# Example reference

This is a placeholder reference shipped with a freshly generated __PLUGIN_NAME__ plugin.

When a file matching a rule in `injection_rules.yaml` is edited, the hook injects the
**full body** of each `required` reference (like this file) into Claude's context.

Replace this file (and `example/`) with your real conventions, then update:

- `references/index.yaml` (+ `index.jp.yaml`) — the path + description
- `references/injection_rules.yaml` — the edit-path patterns that should trigger it

Keep one reference focused on **one use case** so editing a file pulls in only what is relevant.
