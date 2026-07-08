"""PhaseNav24DBridge — łączy 24D bibliotekę z pulpitu z PhaseNav i CIELingo.

Źródło: /home/adrian/new_volume_rw/NOEMA_PHASE_DATA/PHASE_INDEX/
  - library_index.npy: 1287 × 24D wektory
  - library_meta.npy: metadane (id, filename, author, topic)
  - knowledge_graph.json: graf wiedzy (operatory, topic, autorzy)
  - adrian_composite_24d.npy: 24D kompozyt Adriana

Funkcje:
  1. load_24d_library() — wczytuje całą bibliotekę
  2. bridge_to_phasenav() — dodaje 24D wektory do PhaseNav concept_phases
  3. bridge_to_cielingo() — udostępnia jako CIELingo word cards
  4. bridge_to_subconscious() — używa jako stan podświadomości
"""
from __future__ import annotations

import json
import math
import hashlib
import time
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

logger = logging.getLogger("phasenav_24d_bridge")

KAPPA = math.log(2.0) / (24.0 * math.pi)
LIBRARY_ROOT = Path("/home/adrian/new_volume_rw/NOEMA_PHASE_DATA/PHASE_INDEX")
PHASENAV_DATA = Path("/dev/shm/ciel_noema/phasenav")


@dataclass
class LibraryEntry24D:
    """Pojedynczy wpis z 24D biblioteki."""
    entry_id: str
    filename: str
    author: str
    topic: str
    date: str
    on_disk: bool
    disk_path: str
    vector_24d: list[float]

    def phase_24d(self) -> float:
        """Średnia faza z 24D wektora (sprowadzona do [0, 2π))."""
        mean = float(np.mean(self.vector_24d))
        return (mean % (2 * math.pi)) if mean < 0 else mean


@dataclass
class Library24D:
    """Pełna 24D biblioteka."""
    entries: list[LibraryEntry24D]
    index: np.ndarray  # (N, 24)
    meta: np.ndarray   # (N,) structured
    graph: dict[str, Any]
    composite_24d: list[float]

    @property
    def n_entries(self) -> int:
        return len(self.entries)


def load_24d_library() -> Library24D:
    """Wczytuje pełną 24D bibliotekę z pulpitu."""
    index = np.load(str(LIBRARY_ROOT / "library_index.npy"), allow_pickle=False)
    meta = np.load(str(LIBRARY_ROOT / "library_meta.npy"), allow_pickle=True)
    composite = np.load(str(LIBRARY_ROOT / "adrian_composite_24d.npy"), allow_pickle=False)

    try:
        graph = json.loads((LIBRARY_ROOT / "knowledge_graph.json").read_text())
    except Exception:
        logger.warning("knowledge_graph.json not found or invalid at %s", LIBRARY_ROOT / "knowledge_graph.json")
        graph = {"nodes": [], "edges": [], "stats": {}}

    entries = []
    for i in range(len(meta)):
        m = meta[i]
        entries.append(LibraryEntry24D(
            entry_id=str(m["id"]),
            filename=str(m["filename"]),
            author=str(m["author"]),
            topic=str(m["topic"]),
            date=str(m["date"]),
            on_disk=bool(m["on_disk"]),
            disk_path=str(m["disk_path"]),
            vector_24d=index[i].tolist(),
        ))

    return Library24D(
        entries=entries,
        index=index,
        meta=meta,
        graph=graph,
        composite_24d=composite.tolist(),
    )


