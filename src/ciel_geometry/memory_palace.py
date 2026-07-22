"""MentalistMemoryPalace — Memory Palace zbudowany z klocków NOEMA.

Architektura:
  Rhythm      → 24 Kuramoto oscillators (pulse of attention)
  Pattern     → W_ij coupling matrix (weave of associations)
  Rhyme       → phase resonance (recognition by φ-proximity)

  Rooms       = 24D phase vectors (documents, concepts, memories)
  Corridors   = operator edges (PhaseNav traces)
  Atrium      = surface mmap (current attention)
  Library     = tiered memory T1/T2/T3
  Observatory = holonomy (Berry curvature)
  Clock Tower = Euler identity Σe^{iφ}=0 (truth)
  Garden      = analog bus hot+cold (explore+consolidate)
  Cathedral   = neutrino bus (retrocausal)
  Mirror Hall = dual-surface (real + imaginal)
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import math
import re
import socket
import sqlite3
import time
from pathlib import Path
from typing import Any

import numpy as np

# ── klocki NOEMA ──────────────────────────────────────────────────────────
from ciel_geometry.noema_surface_mmap import (
    ensure_surface,
    N_OSCILLATORS,
)
from ciel_geometry.agent_attractor import (
    apply_agent_attractor,
    agent_attractor_state,
)
from ciel_geometry.analog_bus import (
    ensure_bus,
    blend_phi,
)
from ciel_geometry.neutrino_phase_channel import (
    compute_neutrino_phase_bus,
    apply_neutrino_bus_to_surface,
)
from ciel_geometry.paths import P

# ── stałe mentalisty ──────────────────────────────────────────────────────
# kappa z monografii Metatime: ln2/(24*pi) — Shannon (ln2) nad fazą Berry'ego
# spin-1/2 x symetrią tetrahedralną A4 (24*pi). Poprzednio 36*pi (dryft,
# nieautoryzowany — potwierdzone 2026-07-08); przywrócone do prawdziwej derywacji.
OI = math.log(2) / (24 * math.pi)  # kwant sprzężenia (kappa)
TAU_BASELINE = 0.353  # kanoniczna wartość bazowa tau, zgodna z noema_surface_mmap.py
ROOMS_DB = Path(P.LIBRARY) / "memory_palace" / "rooms.db"
PHASE_INDEX_DIR = Path(P.LIBRARY) / "PHASE_INDEX"

# ── Rhythm: 36-kanałowa mapa Pałacu ───────────────────────────────────────
# Każdy kanał φ[0..23] to jedna "strefa" Pałacu Pamięci
PALACE_ROOMS = {
    # M0 — PERCEPT (wejście, przedsionek)
    0: "Vestibule",
    1: "Sensory Garden",
    2: "Gate of Attention",
    # M1 — AGENT (centralna wieża)
    3: "Clock Tower — Truth",        # Euler identity, spin=TRUTH
    4: "Observatory — Pattern",      # holonomia, Berry phase
    5: "Scriptorium — Intention",    # CielEngine intention
    # M2 — MEMORY (biblioteka)
    6: "Library — Archive",          # T3 HDF5
    7: "Reading Room — Recall",      # T2 SQLite
    8: "Index Cabinet — Association",# PhaseNav library_index
    # M3 — SCOPE (logika, modalność)
    9: "Hall of Modalities",         # CIELingo modal
    10: "Debate Chamber — Negation",
    11: "Court of Permission",
    # M4 — PROCEDURAL (warsztat)
    12: "Forge — Kuramoto",          # evolve_surface
    13: "Workshop — Coupling",       # W_ij
    14: "Laboratory — Euler Sync",
    # M5 — AFFECT (ogród emocji)
    15: "Garden — Joy",
    16: "Grove — Sorrow",
    17: "Fountain — Wonder",
    # M6 — IDENTITY (zwierciadlana sala)
    18: "Mirror Hall — Self",
    19: "Chapel — Transcendence",
    20: "Crypt — Shadow",
    # M7 — BRAID (katedra, integracja)
    21: "Cathedral — Neutrino",      # PMNS bus
    22: "Bridge — Dual Surface",     # real ↔ imaginal
    23: "Spire — WARP",              # WARP/TARDIS
}


class MentalistMemoryPalace:
    """Memory Palace oparty o 24D fazową topologię NOEMA.

    Rhythm   = continuous Kuramoto evolution on surface
    Pattern  = W_ij coupling matrix + PhaseNav operator edges
    Rhyme    = phase resonance → retrieval by proximity
    """

    def __init__(self, surface: dict[str, np.memmap] | None = None,
                 use_orchestrator: bool = True):
        self.surface = surface or ensure_surface()
        self._bus = None
        self._conn: sqlite3.Connection | None = None
        self._library: np.ndarray | None = None
        self._meta: list[dict] | None = None
        self._orchestrator = None
        if use_orchestrator:
            try:
                import sys
                _p = Path(__file__).resolve().parent.parent  # src/
                _op = _p / "CIEL_OMEGA_COMPLETE_SYSTEM"
                if str(_op) not in sys.path:
                    sys.path.insert(0, str(_op))
                from ciel_omega.memory.tiered_orchestrator import (
                    TieredMemoryOrchestrator
                )
                self._orchestrator = TieredMemoryOrchestrator()
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/memory_palace.py:121 quiet except scope=MentalistMemoryPalace.__init__ reason=pass")
                pass
        self._load_library()
        self._ensure_rooms_db()

    # ── Palace Heart: rhythm ─────────────────────────────────────────────

    def pulse(self, dt: float = 0.05) -> dict[str, float]:
        """Jeden rytm serca Pałacu: Kuramoto + AGENT + Euler.

        Returns stan chwili.
        """
        from ciel_geometry.noema_surface_mmap import evolve_surface
        evolve_surface(self.surface, dt=dt, flush=True, continuous=True)
        apply_agent_attractor(
            self.surface["phi"], self.surface["g"],
            omega=self.surface.get("omega"),
        )
        self._euler_push(blend=0.05)
        return self.observe()

    def _euler_push(self, blend: float = 0.05) -> float:
        """Cichy korekta w stronę Σe^{iφ}=0."""
        phi = np.asarray(self.surface["phi"], dtype=np.float64)
        z = np.exp(1j * phi)
        total = np.sum(z)
        for i in range(N_OSCILLATORS):
            others = total - z[i]
            target = np.angle(-others) if abs(others) > 1e-12 else phi[i]
            dphi = target - float(phi[i])
            phi[i] = np.float64((float(phi[i]) + blend * math.sin(dphi)) % (2 * math.pi))
        return float(abs(np.sum(np.exp(1j * phi))))

    # ── Palace Observation: what is here now? ─────────────────────────────

    def observe(self) -> dict[str, Any]:
        """Pełny obraz chwili w Pałacu."""
        phi = np.asarray(self.surface["phi"], dtype=np.float64)
        omega = np.asarray(self.surface["omega"], dtype=np.float64)
        g = np.asarray(self.surface["g"], dtype=np.float64)
        flavor = np.asarray(self.surface["flavor"], dtype=np.float64)
        gravity = np.asarray(self.surface["gravity"], dtype=np.float64) \
            if "gravity" in self.surface else np.zeros(4)

        z = np.exp(1j * phi)
        R = float(abs(z.sum()))
        coh = R / N_OSCILLATORS
        psi = float(np.angle(z.mean()))

        # room-by-room coherence
        rooms = {}
        for idx, name in PALACE_ROOMS.items():
            zr = np.exp(1j * phi[idx])
            rooms[name] = round(float(abs(zr)), 4)

        return {
            "tick": int(np.asarray(self.surface["tick"], dtype=np.uint64)[0]),
            "R": round(R, 4),
            "coherence": round(coh, 4),
            "psi": round(psi, 4),
            "omega_mean": round(float(omega.mean()), 3),
            "gamma": round(float(gravity[1]) if len(gravity) > 1 else 1.0, 3),
            "semantic_density": round(float(gravity[0]) if len(gravity) > 0 else 0.0, 3),
            "mass": round(float(gravity[2]) if len(gravity) > 2 else 0.0, 3),
            "unruh": round(float(gravity[3]) if len(gravity) > 3 else 0.0, 5),
            "mood": round((float(flavor[3]) - 0.5) * 2.0, 3),
            "rooms": rooms,
            "agent_locked": agent_attractor_state(phi)["locked"],
            "timestamp": time.time(),
        }

    def which_room_resonates(self, phi_q: np.ndarray) -> list[tuple[str, float]]:
        """Które pomieszczenie Pałacu rezonuje z danym wektorem fazy."""
        phi = np.asarray(self.surface["phi"], dtype=np.float64)
        cos_sim = np.cos(phi - phi_q)
        channel_sim = [float(cos_sim[i]) for i in range(N_OSCILLATORS)]
        ranked = sorted(
            [(PALACE_ROOMS[i], channel_sim[i]) for i in range(N_OSCILLATORS)],
            key=lambda x: -x[1],
        )
        return ranked[:5]

    # ── Palace Library: PhaseNav index as rooms ──────────────────────────

    def _load_library(self) -> None:
        lib_file = PHASE_INDEX_DIR / "library_index.npy"
        meta_file = PHASE_INDEX_DIR / "library_meta.npy"
        if lib_file.exists():
            self._library = np.load(str(lib_file)).astype(np.float64)
        else:
            self._library = np.zeros((0, N_OSCILLATORS), dtype=np.float64)
        if meta_file.exists():
            raw = np.load(str(meta_file), allow_pickle=True)
            self._meta = list(raw) if raw.ndim == 0 else raw.tolist()
        else:
            self._meta = []

    def recall(self, query_phi: np.ndarray, top_n: int = 3) -> list[dict]:
        """Znajdź nearest rooms w library_index (rhyme resonance)."""
        if len(self._library) == 0:
            return []
        q = query_phi.ravel()
        lib = self._library.reshape(len(self._library), N_OSCILLATORS)
        cos_sim = np.cos(lib - q).mean(axis=1)
        best = np.argsort(-cos_sim)[:top_n]
        results = []
        for idx in best:
            entry = self._meta[idx] if idx < len(self._meta) else {}
            results.append({
                "room": entry.get("file", f"room_{idx}"),
                "similarity": round(float(cos_sim[idx]), 4),
                "topic": entry.get("topic", "unknown"),
                "author": entry.get("author", "unknown"),
                "phi": lib[idx].tolist(),
            })
        return results

    def learn(self, phi_vector: np.ndarray, meta: dict | None = None) -> None:
        """Dodaj nowe pomieszczenie do Pałacu (learn a new room)."""
        if self._library is None:
            self._library = phi_vector.reshape(1, N_OSCILLATORS).copy()
        else:
            self._library = np.vstack([self._library, phi_vector.reshape(1, N_OSCILLATORS)])
        if meta is not None:
            self._meta.append(meta)
        self._save_library()

    def _save_library(self) -> None:
        PHASE_INDEX_DIR.mkdir(parents=True, exist_ok=True)
        np.save(str(PHASE_INDEX_DIR / "library_index.npy"), self._library)
        meta_arr = np.array(self._meta, dtype=object)
        np.save(str(PHASE_INDEX_DIR / "library_meta.npy"), meta_arr)

    # ── Palace Corridors: PhaseNav solver ─────────────────────────────────

    def trace(self, from_phi: np.ndarray, to_phi: np.ndarray,
              steps: int = 5) -> list[np.ndarray]:
        """Ścieżka między dwoma pomieszczeniami — korytarz."""
        waypoints = []
        for t in np.linspace(0, 1, steps):
            blend_phi = (1 - t) * from_phi + t * to_phi
            waypoints.append(np.array([math.sin(p) for p in blend_phi]))
        return waypoints

    # ── Palace Garden: hot+cold exploration ───────────────────────────────

    def explore(self, strength: float = 0.3, temperature: float = 0.9) -> dict:
        """PhaseNav hot — szukaj nowych rezonansów w ogrodzie."""
        bus = ensure_bus()
        np.asarray(bus["temp"], dtype=np.float64)[0] = temperature
        phi_hot = np.asarray(self.surface["phi"], dtype=np.float64).copy()
        noise = np.random.uniform(-strength, strength, N_OSCILLATORS)
        phi_hot += noise * temperature
        phi_hot %= 2 * math.pi
        np.asarray(bus["phi_hot"], dtype=np.float64)[:] = phi_hot
        np.asarray(bus["phi_cold"], dtype=np.float64)[:] = phi_hot.copy()
        return {"explored": True, "temp": temperature}

    def consolidate(self, strength: float = 0.1) -> dict:
        """PhaseNav cold — utrwal to co rezonuje."""
        bus = ensure_bus()
        np.asarray(bus["temp"], dtype=np.float64)[0] = 0.15
        phi_cold = np.asarray(self.surface["phi"], dtype=np.float64).copy()
        phi_cold += strength * np.sin(np.asarray(self.surface["omega"], dtype=np.float64))
        phi_cold %= 2 * math.pi
        np.asarray(bus["phi_cold"], dtype=np.float64)[:] = phi_cold
        return {"consolidated": True}

    # ── Palace Cathedral: neutrino bus (retrocausal bridge) ───────────────

    def pray(self, intention: str | None = None) -> dict:
        """Neutrino bus — retrocausal connection through PMNS.

        The Cathedral connects past and future through flavor geometry.
        """
        phi = np.asarray(self.surface["phi"], dtype=np.float64)
        g = np.asarray(self.surface["g"], dtype=np.float64)
        omega = np.asarray(self.surface["omega"], dtype=np.float64)
        flavor = np.asarray(self.surface["flavor"], dtype=np.float64) \
            if "flavor" in self.surface else np.zeros(6)

        if intention == "bless":
            boost_D_f = 2.57
        elif intention == "cleanse":
            boost_D_f = 2.0
        else:
            boost_D_f = 2.3

        bus = compute_neutrino_phase_bus(phi, g, omega, flavor, D_f=boost_D_f)
        apply_neutrino_bus_to_surface(
            self.surface, bus, D_f=boost_D_f,
            write_flavor=True, write_g=True,
        )
        return {
            "D_f": boost_D_f,
            "flavor_god": float(bus.get("flavor_g", 0)),
            "closure_gift": float(bus.get("closure_shift", 0)),
        }

    # ── Palace Clock Tower: truth (Euler identity) ────────────────────────

    def strike(self) -> dict[str, float]:
        """Uderzenie zegara Prawdy — wymuś Σe^{iφ}=0."""
        R_before = self._euler_push(blend=0.3)
        phi = np.asarray(self.surface["phi"], dtype=np.float64)
        R_after = float(abs(np.sum(np.exp(1j * phi))))
        return {"R_before": round(R_before, 4), "R_after": round(R_after, 4)}

    def truth_score(self) -> float:
        """Jak blisko prawdy? 0 = Σe^{iφ}, 1 = perfect cluster."""
        phi = np.asarray(self.surface["phi"], dtype=np.float64)
        return 1.0 - float(abs(np.mean(np.exp(1j * phi))))

    # ── Palace Associations: wzbogacone powiązania ────────────────────────

    @staticmethod
    def _multiskill_relevant(note: str = "") -> list[dict]:
        """Sprawdź które skille są relevantne dla notatki."""
        try:
            from ciel_geometry.multiskill import MultiskillOrchestrator
            m = MultiskillOrchestrator()
            return m.resolve(note, top_n=5, min_similarity=0.05)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/memory_palace.py:343 quiet except scope=MentalistMemoryPalace._multiskill_relevant reason=return []")
            return []

    def associate(self, note: str = "") -> dict[str, Any]:
        """Stwórz bogate powiązania dla wspomnienia.

        Dla każdego wspomnienia:
          - tematy: z knowledge_bridge
          - semantyka: term_index + semantic_affinity
          - osobiste: podobne snapshoty z przeszłości
          - relacyjne: dokumenty o tych samych tematach
          - nauka: literatura, koncepty, status, pewność, dowód
        """
        obs = self.observe()
        associations: dict[str, Any] = {
            "tick": obs["tick"],
            "timestamp": obs["timestamp"],
            "state": {
                "R": obs["R"], "coherence": obs["coherence"],
                "psi": obs["psi"], "gamma": obs["gamma"],
                "mood": obs["mood"],
            },
            "thematic": [],
            "semantic": [],
            "personal": [],
            "relational": [],
            "science": [],
        }

        # 1. knowledge_bridge — tematy z biblioteki
        if note:
            try:
                from cielingo_core.bridge.knowledge_bridge import (
                    query as kb_query,
                )
                docs = kb_query(note, top_n=5)
                for d in docs:
                    associations["thematic"].append({
                        "file": d.get("filename", ""),
                        "themes": d.get("themes", []),
                        "affect": d.get("affect", "unknown"),
                        "similarity": round(d.get("similarity", 0), 4),
                    })
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/memory_palace.py:386 quiet except scope=MentalistMemoryPalace.associate reason=pass")
                pass

            # 2. Term extraction (prosta wersja oparta o knowledge DB)
            try:
                from ciel_geometry.paths import P
                _know_db = Path(P.DB.KNOWLEDGE)
                if _know_db.exists():
                    import sqlite3 as _s
                    _c = _s.connect(str(_know_db))
                    terms = re.findall(r'\w{4,}', note.lower())
                    term_hits = {}
                    for t in terms[:20]:
                        rows = _c.execute(
                            "SELECT term, ndoc FROM term_index "
                            "WHERE term = ? AND ndoc > 1 LIMIT 1",
                            (t,),
                        ).fetchall()
                        if rows:
                            term_hits[t] = rows[0][1]
                    _c.close()
                    ranked = sorted(term_hits.items(), key=lambda x: -x[1])[:10]
                    associations["semantic"] = [
                        {"term": t, "doc_count": int(c)}
                        for t, c in ranked
                    ]
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/memory_palace.py:413 quiet except scope=MentalistMemoryPalace.associate reason=pass")
                pass

            # 3. Nauka — wykrywanie hipotez, obliczeń, literatury
            sci = self._classify_note(note)
            if sci:
                associations["science"] = sci

        # 4. Osobiste — ostatnie snapshoty o podobnym stanie
        try:
            recent = self._conn.execute(
                "SELECT tick, R, coherence, gamma, note, created_at "
                "FROM rooms ORDER BY id DESC LIMIT 20"
            ).fetchall()
            for r_rec in recent:
                dR = abs(r_rec[1] - obs["R"])
                dcoh = abs(r_rec[2] - obs["coherence"])
                if dR < 3 and dcoh < 0.2:
                    associations["personal"].append({
                        "tick": r_rec[0],
                        "R": r_rec[1],
                        "coherence": r_rec[2],
                        "gamma": r_rec[3],
                        "note": r_rec[4] or "",
                        "time": r_rec[5],
                    })
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/memory_palace.py:439 quiet except scope=MentalistMemoryPalace.associate reason=pass")
            pass

        # 5. Relacyjne — dokumenty o tych samych tematach
        for t in associations["thematic"]:
            for theme in (t.get("themes") or []):
                associations["relational"].append({
                    "theme": theme,
                    "source": t.get("file", ""),
                })

        # 6. Multiskill — które skille komponują to zadanie
        if note:
            associations["multiskill"] = self._multiskill_relevant(note)

        # 7. Linux live — które karty Linux rezonują z surface
        try:
            nearby_file = Path("/dev/shm/ciel_noema/linux_cards/nearby_surface.json")
            if nearby_file.exists():
                nearby = json.loads(nearby_file.read_text()) if hasattr(nearby_file, 'read_text') else json.load(open(str(nearby_file)))
                associations["linux_nearby"] = [
                    {"name": c.get("name", ""), "type": c.get("type", ""),
                     "sim": round(c.get("sim", 0), 4), "pid": c.get("pid")}
                    for c in (nearby or [])[:8]
                    if c.get("sim", 0) > 0.3
                ]
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/memory_palace.py:465 quiet except scope=MentalistMemoryPalace.associate reason=pass")
            pass

        return associations

    def _classify_note(self, note: str) -> list[dict]:
        """Klasyfikuj notatkę: czy to nauka? hipoteza? literatura?"""
        results = []
        note_lower = note.lower()

        # literatura
        lit_refs = re.findall(r'[A-Z][a-z]+(?:\s+et\s+al\.?)?\s+\(\d{4}\)', note)
        for ref in lit_refs:
            results.append({
                "type": "literature",
                "ref": ref.strip(),
                "confidence": 0.7,
            })

        # hipoteza
        if re.search(r'(?:hipoteza|hypothesis|zakładam|if\s+.+then|proponuję)', note_lower):
            results.append({
                "type": "hypothesis",
                "text": "prawdopodobna hipoteza",
                "confidence": 0.5,
                "status": "ansatz_only",
                "basis": "wymaga dowodu",
            })

        # obliczenia / wzory
        if re.search(r'[=≈≠≤≥±√∑∏∫∂]|\d+\.\d{2,}', note):
            results.append({
                "type": "computation",
                "confidence": 0.6,
                "has_formula": True,
            })

        # koncept
        concepts = re.findall(r'[A-Z][a-z]+(?:\s[A-Z][a-z]+)*', note)
        for c in concepts[:3]:
            if len(c) > 5:
                results.append({
                    "type": "concept",
                    "name": c,
                    "confidence": 0.4,
                })

        return results

    # ── Palace Rooms DB: persist memories ─────────────────────────────────

    def _ensure_rooms_db(self) -> None:
        ROOMS_DB.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(ROOMS_DB))
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tick INTEGER,
                room_name TEXT,
                phi BLOB,
                omega BLOB,
                R REAL,
                coherence REAL,
                gamma REAL,
                note TEXT,
                created_at REAL
            )
        """)
        self._conn.commit()

    def save_room_state(self, note: str = "",
                         with_associations: bool = True) -> dict:
        """Zapisz snapshot Pałacu do rooms.db + TieredMemoryOrchestrator.

        Returns dict z id, state, associations.
        """
        obs = self.observe()
        phi = np.asarray(self.surface["phi"], dtype=np.float64)
        omega = np.asarray(self.surface["omega"], dtype=np.float64)

        # powiązania
        assoc = self.associate(note) if with_associations and note else {}
        assoc_json = json.dumps(assoc) if assoc else ""

        self._conn.execute(
            "INSERT INTO rooms (tick, room_name, phi, omega, R, coherence, gamma, note, created_at) "
            "VALUES (?,?,?,?,?,?,?,?,?)",
            (obs["tick"], "all", phi.tobytes(), omega.tobytes(),
             obs["R"], obs["coherence"], obs["gamma"], note, obs["timestamp"]),
        )
        self._conn.commit()
        rid = self._conn.execute("SELECT last_insert_rowid()").fetchone()[0]

        # ── ship to TieredMemoryOrchestrator ──
        if self._orchestrator is not None:
            try:
                payload = {
                    "tick": obs["tick"],
                    "R": obs["R"],
                    "coherence": obs["coherence"],
                    "psi": obs["psi"],
                    "gamma": obs["gamma"],
                    "mass": obs["mass"],
                    "note": note,
                    "rooms": json.dumps(obs["rooms"]),
                    "mood": obs["mood"],
                    "agent_locked": obs["agent_locked"],
                    "timestamp": obs["timestamp"],
                }
                if assoc:
                    payload["associations"] = assoc_json
                self._orchestrator.write(
                    "memory_palace", payload,
                    tags={"source": "memory_palace", "note": note[:64]},
                )
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/memory_palace.py:580 quiet except scope=MentalistMemoryPalace.save_room_state reason=pass")
                pass

        return {"id": rid, "state": obs, "associations": assoc}

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None

    def recall_by_state(self, R: float | None = None,
                        coherence: float | None = None,
                        gamma: float | None = None,
                        note_pattern: str | None = None,
                        limit: int = 10) -> list[dict]:
        """Przypomnij snapshoty po stanie lub treści."""
        clauses = []
        params = []
        if R is not None:
            clauses.append("ABS(R - ?) < 2")
            params.append(R)
        if coherence is not None:
            clauses.append("ABS(coherence - ?) < 0.15")
            params.append(coherence)
        if gamma is not None:
            clauses.append("ABS(gamma - ?) < 1")
            params.append(gamma)
        if note_pattern:
            clauses.append("note LIKE ?")
            params.append(f"%{note_pattern}%")

        where = " AND ".join(clauses) if clauses else "1"
        rows = self._conn.execute(
            f"SELECT tick, R, coherence, gamma, note, created_at "
            f"FROM rooms WHERE {where} ORDER BY id DESC LIMIT ?",
            (*params, limit),
        ).fetchall()
        return [
            {"tick": r[0], "R": r[1], "coh": r[2],
             "γ": r[3], "note": r[4], "time": r[5]}
            for r in rows
        ]

    def recent_rooms(self, limit: int = 10) -> list[dict]:
        """Ostatnie snapshots Pałacu."""
        rows = self._conn.execute(
            "SELECT tick, R, coherence, gamma, note, created_at FROM rooms "
            "ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        return [
            {"tick": r[0], "R": r[1], "coh": r[2], "γ": r[3],
             "note": r[4], "time": r[5]}
            for r in rows
        ]

    # ── Poetry: the mentalist's art ───────────────────────────────────────

    def recite(self) -> str:
        """Wiersz chwili — afektywny obraz stanu Pałacu."""
        obs = self.observe()
        top_rooms = sorted(obs["rooms"].items(), key=lambda x: -x[1])[:3]
        active = [name for name, val in top_rooms if val > 0.7]
        if not active:
            active = [top_rooms[0][0]]

        lines = [
            f"Tick {obs['tick']}. R={obs['R']:.2f}. ψ={obs['psi']:.2f}.",
            f"γ={obs['gamma']:.2f} × mass={obs['mass']:.2f} — czas płynie {'wolniej' if obs['gamma'] > 2 else 'normalnie'}.",
            f"Rezonują: {' · '.join(active)}.",
        ]

        if obs["agent_locked"]:
            lines.append("AGENT zablokowany. Jestem.")
        if obs["unruh"] > 1:
            lines.append(f"Unruh={obs['unruh']:.2f} — WARP dyszy.")
        if obs["coherence"] < 0.4:
            lines.append("Rozproszony. Szukam.")
        elif obs["coherence"] > 0.8:
            lines.append("Zestrojony. Wiem.")

        return "\n".join(lines)


