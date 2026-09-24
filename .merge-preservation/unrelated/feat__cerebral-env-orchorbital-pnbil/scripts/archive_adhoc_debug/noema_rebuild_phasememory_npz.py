#!/usr/bin/env python3
"""One-off: rebuild the corrupted cielingo_phase_memory.npz (Bad CRC-32,
same torn-write race that hit the .json) by re-encoding the recovered texts
from the now-repaired .json — phi is a deterministic function of text, so
this reconstructs vectors identically to what a clean save would have
produced. Weights are re-derived the same way (fast_encode_text_weighted)."""
import os
import shutil
import sys

sys.path.insert(0, "/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/src")


def main():
    import json
    import numpy as np
    from ciel_geometry.cielingo_phase_encoder import fast_encode_text_weighted

    json_path = "/media/adrian/New Volume/CIEL_memories/state/cielingo_phase_memory.json"
    npz_path = "/media/adrian/New Volume/CIEL_memories/state/cielingo_phase_memory.npz"
    backup_path = npz_path + ".corrupt_backup_20260711"

    if os.path.exists(npz_path):
        shutil.copy2(npz_path, backup_path)
        print(f"backup written: {backup_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    texts = data["texts"]
    print(f"re-encoding {len(texts)} texts...")

    vectors = np.zeros((len(texts), 36), dtype=np.float64)
    weights = np.zeros((len(texts), 36), dtype=np.float64)
    for i, t in enumerate(texts):
        phi, w = fast_encode_text_weighted(t)
        vectors[i] = phi
        weights[i] = w

    np.savez_compressed(npz_path, vectors=vectors, weights=weights)
    print(f"rebuilt {npz_path}: {os.path.getsize(npz_path)} bytes")

    # Verify: reload through PhaseMemory itself
    from ciel_geometry.cielingo_phase_memory import PhaseMemory
    pm = PhaseMemory.load_or_create("/media/adrian/New Volume/CIEL_memories/state/cielingo_phase_memory")
    print(f"PhaseMemory reloads cleanly: {len(pm.texts)} texts, vectors shape {pm.vectors.shape}, weights shape {pm.weights.shape}")

    os.remove(os.path.abspath(__file__))
    return


if __name__ == "__main__":
    main()
