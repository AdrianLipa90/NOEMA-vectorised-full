#!/usr/bin/env python3
"""NOEMA Audit Consolidator — merge 3 audit systems into state_db.m8_audit.

Reads:
  1. MemoryLog JSONL (CIEL_OMEGA/memory/memory_log.jsonl)
  2. M8 AuditJournalMemory (in-memory snapshot via CIEL pipeline)
  3. state_db.m8_audit (SQLite, canonical target)

Writes:
  - Consolidated to state_db.m8_audit with dedup by timestamp+event
  - Summary to stdout

Usage:
  python3 noema_audit_consolidator.py [--dry-run]
"""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import argparse
import json
import logging
import os
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("audit_consolidator")

# ── source discovery ──────────────────────────────────────────────────────
_SCRIPT_DIR = Path(__file__).resolve().parent
_NOEMA_DEFAULT = os.path.join(os.sep, "media", "adrian", "New Volume1", "NOEMA_LIBRARY")
NOEMA_LIBRARY = Path(os.environ.get("NOEMA_LIBRARY", _NOEMA_DEFAULT))
BASE = NOEMA_LIBRARY
STATE_DB = BASE / "agent_db" / "agent_state.db"
MEMORY_LOG = BASE.parent / "CIEL_OMEGA_COMPLETE_SYSTEM" / "ciel_omega" / "memory" / "memory_log.jsonl"