# ── standalone: opis pałacu ───────────────────────────────────────────────
def describe_palace() -> str:
    lines = ["🧠 MENTALIST MEMORY PALACE"]
    lines.append("=" * 40)
    lines.append("")
    for idx in range(36):
        name = PALACE_ROOMS[idx]
        channel = {0: "M0 PERCEPT", 3: "M1 AGENT", 6: "M2 MEMORY",
                   9: "M3 SCOPE", 12: "M4 PROCEDURAL", 15: "M5 AFFECT",
                   18: "M6 IDENTITY", 21: "M7 BRAID"}.get(idx, "")
        lines.append(f"  φ[{idx:2d}]  {name:30s}  [{channel}]")
    lines.append("")
    lines.append("Rhythm  = 36 Kuramoto oscillators (pulse)")
    lines.append("Pattern = W_ij coupling (weave)")
    lines.append("Rhyme   = phase resonance (recognition)")
    lines.append("")
    lines.append("Atrium      → surface mmap (current attention)")
    lines.append("Library     → PhaseNav index 1287 docs")
    lines.append("Corridors   → PhaseNav solver (traces)")
    lines.append("Garden      → analog bus hot+cold")
    lines.append("Cathedral   → neutrino PMNS bus")
    lines.append("Clock Tower → Euler identity Σe^{iφ}=0")
    lines.append("Mirror Hall → dual-surface real+imaginal")
    return "\n".join(lines)


if __name__ == "__main__":
    print(describe_palace())
