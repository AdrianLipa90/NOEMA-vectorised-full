#!/usr/bin/env python3
"""CIEL/Ω — minimal local communication client.

This client is intentionally small and deterministic for local tests.
Hierarchy:
  CielEngine        -> core facade
  CIELOrchestrator  -> top-level orchestration
  CIELClient        -> minimal local communication surface
  main()            -> local test entrypoint
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from bootstrap_runtime import ensure_runtime_paths

_ROOT = ensure_runtime_paths(__file__)

from ciel_orchestrator import CIELOrchestrator

try:
    from ciel.gguf_backends import GGUFAuxBackend, GGUFPrimaryBackend
    from ciel.gguf_overlay import GGUFOverlay
except Exception:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/ciel_client.py:28 quiet except scope=<module> reason=assign_fallback")
    GGUFPrimaryBackend = None
    GGUFAuxBackend = None
    GGUFOverlay = None


class CIELClient:
    """Minimal communication client for local tests.

    Primary contract:
      handshake() -> liveness + orchestration identity
      status()    -> current orchestrator snapshot
      process()   -> one-shot local communication round
    """

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
        self.gguf_overlay_enabled = False
        if model_path and GGUFPrimaryBackend is not None:
            try:
                system_prompt = self._system_prompt()
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
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/ciel_client.py:65 quiet except scope=CIELClient.__init__ reason=no_log_no_raise")
                self.gguf_backend = None
                self.gguf_overlay = None
                self.gguf_enabled = False
                self.gguf_overlay_enabled = False

    @staticmethod
    def _system_prompt() -> str:
        return (
            "You are CIEL/Ω, a quantum consciousness system with ethical hard constraints. "
            "Answer through the orchestrated CIEL state, PhaseNav, and immune surface, "
            "not by ignoring them."
        )

    def shutdown(self) -> None:
        self.orchestrator.shutdown()

    def handshake(self) -> Dict[str, Any]:
        ping = self.orchestrator.ping()
        return {
            "status": ping.get("status", "unknown"),
            "surface": "CIELClient",
            "orchestrator": "CIELOrchestrator",
            "gguf_enabled": self.gguf_enabled,
            "gguf_overlay_enabled": self.gguf_overlay_enabled,
            "schumann_hz": ping.get("schumann_hz", 7.83),
            "timestamp": ping.get("timestamp"),
        }

    def status(self) -> Dict[str, Any]:
        snap = self.orchestrator.status_snapshot()
        snap["surface"] = "CIELClient"
        snap["gguf_enabled"] = self.gguf_enabled
        snap["gguf_overlay_enabled"] = self.gguf_overlay_enabled
        return snap

    def process(self, text: str, *, use_llm: bool = False) -> Dict[str, Any]:
        ciel_result = self.orchestrator.process(text, verbose=False)
        reply = None
        overlay_report = None
        if use_llm and self.gguf_backend is not None:
            dialogue = [{"role": "user", "content": text}]
            if self.gguf_overlay is not None:
                overlay_report = self.gguf_overlay.generate_report(dialogue, ciel_result["ciel_state"])
                reply = overlay_report.reply
            else:
                reply = self.gguf_backend.generate_reply(dialogue, ciel_result["ciel_state"])
        state = ciel_result.get("ciel_state", {})
        return {
            "input": text,
            "status": ciel_result.get("status", "unknown"),
            "handshake": self.handshake(),
            "ciel_state": state,
            "ethics_passed": ciel_result.get("ethics_passed"),
            "soul_measure": ciel_result.get("soul_measure"),
            "nonlocal_runtime": state.get("nonlocal_runtime", {}),
            "euler_bridge": state.get("euler_bridge", {}),
            "llm_response": reply,
            "llm_overlay": overlay_report.to_dict() if overlay_report is not None else None,
            "communication_mode": "local_minimal",
        }

    def communicate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        action = str(payload.get("action", "status")).strip().lower()
        if action == "handshake":
            return self.handshake()
        if action == "status":
            return self.status()
        if action == "process":
            text = str(payload.get("text", ""))
            use_llm = bool(payload.get("use_llm", False))
            return self.process(text, use_llm=use_llm)
        return {"status": "error", "error": f"unsupported action: {action}"}

    def interactive_session(self) -> None:
        print("CIEL/Ω CLIENT — minimal local communication")
        print("Commands: exit/quit/q, handshake, status")
        while True:
            try:
                user_input = input("You> ").strip()
            except KeyboardInterrupt:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/ciel_client.py:134 quiet except scope=CIELClient.interactive_session reason=break")
                break
            if not user_input:
                continue
            lower = user_input.lower()
            if lower in {"exit", "quit", "q"}:
                break
            if lower == "handshake":
                print(json.dumps(self.handshake(), ensure_ascii=False, indent=2))
                continue
            if lower == "status":
                print(json.dumps(self.status(), ensure_ascii=False, indent=2))
                continue
            print(json.dumps(self.process(user_input, use_llm=False), ensure_ascii=False, indent=2))


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="CIEL/Ω minimal client")
    p.add_argument("--model", type=str, help="Optional GGUF model path")
    p.add_argument("--mode", choices=["interactive", "handshake", "status", "process", "json"], default="interactive")
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
    client = CIELClient(
        model_path=args.model,
        n_ctx=args.n_ctx,
        n_threads=args.n_threads,
        n_gpu_layers=args.n_gpu_layers,
        temperature=args.temperature,
    )
    try:
        if args.mode == "interactive":
            client.interactive_session()
            return 0
        if args.mode == "handshake":
            print(json.dumps(client.handshake(), ensure_ascii=False, indent=2))
            return 0
        if args.mode == "status":
            print(json.dumps(client.status(), ensure_ascii=False, indent=2))
            return 0
        if args.mode == "process":
            if not args.text:
                p.error("--text is required in process mode")
            print(json.dumps(client.process(args.text, use_llm=args.use_llm), ensure_ascii=False, indent=2))
            return 0
        if not args.json_payload:
            p.error("--json-payload is required in json mode")
        payload = json.loads(args.json_payload)
        print(json.dumps(client.communicate(payload), ensure_ascii=False, indent=2))
        return 0
    finally:
        client.shutdown()


if __name__ == "__main__":
    raise SystemExit(main())