def bridge_to_phasenav(lib: Library24D) -> dict[str, Any]:
    """Dodaje 24D wektory do PhaseNav concept_phases.

    Tworzy plik CIELINGO_PHASENAV_CONCEPT_PHASES_24D.jsonl
    z 1287 wpisami. Każdy wpis ma:
      - concept_id: hashed from entry_id
      - orbit_vector_24d: pełny 24D wektor
      - nearest_phasenav_concept: dopasowanie do istniejących 330 PhaseNav concept phases
      - phase: mean phase from 24D
      - semantic_mass: z normy L2 wektora
      - author, topic: z metadanych
    """
    from ciel_geometry.phasenav.solver import PhaseNavSolver
    s = PhaseNavSolver.load()
    cid_list = list(s.data.concept_phases.keys())
    n_phasenav = len(cid_list)

    out = []
    matched_count = 0
    for entry in lib.entries:
        # Phase from 24D mean
        phase_24d = entry.phase_24d()

        # Nearest PhaseNav concept
        nearest = None
        nearest_dist = float('inf')
        for c in cid_list:
            cp = s.data.concept_phases.get(c, {})
            cp_phase = float(cp.get('geometric_phase_rad', 0))
            d = min(abs(phase_24d - cp_phase), 2*math.pi - abs(phase_24d - cp_phase))
            if d < nearest_dist:
                nearest_dist = d
                nearest = c
        if nearest:
            matched_count += 1

        # Semantic mass from L2 norm
        vec = np.array(entry.vector_24d)
        mass = float(np.clip(np.linalg.norm(vec) / math.sqrt(24), 0, 1))

        card = {
            "concept_id": f"lib24d:{entry.entry_id}",
            "source": "ciel_memories_24d",
            "filename": entry.filename,
            "author": entry.author,
            "topic": entry.topic,
            "orbit_vector_24d": [round(v, 6) for v in entry.vector_24d],
            "geometric_phase_rad": round(phase_24d, 6),
            "semantic_mass": round(mass, 6),
            "nearest_phasenav_concept": nearest,
            "phase_distance": round(nearest_dist, 6),
            "on_disk": entry.on_disk,
        }
        out.append(card)

    # Write
    PHASENAV_DATA.mkdir(parents=True, exist_ok=True)
    out_path = PHASENAV_DATA / "CIELINGO_PHASENAV_CONCEPT_PHASES_24D.jsonl"
    with open(out_path, "w") as f:
        for card in out:
            f.write(json.dumps(card) + "\n")

    return {
        "written_to": str(out_path),
        "total_entries": lib.n_entries,
        "matched_to_phasenav": matched_count,
        "phasenav_concepts_available": n_phasenav,
        "unmatched": lib.n_entries - matched_count,
    }


def bridge_to_cielingo(lib: Library24D) -> dict[str, Any]:
    """Tworzy CIELingo word cards z 24D biblioteki i zapisuje jako karty słów.

    Mapuje każdy wpis biblioteki na CielingoRuntimeCard przez card_generator.
    Zapisuje do /data/unknown_words/verified_cards/ jako karty.
    """
    from cielingo_core.global_layer.card_generator import generate_runtime_card
    from cielingo_core.global_layer.card_runtime_schema import (
        CardOntologyClass, CardValidationStatus,
    )
    from cielingo_core.global_layer.card_validator import validate_runtime_card

    card_dir = Path("/home/adrian/new_volume_rw/CIEL_PROJECT_CANON/NOEMA/data/unknown_words/verified_cards")
    card_dir.mkdir(parents=True, exist_ok=True)

    stored = []
    failed = 0
    for entry in lib.entries:
        cid = f"lib24d:{entry.entry_id}"
        # Use filename stem as lemma
        lemma = Path(entry.filename).stem.lower().replace("_", " ").replace("-", " ")
        if not lemma or len(lemma) < 2:
            lemma = entry.topic.lower()[:50] or "unknown"

        try:
            card = generate_runtime_card(
                card_id=cid,
                slot_id=hash(entry.entry_id) % 1000,
                language_id="en",
                lemma=lemma[:100],
                surface_forms=[lemma[:100], entry.filename],
                function=f"author:{entry.author} topic:{entry.topic}",
                ontology_class=CardOntologyClass.KOTO,
                validation_status=CardValidationStatus.DRAFT,
            )
            result = validate_runtime_card(card)
            if not result.ok:
                failed += 1
                continue

            card_path = card_dir / f"{cid}.json"
            card_path.write_text(json.dumps({
                "card_id": cid,
                "lemma": lemma[:100],
                "author": entry.author,
                "topic": entry.topic,
                "filename": entry.filename,
                "language": "en",
                "source": f"24d_library:{entry.entry_id}",
                "confidence": 0.5,
                "validated": True,
                "timestamp": time.time(),
            }, indent=2))
            stored.append(cid)
        except Exception as e:
            logger.debug("failed to store card %s: %s", cid, e)
            failed += 1

    return {
        "total_entries": lib.n_entries,
        "stored_cards": len(stored),
        "failed": failed,
        "card_dir": str(card_dir),
    }


