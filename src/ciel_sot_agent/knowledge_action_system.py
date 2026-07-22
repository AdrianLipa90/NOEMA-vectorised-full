"""Canonical NOEMA knowledge-to-action orchestrator.

The module is intentionally thin. It composes existing subsystem surfaces:
- local retrieval,
- CIELingo semantic framing,
- Doctor diagnostics,
- Sapiens policy,
- UI-friendly trace rendering.

The first version is read-only and deterministic. It produces a structured
decision trace instead of mutating state.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Callable

from .memory_rag import build_memory_context, search_chat_history, search_wave_archive
from .paths import resolve_project_root
from .sapiens_surface_policy import build_surface_policy


RetrievalBundle = dict[str, Any]
LingoBundle = dict[str, Any]
DoctorBundle = dict[str, Any]
PolicyBundle = dict[str, Any]


def _default_root() -> Path:
    return resolve_project_root(__file__)


def _lookup(payload: Any, key: str, default: Any = None) -> Any:
    if isinstance(payload, dict):
        return payload.get(key, default)
    return getattr(payload, key, default)


def collect_retrieval_bundle(text: str, root: str | Path | None = None, top_k: int = 4) -> RetrievalBundle:
    """Collect local evidence without mutating state."""
    root_path = Path(root).resolve() if root is not None else _default_root()
    wave_hits = search_wave_archive(text, root_path, top_k=top_k)
    chat_hits = search_chat_history(text, top_k=max(1, top_k - 1))
    memory_context = build_memory_context(text, root_path)
    total_hits = len(wave_hits) + len(chat_hits)
    return {
        "root": str(root_path),
        "wave_hits": wave_hits,
        "chat_hits": chat_hits,
        "memory_context": memory_context,
        "total_hits": total_hits,
        "evidence_strength": round(min(1.0, total_hits / max(1, top_k * 2)), 3),
    }


def _build_lingo_frame(text: str, *, ciel_state: dict[str, Any] | None = None, language: str | None = None) -> LingoBundle:
    from .cielingo_bridge import build_lingo_frame as _bridge_build_lingo_frame  # lazy import

    return _bridge_build_lingo_frame(text, ciel_state=ciel_state, language=language)


def _build_doctor_report(root: str | Path) -> DoctorBundle:
    from noema_holonomic_doctor import DoctorConfig, build_report  # lazy import

    report = build_report(Path(root), DoctorConfig(write=False))
    return report if isinstance(report, dict) else asdict(report)


def build_policy_bundle(control_profile: dict[str, Any] | None = None, truth_axis: str = "truth") -> PolicyBundle:
    """Build the Sapiens surface policy bundle."""
    return build_surface_policy(control_profile=control_profile, truth_axis=truth_axis)


def score_action(
    retrieval: RetrievalBundle,
    lingo: LingoBundle,
    doctor: DoctorBundle,
    policy: PolicyBundle,
) -> dict[str, Any]:
    """Convert evidence into a bounded decision."""
    binding_blocked = bool(_lookup(lingo, "binding_blocked", False))
    composition_valid = bool(_lookup(lingo, "composition_valid", True))
    projection_confidence = float(_lookup(lingo, "projection_confidence", 0.0) or 0.0)
    doctor_status = str(_lookup(doctor, "status", "UNKNOWN")).upper()
    policy_mode = str(_lookup(policy, "mode", "standard")).lower()
    retrieval_total = int(_lookup(retrieval, "total_hits", 0) or 0)

    signals: list[str] = []
    action = "allow"
    reason = "all_gates_clear"

    if binding_blocked:
        action = "block"
        reason = "binding_blocked"
        signals.append("binding_blocked")
    elif not composition_valid or projection_confidence < 0.35:
        action = "repair"
        reason = "lingo_invalid_or_low_confidence"
        signals.append("composition_invalid" if not composition_valid else "low_confidence")
    elif doctor_status == "FAIL":
        action = "repair"
        reason = "doctor_fail"
        signals.append("doctor_fail")
    elif policy_mode == "safe":
        action = "defer"
        reason = "safe_mode_read_only"
        signals.append("safe_mode")
    elif doctor_status == "WARN" or projection_confidence < 0.65 or retrieval_total == 0:
        action = "defer"
        reason = "needs_more_evidence"
        if doctor_status == "WARN":
            signals.append("doctor_warn")
        if projection_confidence < 0.65:
            signals.append("low_confidence")
        if retrieval_total == 0:
            signals.append("no_retrieval_hits")
    else:
        signals.append("ready")

    return {
        "action": action,
        "reason": reason,
        "signals": signals,
        "binding_blocked": binding_blocked,
        "composition_valid": composition_valid,
        "projection_confidence": round(projection_confidence, 3),
        "doctor_status": doctor_status,
        "policy_mode": policy_mode,
        "retrieval_total": retrieval_total,
    }


def _build_sapiens_bundle(policy: PolicyBundle, decision: dict[str, Any]) -> dict[str, Any]:
    return {
        "surface_policy": policy,
        "interaction_mode": policy.get("mode", "standard"),
        "truth_axis": policy.get("response_axis", "truth-aligned-user-intent"),
        "decision": decision["action"],
        "signals": decision["signals"],
    }


def build_ui_bundle(
    query: str,
    retrieval: RetrievalBundle,
    lingo: LingoBundle,
    doctor: DoctorBundle,
    policy: PolicyBundle,
    decision: dict[str, Any],
) -> dict[str, Any]:
    """Build a human-facing bundle for portal/UI rendering."""
    wave_hits = retrieval.get("wave_hits", []) if isinstance(retrieval, dict) else []
    chat_hits = retrieval.get("chat_hits", []) if isinstance(retrieval, dict) else []
    phase_nav = lingo.get("phase_nav", {}) if isinstance(lingo, dict) else {}
    retriever_summary = {
        "wave_hits": len(wave_hits),
        "chat_hits": len(chat_hits),
        "evidence_strength": retrieval.get("evidence_strength", 0.0),
    }
    doctor_summary = {
        "status": _lookup(doctor, "status", "UNKNOWN"),
        "finding_count": len(_lookup(doctor, "findings", []) or []),
        "manifest_files": _lookup(doctor, "file_count", 0),
    }
    policy_summary = {
        "mode": policy.get("mode", "standard"),
        "response_axis": policy.get("response_axis", "truth-aligned-user-intent"),
        "truth_over_smoothing": policy.get("truth_over_smoothing", True),
    }
    next_step = {
        "allow": "execute",
        "defer": "collect_more_evidence",
        "repair": "repair_surfaces",
        "block": "halt_and_review",
    }.get(decision["action"], "inspect")
    return {
        "headline": f"{decision['action'].upper()} :: {decision['reason']}",
        "query": query,
        "phase_nav": phase_nav,
        "retriever_summary": retriever_summary,
        "doctor_summary": doctor_summary,
        "policy_summary": policy_summary,
        "signals": decision["signals"],
        "suggested_next_step": next_step,
        "render_mode": "sapiens-panel",
    }


@dataclass(frozen=True)
class KnowledgeActionTrace:
    query: str
    root: str
    retrieval: RetrievalBundle
    lingo: LingoBundle
    doctor: DoctorBundle
    policy: PolicyBundle
    decision: dict[str, Any]
    sapiens: dict[str, Any]
    ui: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class KnowledgeActionSystem:
    root: Path = field(default_factory=_default_root)
    top_k: int = 4
    retriever: Callable[[str, str | Path | None, int], RetrievalBundle] = collect_retrieval_bundle
    lingo_builder: Callable[..., LingoBundle] = _build_lingo_frame
    doctor_builder: Callable[[str | Path], DoctorBundle] = _build_doctor_report
    policy_builder: Callable[[dict[str, Any] | None, str], PolicyBundle] = build_policy_bundle

    def run(
        self,
        text: str,
        *,
        control_profile: dict[str, Any] | None = None,
        ciel_state: dict[str, Any] | None = None,
        language: str | None = None,
    ) -> KnowledgeActionTrace:
        retrieval = self.retriever(text, self.root, self.top_k)
        lingo = self.lingo_builder(text, ciel_state=ciel_state, language=language)
        doctor = self.doctor_builder(self.root)
        policy = self.policy_builder(control_profile, "truth")
        decision = score_action(retrieval=retrieval, lingo=lingo, doctor=doctor, policy=policy)
        sapiens = _build_sapiens_bundle(policy, decision)
        ui = build_ui_bundle(text, retrieval, lingo, doctor, policy, decision)
        return KnowledgeActionTrace(
            query=text,
            root=str(self.root),
            retrieval=retrieval,
            lingo=lingo,
            doctor=doctor,
            policy=policy,
            decision=decision,
            sapiens=sapiens,
            ui=ui,
        )


def run_knowledge_action_system(
    text: str,
    *,
    root: str | Path | None = None,
    top_k: int = 4,
    control_profile: dict[str, Any] | None = None,
    ciel_state: dict[str, Any] | None = None,
    language: str | None = None,
    system: KnowledgeActionSystem | None = None,
) -> KnowledgeActionTrace:
    """Convenience wrapper for the canonical knowledge-to-action flow."""
    active_system = system or KnowledgeActionSystem(root=Path(root).resolve() if root is not None else _default_root(), top_k=top_k)
    return active_system.run(text, control_profile=control_profile, ciel_state=ciel_state, language=language)


__all__ = [
    "KnowledgeActionSystem",
    "KnowledgeActionTrace",
    "build_policy_bundle",
    "build_ui_bundle",
    "collect_retrieval_bundle",
    "run_knowledge_action_system",
    "score_action",
]
