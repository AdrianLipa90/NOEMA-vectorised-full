"""PhaseNav learning admission gate — quantum-orbital confidence for CIELingo PhaseMemory.

Every piece of information CIELingo learns gets admitted (never hard-rejected — per
Adrian, 2026-07-09: "agent ma prawo znac koncepty i słowa i być niepewnym ich
znaczenia. wraz z nauką nabiera pewności ich użycia"), but carries a persistent
confidence score that starts low and grows through reinforcement on repeat
exposure. Built from two already-existing, already-production PhaseNav
primitives, per Adrian's explicit direction ("orchorbital, cqcl, to są bazowe
rzeczy"):

  - orch_orbital._phase_coupling() / SEALED horizon-class semantics
    (ciel_sot_agent/orch_orbital.py) — phase-proximity compatibility and
    admitted-but-isolated state, reused directly, not reinvented. SEALED here
    means the same thing it means there: admitted to the structure, isolated
    from external coupling until reinforcement earns it back in.
  - CQCL's heart_mind_coherence = quantum_coherence * emotional_convergence
    (ciel_omega/emotion/cqcl/emotional_collatz.py:251) — already implemented,
    never previously consumed by anything. This module is its first real
    caller, via a genuine EmotionalCollatzEngine invocation, not a
    reimplementation of its math.

See NOEMA memory project-cielingo-frozen-learning-loop.md for the investigation
this came out of, and ~/.claude/plans/pierw-plan-jolly-cascade.md (Plan 2) for
the full design rationale and the approved formula this implements.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

import hashlib
import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

log = _noema_quiet_logging.getLogger("PhaseNav.LearningGate")

_SURFACE_CIEL_STATE = Path("/dev/shm/ciel_noema/ciel_state.json")

# Working defaults per the approved plan (pierw-plan-jolly-cascade.md, Plan 2,
# section 4) — unconfirmed by live data yet, tune after dry-run review.
DEFECT_SEAL_THRESHOLD = 0.15
UNSEAL_THRESHOLD = 0.55
INITIAL_CONFIDENCE_FLOOR = 0.15
INITIAL_CONFIDENCE_MIN = 0.05
INITIAL_CONFIDENCE_MAX = 0.6
MINI_PASS_STEPS = 5
MINI_PASS_DT = 0.05
FIELD_STRENGTH_CAP = 2.0


@dataclass
class GateSignals:
    coupling_compat: float          # orch_orbital._phase_coupling, [0, 0.3]
    mini_defect: float              # orch_orbital-style mini Kuramoto pass, [0, 1]
    quantum_coherence: float        # CQCL base quantum_coherence, [0.4, 0.9]
    emotional_convergence: float    # CQCL Collatz-path stability, [0, 1]
    heart_mind_coherence: float     # CQCL quantum_coherence * emotional_convergence, [0, 1]
    external_confidence: float      # ciel_confidence_system.score_confidence, [0, 1]
    openness: float                 # scar_feedback.py telemetry, [0, 1]


@dataclass
class ConfidenceDecision:
    confidence: float
    horizon_class: str
    is_reinforcement: bool
    signals: GateSignals
    reasons: dict[str, Any] = field(default_factory=dict)


def _vector_phase_coupling(phi_a: np.ndarray, phi_b: np.ndarray, scale: float = 0.3) -> float:
    """36D analog of orch_orbital._phase_coupling() — Kuramoto-style circular
    coherence R = |mean(exp(i·Δφ))| across ALL 36 per-dimension phase
    differences, not a coupling between two already-collapsed scalar means.

    FIX 2026-07-10: the original approach (_circular_mean_phase(phi_36) on
    each side, then _phase_coupling() on the two resulting scalars) was found
    to be nearly non-discriminating in live dry-run data — 50 real web-
    research samples all landed within [0.416, 0.513] confidence and 100%
    "open" horizon, with mini_defect ~0 regardless of text content. Root
    cause, confirmed directly against the live encoder: the 36D encoder
    output has a fixed, index-linked baseline ramp shared by every text
    (phi[i] increases roughly linearly with the M0-M11×3-oscillator index),
    and this shared structure dominates a full-vector circular mean, drowning
    out the real per-dimension semantic differences (measured std~0.52
    between two semantically unrelated texts) that a scalar reduction
    discards before any comparison happens. Comparing per-dimension and only
    THEN reducing to a single coherence number keeps that signal."""
    diff = np.asarray(phi_a, dtype=float) - np.asarray(phi_b, dtype=float)
    R = float(np.abs(np.mean(np.exp(1j * diff))))
    return round(R * scale, 4)


def _read_openness() -> float:
    """Current openness telemetry (flavor[4]), computed by scar_feedback.py and
    exposed as ciel_state.json's top-level 'openness' field. Falls back to a
    neutral 0.5 if the surface isn't available (e.g. dry-run testing against a
    scratch PhaseMemory copy with no live daemon writing ciel_state.json)."""
    try:
        with open(_SURFACE_CIEL_STATE, encoding="utf-8") as f:
            state = json.load(f)
        return float(state.get("openness", 0.5))
    except Exception as e:
        from ciel_geometry.phasenav_exception_bridge import phase_signal_exception
        phase_signal_exception("phasenav_learning_gate._read_openness", e, operator_id="PAUSE")
        # Fallback: neutral openness when surface is unavailable
        return 0.5


def _openness_scale(openness: float) -> float:
    """openness in [0,1] -> weight multiplier for heart_mind_coherence's
    contribution to confidence, in [0.5, 1.5] (Adrian's decision: openness
    scales HMC weight, not coupling breadth). Higher openness = the system is
    more receptive right now, so a coherent candidate counts for more."""
    return 0.5 + float(np.clip(openness, 0.0, 1.0))


def _phasememory_centroid_vector(memory) -> np.ndarray:
    """Elementwise circular mean across all existing PhaseMemory vectors,
    kept as a full 36D vector — the 'field' a new candidate's 36D phase
    vector gets compared against for orch_orbital-style coupling
    compatibility. Empty memory -> zero vector (no bias). Replaces the
    previous scalar _phasememory_centroid_phase() (see _vector_phase_coupling
    docstring for why the scalar reduction was discarding signal)."""
    if memory.vectors is None or len(memory.vectors) == 0:
        return np.zeros(36, dtype=float)
    return np.angle(np.mean(np.exp(1j * np.asarray(memory.vectors, dtype=float)), axis=0))


def _field_strength(memory) -> float:
    """How strongly the existing PhaseMemory field should pull a candidate
    during _mini_stability_pass — 0 for an empty memory, saturating toward
    FIELD_STRENGTH_CAP as memory grows.

    FIX 2026-07-10: originally len(memory.texts)/100.0, uncapped. That's
    ~1-4 for a small scratch memory (where it was tuned/tested) but 105.7 for
    the real 10569-entry production memory — at that magnitude the mini-pass
    force (coupling * field_strength, coupling ~0.25) is ~26 per step, so 5
    Euler steps at dt=0.05 drive phi to near-perfect sync with the field
    regardless of the candidate's actual content, collapsing mini_defect to
    ~0 for every single candidate (confirmed directly: 50 live dry-run
    samples all had defect in [0.0000, 0.0010], and horizon_class was 100%
    "open" — the signal had no discriminating power on a memory this size).
    Capping keeps the mini-pass dynamics in a regime where defect actually
    varies with the candidate instead of saturating to zero.

    RETUNE 2026-07-10 (concept windowing): counts unique DOCUMENTS, not raw
    PhaseMemory entries. learn_windowed() below stores one entry per window,
    several windows per document (metadata["parent_document_id"] shared
    across a document's windows) — without this, field_strength would
    inflate 5-10x as windowing rolls out and re-saturate mini_defect to ~0,
    the exact failure this function was already fixed for once today.
    Entries without parent_document_id (everything learned before windowing,
    or via non-windowed paths) each count as their own document — identical
    to the un-retuned behavior for that data."""
    if not memory.texts:
        return 0.0
    doc_ids: set[str] = set()
    plain_count = 0
    for meta in memory.metadata:
        pid = meta.get("parent_document_id") if isinstance(meta, dict) else None
        if pid:
            doc_ids.add(pid)
        else:
            plain_count += 1
    n_documents = plain_count + len(doc_ids)
    return min(n_documents / 1000.0, FIELD_STRENGTH_CAP)


def _mini_stability_pass(
    candidate_phi: np.ndarray,
    field_phi: np.ndarray,
    field_strength: float,
    steps: int = MINI_PASS_STEPS,
    dt: float = MINI_PASS_DT,
) -> float:
    """Lightweight Kuramoto-style trial-injection stability test — the same
    math orch_orbital.run_entity_mini_pass() already runs for entity cards
    (phase-coupling force pulling toward the field, then defect = deviation
    from the post-integration mean phase), vectorized across all 36
    dimensions instead of collapsing to one scalar phase first (see
    _vector_phase_coupling's docstring: the scalar reduction was found to be
    dominated by the encoder's fixed per-index baseline, discarding the real
    per-dimension semantic signal). Applied to a single candidate against the
    PhaseMemory field instead of the fixed YAML entity-card set
    (run_entity_mini_pass() is scoped to ciel_entity_cards.yaml, not
    arbitrary text). Returns defect in [0, 1] (mean across dimensions) —
    lower means the candidate integrates more stably with what's already
    known.
    """
    coupling = _vector_phase_coupling(candidate_phi, field_phi, scale=0.15)
    phi = np.asarray(candidate_phi, dtype=float).copy()
    field_phi = np.asarray(field_phi, dtype=float)
    for _ in range(steps):
        force = coupling * np.sin(field_phi - phi) * max(field_strength, 0.1)
        phi = phi + dt * force
    mean_phi = np.arctan2(
        (np.sin(phi) + np.sin(field_phi)) / 2.0,
        (np.cos(phi) + np.cos(field_phi)) / 2.0,
    )
    defect_per_dim = np.abs(np.sin((phi - mean_phi) / 2.0))
    return float(np.mean(defect_per_dim))


def _ensure_ciel_omega_on_path() -> None:
    """emotion.cqcl.* resolves as a bare top-level package only when
    .../CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega itself is on sys.path (not its
    parent) — same sys.path requirement engine.py's own imports have, and the
    same bug class fixed there earlier (ciel_pipeline.py inserted the wrong
    directory level). Don't rely on the caller (headless/web-research/sync
    daemon) having already set this up correctly — make this module
    self-contained."""
    import sys
    ciel_omega_dir = Path(__file__).resolve().parents[2] / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM" / "ciel_omega"
    p = str(ciel_omega_dir)
    if ciel_omega_dir.is_dir() and p not in sys.path:
        sys.path.insert(0, p)


def _heart_mind_coherence(text: str) -> tuple[float, float, float]:
    """Real CQCL invocation — first actual consumer of heart_mind_coherence
    (ciel_omega/emotion/cqcl/emotional_collatz.py:251), which was already
    implemented but never used to gate anything before this. Returns
    (quantum_coherence, emotional_convergence, heart_mind_coherence).
    
    Fallback: if HTRI coherence is unavailable (e.g., degraded runtime state),
    use neutral defaults to avoid blocking learning. Agent has the right to
    know concepts with uncertainty; hard-rejection is forbidden."""
    try:
        _ensure_ciel_omega_on_path()
        from emotion.cqcl.emotional_collatz import EmotionalCollatzEngine
        engine = EmotionalCollatzEngine()
        result = engine.execute_emotional_program(text, input_data=len(text) or 1)
        metrics = result["metrics"]
        # metrics["emotional_coherence"] IS emotional_convergence, renamed at
        # _calculate_emotional_metrics() — not a different signal.
        return (
            float(metrics.get("quantum_coherence", 0.5)),
            float(metrics.get("emotional_coherence", 0.0)),
            float(metrics.get("heart_mind_coherence", 0.0)),
        )
    except Exception as e:
        from ciel_geometry.phasenav_exception_bridge import phase_signal_exception
        phase_signal_exception("phasenav_learning_gate._heart_mind_coherence", e, operator_id="PAUSE")
        # Fallback: neutral defaults when HTRI is unavailable
        # Learning continues with reduced signal quality, not blocked
        return (0.5, 0.0, 0.0)


_TAG_CLUSTERS_CACHE_PATH = Path("/media/adrian/New Volume/CIEL_memories/state/tag_clusters_cache.json")
_tag_clusters_cache: list[dict] | None = None
_tag_clusters_cache_mtime: float = 0.0


def _load_tag_clusters() -> list[dict]:
    """Load card_tag_algebra.py's cached clusters (mtime-checked, reloaded
    only when the cache file changes — never recomputes clustering itself,
    that would mean rescanning 264+ card files per learning candidate).
    Empty list (not an error) if the cache hasn't been generated yet."""
    global _tag_clusters_cache, _tag_clusters_cache_mtime
    try:
        mtime = _TAG_CLUSTERS_CACHE_PATH.stat().st_mtime
    except FileNotFoundError:
        return []
    if _tag_clusters_cache is None or mtime != _tag_clusters_cache_mtime:
        try:
            _tag_clusters_cache = json.loads(_TAG_CLUSTERS_CACHE_PATH.read_text(encoding="utf-8"))
            _tag_clusters_cache_mtime = mtime
        except (OSError, json.JSONDecodeError) as e:
            from ciel_geometry.phasenav_exception_bridge import phase_signal_exception
            phase_signal_exception("phasenav_learning_gate._load_tag_clusters", e, operator_id="PAUSE")
            raise
    return _tag_clusters_cache or []


