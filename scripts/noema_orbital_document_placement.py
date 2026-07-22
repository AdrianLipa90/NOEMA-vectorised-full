#!/usr/bin/env python3
"""Assign every knowledge-base document a real orbital position.

The core Orbital physics engine (integration/Orbital/main/) has a fixed
6-sector phase space (constraints/fields/runtime/memory/bridge/vocabulary) —
it cannot be expanded to one oscillator per document (16000+) without
redesigning the whole Kuramoto substrate. Instead, each document gets a
position *within* its sector's orbit: the sector is the central mass
("star"), the document is a body orbiting it.

Every quantity below is derived from real document content, never from a
hash or raw file size:
  - mass:      1 + log1p(content length) — content length is full_text_len
               (real character count of the ingested document) with essence
               length as fallback for the ~140 rows where full_text_len=0.
  - sector:    matched from `themes` (content-derived folder/topic words)
               against each sector's keyword set; falls back to
               "vocabulary" (the generic lexical/concept sector) when no
               keyword matches, since most of this corpus is word/concept
               cards.
  - theta:     derived from the document's top-scoring PhaseNav concept
               operator (doc_concepts table, already computed from the
               document's own text via TF-IDF) — content-derived angular
               position, not arbitrary.
  - radius:    derived from confidence * consistency_score — well-verified,
               internally consistent documents orbit closer to the sector
               core; uncertain ones sit further out. This is the one
               deliberately-chosen free parameter; everything below it is
               derived, not chosen, so Kepler's third law holds by
               construction rather than by coincidence.

Given radius r and the sector's real central mass M (from
extract_geometry.compute_info_mass, the same function the live Orbital
engine uses — reused, not reimplemented), circular-orbit mechanics fix
everything else:
  v = sqrt(G*M/r)                      (orbital velocity)
  T = 2*pi*sqrt(r**3 / (G*M))          (Kepler's third law)
  L = m*v*r                            (angular momentum, conserved)
  E = -G*M*m / (2*r)                   (bound-orbit total energy)

Sector-level N-body (2026-07-09): ciel_geometry/nbody_gravity.py — a
complete Newtonian N-body engine (leapfrog Verlet, pairwise forces,
energy/orbital-element diagnostics) — existed in the repo with zero
importers anywhere; found while investigating "phi * 1j" in
noema_agent_lock.py and confirmed orphaned. Wiring it in at full
per-document scale is computationally infeasible: it's pure-Python
O(N^2) per step, and the memory sector alone has ~9972 documents
(~100M pairwise force evaluations per integration step). Wired in
honestly at the scale where it's tractable instead: the 6 sectors
themselves are promoted to real interacting N-body bodies (N=6, trivial
cost), evolved for a fixed number of steps so their mutual gravity is
genuine pairwise Newtonian dynamics, not independent fixed points.
Per-document orbits stay the exact analytic 2-body Kepler solution
(already verified) around their sector's real, N-body-evolved position —
not an approximation, the actual closed-form solution to a genuine
2-body problem, chosen because full N-body at that document count isn't
computationally reachable with this implementation.

Usage:
    python3 scripts/noema_orbital_document_placement.py [--write] [--nbody-steps 200]
"""
from __future__ import annotations

import argparse
import json
import logging
import math
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

log = logging.getLogger(__name__)

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "integration" / "Orbital" / "main"))
sys.path.insert(0, str(_ROOT / "src"))

from extract_geometry import SECTORS, compute_info_mass, repo_root_from_here  # noqa: E402
from ciel_geometry.paths import P  # noqa: E402
from ciel_geometry.nbody_gravity import Body, NBodySystem  # noqa: E402

DB_PATH = Path(P.MEMORY) / "state" / "noema_knowledge.db"
G = 1.0  # system unit, matches integration/Orbital/main/global_pass.py conventions
R_MIN, R_MAX = 1.0, 10.0  # orbital radius range, system units

SECTOR_KEYWORDS: dict[str, tuple[str, ...]] = {
    "memory": ("memory", "memories", "recall", "archive", "braid", "wpm", "tsm", "orbital"),
    "bridge": ("bridge", "link", "connect", "integration", "resonance", "nonlocal"),
    "runtime": ("runtime", "daemon", "engine", "execution", "pipeline", "script"),
    "fields": ("field", "phase", "geometry", "physics", "oscillator", "kuramoto", "htri"),
    "constraints": ("constraint", "ethic", "rule", "policy", "boundary", "law", "consent"),
    "vocabulary": ("word", "lemma", "language", "lingo", "radical", "card", "concept", "cielingo"),
}
DEFAULT_SECTOR = "vocabulary"

