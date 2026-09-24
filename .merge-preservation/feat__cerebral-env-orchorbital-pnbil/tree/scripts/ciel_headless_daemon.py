#!/usr/bin/env python3
"""Strict headless CIEL service bound to the verified NOEMA topology state.

The daemon has one production pipeline mode:
``ciel_canonical_topology_only``.  It verifies the content-addressed orbital
state receipt before startup and before every request.  A verified topology is
usable even when the source map does not provide a scientific orbital model;
in that case orbital values remain ``None`` and the response says why.

The service does not persist prompts, dialogue, semantic state, or learning
events.  It keeps only bounded, volatile session metadata (topic, focus and
claim identifiers) so follow-up turns have continuity without retaining raw
dialogue.  A separate explicit consent contract is required before durable
conversation writeback may be introduced.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import logging
import os
from pathlib import Path
import signal
import socket
import sys
import threading
import time
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
RUNTIME_CONTRACT_PATH = ROOT / "config" / "ciel_headless_runtime.json"


def _load_runtime_contract() -> dict[str, Any]:
    payload = json.loads(RUNTIME_CONTRACT_PATH.read_text(encoding="utf-8"))
    if payload.get("schema") != "ciel.headless-runtime/v1":
        raise RuntimeError("unsupported CIEL headless runtime contract")
    engine_timeout = int(payload["timeouts"]["engine_step_seconds"])
    socket_timeout = int(payload["timeouts"]["socket_read_seconds"])
    if not 60 <= engine_timeout <= 120 or not 60 <= socket_timeout <= 120:
        raise RuntimeError("CIEL timeout contract requires every timeout in [60, 120] seconds")
    if int(payload["concurrency"]["engine_workers"]) != 1:
        raise RuntimeError("stateful CielEngine requires exactly one serialized worker")
    return payload


RUNTIME_CONTRACT = _load_runtime_contract()
ENGINE_STEP_TIMEOUT = int(RUNTIME_CONTRACT["timeouts"]["engine_step_seconds"])
SOCKET_READ_TIMEOUT = int(RUNTIME_CONTRACT["timeouts"]["socket_read_seconds"])
MAX_REQUEST_BYTES = int(RUNTIME_CONTRACT["request"]["max_bytes"])
SOURCE_ROOT = str(ROOT / "src")
if SOURCE_ROOT not in sys.path:
    sys.path.insert(0, SOURCE_ROOT)

from ciel_geometry.orbital_state_contract import load_verified_orbital_state
from ciel_geometry.paths import P as _P


PIPELINE_MODE = "ciel_canonical_topology_only"
ORBITAL_STATE_PATH = Path(_P.STATE.ORCH_PKL).parent / "noema_orbital_state.json"
SOCKET_PATH = Path(_P.RUN.HEADLESS_SOCK)
PID_PATH = Path(_P.RUN.HEADLESS_PID)
LOG_PATH = Path(_P.LOGS.HEADLESS_LOG)

# Singleton CielEngine — created once, reused across all requests
_engine_instance = None
_engine_lock = threading.Lock()
_engine_step_lock = threading.Lock()
_engine_executor = concurrent.futures.ThreadPoolExecutor(
    max_workers=int(RUNTIME_CONTRACT["concurrency"]["engine_workers"]),
    thread_name_prefix="ciel-engine-serialized",
)
_engine_unhealthy_reason: str | None = None

def _get_engine():
    """Return the singleton CielEngine, creating it only once."""
    global _engine_instance
    if _engine_instance is not None:
        return _engine_instance
    with _engine_lock:
        if _engine_instance is not None:
            return _engine_instance
        _omega_root = ROOT / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM"
        _engine_path = _omega_root / "ciel_omega" / "ciel"
        for _p in [_omega_root, _engine_path]:
            if str(_p) not in sys.path:
                sys.path.insert(0, str(_p))
        from engine import CielEngine as _CE
        eng = _CE()
        eng.boot()
        _engine_instance = eng
        log.info("CielEngine singleton created and booted")
        return _engine_instance

SOCKET_PATH.parent.mkdir(parents=True, exist_ok=True)
SOCKET_PATH.parent.chmod(0o700)
PID_PATH.parent.mkdir(parents=True, exist_ok=True)
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="[ciel-headless] %(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger(__name__)
_log_handler = logging.FileHandler(LOG_PATH)
_log_handler.setFormatter(
    logging.Formatter("[ciel-headless] %(asctime)s %(levelname)s %(message)s")
)
logging.getLogger().addHandler(_log_handler)
del _log_handler


class HeadlessContractError(RuntimeError):
    """The requested operation cannot satisfy the strict headless contract."""


class HeadlessEngineUnavailable(RuntimeError):
    """The serialized engine worker cannot safely accept another request."""


def _require_pipeline_mode() -> str:
    """Require the unit-provided mode; there is no implicit default mode."""
    try:
        mode = os.environ["CIEL_HEADLESS_PIPELINE_MODE"]
    except KeyError as exc:
        raise HeadlessContractError(
            "CIEL_HEADLESS_PIPELINE_MODE is required"
        ) from exc
    if mode != PIPELINE_MODE:
        raise HeadlessContractError(
            f"unsupported CIEL_HEADLESS_PIPELINE_MODE: {mode!r}"
        )
    return mode


def _verified_orbital_binding() -> tuple[dict[str, Any], dict[str, Any]]:
    """Load and validate the strict topology publication used by this request."""
    state, publication = load_verified_orbital_state(ORBITAL_STATE_PATH)

    required_statuses = {
        "structural_status": "ok",
        "topology_status": "ok",
    }
    for field, expected in required_statuses.items():
        actual = state.get(field)
        if actual != expected:
            raise HeadlessContractError(
                f"orbital topology contract rejected {field}={actual!r}"
            )

    endpoint_resolution = state.get("endpoint_resolution")
    if not isinstance(endpoint_resolution, dict):
        raise HeadlessContractError("orbital topology has no endpoint-resolution contract")
    if endpoint_resolution.get("status") != "ok":
        raise HeadlessContractError(
            "orbital topology contains unresolved active endpoints"
        )

    validation_errors = state.get("validation_errors")
    if not isinstance(validation_errors, list) or validation_errors:
        raise HeadlessContractError(
            "orbital topology contains validation errors"
        )

    orbital_status = state.get("orbital_status")
    if orbital_status not in {"explicit", "partial", "unavailable"}:
        raise HeadlessContractError(
            f"unknown orbital_status: {orbital_status!r}"
        )

    scientific_unavailable = state.get("scientific_unavailable")
    if not isinstance(scientific_unavailable, dict):
        scientific_unavailable = {}

    if orbital_status == "explicit":
        orbits = state.get("orbits")
        coherence = state.get("coherence")
        if orbits is None or coherence is None:
            raise HeadlessContractError(
                "explicit orbital publication is missing scientific values"
            )
    else:
        # Partial or unavailable orbital evidence may not be promoted by this
        # topology-only consumer.  Absence stays absence, never numeric zero.
        orbits = None
        coherence = None
        if not scientific_unavailable:
            raise HeadlessContractError(
                "non-explicit orbital publication lacks unavailability provenance"
            )

    binding_status = (
        "topology_verified_orbital_explicit"
        if orbital_status == "explicit"
        else f"topology_verified_orbital_{orbital_status}"
    )
    binding = {
        "status": binding_status,
        "pipeline_mode": PIPELINE_MODE,
        "state_status": state.get("status"),
        "structural_status": state.get("structural_status"),
        "topology_status": state.get("topology_status"),
        "orbital_status": orbital_status,
        "inference_used": state.get("inference_used"),
        "fallback_used": state.get("fallback_used"),
        "systems": state.get("systems"),
        "nodes": state.get("nodes"),
        "edges": state.get("edges"),
        "endpoint_resolution": endpoint_resolution,
        "weight_contract": state.get("weight_contract"),
        "source": state.get("source"),
        "producer": state.get("producer"),
        "publication": publication,
        "orbital_science": {
            "status": orbital_status,
            "orbits": orbits,
            "coherence": coherence,
            "unavailable": scientific_unavailable,
        },
    }
    return state, binding


def _unavailable_semantic_result(
    binding: dict[str, Any],
    started_at: float,
    *,
    reason: str = "no_verified_no_fallback_ciel_pipeline",
    response: str | None = None,
    analysis_performed: bool = False,
) -> dict[str, Any]:
    """Return a factual fail-closed result without analysing the prompt."""
    return {
        "status": "degraded",
        "response": response or (
            "CIEL semantic pipeline is unavailable: no verified no-fallback "
            "CIEL pipeline is currently published."
        ),
        "frame": {
            "semantic_status": "unavailable",
            "reason": reason,
            "analysis_performed": analysis_performed,
        },
        "binding": binding,
        "semantic_status": "unavailable",
        "semantic_reason": reason,
        "privacy": {
            "prompt_persisted": False,
            "dialogue_persisted": False,
            "semantic_state_persisted": False,
            "learning_triggered": False,
        },
        "elapsed_s": time.monotonic() - started_at,
    }


def _run_engine_step(text: str) -> dict[str, Any]:
    """Run the stateful engine in one serialized worker, failing closed on timeout."""
    global _engine_unhealthy_reason
    acquired = _engine_step_lock.acquire(timeout=ENGINE_STEP_TIMEOUT)
    if not acquired:
        raise HeadlessEngineUnavailable("engine_serialization_timeout")
    try:
        if _engine_unhealthy_reason is not None:
            raise HeadlessEngineUnavailable(_engine_unhealthy_reason)
        future = _engine_executor.submit(_get_engine().step, text, context="headless")
        try:
            result = future.result(timeout=ENGINE_STEP_TIMEOUT)
        except concurrent.futures.TimeoutError as exc:
            future.cancel()
            _engine_unhealthy_reason = "engine_step_timeout_fail_closed_until_restart"
            raise HeadlessEngineUnavailable(_engine_unhealthy_reason) from exc
        if not isinstance(result, dict):
            raise HeadlessEngineUnavailable("engine_returned_non_object_state")
        return result
    finally:
        _engine_step_lock.release()


def process_text(text: str, *, session_id: str) -> dict[str, Any]:
    """Process one turn after re-verifying mode, state, and receipt."""
    started_at = time.monotonic()
    _require_pipeline_mode()
    if not isinstance(text, str) or not text.strip():
        raise HeadlessContractError("text must be a non-empty string")
    if not isinstance(session_id, str) or not session_id.strip():
        raise HeadlessContractError("session_id must be a non-empty string")
    _state, binding = _verified_orbital_binding()

    # Per-step wall-clock timing (real seconds — never dressed up as a phase
    # or holonomy value, which measure geometric phase over operator
    # sequences, not duration). Logged so a future client-side timeout/
    # BrokenPipeError shows exactly which step was slow instead of requiring
    # another one-off diagnostic script.
    _step_timings: dict[str, float] = {}

    # Native PhaseNav classification of the incoming prompt — phase_nav_lang
    # ("the only NOEMA coding language") was not previously wired into this
    # request path at all. This is a real application of it (operator
    # classification + genuine holonomy of the prompt's semantic loop), not
    # a repurposing of holonomy to fake a timing measurement.
    _phasenav_analysis: dict[str, Any] | None = None
    _t_phasenav = time.monotonic()
    try:
        from ciel_geometry.phase_nav_lang import analyze_prompt as _analyze_prompt
        _phasenav_analysis = _analyze_prompt(text)
    except Exception as exc:
        log.debug("phase_nav_lang.analyze_prompt failed: %s: %s", type(exc).__name__, exc)
    _step_timings["phasenav_analyze_prompt"] = round(time.monotonic() - _t_phasenav, 6)

    # The engine validates and advances its own canonical surface.  The speech
    # planner is a separate source-grounded layer: unreviewed engine heuristics
    # are deliberately not used as evidence for scientific claims.
    try:
        _t0 = time.monotonic()
        _step_result = _run_engine_step(text)
        _step_timings["run_engine_step"] = round(time.monotonic() - _t0, 6)
        if (
            _step_result.get("status") != "ok"
            or _step_result.get("headless_formal_state") is not True
            or _step_result.get("heuristic_metrics_computed") is not False
            or _step_result.get("memory_write_performed") is not False
        ):
            raise HeadlessEngineUnavailable("headless_engine_formal_contract_rejected")

        # Primary: CIELingoInference — native PhaseNav-powered response
        # CIELingoInference ma priorytet nad autonomous_responder.
        # Uruchamiamy niezależnie od confidence (conf=none dopuszczalne gdy są źródła).
        _cielingo_resp: str | None = None
        _t0 = time.monotonic()

        # Intencja statusu systemu: generuj odpowiedź z rzeczywistych danych
        # zamiast pozwalać CIELingoInference zwrócić chunki autoprezentacji.
        _STATUS_KEYWORDS = {
            "sprawdź stan", "sprawdz stan", "status", "health", "kondycja",
            "stan systemu", "stan demonów", "stan daemonów", "stan daemony",
            "działają", "działaja", "działają demony", "czy działa",
            "co działa", "co jest aktywne", "aktywne demony",
        }
        _text_lower = text.lower().strip()
        _is_status_intent = any(kw in _text_lower for kw in _STATUS_KEYWORDS)

        if _is_status_intent:
            try:
                import subprocess as _sp
                _svc_list = [
                    "noema-surface-init", "noema-kuramoto", "noema-nonlocal-proxy",
                    "noema-resonance", "noema-analog-blend", "noema-neutrino",
                    "noema-subconscious", "noema-consolidator", "noema-archiver",
                    "noema-linux-sensor", "noema-phasenav-hot", "noema-cielingo-sync",
                    "noema-codex-fifo-bridge", "noema-agent-backend", "noema-web-research",
                    "noema-headless", "noema-portal", "noema-doctor", "noema-watchdog",
                ]
                _statuses = []
                for _svc in _svc_list:
                    _r = _sp.run(["systemctl", "--user", "is-active", _svc],
                                 capture_output=True, text=True, timeout=2)
                    _statuses.append((_svc.replace("noema-", ""), _r.stdout.strip()))
                _active = [s for s, st in _statuses if st == "active"]
                _failed = [s for s, st in _statuses if st not in ("active", "activating")]
                _lines = [f"Stan systemu NOEMA ({len(_active)}/{len(_statuses)} aktywnych):"]
                for _svc, _st in _statuses:
                    _mark = "✓" if _st == "active" else "✗"
                    _lines.append(f"  {_mark} {_svc}: {_st}")
                if _failed:
                    _lines.append(f"\nNieaktywne: {', '.join(_failed)}")
                else:
                    _lines.append("\nWszystkie demony aktywne.")
                _cielingo_resp = "\n".join(_lines)
                log.debug("status_intent: generated system health response")
            except Exception as exc:
                log.debug("status_intent generation failed: %s", exc)
        else:
            try:
                from ciel_geometry.cielingo_inference import CIELingoInference as _CI
                _ci = _CI()
                _ci_result = _ci.answer(text, k=5)
                if _ci_result.get("n_sources", 0) > 0:
                    _cielingo_resp = _ci_result["answer"]
            except Exception as exc:
                log.debug("CIELingoInference skipped: %s", exc)
        _step_timings["cielingo_inference"] = round(time.monotonic() - _t0, 6)

        from cielingo_core.autonomous_response import get_autonomous_responder

        _t0 = time.monotonic()
        speech = get_autonomous_responder().respond(
            text,
            session_id=session_id,
        )
        _step_timings["autonomous_responder"] = round(time.monotonic() - _t0, 6)
        # CIELingoInference jest modelem natywnym CIEL — zawsze preferowane.
        # autonomous_responder służy jako fallback gdy CIELingo nie ma źródeł.
        if _cielingo_resp:
            lang_resp = _cielingo_resp
            response_ok = True
        elif speech.status == "ok":
            lang_resp = speech.text
            response_ok = True
        else:
            lang_resp = speech.text
            response_ok = speech.status in ("ok", "web_resolved")

        # Gdy autonomous_response nie ma zweryfikowanych twierdzeń → użyj ciel_speaker
        _ethics_score: float | None = None
        _ethics_components: dict = {}
        _ethics_blocked: bool = False
        if not response_ok:
            _t0 = time.monotonic()
            try:
                import sys as _sys
                _scripts_dir = str(Path(__file__).resolve().parent)
                if _scripts_dir not in _sys.path:
                    _sys.path.insert(0, _scripts_dir)
                from ciel_speaker import speak as _ciel_speak, compute_ethics as _ce, ETHICS_THRESHOLD as _ET
                _lingo: dict = {}
                _state: dict = {}
                _t_sub = time.monotonic()
                try:
                    from ciel_sot_agent.cielingo_bridge import build_lingo_frame as _blf
                    _lingo = _blf(text)
                except Exception as exc:
                    log.debug("fallback build_lingo_frame skipped: %s", exc)
                _step_timings["fallback_build_lingo_frame"] = round(time.monotonic() - _t_sub, 6)
                _t_sub = time.monotonic()
                try:
                    from ciel_coupling import process_user_input as _pui
                    _state = _pui(text, fast=True)
                except Exception as exc:
                    log.debug("fallback process_user_input skipped: %s", exc)
                _step_timings["fallback_process_user_input"] = round(time.monotonic() - _t_sub, 6)
                # Oblicz ethical_score przed speak() — niezależnie od ścieżki
                _t_sub = time.monotonic()
                _ethics_score, _ethics_components = _ce(text, _state)
                _ethics_blocked = _ethics_score < _ET
                _step_timings["fallback_compute_ethics"] = round(time.monotonic() - _t_sub, 6)
                _t_sub = time.monotonic()
                _speaker_resp = _ciel_speak(_state, _lingo, text)
                _step_timings["fallback_ciel_speak"] = round(time.monotonic() - _t_sub, 6)
                if _speaker_resp and _speaker_resp.strip():
                    lang_resp = _speaker_resp
                    response_ok = True
            except Exception as exc:
                log.debug("fallback pipeline skipped: %s", exc)
            _step_timings["fallback_total"] = round(time.monotonic() - _t0, 6)

        _step_timings["total"] = round(time.monotonic() - started_at, 6)
        if _step_timings["total"] > 5.0:
            log.warning("process_text slow (%.3fs total): %s", _step_timings["total"], _step_timings)
        else:
            log.info("process_text timings: %s", _step_timings)
        suppressed_metric_names = (
            "dominant_emotion",
            "mood_scalar",
            "collatz_seed",
            "orbit_length",
            "attractor_score",
        )
        return {
            "status": "ok" if response_ok else "degraded",
            "response": lang_resp,
            "frame": {
                "semantic_status": "ok" if response_ok else "unavailable",
                "analysis_performed": True,
                "dominant_emotion": None,
                "mood_scalar": None,
                "ethical_score": _ethics_score,
                "ethical_threshold": 0.75,
                "ethical_blocked": _ethics_blocked,
                "ethical_components": _ethics_components if _ethics_components else None,
                "cqcl_program": None,
                "collatz_seed": None,
                "orbit_length": None,
                "attractor_score": None,
                "response_status": speech.status,
                "response_mode": speech.generation_mode,
                "response_event_id": speech.event_id,
                "response_fallback_used": speech.fallback_used,
                "raw_prompt_persisted": speech.raw_prompt_persisted,
                "response_operator": speech.operator,
                "response_domain": speech.domain,
                "response_focus": speech.focus,
                "response_claim_ids": list(speech.claim_ids),
                "response_sources": list(speech.sources),
                "response_uncertainty": list(speech.uncertainty),
                "confidence_sieve": speech.confidence_sieve,
                "continuity": speech.continuity,
                "phase_vector": {
                    "dimension": len(speech.phase_vector),
                    "values": list(speech.phase_vector),
                    "basis": list(speech.phase_basis),
                    "encoding": speech.phase_encoding,
                    "source": "verified_knowledge.focus_operators",
                    "measurement_status": "formal_coordinate_not_sensor_metric",
                    "fallback_used": False,
                },
                "metric_provenance": {
                    key: {
                        "status": "unavailable",
                        "reason": "not_certified_for_scientific_or_semantic_response",
                        "value": None,
                    }
                    for key in suppressed_metric_names
                },
                "engine_execution": {
                    "status": "completed",
                    "used_for_claim_selection": False,
                    "reason": "engine heuristics are not reviewed scientific evidence",
                    "heuristic_metrics_computed": False,
                    "memory_write_performed": False,
                },
                "phasenav_native": _phasenav_analysis,
            },
            "step_timings_seconds": _step_timings,
            "binding": binding,
            "semantic_status": "ok" if response_ok else "unavailable",
            "privacy": {
                "prompt_persisted": False,
                "dialogue_persisted": False,
                "session_memory": RUNTIME_CONTRACT["session"]["storage"],
                "learning_triggered": False,
            },
            "elapsed_s": time.monotonic() - started_at,
        }
    except HeadlessEngineUnavailable as exc:
        reason = str(exc)
        log.warning("CielEngine unavailable: %s", reason)
        return _unavailable_semantic_result(binding, started_at, reason=reason)
    except Exception as exc:
        log.debug("CielEngine pipeline failed: %s", type(exc).__name__)
        return _unavailable_semantic_result(
            binding,
            started_at,
            reason=f"pipeline_exception:{type(exc).__name__}",
        )


def _decode_request(payload: bytes) -> tuple[str, str]:
    """Decode the documented JSON or plain-text local socket request."""
    if not payload:
        raise HeadlessContractError("empty request")
    if len(payload) > MAX_REQUEST_BYTES:
        raise HeadlessContractError("request exceeds runtime byte limit")
    try:
        decoded = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HeadlessContractError("request must be UTF-8") from exc
    decoded = decoded.strip()
    if not decoded:
        raise HeadlessContractError("empty request")

    if not decoded.startswith("{"):
        raise HeadlessContractError("JSON request object is required")
    try:
        request = json.loads(decoded)
    except json.JSONDecodeError as exc:
        raise HeadlessContractError("invalid JSON request") from exc
    if not isinstance(request, dict):
        raise HeadlessContractError("JSON request must be an object")
    text = request.get("text")
    session_id = request.get("session_id")
    if not isinstance(text, str) or not text.strip():
        raise HeadlessContractError("JSON request requires non-empty text")
    if not isinstance(session_id, str) or not session_id.strip():
        raise HeadlessContractError("JSON request requires non-empty session_id")
    return text, session_id


class HeadlessSocketServer:
    """Owner-only Unix socket for strict headless CIEL requests."""

    def __init__(self, socket_path: Path = SOCKET_PATH) -> None:
        self.socket_path = socket_path
        self._server: socket.socket | None = None
        self._running = False

    def start(self) -> None:
        if self.socket_path.exists():
            self.socket_path.unlink()
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(str(self.socket_path))
        server.listen()
        self.socket_path.chmod(0o600)
        self._server = server
        self._running = True
        log.info("Unix socket listening: %s", self.socket_path)

    def stop(self) -> None:
        self._running = False
        if self._server is not None:
            self._server.close()
            self._server = None
        if self.socket_path.exists():
            self.socket_path.unlink()

    def serve_forever(self) -> None:
        if self._server is None:
            raise HeadlessContractError("socket server has not been started")
        while self._running:
            try:
                connection, _address = self._server.accept()
            except OSError:
                if self._running:
                    raise
                break
            threading.Thread(
                target=self._handle,
                args=(connection,),
                daemon=True,
                name="ciel-headless-request",
            ).start()

    @staticmethod
    def _handle(connection: socket.socket) -> None:
        with connection:
            try:
                connection.settimeout(SOCKET_READ_TIMEOUT)
                chunks: list[bytes] = []
                received = 0
                while received <= MAX_REQUEST_BYTES:
                    chunk = connection.recv(min(65536, MAX_REQUEST_BYTES + 1 - received))
                    if not chunk:
                        break
                    newline = chunk.find(b"\n")
                    if newline >= 0:
                        chunk = chunk[:newline]
                    chunks.append(chunk)
                    received += len(chunk)
                    if newline >= 0:
                        break
                if received > MAX_REQUEST_BYTES:
                    raise HeadlessContractError("request exceeds runtime byte limit")
                payload = b"".join(chunks)
                text, session_id = _decode_request(payload)
                result = process_text(text, session_id=session_id)
                connection.sendall(json.dumps(result, ensure_ascii=False).encode("utf-8"))
            except Exception as exc:
                error = {
                    "status": "error",
                    "error_type": type(exc).__name__,
                    "error": (
                        str(exc)
                        if isinstance(exc, (HeadlessContractError, socket.timeout))
                        else "internal headless error"
                    ),
                }
                connection.sendall(json.dumps(error, ensure_ascii=False).encode("utf-8"))


def _warmup() -> dict[str, Any]:
    """Synchronously prove the production dependencies before socket-ready."""
    mode = _require_pipeline_mode()
    _state, binding = _verified_orbital_binding()

    # Validate only the active formal headless path and the reviewed pack.
    try:
        eng = _get_engine()
        formal_state = eng.step("CIEL headless warmup", context="headless")
        if formal_state.get("headless_formal_state") is not True:
            raise HeadlessContractError("headless formal warmup rejected")
        from cielingo_core.autonomous_response import get_autonomous_responder
        get_autonomous_responder()
        log.info("warmup: formal engine gate and reviewed knowledge pack loaded")
    except Exception as exc:
        raise HeadlessContractError(
            f"headless warmup failed: {type(exc).__name__}"
        ) from exc

    log.info(
        "warmup verified mode=%s binding=%s receipt=%s semantic_status=ready",
        mode,
        binding["status"],
        binding["publication"]["state_sha256"],
    )
    return {
        "mode": mode,
        "binding": binding,
        "semantic_status": "ready",
        "semantic_reason": None,
    }


def interactive_loop() -> None:
    """Run the same strict pipeline without creating a socket."""
    while True:
        try:
            text = input(">>> ")
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if text.strip().casefold() in {"exit", "exit()", "quit", ":q"}:
            return
        result = process_text(text, session_id="interactive-local")
        print(result["response"])


def main() -> int:
    parser = argparse.ArgumentParser(
        description="CIEL headless canonical topology-only daemon"
    )
    parser.add_argument("--oneshot", type=str)
    parser.add_argument("--session-id", type=str)
    parser.add_argument("--interactive", action="store_true")
    args = parser.parse_args()

    if args.oneshot is not None:
        if not args.session_id:
            raise HeadlessContractError("--oneshot requires --session-id")
        print(
            json.dumps(
                process_text(args.oneshot, session_id=args.session_id),
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    if args.interactive:
        _warmup()
        interactive_loop()
        return 0

    _warmup()
    PID_PATH.write_text(f"{os.getpid()}\n", encoding="ascii")
    PID_PATH.chmod(0o600)

    server = HeadlessSocketServer()

    def _stop(_signum: int, _frame: Any) -> None:
        server.stop()

    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)

    try:
        server.start()
        log.info("CIEL headless ready: pid=%s", os.getpid())
        server.serve_forever()
    finally:
        server.stop()
        if PID_PATH.exists():
            PID_PATH.unlink()
        log.info("CIEL headless stopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
