---
name: rules-creator
description: Scaffold a new domain-linked path-scoped rule under .claude/rules/. Use only when rule-market has no matching rule. Trigger when user says "新しいルール作って", "ルールを新規作成", "make a rule for X", or the claude-rule gateway dispatches here after rule-market found no match.
---

# rules-creator — Scaffold a Domain-Linked Rule

A "domain rule" groups all files that belong to one feature or concern (config, source, docs,
diagrams) and ensures that editing any one of them triggers a review of all the others.
This skill walks the user through creating that rule.

---

## What is a Domain Rule?

<policy>

A domain rule answers: "which files belong together, and what must stay in sync when any of
them changes?"

**Example — "models" domain:**
- Config: `config/models.yaml`
- Source: `src/models/*.py`
- Docs: `wiki/models.md`
- Diagram: `docs/architecture.md`

When you add a new model to `config/models.yaml`, the rule reminds you to also update the
source code, wiki doc, and architecture diagram. When you edit the diagram, the rule reminds
you to check whether the config or source changed too.

The rule also lists itself as a linked resource — if the domain grows (new files added),
update the rule's linked list too.

</policy>

---

## Pre-check: Rule Market First

<policy>

Before creating anything, run `/claude-rule:rule-market list`.
Install if a matching rule exists. Only continue this skill when no market rule matches.

</policy>

---

## Coverage Check

<steps>

1. `Glob` `.claude/rules/*.md` and check `paths:` patterns.
2. If the target files are already covered, offer to extend the existing rule instead.
3. Only proceed with a new file if no existing rule covers this domain.

</steps>

---

## Procedure

### Step 1: Gather domain information

Ask the user:

1. **Domain name** — short kebab-case identifier (e.g. `models`, `auth-service`, `payment-flow`).
2. **All files in this domain** — every file that "belongs" to this feature.
   Help them think in three categories:
   - **Config / schema** — YAML, JSON, ENV files that define the domain
   - **Source code** — implementation files
   - **Documentation** — wiki pages, architecture diagrams, design docs
3. **One-line description** — what this domain does and why these files must stay in sync.

If the user describes a scenario ("when I add a model I need to update X, Y, Z"), extract
the files from that description — don't ask redundant questions.

---

### Step 2: Write the JP mirror (`.claude/rules-jp/<name>.md`)

<steps>

```markdown
---
paths:
  - "<config/schema glob>"
  - "<source glob>"
  - "<docs glob>"
---

# <Domain> ドメインルール（日本語ミラー）

> **このファイルは Claude には読み込まれません**（`.claude/rules-jp/` は公式ルールディレクトリ外）。
> 本体は `.claude/rules/<name>.md`。

## このドメインとは

<1–2 文でこのドメインが何を管理するか説明>

## リンクされたリソース

このドメインのいずれかのファイルを編集するときは、以下をすべて確認・更新すること:

| ファイル / パターン | 役割 | いつ更新するか |
|---|---|---|
| `<config file>` | 設定の正規ソース | モデル・フィールド・値を追加・変更・削除したとき |
| `src/<domain>/` | 実装コード | 設定に合わせて挙動を変更するとき |
| `docs/<doc>.md` | 設計ドキュメント | 構造・挙動が変わるとき |
| `.claude/rules/<name>.md` | このルール自体 | ドメインにファイルが増減したとき |

## 同期手順

1. 何が変わったかを確定する（新規追加・リネーム・削除・値の変更など）
2. 上のリンクリストを順に確認し、影響を受けるファイルをすべて更新する
3. ドメインのファイル構成が変わった場合はこのルール自体も更新する

## やってはいけないこと

- 1ファイルだけ更新して他は「後で」と先送りにしない
- このルールのリンクリストを古いまま放置しない
```

</steps>

---

### Step 3: Translate to the English authoritative file (`.claude/rules/<name>.md`)

<steps>

Translate line-by-line. Apply XML tags:

```markdown
---
paths:
  - "<config/schema glob>"
  - "<source glob>"
  - "<docs glob>"
---

# <Domain> Domain Rule

<when_to_apply>
When editing any file that belongs to the <domain> domain.
</when_to_apply>

## What this domain manages

<1–2 sentence description>

## Linked Resources

<linked_resources>

When editing any file in this domain, check and update ALL of the following:

| File / Pattern | Role | Update when |
|---|---|---|
| `<config file>` | Canonical config source | A value, field, or entry is added / renamed / removed |
| `src/<domain>/` | Implementation | Behavior must reflect the config change |
| `docs/<doc>.md` | Design doc | Structure or behavior changes |
| `.claude/rules/<name>.md` | This rule | Domain files are added or removed |

</linked_resources>

## Sync Procedure

<steps>

1. Identify what changed (new entry, rename, removal, value change, etc.).
2. Work through the Linked Resources table and update every affected file.
3. If the domain's file list has changed, update this rule's `paths:` and the table above.

</steps>

## Don'ts

<hard_rules>

- Do not update one file and defer the rest — do them all in the same PR/commit.
- Do not leave this rule's linked list stale when the domain grows.

</hard_rules>
```

</steps>

---

### Step 4: Update `CLAUDE.md`

If the project has a `Folder-scoped rules` table, append:

```markdown
| `<name>.md` | `<path-pattern>` — <domain description> |
```

Skip if no such table exists.

---

### Step 5: Verify and commit

<checklist>

- [ ] `.claude/rules/<name>.md` — English authoritative file
- [ ] `.claude/rules-jp/<name>.md` — Japanese mirror
- [ ] `CLAUDE.md` — updated if table present
- [ ] `CLAUDE.jp.md` — updated if CLAUDE.md was updated

Commit message: `docs(rules): <name>.md ドメインルール追加`

</checklist>

Tell the user: open a file matching the `paths:` pattern in a new Claude session and confirm
`<system-reminder> Contents of .claude/rules/<name>.md` appears.

---

## Related

- `/claude-rule:rule-market` — check library before creating from scratch
- `/claude-rule:claude-rule` — authoring conventions (bilingual, XML tags, placement)
