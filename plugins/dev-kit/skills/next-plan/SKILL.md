---
name: dev-kit:next-plan
description: |
  Generate an implementation plan for a Next.js App Router project, feature, or API resource.
  Reads dev-kit Next.js references and outputs a structured planning document (file tree, per-file roles,
  conventions, implementation order) — without writing actual code.
  Trigger when the user says "設計を考えて", "何のファイルが必要か", "計画を立てて",
  "構成を教えて", "feature を追加したい", "API を追加したい", "新規プロジェクトを作りたい",
  or invokes `/dev-kit:next-plan` explicitly.
  Do NOT trigger for implementation tasks — use `dev-kit:next-implement` instead.
---

# dev-kit:next-plan — Implementation Plan Generator

Reads dev-kit Next.js references and outputs a structured planning document for a
new project, feature, or API resource — without writing actual code.

---

## Overview

This skill bridges the gap between "I want to build X" and "I start implementing X."
It reads the relevant references and outputs a plan that the user can review before
any files are created.

**Use cases covered by this single skill**:
1. **New project** — full initial scaffold (app structure, auth, DB, shared utilities)
2. **New feature** — add a CRUD feature (list / view / create / edit screens + Server Actions + API)
3. **New API resource** — add `app/api/v1/{resource}/` (route / client / service / db / query / dbHelper)

---

## Tasks

### Step 1: Understand the request

#### Condition

- Always — run first

#### Process

1. Identify what the user wants to build:
   - **Resource/feature name** (e.g. `users`, `products`, `orders`)
   - **Required operations** (list / view / create / edit / delete — or a subset)
   - **Interface needed** (screens only / API only / both)
2. Classify into one of:
   - `new-project` — starting from scratch (no existing Next.js project)
   - `new-feature` — adding a full CRUD feature to an existing project
   - `new-api` — adding only an API resource (no screens)
   - `new-screens` — adding only screens (API already exists)
3. If the classification is ambiguous, ask the user before continuing

→ Proceed to Step 2

#### Output

- Resource name, required operations, interface type, and classification confirmed

---

### Step 2: Load references

#### Condition

- Step 1 complete

#### Process

Read the following from `{plugin_root}/references/` (the plugin root is two levels above this skill file):

**Always**:
- `frontend/feature-folder.md`
- `frontend/route-groups.md`
- `frontend/app-folder-overview.md`

**For `new-feature` or `new-screens`** (based on required operations):

| Operation | Reference |
|---|---|
| List screen | `frontend/list-page-tsx.md`, `frontend/list-screen-tsx.md` |
| View screen | `frontend/view-page-tsx.md`, `frontend/view-screen-tsx.md` |
| Create screen | `frontend/edit-page-tsx.md`, `frontend/edit-screen-tsx.md` |
| Edit screen | `frontend/edit-page-tsx.md`, `frontend/edit-screen-tsx.md` |
| Form handling | `frontend/form-ts.md`, `frontend/use-form-pattern.md` |
| Server Actions | `backend/actions-ts.md`, `shared/error-action-handler.md` |

**For `new-feature` or `new-api`**:
- `backend/api-folder-overview.md`
- `backend/route-ts.md`
- `backend/client-ts.md`
- `backend/service-ts.md`
- `backend/db-ts.md`
- `backend/query-ts.md`
- `backend/db-helper-ts.md`

**For `new-project`** (all of the above, plus):
- `shared/environment.md`
- `shared/error-classes.md`
- `shared/logger-impl.md`
- `backend/auth-setup.md`
- `backend/db-id.md`
- `backend/db-timestamps.md`
- `backend/db-relations.md`
- `frontend/endpoints.md`
- `frontend/query-client-setup.md`

→ Proceed to Step 3

#### Output

- All relevant references loaded

---

### Step 3: Design the file structure

#### Condition

- Step 2 complete

#### Process

Based on the loaded references and the user's request:

1. Determine the complete list of files to create
2. For each file, record:
   - Full path (following `feature-folder.md` and `route-groups.md`)
   - Role / responsibility
   - Key conventions from the matching reference
3. Build the directory tree

Standard paths to follow:

| File type | Path pattern |
|---|---|
| List page | `app/(authenticated)/{feature}/page.tsx` |
| View page | `app/(authenticated)/{feature}/[id]/page.tsx` |
| Create page | `app/(authenticated)/{feature}/new/page.tsx` |
| Edit page | `app/(authenticated)/{feature}/[id]/edit/page.tsx` |
| List screen | `app/(authenticated)/{feature}/{Feature}ListScreen.tsx` |
| View screen | `app/(authenticated)/{feature}/{Feature}ViewScreen.tsx` |
| Create screen | `app/(authenticated)/{feature}/{Feature}NewScreen.tsx` |
| Edit screen | `app/(authenticated)/{feature}/{Feature}EditScreen.tsx` |
| Form schema | `app/(authenticated)/{feature}/form.ts` |
| Server actions | `app/(authenticated)/{feature}/actions.ts` |
| API route | `app/api/v1/{resource}/route.ts` |
| API client | `app/api/v1/{resource}/client.ts` |
| Service | `app/api/v1/{resource}/service.ts` |
| DB mutations | `app/api/v1/{resource}/db.ts` |
| DB queries | `app/api/v1/{resource}/query.ts` |
| DB helper | `app/api/v1/{resource}/dbHelper.ts` |
| DB schema | `drizzle/schema.ts` (extend existing) |

→ Proceed to Step 4

#### Output

- Complete file list with paths, roles, and conventions noted

---

### Step 4: Output the plan

#### Condition

- Step 3 complete

#### Process

Output the following structured planning document in Markdown:

```markdown
# 実装計画: {what to build}

**Type**: {new-project | new-feature | new-api | new-screens}
**Created**: {YYYY-MM-DD}
**Resource**: `{resource-name}`
**Operations**: {list of required operations}

## ディレクトリツリー

\`\`\`
{directory tree using ├── / └── / │}
\`\`\`

## ファイル一覧

| ファイル | 役割 | 参照 reference |
|---|---|---|
| {path} | {role} | `{reference file}` |
...

## 各ファイルの実装ポイント

### `{file1}`

- **役割**: {one-line role}
- **規約ポイント**:
  - {key convention from reference}
  - ...

### `{file2}`
...

## 実装順序（推奨）

1. DB スキーマ (`drizzle/schema.ts`) — 先にデータ構造を確定
2. API 層 (query → db → dbHelper → service → route → client)
3. Server Actions (`actions.ts`) — フロント↔バック橋渡し
4. 画面 (page.tsx → Screen → form.ts) — 上位から下位へ

## 次のステップ

- この計画を確認後、`/dev-kit:next-implement` で実装を開始
- 各ファイル編集時に next-references-injection フックが自動で reference を注入
```

→ Done

#### Output

- Structured planning document output to the conversation

#### Notes

##### Prohibitions

- Do NOT create or edit any source files in this skill — planning only
- Do NOT call `/dev-kit:next-implement` automatically — the user reviews the plan first

---

## References

- `references/CLAUDE.md` — full index of all references and the injection hook
- `references/injection_rules.yaml` — file-path pattern → reference mapping
- `references/frontend/feature-folder.md` — feature folder layout and naming
- `references/frontend/route-groups.md` — `(authenticated)` / `(auth)` / `(shared)` route groups
- `references/frontend/app-folder-overview.md` — overall app directory structure
