#!/usr/bin/env python3
"""One-off, READ-ONLY: check ~/Pulpit/CIEL_memories/ (the append-only
memory tier named in IMMUTABLE_CONTRACT.md) vs the two other candidates
(~/CIEL_memories, ~/ciel_memories) and the production path used tonight
(/media/adrian/New Volume/CIEL_memories/)."""
import os


def main():
    candidates = [
        os.path.expanduser("~/Pulpit/CIEL_memories"),
        os.path.expanduser("~/CIEL_memories"),
        os.path.expanduser("~/ciel_memories"),
        "/media/adrian/New Volume/CIEL_memories",
    ]
    for c in candidates:
        exists = os.path.exists(c)
        is_link = os.path.islink(c)
        real = os.path.realpath(c) if exists else None
        print(f"{c}: exists={exists} is_symlink={is_link} realpath={real}")
        if exists and os.path.isdir(c):
            try:
                entries = sorted(os.listdir(c))
                print(f"  entries: {entries}")
            except PermissionError:
                print("  (permission denied)")

    os.remove(os.path.abspath(__file__))
    return


if __name__ == "__main__":
    main()
