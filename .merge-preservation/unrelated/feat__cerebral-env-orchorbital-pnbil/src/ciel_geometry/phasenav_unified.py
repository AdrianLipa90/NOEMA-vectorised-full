"""UnifiedPhaseNavIndex — jeden indeks, wszystkie źródła NOEMA + Linux.

Łączy w jednej 24D przestrzeni fazowej:
  - skill_index         (skilli PhaseNav 24D)
  - knowledge_db        (15 tabel z noema_knowledge.db)
  - palace_rooms        (snapshoty MemoryPalace)
  - linux_cards         (560+ kart live: CPU, PROC, NET, DISK, SENSOR…)

Każdy wpis ma source_type + source_table.
Szukaj przez 24D angular similarity w jednym indeksie.
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import math
import re
import sqlite3
import hashlib
from pathlib import Path
from typing import Any

import numpy as np

from ciel_geometry.paths import P

PHASE_INDEX_DIR = Path(P.LIBRARY) / "PHASE_INDEX"
# Was pointed at NOEMA_LIBRARY/INDEX/noema_knowledge.db — a third, stale
# (872KB, last touched 2026-06-29) knowledge DB snapshot disconnected
# from the actively-used one. Aligned to the same canonical persistent
# store as everywhere else (fixed 2026-07-08).
KNOWLEDGE_DB = Path(P.DB.KNOWLEDGE)
ROOMS_DB = Path(P.LIBRARY) / "memory_palace" / "rooms.db"
LINUX_CARDS_DIR = Path("/dev/shm/ciel_noema/linux_cards")
N_OSCILLATORS = 24

STOP_WORDS = {
    "this", "that", "with", "from", "have", "been", "will", "they",
    "there", "which", "their", "what", "when", "where", "than", "them",
    "also", "into", "over", "then", "each", "about", "would", "could",
    "should", "other", "more", "some", "these", "those",
}


class UnifiedPhaseNavIndex:
    """Jeden indeks PhaseNav dla wszystkiego."""

    def __init__(self):
        self.vectors: np.ndarray | None = None
        self.meta: list[dict] = []
        self.source_counts: dict[str, int] = {}
        self._build()

    # ── building ──────────────────────────────────────────────────────────

    def _build(self) -> None:
        self.vectors = None
        self.meta = []
        self._load_skills()
        self._load_knowledge_db()
        self._load_palace_rooms()
        self._load_linux_cards()
        self._load_taskplan_db()
        self._load_task_queue()
        self._load_system_map()

    def _add(self, vec: np.ndarray, meta: dict) -> None:
        vec_flat = vec.ravel().astype(np.float64)
        if self.vectors is None:
            self.vectors = vec_flat.reshape(1, N_OSCILLATORS)
        else:
            self.vectors = np.vstack([self.vectors, vec_flat])
        self.meta.append(meta)
        st = meta.get("source_type", "unknown")
        self.source_counts[st] = self.source_counts.get(st, 0) + 1

    def _load_skills(self) -> None:
        vec_file = PHASE_INDEX_DIR / "skill_index.npy"
        meta_file = PHASE_INDEX_DIR / "skill_meta.npy"
        if not vec_file.exists():
            return
        vecs = np.load(str(vec_file)).astype(np.float64)
        raw_meta = []
        if meta_file.exists():
            raw = np.load(str(meta_file), allow_pickle=True)
            raw_meta = list(raw) if raw.ndim == 0 else raw.tolist()
        for i in range(len(vecs)):
            m = raw_meta[i] if i < len(raw_meta) else {}
            self._add(vecs[i], {
                "source_type": "skill",
                "name": m.get("name", f"skill_{i}"),
                "priority": m.get("priority", 3),
                "dir": m.get("dir", ""),
                "description": m.get("description", ""),
            })

    def _load_knowledge_db(self) -> None:
        """Wczytaj wszystkie tabelki noema_knowledge.db jako 24D wektory."""
        if not KNOWLEDGE_DB.exists():
            return
        try:
            conn = sqlite3.connect(str(KNOWLEDGE_DB))
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/phasenav_unified.py:97 quiet except scope=UnifiedPhaseNavIndex._load_knowledge_db reason=return None")
            return

        # corpus_structure → sekcje dokumentów
        try:
            rows = conn.execute(
                "SELECT category, file_count FROM corpus_structure"
            ).fetchall()
            for name, cnt in rows:
                if cnt and cnt > 3:
                    self._add(self._text_to_phi(name), {
                        "source_type": "corpus_section",
                        "name": name,
                        "doc_count": cnt,
                    })
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/phasenav_unified.py:112 quiet except scope=UnifiedPhaseNavIndex._load_knowledge_db reason=pass")
            pass

        # corpus_topics → tematy
        try:
            rows = conn.execute(
                "SELECT topic, doc_count FROM corpus_topics"
            ).fetchall()
            for name, cnt in rows:
                self._add(self._text_to_phi(name), {
                    "source_type": "topic",
                    "name": name,
                    "doc_count": cnt or 0,
                })
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/phasenav_unified.py:126 quiet except scope=UnifiedPhaseNavIndex._load_knowledge_db reason=pass")
            pass

        # daemons → nazwy demonów
        try:
            rows = conn.execute("SELECT name FROM daemons").fetchall()
            for (name,) in rows:
                self._add(self._text_to_phi(name), {
                    "source_type": "daemon",
                    "name": name,
                })
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/phasenav_unified.py:137 quiet except scope=UnifiedPhaseNavIndex._load_knowledge_db reason=pass")
            pass

        # system_map → nazwy sekcji + skrócone treści
        try:
            rows = conn.execute(
                "SELECT section, content FROM system_map LIMIT 100"
            ).fetchall()
            for section, content in rows:
                    vec = self._text_to_phi(section + " " + (content or "")[:500])
                    self._add(vec, {
                        "source_type": "system_meta",
                        "name": section,
                    })
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/phasenav_unified.py:151 quiet except scope=UnifiedPhaseNavIndex._load_knowledge_db reason=pass")
            pass

        # code_files → nazwy plików
        try:
            rows = conn.execute(
                "SELECT filepath, lines FROM code_files ORDER BY lines DESC LIMIT 200"
            ).fetchall()
            for filepath, lines in rows:
                name = filepath.split("/")[-1] if "/" in filepath else filepath
                self._add(self._text_to_phi(name), {
                    "source_type": "code_file",
                    "name": name,
                    "lines": lines,
                })
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/phasenav_unified.py:166 quiet except scope=UnifiedPhaseNavIndex._load_knowledge_db reason=pass")
            pass

        # live_state → nazwy pól
        try:
            row = conn.execute(
                "SELECT * FROM live_state ORDER BY rowid DESC LIMIT 1"
            ).fetchone()
            if row:
                desc = conn.execute("PRAGMA table_info(live_state)").fetchall()
                col_names = [c[1] for c in desc]
                all_text = " ".join(
                    f"{col_names[i]}={row[i]}" for i in range(len(row))
                )
                vec = self._text_to_phi(all_text)
                self._add(vec, {
                    "source_type": "live_state",
                    "name": "live_state snapshot",
                })
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/phasenav_unified.py:185 quiet except scope=UnifiedPhaseNavIndex._load_knowledge_db reason=pass")
            pass

        # pozostałe tabele z pojedynczymi kolumnami tekstowymi
        for tbl in ["corpus_key_claims", "system_fixes",
                     "temporal_observations", "formal_proofs",
                     "publication_claims", "corpus_audit"]:
            try:
                info = conn.execute(f"PRAGMA table_info({tbl})").fetchall()
                text_cols = [c[1] for c in info
                             if c[2] in ("TEXT",) and c[1] != "timestamp"]
                if text_cols:
                    col = text_cols[0]
                    rows = conn.execute(
                        f"SELECT DISTINCT {col} FROM {tbl} LIMIT 50"
                    ).fetchall()
                    for (val,) in rows:
                        if val and len(str(val)) > 2:
                            self._add(self._text_to_phi(str(val)), {
                                "source_type": tbl,
                                "name": str(val)[:80],
                            })
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/phasenav_unified.py:207 quiet except scope=UnifiedPhaseNavIndex._load_knowledge_db reason=pass")
                pass

        conn.close()

    def _load_palace_rooms(self) -> None:
        """Zakoduj snapshoty MemoryPalace."""
        if not ROOMS_DB.exists():
            return
        try:
            conn = sqlite3.connect(str(ROOMS_DB))
            rows = conn.execute(
                "SELECT id, tick, R, coherence, gamma, note, created_at "
                "FROM rooms ORDER BY id DESC LIMIT 200"
            ).fetchall()
            conn.close()
            for rid, tick, R, coh, gamma, note, ts in rows:
                # reprezentacja snapshota: [R, coh, gamma, ...] + hash notatki
                vec = np.zeros(N_OSCILLATORS, dtype=np.float64)
                vec[0] = R * 2 * math.pi / N_OSCILLATORS if R else 0
                vec[1] = coh * 2 * math.pi if coh else 0
                vec[2] = (gamma / 10.0) * 2 * math.pi if gamma else 0
                if note:
                    note_vec = self._text_to_phi(note)
                    vec = (vec + note_vec) / 2
                self._add(vec, {
                    "source_type": "memory",
                    "name": f"snapshot_{rid}",
                    "palace_id": rid,
                    "tick": tick,
                    "R": R,
                    "coherence": coh,
                    "gamma": gamma,
                    "note": (note or "")[:128],
                    "timestamp": ts,
                })
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/phasenav_unified.py:243 quiet except scope=UnifiedPhaseNavIndex._load_palace_rooms reason=pass")
            pass

    def _load_linux_cards(self) -> None:
        """Wczytaj live Linux karty z JSONL."""
        cards_file = LINUX_CARDS_DIR / "cards.jsonl"
        if not cards_file.exists():
            return
        try:
            cards_file = LINUX_CARDS_DIR / "cards.jsonl"
            with open(str(cards_file)) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        card = json.loads(line)
                    except json.JSONDecodeError:
                        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/phasenav_unified.py:260 quiet except scope=UnifiedPhaseNavIndex._load_linux_cards reason=continue")
                        continue
                    ctype = card.get("type", "?")
                    name = card.get("name", "?")
                    # zbuduj tekst opisowy karty
                    desc = f"{ctype} {name}"
                    for key in ("label", "device", "state", "proto",
                                 "proc_name", "filesystem", "model",
                                 "vendor", "driver", "temp_input"):
                        val = card.get(key)
                        if val:
                            desc += f" {val}"
                    # kluczowe wartości numeryczne jako słowa
                    for num_key in ("busy_pct", "freq_mhz", "rxtx_mbps",
                                     "used_pct", "rx_bytes", "cpu",
                                     "memory_mb", "temp_input",
                                     "curr_input", "in_input"):
                        val = card.get(num_key)
                        if val:
                            desc += f" {num_key}={val}"
                    vec = self._text_to_phi(desc)
                    self._add(vec, {
                        "source_type": "linux_card",
                        "card_type": ctype,
                        "name": f"{ctype}/{name}",
                        "card_id": card.get("card_id", ""),
                        "label": card.get("label", ""),
                    })
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/phasenav_unified.py:288 quiet except scope=UnifiedPhaseNavIndex._load_linux_cards reason=pass")
            pass

    def _load_taskplan_db(self) -> None:
        """Wczytaj TaskPlan DB — tasks, plans, lessons, decisions, skill_registry."""
        tp_path = Path(P.DB.TASKPLAN)
        if not tp_path.exists():
            return
        try:
            conn = sqlite3.connect(str(tp_path))
            # skill_registry: 296+ skilli z kategoriami
            try:
                rows = conn.execute(
                    "SELECT name, category, merge_group, frequency, description "
                    "FROM skill_registry LIMIT 500"
                ).fetchall()
                for name, cat, mg, freq, desc in rows:
                    text = f"{name} {cat} {mg or ''} {desc or ''}"
                    self._add(self._text_to_phi(text), {
                        "source_type": "skill_registry",
                        "name": name,
                        "category": cat or "",
                        "merge_group": mg or "",
                        "frequency": freq or 0,
                    })
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/phasenav_unified.py:313 quiet except scope=UnifiedPhaseNavIndex._load_taskplan_db reason=pass")
                pass
            # decisions: drzewo decyzyjne
            try:
                rows = conn.execute(
                    "SELECT lp, title, decision_type, status, parent_id "
                    "FROM decisions ORDER BY lp"
                ).fetchall()
                for lp, title, dtype, status, parent in rows:
                    self._add(self._text_to_phi(f"{lp} {title} {dtype} {status}"), {
                        "source_type": "decision",
                        "name": f"{lp}: {title}",
                        "lp": lp,
                        "decision_type": dtype,
                        "status": status,
                        "parent_id": parent or "",
                    })
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/phasenav_unified.py:330 quiet except scope=UnifiedPhaseNavIndex._load_taskplan_db reason=pass")
                pass
            # tasks: taski z priorytetami
            try:
                rows = conn.execute(
                    "SELECT lp, title, priority, status, category "
                    "FROM tasks ORDER BY priority, status LIMIT 100"
                ).fetchall()
                for lp, title, prio, status, cat in rows:
                    self._add(self._text_to_phi(f"{title} {cat or ''} {status}"), {
                        "source_type": "task",
                        "name": f"{lp}: {title}",
                        "lp": lp,
                        "priority": prio or "medium",
                        "status": status,
                        "category": cat or "",
                    })
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/phasenav_unified.py:347 quiet except scope=UnifiedPhaseNavIndex._load_taskplan_db reason=pass")
                pass
            # lessons
            try:
                rows = conn.execute(
                    "SELECT lp, title, category FROM lessons ORDER BY lp"
                ).fetchall()
                for lp, title, cat in rows:
                    self._add(self._text_to_phi(f"{lp} {title} {cat or ''}"), {
                        "source_type": "lesson",
                        "name": f"{lp}: {title}",
                        "category": cat or "",
                    })
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/phasenav_unified.py:360 quiet except scope=UnifiedPhaseNavIndex._load_taskplan_db reason=pass")
                pass
            conn.close()
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/phasenav_unified.py:363 quiet except scope=UnifiedPhaseNavIndex._load_taskplan_db reason=pass")
            pass

    def _load_task_queue(self) -> None:
        """Wczytaj task_queue.noema.json — dynamiczne TODO."""
        tq_path = Path(__file__).resolve().parent.parent.parent / "NOEMA" / "task_queue.noema.json"
        if not tq_path.exists():
            return
        try:
            data = json.loads(tq_path.read_text(encoding="utf-8"))
            for item in data.get("queue", []):
                task = item.get("task", "")
                status = item.get("status", "pending")
                priority = item.get("priority", "normal")
                source = item.get("source", "")
                notes = item.get("notes", "")
                text = f"{task} {priority} {status} {source} {notes}"
                self._add(self._text_to_phi(text), {
                    "source_type": "task_queue",
                    "name": str(item.get("id", "")),
                    "task": task[:120],
                    "status": status,
                    "priority": priority,
                    "source": source,
                })
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/phasenav_unified.py:388 quiet except scope=UnifiedPhaseNavIndex._load_task_queue reason=pass")
            pass

    def _load_system_map(self) -> None:
        """Wczytaj system_map_v2.json — orbitalna mapa systemu."""
        sm_path = Path(__file__).resolve().parent.parent.parent / "system_map_v2.json"
        if not sm_path.exists():
            return
        try:
            data = json.loads(sm_path.read_text(encoding="utf-8"))
            for sys_entry in data.get("systems", []):
                name = sys_entry.get("name", "")
                ordinal = sys_entry.get("ordinal", "")
                layer = sys_entry.get("layer", "")
                desc = sys_entry.get("description", "")
                text = f"{ordinal} {name} {layer} {desc}"
                self._add(self._text_to_phi(text), {
                    "source_type": "system_map",
                    "name": f"{ordinal}: {name}",
                    "ordinal": ordinal,
                    "layer": layer,
                    "status": sys_entry.get("status", ""),
                })
            # connections jako osobne wpisy
            for conn_entry in data.get("connections", []):
                src = conn_entry.get("source", "")
                tgt = conn_entry.get("target", "")
                wij = conn_entry.get("W_ij", 0)
                text = f"connection {src} {tgt} weight {wij}"
                self._add(self._text_to_phi(text), {
                    "source_type": "system_connection",
                    "name": f"{src} → {tgt}",
                    "source": src,
                    "target": tgt,
                    "weight": wij,
                })
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/phasenav_unified.py:424 quiet except scope=UnifiedPhaseNavIndex._load_system_map reason=pass")
            pass

    # ── encoding ──────────────────────────────────────────────────────────

    @staticmethod
    def _text_to_phi(text: str) -> np.ndarray:
        """Tekst → 24D wektor fazy. Każde słowo → π/4 na 3 pozycjach."""
        words = re.findall(r'[a-zA-Z]{4,}', text.lower())
        words = [w for w in words if w not in STOP_WORDS]
        if not words:
            return np.zeros(N_OSCILLATORS, dtype=np.float64)
        phi = np.zeros(N_OSCILLATORS, dtype=np.float64)
        for w in set(words):
            h = hashlib.sha256(w.encode()).hexdigest()
            for offset in (0, 6, 12):
                idx = int(h[offset:offset+8], 16) % N_OSCILLATORS
                phi[idx] += math.pi / 4
        # normalize by unique word count to keep scale
        return phi

    @staticmethod
    def _angular_sim(vecs: np.ndarray, q: np.ndarray) -> np.ndarray:
        """Średnia angularna tylko po query-aktywnych wymiarach."""
        q_active = np.abs(q) > 1e-10
        if not q_active.any():
            return np.zeros(len(vecs))
        cos_vals = np.cos(vecs[:, q_active] - q[q_active])
        return cos_vals.mean(axis=1)

    # ── unified search ───────────────────────────────────────────────────

    @property
    def count(self) -> int:
        return len(self.meta) if self.vectors is not None else 0

    def search(self, query: str, top_n: int = 10,
               source_filter: str | None = None,
               min_similarity: float = 0.05,
               include_linux_cards: bool = True) -> list[dict]:
        """Szukaj we wszystkich źródłach. Linux karty przez structured match."""
        results = []

        # Decide if query is technical (include linux cards in PhaseNav)
        q_lower = query.lower()
        sys_triggers = {"proces", "cpu", "dysk", "disk", "sensor",
                        "network", "pci", "mount", "usb", "pcie",
                        "kernel", "temperatura", "temp"}
        is_technical = bool(set(q_lower.split()) & sys_triggers)

        # PhaseNav semantic search (skills, knowledge, memories)
        if self.vectors is not None and len(self.vectors) > 0:
            q = self._text_to_phi(query)
            if q.any():
                cos_sim = self._angular_sim(self.vectors, q)
                best = np.argsort(-cos_sim)
                for idx in best:
                    if cos_sim[idx] < min_similarity:
                        continue
                    m = self.meta[idx]
                    if source_filter and m.get("source_type") != source_filter:
                        continue
                    st = m.get("source_type", "")
                    # pomiń karty Linux w nietechnicznych zapytaniach
                    if st == "linux_card" and not is_technical:
                        continue
                    if not include_linux_cards and st == "linux_card":
                        continue
                    results.append({
                        "source_type": st,
                        "name": m.get("name", ""),
                        "similarity": round(float(cos_sim[idx]), 4),
                        **{k: v for k, v in m.items()
                           if k not in ("source_type", "name")},
                    })
                    if len(results) >= top_n:
                        break

        # Structured Linux card search — tylko dla technicznych zapytań
        if include_linux_cards and is_technical and (not source_filter or source_filter == "linux_card"):
            card_matches = self._search_linux_cards_structured(query, top_n)
            if card_matches:
                existing_names = {r["name"] for r in results}
                for cm in card_matches:
                    if cm["name"] not in existing_names:
                        results.insert(0, cm)
                        existing_names.add(cm["name"])

        return results[:top_n]

    def _search_linux_cards_structured(self, query: str, top_n: int) -> list[dict]:
        """Dopasuj Linux karty po typie + nazwie + polach."""
        if not LINUX_CARDS_DIR.exists():
            return []
        cards_file = LINUX_CARDS_DIR / "cards.jsonl"
        if not cards_file.exists():
            return []
        q = query.lower()
        q_words = set(re.findall(r'[a-zA-Z0-9]{3,}', q))
        results = []
        try:
            with open(str(cards_file)) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        card = json.loads(line)
                    except json.JSONDecodeError:
                        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/phasenav_unified.py:532 quiet except scope=UnifiedPhaseNavIndex._search_linux_cards_structured reason=continue")
                        continue
                    score = 0.0
                    ctype = (card.get("type") or "").lower()
                    cname = (card.get("name") or "").lower()
                    clabel = (card.get("label") or "").lower()
                    cproc = (card.get("proc_name") or "").lower()
                    cdevice = (card.get("device") or "").lower()
                    cstate = (card.get("state") or "").lower()

                    # full text dla multi-word match
                    card_text = f"{ctype} {cname} {clabel} {cproc} {cdevice} {cstate}"

                    # match typu
                    type_score = 0
                    if ctype in q_words or any(w in ctype for w in q_words if len(w) > 3):
                        type_score = 0.3

                    # Polish→English aliases
                    pl_map = {
                        "proces": {"process", "proc", "worker"},
                        "dysk": {"disk", "sd", "nvme"},
                        "temperatura": {"temp", "thermal", "coretemp"},
                        "siec": {"network", "net", "tcp", "udp"},
                        "urzadzenie": {"device", "pci"},
                        "pamiec": {"memory", "mem"},
                        "module": {"module", "driver", "ko"},
                    }
                    # match nazwy/procesu (z aliasingiem PL→EN)
                    name_score = 0
                    for w in q_words:
                        if len(w) < 3:
                            continue
                        variants = {w} | pl_map.get(w, set())
                        if any(v in cname or v in clabel or v in cproc for v in variants):
                            name_score = max(name_score, 0.5)

                    # exact match
                    exact_score = 0
                    for field in (cname, clabel, cproc, cdevice):
                        if q in field:
                            exact_score = 0.8
                            break

                    text_score = len([w for w in q_words if w in card_text]) / max(len(q_words), 1) * 0.3

                    # multi-word all-match boost: dla "proces firefox" szukaj procesów z "firefox"
                    all_match_score = 0
                    meaningful = [w for w in q_words if len(w) > 3 and w not in
                                  {"this", "that", "with", "from", "proces", "device"}]
                    if len(meaningful) >= 2:
                        all_present = all(
                            w in card_text for w in meaningful
                        )
                        if all_present:
                            all_match_score = 0.9

                    score = min(1.0, type_score + name_score + text_score)
                    if all_match_score > 0:
                        score = max(score, all_match_score)
                    if exact_score > 0:
                        score = max(score, exact_score)
                    if score > 0:
                        meta = {
                            "source_type": "linux_card",
                            "name": f"{card.get('type','?')}/{cname}",
                            "similarity": round(score, 4),
                            "card_id": card.get("card_id", ""),
                            "card_type": card.get("type", ""),
                        }
                        # dodaj kluczowe pola
                        for k in ("busy_pct", "freq_mhz", "used_pct",
                                   "rx_bytes", "tx_bytes", "state",
                                   "temp_input", "cpu"):
                            v = card.get(k)
                            if v is not None:
                                meta[k] = v
                        results.append(meta)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/phasenav_unified.py:610 quiet except scope=UnifiedPhaseNavIndex._search_linux_cards_structured reason=pass")
            pass
        results.sort(key=lambda x: -x["similarity"])
        return results[:top_n]

    def search_by_phi(self, query_phi: np.ndarray, top_n: int = 10,
                       source_filter: str | None = None) -> list[dict]:
        """Szukaj wektor→wektor (maskowana angularna)."""
        if self.vectors is None or len(self.vectors) == 0:
            return []
        if query_phi.size != N_OSCILLATORS:
            return []
        q = query_phi.ravel()
        if not q.any():
            return []
        cos_sim = self._angular_sim(self.vectors, q)
        best = np.argsort(-cos_sim)[:top_n]
        results = []
        for idx in best:
            m = self.meta[idx]
            if source_filter and m.get("source_type") != source_filter:
                continue
            results.append({
                "source_type": m.get("source_type", "unknown"),
                "name": m.get("name", ""),
                "similarity": round(float(cos_sim[idx]), 4),
            })
        return results

    def filter_by_source(self, source_type: str) -> list[dict]:
        """Filtruj wpisy po typie źródła."""
        return [
            {"name": self.meta[i].get("name", ""), "idx": i}
            for i in range(len(self.meta))
            if self.meta[i].get("source_type") == source_type
        ]

    def _log_stats(self) -> None:
        total = self.count
        if total == 0:
            return

    def stats(self) -> dict:
        return {
            "total": self.count,
            "by_source": dict(self.source_counts),
            "sources": list(self.source_counts.keys()),
        }

    def rebuild(self) -> None:
        """Przebuduj cały indeks od zera."""
        self._build()


# ── standalone ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    u = UnifiedPhaseNavIndex()
    print(f"Unified PhaseNav: {u.count} entries")
    print(f"  by source: {u.source_counts}")
    print()
    for q in ["memory palace", "kuramoto phase", "testy python", "consciousness"]:
        print(f"--- '{q}' ---")
        for r in u.search(q, top_n=3):
            print(f"  [{r['source_type']:8s}] sim={r['similarity']:.4f}  {r['name'][:60]}")
        print()
