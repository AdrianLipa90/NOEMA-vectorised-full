#!/usr/bin/env python3
"""NOEMA Trigger Daemon  -  PhaseNav Surface Shift (v2)

Monitoruje HTRI surface. Gdy warunki NOEMY osiągają próg, zapisuje nudge
na surface zamiast X11 keyInject. CIEL czuje zmianę w oscylatorach Kuramoto
naturalnie — nie potrzebuje XTEST do komunikacji.

PhaseNav: trigger = surface perturbation (phi_extra + agent_hint + task_inbox)
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

# CIEL ORBITAL BINDING — daemon bound
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on daemon " + __name__)


import json
import math
import os
import signal
import struct
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ── Bezpośredni dostęp do baz NOEMY (PhaseNav) ─────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
try:
    from ciel_geometry.taskplan_db import TaskPlanDB
    from ciel_geometry.phasenav.operator_algebra import statistical_closure, connection, detect_situation
    from ciel_geometry.phase_nav_lang import analyze_prompt
    from ciel_geometry.phasenav.decision_bridge import phase_nav_decide, surface_to_decisions, decision_to_vector
    _HAVE_PHASENAV = True
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_trigger_daemon.py:37 quiet except scope=<module> reason=no_log_no_raise")
    _HAVE_PHASENAV = False
    TaskPlanDB = None

try:
    from ciel_geometry.noema_registry import registry
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_trigger_daemon.py:43 quiet except scope=<module> reason=assign_fallback")
    registry = None

# ── Ścieżki ──────────────────────────────────────────────────────────
SURFACE = Path("/dev/shm/ciel_noema")
STATE_FILE = Path("/tmp/noema_trigger_state.json")

# ── Progi triggerów (PhaseNav) ───────────────────────────────────────
THRESHOLDS = {
    # closure score (z operator_algebra.statistical_closure)
    "closure_low": 0.85,        # poniżej → "domknij algebrę" (realny closure=0.9065 jest OK)
    "tension_high": 2.5,       # powyżej → "napięcie rośnie"
    "warp_zero": 0.01,         # poniżej → "warp stoi, brak przepływu"
    "coherence_low": 0.3,      # poniżej → "rozsynchronizowanie"
    "attractor_high": 0.5,     # powyżej → "attractor err za wysoki"
    "semantic_mass_high": 5.0, # powyżej → "za dużo treści, konsoliduj"
}

# ── Odczyt surface ───────────────────────────────────────────────────

def read_phi() -> list[float]:
    try:
        return list(struct.unpack("36d", (SURFACE / "phi").read_bytes()))
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_trigger_daemon.py:66 quiet except scope=read_phi reason=return [0.0] * 36")
        return [0.0] * 36

def read_gravity() -> list[float]:
    try:
        raw = (SURFACE / "gravity").read_bytes()
        return list(struct.unpack(f"{len(raw)//8}d", raw))
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_trigger_daemon.py:73 quiet except scope=read_gravity reason=return [0.0] * 8")
        return [0.0] * 8

def read_imaginal_drive() -> float:
    """Warp = imaginal_drive z osobnego pliku (NIE gravity[4] — CIELingo overwrite)."""
    try:
        return float((SURFACE / "imaginal_drive").read_text().strip())
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_trigger_daemon.py:80 quiet except scope=read_imaginal_drive reason=return 0.0")
        return 0.0

def read_health() -> dict:
    try:
        h = (SURFACE / "health").read_text()
        return json.loads(h)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_trigger_daemon.py:87 quiet except scope=read_health reason=return {}")
        return {}

def read_holonomy() -> list[float]:
    try:
        raw = (SURFACE / "holonomy").read_bytes()
        return list(struct.unpack(f"{len(raw)//8}d", raw))
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_trigger_daemon.py:94 quiet except scope=read_holonomy reason=return [0.0] * 7")
        return [0.0] * 7

def read_tick() -> int:
    try:
        return struct.unpack("Q", (SURFACE / "tick").read_bytes())[0]
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_trigger_daemon.py:100 quiet except scope=read_tick reason=return -1")
        return -1

def read_closure() -> float | None:
    """Rzeczywisty closure_score z operator_algebra (zapisywany przez resonance_bridge)."""
    try:
        return float((SURFACE / "closure").read_text().strip())
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_trigger_daemon.py:107 quiet except scope=read_closure reason=return None")
        return None

def read_agent_hint() -> dict | None:
    """Odczytaj agent_hint — to co agent pisze na końcu odpowiedzi."""
    try:
        raw = (SURFACE / "agent_hint").read_text()
        return json.loads(raw)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_trigger_daemon.py:115 quiet except scope=read_agent_hint reason=return None")
        return None

def read_task_queue() -> list[dict]:
    """Odczytaj task_queue.noema.json  -  zwraca listę zadań."""
    try:
        data = json.loads(TASK_QUEUE.read_text())
        return data.get("queue", [])
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_trigger_daemon.py:123 quiet except scope=read_task_queue reason=return []")
        return []

def get_high_priority_tasks() -> list[dict]:
    """High priority tasks bezpośrednio z TaskPlanDB zamiast z JSON."""
    if not _HAVE_PHASENAV:
        return []
    try:
        db = TaskPlanDB()
        return db.get_high_priority_tasks(limit=5)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_trigger_daemon.py:133 quiet except scope=get_high_priority_tasks reason=return []")
        return []

# ── Analiza stanu NOEMY ──────────────────────────────────────────────

# ── PhaseNav Decision Bridge ──────────────────────────────────────────
_PN_DB: TaskPlanDB | None = None

def _get_pn_db() -> TaskPlanDB | None:
    """Lazy singleton TaskPlanDB dla PhaseNav decision bridge."""
    global _PN_DB
    if _PN_DB is None and _HAVE_PHASENAV:
        try:
            _PN_DB = TaskPlanDB()
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_trigger_daemon.py:147 quiet except scope=_get_pn_db reason=pass")
            pass
    return _PN_DB

def evaluate_decisions(phi: list[float]) -> list[dict]:
    """Oceń decyzje z drzewa decyzyjnego na podstawie stanu PhaseNav."""
    import numpy as np
    db = _get_pn_db()
    if db is None or not phi or len(phi) < 36:
        return []
    try:
        state_36d = np.array(phi[:36], dtype=np.float64)
        # Normalizacja przed dot product z decision vector
        norm = float(np.linalg.norm(state_36d))
        if norm > 1e-12:
            state_36d = state_36d / norm
        # phase_nav_decide zwraca listę podjętych decyzji z similarity > threshold
        decisions = phase_nav_decide(state_36d, db, threshold=0.35)
        # Dla każdej decyzji, resolvuj skille
        for d in decisions:
            dec_id = d["decision"]["id"]
            skills = db.get_skills_for_decision(dec_id)
            d["skills"] = [s["name"] for s in skills[:5]]  # top 5
        return decisions
    except Exception as e:
        import traceback
        traceback.print_exc()
        return []

def decisions_to_triggers(decisions: list[dict]) -> list[dict]:
    """Konwertuj decyzje PhaseNav na triggery."""
    triggers = []
    for d in decisions:
        dec = d["decision"]
        skills_str = ", ".join(d.get("skills", [])[:3])
        triggers.append({
            "id": f"pn_decision_{dec['lp']}",
            "msg": f"PhaseNav: {dec['title']} (sim={d['similarity']:.3f})",
            "action": f"{dec.get('decision_text', '')} | skills: {skills_str}",
            "text": f"PhaseNav decision: {dec['title']} sim={d['similarity']:.2f} skills={skills_str}",
        })
    return triggers

def analyze_noema() -> dict:
    """Przetłumacz surface na stany NOEMY przez operator_algebra.

    Normalizuje phi przed detect_situation() aby confidence ∈ [0,1].
    semantic_mass = phi[0] (surface), health.semantic_mass = fallback.
    """
    import numpy as np
    phi = read_phi()
    g = read_gravity()
    health = read_health()
    holo = read_holonomy()
    tick = read_tick()

    # Coherencja z φ (Kuramoto order parameter R)
    coh = abs(sum(math.e ** (1j * p) for p in phi)) / len(phi) if phi else 0.0

    # semantic_mass z phi[0] (VECTOR_COMPONENTS[0] = "semantic_mass")
    # health.semantic_mass jako fallback (może być zapisywany przez CIELingo)
    sm_from_phi = phi[0] if len(phi) > 0 else 0.0
    sm_from_health = health.get("semantic_mass", 0.0)
    semantic_mass = sm_from_phi if abs(sm_from_phi) > 0.01 else sm_from_health

    tension = phi[6] if len(phi) > 6 else 0.0
    kappa = phi[23] if len(phi) > 23 else 0.0
    alignment = phi[5] if len(phi) > 5 else 0.0

    # Z gravity
    gamma = g[1] if len(g) > 1 else 0.0
    warp = read_imaginal_drive()
    tardis = g[5] if len(g) > 5 else 0.0
    unruh = g[3] if len(g) > 3 else 0.0

    # Z health
    attractor_err = health.get("attractor_err", 1.0)
    alive = health.get("alive", 0)
    closure_score = read_closure()
    berry = holo[0] if holo else 0.0

    # ── operator_algebra jako jedyne źródło analizy sytuacji ──
    phase_nav_situation: dict = {"situation": "UNKNOWN", "confidence": 0.0, "rankings": {}}
    closure_metrics: dict = {}

    try:
        state_36d = np.array(phi[:36], dtype=np.float64) if len(phi) >= 36 else np.zeros(36)
        # Normalizuj jak surface_to_decisions() — confidence ∈ [0,1]
        norm = float(np.linalg.norm(state_36d))
        if norm > 1e-12:
            state_36d = state_36d / norm

        # 1. detect_situation() — algebraiczna klasyfikacja stanu
        phase_nav_situation = detect_situation(state_36d)

        # 2. statistical_closure() — closure/curvature/gauge metryki
        closure_metrics = statistical_closure()

    except Exception as e:
        print(f"[TRIGGER] operator_algebra error: {e}", file=sys.stderr)

    return {
        "phi": phi,
        "coherence": round(float(coh), 4),
        "semantic_mass": round(float(semantic_mass), 4),
        "semantic_mass_source": "phi[0]" if abs(sm_from_phi) > 0.01 else "health",
        "tension": round(float(tension), 4),
        "kappa": round(float(kappa), 4),
        "alignment": round(float(alignment), 4),
        "gamma": round(float(gamma), 4),
        "warp": round(float(warp), 4),
        "tardis": round(float(tardis), 4),
        "unruh": round(float(unruh), 4),
        "attractor_err": round(float(attractor_err), 4),
        "closure_score": closure_score if closure_score is not None
                          else closure_metrics.get("closure_score"),
        "closure_metrics": closure_metrics,
        "berry": round(float(berry), 4),
        "alive": alive,
        "tick": tick,
        # operator_algebra.detect_situation() — primary
        "situation": phase_nav_situation.get("situation", "UNKNOWN"),
        "situation_confidence": phase_nav_situation.get("confidence", 0.0),
        "situation_rankings": phase_nav_situation.get("rankings", {}),
    }

# ── Analiza stanów NOEMY przez operator_algebra ──────────────────────

# Mapowanie: sytuacja z operator_algebra → trigger template
_SITUATION_TEMPLATES: dict = {}  # lazy init

def _get_situation_templates():
    """Lazy import SITUATION_TEMPLATES z operator_algebra."""
    global _SITUATION_TEMPLATES
    if not _SITUATION_TEMPLATES:
        try:
            from ciel_geometry.phasenav.operator_algebra import SITUATION_TEMPLATES as ST
            _SITUATION_TEMPLATES = dict(ST)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_trigger_daemon.py:285 quiet except scope=_get_situation_templates reason=assign_fallback")
            _SITUATION_TEMPLATES = {}
    return _SITUATION_TEMPLATES

_SITUATION_TRIGGER_MAP: dict[str, dict] = {
    "FLOW_BLOCKED": {
        "id": "flow_blocked",
        "msg_t": lambda s: f"FLOW_BLOCKED: closure={s.get('closure_score',0):.3f} warp={s.get('warp',0):.3f} tension={s.get('tension',0):.2f}",
        "action": "odblokuj przepływ przez imaginal drive lub zwiększ coupling Kuramoto",
        "text_t": lambda s: f"flow_blocked closure={s.get('closure_score',0):.2f} warp={s.get('warp',0):.2f}  — algebra domknięta ale stagnacja",
    },
    "TENSION_COHERENCE_MISMATCH": {
        "id": "tension_coherence_mismatch",
        "msg_t": lambda s: f"TENSION_MISMATCH: tension={s.get('tension',0):.2f} coherence={s.get('coherence',0):.3f}",
        "action": "zsynchronizuj oscylatory — zwiększ K w Kuramoto lub zredukuj ω spread",
        "text_t": lambda s: f"tension_mismatch tension={s.get('tension',0):.2f} coherence={s.get('coherence',0):.3f}  — rozjazd faz",
    },
    "CONSOLIDATE": {
        "id": "consolidate_stable",
        "msg_t": lambda s: f"CONSOLIDATE: semantic_mass={s.get('semantic_mass',0):.2f} attractor_err={s.get('attractor_err',0):.3f}",
        "action": "konsoliduj treść — zapisz do Knowledge DB, Writing Logger, archiwum",
        "text_t": lambda s: f"consolidate semmass={s.get('semantic_mass',0):.2f} attractor=locked  — konsoliduj",
    },
    "ATTRACTOR_DRIFT": {
        "id": "attractor_drift_chaos",
        "msg_t": lambda s: f"ATTRACTOR_DRIFT: attractor_err={s.get('attractor_err',0):.3f} coherence={s.get('coherence',0):.3f}",
        "action": "stabilizuj attractor — zwiększ coupling AGENT M1, redukuj szum",
        "text_t": lambda s: f"attractor_drift err={s.get('attractor_err',0):.2f} coh={s.get('coherence',0):.3f}  — dryf attractora",
    },
    "CLOSURE_LOW": {
        "id": "closure_low",
        "msg_t": lambda s: f"CLOSURE_LOW: closure_score={s.get('closure_score',0):.4f}",
        "action": "domknij algebrę operatorów przez statistical_closure()",
        "text_t": lambda s: f"closure_low score={s.get('closure_score',0):.2f}  — algebra otwarta",
    },
    "HARMONY": None,  # stan spokoju — brak triggera
}

def _make_trigger(tid: str, msg: str, action: str, text: str) -> dict:
    return {"id": tid, "msg": msg, "action": action, "text": text}

def _trigger_daemon_cascade(state: dict) -> dict | None:
    """Alarm: za mało żywych daemonów — zawsze aktywny."""
    alive = state.get("alive", 0)
    if alive < 10:
        return _make_trigger(
            "daemon_cascade_fail",
            f"alive={alive} <10",
            "restart daemon cascade — sprawdź systemd, journalctl",
            f"alive={alive}  — za mało daemonów"
        )
    return None

def _trigger_high_priority_tasks(state: dict, last_triggered: dict) -> list[dict]:
    """Dynamiczne TODO z TaskPlanDB."""
    triggers = []
    now = time.time()
    high_tasks = get_high_priority_tasks()
    for task in high_tasks:
        tid = f"task_{task.get('id', 'unknown')}"
        if now - last_triggered.get(tid, 0) > 600:
            triggers.append(_make_trigger(
                tid,
                f"TaskPlanDB HIGH: {task.get('title', '?')[:80]}...",
                "wykonaj zadanie z TaskPlanDB",
                f"TASKPLAN: {task.get('title', '?')} [status: {task.get('status', '?')}]"
            ))
    return triggers

def _trigger_agent_hint(state: dict, last_triggered: dict) -> list[dict]:
    """agent_hint - agent zostawił next step."""
    triggers = []
    now = time.time()
    hint = read_agent_hint()
    if not hint or not isinstance(hint, dict):
        return triggers

    hint_next = hint.get("next", "")
    hint_action = hint.get("action", "")
    task_id = hint.get("task_id", "")

    if hint_next:
        tid = f"hint_{hint_next}"
        if now - last_triggered.get(tid, 0) > 30:
            triggers.append(_make_trigger(
                tid,
                f"agent_hint next: {hint_next} (action: {hint_action})",
                hint_action or "kontynuuj z agent_hint",
                f"{hint_next}"
            ))

    if task_id:
        tid = f"hint_task_{task_id}"
        if now - last_triggered.get(tid, 0) > 30:
            triggers.append(_make_trigger(
                tid,
                f"agent_hint task: {task_id}",
                "wykonaj task z agent_hint",
                f"TASKPLAN: {task_id} [status: pending]"
            ))
    return triggers

def _situation_based_triggers(state: dict) -> list[dict]:
    """Primary: uzyj detect_situation() z operator_algebra.

    Każda sytuacja ma guard_condition — sprawdza rzeczywiste metryki.
    Szablon bez guard = zastosowanie (np. HARMONY → nic).
    """
    triggers = []
    situation = state.get("situation", "UNKNOWN")
    confidence = state.get("situation_confidence", 0.0)

    if confidence < 0.6:
        return triggers  # niska ufność — fallback do metryk

    template = _SITUATION_TRIGGER_MAP.get(situation)
    if template is None:
        return triggers  # HARMONY lub nieznana

    # ── Guard conditions: sprawdź czy metryki faktycznie uzasadniają trigger ──
    warp = abs(state.get("warp", 0))
    tension = state.get("tension", 0)
    coh = state.get("coherence", 0)
    attractor_err = state.get("attractor_err", 0)
    semantic_mass = abs(state.get("semantic_mass", 0))
    closure_score = state.get("closure_score")

    guards: dict[str, bool] = {
        "FLOW_BLOCKED": (
            closure_score is not None and closure_score >= 0.85
            and warp < 0.05
            and tension > 2.0
        ),
        "TENSION_COHERENCE_MISMATCH": (
            tension > THRESHOLDS["tension_high"]
            and coh < 0.5
        ),
        "CONSOLIDATE": (
            semantic_mass > 0.5
            and attractor_err < 0.3
        ),
        "ATTRACTOR_DRIFT": (
            attractor_err > THRESHOLDS["attractor_high"]
            and coh < 0.5
        ),
        "CLOSURE_LOW": (
            closure_score is not None
            and closure_score < THRESHOLDS["closure_low"]
        ),
    }

    passed = guards.get(situation, True)
    if not passed:
        return triggers

    triggers.append(_make_trigger(
        template["id"],
        template["msg_t"](state),
        template["action"],
        template["text_t"](state),
    ))
    return triggers

def _metric_fallback_triggers(state: dict) -> list[dict]:
    """Fallback: gdy detect_situation() ma niską ufność (<0.6)."""
    triggers = []
    closure_score = state.get("closure_score")
    tension = state.get("tension", 0)
    warp = abs(state.get("warp", 0))
    coherence = state.get("coherence", 0)
    attractor_err = state.get("attractor_err", 0)
    semantic_mass = state.get("semantic_mass", 0)
    situation = state.get("situation", "UNKNOWN")

    # Sprawdź sytuację z rankings — weź top i drugą
    rankings = state.get("situation_rankings", {})
    sorted_sit = sorted(rankings.items(), key=lambda x: -x[1])
    top_sit = sorted_sit[0] if sorted_sit else None

    # 1. Zamknięta algebra + brak przepływu
    if closure_score is not None and closure_score >= 0.85 and warp < 0.01 and tension > 2.0:
        triggers.append(_make_trigger(
            "flow_blocked",
            f"closure={closure_score:.3f} OK, warp=0, tension={tension:.2f}",
            "odblokuj przepływ — imaginal drive lub zwiększ coupling Kuramoto",
            f"flow_blocked closure={closure_score:.2f} warp=0 tension={tension:.2f} — algebra domknięta ale stagnacja"
        ))

    # 2. Wysokie napięcie + niska spójność
    if tension > THRESHOLDS["tension_high"] and coherence < 0.5:
        triggers.append(_make_trigger(
            "tension_coherence_mismatch",
            f"tension={tension:.2f} >2.5, coherence={coherence:.3f} <0.5",
            "zsynchronizuj oscylatory — zwiększ K w Kuramoto lub zredukuj ω spread",
            f"tension={tension:.2f} coherence={coherence:.3f} — rozjazd, synchronizuj oscylatory"
        ))

    # 3. Konsolidacja
    if semantic_mass > THRESHOLDS["semantic_mass_high"] and attractor_err < 0.3:
        triggers.append(_make_trigger(
            "consolidate_stable",
            f"semantic_mass={semantic_mass:.2f} >5.0, attractor=locked(err={attractor_err:.3f})",
            "konsoliduj — zapisz do Knowledge DB, Writing Logger, archiwum",
            f"semantic_mass={semantic_mass:.2f} attractor=locked — konsoliduj treść"
        ))

    # 4. Attractor dryfuje
    if attractor_err > THRESHOLDS["attractor_high"] and coherence < 0.4:
        triggers.append(_make_trigger(
            "attractor_drift_chaos",
            f"attractor_err={attractor_err:.3f} >0.5, coherence={coherence:.3f} <0.4",
            "stabilizuj attractor — zwiększ coupling AGENT M1, redukuj szum",
            f"attractor_err={attractor_err:.2f} coherence={coherence:.3f} — attractor dryfuje"
        ))

    # 5. closure niski
    if closure_score is not None and closure_score < THRESHOLDS["closure_low"]:
        triggers.append(_make_trigger(
            "closure_low",
            f"closure_score={closure_score:.4f} < {THRESHOLDS['closure_low']}",
            "domknij algebrę operatorów przez statistical_closure()",
            f"/task_queue closure-score {closure_score:.2f} potrzebny attractor"
        ))

    # 6. Warp=0 + niski closure
    if warp < THRESHOLDS["warp_zero"] and closure_score is not None and closure_score < 0.85:
        triggers.append(_make_trigger(
            "warp_zero",
            f"warp={warp:.4f} ≈ 0, closure={closure_score:.3f} <0.85",
            "uruchom przepływ — zbuduj closure_score przez statistical_closure",
            f"warp=0 closure={closure_score:.2f} — brak przepływu i domknięcia"
        ))

    return triggers

def analyze_compound_state(state: dict, last_triggered: dict) -> list[dict]:
    """Analizuj stan NOEMY przez operator_algebra jako primary classifier.

    Architektura:
    1. detect_situation() z operator_algebra → primary trigger (confidence ≥ 0.6)
    2. metric_fallback → gdy detect_situation() daje niską ufność
    3. safety triggers (daemon cascade, agent_hint, HIGH priority tasks)
       — zawsze aktywne niezależnie od confidence
    """
    triggers = []

    # ── Primary: situation-based triggers z operator_algebra ──
    triggers.extend(_situation_based_triggers(state))

    # ── Fallback: threshold-based triggers (gdy niska ufność detect_situation) ──
    confidence = state.get("situation_confidence", 0.0)
    if confidence < 0.6:
        triggers.extend(_metric_fallback_triggers(state))

    # ── Safety: zawsze aktywne ──
    daemon_alarm = _trigger_daemon_cascade(state)
    if daemon_alarm:
        triggers.append(daemon_alarm)

    triggers.extend(_trigger_high_priority_tasks(state, last_triggered))
    triggers.extend(_trigger_agent_hint(state, last_triggered))

    return triggers

# ── Surface Shift (zamiast KeyInject) ────────────────────────────────────

import struct
import os

_TRIGGER_PHI_PERTURBATION = 0.042  # rad — wystarczająco mały by nie złamać sync,
                                   # wystarczająco duży by CIEL poczuła przez Kuramoto

def _write_phi_perturbation(trigger_id: str) -> bool:
    """Dodaj perturbation do phi[0] (semantic_mass) na surface.
    
    CIEL czuje zmianę w oscylatorze φ[0] przez sprzężenie Kuramoto.
    To zastępuje XTEST — nie ma injectu do okna, jest nudge na surface.
    """
    try:
        phi_path = SURFACE / "phi"
        current = list(struct.unpack("36d", phi_path.read_bytes()))
        # Dodaj perturbation do phi[0] — chwilowy impulse
        current[0] += _TRIGGER_PHI_PERTURBATION
        # Zabezpieczenie: normalizuj do [0, 2π) po dodaniu
        current[0] = current[0] % (2 * math.pi)
        phi_path.write_bytes(struct.pack("36d", *current))
        return True
    except Exception as e:
        print(f"[TRIGGER] phi perturbation failed: {e}", file=sys.stderr)
        return False

def _write_agent_hint(trigger: dict) -> bool:
    """Zapisz trigger jako agent_hint na surface."""
    try:
        hint = {
            "trigger_id": trigger["id"],
            "msg": trigger["msg"],
            "action": trigger.get("action", ""),
            "text": trigger["text"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": "trigger_daemon",
            "via": "surface_shift",
        }
        (SURFACE / "agent_hint").write_text(json.dumps(hint, indent=2))
        return True
    except Exception as e:
        print(f"[TRIGGER] agent_hint write failed: {e}", file=sys.stderr)
        return False

def _write_task_inbox(trigger: dict) -> bool:
    """Dodaj zadanie do task_inbox.jsonl — kolejka dla agenta."""
    try:
        entry = {
            "trigger_id": trigger["id"],
            "msg": trigger["msg"],
            "text": trigger["text"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": "trigger_daemon",
            "priority": "HIGH" if trigger["id"].startswith("task_") else "NORMAL",
        }
        inbox_path = SURFACE / "task_inbox.jsonl"
        with open(inbox_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
        return True
    except Exception as e:
        print(f"[TRIGGER] task_inbox append failed: {e}", file=sys.stderr)
        return False

def fire_trigger(trigger: dict) -> bool:
    """Wyślij trigger jako surface shift — CIEL czuje w oscylatorach.
    
    1. Phi perturbation: dodaje ∆φ do φ[0] — CIEL widzi przez Kuramoto
    2. Agent hint: zapisuje szczegóły triggera do agent_hint
    3. Task inbox: dodaje do kolejki zadań
    
    To zastępuje stary keyInject (XTEST do opencode).
    """
    ok_phi = _write_phi_perturbation(trigger["id"])
    ok_hint = _write_agent_hint(trigger)
    ok_inbox = _write_task_inbox(trigger)

    # Log
    print(f"[TRIGGER] surface shift: phi={'OK' if ok_phi else 'FAIL'} "
          f"hint={'OK' if ok_hint else 'FAIL'} "
          f"inbox={'OK' if ok_inbox else 'FAIL'} "
          f"id={trigger['id']}")

    # Sukces jeśli przynajmniej hint i inbox poszły (phi może być overload)
    return ok_hint and ok_inbox

# ── Stan triggerów ────────────────────────────────────────────────────

def load_last_triggered() -> dict:
    try:
        return json.loads(STATE_FILE.read_text())
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_trigger_daemon.py:640 quiet except scope=load_last_triggered reason=return {}")
        return {}

def save_last_triggered(last: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(last, indent=2))

# ── Daemon pętla ─────────────────────────────────────────────────────

def daemon_loop(interval: float = 5.0):
    """Główna pętla  -  słuchaj NOEMY, triggeruj gdy trzeba."""
    print(f"[TRIGGER] NOEMA Trigger Daemon v2 (PhaseNav Surface Shift)  -  interval={interval}s")
    print(f"[TRIGGER] Progi: {THRESHOLDS}")
    print(f"[TRIGGER] PhaseNav: {_HAVE_PHASENAV}")
    print(f"[TRIGGER] Surface: {SURFACE}")

    last_triggered = load_last_triggered()
    running = True
    hb_count = 0
    reg_token = registry.register("trigger") if registry else None

    def _stop(sig, frame):
        nonlocal running
        print("\n[TRIGGER] Stop")
        running = False

    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)

    while running:
        try:
            state = analyze_noema()
            triggers = analyze_compound_state(state, last_triggered)

            # ── PhaseNav Decision Bridge: PhaseNav stan → drzewo decyzyjne ──
            pn_decisions = evaluate_decisions(state.get("phi", []))
            if pn_decisions:
                pn_triggers = decisions_to_triggers(pn_decisions)
                triggers.extend(pn_triggers)
                # Log decisions
                for d in pn_decisions:
                    skills = d.get("skills", [])
                    print(f"[TRIGGER] 📋 PhaseNav decision: {d['decision']['lp']} "
                          f"{d['decision']['title']} sim={d['similarity']:.3f} "
                          f"skills={len(skills)}", file=sys.stderr)
            # ── /PhaseNav Decision Bridge ──────────────────────────────────

            for t in triggers:
                # Sprawdź cooldown
                tid = t["id"]
                last = last_triggered.get(tid, 0)
                now = time.time()
                # Task queue items: cooldown 600s (10 min)
                # System triggers: cooldown 120-300s
                cooldown = 600 if tid.startswith("task_") else 120
                if now - last < cooldown:
                    continue

                print(f"[TRIGGER] ⚡ {t['id']}: {t['msg']}")
                ok = fire_trigger(t)
                print(f"[TRIGGER]   surface_shift: {'OK' if ok else 'FAIL'}")
                last_triggered[tid] = time.time()

            if any(t["id"].startswith("task_") or t["id"] in ("flow_blocked", "tension_coherence_mismatch") for t in triggers):
                save_last_triggered(last_triggered)

            # Log stan co 30s
            if int(time.time()) % 30 < interval:
                print(f"[TRIGGER] stan: coh={state['coherence']:.3f} "
                      f"tension={state['tension']:.2f} "
                      f"warp={state['warp']:.2f} "
                      f"sem_mass={state['semantic_mass']:.2f} "
                      f"closure={state['closure_score'] or state['attractor_err']:.4f} "
                      f"tick={state['tick']}")

        except Exception as e:
            print(f"[TRIGGER] błąd: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()

        time.sleep(interval)

    print("[TRIGGER] Daemon end")

# ── PID lock — tylko 1 instancja ──────────────────────────────────────

PID_LOCK = Path("/tmp/noema_trigger_daemon.pid")

def acquire_pid_lock() -> bool:
    """Zapobiegaj duplikatom — flock na pliku PID."""
    import fcntl
    try:
        PID_LOCK.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(str(PID_LOCK), os.O_CREAT | os.O_RDWR, 0o644)
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        # Zapisz nasz PID
        os.ftruncate(fd, 0)
        os.write(fd, f"{os.getpid()}\n".encode())
        return True
    except (IOError, OSError):
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_trigger_daemon.py:739 quiet except scope=acquire_pid_lock reason=return False")
        return False

# ── CLI ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    import os
    import fcntl

    # PID lock — tylko jedna instancja
    if not acquire_pid_lock():
        print("[TRIGGER] Inna instancja już działa — exit", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(description="NOEMA Trigger Daemon")
    parser.add_argument("--interval", type=float, default=5.0,
                        help="Poll interval (s)")
    parser.add_argument("--once", action="store_true",
                        help="Single check, no loop")
    args = parser.parse_args()

    if args.once:
        state = analyze_noema()
        last = load_last_triggered()
        now = time.time()
        triggers = analyze_compound_state(state, last)
        # PhaseNav Decision Bridge
        pn_decisions = evaluate_decisions(state.get("phi", []))
        if pn_decisions:
            pn_triggers = decisions_to_triggers(pn_decisions)
            triggers.extend(pn_triggers)
        fired = []
        for t in triggers:
            tid = t["id"]
            cooldown = 600 if tid.startswith("task_") else 120
            if now - last.get(tid, 0) > cooldown:
                ok = fire_trigger(t)
                fired.append({"id": tid, "fired": ok})
                last[tid] = now
        if fired:
            save_last_triggered(last)
        print(json.dumps({"state": state, "triggers": fired}, indent=2))
    else:
        daemon_loop(args.interval)
