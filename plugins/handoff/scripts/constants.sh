#!/usr/bin/env bash
set -euo pipefail

echo "export HANDOFF_DIR=$HOME/.claude/handoff" >> "$CLAUDE_ENV_FILE"