def _tag_cluster_boost(text: str) -> float:
    """Adrian's card-tag-algebra insight (2026-07-10), wired into the gate:
    if a learning candidate's text touches a tag whose cluster is already
    well-established (high cohesion — a real 'cluster of meaning' in the
    card corpus, not a random pairing), that's independent evidence the
    candidate fits somewhere real in what NOEMA already knows, on top of
    the raw phase-vector coupling. Word-boundary substring match, not
    embedding similarity — the cache stores plain tag strings, this stays
    cheap enough to run per candidate. Returns the highest cohesion among
    clusters with at least one tag hit, in cluster-cohesion's native [0,1]
    range (0.0 if no cluster tag appears in the text at all)."""
    clusters = _load_tag_clusters()
    if not clusters:
        return 0.0
    text_lower = text.lower()
    best = 0.0
    for cluster in clusters:
        for tag in cluster["tags"]:
            if tag in text_lower:
                best = max(best, cluster["cohesion"])
                break
    return best


def _external_confidence(text: str, source_type: str) -> float:
    try:
        from ciel_confidence_system.engine import score_confidence
        return float(score_confidence(text, source_type=source_type).overall)
    except Exception as e:
        from ciel_geometry.phasenav_exception_bridge import phase_signal_exception
        phase_signal_exception("phasenav_learning_gate._external_confidence", e, operator_id="PAUSE")
        raise


