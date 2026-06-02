---
name: claude-kit:plugin-creator
description: |
  Create or update a Claude Code plugin with versioning (changelogs/ folder).
  Trigger when the user says "新しいプラグインを作りたい", "プラグインを作って", "プラグインを更新したい", "create a plugin", "update a plugin", "make a new plugin", or "plugin-creator して".
---

# plugin-creator — Plugin Scaffold & Update (thin wrapper)

Authoring guidance for plugins now lives in this plugin's references and is **auto-injected** by the
`claude-kit-references-injection` hook whenever you edit a `plugin.json` or `marketplace.json`. This
skill is a thin wrapper, kept for explicit invocation.

## What to do

1. Follow `references/plugin-structure.md` + `references/common.md` (in this plugin). They are
   injected automatically when you write `plugin.json` / `marketplace.json`; if not, read them
   directly. Together they cover: the standard directory layout, create-vs-update mode, plugin.json
   fields, the marketplace.json entry, version bump rules, the plugin.json/marketplace.json/changelog
   version-sync invariant, and the changelog format.
2. Keep the version identical across `plugin.json`, the `marketplace.json` entry, and
   `changelogs/v{X.Y.Z}.md`; write the changelog's "構造の変更" section.
3. For attaching the reference auto-injection mechanism to a plugin, use `/ref-inject:apply <plugin>`
   (it owns the injection files; plugin-creator owns `plugin.json` / root `CLAUDE.md` / `marketplace.json`).
4. Stamp each generated file per `references/provenance.md` — it is auto-injected when you write the
   file, so write the stamp directly (no skill call needed).
5. **Generate the required skills** — every plugin must ship `plugin-migrate`, and
   (if the plugin has env vars) `plugin-config`.
