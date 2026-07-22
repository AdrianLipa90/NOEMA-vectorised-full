#!/usr/bin/env python3
"""NOEMA DB Refresh Orchestrator — metatime-grounded phase correction.

Runs every 30 min via systemd timer. Refreshes stale databases by running
generators in dependency order with per-step timeouts.

Refresh contract:
  The systemd timer is the cadence authority (30 minutes). Database TTLs are
  that cadence multiplied by the documented stability factors. The orbital
  report is refreshed every cycle because the portal declares it stale after
  120 seconds.

Usage:
    python3 scripts/noema_db_refresh_orchestrator.py              # normal cycle
    python3 scripts/noema_db_refresh_orchestrator.py --cold-start # first run
    python3 scripts/noema_db_refresh_orchestrator.py --dry-run    # check only
"""
from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
VENV_PYTHON = ROOT / ".venv" / "bin" / "python3"
LOG_DIR = Path("/media/adrian/New Volume/CIEL_memories/logs")
LOG_FILE = LOG_DIR / "db_refresh.jsonl"

# Refresh cadence and TTLs (seconds), mirroring the active 30-minute timer.
REFRESH_CADENCE_SECONDS = 30 * 60
TTL_KNOWLEDGE = REFRESH_CADENCE_SECONDS
TTL_PHASENAV = REFRESH_CADENCE_SECONDS * 2
TTL_CARDS = REFRESH_CADENCE_SECONDS * 4
TTL_MAP = REFRESH_CADENCE_SECONDS * 8
TTL_ORBITAL = REFRESH_CADENCE_SECONDS

# Max runtime per step (seconds)
MAX_RUNTIME = {
    "analyze": 600,
    "affinity": 600,
    "indexer": 300,
    "cards": 120,
    "map": 60,
    "orbital": 120,
}

# Knowledge DB path — hardcoded to avoid heavy import chain
KNOWLEDGE_DB = "/media/adrian/New Volume/CIEL_memories/state/noema_knowledge.db"
PHASE_DATA_ROOT = Path("/media/adrian/New Volume/NOEMA_PHASE_DATA")
LIBRARY_ROOT = Path("/media/adrian/New Volume/NOEMA_LIBRARY")
PHASENAV_OUTPUTS = (
    PHASE_DATA_ROOT / "PHASE_INDEX" / "knowledge_graph.json",
    PHASE_DATA_ROOT / "PHASE_INDEX" / "library_map.json",
    LIBRARY_ROOT / "INDEX" / "phasenav_meta.jsonl",
)
CARD_OUTPUTS = (
    PHASE_DATA_ROOT / "orbital_cards",
    ROOT / "docs" / "object_cards" / "db",
)
SYSTEM_MAP = ROOT / "system_map_v2.json"
ORBITAL_REPORT = ROOT / "integration" / "reports" / "orbital_bridge" / "orbital_bridge_report.json"


