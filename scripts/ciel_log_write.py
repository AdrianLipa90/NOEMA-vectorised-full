#!/usr/bin/env python3
"""
ciel_log_write.py — One-shot writer to auto-log FIFO.

Wołane z odpowiedzi opencode:
    python3 scripts/ciel_log_write.py --role assistant --content "..." --tags "tagi"

Non-blocking: jeśli FIFO nie istnieje lub daemon nie słucha — cicho pomija.
"""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import sys
import os
import pathlib
from datetime import datetime, timezone

FIFO_PATH = pathlib.Path("/dev/shm/ciel_noema/auto_log.fifo")


def write(role: str, content: str, tags: str = ""):
    if not content:
        return

    row = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "role": role,
        "content": content,
        "tags": tags,
    }

    try:
        if FIFO_PATH.exists():
            with open(FIFO_PATH, "w", encoding="utf-8") as fifo:
                fifo.write(json.dumps(row, ensure_ascii=False) + "\n")
    except (FileNotFoundError, BrokenPipeError, OSError):
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_log_write.py:35 quiet except scope=write reason=pass")
        pass  # daemon not running — silent skip


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Write one log entry to auto-log FIFO")
    parser.add_argument("--role", required=True, choices=["user", "assistant", "system"])
    parser.add_argument("--content", required=True, help="Log content")
    parser.add_argument("--tags", default="", help="Optional comma-separated tags")
    args = parser.parse_args()

    write(args.role, args.content, args.tags)


if __name__ == "__main__":
    main()
