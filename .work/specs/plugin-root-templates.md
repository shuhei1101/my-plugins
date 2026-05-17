# Spec: plugin-root-templates

## 背景

`work-start` スキルの Step 5 / Step 6 がテンプレートファイルを
`.work/tasks/yyyymmdd_xxx/PRXXX/TODO.md` などの存在しないパスで参照しており、
Claude が毎回 Read に失敗してからファイルを作成している。

## 方針

プラグインが持つテンプレートファイルを `${CLAUDE_PLUGIN_ROOT}/templates/` 配下に置き、
スキルからは `${CLAUDE_PLUGIN_ROOT}/templates/TODO.md` のように参照する。

## テンプレートファイル一覧

| ファイル | 用途 |
|---------|------|
| `templates/TODO.md` | PR TODO ドキュメントのひな形 |
| `templates/QA.md` | PR QA ドキュメントのひな形 |
| `templates/spec.md` | スペックドキュメントのひな形 |

## SKILL.md の変更箇所

### Step 5（変更前）
```
Create `TODO.md` using the template at `.work/tasks/yyyymmdd_xxx/PRXXX/TODO.md`
Create `QA.md` using the template at `.work/tasks/yyyymmdd_xxx/PRXXX/QA.md`
```

### Step 5（変更後）
```
Create `TODO.md` using the template at `${CLAUDE_PLUGIN_ROOT}/templates/TODO.md`
Create `QA.md` using the template at `${CLAUDE_PLUGIN_ROOT}/templates/QA.md`
```

### Step 6（変更前）
```
create a new spec using the template at `.work/specs/xxx.md`
```

### Step 6（変更後）
```
create a new spec using the template at `${CLAUDE_PLUGIN_ROOT}/templates/spec.md`
```
