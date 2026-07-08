"""Idle-time book consolidation for the sleep mode braid.

The intent here is explicit:
- analyse book-like sources when the system is quiet,
- digest them through the existing cognitive book analysis pipeline,
- evaluate pairwise holonomy / coherence,
- promote the stabilized corpus into a higher memory layer only when the gate is open.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable, Sequence
import json
import math
import os
from datetime import datetime, timezone

from .cognitive_book_analysis import CorpusAnalysis, analyze_corpus

DEFAULT_SLEEP_REPORT_ROOT = Path.home() / "CIEL_memories" / "sleep_consolidation"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _utc_now_epoch() -> float:
    return datetime.now(timezone.utc).timestamp()


def _bounded(value: float) -> float:
    if not math.isfinite(value):
        return 0.0
    return max(0.0, min(1.0, float(value)))


def _sha256_text(text: str) -> str:
    import hashlib

    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _norm_load(load_avg: float | None = None, cpu_count: int | None = None) -> float:
    if load_avg is None:
        try:
            load_avg = os.getloadavg()[0]
        except Exception:
            load_avg = 0.0
    if cpu_count is None:
        cpu_count = os.cpu_count() or 1
    return max(0.0, float(load_avg) / max(float(cpu_count), 1.0))


def default_sleep_corpus_paths() -> list[Path]:
    pobrane = Path("/home/adrian/Pobrane")
    return [
        pobrane / "HTRI_FULL_WORKING_PROTOTYPE_i7_LATEX.pdf",
        pobrane / "Law_and_Order__The_Intention_of_Obligation.pdf",
        pobrane / "Love_and_War__The_Axis_of_Phase_Intention.pdf",
        pobrane / "TheArchitectureofCoherenceSymbolicSystemsPhaseIntentionandtheMathematicsofEthicalIntegration.pdf",
    ]


def _existing_paths(paths: Iterable[str | Path]) -> list[Path]:
    out: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.exists():
            out.append(path)
    return out


def _pairwise_holonomy_score(corpus: CorpusAnalysis) -> float:
    if not corpus.pairwise:
        return 0.0
    tensor_cosines = [float(item.get("tensor_cosine", 0.0)) for item in corpus.pairwise]
    normalized = [(_bounded((value + 1.0) / 2.0)) for value in tensor_cosines]
    return float(sum(normalized) / max(len(normalized), 1))


def _promotion_score(corpus: CorpusAnalysis) -> float:
    mean_meaning = float(corpus.summary.get("mean_meaning_scalar", 0.0))
    mean_capacity = float(corpus.summary.get("mean_transport_capacity", 0.0))
    mean_coherence = float(corpus.summary.get("mean_berry_coherence", 0.0))
    mean_recursion = float(corpus.summary.get("mean_recursive_score", 0.0))
    holonomy = _pairwise_holonomy_score(corpus)
    score = (
        0.28 * _bounded(mean_meaning)
        + 0.24 * _bounded(mean_capacity)
        + 0.22 * _bounded(mean_coherence)
        + 0.16 * _bounded(1.0 - mean_recursion)
        + 0.10 * _bounded(holonomy)
    )
    return _bounded(score)


def _idle_gate(idle_threshold: float, load_avg: float | None = None, cpu_count: int | None = None) -> dict[str, Any]:
    normalized_load = _norm_load(load_avg=load_avg, cpu_count=cpu_count)
    return {
        "load_avg": float(load_avg if load_avg is not None else (os.getloadavg()[0] if hasattr(os, "getloadavg") else 0.0)),
        "cpu_count": int(cpu_count if cpu_count is not None else (os.cpu_count() or 1)),
        "normalized_load": round(normalized_load, 6),
        "idle_threshold": float(idle_threshold),
        "idle_ready": normalized_load <= idle_threshold,
    }


@dataclass(slots=True)
class SleepConsolidationReport:
    schema: str
    created_at: str
    corpus_label: str
    idle_gate: dict[str, Any]
    promotion_score: float
    promotion_gate: str
    corpus: dict[str, Any] | None
    report_root: str
    notes: list[str]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def analyze_sleep_mode_corpus(
    paths: Sequence[str | Path] | None = None,
    *,
    corpus_label: str = "sleep_books",
    store_memory: bool = True,
    report_root: Path | None = None,
    idle_threshold: float = 0.35,
    allow_busy: bool = False,
    load_avg: float | None = None,
    cpu_count: int | None = None,
) -> dict[str, Any]:
    chosen_paths = _existing_paths(paths or default_sleep_corpus_paths())
    notes: list[str] = []
    if not chosen_paths:
        notes.append("no_existing_paths")
        report = SleepConsolidationReport(
            schema="ciel/sleep-consolidation/v0.1",
            created_at=_utc_now_iso(),
            corpus_label=corpus_label,
            idle_gate=_idle_gate(idle_threshold, load_avg=load_avg, cpu_count=cpu_count),
            promotion_score=0.0,
            promotion_gate="DEFER",
            corpus=None,
            report_root=str(report_root or DEFAULT_SLEEP_REPORT_ROOT),
            notes=notes,
        )
        return report.as_dict()

    idle_gate = _idle_gate(idle_threshold, load_avg=load_avg, cpu_count=cpu_count)
    if not idle_gate["idle_ready"] and not allow_busy:
        notes.append("deferred_until_idle")
        report = SleepConsolidationReport(
            schema="ciel/sleep-consolidation/v0.1",
            created_at=_utc_now_iso(),
            corpus_label=corpus_label,
            idle_gate=idle_gate,
            promotion_score=0.0,
            promotion_gate="DEFER",
            corpus=None,
            report_root=str(report_root or DEFAULT_SLEEP_REPORT_ROOT),
            notes=notes,
        )
        return report.as_dict()

    corpus = analyze_corpus(corpus_label, chosen_paths, store_memory=store_memory, report_root=report_root)
    score = _promotion_score(corpus)
    promotion_gate = "PASS" if score >= 0.55 else "REVIEW"

    if store_memory:
        try:
            from cielingo_core.phasenav.memory import MemoryStore

            store = MemoryStore()
            summary = dict(corpus.summary)
            summary.update(
                {
                    "promotion_score": round(score, 6),
                    "promotion_gate": promotion_gate,
                    "idle_ready": idle_gate["idle_ready"],
                    "normalized_load": idle_gate["normalized_load"],
                    "holonomy_score": round(_pairwise_holonomy_score(corpus), 6),
                    "sleep_mode": True,
                }
            )
            store.store(
                {
                    "schema": "cielingo/sleep-consolidation-entry/v0.1",
                    "timestamp": _utc_now_epoch(),
                    "turn_id": f"{corpus_label}:sleep_consolidation",
                    "session_id": f"sleep_books:{corpus_label}",
                    "prompt_hash": _sha256_text(f"sleep_mode:{corpus_label}"),
                    "response_hash": _sha256_text(json.dumps(summary, sort_keys=True)),
                    "orbit_vector": [
                        _bounded(score),
                        _bounded(corpus.summary.get("mean_meaning_scalar", 0.0)),
                        _bounded(corpus.summary.get("mean_transport_capacity", 0.0)),
                        _bounded(corpus.summary.get("mean_berry_coherence", 0.0)),
                        _bounded(corpus.summary.get("mean_recursive_score", 0.0)),
                        _bounded(_pairwise_holonomy_score(corpus)),
                        _bounded(idle_gate["normalized_load"]),
                        _bounded(len(corpus.sources) / 12.0),
                        _bounded(len(corpus.pairwise) / 12.0),
                        _bounded(sum(source.chunk_count for source in corpus.sources) / 400.0),
                        _bounded(len(corpus.summary.get("summary_terms", [])) / 40.0),
                    ],
                    "prompt_phase": score,
                    "response_phase": idle_gate["normalized_load"],
                    "chain_hash": _sha256_text(
                        f"{corpus_label}:{score}:{idle_gate['normalized_load']}:{len(corpus.sources)}:{len(corpus.pairwise)}"
                    ),
                    "tags": ["sleep-mode", "book-analysis", "holonomy", "consolidation", corpus_label],
                    "source_layer": "sleep_consolidation",
                    "card_id": corpus_label,
                    "card_kind": "sleep_corpus",
                    "concept_label": corpus_label,
                    "source_kind": "sleep_consolidation",
                    "memory_frame": {
                        "concept_id": corpus_label,
                        "label": corpus_label,
                        "source_kind": "sleep_consolidation",
                        "card_kind": "sleep_corpus",
                        "phase": score,
                        "scalar": corpus.summary.get("mean_meaning_scalar", 0.0),
                        "semantic_mass": corpus.summary.get("mean_meaning_scalar", 0.0),
                        "orbit_vector": [
                            _bounded(score),
                            _bounded(corpus.summary.get("mean_meaning_scalar", 0.0)),
                            _bounded(corpus.summary.get("mean_transport_capacity", 0.0)),
                            _bounded(corpus.summary.get("mean_berry_coherence", 0.0)),
                            _bounded(corpus.summary.get("mean_recursive_score", 0.0)),
                            _bounded(_pairwise_holonomy_score(corpus)),
                            _bounded(idle_gate["normalized_load"]),
                            _bounded(len(corpus.sources) / 12.0),
                            _bounded(len(corpus.pairwise) / 12.0),
                            _bounded(sum(source.chunk_count for source in corpus.sources) / 400.0),
                            _bounded(len(corpus.summary.get("summary_terms", [])) / 40.0),
                        ],
                        "tags": ["sleep-mode", "book-analysis", "holonomy", "consolidation", corpus_label],
                    },
                }
            )
        except Exception as exc:
            notes.append(f"memory_store_failed:{type(exc).__name__}")

    report = SleepConsolidationReport(
        schema="ciel/sleep-consolidation/v0.1",
        created_at=_utc_now_iso(),
        corpus_label=corpus_label,
        idle_gate=idle_gate,
        promotion_score=round(score, 6),
        promotion_gate=promotion_gate,
        corpus=corpus.as_dict(),
        report_root=str(report_root or DEFAULT_SLEEP_REPORT_ROOT),
        notes=notes,
    )

    out_root = Path(report_root or DEFAULT_SLEEP_REPORT_ROOT)
    out_root.mkdir(parents=True, exist_ok=True)
    json_path = out_root / f"{corpus_label}.sleep-consolidation.noema.json"
    md_path = out_root / f"{corpus_label}.sleep-consolidation.noema.md"
    json_path.write_text(json.dumps(report.as_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_lines = [
        f"# {corpus_label} sleep consolidation",
        "",
        f"- Idle ready: {idle_gate['idle_ready']}",
        f"- Normalized load: {idle_gate['normalized_load']}",
        f"- Promotion score: {round(score, 6)}",
        f"- Promotion gate: {promotion_gate}",
        f"- Sources: {len(corpus.sources)}",
        f"- Pairwise holonomy score: {round(_pairwise_holonomy_score(corpus), 6)}",
        "",
        "## Notes",
    ]
    md_lines.extend(f"- {note}" for note in notes or ["none"])
    md_lines.append("")
    md_lines.append("## Source paths")
    for source in corpus.sources:
        md_lines.append(f"- `{source.source_path}`")
    md_path.write_text("\n".join(md_lines).strip() + "\n", encoding="utf-8")

    return report.as_dict()


def analyze_sleep_mode_default_corpus(**kwargs: Any) -> dict[str, Any]:
    return analyze_sleep_mode_corpus(**kwargs)


__all__ = [
    "DEFAULT_SLEEP_REPORT_ROOT",
    "SleepConsolidationReport",
    "default_sleep_corpus_paths",
    "analyze_sleep_mode_corpus",
    "analyze_sleep_mode_default_corpus",
]