def bridge_to_subconscious(lib: Library24D) -> dict[str, Any]:
    """Używa 24D biblioteki jako źródła stanu podświadomości.

    Oblicza:
      - oscillators_12d: średnia 24D → 12D redukcja
      - R_24d: Kuramoto rząd z 1287 wektorów
      - dominant_topics: top 5 topiców
      - composite: wektor kompozytowy Adriana
    """
    # Reduce 24D to 12D: average adjacent pairs
    vecs = lib.index  # (1287, 24)
    reduced = vecs.reshape(lib.n_entries, 12, 2).mean(axis=2)  # (1287, 12)

    # Mean across all entries → 12D oscillators
    oscillators_12d = np.mean(reduced, axis=0).tolist()
    oscillators_12d = [max(0.0, min(1.0, float(v))) for v in oscillators_12d]

    # Kuramoto order from 1287 × 12D phases
    phases_rad = np.arctan2(vecs[:, 1], vecs[:, 0])  # rough phase per entry
    R_24d = float(abs(np.mean(np.exp(1j * phases_rad))))

    # Topic dominance
    topic_counts: dict[str, int] = {}
    for entry in lib.entries:
        topic_counts[entry.topic] = topic_counts.get(entry.topic, 0) + 1
    top5 = sorted(topic_counts.items(), key=lambda x: -x[1])[:5]

    return {
        "oscillators_12d": [round(v, 4) for v in oscillators_12d],
        "R_24d": round(R_24d, 4),
        "composite_24d_adrian": [round(v, 4) for v in lib.composite_24d],
        "dominant_topics": [{"topic": t, "count": c} for t, c in top5],
        "n_entries": lib.n_entries,
        "graph_nodes": len(lib.graph.get("nodes", [])),
        "graph_edges": len(lib.graph.get("edges", [])),
    }


def full_bridge() -> dict[str, Any]:
    """Uruchamia wszystkie mosty i zwraca raport."""
    lib = load_24d_library()
    report = {
        "library": {
            "n_entries": lib.n_entries,
            "vector_dim": lib.index.shape[1],
            "composite_24d": len(lib.composite_24d),
            "graph_nodes": len(lib.graph.get("nodes", [])),
            "graph_edges": len(lib.graph.get("edges", [])),
        },
        "phasenav_bridge": None,
        "cielingo_bridge": None,
        "subconscious_bridge": None,
        "errors": [],
    }

    try:
        report["phasenav_bridge"] = bridge_to_phasenav(lib)
    except Exception as e:
        logger.error("phasenav_bridge failed: %s", e)
        report["errors"].append(f"phasenav: {e}")

    try:
        report["cielingo_bridge"] = bridge_to_cielingo(lib)
    except Exception as e:
        logger.error("cielingo_bridge failed: %s", e)
        report["errors"].append(f"cielingo: {e}")

    try:
        report["subconscious_bridge"] = bridge_to_subconscious(lib)
    except Exception as e:
        logger.error("subconscious_bridge failed: %s", e)
        report["errors"].append(f"subconscious: {e}")

    return report
