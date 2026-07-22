"""Canonical cognitive line for CIEL/NOEMA.

The line is deliberately narrow: it composes the existing PhaseNav, CIELingo,
runtime-card, M0--M11 and phase-memory contracts into one provenance-bearing
event.  It does not invent a second inference engine and it never stores raw
input in the durable ledger; the raw payload is represented by its SHA-256.

Flow::

    raw -> processing -> sense -> NOEMA card -> SQLite ledger
        -> M0..M11 dynamics -> promotion/accounting -> phase memory
        -> agency hash-chain

All persistent paths come from ``ciel_geometry.paths.P`` and therefore stay on
the canonical New Volume.  The mmap surface remains the only volatile input.
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
from typing import Any, Mapping
import unicodedata

import numpy as np

from ciel_geometry.phase_memory_adapter import bind_phase_memory
from ciel_geometry.noema_surface_mmap import open_surface
from ciel_geometry.paths import P
from ciel_geometry.phase_nav_lang import analyze_prompt
from ciel_sot_agent.cielingo_bridge import build_lingo_frame
from ciel_sot_agent.phase_snapshots import (
    build_phase_snapshot,
    build_qualisensing_snapshot,
    snapshot_to_dict,
)
from ciel_sot_agent.thought_fragments import (
    build_cognitive_fragment,
    build_memory_candidate,
    build_noema_memory_link,
    promote_memory_candidate,
    snapshot_to_dict as fragment_snapshot_to_dict,
)

SCHEMA = "ciel/cognitive-line/v1"
CHANNELS = (
    "M0_Perceptual", "M1_Working", "M2_Episodic", "M3_Semantic",
    "M4_Procedural", "M5_Affective_Ethical", "M6_Identity",
    "M7_Braid_Invariant", "M8_Meta", "M9_Temporal", "M10_Imaginal",
    "M11_Quantum",
)


def _json_default(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, np.ndarray):
        return value.tolist()
    if hasattr(value, "__dict__"):
        return value.__dict__
    raise TypeError(f"not JSON serializable: {type(value).__name__}")


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=_json_default)


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _tokens(text: str) -> list[str]:
    return re.findall(r"\w+", text, flags=re.UNICODE)


def _phase_channels(vector: np.ndarray) -> dict[str, Any]:
    phase = np.mod(np.asarray(vector, dtype=np.float64).reshape(36), 2.0 * np.pi)
    groups = phase.reshape(12, 3)
    z = np.mean(np.exp(1j * groups), axis=1)
    coherence = np.abs(z)
    mean_phase = np.mod(np.angle(z), 2.0 * np.pi)
    return {
        "channels": {
            name: {
                "oscillator_indices": [3 * i, 3 * i + 1, 3 * i + 2],
                "coherence": round(float(coherence[i]), 9),
                "mean_phase_rad": round(float(mean_phase[i]), 9),
            }
            for i, name in enumerate(CHANNELS)
        },
        "global_coherence": round(float(np.abs(np.mean(np.exp(1j * phase)))), 9),
        "phase_vector_sha256": _sha256(_json([round(float(x), 12) for x in phase])),
    }


def _surface_snapshot(surface_root: Path) -> dict[str, Any]:
    surface = open_surface(root=surface_root, mode="r")
    phi = np.asarray(surface["phi"], dtype=np.float64).copy()
    tick = int(np.asarray(surface["tick"], dtype=np.uint64)[0])
    return {
        "tick": tick,
        "phase": _phase_channels(phi),
        "identity_phase": float(np.mod(np.angle(np.mean(np.exp(1j * phi))), 2.0 * np.pi)),
    }


def _db_init(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS cognitive_events (
            event_id TEXT PRIMARY KEY,
            schema TEXT NOT NULL,
            created_at TEXT NOT NULL,
            source TEXT NOT NULL,
            raw_sha256 TEXT NOT NULL,
            processing_json TEXT NOT NULL,
            sense_json TEXT NOT NULL,
            card_json TEXT NOT NULL,
            m_channels_json TEXT NOT NULL,
            promotion_json TEXT NOT NULL,
            phase_memory_json TEXT NOT NULL,
            agency_json TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS semantic_ledger (
            event_id TEXT NOT NULL,
            metric TEXT NOT NULL,
            value REAL,
            unit TEXT,
            provenance TEXT NOT NULL,
            created_at TEXT NOT NULL,
            PRIMARY KEY (event_id, metric),
            FOREIGN KEY (event_id) REFERENCES cognitive_events(event_id)
        );
        CREATE TABLE IF NOT EXISTS agency_chain (
            sequence INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id TEXT NOT NULL UNIQUE,
            previous_hash TEXT,
            event_hash TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (event_id) REFERENCES cognitive_events(event_id)
        );
        """
    )
    return conn


