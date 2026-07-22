from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from .gguf_backends import _immune_surface_brief, _phasenav_brief
from .language_backend import AuxiliaryBackend, LanguageBackend
from .memory_prompt_context import build_semantic_speech_context

if TYPE_CHECKING:
    from .llm_registry import LLMBackendBundle

_log = logging.getLogger(__name__)


def _coerce_role(role: str) -> str:
    key = (role or "").strip().lower()
    if key in {"system", "user", "assistant"}:
        return key
    return "user"


def _normalize_dialogue(dialogue: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    normalized: List[Dict[str, str]] = []
    for message in dialogue:
        if not isinstance(message, dict):
            continue
        normalized.append(
            {
                "role": _coerce_role(str(message.get("role", "user"))),
                "content": str(message.get("content", "")),
            }
        )
    return normalized


def _json_default(obj: Any) -> Any:
    try:
        import numpy as np  # noqa: WPS433

        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, (np.floating, np.integer)):
            return obj.item()
    except (ImportError, AttributeError, TypeError):
        _log.debug("gguf_overlay.py:45 numpy-aware JSON coercion unavailable, falling back to str(obj)", exc_info=True)
    return str(obj)


def _is_stub_backend(backend: Any | None) -> bool:
    if backend is None:
        return False
    return backend.__class__.__name__.startswith("Stub")


def _backend_name(backend: Any | None, fallback: str) -> str:
    if backend is None:
        return fallback
    name = getattr(backend, "name", None)
    if isinstance(name, str) and name.strip():
        return name.strip()
    return fallback


def _aux_report(
    backend: AuxiliaryBackend | None,
    ciel_state: Dict[str, Any],
    candidate_reply: str,
    *,
    label: str,
) -> Dict[str, Any]:
    if backend is None:
        return {
            "backend": label,
            "available": False,
            "status": "skipped",
            "reason": "missing_backend",
        }

    out = backend.analyse_state(ciel_state, candidate_reply)
    if isinstance(out, dict):
        report = dict(out)
    else:
        report = {"raw": str(out)}
    report.setdefault("backend", _backend_name(backend, label))
    report.setdefault("available", True)
    report.setdefault("status", "ok")
    return report


def _state_digest(ciel_state: Dict[str, Any], *, max_items_per_channel: int) -> Dict[str, Any]:
    digest = {
        "intention_vector": ciel_state.get("intention_vector"),
        "simulation": ciel_state.get("simulation"),
        "cognition": ciel_state.get("cognition"),
        "affect": ciel_state.get("affect"),
        "semantic_labels": ciel_state.get("semantic_labels"),
        "memory_score": ciel_state.get("memory_score"),
        "immune_surface": _immune_surface_brief(ciel_state),
        "phasenav": _phasenav_brief(ciel_state),
        "nonlocal_runtime": ciel_state.get("nonlocal_runtime") if isinstance(ciel_state.get("nonlocal_runtime"), dict) else {},
        "euler_bridge": ciel_state.get("euler_bridge") if isinstance(ciel_state.get("euler_bridge"), dict) else {},
        "runtime_policy": ciel_state.get("runtime_policy") if isinstance(ciel_state.get("runtime_policy"), dict) else {},
        "lingo_frame": ciel_state.get("lingo_frame") if isinstance(ciel_state.get("lingo_frame"), dict) else {},
        "semantic_speech": build_semantic_speech_context(
            ciel_state,
            max_items_per_channel=max_items_per_channel,
        ),
    }
    return digest


def _render_overlay_prompt(
    *,
    profile: str,
    system_prompt: str,
    state_digest: Dict[str, Any],
) -> str:
    semantic_speech = state_digest.get("semantic_speech", {})
    semantic_text = ""
    if isinstance(semantic_speech, dict):
        semantic_text = str(semantic_speech.get("text", "") or "").strip()
    immune_surface = state_digest.get("immune_surface", {})
    phasenav = state_digest.get("phasenav", {})

    prompt_lines = [
        system_prompt.strip(),
        f"GGUF overlay profile: {profile}",
        "Ground every answer in the supplied CIEL state.",
        "Do not invent memory, labels, or phase data that are not present.",
        "Use the semantic speech brief as the primary grounding channel.",
        "PhaseNav immune gate: treat immune_surface and phasenav as binding context.",
    ]
    if isinstance(immune_surface, dict) and immune_surface:
        prompt_lines.extend(["Immune surface:", json.dumps(immune_surface, ensure_ascii=False, default=_json_default)])
    if isinstance(phasenav, dict) and phasenav:
        prompt_lines.extend(["PhaseNav brief:", json.dumps(phasenav, ensure_ascii=False, default=_json_default)])
    if semantic_text:
        prompt_lines.extend(["Semantic speech brief:", semantic_text])

    prompt_lines.extend(
        [
            "State digest:",
            json.dumps(
                {k: v for k, v in state_digest.items() if k != "semantic_speech"},
                ensure_ascii=False,
                default=_json_default,
            ),
        ]
    )
    return "\n".join(line for line in prompt_lines if line)


