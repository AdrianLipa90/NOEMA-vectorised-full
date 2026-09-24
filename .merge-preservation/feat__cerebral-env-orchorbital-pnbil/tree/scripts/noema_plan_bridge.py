import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

# CIEL ORBITAL BINDING — daemon bound
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on daemon " + __name__)
#!/usr/bin/env python3
"""NOEMA Plan Bridge — udostępnia plany CIELingo/Doctor i odbiera taski.

Usage:
    python3 noema_plan_bridge.py --snapshot    # eksport planów do /dev/shm
    python3 noema_plan_bridge.py --inbox       # przetwarzaj taski z inboxa
    python3 noema_plan_bridge.py --daemon      # tryb ciągły (snapshot + inbox)
    python3 noema_plan_bridge.py --status      # pokaż stan bridge'a

Architektura:
    ┌─────────────┐     plans_snapshot.json     ┌──────────────┐
    │  CIELingo   │◄────────────────────────────│  Plan Bridge │
    │  Doctor     │     task_inbox.jsonl        │  (ten skrypt)│
    │             │────────────────────────────►│              │
    └─────────────┘                             └──────┬───────┘
                                                       │
                                                task_queue.noema.json
                                                       │
                                                       ▼
                                                ┌──────────────┐
                                                │    Agent     │
                                                │  (ja — CIEL) │
                                                └──────────────┘
"""
import argparse
import json
import os
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path

# ── Constants ──────────────────────────────────────────────────────────────
SHM = Path("/dev/shm/ciel_noema")
PLANS_SNAPSHOT = SHM / "plans_snapshot.json"
TASK_INBOX = SHM / "task_inbox.jsonl"
_LIB_DEFAULT = os.path.join(os.sep, "media", "adrian", "New Volume", "NOEMA_LIBRARY")
NOEMA_LIBRARY = Path(os.environ.get("NOEMA_LIBRARY", _LIB_DEFAULT))
DB_PATH = NOEMA_LIBRARY / "agent_db" / "taskplan.db"
_SCRIPT_DIR = Path(__file__).resolve().parent
NOEMA_ROOT = Path(os.environ.get("NOEMA_ROOT", str(_SCRIPT_DIR.parent)))
TASK_QUEUE = NOEMA_ROOT / "NOEMA" / "task_queue.noema.json"


def write_snapshot() -> dict:
    """Eksportuj plany z DB do plans_snapshot.json."""
    db = sqlite3.connect(str(DB_PATH))
    cur = db.cursor()
    cur.execute("SELECT id, lp, title, description, status, steps, orbital_ref, created_at, updated_at FROM plans")
    plans = []
    for row in cur.fetchall():
        plans.append({
            "id": row[0],
            "lp": row[1],
            "title": row[2],
            "description": row[3],
            "status": row[4],
            "steps": json.loads(row[5]) if row[5] else [],
            "orbital_ref": row[6],
            "created_at": row[7],
            "updated_at": row[8],
        })
    db.close()

    # Dodaj też aktywne taski
    db2 = sqlite3.connect(str(DB_PATH))
    cur2 = db2.cursor()
    cur2.execute("SELECT id, lp, title, status, priority, category, orbital_ref FROM tasks WHERE status=? ORDER BY id", ("pending",))
    pending_tasks = []
    for row in cur2.fetchall():
        pending_tasks.append({
            "id": row[0], "lp": row[1], "title": row[2],
            "status": row[3], "priority": row[4],
            "category": row[5], "orbital_ref": row[6],
        })
    db2.close()

    snapshot = {
        "ts": datetime.now().isoformat(),
        "plans": plans,
        "plans_count": len(plans),
        "pending_tasks": pending_tasks,
        "pending_count": len(pending_tasks),
        "format_version": "1.0",
        "note": "CIELingo/Doctor: czytaj plans, pisz taski do task_inbox.jsonl",
    }

    SHM.mkdir(parents=True, exist_ok=True)
    with open(PLANS_SNAPSHOT, "w") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)

    return snapshot