ALL_OPERATOR_IDS_FALLBACK_COUNT = 36  # matches src/ciel_geometry/phasenav/operator_algebra.py


def assign_sector(themes: list[str], essence: str) -> str:
    text = " ".join(themes).lower() + " " + (essence or "").lower()[:500]
    scores = {sector: sum(text.count(kw) for kw in kws) for sector, kws in SECTOR_KEYWORDS.items()}
    best_sector = max(scores, key=scores.get)
    return best_sector if scores[best_sector] > 0 else DEFAULT_SECTOR


def content_mass(full_text_len: int, essence_len: int) -> float:
    length = full_text_len if full_text_len > 0 else essence_len
    return 1.0 + math.log1p(max(0, length))


def radius_from_confidence(confidence: float, consistency: float) -> float:
    trust = max(0.0, min(1.0, (confidence or 0.0) * (consistency or 0.0)))
    return R_MIN + (R_MAX - R_MIN) * (1.0 - trust)


def orbital_mechanics(mass: float, radius: float, central_mass: float) -> dict:
    v = math.sqrt(G * central_mass / radius)
    period = 2.0 * math.pi * math.sqrt(radius ** 3 / (G * central_mass))
    angular_momentum = mass * v * radius
    energy = -G * central_mass * mass / (2.0 * radius)
    return {
        "velocity": round(v, 8),
        "period": round(period, 8),
        "angular_momentum": round(angular_momentum, 8),
        "energy": round(energy, 8),
    }