_CIEL_OMEGA_DEFAULT = str(_SCRIPT_DIR.parent.parent / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM" / "ciel_omega")
CIEL_OMEGA = Path(os.environ.get("CIEL_OMEGA_ROOT", _CIEL_OMEGA_DEFAULT))
MEMORY_LOG_ALT = CIEL_OMEGA / "memory" / "memory_log.jsonl"


def _read_jsonl(path):
    if not path.exists():
        return []
    records = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if line:
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_audit_consolidator.py:50 quiet except scope=_read_jsonl reason=pass")
                pass
    return records


def _ensure_schema(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS m8_audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            event TEXT NOT NULL,
            source TEXT NOT NULL,
            details TEXT,
            severity TEXT DEFAULT 'info',
            created_at TEXT DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_m8_ts ON m8_audit(timestamp);
    """)


def _scan_cielingo_cards() -> list[tuple[str, str, str, str, str]]:
    """Scan CIELingo writing cards JSONL for audit events.

    Bridges the gap between CIELingo runtime cards and persistent audit DB.
    Cards contain phase-encoded semantic state at each write event.

    Returns:
        list of (timestamp, event, source, details_json, severity)
    """
    cards_path = Path("/tmp/noema_cielingo_cards.jsonl")
    entries = _read_jsonl(cards_path)
    results = []
    for card in entries:
        ts = card.get("timestamp", card.get("created_at", ""))
        event = f"cielingo_card:{card.get('card_type', 'unknown')}"
        phase_info = {
            "oscillator_group": card.get("oscillator_group", ""),
            "phase_hot": card.get("phase_hot", None),
            "tick": card.get("tick", 0),
        }
        details = json.dumps(phase_info, default=str)
        results.append((ts, event, "cielingo_cards", details, "info"))
    return results


def _scan_writings_log() -> list[tuple[str, str, str, str, str]]:
    """Scan NOEMA writings JSONL for audit events.

    Writings log contains records of every file creation/modification
    in the NOEMA system, tagged with PhaseNav phase vectors.

    Returns:
        list of (timestamp, event, source, details_json, severity)
    """
    writings_path = Path("/tmp/noema_writings.jsonl")
    entries = _read_jsonl(writings_path)
    results = []
    for entry in entries:
        ts = entry.get("timestamp", entry.get("created_at", ""))
        event = f"writing:{entry.get('action', 'create')}:{entry.get('file_type', 'unknown')}"
        phase_info = {
            "card_path": entry.get("noema_card_path", ""),
            "phase_phi": entry.get("phase_phi", None),
            "cielingo_card": entry.get("cielingo_card_path", ""),
        }
        details = json.dumps(phase_info, default=str)
        results.append((ts, event, "writings_log", details, "info"))
    return results


def consolidate(
    dry_run: bool = False,
    *,
    scan_cielingo: bool = True,
    scan_writings: bool = True,
) -> dict[str, Any]:
    sources: dict[str, list] = {}

    # ── Source 1: MemoryLog JSONL ──
    ml_path = MEMORY_LOG if MEMORY_LOG.exists() else MEMORY_LOG_ALT
    ml_records = _read_jsonl(ml_path)
    sources["memory_log"] = ml_records
    log.info("MemoryLog: %d records from %s", len(ml_records), ml_path)

    # ── Source 2: CIELingo cards JSONL ──
    if scan_cielingo:
        cielingo_entries = _scan_cielingo_cards()
        sources["cielingo_cards"] = cielingo_entries
        log.info("CIELingo cards: %d records from /tmp/noema_cielingo_cards.jsonl", len(cielingo_entries))
    else:
        cielingo_entries = []

    # ── Source 3: Writings log JSONL (PhaseNav phase flux) ──
    if scan_writings:
        writings_entries = _scan_writings_log()
        sources["writings_log"] = writings_entries
        log.info("Writings log: %d records from /tmp/noema_writings.jsonl", len(writings_entries))
    else:
        writings_entries = []

    # ── Source 4: state_db.m8_audit (existing canonical for dedup) ──
    conn = sqlite3.connect(str(STATE_DB))
    _ensure_schema(conn)
    existing = conn.execute("SELECT timestamp, event, source FROM m8_audit").fetchall()
    existing_set = {(r[0], r[1], r[2]) for r in existing}
    log.info("state_db.m8_audit: %d existing rows", len(existing))

    # Dedup by (timestamp, event, source)
    new_entries = []

    # From MemoryLog
    for r in ml_records:
        ts = r.get("timestamp", r.get("time", r.get("created_at", "")))
        event = r.get("event", r.get("action", r.get("type", "unknown")))
        src = "memory_log"
        key = (ts, event, src)
        if key not in existing_set:
            details = {k: v for k, v in r.items() if k not in ("timestamp", "time", "created_at", "event", "action", "type")}
            new_entries.append((ts, event, src, json.dumps(details, default=str), r.get("severity", "info")))
            existing_set.add(key)

    # From CIELingo cards (PhaseNav phase flux)
    for ts, event, src, details, severity in cielingo_entries:
        key = (ts, event, src)
        if key not in existing_set:
            new_entries.append((ts, event, src, details, severity))
            existing_set.add(key)

    # From Writings log
    for ts, event, src, details, severity in writings_entries:
        key = (ts, event, src)
        if key not in existing_set:
            new_entries.append((ts, event, src, details, severity))
            existing_set.add(key)

    # Source 5: M8 in-memory audit journal snapshot is now partially bridged
    # by CIELingo cards + Writings log above. Full M8 runtime snapshot
    # still requires CIEL pipeline to call snapshot_m8_to_state_db() periodically.
    # This is tracked as GAP-M8 and flagged in summary.

    log.info("New entries total: %d (memory_log=%d, cielingo=%d, writings=%d)",
             len(new_entries),
             len([e for e in new_entries if e[2] == "memory_log"]),
             len([e for e in new_entries if e[2] == "cielingo_cards"]),
             len([e for e in new_entries if e[2] == "writings_log"]))

    if not dry_run and new_entries:
        conn.executemany(
            "INSERT INTO m8_audit (timestamp, event, source, details, severity) VALUES (?,?,?,?,?)",
            new_entries,
        )
        conn.commit()
        log.info("Wrote %d new entries to state_db.m8_audit", len(new_entries))

    # ── Summary ──
    conn.close()
    return {
        "sources": list(sources.keys()),
        "memory_log_count": len(ml_records),
        "cielingo_card_count": len(cielingo_entries),
        "writings_log_count": len(writings_entries),
        "existing_in_db": len(existing),
        "new_written": len(new_entries) if not dry_run else 0,
        "gaps": ["M8 runtime snapshot requires CIEL pipeline periodic call"],
    }


def snapshot_m8_to_state_db(
    events: list[dict[str, Any]],
    *,
    source: str = "m8_runtime",
) -> int:
    """Bridge GAP-M8: zapisz M8 runtime audit events do state_db.

    Call this from CIEL pipeline periodically to persist M8 audit data.

    Args:
        events: list of audit event dicts with keys:
                timestamp, event, [details], [severity]
        source: source label for m8_audit.source column

    Returns:
        number of new entries written
    """
    conn = sqlite3.connect(str(STATE_DB))
    _ensure_schema(conn)
    existing = conn.execute("SELECT timestamp, event, source FROM m8_audit").fetchall()
    existing_set = {(r[0], r[1], r[2]) for r in existing}

    new_entries = []
    for ev in events:
        ts = ev.get("timestamp", "")
        event = ev.get("event", "unknown")
        key = (ts, event, source)
        if ts and key not in existing_set:
            details = ev.get("details", {})
            severity = ev.get("severity", "info")
            new_entries.append((ts, event, source, json.dumps(details, default=str), severity))
            existing_set.add(key)

    if new_entries:
        conn.executemany(
            "INSERT INTO m8_audit (timestamp, event, source, details, severity) VALUES (?,?,?,?,?)",
            new_entries,
        )
        conn.commit()

    conn.close()
    return len(new_entries)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="NOEMA Audit Consolidator")
    ap.add_argument("--dry-run", action="store_true", help="Scan only, no writes")
    args = ap.parse_args()
    src_count, ml_count, new_count = consolidate(dry_run=args.dry_run)
    print(f"Sources: {src_count}, MemoryLog: {ml_count}, New: {new_count}")
