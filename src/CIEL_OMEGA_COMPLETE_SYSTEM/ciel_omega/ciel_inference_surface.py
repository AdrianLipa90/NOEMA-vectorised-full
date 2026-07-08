#!/usr/bin/env python3
"""CIEL/Ω — canonical orbital-ethical inference surface.

This surface keeps inference outside InformationFlow while still grounding it in
canonical Omega state:
    CIELOrchestrator -> prepared state -> orbital/ethical inference surface

It supports a dry-run mode by default and only attempts GGUF-wrapped inference
when an explicit backend is available.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import argparse
import json
from pathlib import Path
from typing import Any, Dict, Optional

from bootstrap_runtime import ensure_runtime_paths

_ROOT = ensure_runtime_paths(__file__)

from ciel_orchestrator import CIELOrchestrator
from inference.middleware import build_orbital_ethical_inference_surface

try:
    from ciel.gguf_backends import GGUFAuxBackend, GGUFPrimaryBackend
    from ciel.gguf_overlay import GGUFOverlay
except Exception:  # pragma: no cover - optional local backend
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/ciel_inference_surface.py:27 quiet except scope=<module> reason=assign_fallback")
    GGUFPrimaryBackend = None
    GGUFAuxBackend = None
    GGUFOverlay = None


class CIELInferenceSurface:
    """Canonical local surface for orbital-ethical inference."""

    def __init__(
        self,
        model_path: Optional[str] = None,
        *,
        n_ctx: int = 4096,
        n_threads: int = 8,
        n_gpu_layers: int = 0,
        temperature: float = 0.7,
        boot: bool = True,
    ) -> None:
        self.orchestrator = CIELOrchestrator(boot=boot)
        self.gguf_backend = None
        self.gguf_overlay = None
        self.gguf_enabled = False
        self.gguf_backend_status = "disabled"
        self.gguf_overlay_enabled = False
        if model_path and GGUFPrimaryBackend is not None:
            try:
                system_prompt = (
                    "You are CIEL/Ω inference surface. Stay aligned with the"
                    " orbital-ethical gate, PhaseNav, and immune surface; do not override system state."
                )
                self.gguf_backend = GGUFPrimaryBackend(
                    model_path=model_path,
                    n_ctx=n_ctx,
                    n_threads=n_threads,
                    n_gpu_layers=n_gpu_layers,
                    temperature=temperature,
                    system_prompt=system_prompt,
                )
                analysis_backend = None
                if GGUFAuxBackend is not None:
                    analysis_backend = GGUFAuxBackend(
                        model_path=model_path,
                        n_ctx=n_ctx,
                        n_threads=n_threads,
                        n_gpu_layers=n_gpu_layers,
                        temperature=min(0.3, temperature),
                        system_prompt=system_prompt,
                    )
                if GGUFOverlay is not None:
                    self.gguf_overlay = GGUFOverlay(
                        primary_backend=self.gguf_backend,
                        analysis_backend=analysis_backend,
                        validator_backend=analysis_backend,
                        profile="standard",
                        system_prompt=system_prompt,
                    )
                    self.gguf_overlay_enabled = True
                self.gguf_enabled = True
                self.gguf_backend_status = "enabled"
            except Exception as exc:  # pragma: no cover - optional backend path
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/ciel_inference_surface.py:63 quiet except scope=CIELInferenceSurface.__init__ reason=no_log_no_raise")
                self.gguf_backend = None
                self.gguf_overlay = None
                self.gguf_enabled = False
                self.gguf_backend_status = f"unavailable:{type(exc).__name__}"
                self.gguf_overlay_enabled = False

    def shutdown(self) -> None:
        self.orchestrator.shutdown()

    def handshake(self) -> Dict[str, Any]:
        ping = self.orchestrator.ping()
        return {
            "status": ping.get("status", "unknown"),
            "surface": "CIELInferenceSurface",
            "orchestrator": "CIELOrchestrator",
            "gguf_enabled": self.gguf_enabled,
            "gguf_overlay_enabled": self.gguf_overlay_enabled,
            "gguf_backend_status": self.gguf_backend_status,
            "timestamp": ping.get("timestamp"),
        }

    def status(self) -> Dict[str, Any]:
        snap = self.orchestrator.status_snapshot()
        snap.update(
            {
                "surface": "CIELInferenceSurface",
                "gguf_enabled": self.gguf_enabled,
                "gguf_overlay_enabled": self.gguf_overlay_enabled,
                "gguf_backend_status": self.gguf_backend_status,
            }
        )
        return snap

    def process(self, text: str, *, use_llm: bool = False) -> Dict[str, Any]:
        process_result = self.orchestrator.process(text, verbose=False)
        ciel_state = process_result.get("ciel_state", {}) or {}
        information_flow = ciel_state.get("information_flow", {}) or {}
        euler_bridge = ciel_state.get("euler_bridge", {}) or {}
        euler_metrics = euler_bridge.get("euler_metrics", {}) if isinstance(euler_bridge, dict) else {}
        target_phase = euler_metrics.get("target_phase", 0.0)
        ethical_score = float(ciel_state.get("ethical_score", 0.0) or 0.0)

        messages = None
        backend = None
        model = None
        overlay_report = None
        if use_llm and self.gguf_backend is not None:
            backend = self.gguf_backend
            model = getattr(self.gguf_backend, "model_path", None) or str(getattr(self.gguf_backend, "model_name", "gguf-local"))
            messages = [{"role": "user", "content": text}]
            if self.gguf_overlay is not None:
                overlay_report = self.gguf_overlay.generate_report(messages, ciel_state)

        inference_runtime = build_orbital_ethical_inference_surface(
            flow_entry=information_flow,
            target_phase=target_phase,
            ethical_score=ethical_score,
            backend=backend,
            model=model,
            messages=messages,
            temperature=0.0,
            max_tokens=128,
        )
        if use_llm and self.gguf_overlay is not None and inference_runtime.get("response_text"):
            overlay_report = self.gguf_overlay.generate_report(
                messages or [{"role": "user", "content": text}],
                ciel_state,
                candidate_reply=str(inference_runtime.get("response_text", "")),
            )

        return {
            "input": text,
            "status": process_result.get("status", "unknown"),
            "surface": "CIELInferenceSurface",
            "handshake": self.handshake(),
            "ethical_score": ethical_score,
            "orbital_context": {
                "target_phase": target_phase,
                "closure_score": euler_metrics.get("closure_score", 0.0),
            },
            "inference_runtime": inference_runtime,
            "gguf_enabled": self.gguf_enabled,
            "gguf_overlay_enabled": self.gguf_overlay_enabled,
            "llm_overlay": overlay_report.to_dict() if overlay_report is not None else None,
            "use_llm": bool(use_llm and self.gguf_enabled),
            "communication_mode": "orbital_ethical_inference_surface",
        }

    def communicate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        action = str(payload.get("action", "status")).strip().lower()
        if action == "handshake":
            return self.handshake()
        if action == "status":
            return self.status()
        if action == "process":
            return self.process(str(payload.get("text", "")), use_llm=bool(payload.get("use_llm", False)))
        return {"status": "error", "error": f"unsupported action: {action}", "surface": "CIELInferenceSurface"}


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="CIEL/Ω orbital-ethical inference surface")
    p.add_argument("--model", type=str, help="Optional GGUF model path")
    p.add_argument("--mode", choices=["handshake", "status", "process", "json"], default="handshake")
    p.add_argument("--text", type=str, help="Text for process mode")
    p.add_argument("--json-payload", type=str, help="JSON payload for json mode")
    p.add_argument("--n-ctx", type=int, default=4096)
    p.add_argument("--n-threads", type=int, default=8)
    p.add_argument("--n-gpu-layers", type=int, default=0)
    p.add_argument("--temperature", type=float, default=0.7)
    p.add_argument("--use-llm", action="store_true")
    return p


def main(argv: Optional[list[str]] = None) -> int:
    p = build_arg_parser()
    args = p.parse_args(argv)
    surface = CIELInferenceSurface(
        model_path=args.model,
        n_ctx=args.n_ctx,
        n_threads=args.n_threads,
        n_gpu_layers=args.n_gpu_layers,
        temperature=args.temperature,
    )
    try:
        if args.mode == "handshake":
            print(json.dumps(surface.handshake(), ensure_ascii=False, indent=2))
            return 0
        if args.mode == "status":
            print(json.dumps(surface.status(), ensure_ascii=False, indent=2))
            return 0
        if args.mode == "process":
            if not args.text:
                p.error("--text is required in process mode")
            print(json.dumps(surface.process(args.text, use_llm=args.use_llm), ensure_ascii=False, indent=2))
            return 0
        if not args.json_payload:
            p.error("--json-payload is required in json mode")
        payload = json.loads(args.json_payload)
        print(json.dumps(surface.communicate(payload), ensure_ascii=False, indent=2))
        return 0
    finally:
        surface.shutdown()


if __name__ == "__main__":
    raise SystemExit(main())
