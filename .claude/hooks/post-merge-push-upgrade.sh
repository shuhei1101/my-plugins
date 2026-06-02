#!/bin/bash
# PostToolUse(Bash) フックから呼び出される
# master への git merge 完了後に push + marketplace upgrade を実行する

data=$(cat)
cmd=$(printf '%s' "$data" | python3 -c 'import sys,json; print(json.load(sys.stdin).get("tool_input",{}).get("command",""))')

if echo "$cmd" | grep -qE 'git[[:space:]]+merge'; then
  branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
  if [ "$branch" = "master" ]; then
    git push && python tools/marketplace.py upgrade
  fi
fi
