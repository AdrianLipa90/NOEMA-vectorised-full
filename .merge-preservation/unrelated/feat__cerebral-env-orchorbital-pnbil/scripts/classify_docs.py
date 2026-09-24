#!/usr/bin/env python3
"""Interactive document classifier — k = keep, d = duplicate, q = quit."""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

import json, sys, tty, termios, select, os, signal
from pathlib import Path
import numpy as np

if __name__ == "__main__":
    META_PATH = Path("/media/adrian/New Volume/NOEMA_PHASE_DATA/PHASE_INDEX/library_meta.npy")
    VEC_PATH = Path("/media/adrian/New Volume/NOEMA_PHASE_DATA/PHASE_INDEX/library_index.npy")
    STATE_PATH = Path("/tmp/noema_doc_classify.json")

    meta = list(np.load(str(META_PATH), allow_pickle=True))
    vec = np.load(str(VEC_PATH))

    adrian_idx = [i for i, m in enumerate(meta) if len(m) > 3 and m[3] == "Adrian Lipa"]

    state = {"keep": [], "duplicate": []}
    if STATE_PATH.exists():
        try:
            state = json.loads(STATE_PATH.read_text())
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/classify_docs.py:21 quiet except scope=<module> reason=pass")
            raise
            pass

    keep_set = set(state["keep"])
    dup_set = set(state["duplicate"])

def save_state():
    state["keep"] = sorted(keep_set)
    state["duplicate"] = sorted(dup_set)
    STATE_PATH.write_text(json.dumps(state, indent=2))

def getch():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch

print("=== NOEMA Document Classifier ===")
print(f"Total: {len(adrian_idx)} documents")
print(f"Already classified: keep={len(keep_set)}, dup={len(dup_set)}")
print()
print("Keys:  k = KEEP  |  d = DUPLICATE  |  q = QUIT (save progress)")
print("       u = UNDO last  |  s = STATUS")
print()

done = False
for pos, idx in enumerate(adrian_idx):
    if idx in keep_set or idx in dup_set:
        continue
    m = meta[idx]
    fn = str(m[1])
    topic = str(m[2])
    path = str(m[6])

    os.system("clear" if os.name == "posix" else "cls")
    print(f"[{pos+1}/{len(adrian_idx)}]  keep={len(keep_set)}  dup={len(dup_set)}")
    print(f"  Plik: {fn}")
    if topic not in ("unknown", "Adrian Lipa", "Adrian Lipa (by filename)"):
        print(f"  Topic: {topic}  <<< UWAGA")
    if not path.strip():
        print(f"  Sciezka: (brak)  <<< UWAGA")
    elif "/Adrian Lipa/" not in path:
        print(f"  Katalog: {path.split('/')[-2]}  <<< UWAGA")
    print()

    while True:
        ch = getch().lower()
        if ch == "k":
            keep_set.add(idx)
            break
        elif ch == "d":
            dup_set.add(idx)
            break
        elif ch == "q":
            done = True
            break
        elif ch == "u":
            if keep_set: keep_set.pop()
            elif dup_set: dup_set.pop()
            print("Cofnieto ostatni")
        elif ch == "s":
            print(f"Status: keep={len(keep_set)} dup={len(dup_set)}")

    if done:
        break
    if (pos + 1) % 50 == 0:
        save_state()
        print("Auto-zapis...")

save_state()
print(f"\nZakonczono. keep={len(keep_set)} dup={len(dup_set)}")

keep_arr = np.array(sorted(keep_set))
dup_arr = np.array(sorted(dup_set))

DST = "/media/adrian/New Volume/NOEMA_PHASE_DATA/PHASE_INDEX"
np.save(f"{DST}/library_index_adrian_keep.npy", vec[keep_arr])
np.save(f"{DST}/library_meta_adrian_keep.npy", np.array([meta[i] for i in sorted(keep_set)], dtype=object))
np.save(f"{DST}/library_index_adrian_dup.npy", vec[dup_arr])
np.save(f"{DST}/library_meta_adrian_dup.npy", np.array([meta[i] for i in sorted(dup_set)], dtype=object))
print(f"Zapisano: {DST}/library_index_adrian_keep.npy ({len(keep_set)} dok.)")
print(f"          {DST}/library_index_adrian_dup.npy ({len(dup_set)} dok.)")