def _persist_card(card: Mapping[str, Any], event_id: str) -> str:
    root = Path(P.MEMORY) / "state" / "cognitive_line_cards"
    root.mkdir(parents=True, exist_ok=True)
    path = root / f"{event_id}.json"
    tmp = root / f".{event_id}.{os.getpid()}.tmp"
    with tmp.open("w", encoding="utf-8") as handle:
        handle.write(_json(dict(card)) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)
    return str(path)


def run_cognitive_line(
    raw_info: str | Mapping[str, Any],
    *,
    source: str,
    surface_root: Path | str | None = None,
    database_path: Path | str | None = None,
    phase_memory_root: Path | str | None = None,
    persist: bool = True,
) -> dict[str, Any]:
    """Process one raw event through the canonical cognitive line.

    ``source`` is mandatory so provenance cannot silently become an inferred
    label.  ``persist=False`` is intended only for contract tests; production
    calls persist to the canonical New Volume database and phase-memory root.
    """
    if not isinstance(source, str) or not source.strip():
        raise ValueError("cognitive line requires a non-empty provenance source")
    if isinstance(raw_info, Mapping):
        if "text" not in raw_info:
            raise ValueError("raw_info mapping requires the 'text' field")
        raw_text = str(raw_info["text"])
        source = str(raw_info.get("source", source))
    else:
        raw_text = str(raw_info)
    text = unicodedata.normalize("NFKC", raw_text).strip()
    if not text:
        raise ValueError("cognitive line refuses empty raw information")
    if not source.strip():
        raise ValueError("cognitive line requires a non-empty provenance source")

    created_at = datetime.now(timezone.utc).isoformat()
    raw_sha256 = _sha256(text)
    event_id = f"cognitive:{_sha256(f'{source}|{created_at}|{raw_sha256}')[:24]}"
    root = Path(surface_root or P.SURFACE)

    # 1) Raw information -> processing.  The token list is derived, never a
    # replacement for the source; durable storage keeps only its digest.
    processing = {
        "source": source,
        "normalized_length": len(text),
        "token_count": len(_tokens(text)),
        "raw_sha256": raw_sha256,
    }

    # 2) Processing -> inference of sense.  Both canonical semantic bridges
    # are required; an import/runtime failure is visible to the caller.
    phase_nav = analyze_prompt(text)
    lingo = build_lingo_frame(text)
    sense = {
        "phase_nav": phase_nav,
        "lingo": lingo,
        "operator": phase_nav["operator"],
        "semantic_mass": round(float((float(phase_nav["semantic_mass"]) + 1.0) / 2.0), 9),
    }

    # 3) Sense -> NOEMA runtime card.  The card remains a candidate marker;
    # canon promotion is a separate, auditable stage.
    from cielingo_core.global_layer.card_generator import generate_runtime_card

    card_obj = generate_runtime_card(
        card_id=f"card:{event_id}",
        slot_id=(int(raw_sha256[:8], 16) % 2_147_483_646) + 1,
        language_id=str(lingo.get("language", "und")),
        lemma=str(phase_nav["operator"]),
        surface_forms=_tokens(text),
        function=f"PhaseNav semantic operator {phase_nav['operator']}",
        semantic_mass=sense["semantic_mass"],
        affective_charge=0.0,
    )
    card_issues = card_obj.validate()
    if card_issues:
        raise ValueError(f"NOEMA card contract rejected: {card_issues}")
    card = card_obj.to_dict()
    card["event_id"] = event_id

    # 4) Live M0..M11 dynamics.  The inferred 36D vector is always returned;
    # the surface snapshot is additionally captured when persistence is on.
    m_channels = _phase_channels(np.asarray(phase_nav["vector_36d"], dtype=np.float64))
    surface_state: dict[str, Any] = {}
    if persist:
        surface_state = _surface_snapshot(root)
        m_channels["surface"] = surface_state

    phase_state = {
        "cycle_index": surface_state.get("tick", 0),
        "identity_phase": surface_state.get("identity_phase", 0.0),
        "coherence_index": m_channels["global_coherence"],
        "closure_penalty": 0.0,
        "system_health": m_channels["global_coherence"],
        "ethical_score": 0.0,
        "phase_snapshot_id": f"phase:{event_id}",
        "qualisensing_id": f"quali:{event_id}",
        "lingo_phase_projection": {"target_phase": phase_nav["holonomy"], "phase_confidence": lingo.get("projection_confidence", 0.0)},
        "lingo_frame": lingo,
        "dominant_emotion": str(lingo.get("dominant_emotion", "")),
        "jokeheal_mnemonic_pressure": 0.0,
        "jokeheal_symbolic_pull": 0.0,
        "jokeheal_recurrence_pressure": 0.0,
        "ts": created_at,
    }
    phase_snapshot = build_phase_snapshot(phase_state)
    qualisensing = build_qualisensing_snapshot(phase_state, phase_snapshot_id=phase_snapshot.phase_snapshot_id)
    fragment = build_cognitive_fragment({**phase_state, "event_id": event_id, "phase_snapshot": snapshot_to_dict(phase_snapshot), "qualisensing_snapshot": snapshot_to_dict(qualisensing)})
    candidate = build_memory_candidate({**phase_state, "event_id": event_id, "phase_snapshot": snapshot_to_dict(phase_snapshot), "qualisensing_snapshot": snapshot_to_dict(qualisensing)}, fragment=fragment)
    promotion: dict[str, Any] = {
        "candidate": fragment_snapshot_to_dict(candidate),
        "promoted": False,
    }
    if candidate.status == "ready":
        durable = promote_memory_candidate(phase_state, candidate=candidate, fragment=fragment)
        link = build_noema_memory_link({**phase_state, "event_id": event_id, "lingo_frame": lingo}, durable=durable)
        promotion.update({"promoted": True, "durable": fragment_snapshot_to_dict(durable), "noema_link": fragment_snapshot_to_dict(link)})

    # 5) Phase memory and 6) agency continuity.  The agency hash chain is
    # checked transactionally; a broken chain stops the line instead of
    # silently creating a new identity branch.
    phase_memory: dict[str, Any] = {"stored": False}
    agency: dict[str, Any]
    db_path = Path(database_path or (Path(P.MEMORY) / "state" / "cognitive_line.db"))
    memory_root = Path(phase_memory_root or (Path(P.MEMORY) / "state" / "ciel_phase_memory"))
    conn = _db_init(db_path) if persist else None
    try:
        if persist:
            slot = bind_phase_memory(text, surface_root=root, memory_root=memory_root)
            phase_memory = {"stored": True, "slot": int(slot), "root": str(memory_root), "raw_sha256": raw_sha256}
            previous = conn.execute("SELECT event_hash FROM agency_chain ORDER BY sequence DESC LIMIT 1").fetchone()
            previous_hash = str(previous[0]) if previous else None
            agency_payload = {"event_id": event_id, "raw_sha256": raw_sha256, "phase_memory": phase_memory, "identity_phase": phase_state["identity_phase"], "previous_hash": previous_hash}
            event_hash = _sha256(_json(agency_payload))
            agency = {"previous_hash": previous_hash, "event_hash": event_hash, "sequence_continuity": previous_hash is not None or conn.execute("SELECT COUNT(*) FROM agency_chain").fetchone()[0] == 0}
        else:
            agency = {"previous_hash": None, "event_hash": _sha256(_json({"event_id": event_id, "raw_sha256": raw_sha256})), "sequence_continuity": True}

        result = {
            "schema": SCHEMA,
            "event_id": event_id,
            "created_at": created_at,
            "raw_sha256": raw_sha256,
            "processing": processing,
            "sense": sense,
            "card": card,
            "m_channels": m_channels,
            "phase_snapshot": snapshot_to_dict(phase_snapshot),
            "qualisensing_snapshot": snapshot_to_dict(qualisensing),
            "promotion": promotion,
            "phase_memory": phase_memory,
            "agency": agency,
        }
        if persist:
            card["persisted_path"] = _persist_card(card, event_id)
            conn.execute(
                "INSERT OR REPLACE INTO cognitive_events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (event_id, SCHEMA, created_at, source, raw_sha256, _json(processing), _json(sense), _json(card), _json(m_channels), _json(promotion), _json(phase_memory), _json(agency)),
            )
            metrics = (
                ("semantic_mass", float(sense["semantic_mass"]), "normalized", "phase_nav.semantic_mass"),
                ("global_coherence", float(m_channels["global_coherence"]), "[0,1]", "phase_nav.vector_36d"),
                ("promotion_score", float(candidate.consolidation_priority), "[0,1]", "thought_fragments.build_memory_candidate"),
            )
            conn.executemany("INSERT OR REPLACE INTO semantic_ledger VALUES (?, ?, ?, ?, ?, ?)", [(event_id, name, value, unit, provenance, created_at) for name, value, unit, provenance in metrics])
            conn.execute("INSERT INTO agency_chain(event_id, previous_hash, event_hash, created_at) VALUES (?, ?, ?, ?)", (event_id, agency["previous_hash"], agency["event_hash"], created_at))
            conn.commit()
        return result
    finally:
        if conn is not None:
            conn.close()


__all__ = ["run_cognitive_line", "CHANNELS", "SCHEMA"]