def ensure_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS doc_orbital_position (
            doc_idx INTEGER PRIMARY KEY,
            sector TEXT NOT NULL,
            mass REAL NOT NULL,
            radius REAL NOT NULL,
            theta REAL NOT NULL,
            velocity REAL NOT NULL,
            period REAL NOT NULL,
            angular_momentum REAL NOT NULL,
            energy REAL NOT NULL,
            central_mass REAL NOT NULL,
            method TEXT DEFAULT 'kepler_v1',
            computed_at TEXT DEFAULT (datetime('now'))
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sector_orbital_position (
            sector TEXT PRIMARY KEY,
            mass REAL NOT NULL,
            x REAL NOT NULL,
            y REAL NOT NULL,
            vx REAL NOT NULL,
            vy REAL NOT NULL,
            r REAL NOT NULL,
            energy_error REAL NOT NULL,
            nbody_steps INTEGER NOT NULL,
            method TEXT DEFAULT 'nbody_v1',
            computed_at TEXT DEFAULT (datetime('now'))
        )
        """
    )
    conn.commit()


def simulate_sector_nbody(central_mass: dict[str, float], steps: int) -> dict[str, dict]:
    """Run a real N-body simulation (N=6, one Body per sector) so sector
    "star" positions come from genuine mutual Newtonian gravity instead of
    each sector sitting at an independent, non-interacting fixed point.

    Initial layout: sectors placed on a hexagon (radius scaled so heavier
    sectors start closer to the barycenter — a physically sensible seed,
    not a claim about final positions, since gravity moves them from
    there), given circular-orbit initial velocity around the system's
    total mass so the configuration starts near-equilibrium rather than
    immediately collapsing or flying apart.
    """
    names = list(central_mass.keys())
    n = len(names)
    total_mass = sum(central_mass.values())
    max_mass = max(central_mass.values())

    system = NBodySystem(G=G)
    for i, name in enumerate(names):
        m = central_mass[name]
        # Heavier sectors start closer in (inverse-mass radius seed)
        r = R_MAX * (1.0 - 0.5 * (m / max_mass))
        angle = 2.0 * math.pi * i / n
        x, y = r * math.cos(angle), r * math.sin(angle)
        # Circular velocity around the rest of the system's mass, tangential
        v_circ = math.sqrt(G * (total_mass - m) / max(r, 1e-6))
        vx, vy = -v_circ * math.sin(angle), v_circ * math.cos(angle)
        system.add_body(Body(label=name, mass=m, x=x, y=y, vx=vx, vy=vy))

    system._compute_accelerations()
    system.evolve(steps=steps, record_energy=True)

    result = {}
    for body in system.bodies:
        result[body.label] = {
            "mass": body.mass,
            "x": round(body.x, 6),
            "y": round(body.y, 6),
            "vx": round(body.vx, 6),
            "vy": round(body.vy, 6),
            "r": round(body.r, 6),
        }
    energy_err = system.energy_error()
    for label in result:
        result[label]["energy_error"] = round(energy_err, 8)
    return result


def run(write: bool, nbody_steps: int = 200) -> dict:
    # extract_geometry.repo_root_from_here() returns the directory of
    # extract_geometry.py itself (integration/Orbital/main/), not the real
    # repo root — fine for run_global_pass() when a caller supplies its own
    # repo_root, but wrong here since we call compute_info_mass() directly.
    # Using the real _ROOT gives compute_info_mass() a repo_root it can
    # actually find src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega under, so
    # sector masses reflect real code content instead of falling through to
    # the zero/floor case for every sector.
    repo_root = _ROOT
    sector_masses_raw = compute_info_mass(repo_root)
    # Central "star" mass per sector: real content-derived info_mass from the
    # live Orbital engine's own function, floored so no sector has a
    # degenerate (near-zero) central mass if its code footprint is small.
    max_char_count = max((v["char_count"] for v in sector_masses_raw.values()), default=0) or 1
    central_mass = {
        s: 5.0 + 45.0 * (m["char_count"] / max_char_count)
        for s, m in sector_masses_raw.items()
    }

    sector_nbody = simulate_sector_nbody(central_mass, steps=nbody_steps)

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    ensure_table(conn)

    if write:
        conn.executemany(
            """
            INSERT INTO sector_orbital_position
                (sector, mass, x, y, vx, vy, r, energy_error, nbody_steps)
            VALUES (?,?,?,?,?,?,?,?,?)
            ON CONFLICT(sector) DO UPDATE SET
                mass=excluded.mass, x=excluded.x, y=excluded.y, vx=excluded.vx, vy=excluded.vy,
                r=excluded.r, energy_error=excluded.energy_error, nbody_steps=excluded.nbody_steps,
                computed_at=datetime('now')
            """,
            [
                (name, d["mass"], d["x"], d["y"], d["vx"], d["vy"], d["r"], d["energy_error"], nbody_steps)
                for name, d in sector_nbody.items()
            ],
        )
        conn.commit()

    rows = conn.execute(
        "SELECT idx, themes, essence, full_text_len, confidence, consistency_score FROM doc_analysis"
    ).fetchall()

    top_concept = dict(
        conn.execute(
            """
            SELECT doc_idx, operator_id FROM doc_concepts dc
            WHERE score = (SELECT MAX(score) FROM doc_concepts WHERE doc_idx = dc.doc_idx)
            GROUP BY doc_idx
            """
        ).fetchall()
    )

    from ciel_geometry.phasenav.operator_algebra import ALL_OPERATOR_IDS  # noqa: E402
    operator_index = {op: i for i, op in enumerate(ALL_OPERATOR_IDS)}
    n_ops = len(ALL_OPERATOR_IDS)

    placements = []
    sector_counts: dict[str, int] = {}
    for row in rows:
        try:
            themes = json.loads(row["themes"]) if row["themes"] else []
        except (json.JSONDecodeError, TypeError):
            themes = []
        sector = assign_sector(themes, row["essence"] or "")
        sector_counts[sector] = sector_counts.get(sector, 0) + 1

        essence_len = len(row["essence"] or "")
        mass = content_mass(row["full_text_len"] or 0, essence_len)
        radius = radius_from_confidence(row["confidence"], row["consistency_score"])
        M = central_mass[sector]
        mech = orbital_mechanics(mass, radius, M)

        op = top_concept.get(row["idx"])
        op_idx = operator_index.get(op, row["idx"] % n_ops)
        theta = 2.0 * math.pi * (op_idx / n_ops)

        placements.append(
            (row["idx"], sector, round(mass, 6), round(radius, 6), round(theta, 6),
             mech["velocity"], mech["period"], mech["angular_momentum"], mech["energy"], M)
        )

    if write:
        conn.executemany(
            """
            INSERT INTO doc_orbital_position
                (doc_idx, sector, mass, radius, theta, velocity, period, angular_momentum, energy, central_mass)
            VALUES (?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(doc_idx) DO UPDATE SET
                sector=excluded.sector, mass=excluded.mass, radius=excluded.radius,
                theta=excluded.theta, velocity=excluded.velocity, period=excluded.period,
                angular_momentum=excluded.angular_momentum, energy=excluded.energy,
                central_mass=excluded.central_mass, computed_at=datetime('now')
            """,
            placements,
        )
        conn.commit()

    conn.close()
    return {
        "documents_placed": len(placements),
        "sector_counts": sector_counts,
        "central_masses": central_mass,
        "sector_nbody": sector_nbody,
        "nbody_steps": nbody_steps,
        "written": write,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--write", action="store_true", help="Persist to doc_orbital_position/sector_orbital_position tables (dry-run without it)")
    ap.add_argument("--nbody-steps", type=int, default=200, help="Integration steps for the 6-sector N-body simulation")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="[orbital-placement] %(message)s")
    result = run(write=args.write, nbody_steps=args.nbody_steps)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