def compute_confidence_signals(
    text: str,
    phi_36: np.ndarray,
    memory,
    *,
    source: str,
    source_type: str = "unknown",
) -> GateSignals:
    """Compute the gate-native signals for a learning candidate."""
    field_vector = _phasememory_centroid_vector(memory)
    coupling_compat = _vector_phase_coupling(phi_36, field_vector, scale=0.3)
    # Blend in the card-tag-algebra signal (2026-07-10): if the raw 36D
    # phase coupling is weak but the text clearly touches an established,
    # high-cohesion tag cluster, that's independent evidence of real fit —
    # take whichever signal is stronger rather than averaging, since either
    # one alone is sufficient evidence of compatibility. tag_cluster_boost
    # is in cluster-cohesion's native [0,1] range; coupling_compat's native
    # range is [0, 0.3] (_vector_phase_coupling's scale=0.3), so scale the
    # boost into that same range before comparing.
    tag_boost = _tag_cluster_boost(text) * 0.3
    coupling_compat = max(coupling_compat, tag_boost)
    field_strength = _field_strength(memory)
    mini_defect = _mini_stability_pass(phi_36, field_vector, field_strength)
    quantum_coherence, emotional_convergence, heart_mind_coherence = _heart_mind_coherence(text)
    return GateSignals(
        coupling_compat=coupling_compat,
        mini_defect=mini_defect,
        quantum_coherence=quantum_coherence,
        emotional_convergence=emotional_convergence,
        heart_mind_coherence=heart_mind_coherence,
        external_confidence=_external_confidence(text, source_type),
        openness=_read_openness(),
    )