def log_entry(entry: dict) -> None:
    """Append one JSONL entry to the audit log."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def check_staleness() -> dict[str, dict]:
    """Check phase drift for each database. Returns {name: {mtime, ttl, stale, drift_s}}."""
    now = time.time()
    checks = {}

    # Knowledge DB — check doc_analysis ingested count
    try:
        db = sqlite3.connect(KNOWLEDGE_DB, timeout=5.0)
        db.row_factory = sqlite3.Row
        n_ingested = db.execute(
            "SELECT COUNT(*) FROM doc_analysis WHERE status='ingested'"
        ).fetchone()[0]
        n_analyzed = db.execute(
            "SELECT COUNT(*) FROM doc_analysis WHERE status='analyzed'"
        ).fetchone()[0]
        db.close()
        mtime = os.path.getmtime(KNOWLEDGE_DB)
        drift = now - mtime
        checks["knowledge"] = {
            "path": KNOWLEDGE_DB,
            "mtime_s": mtime,
            "drift_s": round(drift),
            "ttl": TTL_KNOWLEDGE,
            "stale": drift > TTL_KNOWLEDGE or n_ingested > 100,
            "n_ingested": n_ingested,
            "n_analyzed": n_analyzed,
        }
    except Exception as e:
        checks["knowledge"] = {"error": str(e), "stale": True}

    # PhaseNav indexes on New Volume (runtime shm is not a database source).
    phasenav_files = [path for path in PHASENAV_OUTPUTS if path.exists() and path.is_file()]
    if phasenav_files:
        newest = max(phasenav_files, key=lambda path: path.stat().st_mtime)
        mtime = newest.stat().st_mtime
        drift = now - mtime
        checks["phasenav"] = {
            "path": str(newest),
            "candidates": [str(path) for path in PHASENAV_OUTPUTS],
            "mtime_s": mtime,
            "drift_s": round(drift),
            "ttl": TTL_PHASENAV,
            "stale": drift > TTL_PHASENAV,
        }
    else:
        checks["phasenav"] = {"error": "file not found", "stale": True}

    # Orbital cards on the canonical library/canon trees.
    card_files = [
        path for output in CARD_OUTPUTS if output.exists()
        for path in (list(output.rglob("*")) if output.is_dir() else [output])
        if path.is_file()
    ]
    if card_files:
        mtimes = [path.stat().st_mtime for path in card_files]
        if mtimes:
            newest = max(mtimes)
            drift = now - newest
            checks["cards"] = {
                "path": str(max(card_files, key=lambda path: path.stat().st_mtime).parent),
                "drift_s": round(drift),
                "ttl": TTL_CARDS,
                "stale": drift > TTL_CARDS,
                "n_files": len(mtimes),
            }
        else:
            checks["cards"] = {"error": "empty dir", "stale": True}
    else:
        checks["cards"] = {"error": "dir not found", "stale": True}

    # Canonical system map in the active checkout.
    if SYSTEM_MAP.exists():
        mtime = SYSTEM_MAP.stat().st_mtime
        drift = now - mtime
        checks["map"] = {
            "path": str(SYSTEM_MAP),
            "drift_s": round(drift),
            "ttl": TTL_MAP,
            "stale": drift > TTL_MAP,
        }
    else:
        checks["map"] = {"error": "file not found", "stale": True}

    # Portal source: refresh every timer cycle, independent of database TTLs.
    if ORBITAL_REPORT.exists():
        mtime = ORBITAL_REPORT.stat().st_mtime
        drift = now - mtime
        checks["orbital"] = {
            "path": str(ORBITAL_REPORT),
            "mtime_s": mtime,
            "drift_s": round(drift),
            "ttl": TTL_ORBITAL,
            "stale": drift > TTL_ORBITAL,
            "refresh_each_cycle": True,
        }
    else:
        checks["orbital"] = {
            "path": str(ORBITAL_REPORT),
            "error": "file not found",
            "ttl": TTL_ORBITAL,
            "stale": True,
            "refresh_each_cycle": True,
        }

    return checks


def run_step(name: str, cmd: list[str], max_time: int) -> dict:
    """Run a generator step with timeout. Returns result dict."""
    t0 = time.time()
    result = {"step": name, "started_at": datetime.now(timezone.utc).isoformat()}
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=max_time,
            cwd=str(ROOT),
            env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
        )
        elapsed = time.time() - t0
        result["elapsed_s"] = round(elapsed, 1)
        result["returncode"] = proc.returncode
        result["stdout_tail"] = proc.stdout[-500:] if proc.stdout else ""
        result["stderr_tail"] = proc.stderr[-500:] if proc.stderr else ""
        if proc.returncode == 0:
            result["status"] = "ok"
        else:
            result["status"] = "failed"
    except subprocess.TimeoutExpired:
        elapsed = time.time() - t0
        result["elapsed_s"] = round(elapsed, 1)
        result["status"] = "timeout"
        result["timeout_s"] = max_time
    except Exception as e:
        elapsed = time.time() - t0
        result["elapsed_s"] = round(elapsed, 1)
        result["status"] = "error"
        result["error"] = str(e)
    return result


def step_analyze(stale: bool, n_ingested: int) -> dict:
    """Step 1: Process ingested documents in batches (avoids long SQLite locks)."""
    if not stale and n_ingested < 100:
        return {"step": "analyze", "status": "skipped", "reason": "not_stale", "n_ingested": n_ingested}

    try:
        db = sqlite3.connect(KNOWLEDGE_DB, timeout=10.0)
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("PRAGMA busy_timeout=5000")
        batch_size = 1000
        total_moved = 0
        while True:
            cursor = db.execute(
                "UPDATE doc_analysis SET status='analyzed' WHERE rowid IN "
                "(SELECT rowid FROM doc_analysis WHERE status='ingested' LIMIT ?)",
                (batch_size,),
            )
            db.commit()
            moved = cursor.rowcount
            total_moved += moved
            if moved < batch_size:
                break
        remaining = db.execute(
            "SELECT COUNT(*) FROM doc_analysis WHERE status='ingested'"
        ).fetchone()[0]
        db.close()
        return {
            "step": "analyze",
            "status": "ok",
            "docs_processed": total_moved,
            "remaining_ingested": remaining,
        }
    except Exception as e:
        return {"step": "analyze", "status": "error", "error": str(e)}


def step_affinity(stale: bool) -> dict:
    """Step 2: Build semantic affinity matrix."""
    if not stale:
        return {"step": "affinity", "status": "skipped", "reason": "not_stale"}
    return run_step(
        "affinity",
        [str(VENV_PYTHON), str(SCRIPTS / "noema_build_semantic_affinity.py")],
        MAX_RUNTIME["affinity"],
    )


def step_indexer(stale: bool) -> dict:
    """Step 3: Build PhaseNav 36D index."""
    if not stale:
        return {"step": "indexer", "status": "skipped", "reason": "not_stale"}
    return run_step(
        "indexer",
        [str(VENV_PYTHON), str(SCRIPTS / "noema_indexer.py"), "--build"],
        MAX_RUNTIME["indexer"],
    )


def step_cards(stale: bool) -> dict:
    """Step 4: Generate orbital cards."""
    if not stale:
        return {"step": "cards", "status": "skipped", "reason": "not_stale"}
    return run_step(
        "cards",
        [str(VENV_PYTHON), str(SCRIPTS / "generate_orbital_cards.py")],
        MAX_RUNTIME["cards"],
    )


def step_map(stale: bool) -> dict:
    """Step 5: Canonicalize system map edges."""
    if not stale:
        return {"step": "map", "status": "skipped", "reason": "not_stale"}
    return run_step(
        "map",
        [str(VENV_PYTHON), str(SCRIPTS / "canonicalize_system_map_edges.py"), "--apply"],
        MAX_RUNTIME["map"],
    )


def step_orbital() -> dict:
    """Step 6: Refresh the portal's PhaseNav + canonical EBA report."""
    return run_step(
        "orbital",
        [str(VENV_PYTHON), "-m", "ciel_sot_agent.orbital_bridge", "--phase-orbital-only"],
        MAX_RUNTIME["orbital"],
    )


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="NOEMA DB Refresh Orchestrator")
    parser.add_argument("--cold-start", action="store_true", help="Force refresh all stale databases")
    parser.add_argument("--dry-run", action="store_true", help="Check staleness only, don't run generators")
    args = parser.parse_args()

    cycle_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    t0 = time.time()

    print(f"[orchestrator] cycle={cycle_id} cold_start={args.cold_start}")

    # Phase 1: Staleness detection
    checks = check_staleness()
    n_stale = sum(1 for c in checks.values() if c.get("stale", False))
    print(f"[orchestrator] staleness check: {n_stale}/{len(checks)} databases stale")
    for name, c in checks.items():
        status = "STALE" if c.get("stale") else "ok"
        drift = c.get("drift_s", "?")
        print(f"  {name}: {status} (drift={drift}s, ttl={c.get('ttl', '?')}s)")

    if args.dry_run:
        log_entry({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "cycle": cycle_id,
            "mode": "dry_run",
            "checks": checks,
        })
        print("[orchestrator] dry-run complete")
        return

    # Phase 2: Sequential execution
    steps = []

    # Step 1: Analyze (always run if stale)
    knowledge_stale = checks.get("knowledge", {}).get("stale", False)
    n_ingested = checks.get("knowledge", {}).get("n_ingested", 0)
    r = step_analyze(knowledge_stale or args.cold_start, n_ingested)
    steps.append(r)
    print(f"[orchestrator] step 1 (analyze): {r['status']} {r.get('docs_processed', '')}")

    # Step 2: Affinity (depends on analyze)
    r = step_affinity(knowledge_stale or args.cold_start)
    steps.append(r)
    print(f"[orchestrator] step 2 (affinity): {r['status']} {r.get('elapsed_s', '')}")

    # Step 3: Indexer (depends on analyze, parallel with affinity)
    phasenav_stale = checks.get("phasenav", {}).get("stale", False)
    r = step_indexer(phasenav_stale or args.cold_start)
    steps.append(r)
    print(f"[orchestrator] step 3 (indexer): {r['status']} {r.get('elapsed_s', '')}")

    # Step 4: Cards (depends on indexer)
    cards_stale = checks.get("cards", {}).get("stale", False)
    r = step_cards(cards_stale or args.cold_start)
    steps.append(r)
    print(f"[orchestrator] step 4 (cards): {r['status']} {r.get('elapsed_s', '')}")

    # Step 5: Map (parallel with 1-4)
    map_stale = checks.get("map", {}).get("stale", False)
    r = step_map(map_stale or args.cold_start)
    steps.append(r)
    print(f"[orchestrator] step 5 (map): {r['status']} {r.get('elapsed_s', '')}")

    # Step 6: portal report — always refresh; the portal has a 120s freshness
    # contract and the report is backed by the live read-only NoemaSurface.
    r = step_orbital()
    steps.append(r)
    print(f"[orchestrator] step 6 (orbital): {r['status']} {r.get('elapsed_s', '')}")

    # Phase 3: Validation
    total_elapsed = round(time.time() - t0, 1)
    n_ok = sum(1 for s in steps if s.get("status") == "ok")
    n_skipped = sum(1 for s in steps if s.get("status") == "skipped")
    n_failed = sum(1 for s in steps if s.get("status") in ("failed", "timeout", "error"))

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "cycle": cycle_id,
        "cold_start": args.cold_start,
        "checks": checks,
        "steps": steps,
        "summary": {
            "total_ok": n_ok,
            "total_skipped": n_skipped,
            "total_failed": n_failed,
            "total_elapsed_s": total_elapsed,
        },
    }
    log_entry(entry)

    print(f"[orchestrator] cycle complete: ok={n_ok} skipped={n_skipped} failed={n_failed} elapsed={total_elapsed}s")

    if n_failed > 0:
        print("[orchestrator] FAILED STEPS:")
        for s in steps:
            if s.get("status") in ("failed", "timeout", "error"):
                print(f"  {s['step']}: {s.get('error', s.get('stderr_tail', 'unknown'))}")
        sys.exit(1)


if __name__ == "__main__":
    main()
