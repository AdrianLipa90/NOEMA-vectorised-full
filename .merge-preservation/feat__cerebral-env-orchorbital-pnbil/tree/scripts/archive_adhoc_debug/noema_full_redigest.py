#!/usr/bin/env python3
"""One-off: full redigest of the 16815-document Knowledge DB into the
production PhaseMemory, through the encoder fixed earlier tonight
(circular-mean bugfix). Backup already taken. Additive (dedup by text
hash protects existing 215 conversational entries)."""
import os
import sys
import time

sys.path.insert(0, "/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/src")


def main():
    from ciel_geometry.cielingo_phase_memory import PhaseMemory
    from ciel_geometry.cielingo_inference import MEMORY_PATH
    from ciel_geometry.cielingo_train import train_from_knowledge_db

    memory = PhaseMemory.load_or_create(MEMORY_PATH, max_size=30000)
    print(f"loaded production memory: {memory.size} entries before redigest")

    db_path = "/media/adrian/New Volume/CIEL_memories/state/noema_knowledge.db"
    t0 = time.time()
    stats = train_from_knowledge_db(memory, db_path, max_docs=0, enriched=True)
    elapsed = time.time() - t0

    print(f"\nredigest stats: {stats}")
    print(f"total elapsed: {elapsed:.1f}s")
    print(f"memory size after: {memory.size}")

    memory.save(MEMORY_PATH)
    print(f"saved to {MEMORY_PATH}")

    os.remove(os.path.abspath(__file__))
    return


if __name__ == "__main__":
    main()
