"""Concept dependency graph — relates concept_windows.py's windows to each
other instead of treating them as isolated retrieval points.

Origin (2026-07-10, same conversation as concept_windows.py): Adrian asked
directly "a co z zależnościami pomiędzy konceptami?" (what about
dependencies between concepts?) after windowing was designed — splitting a
document into windows loses the relationships between them unless those
relationships are captured explicitly.

Edge weight = combination of:
  (a) sentence proximity — 1/(1+gap), windows anchored close together in the
      source text are more likely related than distant ones.
  (b) phase coupling — Kuramoto order parameter |mean(exp(i·Δφ))| between two
      windows' 36D vectors, reusing exactly the math already fixed in
      phasenav_learning_gate.py::_vector_phase_coupling() for the analogous
      false-similarity problem (mean(cos(Δφ)) over-collapses before
      comparing; this compares per-dimension first).
  (c) causal discourse marker bonus — surface forms from
      data/operator_cards/individual/because.yaml (PL: bo/ponieważ/gdyż,
      EN: because/since) found in the text between two windows.

Deliberately out of scope (see glittery-wondering-platypus.md plan): a
concession/contrast card (jednak/however) doesn't exist yet in the LNS
repo — the graph starts with only the causal signal + proximity + phase
coupling.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

import hashlib
import json
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

from ciel_geometry.concept_windows import ConceptWindow

_GRAPHS_OUT = Path("/media/adrian/New Volume/CIEL_memories/state/concept_graphs")

# Causal surface forms lifted directly from because.yaml — see module
# docstring. Loaded as a flat set (PL+EN) since the graph doesn't need to
# know WHICH language matched, only that a causal marker is present.
_CAUSAL_MARKERS = {"bo", "ponieważ", "gdyż", "because", "since"}
_WORD_RE = re.compile(r"[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+")


@dataclass
class ConceptNode:
    """One concept window, encoded for graph relations."""
    index: int
    text: str
    sentence_range: tuple[int, int]
    vector: np.ndarray  # 36D, from fast_encode_text() — encoder unchanged


@dataclass
class ConceptEdge:
    a: int  # ConceptNode.index
    b: int
    weight: float
    proximity: float
    phase_coupling: float
    has_causal_marker: bool
    horizon_class: str  # "open" | "SEALED" — see build_concept_graph()


def build_concept_nodes(windows: list[ConceptWindow]) -> list[ConceptNode]:
    """Encode each window's text into a 36D vector, in window order."""
    from ciel_geometry.cielingo_phase_encoder import fast_encode_text

    return [
        ConceptNode(
            index=i,
            text=w.window_text,
            sentence_range=w.sentence_range,
            vector=fast_encode_text(w.window_text),
        )
        for i, w in enumerate(windows)
    ]


def _proximity(node_a: ConceptNode, node_b: ConceptNode) -> float:
    """1/(1+gap) between the two windows' sentence ranges — 1.0 for
    adjacent/overlapping windows, decaying for windows far apart in the
    source text."""
    a_start, a_end = node_a.sentence_range
    b_start, b_end = node_b.sentence_range
    if a_end < b_start:
        gap = b_start - a_end
    elif b_end < a_start:
        gap = a_start - b_end
    else:
        gap = 0  # overlapping ranges
    return round(1.0 / (1.0 + gap), 4)


def _phase_coupling(node_a: ConceptNode, node_b: ConceptNode) -> float:
    """Kuramoto order parameter |mean(exp(i·Δφ))| — same math as
    phasenav_learning_gate.py::_vector_phase_coupling(), reused here so the
    concept graph doesn't fall into the same false-high-similarity trap
    (comparing per-dimension before collapsing to a scalar)."""
    diff = node_a.vector - node_b.vector
    return round(float(np.abs(np.mean(np.exp(1j * diff)))), 4)


def _has_causal_marker(between_text: str) -> bool:
    tokens = {t.lower() for t in _WORD_RE.findall(between_text)}
    return bool(tokens & _CAUSAL_MARKERS)