@dataclass(slots=True)
class GGUFOverlayReport:
    profile: str
    primary_backend: str
    dialogue: List[Dict[str, str]]
    state_digest: Dict[str, Any]
    semantic_speech: Dict[str, Any]
    overlay_prompt: str
    reply: str
    analysis: Dict[str, Any]
    validator: Dict[str, Any]
    generated_at: str
    backend_status: Dict[str, Any] = field(default_factory=dict)
    prompt_messages: List[Dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "profile": self.profile,
            "primary_backend": self.primary_backend,
            "dialogue": self.dialogue,
            "state_digest": self.state_digest,
            "semantic_speech": self.semantic_speech,
            "overlay_prompt": self.overlay_prompt,
            "reply": self.reply,
            "analysis": self.analysis,
            "validator": self.validator,
            "generated_at": self.generated_at,
            "backend_status": self.backend_status,
            "prompt_messages": self.prompt_messages,
        }


@dataclass(slots=True)
class GGUFOverlay:
    primary_backend: LanguageBackend
    analysis_backend: AuxiliaryBackend | None = None
    validator_backend: AuxiliaryBackend | None = None
    profile: str = "standard"
    system_prompt: str = ""
    max_items_per_channel: int = 2
    allow_missing_aux: bool = True
    name: str = field(init=False)
    last_report: GGUFOverlayReport | None = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        if _is_stub_backend(self.primary_backend):
            raise RuntimeError("GGUFOverlay requires a real primary backend, not a stub")
        self.profile = (self.profile or "standard").strip().lower() or "standard"
        self.system_prompt = self.system_prompt.strip()
        if _is_stub_backend(self.analysis_backend):
            self.analysis_backend = None
        if _is_stub_backend(self.validator_backend):
            self.validator_backend = None
        self.name = f"gguf-overlay:{_backend_name(self.primary_backend, 'gguf')}"

    @classmethod
    def from_bundle(
        cls,
        bundle: "LLMBackendBundle",
        *,
        profile: str = "standard",
        system_prompt: str = "",
        max_items_per_channel: int = 2,
    ) -> "GGUFOverlay":
        return cls(
            primary_backend=bundle.primary_for(profile),
            analysis_backend=bundle.analysis,
            validator_backend=bundle.validator,
            profile=profile,
            system_prompt=system_prompt,
            max_items_per_channel=max_items_per_channel,
        )

    @property
    def primary_name(self) -> str:
        return _backend_name(self.primary_backend, "gguf")

    @property
    def model_path(self) -> str | None:
        return getattr(self.primary_backend, "model_path", None)

    def build_report(
        self,
        dialogue: List[Dict[str, Any]],
        ciel_state: Dict[str, Any],
        *,
        candidate_reply: str | None = None,
    ) -> GGUFOverlayReport:
        normalized_dialogue = _normalize_dialogue(dialogue)
        state_digest = _state_digest(ciel_state, max_items_per_channel=self.max_items_per_channel)
        overlay_prompt = _render_overlay_prompt(
            profile=self.profile,
            system_prompt=self.system_prompt,
            state_digest=state_digest,
        )
        prompt_messages = [{"role": "system", "content": overlay_prompt}, *normalized_dialogue]
        if candidate_reply is None:
            # The backend already injects its own system prompt from initialization.
            # Keep the overlay envelope for provenance, but do not double-inject it.
            reply = self.primary_backend.generate_reply(normalized_dialogue, ciel_state)
        else:
            reply = str(candidate_reply)
        analysis = _aux_report(self.analysis_backend, ciel_state, reply, label="analysis")
        validator = _aux_report(self.validator_backend, ciel_state, reply, label="validator")
        backend_status = {
            "primary": {"backend": self.primary_name, "available": True},
            "analysis": {"backend": analysis.get("backend"), "available": bool(analysis.get("available"))},
            "validator": {"backend": validator.get("backend"), "available": bool(validator.get("available"))},
        }
        report = GGUFOverlayReport(
            profile=self.profile,
            primary_backend=self.primary_name,
            dialogue=normalized_dialogue,
            state_digest=state_digest,
            semantic_speech=state_digest.get("semantic_speech", {}),
            overlay_prompt=overlay_prompt,
            reply=reply,
            analysis=analysis,
            validator=validator,
            generated_at=datetime.now(timezone.utc).isoformat(),
            backend_status=backend_status,
            prompt_messages=prompt_messages,
        )
        self.last_report = report
        return report

    def generate_report(
        self,
        dialogue: List[Dict[str, Any]],
        ciel_state: Dict[str, Any],
        *,
        candidate_reply: str | None = None,
    ) -> GGUFOverlayReport:
        return self.build_report(dialogue, ciel_state, candidate_reply=candidate_reply)

    def generate_reply(self, dialogue: List[Dict[str, Any]], ciel_state: Dict[str, Any]) -> str:
        return self.build_report(dialogue, ciel_state).reply

    def analyse_state(self, ciel_state: Dict[str, Any], candidate_reply: str) -> Dict[str, Any]:
        analysis = _aux_report(self.analysis_backend, ciel_state, candidate_reply, label="analysis")
        validator = _aux_report(self.validator_backend, ciel_state, candidate_reply, label="validator")
        return {
            "backend": self.name,
            "available": True,
            "status": "ok",
            "analysis": analysis,
            "validator": validator,
        }


__all__ = ["GGUFOverlay", "GGUFOverlayReport"]
