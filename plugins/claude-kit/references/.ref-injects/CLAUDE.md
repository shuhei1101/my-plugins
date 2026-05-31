# claude-kit references

Authoring guides for Claude Code instruction files (skills, rules, CLAUDE.md, hooks, plugins).
Auto-injected by the `claude-kit-references-injection` hook based on the edited file path.

These references **are the source of truth** for how to author each file type. The creator
skills (`skill-creator` / `rule-creator` / `hook-creator` / `claude-creator` / `plugin-creator`)
are now thin wrappers that defer to these docs — editing the target file injects the matching
guide directly, so you can write the file without invoking a skill.

## Reading manually

- `_index.yaml` — the list of all references (path + one-line description; parsed by the hook)
- `_injection_rules.yaml` — edit-path pattern → `required` / `optional` references

## Reading automatically

On `PreToolUse(Edit | Write | MultiEdit | Read)`, `hooks/scripts/inject_references.py`:

1. Matches the edited file path against `_injection_rules.yaml` patterns
2. Injects each matched `required` reference **in full body**, and each `optional` as **path + description only**
3. De-dupes via a two-tier TTL token at `~/.claude/tokens/claude-kit/{session_id}.yaml`
   (re-injects once `CLAUDE_KIT_INJECTION_TTL` seconds elapse, default 3600):
   - `patterns`: a matched pattern is skipped entirely while still fresh
   - `references`: a `required` reference whose body was already injected this session (via any
     pattern) is shown by **path only**, so a reference shared across patterns is never re-injected

Set `CLAUDE_KIT_INJECTION_LANG=jp` to inject Japanese descriptions (`_index.jp.yaml` + `injection.jp.md.j2`).

## Path → reference map

| Edited file | Injected guide |
|---|---|
| `**/skills/*/SKILL.md` | `common/共通ガイド.md` + `skill/スキル.md` |
| `**/CLAUDE{.local,.jp,}.md` | `common/共通ガイド.md` + `claude-md/CLAUDE-md記述ガイド.md` |
| `plugins/*/CLAUDE{.jp,}.md` | ↑ + `plugin/プラグインCLAUDE-md.md` + `plugin/バージョン同期.md` |
| `**/hooks/hooks.json`, `**/.claude/settings.json` | `common/共通ガイド.md` + `hook/フック.md` + `common/環境変数.md` |
| `**/hooks/prompts/*.md` | `hook/フック.md` |
| `**/.claude-plugin/{plugin,marketplace}.json` | `common/共通ガイド.md` + `plugin/プラグイン構造.md` + `plugin/バージョン同期.md` |
| `plugins/*/references/**/*.md` | `common/リファレンス同期.md` |
| `plugins/*-kit/hooks/scripts/*.py` | `hook/キットフック同期.md` |
| `plugins/*-kit/hooks/templates/*.j2` | `hook/キットフック同期.md` + `hook/jinja2/執筆ガイド.md` |
| `**/hooks/templates/*.j2` | `hook/jinja2/テンプレート注意点.md` |

## Maintenance

- Add a reference: create the file, add it to `_index.yaml` (+ `_index.jp.yaml`), bind it to a pattern in `_injection_rules.yaml`
- Keep `1 reference = 1 use case` so a single edited file does not pull in unrelated docs
- After editing `_injection_rules.yaml`, verify no reference is orphaned (listed in index but bound to no pattern, or vice versa)
- This injection structure is shared across all `*-kit` plugins — see the `kit-hooks-index-sync` rule; change the structure in lock-step
