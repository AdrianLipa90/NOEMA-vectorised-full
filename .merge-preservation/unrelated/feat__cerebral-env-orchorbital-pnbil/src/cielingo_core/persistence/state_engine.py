import json, sqlite3, time, threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STATE_DB = str(Path.home() / ".cielingo" / "state.db")


def _ensure_db(path: str = STATE_DB) -> sqlite3.Connection:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA synchronous=NORMAL")
    db.executescript("""
        CREATE TABLE IF NOT EXISTS meaning_loops (
            loop_id TEXT PRIMARY KEY,
            input_ref TEXT,
            response_ref TEXT,
            loop_state TEXT,
            closure_score REAL,
            contradiction_score REAL,
            residue_score REAL,
            return_required INTEGER,
            scar_count INTEGER,
            source TEXT,
            created_at REAL,
            updated_at REAL
        );
        CREATE TABLE IF NOT EXISTS scars (
            scar_id TEXT PRIMARY KEY,
            loop_id TEXT,
            scar_type TEXT,
            source_ref TEXT,
            severity REAL,
            memory_effect TEXT,
            repair_hint TEXT,
            source_binding TEXT,
            created_at REAL,
            resolved_at REAL,
            resolution TEXT,
            FOREIGN KEY(loop_id) REFERENCES meaning_loops(loop_id)
        );
        CREATE TABLE IF NOT EXISTS repair_candidates (
            repair_id TEXT PRIMARY KEY,
            loop_id TEXT,
            scar_id TEXT,
            route_kind TEXT,
            target_ref TEXT,
            description TEXT,
            required_before_closure INTEGER,
            confidence REAL,
            status TEXT DEFAULT 'pending',
            resolved_at REAL,
            resolution_note TEXT,
            created_at REAL,
            FOREIGN KEY(loop_id) REFERENCES meaning_loops(loop_id),
            FOREIGN KEY(scar_id) REFERENCES scars(scar_id)
        );
        CREATE TABLE IF NOT EXISTS experience_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            event_type TEXT,
            source TEXT,
            summary TEXT,
            details TEXT,
            salience REAL,
            consolidated INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS self_metrics (
            metric TEXT PRIMARY KEY,
            value REAL,
            updated_at REAL
        );
        CREATE TABLE IF NOT EXISTS knowledge_writes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_term TEXT,
            target_term TEXT,
            relationship TEXT,
            strength REAL,
            created_at REAL,
            source TEXT
        );
    """)
    return db


