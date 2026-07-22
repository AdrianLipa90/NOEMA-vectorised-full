#!/usr/bin/env python3
"""Resolve + canonize one chunk of the source_lookup_queue, given an
offset/limit via argv. Kept as a permanent, reusable utility (not
self-deleting) since more batches will follow across multiple tool calls.

Usage: noema_resolve_canonize_chunk.py <offset> <limit>
"""
import sys
from pathlib import Path

sys.path.insert(0, "/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/src")


def main():
    offset = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 50

    root = Path("/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA")
    from cielingo.unknown_word_audit import resolve_source_lookup_queue, canonize_resolved_words

    queue_path = root / "data/cielingo/unknown_word_audit/source_lookup_queue.jsonl"
    resolved_path = root / "data/cielingo/unknown_word_audit/resolved_lookups.jsonl"
    cards_dir = root / "cards/words"

    resolve_stats = resolve_source_lookup_queue(queue_path, output_path=resolved_path, offset=offset, limit=limit)
    print(f"offset={offset} limit={limit}  resolve stats: {resolve_stats}")

    # Only canonize the NEW slice just resolved (re-slice resolved file to
    # the same offset/limit window to avoid re-canonizing earlier batches
    # into duplicate WORD- cards each run).
    import json
    all_resolved = [json.loads(l) for l in resolved_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    this_batch = all_resolved[offset:offset + limit] if len(all_resolved) >= offset + limit else all_resolved[-limit:]

    tmp_path = root / "data/cielingo/unknown_word_audit/_tmp_batch.jsonl"
    with tmp_path.open("w", encoding="utf-8") as f:
        for r in this_batch:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    canonize_stats = canonize_resolved_words(tmp_path, cards_dir)
    print(f"canonize stats: n_canonized={canonize_stats['n_canonized']}")
    tmp_path.unlink()

    return


if __name__ == "__main__":
    main()
