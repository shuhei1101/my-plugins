# Common helpers for dev-kit hook scripts.
#
# Kept intentionally per-plugin (not shared across plugins) per the
# `premature-cross-plugin-centralization` incident: env prefixes and log tags
# differ per plugin, so cross-plugin abstraction costs more than it saves.

from __future__ import annotations

import json
import os
import pathlib
import sys
import tempfile

ENV_PREFIX = "DEV_KIT"

FALSY = {"false", "0", "no", "off"}
TRUTHY = {"true", "1", "yes", "on"}


def read_hook_input() -> dict:
    """Read the hook input JSON from stdin."""
    return json.loads(sys.stdin.read())


def env_truthy(name: str, default: bool = True) -> bool:
    """Return whether the env var is truthy.

    Default is opt-out: anything except falsy values is treated truthy when
    default=True; the opposite when default=False.
    """
    raw = os.environ.get(name)
    if raw is None:
        return default
    val = raw.strip().lower()
    if default:
        return val not in FALSY
    return val in TRUTHY


def exit_if_stop_loop(input_data: dict) -> None:
    """Exit silently when the Stop hook is being re-fired (stop_hook_active)."""
    if input_data.get("stop_hook_active"):
        sys.exit(0)


def already_dispatched_this_session(tag: str, session_id: str) -> bool:
    """Once-per-session guard via a flag file in tempdir.

    Returns True if the flag already exists; otherwise creates the flag and
    returns False. Caller decides whether to early-exit or proceed.
    """
    flag = pathlib.Path(tempfile.gettempdir()) / f"{tag}-{session_id}"
    if flag.exists():
        return True
    flag.touch()
    return False


def emit_block_reason(prompt_path: pathlib.Path) -> None:
    """Emit `{decision: block, reason: <prompt body>}` JSON to stdout."""
    if not prompt_path.exists():
        return
    body = prompt_path.read_text("utf-8")
    payload = {"decision": "block", "reason": body}
    sys.stdout.buffer.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))
