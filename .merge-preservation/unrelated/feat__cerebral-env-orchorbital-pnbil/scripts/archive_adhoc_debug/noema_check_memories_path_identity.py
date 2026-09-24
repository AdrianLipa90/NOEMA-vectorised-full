#!/usr/bin/env python3
"""One-off, READ-ONLY: check whether ~/Pulpit/CIEL_memories/ (the
append-only memory tier named in IMMUTABLE_CONTRACT.md Section V) is the
same location, via symlink or otherwise, as /media/adrian/New Volume1/
CIEL_memories/ (where cielingo_phase_memory.json/.npz, repaired tonight,
actually live)."""
import os


def main():
    candidates = [
        os.path.expanduser("~/Pulpit/CIEL_memories"),
        os.path.expanduser("~/Pulpit"),
        "/media/adrian/New Volume/CIEL_memories",
    ]
    for c in candidates:
        exists = os.path.exists(c)
        is_link = os.path.islink(c)
        real = os.path.realpath(c) if exists else None
        print(f"{c}: exists={exists} is_symlink={is_link} realpath={real}")

    # Does the state/ subfolder (where cielingo_phase_memory.* lives)
    # appear under BOTH paths, or only one?
    for base in candidates:
        state = os.path.join(base, "state")
        if os.path.exists(state):
            has_pm = os.path.exists(os.path.join(state, "cielingo_phase_memory.json"))
            print(f"{state}: exists, cielingo_phase_memory.json present={has_pm}")

    os.remove(os.path.abspath(__file__))
    return


if __name__ == "__main__":
    main()
