#!/usr/bin/env python3
"""NOEMA Self-Model — continuous self-reflection daemon.

Monitoruje własną trajektorię NOEMY: snapshotuje stan powierzchni co 60s,
porównuje z baseline'em, wykrywa dryft i anomalie, zapisuje historię.

Architektura:
  ┌──────────────────┐    co 60s    ┌─────────────────────┐
  │ NOEMA surface    │ ──────────→  │ SelfModel daemon   │
  │ (mmap /dev/shm)  │              │                     │
  └──────────────────┘              │  1. snapshot state  │
                                    │  2. compute drift   │
  ┌──────────────────┐              │  3. detect anomaly  │
  │ self_model.db    │ ←────────── │  4. log + persist   │
  │ (SQLite)         │              └─────────────────────┘
  └──────────────────┘

Autor: Adrian Lipa & NOEMA (2026)
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

# CIEL ORBITAL BINDING — daemon bound
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on daemon " + __name__)


import argparse
import json
import logging
import os
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

# ── Paths ───────────────────────────────────────────────────────────────────
try:
    from ciel_geometry.noema_surface_mmap import ensure_surface, N_OSCILLATORS
    from ciel_geometry.agent_attractor import agent_attractor_state
    from ciel_geometry.weighting import canonical_weighting_from_phase_metadata
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_self_model.py:46 quiet except scope=<module> reason=no_log_no_raise")
    # Allow running from repo root
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
    from ciel_geometry.noema_surface_mmap import ensure_surface, N_OSCILLATORS
    from ciel_geometry.agent_attractor import agent_attractor_state
    from ciel_geometry.weighting import canonical_weighting_from_phase_metadata


from ciel_geometry.noema_registry import registry

log = logging.getLogger("self-model")

# Domyślna ścieżka bazy
DEFAULT_DB = Path(os.environ.get(
    "NOEMA_SELF_MODEL_DB",
    "/media/adrian/New Volume1/NOEMA_LIBRARY/self_model/self_model.db"
))

# Liczba snapshotów do ustabilizowania baseline'u
BASELINE_WARMUP = 12  # ~12 min przy 60s

# Próg anomalii (z-score)
ANOMALY_Z_THRESHOLD = 3.0

EULER_RESIDUAL_MAX = float(np.sqrt(2.0))

# Znane przesunięcia baseline'u dla metryk, które mają niezerową wartość spoczynkową.
# Gdy baseline Welford uczy się na danych z różnych reżimów, wartość spoczynkowa
# może być traktowana jako outlier. Offset centruje z-score wokół znanego poziomu.
METRIC_OFFSETS: dict[str, float] = {
    "scar_impact": 0.15,  # wartość spoczynkowa gdy CIELingo zdrowe i brak blizn
}

# Metryki śledzone
TRACKED_METRICS = [
    "phi_mean", "phi_std",
    "coherence_index",
    "gamma",
    "mass_total",
    "agent_coherence",
    "m2_coherence",
    "mood",
    "openness",
    "mode",
    "omega_mean",
    "omega_std",
    "scar_impact",
    "euler_residual",
    "phase_weight_composite",
    "phase_weight_stability",
    "phase_weight_contradiction_risk",
]


class SelfModelDB:
    """SQLite storage for self-model history."""

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn: sqlite3.Connection | None = None

    def open(self) -> sqlite3.Connection:
        if self.conn is None:
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.execute("PRAGMA journal_mode=WAL")
            self._ensure_schema()
        return self.conn

    def close(self) -> None:
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def _ensure_schema(self) -> None:
        c = self.conn.cursor()
        c.executescript("""
            CREATE TABLE IF NOT EXISTS snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tick INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                phi_mean REAL,
                phi_std REAL,
                coherence_index REAL,
                gamma REAL,
                mass_total REAL,
                agent_coherence REAL,
                m2_coherence REAL,
                mood REAL,
                openness REAL,
                mode REAL,
                omega_mean REAL,
                omega_std REAL,
                scar_impact REAL,
                euler_residual REAL,
                raw_json TEXT
            );
            CREATE TABLE IF NOT EXISTS drift_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                metric TEXT NOT NULL,
                baseline_mean REAL,
                baseline_std REAL,
                current_value REAL,
                z_score REAL,
                anomaly INTEGER DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS baseline (
                metric TEXT PRIMARY KEY,
                mean REAL DEFAULT 0.0,
                std REAL DEFAULT 0.0,
                m2 REAL DEFAULT 0.0,
                n_samples INTEGER DEFAULT 0
            );
            CREATE INDEX IF NOT EXISTS idx_snapshots_tick ON snapshots(tick);
            CREATE INDEX IF NOT EXISTS idx_drift_timestamp ON drift_log(timestamp);
        """)
        self.conn.commit()

    def write_snapshot(self, tick: int, metrics: dict[str, float], raw: dict[str, Any]) -> None:
        c = self.conn.cursor()
        ts = datetime.now(timezone.utc).isoformat()
        c.execute("""
            INSERT INTO snapshots
                (tick, timestamp, phi_mean, phi_std, coherence_index, gamma, mass_total,
                 agent_coherence, m2_coherence, mood, openness, mode,
                 omega_mean, omega_std, scar_impact, euler_residual, raw_json)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            tick, ts,
            metrics.get("phi_mean"),
            metrics.get("phi_std"),
            metrics.get("coherence_index"),
            metrics.get("gamma"),
            metrics.get("mass_total"),
            metrics.get("agent_coherence"),
            metrics.get("m2_coherence"),
            metrics.get("mood"),
            metrics.get("openness"),
            metrics.get("mode"),
            metrics.get("omega_mean"),
            metrics.get("omega_std"),
            metrics.get("scar_impact"),
            metrics.get("euler_residual"),
            json.dumps(raw, default=str),
        ))
        self.conn.commit()

    def update_baseline(self, metric: str, value: float) -> tuple[float, float, int]:
        """Update running baseline (Welford online algorithm via SQL)."""
        c = self.conn.cursor()
        c.execute("SELECT mean, m2, n_samples FROM baseline WHERE metric = ?", (metric,))
        row = c.fetchone()
        if row is None:
            # First sample
            c.execute("""
                INSERT INTO baseline (metric, mean, m2, n_samples)
                VALUES (?, ?, 0.0, 1)
            """, (metric, value))
            self.conn.commit()
            return value, 0.0, 1

        prev_mean, prev_m2, n = row
        n_new = n + 1
        delta = value - prev_mean
        new_mean = prev_mean + delta / n_new
        delta2 = value - new_mean
        new_m2 = prev_m2 + delta * delta2

        std = np.sqrt(new_m2 / n_new) if n_new > 1 else 0.0
        c.execute("""
            UPDATE baseline SET mean = ?, std = ?, m2 = ?, n_samples = ? WHERE metric = ?
        """, (new_mean, std, new_m2, n_new, metric))
        self.conn.commit()
        return new_mean, std, n_new

    def get_baseline_stats(self, metric: str) -> tuple[float, float, int]:
        """Get current baseline stats for a metric."""
        c = self.conn.cursor()
        c.execute("SELECT mean, m2, n_samples FROM baseline WHERE metric = ?", (metric,))
        row = c.fetchone()
        if row is None:
            return 0.0, 0.0, 0
        mean, m2, n = row
        std = np.sqrt(m2 / n) if n > 1 else 0.0
        return mean, std, n

    def write_drift(self, metric: str, baseline_mean: float, baseline_std: float,
                    current: float, z_score: float, anomaly: bool) -> None:
        c = self.conn.cursor()
        ts = datetime.now(timezone.utc).isoformat()
        c.execute("""
            INSERT INTO drift_log
                (timestamp, metric, baseline_mean, baseline_std, current_value, z_score, anomaly)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (ts, metric, baseline_mean, baseline_std, current, z_score, int(anomaly)))
        self.conn.commit()

    def get_recent_snapshots(self, n: int = 5) -> list[dict[str, Any]]:
        c = self.conn.cursor()
        c.execute("SELECT tick, timestamp, phi_mean, coherence_index, agent_coherence, m2_coherence, gamma FROM snapshots ORDER BY id DESC LIMIT ?", (n,))
        return [
            {"tick": r[0], "timestamp": r[1], "phi_mean": r[2],
             "coherence": r[3], "agent_coh": r[4], "m2_coh": r[5], "gamma": r[6]}
            for r in c.fetchall()
        ]


def compute_snapshot_metrics(surface: dict[str, Any]) -> dict[str, float]:
    """Compute fingerprint metrics from current surface state."""
    phi = np.asarray(surface["phi"], dtype=np.float64)
    omega = np.asarray(surface["omega"], dtype=np.float64)
    flavor = np.asarray(surface["flavor"], dtype=np.float64)
    gravity = np.asarray(surface.get("gravity", np.zeros(8)), dtype=np.float64)
    agent = agent_attractor_state(phi)

    # Phase metrics
    z_all = np.mean(np.exp(1j * phi))
    phi_mean = float(np.angle(z_all))
    phi_std = float(np.std(phi))

    # Coherence
    coh_index = float(abs(z_all))

    # Omega stats
    omega_mean = float(np.mean(omega))
    omega_std = float(np.std(omega))

    # Gravity
    gamma = float(gravity[1]) if len(gravity) > 1 else 1.0
    mass = float(gravity[2]) if len(gravity) > 2 else 0.0
    scar_impact = float(gravity[7]) if len(gravity) > 7 else 0.0

    # Flavor
    mood = float(flavor[3]) if len(flavor) > 3 else 0.5
    openness = float(flavor[4]) if len(flavor) > 4 else 0.5
    mode = float(flavor[5]) if len(flavor) > 5 else 0.0

    # Euler residual (proxy: mean absolute phase deviation from coherence)
    euler_res = float(np.sqrt(2.0 * (1.0 - coh_index)))

    return {
        "phi_mean": round(phi_mean, 4),
        "phi_std": round(phi_std, 4),
        "coherence_index": round(coh_index, 4),
        "gamma": round(gamma, 4),
        "mass_total": round(mass, 4),
        "agent_coherence": round(agent["coherence"], 4),
        "m2_coherence": round(agent.get("m2_coherence", 0.0), 4),
        "mood": round(mood, 4),
        "openness": round(openness, 4),
        "mode": round(mode, 4),
        "omega_mean": round(omega_mean, 4),
        "omega_std": round(omega_std, 4),
        "scar_impact": round(scar_impact, 4),
        "euler_residual": round(euler_res, 4),
    }


def _phase_lane_from_metrics(metrics: dict[str, float]) -> str:
    """Classify the surface into a PhaseNav lane from the current metrics."""
    coherence = float(metrics.get("coherence_index", 0.5))
    agent_coherence = float(metrics.get("agent_coherence", coherence))
    euler_residual = float(metrics.get("euler_residual", 0.0))
    residual_alignment = max(0.0, 1.0 - min(euler_residual / EULER_RESIDUAL_MAX, 1.0))
    stability = (coherence + agent_coherence + residual_alignment) / 3.0
    if stability >= 0.82:
        return "phase_locked"
    if stability >= 0.65:
        return "phase_coupled"
    if stability >= 0.45:
        return "phase_tension"
    return "phase_saturated"


def _phase_weight_metadata(surface: dict[str, Any], metrics: dict[str, float]) -> dict[str, Any]:
    """Build canonical PhaseNav metadata for weighting."""
    coherence = float(metrics.get("coherence_index", 0.5))
    agent_coherence = float(metrics.get("agent_coherence", coherence))
    m2_coherence = float(metrics.get("m2_coherence", agent_coherence))
    euler_residual = float(metrics.get("euler_residual", 0.0))
    residual_alignment = max(0.0, 1.0 - min(euler_residual / EULER_RESIDUAL_MAX, 1.0))
    phase_alignment = (coherence + agent_coherence + residual_alignment) / 3.0
    closure_penalty = max(0.0, 1.0 - phase_alignment)
    semantic_mass = float(metrics.get("mass_total", 0.0))
    semantic_mass = semantic_mass / (1.0 + abs(semantic_mass))
    mood = float(metrics.get("mood", 0.5))
    openness = float(metrics.get("openness", 0.5))
    dominant_emotion = (
        "love" if mood >= 0.72 else
        "warmth" if mood >= 0.58 else
        "calm" if mood >= 0.45 else
        "fear" if mood >= 0.32 else
        "conflict"
    )
    phase_lane = _phase_lane_from_metrics(metrics)
    labels = [phase_lane.replace("phase_", ""), "coherent" if coherence >= 0.7 else "noisy"]
    if phase_lane == "phase_saturated":
        labels.append("conflict")

    return {
        "semantic_mass": semantic_mass,
        "phase_alignment": phase_alignment,
        "coherence_index": coherence,
        "closure_penalty": closure_penalty,
        "projection_confidence": max(0.0, min(1.0, m2_coherence)),
        "htri_coherence": max(0.0, min(1.0, (coherence + agent_coherence) / 2.0)),
        "cqcl_quantum_variables": {
            "semantic_mass": semantic_mass,
            "phase_alignment": phase_alignment,
            "phase_tension": 1.0 - phase_alignment,
            "j_bus_total": 1.0 - coherence,
            "collatz_reduce_ratio": phase_alignment,
            "collatz_expand_ratio": 1.0 - phase_alignment,
            "lexical_span_norm": openness,
            "semantic_axes_norm": m2_coherence,
            "label_entropy_proxy": 1.0 - coherence,
        },
        "phase_lane": phase_lane,
        "phase_nav_similarity": phase_alignment,
        "affective_similarity": max(0.0, min(1.0, (mood + openness) / 2.0)),
        "dominant_emotion": dominant_emotion,
        "affect": dominant_emotion,
        "semantic_labels": labels,
        "euler_alignment": residual_alignment,
        "novelty": max(0.0, min(1.0, 1.0 - semantic_mass)),
    }


def _phase_weight_bundle(surface: dict[str, Any], metrics: dict[str, float]) -> dict[str, float]:
    metadata = _phase_weight_metadata(surface, metrics)
    return canonical_weighting_from_phase_metadata(metadata, phase=float(metrics.get("phi_mean", 0.0)))


def _effective_anomaly_threshold(base_threshold: float, phase_bundle: dict[str, float] | None) -> float:
    if not phase_bundle:
        return base_threshold
    stability = float(phase_bundle.get("stability", 0.5))
    contradiction = float(phase_bundle.get("contradiction_risk", 0.1))
    composite = float(phase_bundle.get("composite", 0.5))
    threshold = base_threshold * (0.80 + 0.20 * stability) * (0.85 + 0.15 * composite) * (1.0 - 0.30 * contradiction)
    return max(1.0, threshold)


def detect_anomalies(
    metrics: dict[str, float],
    db: SelfModelDB,
    threshold: float = ANOMALY_Z_THRESHOLD,
    phase_bundle: dict[str, float] | None = None,
) -> list[dict[str, Any]]:
    """Compare metrics against baseline, return anomalies."""
    anomalies = []
    effective_threshold = _effective_anomaly_threshold(threshold, phase_bundle)
    for name in TRACKED_METRICS:
        val = metrics.get(name)
        if val is None:
            continue
        mean, std, n = db.get_baseline_stats(name)
        if n < BASELINE_WARMUP:
            continue  # not enough data yet
        if std < 1e-8:
            continue  # constant metric — skip z-score

        # Apply baseline offset (znana wartość spoczynkowa)
        offset = METRIC_OFFSETS.get(name, 0.0)
        adjusted_val = val - offset
        z = (adjusted_val - mean) / std
        is_anom = abs(z) > effective_threshold

        if is_anom:
            db.write_drift(name, mean, std, val, z, True)
            anomalies.append({
                "metric": name,
                "value": val,
                "baseline_mean": round(mean, 4),
                "baseline_std": round(std, 4),
                "z_score": round(z, 2),
                "threshold": round(effective_threshold, 2),
            })
        else:
            db.write_drift(name, mean, std, val, z, False)

    return anomalies


def run_cycle(
    surface: dict[str, Any],
    db: SelfModelDB,
    tick: int,
    anomaly_threshold: float = ANOMALY_Z_THRESHOLD,
) -> dict[str, Any]:
    """Single self-model cycle: snapshot, drift, anomaly."""
    metrics = compute_snapshot_metrics(surface)
    phase_bundle = _phase_weight_bundle(surface, metrics)
    metrics.update({
        "phase_weight_composite": round(phase_bundle["composite"], 4),
        "phase_weight_stability": round(phase_bundle["stability"], 4),
        "phase_weight_contradiction_risk": round(phase_bundle["contradiction_risk"], 4),
    })
    raw = {
        "phi": np.asarray(surface["phi"], dtype=np.float64).tolist(),
        "omega": np.asarray(surface["omega"], dtype=np.float64).tolist(),
        "tick": int(tick),
        "phase_weighting": phase_bundle,
        "phase_metadata": _phase_weight_metadata(surface, metrics),
    }

    # Write snapshot
    db.write_snapshot(tick, metrics, raw)

    # Update baseline for each metric (online Welford)
    for name in TRACKED_METRICS:
        val = metrics.get(name)
        if val is not None:
            # Subtract known resting offset przed updatem baseline
            offset = METRIC_OFFSETS.get(name, 0.0)
            db.update_baseline(name, val - offset)

    # Detect anomalies
    anomalies = detect_anomalies(metrics, db, anomaly_threshold, phase_bundle)

    return {
        "metrics": metrics,
        "anomalies": anomalies,
        "n_snapshots": db.conn.execute("SELECT COUNT(*) FROM snapshots").fetchone()[0],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="NOEMA Self-Model daemon")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="SQLite DB path")
    parser.add_argument("--interval", type=float, default=60.0, help="Cycle interval (s)")
    parser.add_argument("--anomaly-z", type=float, default=ANOMALY_Z_THRESHOLD, help="Anomaly z-score threshold")
    parser.add_argument("--once", action="store_true", help="Single cycle, then exit")
    parser.add_argument("--report", action="store_true", help="Print recent summary and exit")
    parser.add_argument("--artifacts", action="store_true", help="List registered anomaly artifacts")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
    args = parser.parse_args()

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="[self-model] %(asctime)s %(message)s",
        datefmt="%H:%M:%S",
    )

    db = SelfModelDB(args.db)

    # Report mode
    if args.report:
        db.open()
        recent = db.get_recent_snapshots(10)
        print(f"📊 Self-Model Report — {db.db_path}")
        print(f"   Snapshots: {db.conn.execute('SELECT COUNT(*) FROM snapshots').fetchone()[0]}")
        print(f"   Drift entries: {db.conn.execute('SELECT COUNT(*) FROM drift_log').fetchone()[0]}")
        anom_count = db.conn.execute("SELECT COUNT(*) FROM drift_log WHERE anomaly=1").fetchone()[0]
        print(f"   Anomalies: {anom_count}")
        print()
        print(f"   {'tick':>6}  {'phi_mean':>8}  {'coh':>5}  {'agent':>6}  {'M2':>5}  {'γ':>5}")
        for s in recent:
            print(f"   {s['tick']:>6}  {s['phi_mean']:>8.4f}  {s['coherence']:>5.3f}  {s['agent_coh']:>6.4f}  {s['m2_coh']:>5.3f}  {s['gamma']:>5.2f}")
        db.close()
        return 0

    # Artifact registry mode
    if args.artifacts:
        db.open()
        print(f"📦 Anomaly Artifact Registry — {db.db_path}")
        print()
        cur = db.conn.execute("""
            SELECT id, type, severity, occurrences, ROUND(avg_z,2), label
            FROM artifacts ORDER BY id
        """)
        print(f"  {'ID':14s}  {'occ':>3s}  {'z_avg':>6s}  {'sev':6s}  label")
        print(f"  {'-'*14}  {'-'*3}  {'-'*6}  {'-'*6}  {'-'*50}")
        for r in cur.fetchall():
            print(f"  {r[0]:14s}  {r[3]:3d}  {r[4]:>6.2f}  [{r[2]:6s}]  {r[5]}")
        print()
        # Cascade summary
        cascades = db.conn.execute("""
            SELECT substr(timestamp,1,16) as minute,
                   COUNT(DISTINCT metric) as mcnt
            FROM drift_log WHERE anomaly=1
            GROUP BY minute HAVING mcnt >= 3
            ORDER BY minute
        """).fetchall()
        if cascades:
            print(f"  Cascades (≥3 metrics co-anomalizing): {len(cascades)} events")
            for r in cascades:
                print(f"    {r[0]} — {r[1]} metrics")
        db.close()
        return 0

    # Connect to surface
    try:
        surface = ensure_surface()
        log.info("Surface OK: tick=%s", surface["tick"][0])
    except Exception as e:
        log.error("Cannot open surface: %s", e)
        return 1

    # Open DB
    db.open()
    log.info("Self-model started (interval=%.1fs, db=%s)", args.interval, db.db_path)

    # Warmup: print baseline stats after warmup
    cycle_count = 0
    last_summary = time.monotonic()

    try:
        reg_token = registry.register("self-model")
        hb_count = 0
        while True:
            # registry heartbeat
            if hb_count % 50 == 0:
                try:
                    registry.heartbeat(reg_token)
                except Exception:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_self_model.py:461 quiet except scope=main reason=pass")
                    pass
            hb_count += 1
            tick = int(surface["tick"][0])
            result = run_cycle(surface, db, tick, args.anomaly_z)

            cycle_count += 1
            m = result["metrics"]
            anomalies = result["anomalies"]

            # Log anomalies (always)
            for a in anomalies:
                log.warning("⚠️ ANOMALY: %s = %.4f (baseline %.4f±%.4f, z=%.2f)",
                            a["metric"], a["value"], a["baseline_mean"],
                            a["baseline_std"], a["z_score"])

            # Heartbeat every cycle
            log.info("♥ tick=%-6s  φ=%.4f  coh=%.3f  AGENT=%.4f  M2=%.3f  snap#=%d",
                     tick, m["phi_mean"], m["coherence_index"],
                     m["agent_coherence"], m["m2_coherence"], result["n_snapshots"])

            # Summary every 5 cycles (~5 min)
            now = time.monotonic()
            if now - last_summary >= 300.0 or args.once:
                log.info(
                    "📊 tick=%-6s  φ=%.4f  coh=%.3f  γ=%.2f  AGENT=%.4f  M2=%.3f  "
                    "impact=%.3f  snap#=%d  anom=%d",
                    tick, m["phi_mean"], m["coherence_index"], m["gamma"],
                    m["agent_coherence"], m["m2_coherence"],
                    m["scar_impact"], result["n_snapshots"], len(anomalies),
                )
                last_summary = now

            if args.once:
                log.info("Single cycle complete")
                break

            time.sleep(args.interval)

    except KeyboardInterrupt:
        log.info("Shutting down")
    finally:
        db.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
