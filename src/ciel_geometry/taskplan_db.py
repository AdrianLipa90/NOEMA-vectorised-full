"""
taskplan_db.py — Baza tasków, planów i lekcji z LP (liczbą porządkową).

Tabele:
  tasks    — zadania/zadania z LP, status, priorytet, orbital_ref
  plans    — plany z LP, kroki (JSON), status
  lessons  — lekcje z LP (odpowiednik LEARNED_LESSONS.md)
  registry — klucze meta (wersja schematu, ostatni update)
"""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import sqlite3
import json
import time
from pathlib import Path

from ciel_geometry.paths import P

# Was hardcoded /tmp/noema_taskplan.db (tmpfs, wiped on reboot) — this is
# very likely why tasks/plans/lessons were found empty (0/0/0) on
# 2026-07-08: any daemon that ever populated it lost everything on the
# next reboot. Fixed to a persistent path.
DB_PATH = str(P.DB.TASKPLAN)

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS tasks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    lp          TEXT NOT NULL,            -- np. "01", "01.01"
    title       TEXT NOT NULL,
    description TEXT DEFAULT '',
    status      TEXT NOT NULL DEFAULT 'pending',  -- pending|in_progress|completed|cancelled
    priority    TEXT NOT NULL DEFAULT 'medium',   -- high|medium|low
    category    TEXT DEFAULT '',           -- np. "portal", "knowledge", "lesson"
    orbital_ref TEXT DEFAULT '',           -- system_map_v2.json#LP
    parent_id   INTEGER REFERENCES tasks(id),
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS plans (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    lp          TEXT NOT NULL,
    title       TEXT NOT NULL,
    description TEXT DEFAULT '',
    status      TEXT NOT NULL DEFAULT 'draft',  -- draft|active|completed|cancelled
    steps       TEXT DEFAULT '[]',         -- JSON array of step objects
    orbital_ref TEXT DEFAULT '',
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS lessons (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    lp          TEXT NOT NULL UNIQUE,      -- np. "L-019"
    title       TEXT NOT NULL,
    description TEXT DEFAULT '',
    category    TEXT DEFAULT '',           -- np. "lesson", "warning", "rule"
    lesson_date TEXT DEFAULT '',
    source      TEXT DEFAULT '',           -- np. "sesja 2026-06-29"
    tags        TEXT DEFAULT '[]',         -- JSON array
    created_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS registry (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS decisions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    lp              TEXT NOT NULL UNIQUE,     -- np. "D-001", "D-001.01"
    title           TEXT NOT NULL,
    description     TEXT DEFAULT '',
    decision_type   TEXT DEFAULT 'branch',    -- branch|rule|choice|consequence
    condition       TEXT DEFAULT '',          -- warunek logiczny
    decision_text   TEXT DEFAULT '',          -- co wybrano
    consequence     TEXT DEFAULT '',          -- co z tego wynika
    context         TEXT DEFAULT '',          -- kontekst decyzji
    status          TEXT DEFAULT 'active',    -- active|superseded|reverted
    parent_id       INTEGER REFERENCES decisions(id),
    orbital_ref     TEXT DEFAULT '',
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS skill_registry (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL UNIQUE,        -- nazwa katalogu skillu
    title       TEXT DEFAULT '',
    category    TEXT DEFAULT '',             -- kategoria (lns, noema, ciel, ...)
    file_path   TEXT DEFAULT '',
    lines       INTEGER DEFAULT 0,
    frequency   REAL DEFAULT 0.0,           -- częstotliwość użycia (0-1)
    merge_group TEXT DEFAULT '',             -- grupa merge'owania
    orbital_ref TEXT DEFAULT '',
    tags        TEXT DEFAULT '[]',           -- JSON array
    created_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS decision_skills (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    decision_id INTEGER NOT NULL REFERENCES decisions(id) ON DELETE CASCADE,
    skill_id    INTEGER NOT NULL REFERENCES skill_registry(id) ON DELETE CASCADE,
    role        TEXT DEFAULT 'tool',         -- tool|input|output|validator
    weight      REAL DEFAULT 1.0,           -- jak bardzo potrzebny (0-1)
    created_at  TEXT NOT NULL,
    UNIQUE(decision_id, skill_id)
);

INSERT OR IGNORE INTO registry (key, value) VALUES ('schema_version', '3.0');
INSERT OR IGNORE INTO registry (key, value) VALUES ('last_update', '');
"""


class TaskPlanDB:
    """Singleton bazy tasków/planów/lekcji."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = str(Path(db_path).resolve())
        self._init_schema()

    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def _init_schema(self):
        conn = self._conn()
        try:
            conn.executescript(SCHEMA_SQL)
            conn.commit()
        finally:
            conn.close()

    # ── timestamp helper ──
    @staticmethod
    def _ts():
        return time.strftime("%Y-%m-%dT%H:%M:%S")

    # ── LP helpers ──
    def next_lp(self, table: str, parent_lp: str = "") -> str:
        """Generuje następną LP dla tabeli. Jeśli parent_lp='', globalna sekwencja."""
        conn = self._conn()
        try:
            if parent_lp:
                cur = conn.execute(
                    f"SELECT lp FROM {table} WHERE lp LIKE ? ORDER BY lp DESC LIMIT 1",
                    (parent_lp + ".%",)
                )
                row = cur.fetchone()
                if row:
                    parts = row["lp"].rsplit(".", 1)
                    nxt = int(parts[-1]) + 1
                    return f"{parent_lp}.{nxt:02d}"
                else:
                    return f"{parent_lp}.01"
            else:
                cur = conn.execute(f"SELECT lp FROM {table} ORDER BY lp DESC LIMIT 1")
                row = cur.fetchone()
                if row:
                    # lp format: "01", "02" ... lub "10.01" (minor)
                    major = row["lp"].split(".")[0]
                    nxt = int(major) + 1
                    return f"{nxt:02d}"
                else:
                    return "01"
        finally:
            conn.close()

    # ── Tasks ──
    def add_task(self, title: str, description: str = "", priority: str = "medium",
                 category: str = "", orbital_ref: str = "", lp: str = "",
                 parent_id: int = None) -> dict:
        conn = self._conn()
        try:
            if not lp:
                lp = self.next_lp("tasks")
            now = self._ts()
            conn.execute(
                """INSERT INTO tasks (lp, title, description, priority, category, orbital_ref, parent_id, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (lp, title, description, priority, category, orbital_ref, parent_id, now, now)
            )
            conn.commit()
            tid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            conn.execute("UPDATE registry SET value=? WHERE key='last_update'", (now,))
            conn.commit()
            return {"id": tid, "lp": lp, "title": title, "status": "pending"}
        finally:
            conn.close()

    def update_task(self, tid: int, **kwargs) -> bool:
        conn = self._conn()
        try:
            allowed = {"title", "description", "status", "priority", "category", "orbital_ref"}
            sets = []
            vals = []
            for k, v in kwargs.items():
                if k in allowed:
                    sets.append(f"{k}=?")
                    vals.append(v)
            if not sets:
                return False
            vals.append(self._ts())
            cur = conn.execute(f"UPDATE tasks SET {', '.join(sets)}, updated_at=? WHERE id=?", (*vals, tid))
            conn.commit()
            return cur.rowcount > 0
        finally:
            conn.close()

    def get_task(self, tid: int) -> dict:
        conn = self._conn()
        try:
            row = conn.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
            return dict(row) if row else {}
        finally:
            conn.close()

    def list_tasks(self, status: str = "", category: str = "", priority: str = "", limit: int = 50) -> list:
        conn = self._conn()
        try:
            where = []
            vals = []
            if status:
                where.append("status=?")
                vals.append(status)
            if category:
                where.append("category=?")
                vals.append(category)
            if priority:
                where.append("priority=?")
                vals.append(priority)
            q = "SELECT * FROM tasks"
            if where:
                q += " WHERE " + " AND ".join(where)
            q += " ORDER BY CASE priority WHEN 'high' THEN 0 WHEN 'medium' THEN 1 ELSE 2 END, updated_at DESC LIMIT ?"
            vals.append(limit)
            rows = conn.execute(q, vals).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def get_high_priority_tasks(self, limit: int = 5) -> list:
        """Zwraca zadania HIGH lub in_progress — najważniejsze do działania."""
        conn = self._conn()
        try:
            rows = conn.execute(
                """SELECT * FROM tasks
                   WHERE priority = 'high' OR status = 'in_progress'
                   ORDER BY
                       CASE priority WHEN 'high' THEN 0 ELSE 1 END,
                       updated_at DESC
                   LIMIT ?""",
                (limit,)
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def delete_task(self, tid: int) -> bool:
        conn = self._conn()
        try:
            cur = conn.execute("DELETE FROM tasks WHERE id=?", (tid,))
            conn.commit()
            return cur.rowcount > 0
        finally:
            conn.close()

    # ── Plans ──
    def add_plan(self, title: str, description: str = "", steps: list = None,
                 orbital_ref: str = "", lp: str = "") -> dict:
        conn = self._conn()
        try:
            if not lp:
                lp = self.next_lp("plans")
            now = self._ts()
            steps_json = json.dumps(steps or [])
            conn.execute(
                """INSERT INTO plans (lp, title, description, steps, orbital_ref, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (lp, title, description, steps_json, orbital_ref, now, now)
            )
            conn.commit()
            pid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            return {"id": pid, "lp": lp, "title": title, "status": "draft"}
        finally:
            conn.close()

    def update_plan(self, pid: int, **kwargs) -> bool:
        conn = self._conn()
        try:
            allowed = {"title", "description", "status", "steps", "orbital_ref"}
            sets = []
            vals = []
            for k, v in kwargs.items():
                if k in allowed:
                    sets.append(f"{k}=?")
                    vals.append(json.dumps(v) if k == "steps" else v)
            if not sets:
                return False
            vals.append(self._ts())
            cur = conn.execute(f"UPDATE plans SET {', '.join(sets)}, updated_at=? WHERE id=?", (*vals, pid))
            conn.commit()
            return cur.rowcount > 0
        finally:
            conn.close()

    def get_plan(self, pid: int) -> dict:
        conn = self._conn()
        try:
            row = conn.execute("SELECT * FROM plans WHERE id=?", (pid,)).fetchone()
            if row:
                d = dict(row)
                if isinstance(d.get("steps"), str):
                    d["steps"] = json.loads(d["steps"])
                return d
            return {}
        finally:
            conn.close()

    def list_plans(self, status: str = "", limit: int = 20) -> list:
        conn = self._conn()
        try:
            where = []
            vals = []
            if status:
                where.append("status=?")
                vals.append(status)
            q = "SELECT * FROM plans"
            if where:
                q += " WHERE " + " AND ".join(where)
            q += " ORDER BY lp ASC LIMIT ?"
            vals.append(limit)
            rows = conn.execute(q, vals).fetchall()
            result = []
            for r in rows:
                d = dict(r)
                if isinstance(d.get("steps"), str):
                    d["steps"] = json.loads(d["steps"])
                result.append(d)
            return result
        finally:
            conn.close()

    def delete_plan(self, pid: int) -> bool:
        conn = self._conn()
        try:
            cur = conn.execute("DELETE FROM plans WHERE id=?", (pid,))
            conn.commit()
            return cur.rowcount > 0
        finally:
            conn.close()

    # ── Lessons ──
    def add_lesson(self, lp: str, title: str, description: str = "",
                   category: str = "", lesson_date: str = "",
                   source: str = "", tags: list = None) -> dict:
        conn = self._conn()
        try:
            now = self._ts()
            tags_json = json.dumps(tags or [])
            conn.execute(
                """INSERT OR REPLACE INTO lessons (lp, title, description, category, lesson_date, source, tags, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (lp, title, description, category, lesson_date, source, tags_json, now)
            )
            conn.commit()
            return {"lp": lp, "title": title}
        finally:
            conn.close()

    def get_lesson(self, lp: str) -> dict:
        conn = self._conn()
        try:
            row = conn.execute("SELECT * FROM lessons WHERE lp=?", (lp,)).fetchone()
            if row:
                d = dict(row)
                if isinstance(d.get("tags"), str) and d["tags"].strip():
                    try:
                        d["tags"] = json.loads(d["tags"])
                    except json.JSONDecodeError:
                        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/taskplan_db.py:375 quiet except scope=TaskPlanDB.get_lesson reason=assign_fallback")
                        d["tags"] = [t.strip() for t in d["tags"].split(",") if t.strip()]
                return d
            return {}
        finally:
            conn.close()

    def list_lessons(self, category: str = "", limit: int = 50) -> list:
        conn = self._conn()
        try:
            where = []
            vals = []
            if category:
                where.append("category=?")
                vals.append(category)
            q = "SELECT * FROM lessons"
            if where:
                q += " WHERE " + " AND ".join(where)
            q += " ORDER BY lp ASC LIMIT ?"
            vals.append(limit)
            rows = conn.execute(q, vals).fetchall()
            result = []
            for r in rows:
                d = dict(r)
                if isinstance(d.get("tags"), str) and d["tags"].strip():
                    try:
                        d["tags"] = json.loads(d["tags"])
                    except json.JSONDecodeError:
                        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/taskplan_db.py:402 quiet except scope=TaskPlanDB.list_lessons reason=assign_fallback")
                        d["tags"] = [t.strip() for t in d["tags"].split(",") if t.strip()]
                result.append(d)
            return result
        finally:
            conn.close()

    def delete_lesson(self, lp: str) -> bool:
        conn = self._conn()
        try:
            cur = conn.execute("DELETE FROM lessons WHERE lp=?", (lp,))
            conn.commit()
            return cur.rowcount > 0
        finally:
            conn.close()

    # ── Decisions ──
    def add_decision(self, title: str, description: str = "",
                     decision_type: str = "branch", condition: str = "",
                     decision_text: str = "", consequence: str = "",
                     context: str = "", orbital_ref: str = "",
                     parent_id: int = None, lp: str = "") -> dict:
        conn = self._conn()
        try:
            if not lp:
                lp = self._next_decision_lp(conn, parent_id)
            now = self._ts()
            conn.execute(
                """INSERT INTO decisions
                   (lp, title, description, decision_type, condition, decision_text,
                    consequence, context, parent_id, orbital_ref, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (lp, title, description, decision_type, condition, decision_text,
                 consequence, context, parent_id, orbital_ref, now, now)
            )
            conn.commit()
            did = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            conn.execute("UPDATE registry SET value=? WHERE key='last_update'", (now,))
            conn.commit()
            return {"id": did, "lp": lp, "title": title}
        finally:
            conn.close()

    def _next_decision_lp(self, conn, parent_id=None):
        """Generuje LP dla decyzji: D-001, D-002 lub D-001.01 jeśli parent."""
        if parent_id:
            row = conn.execute("SELECT lp FROM decisions WHERE id=?", (parent_id,)).fetchone()
            if row:
                parent_lp = row["lp"]
                sub = conn.execute(
                    "SELECT lp FROM decisions WHERE lp LIKE ? ORDER BY lp DESC LIMIT 1",
                    (parent_lp + ".%",)
                ).fetchone()
                if sub:
                    parts = sub["lp"].rsplit(".", 1)
                    nxt = int(parts[-1]) + 1
                    return f"{parent_lp}.{nxt:02d}"
                else:
                    return f"{parent_lp}.01"
        row = conn.execute("SELECT lp FROM decisions ORDER BY lp DESC LIMIT 1").fetchone()
        if row:
            lp = row["lp"]
            base = lp.split(".")[0]
            nxt = int(base.replace("D-", "")) + 1
            return f"D-{nxt:03d}"
        return "D-001"

    def update_decision(self, did: int, **kwargs) -> bool:
        conn = self._conn()
        try:
            allowed = {"title", "description", "decision_type", "condition",
                       "decision_text", "consequence", "context", "status", "orbital_ref"}
            sets = []
            vals = []
            for k, v in kwargs.items():
                if k in allowed:
                    sets.append(f"{k}=?")
                    vals.append(v)
            if not sets:
                return False
            vals.append(self._ts())
            cur = conn.execute(f"UPDATE decisions SET {', '.join(sets)}, updated_at=? WHERE id=?", (*vals, did))
            conn.commit()
            return cur.rowcount > 0
        finally:
            conn.close()

    def get_decision(self, did: int) -> dict:
        conn = self._conn()
        try:
            row = conn.execute("SELECT * FROM decisions WHERE id=?", (did,)).fetchone()
            return dict(row) if row else {}
        finally:
            conn.close()

    def list_decisions(self, decision_type: str = "", parent_id: int = None,
                       status: str = "", limit: int = 100) -> list:
        conn = self._conn()
        try:
            where = []
            vals = []
            if decision_type:
                where.append("decision_type=?")
                vals.append(decision_type)
            if parent_id is not None:
                where.append("parent_id=?")
                vals.append(parent_id)
            else:
                where.append("parent_id IS NULL")
            if status:
                where.append("status=?")
                vals.append(status)
            q = "SELECT * FROM decisions"
            if where:
                q += " WHERE " + " AND ".join(where)
            q += " ORDER BY lp ASC LIMIT ?"
            vals.append(limit)
            rows = conn.execute(q, vals).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def get_decision_tree(self, root_id: int = None) -> list:
        """Rekurencyjnie buduje drzewo decyzyjne od korzenia."""
        conn = self._conn()
        try:
            if root_id:
                root = conn.execute("SELECT * FROM decisions WHERE id=?", (root_id,)).fetchone()
                if not root:
                    return []
                roots = [root]
            else:
                roots = conn.execute(
                    "SELECT * FROM decisions WHERE parent_id IS NULL ORDER BY lp ASC"
                ).fetchall()
            return [self._build_subtree(conn, dict(r)) for r in roots]
        finally:
            conn.close()

    def _build_subtree(self, conn, node: dict) -> dict:
        children = conn.execute(
            "SELECT * FROM decisions WHERE parent_id=? ORDER BY lp ASC",
            (node["id"],)
        ).fetchall()
        node["children"] = [self._build_subtree(conn, dict(c)) for c in children]
        return node

    def delete_decision(self, did: int) -> bool:
        conn = self._conn()
        try:
            # kaskadowo usuń dzieci
            conn.execute("DELETE FROM decisions WHERE parent_id=?", (did,))
            cur = conn.execute("DELETE FROM decisions WHERE id=?", (did,))
            conn.commit()
            return cur.rowcount > 0
        finally:
            conn.close()

    # ── Skill Registry ──
    def add_skill(self, name: str, title: str = "", category: str = "",
                  file_path: str = "", lines: int = 0, frequency: float = 0.0,
                  merge_group: str = "", orbital_ref: str = "", tags: list = None) -> dict:
        conn = self._conn()
        try:
            now = self._ts()
            tags_json = json.dumps(tags or [])
            conn.execute(
                """INSERT OR REPLACE INTO skill_registry
                   (name, title, category, file_path, lines, frequency, merge_group, orbital_ref, tags, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (name, title, category, file_path, lines, frequency, merge_group, orbital_ref, tags_json, now)
            )
            conn.commit()
            sid = conn.execute("SELECT id FROM skill_registry WHERE name=?", (name,)).fetchone()[0]
            return {"id": sid, "name": name, "category": category}
        finally:
            conn.close()

    def update_skill(self, sid: int, **kwargs) -> bool:
        conn = self._conn()
        try:
            allowed = {"title", "category", "frequency", "merge_group", "orbital_ref", "tags"}
            sets = []
            vals = []
            for k, v in kwargs.items():
                if k in allowed:
                    sets.append(f"{k}=?")
                    vals.append(json.dumps(v) if k == "tags" else v)
            if not sets:
                return False
            cur = conn.execute(f"UPDATE skill_registry SET {', '.join(sets)} WHERE id=?", (*vals, sid))
            conn.commit()
            return cur.rowcount > 0
        finally:
            conn.close()

    def list_skills(self, category: str = "", merge_group: str = "", limit: int = 300) -> list:
        conn = self._conn()
        try:
            where = []
            vals = []
            if category:
                where.append("category=?")
                vals.append(category)
            if merge_group:
                where.append("merge_group=?")
                vals.append(merge_group)
            q = "SELECT * FROM skill_registry"
            if where:
                q += " WHERE " + " AND ".join(where)
            q += " ORDER BY category ASC, name ASC LIMIT ?"
            vals.append(limit)
            rows = conn.execute(q, vals).fetchall()
            result = []
            for r in rows:
                d = dict(r)
                if isinstance(d.get("tags"), str) and d["tags"].strip():
                    try:
                        d["tags"] = json.loads(d["tags"])
                    except json.JSONDecodeError:
                        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/taskplan_db.py:621 quiet except scope=TaskPlanDB.list_skills reason=assign_fallback")
                        d["tags"] = [t.strip() for t in d["tags"].split(",") if t.strip()]
                result.append(d)
            return result
        finally:
            conn.close()

    def get_skill_stats(self) -> dict:
        conn = self._conn()
        try:
            total = conn.execute("SELECT COUNT(*) FROM skill_registry").fetchone()[0]
            cats = conn.execute(
                "SELECT category, COUNT(*) as cnt FROM skill_registry GROUP BY category ORDER BY cnt DESC"
            ).fetchall()
            merged = conn.execute(
                "SELECT merge_group, COUNT(*) as cnt FROM skill_registry WHERE merge_group!='' GROUP BY merge_group ORDER BY cnt DESC"
            ).fetchall()
            return {
                "total": total,
                "categories": [{"name": r["category"], "count": r["cnt"]} for r in cats],
                "merge_groups": [{"group": r["merge_group"], "count": r["cnt"]} for r in merged],
            }
        finally:
            conn.close()

    # ── Decision ↔ Skills mapping ──
    def map_skill_to_decision(self, decision_id: int, skill_id: int,
                              role: str = "tool", weight: float = 1.0) -> dict:
        conn = self._conn()
        try:
            now = self._ts()
            conn.execute(
                """INSERT OR REPLACE INTO decision_skills (decision_id, skill_id, role, weight, created_at)
                   VALUES (?, ?, ?, ?, ?)""",
                (decision_id, skill_id, role, weight, now)
            )
            conn.commit()
            return {"decision_id": decision_id, "skill_id": skill_id, "role": role}
        finally:
            conn.close()

    def get_skills_for_decision(self, decision_id: int) -> list:
        conn = self._conn()
        try:
            rows = conn.execute(
                """SELECT s.*, ds.role, ds.weight
                   FROM decision_skills ds
                   JOIN skill_registry s ON s.id = ds.skill_id
                   WHERE ds.decision_id=?
                   ORDER BY ds.weight DESC""",
                (decision_id,)
            ).fetchall()
            result = []
            for r in rows:
                d = dict(r)
                if isinstance(d.get("tags"), str) and d["tags"].strip():
                    try:
                        d["tags"] = json.loads(d["tags"])
                    except json.JSONDecodeError:
                        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/taskplan_db.py:679 quiet except scope=TaskPlanDB.get_skills_for_decision reason=assign_fallback")
                        d["tags"] = [t.strip() for t in d["tags"].split(",") if t.strip()]
                result.append(d)
            return result
        finally:
            conn.close()

    def get_decisions_for_skill(self, skill_id: int) -> list:
        conn = self._conn()
        try:
            rows = conn.execute(
                """SELECT d.*, ds.role, ds.weight
                   FROM decision_skills ds
                   JOIN decisions d ON d.id = ds.decision_id
                   WHERE ds.skill_id=?
                   ORDER BY d.lp ASC""",
                (skill_id,)
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    # ── Stats ──
    def stats(self) -> dict:
        conn = self._conn()
        try:
            tasks_total = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
            tasks_pending = conn.execute("SELECT COUNT(*) FROM tasks WHERE status='pending'").fetchone()[0]
            tasks_progress = conn.execute("SELECT COUNT(*) FROM tasks WHERE status='in_progress'").fetchone()[0]
            tasks_done = conn.execute("SELECT COUNT(*) FROM tasks WHERE status='completed'").fetchone()[0]
            plans_total = conn.execute("SELECT COUNT(*) FROM plans").fetchone()[0]
            plans_active = conn.execute("SELECT COUNT(*) FROM plans WHERE status='active'").fetchone()[0]
            lessons_total = conn.execute("SELECT COUNT(*) FROM lessons").fetchone()[0]
            last = conn.execute("SELECT value FROM registry WHERE key='last_update'").fetchone()
            return {
                "tasks": {"total": tasks_total, "pending": tasks_pending,
                          "in_progress": tasks_progress, "completed": tasks_done},
                "plans": {"total": plans_total, "active": plans_active},
                "lessons": {"total": lessons_total},
                "last_update": last["value"] if last else "",
            }
        finally:
            conn.close()


# ── CLI quick test ──
if __name__ == "__main__":
    db = TaskPlanDB()
    print("Stats:", db.stats())