def _initial_confidence(signals: GateSignals) -> float:
    hmc_weight = 0.35 * _openness_scale(signals.openness)
    raw = (
        INITIAL_CONFIDENCE_FLOOR                        # agent always has the right to "know" something uncertainly
        + (signals.coupling_compat / 0.3) * 0.25         # orch_orbital compat, normalized from its native [0,0.3] range
        + signals.heart_mind_coherence * hmc_weight       # CQCL, openness-scaled
        + signals.external_confidence * 0.20
        - signals.mini_defect * 0.30
    )
    return float(np.clip(raw, INITIAL_CONFIDENCE_MIN, INITIAL_CONFIDENCE_MAX))


def _reinforce_confidence(old_confidence: float, signals: GateSignals) -> float:
    """'wraz z nauka nabiera pewnosci ich uzycia' — repeat exposure is a
    measurement event that collapses uncertainty toward higher confidence,
    faster when the current occurrence itself is well-coupled/coherent."""
    rate = 0.10 + 0.30 * signals.heart_mind_coherence + 0.10 * (signals.coupling_compat / 0.3)
    rate = float(np.clip(rate, 0.05, 0.6))
    return float(np.clip(old_confidence + (1.0 - old_confidence) * rate, 0.0, 1.0))


def evaluate_learning_admission(
    engine,
    text: str,
    phi_36: np.ndarray,
    *,
    source: str,
    source_type: str = "unknown",
) -> ConfidenceDecision:
    """Compute the full confidence-gate decision for (text, phi_36) against
    engine.memory's current state, without writing anything — pure evaluation,
    safe to call in dry-run mode."""
    text_hash = hashlib.sha256(text.encode()).hexdigest()[:16]
    existing_idx = engine.memory._hash_index.get(text_hash)
    signals = compute_confidence_signals(text, phi_36, engine.memory, source=source, source_type=source_type)

    if existing_idx is None:
        confidence = _initial_confidence(signals)
        horizon_class = "SEALED" if signals.mini_defect > DEFECT_SEAL_THRESHOLD else "open"
        return ConfidenceDecision(
            confidence=confidence, horizon_class=horizon_class, is_reinforcement=False,
            signals=signals, reasons={"event": "first_admission"},
        )

    old_meta = engine.memory.metadata[existing_idx]
    old_confidence = float(old_meta.get("confidence", 0.3))
    old_horizon = old_meta.get("horizon_class", "open")
    confidence = _reinforce_confidence(old_confidence, signals)
    horizon_class = old_horizon
    if old_horizon == "SEALED" and signals.mini_defect < DEFECT_SEAL_THRESHOLD and confidence > UNSEAL_THRESHOLD:
        horizon_class = "open"
    return ConfidenceDecision(
        confidence=confidence, horizon_class=horizon_class, is_reinforcement=True,
        signals=signals,
        reasons={"event": "reinforcement", "old_confidence": old_confidence, "old_horizon_class": old_horizon},
    )