def build_concept_graph(
    nodes: list[ConceptNode],
    *,
    source_text: str = "",
    proximity_weight: float = 0.4,
    phase_weight: float = 0.4,
    causal_bonus: float = 0.2,
    unseal_threshold: float | None = None,
) -> list[ConceptEdge]:
    """Build weighted edges between every pair of concept nodes. O(n^2) over
    windows in one document — fine at concept-window scale (single-digit to
    low-double-digit windows per document, same order as card_tag_algebra's
    tag count, not the full corpus).

    Phase gate (2026-07-11, Adrian's direct architectural correction): every
    other phase-relation structure in this system (phasenav_learning_gate.py's
    SEALED/open horizon_class, orch_orbital.py's SEALED entities) is a real
    threshold GATE, not just a continuous score — an edge is either admitted
    to the graph's navigable structure or held SEALED (present in the data,
    excluded from traversal/aggregation) until its phase_coupling earns it
    back in. This graph was missing that; a continuous weight alone is
    architecturally inconsistent with the rest of NOEMA's phase-relation
    modules. Reuses UNSEAL_THRESHOLD directly from phasenav_learning_gate.py
    rather than inventing a second threshold constant."""
    if unseal_threshold is None:
        from ciel_sot_agent.phasenav_learning_gate import UNSEAL_THRESHOLD
        unseal_threshold = UNSEAL_THRESHOLD

    edges: list[ConceptEdge] = []
    for i, node_a in enumerate(nodes):
        for node_b in nodes[i + 1:]:
            proximity = _proximity(node_a, node_b)
            phase = _phase_coupling(node_a, node_b)

            has_marker = False
            if source_text and node_a.text in source_text and node_b.text in source_text:
                start = source_text.find(node_a.text)
                end = source_text.find(node_b.text)
                if start != -1 and end != -1 and start < end:
                    has_marker = _has_causal_marker(source_text[start:end])

            weight = proximity_weight * proximity + phase_weight * phase
            if has_marker:
                weight += causal_bonus
            weight = round(min(1.0, weight), 4)

            horizon_class = "open" if phase >= unseal_threshold else "SEALED"

            edges.append(ConceptEdge(
                a=node_a.index, b=node_b.index, weight=weight,
                proximity=proximity, phase_coupling=phase,
                has_causal_marker=has_marker, horizon_class=horizon_class,
            ))
    return edges


def open_edges(edges: list[ConceptEdge]) -> list[ConceptEdge]:
    """Edges admitted to navigable structure — excludes SEALED. Any future
    traversal/aggregation over the concept graph should go through this,
    not the raw edge list, mirroring how phasenav_learning_gate.py treats
    SEALED entries as admitted-but-isolated rather than deleting them."""
    return [e for e in edges if e.horizon_class == "open"]


