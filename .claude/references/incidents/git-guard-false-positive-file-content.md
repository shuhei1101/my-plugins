# git-guard Hook False Positive from Command String Text

**Date**: 2026-05-30
**Category**: tool-misuse

## What Happened

The git-guard hook (`PreToolUse(Bash)`) fires on the entire Bash command string. Any occurrence of "git push" or "git merge" — even as literal text in arguments, file content, or summaries — triggers the guard.

**Case A — Shell heredoc** (2026-05-30):
```bash
cat > plugins/work/.claude-plugin/plugin.json << 'EOF'
{
  "description": "...guards git push/merge confirmation..."
}
EOF
```
The file body is part of the command string, so the literal phrase "git merge" blocked the write.

**Case B — Python command arguments** (2026-05-30):
```bash
python index-tool.py add ... --summary "git merge master/main は許可..."
python -c "..." "git-guardフックを修正し、git merge master/mainは許可..." "session-id"
```
The `--summary` or positional argument value containing "git merge" as text triggers the guard, even though the command itself is not a git operation.

## How to Avoid

1. **Rephrase**: avoid the literal strings "git push" / "git merge" in arguments and file content (e.g., "マージ", "ギットマージ", "force-operations").
2. **Python file write**: use Python's file API instead of a heredoc when writing files that contain these phrases.
3. **WORK_GUARD=false**: temporarily disable the guard via the env var when the false positive cannot be avoided.

## Context

The git-guard hook regex (`r"\bgit\s+(push|merge)\b"`) scans the full Bash command string, including all arguments and embedded content. It cannot distinguish between "git merge" as a command and as text being discussed.