class CIELingoStateEngine:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, path: str | None = None):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._db_path = path or STATE_DB
                    cls._instance._local = threading.local()
        return cls._instance

    def _db(self) -> sqlite3.Connection:
        if not hasattr(self._local, "conn") or self._local.conn is None:
            self._local.conn = _ensure_db(self._db_path)
        return self._local.conn

    # ── Meaning loops ──

    def save_loop(self, loop_data: dict[str, Any]) -> None:
        db = self._db()
        now = time.time()
        db.execute(
            """INSERT OR REPLACE INTO meaning_loops
               (loop_id, input_ref, response_ref, loop_state, closure_score,
                contradiction_score, residue_score, return_required,
                scar_count, source, created_at, updated_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                loop_data.get("loop_id"),
                loop_data.get("input_ref", ""),
                loop_data.get("response_ref"),
                loop_data.get("loop_state", "open"),
                loop_data.get("closure_score", 0.0),
                loop_data.get("contradiction_score", 0.0),
                loop_data.get("residue_score", 0.0),
                1 if loop_data.get("return_required") else 0,
                len(loop_data.get("scars", [])),
                loop_data.get("source", "engine"),
                loop_data.get("created_at", now),
                now,
            ),
        )
        for scar in loop_data.get("scars", []):
            self._save_scar(loop_data.get("loop_id"), scar)
        db.commit()

    def _save_scar(self, loop_id: str | None, scar: dict[str, Any]) -> None:
        db = self._db()
        db.execute(
            """INSERT OR REPLACE INTO scars
               (scar_id, loop_id, scar_type, source_ref, severity,
                memory_effect, repair_hint, source_binding, created_at)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (
                scar.get("scar_id"),
                loop_id,
                scar.get("scar_type"),
                scar.get("source_ref", ""),
                scar.get("severity", 0.0),
                scar.get("memory_effect", ""),
                scar.get("repair_hint", ""),
                scar.get("source_binding", "artifact_grounded"),
                time.time(),
            ),
        )

    def get_loops(self, limit: int = 50, state: str | None = None) -> list[dict[str, Any]]:
        db = self._db()
        if state:
            rows = db.execute(
                "SELECT * FROM meaning_loops WHERE loop_state=? ORDER BY created_at DESC LIMIT ?",
                (state, limit),
            ).fetchall()
        else:
            rows = db.execute(
                "SELECT * FROM meaning_loops ORDER BY created_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [dict(r) for r in rows]

    def get_scars(self, unresolved_only: bool = False) -> list[dict[str, Any]]:
        db = self._db()
        if unresolved_only:
            rows = db.execute(
                "SELECT * FROM scars WHERE resolved_at IS NULL ORDER BY severity DESC LIMIT 50"
            ).fetchall()
        else:
            rows = db.execute(
                "SELECT * FROM scars ORDER BY created_at DESC LIMIT 100"
            ).fetchall()
        return [dict(r) for r in rows]

    def resolve_scar(self, scar_id: str, resolution: str = "auto_resolved", note: str = "") -> None:
        db = self._db()
        db.execute(
            "UPDATE scars SET resolved_at=?, resolution=? WHERE scar_id=?",
            (time.time(), resolution, scar_id),
        )
        db.commit()
        if note:
            self.log_experience("scar_resolved", "state_engine",
                                f"Scar {scar_id[:16]} resolved: {resolution}", note, 0.3)

    def update_loop_state(self, loop_id: str, new_state: str, closure_score: float | None = None) -> None:
        db = self._db()
        now = time.time()
        if closure_score is not None:
            db.execute(
                "UPDATE meaning_loops SET loop_state=?, closure_score=?, updated_at=? WHERE loop_id=?",
                (new_state, closure_score, now, loop_id),
            )
        else:
            db.execute(
                "UPDATE meaning_loops SET loop_state=?, updated_at=? WHERE loop_id=?",
                (new_state, now, loop_id),
            )
        db.commit()

    # ── Repair candidates ──

    def save_repair(self, repair: dict[str, Any]) -> None:
        db = self._db()
        now = time.time()
        db.execute(
            """INSERT OR REPLACE INTO repair_candidates
               (repair_id, loop_id, scar_id, route_kind, target_ref,
                description, required_before_closure, confidence,
                status, created_at)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (
                repair.get("repair_id"),
                repair.get("loop_id"),
                repair.get("scar_id"),
                repair.get("route_kind"),
                repair.get("target_ref", ""),
                repair.get("description", ""),
                1 if repair.get("required_before_closure") else 0,
                repair.get("confidence", 0.0),
                repair.get("status", "pending"),
                now,
            ),
        )
        db.commit()

    def resolve_repair(self, repair_id: str, resolution: str, note: str = "") -> None:
        db = self._db()
        db.execute(
            "UPDATE repair_candidates SET status=?, resolved_at=?, resolution_note=? WHERE repair_id=?",
            (resolution, time.time(), note, repair_id),
        )
        db.commit()

    def get_pending_repairs(self) -> list[dict[str, Any]]:
        db = self._db()
        rows = db.execute(
            "SELECT * FROM repair_candidates WHERE status='pending' ORDER BY confidence DESC, required_before_closure DESC"
        ).fetchall()
        return [dict(r) for r in rows]

    # ── Experience ──

    def log_experience(self, event_type: str, source: str, summary: str,
                       details: str = "", salience: float = 0.5) -> None:
        db = self._db()
        db.execute(
            "INSERT INTO experience_log (timestamp, event_type, source, summary, details, salience) VALUES (?,?,?,?,?,?)",
            (time.time(), event_type, source, summary, details, salience),
        )
        db.commit()

    def get_recent_experience(self, limit: int = 20) -> list[dict[str, Any]]:
        db = self._db()
        rows = db.execute(
            "SELECT * FROM experience_log ORDER BY timestamp DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]

    # ── Self metrics ──

    def increment_metric(self, name: str, delta: float = 1.0) -> float:
        current = self.get_metric(name, 0.0)
        new_val = current + delta
        self.update_metric(name, new_val)
        return new_val

    def update_metric(self, name: str, value: float) -> None:
        db = self._db()
        db.execute(
            "INSERT OR REPLACE INTO self_metrics (metric, value, updated_at) VALUES (?,?,?)",
            (name, value, time.time()),
        )
        db.commit()

    def get_metric(self, name: str, default: float = 0.0) -> float:
        db = self._db()
        row = db.execute("SELECT value FROM self_metrics WHERE metric=?", (name,)).fetchone()
        return row["value"] if row else default

    def get_all_metrics(self) -> dict[str, float]:
        db = self._db()
        rows = db.execute("SELECT metric, value FROM self_metrics").fetchall()
        return {r["metric"]: r["value"] for r in rows}

    # ── Knowledge graph writes ──

    def write_knowledge_relation(self, source: str, target: str, relationship: str,
                                  strength: float = 0.5, tag: str = "cielingo") -> None:
        db = self._db()
        db.execute(
            "INSERT INTO knowledge_writes (source_term, target_term, relationship, strength, source) VALUES (?,?,?,?,?)",
            (source, target, relationship, strength, tag),
        )
        db.commit()

    # ── Exports ──

    def export_state(self) -> dict[str, Any]:
        loops = self.get_loops(limit=100)
        scars = self.get_scars(unresolved_only=True)
        pending = self.get_pending_repairs()
        metrics = self.get_all_metrics()
        return {
            "n_loops": len(loops),
            "n_unresolved_scars": len(scars),
            "n_pending_repairs": len(pending),
            "recent_loops": loops[:10],
            "top_scars": scars[:10],
            "pending_repairs": pending[:10],
            "metrics": metrics,
        }

    def close(self) -> None:
        if hasattr(self._local, "conn") and self._local.conn:
            self._local.conn.close()
            self._local.conn = None
