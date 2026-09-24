#!/usr/bin/env python3
"""NOEMA Word Canonize Cycle — one autonomous batch of the source-lookup-
queue resolver + canonizer, run periodically by noema-word-canonize.timer.

Origin (2026-07-11): Adrian, direct — "cielingo ma samodzielnie
kanonizowac! na huj ty tam?!" (CIELingo should canonize AUTONOMOUSLY, why
are you doing it manually). Tracks its own resume offset in a state file
so each timer firing picks up where the last one left off, processing the
644-word source_lookup_queue.jsonl in batches of 20 without any manual
invocation.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

import json
import sys
from pathlib import Path

sys.path.insert(0, "/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/src")

BATCH_SIZE = 20
STATE_PATH = Path("/media/adrian/New Volume/CIEL_memories/state/word_canonize_cycle_offset.json")


def _load_offset() -> int:
    if not STATE_PATH.exists():
        return 0
    try:
        return int(json.loads(STATE_PATH.read_text(encoding="utf-8")).get("offset", 0))
    except (json.JSONDecodeError, ValueError, OSError) as e:
        from ciel_geometry.phasenav_exception_bridge import phase_signal_exception
        phase_signal_exception("noema_word_canonize_cycle._load_offset", e, operator_id="PAUSE")
        return 0


def _save_offset(offset: int) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps({"offset": offset}), encoding="utf-8")


def main() -> int:
    root = Path("/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA")
    from cielingo.unknown_word_audit import resolve_source_lookup_queue, canonize_resolved_words, read_jsonl

    queue_path = root / "data/cielingo/unknown_word_audit/source_lookup_queue.jsonl"
    resolved_path = root / "data/cielingo/unknown_word_audit/resolved_lookups.jsonl"
    cards_dir = root / "cards/words"

    total = len(read_jsonl(queue_path))
    offset = _load_offset()
    if offset >= total:
        print(f"queue fully processed ({total}/{total}) — nothing to do this cycle")
        return 0

    resolve_stats = resolve_source_lookup_queue(queue_path, output_path=resolved_path, offset=offset, limit=BATCH_SIZE)
    print(f"offset={offset}  resolve stats: {resolve_stats}")

    all_resolved = read_jsonl(resolved_path)
    this_batch = all_resolved[offset:offset + BATCH_SIZE] if len(all_resolved) >= offset + BATCH_SIZE else all_resolved[-BATCH_SIZE:]
    tmp_path = root / "data/cielingo/unknown_word_audit/_tmp_cycle_batch.jsonl"
    with tmp_path.open("w", encoding="utf-8") as f:
        for r in this_batch:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    canonize_stats = canonize_resolved_words(tmp_path, cards_dir)
    tmp_path.unlink()
    print(f"canonize stats: n_canonized={canonize_stats['n_canonized']}")

    new_offset = offset + resolve_stats["queue_size_processed"]
    _save_offset(new_offset)
    print(f"progress: {new_offset}/{total}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