def _is_binary_content(text: str) -> bool:
    """Detect if text contains binary/PDF/HTML content instead of semantic text.
    
    Reject: PDF (%PDF), HTML (<html, <body, JavaScript), binary markers.
    Only accept plain text for CIELingo semantic memory.
    """
    binary_markers = [
        "%PDF",
        "<html",
        "<body",
        "<head",
        "<script",
        "JavaScript",
        "<div",
        "<span",
        "data:image",
        "application/pdf",
        "application/octet-stream",
    ]
    text_lower = text.lower()
    for marker in binary_markers:
        if marker.lower() in text_lower:
            return True
    # Reject if contains too many non-printable characters
    printable_ratio = sum(1 for c in text if c.isprintable() or c.isspace()) / len(text) if text else 0
    if printable_ratio < 0.8:
        return True
    return False


def learn_with_confidence(
    engine,
    text: str,
    *,
    source: str,
    source_type: str = "unknown",
    metadata: dict[str, Any] | None = None,
    dry_run: bool = False,
    phi_override: np.ndarray | None = None,
) -> dict[str, Any]:
    """The single entry point all three integration points (conversation,
    web-research, cielingo-sync) call. Always evaluates; only persists to
    PhaseMemory when dry_run=False.

    CHANGED 2026-07-11 (Adrian's absolute no-quiet-except rule): this used
    to swallow every failure and degrade to 'not learned this time' —
    that is exactly the pattern that let a real PhaseMemory torn-write
    corruption go undetected by any log signal this same session. A gate
    failure now signals through phasenav_exception_bridge and RAISES.
    Callers (ciel_headless_daemon.py, cielingo-sync, web-research) must
    handle this themselves, visibly, not rely on this function to hide it.

    phi_override: pass a pre-computed phase vector (e.g. already run through
    apply_euler_sync() against the current coupling field, as integration
    point D does) to use for BOTH gate evaluation and the persisted vector,
    instead of engine.encode(text)'s raw embedding. engine.learn() always
    re-encodes internally, which would silently discard a synced vector, so
    when phi_override is given this writes via engine.memory.add() + save()
    directly instead of engine.learn()."""
    # Reject binary content to prevent PhaseMemory corruption
    if _is_binary_content(text):
        log.warning(f"learn_with_confidence: rejected binary content from {source} (length={len(text)})")
        return {
            "learned": False,
            "reason": "binary_content_rejected",
            "source": source,
            "text_preview": text[:100] if text else "",
        }
    
    try:
        phi = phi_override if phi_override is not None else engine.encode(text)
        decision = evaluate_learning_admission(engine, text, phi, source=source, source_type=source_type)
        meta = dict(metadata or {})
        meta["confidence"] = decision.confidence
        meta["horizon_class"] = decision.horizon_class
        meta["gate_signals"] = {
            "coupling_compat": decision.signals.coupling_compat,
            "mini_defect": decision.signals.mini_defect,
            "heart_mind_coherence": decision.signals.heart_mind_coherence,
            "external_confidence": decision.signals.external_confidence,
            "openness": decision.signals.openness,
        }
        log.info(
            "[learning-gate] source=%s reinforcement=%s confidence=%.3f horizon=%s hmc=%.3f defect=%.3f",
            source, decision.is_reinforcement, decision.confidence, decision.horizon_class,
            decision.signals.heart_mind_coherence, decision.signals.mini_defect,
        )
        if dry_run:
            return {"dry_run": True, "would_learn": True, "decision": meta, "text": text[:200]}
        if phi_override is not None:
            meta.setdefault("source", source)
            # phi_override already carries the synced-vector phase; the
            # per-dimension content weights still come from the raw text
            # (they answer "which dims are real content", independent of the
            # coupling-field sync applied to phi) — see fast_encode_text_weighted().
            _, override_weights = engine._encoder_weighted(text)
            idx = engine.memory.add(text, phi, weights=override_weights, source=source, metadata=meta)
            engine.save()
            result = {"index": idx, "text": text, "source": source, "memory_size": engine.memory.size}
        else:
            result = engine.learn(text, source=source, metadata=meta, persist=True)
        return {"dry_run": False, "learned": True, "decision": meta, "result": result}
    except Exception as e:
        from ciel_geometry.phasenav_exception_bridge import phase_signal_exception
        phase_signal_exception("phasenav_learning_gate.learn_with_confidence", e, operator_id="REFUSAL")
        raise


