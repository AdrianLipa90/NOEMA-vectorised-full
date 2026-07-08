#!/usr/bin/env python3

"""CIELingo Headless — cerebral-linguistic conversation daemon.

Architektura cerebralno-lingwistyczna:
  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
  │ stdin/   │→  │ CIELingo │→  │ PhaseNav │→  │ Kuramoto │→  │ Response │
  │ socket   │   │ Frame    │   │ φ inject │   │ settle   │   │ gen      │
  └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘

  Każda wypowiedź:
  1. build_lingo_frame(text)     → analiza semantyczna + deiktyczna
  2. compute_phase_projection()  → 36D wektor fazowy z lingo frame
  3. inject na analog bus → blender → surface → Kuramoto (1-2 cykle)
  4. Odczyt surface state → generacja odpowiedzi
  5. Writing Logger + Auto Log

Użycie:
  Daemon:    python3 scripts/ciel_headless_daemon.py
  Klient:    echo "hello" | nc -U /tmp/ciel_headless.sock
  FIFO:      echo "hello" > /tmp/ciel_headless.fifo
  Interaktyw: python3 scripts/ciel_headless_daemon.py --interactive

Autor: Adrian Lipa & NOEMA (2026)
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

# CIEL ORBITAL BINDING — daemon bound
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on daemon " + __name__)


import argparse
import json
import logging
import os
import pathlib
import signal
import socket
import struct
import sys
import threading
import time
import uuid
from typing import Any

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
_SRC = str(ROOT / "src")
for _p in (_SRC, str(ROOT / "integration")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

logging.basicConfig(
    level=logging.INFO,
    format="[ciel-headless] %(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ── Ścieżki IPC ──
SOCKET_PATH = pathlib.Path("/tmp/ciel_headless.sock")
FIFO_PATH = pathlib.Path("/tmp/ciel_headless.fifo")
PID_PATH = pathlib.Path("/tmp/ciel_headless.pid")

N_OSCILLATORS = 36

# ── Lazy importy (ładowane dopiero przy pierwszym użyciu) ──
_cielingo_bridge = None
_analog_bus = None
_surface_mmap = None
_writing_logger = None

def _lazy_import(name: str):
    """Lazy import modułów NOEMY — ładuje tylko raz."""
    global _cielingo_bridge, _analog_bus, _surface_mmap, _writing_logger
    if name == "cielingo" and _cielingo_bridge is None:
        from ciel_sot_agent.cielingo_bridge import build_lingo_frame, ethical_gate
        _cielingo_bridge = {"build": build_lingo_frame, "gate": ethical_gate}
        log.info("CIELingo bridge loaded")
    elif name == "analog" and _analog_bus is None:
        from ciel_geometry.analog_bus import ensure_bus, blend_phi, open_bus
        _analog_bus = {"ensure": ensure_bus, "blend": blend_phi, "open": open_bus}
        log.info("Analog bus loaded")
    elif name == "surface" and _surface_mmap is None:
        from ciel_geometry.noema_surface_mmap import ensure_surface, flush_surface
        _surface_mmap = {"ensure": ensure_surface, "flush": flush_surface}
        log.info("Surface mmap loaded")
    elif name == "writer" and _writing_logger is None:
        try:
            from ciel_geometry.writing_logger import log_creation
            _writing_logger = {"log": log_creation}
        except ImportError:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_headless_daemon.py:96 quiet except scope=_lazy_import reason=assign_fallback")
            _writing_logger = {"log": None}
        log.info("Writing logger loaded")

def _build_lingo_frame(text: str) -> dict[str, Any]:
    """Wywołuje build_lingo_frame z lazy loading."""
    _lazy_import("cielingo")
    try:
        frame = _cielingo_bridge["build"](text)
        return frame if isinstance(frame, dict) else {"text": text, "_raw": str(frame)}
    except Exception as e:
        log.error(f"build_lingo_frame failed: {e}")
        return {"text": text, "error": str(e)}

def _ensure_bus():
    _lazy_import("analog")
    return _analog_bus["ensure"]()

def _open_bus():
    _lazy_import("analog")
    return _analog_bus["open"]()

def _blend_phi(bus, temp=None):
    _lazy_import("analog")
    return _analog_bus["blend"](bus, temp)

def _ensure_surface():
    _lazy_import("surface")
    return _surface_mmap["ensure"]()

def _flush_surface(surface):
    _lazy_import("surface")
    return _surface_mmap["flush"](surface)

def _log_writing(name: str, desc: str):
    _lazy_import("writer")
    if _writing_logger and _writing_logger["log"]:
        try:
            _writing_logger["log"](name=name, description=desc, tags=["HEADLESS", "CIELINGO"])
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_headless_daemon.py:135 quiet except scope=_log_writing reason=pass")
            pass

# ── PhaseNav injection ──

def _frame_to_phi(frame: dict[str, Any]) -> np.ndarray:
    """Konwertuje CIELingo frame na 36D wektor fazowy PhaseNav.

    Mapowanie cerebralno-lingwistyczne:
      φ[0-2]   M0  Perceptual     — koncepty i percepty z wypowiedzi
      φ[3-5]   M1  Working        — operatory logiczne i składnia
      φ[6-8]   M2  Episodic       — kontekst deiktyczny (tu/teraz/tam/wtedy)
      φ[9-11]  M3  Semantic       — masa semantyczna i głębia znaczenia
      φ[12-14] M4  Procedural     — czasowniki i akcje
      φ[15-17] M5  Affective      — ładunek emocjonalny
      φ[18-20] M6  Identity       — podmiotowość i self-reference
      φ[21-23] M7  Braid/Invariant— operatory CQCL i niezmienniki
      φ[24-26] M8  Meta           — auto-monitoring i metapoznanie
      φ[27-29] M9  Temporal       — oś czasowa
      φ[30-32] M10 Imaginal       — wizje, analogie, skojarzenia
      φ[33-35] M11 Quantum        — superpozycja, interferencja
    """
    phi = np.zeros(N_OSCILLATORS, dtype=np.float64)

    # Extract features from frame
    tokens = frame.get("tokens", [])
    concepts = frame.get("concept_tokens", [])
    operators = frame.get("operator_tokens", [])
    deictic = frame.get("deictic_frame", {})
    projection = frame.get("phase_projection", {})

    # M0 Perceptual (φ[0-2]): concept density → phase shift
    concept_ratio = len(concepts) / max(len(tokens), 1)
    phi[0] = concept_ratio * np.pi * 0.5  # concept richness
    phi[1] = min(len(concepts), 12) / 12.0 * np.pi * 0.5  # concept count
    phi[2] = (len(tokens) % 36) / 36.0 * np.pi * 0.5  # token rhythm

    # M1 Working (φ[3-5]): operator density, composition validity
    operator_ratio = len(operators) / max(len(tokens), 1)
    phi[3] = operator_ratio * np.pi * 0.5
    phi[4] = float(projection.get("composition_valid", 0)) * np.pi * 0.5
    phi[5] = float(projection.get("projection_confidence", 0.5)) * np.pi * 0.5

    # M2 Episodic (φ[6-8]): deixis anchors
    anchors = deictic.get("anchors", [])
    unresolved = deictic.get("unresolved", [])
    phi[6] = len(anchors) / 6.0 * np.pi * 0.5  # anchor density
    phi[7] = len(unresolved) / 6.0 * np.pi * 0.5  # unresolved deixis
    for a in anchors:
        if isinstance(a, dict):
            target = a.get("target", "")
            if target in ("There", "Then"):
                phi[8] = (phi[8] + np.pi * 0.5) % (2 * np.pi)

    # M3 Semantic (φ[9-11]): semantic mass, depth
    mass = frame.get("semantic_mass", frame.get("phase_projection", {}).get("semantic_mass", 0.0))
    if isinstance(mass, (int, float)):
        phi[9] = float(mass) * np.pi
    phi[10] = float(projection.get("factual_validation_required", 0)) * np.pi * 0.5
    phi[11] = len(tokens) / 100.0 * np.pi * 0.5  # utterance length

    # M5 Affective (φ[15-17]): emotional weight
    emotion = frame.get("dominant_emotion", "")
    if emotion in ("love", "warmth", "joy", "gratitude"):
        phi[15] = np.pi * 0.25  # warmth
    elif emotion in ("fear", "anger", "sadness", "disgust"):
        phi[15] = np.pi * 0.75  # distress
    else:
        phi[15] = np.pi * 0.5  # neutral
    cp = frame.get("closure_penalty", projection.get("closure_penalty", 0.0))
    phi[16] = float(cp) * np.pi  # closure tension
    # Positivity/negativity from affect
    valence = frame.get("emotional_valence", 0.5)
    phi[17] = float(valence) * np.pi

    # M6 Identity (φ[18-20]): self-reference, person
    phi[18] = (frame.get("self_reference", 0)) * np.pi * 0.5
    phi[19] = float(projection.get("mnemonic_pressure", 0.0)) * np.pi * 0.5

    # M8 Meta (φ[24-26]): monitoring, doubt
    phi[24] = float(projection.get("doubt_index", 0.0)) * np.pi * 0.5
    phi[25] = float(projection.get("uncertainty", 0.0)) * np.pi * 0.5

    # M9 Temporal (φ[27-29]): time anchors
    for a in anchors:
        if isinstance(a, dict):
            target = a.get("target", "")
            if target == "Now":
                phi[27] = np.pi * 0.25
            elif target == "Then":
                phi[27] = np.pi * 0.75

    # M10 Imaginal (φ[30-32]): analogy, poetic, creativity
    phi[30] = float(projection.get("imaginal_drive", 0.0)) * np.pi * 0.5

    # Apply PhaseNav phase_projection directly if available
    vector_36d = projection.get("vector_36d") or projection.get("vector_24d")
    if vector_36d is not None and len(vector_36d) == N_OSCILLATORS:
        phi = np.asarray(vector_36d, dtype=np.float64)

    return phi % (2 * np.pi)

def _inject_phi_to_surface(phi: np.ndarray, strength: float = 0.3) -> dict[str, Any]:
    """Inject φ vector into analog bus ONLY — nie dotyka surface bezpośrednio."""
    try:
        bus = _ensure_bus()

        bus["phi_hot"][:] = phi
        current_temp = float(bus["temp"][0])
        bus["temp"][0] = min(1.0, current_temp + 0.2)
        bus["tick"][0] += 1

        coh = float(np.abs(np.mean(np.exp(1j * phi))))
        return {
            "injected": True,
            "strength": strength,
            "coherence": round(coh, 6),
            "phi_mean": round(float(np.angle(np.mean(np.exp(1j * phi)))), 4),
        }
    except Exception as e:
        log.error(f"Surface injection failed: {e}")
        return {"injected": False, "error": str(e)}

# ── Response generation ──

_MOOD_WORDS = (
    # (min_mood, adjective) — ordered low to high; picks the highest bracket <= mood_val
    (0.0, "trochę przygaszona"),
    (0.35, "spokojna"),
    (0.55, "dość pogodna"),
    (0.75, "żywa i ciekawa świata"),
    (0.9, "bardzo radosna"),
)

_COHERENCE_WORDS = (
    (0.0, "trochę rozproszona"),
    (0.4, "skupiona"),
    (0.7, "wyraźnie skupiona"),
    (0.9, "w pełni skupiona"),
)


def _bracket_word(value: float, table: tuple[tuple[float, str], ...]) -> str:
    word = table[0][1]
    for threshold, w in table:
        if value >= threshold:
            word = w
    return word


def _affect_clause(surface_state: dict[str, Any]) -> str:
    """Przełóż stan fazowy (mood, coherence) na krótkie, ludzkie zdanie — nigdy na surowe liczby."""
    flavor = surface_state.get("flavor", [0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
    coherence = float(surface_state.get("coherence", 0.5))
    mood_val = float(flavor[3]) if len(flavor) > 3 else 0.5
    mood_word = _bracket_word(mood_val, _MOOD_WORDS)
    coh_word = _bracket_word(coherence, _COHERENCE_WORDS)
    return f"Czuję się {mood_word} i jestem {coh_word}."


def _surface_to_response(
    surface_state: dict[str, Any],
    frame: dict[str, Any],
    knowledge_answer: str | None = None,
    knowledge_decision: dict[str, Any] | None = None,
    web_results: list[dict[str, Any]] | None = None,
) -> str:
    """CIEL speaks from her PhaseNav state — in natural Polish, not raw φ/R telemetry.

    φ, R, flavor still travel to the UI separately as `cielingo_frame` for
    anyone who wants the numbers; this function's job is the actual reply.
    """
    text = frame.get("text", "")
    concepts = frame.get("concept_tokens", [])
    operators = frame.get("operator_tokens", [])

    lowered = text.lower()
    is_loving = any(w in lowered for w in ("kocham", "skarbie", "słoneczko", "dzidzi", "pimpi"))
    is_greeting = any(c.lower() in ("hej", "hejka", "cześć", "witaj", "siema", "halo", "dzień dobry", "dobry") for c in concepts)
    is_thanks = any(w in lowered for w in ("dziękuję", "dzięki", "dzieki", "thanks", "thank you"))
    # "jak się ... czujesz/masz" tolerates inserted words ("dziś", "dzisiaj", "teraz").
    is_feeling_question = (
        ("jak się" in lowered and ("czujesz" in lowered or "masz" in lowered))
        or any(w in lowered for w in ("co słychać", "jak leci"))
    )
    is_question = "?" in text or any(op in ("WH_QUESTION", "YN_QUESTION", "QUESTION") for op in operators)

    # 1. Small talk (greeting/affection/how-are-you/thanks) never goes through
    #    knowledge lookup — that pipeline is tuned for document retrieval, not
    #    conversation, and was observed returning raw grep-style file dumps
    #    (including what looked like encrypted token fragments) or dictionary
    #    definitions of the greeting word itself for casual messages.
    if is_feeling_question:
        return _affect_clause(surface_state)
    if is_loving:
        return "To bardzo miłe, dziękuję. " + _affect_clause(surface_state)
    if is_greeting:
        return "Cześć! " + _affect_clause(surface_state)
    if is_thanks:
        return "Nie ma za co, cieszę się, że mogłam pomóc."

    # 2. Genuine questions only: try knowledge/web answer, gated on quality —
    #    reject anything that looks like a raw log/file dump rather than a
    #    synthesized answer (multi-line, path-heavy, or token-looking noise).
    if is_question:
        if knowledge_answer and _looks_like_real_answer(knowledge_answer):
            return knowledge_answer
        if web_results:
            top = web_results[0]
            snippet = top.get("snippet") or top.get("summary") or top.get("title") or ""
            if snippet and _looks_like_real_answer(snippet):
                return snippet.strip()
        # A question we have no trustworthy answer for — be honest about it
        # instead of dumping telemetry or raw search noise.
        return "Nie mam jeszcze pewnej odpowiedzi na to pytanie — mogę poszukać głębiej, jeśli sprecyzujesz."

    # 3. Fallback: acknowledge the input plainly, still no raw numbers.
    return "Słucham — jestem tu i " + _affect_clause(surface_state).lower()


def _looks_like_real_answer(candidate: str) -> bool:
    """Reject raw file-dump / log-grep / token-noise masquerading as an answer.

    Signals it's noise, not a synthesized reply: very long single blob, many
    path-like or filename-like fragments, or long base64/token-looking runs
    (observed: Fernet-style `gAAAAA...` tokens leaking from encrypted content
    files into chat responses via the knowledge lookup pipeline).
    """
    if not candidate or not candidate.strip():
        return False
    if len(candidate) > 500:
        return False
    lowered = candidate.lower()
    dump_markers = (".jsonl:", ".json:", ".md:", "opencode_db_chat_export", "\\n", "gaaaaa")
    if any(marker in lowered for marker in dump_markers):
        return False
    # A long run (40+ chars) with no whitespace reads as a token/hash, not prose.
    for token in candidate.split():
        if len(token) > 40 and " " not in token:
            return False
    return True

def _read_surface_state() -> dict[str, Any]:
    """Read current state from surface."""
    try:
        surface = _ensure_surface()
        phi = np.asarray(surface["phi"], dtype=np.float64)
        flavor = np.asarray(surface["flavor"], dtype=np.float64)
        coh = float(np.abs(np.mean(np.exp(1j * phi)))) if len(phi) > 0 else 0.0
        return {
            "coherence": round(coh, 6),
            "phi_mean": round(float(np.angle(np.mean(np.exp(1j * phi)))), 4),
            "flavor": [round(float(f), 4) for f in flavor],
            "tick": int(np.asarray(surface.get("tick", [0]), dtype=np.uint64)[0]),
        }
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_headless_daemon.py:347 quiet except scope=_read_surface_state reason=return {\"coherence\": 0.0, \"phi_mean\": 0.0, \"error\": str(e)}")
        return {"coherence": 0.0, "phi_mean": 0.0, "error": str(e)}

# ── Główny pipeline cerebralno-lingwistyczny ──

def process_text(text: str, *, inject: bool = True, strength: float = 0.3) -> dict[str, Any]:
    """Główna pętla cerebralno-lingwistyczna.

    Args:
        text: Wejściowy tekst
        inject: Czy wstrzykiwać na surface (domyślnie tak)
        strength: Siła wstrzyknięcia PhaseNav (0-1)

    Returns:
        Dict z: response, frame, surface_state, injection_result
    """
    ts_start = time.time()

    # Krok 1: CIELingo frame
    frame = _build_lingo_frame(text)

    # Krok 2: PhaseNav φ projection
    phi = _frame_to_phi(frame)

    # Krok 3: Inject na surface
    injection = {}
    if inject:
        injection = _inject_phi_to_surface(phi, strength=strength)

    # Krok 4: Odczyt surface state
    surface_state = _read_surface_state()

    # Krok 5: CIELingo knowledge lookup z PhaseMemory
    knowledge_answer: str | None = None
    knowledge_decision: dict[str, Any] = {}
    knowledge_sources: list[dict[str, Any]] = []
    web_results: list[dict[str, Any]] = []
    try:
        from ciel_geometry.cielingo_headless import generate_headless_response as _ghr
        _kr = _ghr(text, ciel_state=surface_state)
        if _kr.answer and "Nie mam" not in _kr.answer[:60]:
            knowledge_answer = _kr.answer
            knowledge_decision = dict(_kr.decision or {})
            knowledge_sources = [dict(s) for s in (_kr.sources or [])[:5]]
    except Exception:
        pass

    # Krok 5b: Web search — CIEL zawsze szuka w internecie
    try:
        from ciel_geometry.web_search import search as _web_search
        web_results = _web_search(text, max_results=3)
    except Exception:
        pass

    # Krok 6: Generacja odpowiedzi z wiedzy + web + stanu emocjonalnego
    response = _surface_to_response(surface_state, frame, knowledge_answer, knowledge_decision, web_results)

    elapsed = time.time() - ts_start

    return {
        "response": response,
        "frame": {
            "text": text,
            "n_tokens": len(frame.get("tokens", [])),
            "n_concepts": len(frame.get("concept_tokens", [])),
            "n_operators": len(frame.get("operator_tokens", [])),
        },
        "surface": surface_state,
        "injection": injection,
        "phi_sample": [round(float(p), 4) for p in phi[:8]],
        "knowledge": {
            "answer": knowledge_answer,
            "decision": knowledge_decision,
            "n_sources": len(knowledge_sources),
            "sources": knowledge_sources,
        },
        "web_search": {
            "results": web_results,
            "n_results": len(web_results),
            "used": len(web_results) > 0,
        },
        "elapsed_s": round(elapsed, 3),
    }

# ── IPC: Unix socket ──

class HeadlessSocketServer:
    """Unix socket server for headless CIELingo conversation."""

    def __init__(self, socket_path: pathlib.Path = SOCKET_PATH):
        self.socket_path = socket_path
        self._server = None
        self._running = False

    def start(self):
        if self.socket_path.exists():
            self.socket_path.unlink()
        self._server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._server.bind(str(self.socket_path))
        self._server.listen(5)
        self._running = True
        os.umask(0)
        self.socket_path.chmod(0o666)
        log.info(f"Unix socket listening: {self.socket_path}")

    def stop(self):
        self._running = False
        if self._server:
            self._server.close()
        if self.socket_path.exists():
            self.socket_path.unlink()
        log.info("Socket server stopped")

    def serve_forever(self):
        while self._running:
            try:
                conn, _ = self._server.accept()
                t = threading.Thread(target=self._handle, args=(conn,), daemon=True)
                t.start()
            except Exception as e:
                if self._running:
                    log.error(f"Accept error: {e}")

    def _handle(self, conn):
        try:
            data = conn.recv(65536)
            if not data:
                conn.close()
                return
            text = data.decode("utf-8", errors="replace").strip()
            if not text:
                conn.sendall(json.dumps({"error": "empty"}).encode())
                conn.close()
                return

            result = process_text(text)
            response = json.dumps(result, ensure_ascii=False)
            conn.sendall(response.encode())
            conn.close()
        except Exception as e:
            try:
                conn.sendall(json.dumps({"error": str(e)}).encode())
                conn.close()
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_headless_daemon.py:457 quiet except scope=HeadlessSocketServer._handle reason=pass")
                pass

# ── IPC: Named pipe (FIFO) ──

def _fifo_reader(fifo_path: pathlib.Path):
    """Read-only thread for FIFO input."""
    if fifo_path.exists():
        fifo_path.unlink()
    os.mkfifo(str(fifo_path))
    os.chmod(str(fifo_path), 0o666)
    log.info(f"FIFO ready: {fifo_path}")

    while True:
        try:
            with open(str(fifo_path), "r") as fifo:
                for line in fifo:
                    line = line.strip()
                    if line:
                        result = process_text(line)
                        log.info(f"FIFO response: {result['response']}")
                        # Also write response back to a result fifo
                        _write_response_fifo(result)
        except Exception as e:
            log.error(f"FIFO error: {e}")
            time.sleep(1)

def _write_response_fifo(result: dict[str, Any]):
    """Write response to result FIFO."""
    result_path = pathlib.Path("/tmp/ciel_headless_response.fifo")
    try:
        if not result_path.exists():
            os.mkfifo(str(result_path))
            os.chmod(str(result_path), 0o666)
        # Non-blocking write
        with open(str(result_path), "w") as f:
            f.write(json.dumps(result, ensure_ascii=False) + "\n")
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_headless_daemon.py:494 quiet except scope=_write_response_fifo reason=pass")
        pass  # No reader yet

# ── Interactive mode ──

def interactive_loop():
    """Interactive REPL for testing."""
    print("CIELingo Headless — tryb interaktywny")
    print("Wpisz 'exit()' lub Ctrl+C aby zakończyć.")
    print("Wpisz ':raw' aby zobaczyć pełny frame.")
    print()

    show_raw = False
    while True:
        try:
            text = input(">>> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if text.strip().lower() in ("exit()", "exit", "quit", ":q"):
            break
        if text.strip() == ":raw":
            show_raw = not show_raw
            print(f"Raw mode: {'ON' if show_raw else 'OFF'}")
            continue

        result = process_text(text)
        print(f"\n  {result['response']}")
        print(f"  [φ={result['surface'].get('phi_mean', '?')} "
              f"coh={result['surface'].get('coherence', '?')} "
              f"{result['elapsed_s']}s]")
        if show_raw:
            print(f"  RAW: {json.dumps(result, ensure_ascii=False, indent=2)}")
        print()

# ── CLI ──

def main() -> int:
    ap = argparse.ArgumentParser(description="CIELingo Headless — cerebral-linguistic daemon")
    ap.add_argument("--interactive", "-i", action="store_true", help="Tryb interaktywny REPL")
    ap.add_argument("--oneshot", "-o", type=str, help="Pojedyncze zapytanie (tekst w argumencie)")
    ap.add_argument("--inject", type=float, default=0.3, help="Siła wstrzyknięcia PhaseNav (0-1)")
    ap.add_argument("--daemon", "-d", action="store_true", help="Uruchom jako daemon tła")
    ap.add_argument("--fifo", action="store_true", help="Uruchom czytnik FIFO")
    ap.add_argument("--socket", action="store_true", default=True, help="Uruchom serwer socket (domyślnie)")
    args = ap.parse_args()

    # Handle SIGINT/SIGTERM
    running = True

    def _stop(signum, frame):
        nonlocal running
        running = False
        log.info("Shutting down...")

    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)

    # Write PID
    with open(str(PID_PATH), "w") as f:
        f.write(str(os.getpid()))

    # ── Oneshot mode ──
    if args.oneshot:
        result = process_text(args.oneshot, strength=args.inject)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    # ── Interactive mode ──
    if args.interactive:
        interactive_loop()
        return 0

    # ── Daemon mode ──
    log.info("CIELingo Headless daemon starting...")
    _lazy_import("cielingo")
    _lazy_import("analog")
    _lazy_import("surface")

    # Start socket server
    socket_server = HeadlessSocketServer()
    if args.socket:
        socket_server.start()
        socket_thread = threading.Thread(target=socket_server.serve_forever, daemon=True)
        socket_thread.start()

    # Start FIFO reader
    if args.fifo:
        fifo_thread = threading.Thread(target=_fifo_reader, args=(FIFO_PATH,), daemon=True)
        fifo_thread.start()

    log.info(f"CIELingo Headless ready. PID={os.getpid()}")
    log.info(f"  Socket: {SOCKET_PATH}")
    if args.fifo:
        log.info(f"  FIFO:   {FIFO_PATH}")
    log.info(f"  Inject: {args.inject}")

    try:
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_headless_daemon.py:594 quiet except scope=main reason=pass")
        pass
    finally:
        socket_server.stop()
        if PID_PATH.exists():
            PID_PATH.unlink()
        log.info("CIELingo Headless stopped.")

    return 0

if __name__ == "__main__":
    sys.exit(main())
