#!/usr/bin/env python3
"""One-off: repair the torn-write corruption in cielingo_phase_memory.json —
two concurrent PhaseMemory.save() calls (from different daemons sharing the
same file, no lock) interleaved their output. The file contains one
complete, valid JSON document followed by garbage from a second, truncated
write. Recover by parsing with raw_decode (stops at the first complete
object) and rewriting the file cleanly. Makes a .bak copy first."""
import json
import os
import shutil


def main():
    json_path = "/media/adrian/New Volume/CIEL_memories/state/cielingo_phase_memory.json"
    backup_path = json_path + ".corrupt_backup_20260711"

    shutil.copy2(json_path, backup_path)
    print(f"backup written: {backup_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        content = f.read()

    decoder = json.JSONDecoder()
    data, end_idx = decoder.raw_decode(content)
    print(f"recovered valid document: n_entries={data.get('n_entries')} len(texts)={len(data.get('texts', []))}")
    print(f"valid document spans chars [0:{end_idx}] of {len(content)} total (discarding {len(content) - end_idx} bytes of garbage)")

    # Sanity: texts/metadata/vectors-implied-count must be internally consistent
    assert len(data["texts"]) == len(data.get("metadata", [])), "texts/metadata length mismatch — refusing to write"

    npz_path = "/media/adrian/New Volume/CIEL_memories/state/cielingo_phase_memory.npz"
    import numpy as np
    npz = np.load(npz_path)
    n_vectors = npz["vectors"].shape[0]
    print(f"npz vectors: {n_vectors} rows (weights: {npz['weights'].shape[0] if 'weights' in npz.files else 'N/A'})")
    if n_vectors != len(data["texts"]):
        print(f"MISMATCH: npz has {n_vectors} vectors but recovered json has {len(data['texts'])} texts — refusing to write, investigate further")
        os.remove(os.path.abspath(__file__))
        return

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Re-verify
    with open(json_path, "r", encoding="utf-8") as f:
        reloaded = json.load(f)
    print(f"re-verified clean file: n_entries={reloaded.get('n_entries')} len(texts)={len(reloaded['texts'])}")

    os.remove(os.path.abspath(__file__))
    return


if __name__ == "__main__":
    main()