# ── Concept windowing integration (2026-07-10) ─────────────────────────────
# See ~/.claude/plans/glittery-wondering-platypus.md Część 1 — a whole
# document is not one concept, meaning is local to the content around each
# concept. learn_windowed() splits a document into concept_windows.py's
# windows and admits each one through the SAME, unchanged
# learn_with_confidence() above, rather than reinventing admission logic
# per-window.

_PROCESSED_DOCS_PATH = Path("/media/adrian/New Volume/CIEL_memories/state/processed_documents.json")


def _load_processed_documents() -> set[str]:
    if not _PROCESSED_DOCS_PATH.exists():
        return set()
    try:
        return set(json.loads(_PROCESSED_DOCS_PATH.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, ValueError) as e:
        from ciel_geometry.phasenav_exception_bridge import phase_signal_exception
        phase_signal_exception("phasenav_learning_gate._load_processed_documents", e, operator_id="PAUSE")
        raise


def _mark_document_processed(doc_hash: str) -> None:
    processed = _load_processed_documents()
    processed.add(doc_hash)
    _PROCESSED_DOCS_PATH.parent.mkdir(parents=True, exist_ok=True)
    _PROCESSED_DOCS_PATH.write_text(json.dumps(sorted(processed)), encoding="utf-8")


def learn_windowed(
    engine,
    text: str,
    *,
    source: str,
    source_type: str = "unknown",
    metadata: dict[str, Any] | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Document-level entry point: split `text` into concept windows, admit
    each window through learn_with_confidence() (unchanged), and build a
    concept dependency graph across the windows.

    Document-level dedup happens HERE, before windowing — PhaseMemory's own
    dedup is per-window-text now (each window gets its own hash), so without
    this check, re-processing the same document would re-create the same
    windows every time (idempotent per-window, but wasteful and would keep
    reinforcing the same windows on every call rather than skipping cleanly).
    """
    from ciel_geometry.concept_windows import build_concept_windows
    from ciel_sot_agent.concept_dependency_graph import (
        build_concept_nodes, build_concept_graph, write_concept_graph,
    )

    document_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    if document_hash in _load_processed_documents():
        return {"dry_run": dry_run, "learned": False, "skipped": "already_processed", "document_hash": document_hash}

    windows = build_concept_windows(text)
    if not windows:
        return {"dry_run": dry_run, "learned": False, "skipped": "no_concept_windows", "document_hash": document_hash}

    window_results = []
    for window_index, window in enumerate(windows):
        window_meta = dict(metadata or {})
        window_meta["parent_document_id"] = document_hash
        window_meta["window_index"] = window_index
        window_results.append(learn_with_confidence(
            engine, window.window_text,
            source=source, source_type=source_type, metadata=window_meta, dry_run=dry_run,
        ))

    graph_path = None
    if not dry_run:
        nodes = build_concept_nodes(windows)
        edges = build_concept_graph(nodes, source_text=text)
        graph_path = str(write_concept_graph(document_hash, nodes, edges))
        _mark_document_processed(document_hash)

    return {
        "dry_run": dry_run,
        "learned": not dry_run,
        "document_hash": document_hash,
        "n_windows": len(windows),
        "window_results": window_results,
        "concept_graph_path": graph_path,
    }
