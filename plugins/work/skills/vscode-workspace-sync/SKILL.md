---
name: vscode-workspace-sync
description: |
  Set up PostToolUse hooks that keep a VS Code .code-workspace file in sync with git worktrees.
  When run, finds the workspace file, confirms it with the user, then writes two hooks to
  .claude/settings.json: one adds a worktree path to `folders` on `git worktree add`,
  the other removes it on `git worktree remove`.
  Trigger when the user says "ワークスペース同期を設定して", "VS Codeのワークツリーを自動追加したい",
  "worktreeをワークスペースに自動登録したい", or invokes explicitly as `/work:vscode-workspace-sync`.
---

# work:vscode-workspace-sync — VS Code Workspace ↔ Worktree Sync

Writes two `PostToolUse` hooks to `.claude/settings.json` so VS Code's `.code-workspace` file
stays in sync whenever Claude Code creates or removes a git worktree.

---

## Tasks

### Step 1: Find the `.code-workspace` file

#### Condition

- Always — run first

#### Process

1. Search for `*.code-workspace` files in:
   - The current project directory (`${CLAUDE_PROJECT_DIR}`)
   - One level up (`..`)
2. If **one file found** → proceed with it
3. If **multiple files found** → present the list and ask the user to choose
4. If **none found** → show the message below, ask the user to enter the absolute path manually, then proceed with that path:

   > `.code-workspace` ファイルが見つかりませんでした。絶対パスを入力してください。

→ Proceed to Step 2

#### Output

- Absolute path to the `.code-workspace` file confirmed (stored as `WORK_PATH`)

---

### Step 2: Confirm with the user

#### Condition

- Step 1 complete

#### Process

1. Show the resolved path and ask for confirmation:

   > 使用するワークスペースファイル: `{WORK_PATH}`  
   > このファイルにフックを設定しますか？

2. Wait for user confirmation before proceeding

→ Proceed to Step 3

#### Output

- `WORK_PATH` confirmed

---

### Step 3: Write hooks to `.claude/settings.json`

#### Condition

- Step 2 complete

#### Process

1. Read `${CLAUDE_PROJECT_DIR}/.claude/settings.json`; start from `{}` if it does not exist
2. Merge the two hook entries below into the `hooks.PostToolUse` array,
   appending to any existing `matcher: "Bash"` entry (do not duplicate entries)
3. Substitute `WORK_PATH` with the confirmed absolute path from Step 1
4. Write the result back to `.claude/settings.json`

**Hook 1 — worktree add → add path to workspace folders:**

```json
{
  "matcher": "Bash",
  "hooks": [
    {
      "type": "command",
      "command": "python",
      "args": [
        "-c",
        "import sys,json,re,pathlib; d=json.loads(sys.stdin.read()); cmd=d.get('tool_input',{}).get('command',''); sys.exit(0) if 'git worktree add' not in cmd else None; m=re.search(r'git\\s+worktree\\s+add\\s+(?:-b\\s+\\S+\\s+)?(\\S+)',cmd); sys.exit(0) if not m else None; p=pathlib.Path(r'WORK_PATH'); sys.exit(0) if not p.exists() else None; data=json.loads(p.read_text('utf-8')); folders=data.get('folders',[]); wt=m.group(1); folders.append({'path':wt}) if not any(f.get('path')==wt for f in folders) else None; data['folders']=folders; p.write_text(json.dumps(data,indent=2,ensure_ascii=False),'utf-8')"
      ]
    }
  ]
}
```

**Hook 2 — worktree remove → remove path from workspace folders:**

```json
{
  "matcher": "Bash",
  "hooks": [
    {
      "type": "command",
      "command": "python",
      "args": [
        "-c",
        "import sys,json,re,pathlib; d=json.loads(sys.stdin.read()); cmd=d.get('tool_input',{}).get('command',''); sys.exit(0) if 'git worktree remove' not in cmd else None; m=re.search(r'git\\s+worktree\\s+remove\\s+(?:--force\\s+)?(\\S+)',cmd); sys.exit(0) if not m else None; p=pathlib.Path(r'WORK_PATH'); sys.exit(0) if not p.exists() else None; data=json.loads(p.read_text('utf-8')); data['folders']=[f for f in data.get('folders',[]) if f.get('path')!=m.group(1)]; p.write_text(json.dumps(data,indent=2,ensure_ascii=False),'utf-8')"
      ]
    }
  ]
}
```

#### Notes

- Each hook entry is a **separate** object in the `PostToolUse` array — do not merge the two `matcher: "Bash"` blocks into one
- If `.claude/` directory does not exist, create it first
- `WORK_PATH` must be an absolute path (forward slashes or escaped backslashes both work on Windows)

→ Proceed to Step 4

#### Output

- `.claude/settings.json` updated with both hook entries

---

### Step 4: Report to the user

#### Condition

- Step 3 complete

#### Process

1. List created/updated files
2. Show the verification steps:

   > **確認方法**:  
   > 1. Claude Code を再起動してフックを読み込む  
   > 2. `git worktree add` を実行 → `.code-workspace` の `folders` にパスが追加されることを確認  
   > 3. `git worktree remove` を実行 → `folders` からパスが削除されることを確認

#### Notes

##### Checklist

- [ ] `.claude/settings.json` に `PostToolUse` フックが2件追加されている
- [ ] 両フックの `WORK_PATH` が実際のファイルパスに置換されている