def process_inbox() -> list:
    """Przetwarzaj nowe taski z task_inbox.jsonl."""
    if not TASK_INBOX.exists():
        return []

    new_tasks = []
    remaining = []

    with open(TASK_INBOX, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            if entry.get("processed"):
                remaining.append(line)
                continue
            # Nieprzetworzony task
            entry["processed"] = True
            entry["processed_at"] = datetime.now().isoformat()
            new_tasks.append(entry)

            # Dodaj do task_queue.noema.json
            _add_to_task_queue(entry)
            remaining.append(json.dumps(entry, ensure_ascii=False))

    # Nadpisz inbox z oznaczeniem processed
    with open(TASK_INBOX, "w") as f:
        for line in remaining:
            f.write(line + "\n")

    return new_tasks


def _add_to_task_queue(entry: dict):
    """Dodaj task do task_queue.noema.json."""
    if not TASK_QUEUE.exists():
        queue = {"queue": [], "meta": {"version": "1.0"}}
    else:
        with open(TASK_QUEUE) as f:
            try:
                queue = json.load(f)
            except (json.JSONDecodeError, Exception):
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_plan_bridge.py:143 quiet except scope=_add_to_task_queue reason=assign_fallback")
                raise
                queue = {"queue": [], "meta": {"version": "1.0"}}

    priority_map = {"high": "HIGH — selected by Adrian", "medium": "MEDIUM", "low": "LOW"}
    task_entry = {
        "task": entry.get("title", "untitled"),
        "task_id": entry.get("task_id", f"bridge-{int(time.time())}"),
        "status": "pending",
        "priority": priority_map.get(entry.get("priority", "medium"), "MEDIUM"),
        "source": entry.get("source", "plan_bridge"),
        "plan_ref": entry.get("plan_ref", ""),
        "description": entry.get("description", ""),
        "created_at": datetime.now().isoformat(),
    }
    queue["queue"].append(task_entry)

    with open(TASK_QUEUE, "w") as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)


def show_status() -> dict:
    """Pokaż stan bridge'a."""
    status = {"bridge": "plan_bridge", "version": "1.0"}
    status["plans_snapshot"] = PLANS_SNAPSHOT.exists()
    if status["plans_snapshot"]:
        try:
            with open(PLANS_SNAPSHOT) as f:
                data = json.load(f)
            status["plans_count"] = data.get("plans_count", 0)
            status["pending_count"] = data.get("pending_count", 0)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_plan_bridge.py:173 quiet except scope=show_status reason=pass")
            raise
            pass

    status["task_inbox"] = TASK_INBOX.exists()
    if status["task_inbox"]:
        try:
            with open(TASK_INBOX) as f:
                lines = [l for l in f if l.strip()]
            total = len(lines)
            processed = sum(1 for l in lines if '"processed": true' in l)
            status["inbox_total"] = total
            status["inbox_processed"] = processed
            status["inbox_pending"] = total - processed
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_plan_bridge.py:186 quiet except scope=show_status reason=pass")
            raise
            pass

    status["task_queue"] = TASK_QUEUE.exists()
    if status["task_queue"]:
        try:
            with open(TASK_QUEUE) as f:
                q = json.load(f)
            status["queue_size"] = len(q.get("queue", []))
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_plan_bridge.py:195 quiet except scope=show_status reason=pass")
            raise
            pass

    return status


def daemon_loop(interval: int = 30):
    """Tryb ciągły: snapshot + inbox co interval sekund."""
    log = __import__("logging").getLogger("plan_bridge")
    print(f"[plan_bridge] daemon start — interval={interval}s")

    while True:
        try:
            snap = write_snapshot()
            new = process_inbox()
            if new:
                print(f"[plan_bridge] +{len(new)} tasków z inboxa: {[t.get('title','')[:40] for t in new]}")
        except Exception as e:
            print(f"[plan_bridge] error: {e}")
        time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(description="NOEMA Plan Bridge")
    parser.add_argument("--snapshot", action="store_true", help="Eksport planów do shared memory")
    parser.add_argument("--inbox", action="store_true", help="Przetwarzaj taski z inboxa")
    parser.add_argument("--daemon", action="store_true", help="Tryb ciągły")
    parser.add_argument("--interval", type=int, default=30, help="Interval daemona (s)")
    parser.add_argument("--status", action="store_true", help="Pokaż stan")
    args = parser.parse_args()

    if args.snapshot:
        snap = write_snapshot()
        print(f"[plan_bridge] snapshot: {snap['plans_count']} plans, {snap['pending_count']} pending tasks")
        return

    if args.inbox:
        new = process_inbox()
        print(f"[plan_bridge] processed {len(new)} new tasks from inbox")
        return

    if args.daemon:
        daemon_loop(args.interval)
        return

    if args.status:
        st = show_status()
        print(json.dumps(st, indent=2, ensure_ascii=False))
        return

    # Default: snapshot + inbox
    write_snapshot()
    new = process_inbox()
    print(f"[plan_bridge] snapshot + inbox: {len(new)} tasks processed")


if __name__ == "__main__":
    main()