def partition_concepts(
    nodes: list[ConceptNode],
    edges: list[ConceptEdge],
    *,
    coupling_attr: str = "weight",
    steps: int = 4000,
    dt: float = 0.01,
    n_restarts: int = 20,
    seed: int = 0,
) -> dict[str, Any]:
    """Split concept windows into two groups via anti-phase Kuramoto
    relaxation over the graph's OPEN edges — the exact mechanism validated
    in scripts/noema_experiment_kuramoto_maxcut.py (anti-phase Kuramoto
    coupling solving MAX-CUT correctly against brute-force ground truth:
    exact match on 6- and 10-node test graphs, 95% of optimum on a sparser
    13-node graph), applied here to real semantic nodes instead of an
    abstract test graph.

    Origin (2026-07-11): Adrian's framing — PhaseNav should be exactly this
    kind of general phase-coupling solver, but with semantics on the
    parameters that are explicit/legible to us instead of opaque generic
    spins. First test on a real (block-topic) document mixed the two
    topics rather than cleanly separating them — proximity dominates the
    default blended `weight` for windows that are textually adjacent
    regardless of topic. Adrian's answer, verbatim: "hybrydowo" — support
    BOTH the blended weight (proximity+phase+causal, the default, useful
    when adjacency itself is a meaningful signal) AND pure phase_coupling
    (useful for topic separation independent of text position, e.g.
    interleaved-topic documents) rather than picking one.

    Args:
        coupling_attr: "weight" (default, blended proximity+phase+causal)
            or "phase_coupling" (pure semantic phase relation, ignores
            textual adjacency — the mode to use when adjacency itself
            would confound the partition, e.g. interleaved topics).

    Only open_edges() feed the coupling matrix — SEALED edges (below
    UNSEAL_THRESHOLD) don't participate, matching how phase gates are
    treated everywhere else in this codebase (admitted-but-isolated, not
    deleted, but excluded from aggregation).

    Returns:
        dict with cut_weight (total open-edge coupling-attr crossing the
        partition), partition (tuple of 0/1 per node index), and the two
        groups' window texts for direct semantic inspection.
    """
    if coupling_attr not in ("weight", "phase_coupling"):
        raise ValueError(f"coupling_attr must be 'weight' or 'phase_coupling', got {coupling_attr!r}")

    n = len(nodes)
    if n == 0:
        return {"cut_weight": 0.0, "partition": (), "group_a": [], "group_b": []}
    if n == 1:
        return {"cut_weight": 0.0, "partition": (0,), "group_a": [nodes[0].text], "group_b": []}

    admitted = open_edges(edges)
    K = np.zeros((n, n))
    for e in admitted:
        strength = getattr(e, coupling_attr)
        K[e.a, e.b] = K[e.b, e.a] = -strength  # antiferromagnetic coupling

    rng = np.random.default_rng(seed)
    best_cut = -1.0
    best_bits: tuple[int, ...] = tuple([0] * n)

    for _ in range(n_restarts):
        phi = rng.uniform(0, 2 * np.pi, n)
        for _ in range(steps):
            diff = phi[None, :] - phi[:, None]  # phi_j - phi_i
            force = np.sum(K * np.sin(diff), axis=1)
            phi = (phi + dt * force) % (2 * np.pi)

        mean_phi = np.angle(np.mean(np.exp(1j * phi)))
        bits = tuple(int(((p - mean_phi) % (2 * np.pi)) > np.pi) for p in phi)
        cut = sum(getattr(e, coupling_attr) for e in admitted if bits[e.a] != bits[e.b])

        if cut > best_cut:
            best_cut = cut
            best_bits = bits

    group_a = [nodes[i].text for i in range(n) if best_bits[i] == 0]
    group_b = [nodes[i].text for i in range(n) if best_bits[i] == 1]

    return {
        "cut_weight": round(best_cut, 4),
        "coupling_attr": coupling_attr,
        "n_open_edges": len(admitted),
        "partition": best_bits,
        "group_a": group_a,
        "group_b": group_b,
    }


def write_concept_graph(
    document_id: str,
    nodes: list[ConceptNode],
    edges: list[ConceptEdge],
) -> Path:
    """Persist the graph as JSON, keyed by a hash of document_id — same
    output-location pattern as card_tag_algebra.py's cluster cache."""
    _GRAPHS_OUT.mkdir(parents=True, exist_ok=True)
    doc_hash = hashlib.sha256(document_id.encode("utf-8")).hexdigest()[:16]
    path = _GRAPHS_OUT / f"{doc_hash}.json"
    payload = {
        "document_id": document_id,
        "generated_at": time.time(),
        "n_nodes": len(nodes),
        "nodes": [
            {"index": n.index, "text": n.text[:200], "sentence_range": list(n.sentence_range)}
            for n in nodes
        ],
        "n_open_edges": len(open_edges(edges)),
        "edges": [
            {
                "a": e.a, "b": e.b, "weight": e.weight,
                "proximity": e.proximity, "phase_coupling": e.phase_coupling,
                "has_causal_marker": e.has_causal_marker,
                "horizon_class": e.horizon_class,
            }
            for e in edges
        ],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


if __name__ == "__main__":
    from ciel_geometry.concept_windows import build_concept_windows

    sample = (
        "Czy 2+2 to 4? To pytanie testowe. "
        "PhaseMemory przechowuje wektory 36D. Każdy wektor reprezentuje tekst. "
        "Dzisiaj naprawiłem kilka bugów w systemd, bo chmod nie działał na NTFS."
    )
    windows = build_concept_windows(sample)
    nodes = build_concept_nodes(windows)
    edges = build_concept_graph(nodes, source_text=sample)
    for e in edges:
        print(f"{e.a}-{e.b} weight={e.weight} prox={e.proximity} phase={e.phase_coupling} causal={e.has_causal_marker} horizon={e.horizon_class}")
    print(f"\nopen edges: {len(open_edges(edges))}/{len(edges)}")
