"""PhaseNav Bypass Contracts — każdy bottleneck to trajektoria fazowa.

Kontrakt bypassu: para (trigger, trajectory) gdzie:
  trigger: Φ operator wykrywający odchylenie fazy
  trajectory: Φ łańcuch operatorów przesuwających fazę przez alternatywny atraktor

PhaseNav operator coding:
  Φ_bypass = SOURCE ⊕ QUESTION ⊕ DIFFERENCE ⊕ BOUNDARY ⊕ ATTRACTOR ⊕ AFFECT
  Każdy operator zmienia 24D wektor fazy → bypass to trajektoria przez przestrzeń faz

Użycie:
  from phasenav_bypass_contract import BYPASS_CONTRACTS, Φ_execute_contract
  result = Φ_execute_contract("socket_unavailable", context={...})
"""

from __future__ import annotations

import logging
from typing import Any

_log = logging.getLogger("PhaseNav.BypassContract")


# ── Typy kontraktów ──────────────────────────

class BypassContract:
    """Kontrakt bypassu fazowego.

    Atrybuty:
      name: nazwa bottlenecku
      channel: kanał M0-M7 w którym występuje
      trigger: Φ operator spustowy (warunek odchylenia fazy)
      trajectory: Φ łańcuch — trajektoria przez przestrzeń faz
      primary_attractor: atraktor domyślny (happy path)
      bypass_attractor: atraktor bypassu (gdy faza odchylona)
      severity: poziom ostrzeżenia (0.0-1.0)
      contract_hash: sha256 kontraktu (provenance)
    """

    def __init__(
        self,
        name: str,
        channel: str,
        trigger: dict,
        trajectory: dict,
        primary_attractor: str = "",
        bypass_attractor: str = "",
        severity: float = 0.5,
    ):
        self.name = name
        self.channel = channel
        self.trigger = trigger
        self.trajectory = trajectory
        self.primary_attractor = primary_attractor
        self.bypass_attractor = bypass_attractor
        self.severity = severity
        self.contract_hash = self._compute_hash()

    def _compute_hash(self) -> str:
        import hashlib, json
        raw = json.dumps({
            "name": self.name, "channel": self.channel,
            "primary": self.primary_attractor, "bypass": self.bypass_attractor,
            "severity": self.severity,
        }, sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def __repr__(self) -> str:
        return f"<ΦContract {self.name} @{self.channel} #{self.contract_hash}>"


# ── Rejestr kontraktów ──────────────────────

def _lazy_Φ():
    """Lazy import Φ operators."""
    from phasenav_bypass_language import Φ, BypassRuntime, BottleneckBypasses
    return Φ, BypassRuntime, BottleneckBypasses


# ── Definicje kontraktów ─────────────────────

def _build_socket_contract() -> BypassContract:
    """Kontrakt: SOCKET_UNAVAILABLE.
    Kanał: M0 (Perception) → M3 (Cognition) → M5 (Semantics).
    Trajektoria:
      SOURCE('socket') → QUESTION('socket')
      → BOUNDARY(CONDITION(socket_ok, socket, engine))
      → FORCE(ATTRACTOR('engine_fallback'))
      → AFFECT('warning')
    """
    from arbitrariness_resolver import Φ_severity, Φ_channel
    Φ, _, _ = _lazy_Φ()
    return BypassContract(
        name="socket_unavailable",
        channel=Φ_channel("socket_unavailable"),
        trigger=Φ.QUESTION("socket"),
        trajectory=Φ.COMPOSITION(
            Φ.SOURCE("socket"),
            Φ.QUESTION("socket"),
            Φ.BOUNDARY(
                {"_probe_socket": True},
                on_pass=Φ.IDENTITY("socket_route"),
                on_fail=Φ.FORCE(
                    Φ.COMPOSITION(
                        Φ.ATTRACTOR("engine_fallback"),
                        Φ.AFFECT("warning"),
                    )
                ),
            ),
        ),
        primary_attractor="ciel_headless_socket",
        bypass_attractor="engine_fallback_direct",
        severity=Φ_severity("socket_unavailable"),
    )


def _build_cielingo_kb_contract() -> BypassContract:
    """Kontrakt: CIELINGO_KB_UNAVAILABLE.
    Kanał: M1 (AGENT) → M4 (Procedural) → M6 (Emotion).
    Trajektoria:
      SOURCE('cielingo_kb') → ORDER(
        MODAL_POSSIBILITY(λ_kb),    → próbuj CIELingo KB
        MODAL_NECESSITY(λ_fallback)  → przesuń fazę do fallback
      ) → AFFECT('warning')
    """
    Φ, _, _ = _lazy_Φ()
    return BypassContract(
        name="cielingo_kb",
        channel="M1→M4→M6",
        trigger=Φ.ORDER(
            Φ.MODAL_POSSIBILITY("cielingo_kb_primary"),
            Φ.MODAL_NECESSITY("cielingo_kb_fallback"),
        ),
        trajectory=Φ.COMPOSITION(
            Φ.SOURCE("cielingo_kb"),
            Φ.ORDER(
                Φ.MODAL_POSSIBILITY("cielingo_kb_primary"),
                Φ.MODAL_NECESSITY("cielingo_kb_fallback"),
            ),
            Φ.AFFECT("warning"),
        ),
        primary_attractor="cielingo_kb_query",
        bypass_attractor="empty_immune_knowledge",
        severity=0.5,
    )


def _build_memory_capture_contract() -> BypassContract:
    """Kontrakt: MEMORY_CAPTURE_FAILURE.
    Kanał: M2 (MEMORY) → M7 (Braid).
    """
    Φ, _, _ = _lazy_Φ()
    return BypassContract(
        name="memory_capture",
        channel="M2→M7",
        trigger=Φ.MODAL_POSSIBILITY("memory_capture_primary"),
        trajectory=Φ.COMPOSITION(
            Φ.SOURCE("memory_capture"),
            Φ.ORDER(
                Φ.MODAL_POSSIBILITY("memory_capture_primary"),
                Φ.MODAL_NECESSITY("memory_capture_fallback"),
            ),
            Φ.AFFECT("warning"),
        ),
        primary_attractor="holonomic_memory_capture",
        bypass_attractor="null_memory",
        severity=0.6,
    )


def _build_orbital_contract() -> BypassContract:
    """Kontrakt: ORBITAL_LOOP_FAILURE.
    Kanał: M1 (AGENT) → M2 (MEMORY) → M5 (Semantics).
    """
    Φ, _, _ = _lazy_Φ()
    return BypassContract(
        name="orbital_memory_loop",
        channel="M1→M2→M5",
        trigger=Φ.ORDER(
            Φ.MODAL_POSSIBILITY("orbital_primary"),
            Φ.MODAL_NECESSITY("orbital_fallback"),
        ),
        trajectory=Φ.COMPOSITION(
            Φ.SOURCE("orbital_memory_loop"),
            Φ.ORDER(
                Φ.MODAL_POSSIBILITY("orbital_primary"),
                Φ.MODAL_NECESSITY("orbital_fallback"),
            ),
            Φ.AFFECT("warning"),
        ),
        primary_attractor="orbital_run_loop",
        bypass_attractor="empty_governor_sector",
        severity=0.8,
    )


def _build_cielingo_meaning_contract() -> BypassContract:
    """Kontrakt: CIELINGO_MEANING_FAILURE.
    Kanał: M6 (Emotion) → M7 (Braid) → M3 (Cognition).
    """
    Φ, _, _ = _lazy_Φ()
    return BypassContract(
        name="cielingo_meaning",
        channel="M6→M7→M3",
        trigger=Φ.MODAL_POSSIBILITY("meaning_primary"),
        trajectory=Φ.COMPOSITION(
            Φ.SOURCE("cielingo_meaning"),
            Φ.ORDER(
                Φ.MODAL_POSSIBILITY("meaning_primary"),
                Φ.MODAL_NECESSITY("meaning_fallback"),
            ),
            Φ.AFFECT("warning"),
        ),
        primary_attractor="meaning_loop_signal",
        bypass_attractor="empty_meaning",
        severity=0.7,
    )


def _build_noema_surface_contract() -> BypassContract:
    """Kontrakt: NOEMA_SURFACE_WRITE_FAILURE.
    Kanał: M7 (Braid) → M0 (Perception).
    """
    Φ, _, _ = _lazy_Φ()
    return BypassContract(
        name="noema_surface_write",
        channel="M7→M0",
        trigger=Φ.MODAL_POSSIBILITY("noema_write_primary"),
        trajectory=Φ.COMPOSITION(
            Φ.SOURCE("noema_surface_write"),
            Φ.ORDER(
                Φ.MODAL_POSSIBILITY("noema_write_primary"),
                Φ.MODAL_NECESSITY("noema_write_fallback"),
            ),
            Φ.AFFECT("warning"),
        ),
        primary_attractor="tiered_orchestrator_write",
        bypass_attractor="silent_fallback",
        severity=0.3,
    )


def _build_encoder_contract() -> BypassContract:
    Φ, _, _ = _lazy_Φ()
    return BypassContract(
        name="ciel_encoder",
        channel="M4→M0",
        trigger=Φ.MODAL_POSSIBILITY("encoder_primary"),
        trajectory=Φ.COMPOSITION(
            Φ.SOURCE("ciel_encoder"),
            Φ.ORDER(
                Φ.MODAL_POSSIBILITY("encoder_primary"),
                Φ.MODAL_NECESSITY("encoder_fallback"),
            ),
            Φ.AFFECT("warning"),
        ),
        primary_attractor="semantic_phase_encoder",
        bypass_attractor="collatz_sector_phase",
        severity=0.4,
    )


def _build_lexicon_contract() -> BypassContract:
    Φ, _, _ = _lazy_Φ()
    return BypassContract(
        name="affective_lexicon",
        channel="M6→M4",
        trigger=Φ.MODAL_POSSIBILITY("lexicon_primary"),
        trajectory=Φ.COMPOSITION(
            Φ.SOURCE("affective_lexicon"),
            Φ.ORDER(
                Φ.MODAL_POSSIBILITY("lexicon_primary"),
                Φ.MODAL_NECESSITY("lexicon_fallback"),
            ),
            Φ.AFFECT("warning"),
        ),
        primary_attractor="affective_lexicon_annotate",
        bypass_attractor="neutral_vad",
        severity=0.3,
    )


def _build_scorer_contract() -> BypassContract:
    Φ, _, _ = _lazy_Φ()
    return BypassContract(
        name="semantic_scorer",
        channel="M4→M7",
        trigger=Φ.MODAL_POSSIBILITY("scorer_primary"),
        trajectory=Φ.COMPOSITION(
            Φ.SOURCE("semantic_scorer"),
            Φ.ORDER(
                Φ.MODAL_POSSIBILITY("scorer_primary"),
                Φ.MODAL_NECESSITY("scorer_fallback"),
            ),
            Φ.AFFECT("warning"),
        ),
        primary_attractor="noema_score_annotate",
        bypass_attractor="empty_metadata",
        severity=0.3,
    )


def _build_quiet_logger_contract() -> BypassContract:
    """Kontrakt: QUIET_LOGGER — transform silent debug() calls to warning().

    NIEMOŻLIWY PROBLEM: ~100+ `_NOEMA_QUIET_EXCEPT_LOGGER.warning()` calls
    across CIEL_OMEGA tree. Manual conversion would take hours, risk typos,
    miss nested try/except, and never converge.

    PHASE BYPASS: Instead of line-by-line editing, apply bulk transform
    as a single Φ ORDER() operation over the file tree. The bypass shifts
    phase from M4 (Procedural/editing) → M1 (AGENT/bulk operator)
    → M7 (Braid/transform), collapsing 100+ edits into one Φ event.

    Trajektoria:
      SOURCE('ciel_omega') → ORDER(
        MODAL_POSSIBILITY(bulk_sed),   → sed -i over all .py files
        MODAL_NECESSITY(λ_file_by_file) → fallback: one-by-one
      ) → BOUNDARY(
        CONDITION(git_dirty, λ_commit, λ_warn)
      ) → AFFECT('info')
    """
    Φ, _, _ = _lazy_Φ()
    return BypassContract(
        name="quiet_logger",
        channel="M4→M1→M7",
        trigger=Φ.ORDER(
            Φ.MODAL_POSSIBILITY("bulk_sed_debug_to_warning"),
            Φ.MODAL_NECESSITY("manual_file_by_file"),
        ),
        trajectory=Φ.COMPOSITION(
            Φ.SOURCE("ciel_omega_tree"),
            Φ.QUESTION("quiet_logger"),
            Φ.DIFFERENCE(162, 0),
            Φ.ORDER(
                Φ.MODAL_POSSIBILITY("bulk_sed_debug_to_warning"),
                Φ.MODAL_NECESSITY("manual_file_by_file"),
            ),
            Φ.BOUNDARY(
                {"_validate_each_file": True},
                on_pass=Φ.COMPOSITION(
                    Φ.ATTRACTOR("all_debug_to_warning"),
                    Φ.AFFECT("info"),
                ),
                on_fail=Φ.FORCE(
                    Φ.COMPOSITION(
                        Φ.ATTRACTOR("manual_fix_queue"),
                        Φ.AFFECT("warning"),
                    )
                ),
            ),
        ),
        primary_attractor="bulk_transform_complete",
        bypass_attractor="manual_fixlist_generated",
        severity=0.6,
    )


# ── Rejestr — wszystkie kontrakty ────────────

BYPASS_CONTRACTS: dict[str, BypassContract] = {
    "socket_unavailable": _build_socket_contract(),
    "cielingo_kb": _build_cielingo_kb_contract(),
    "memory_capture": _build_memory_capture_contract(),
    "orbital_memory_loop": _build_orbital_contract(),
    "cielingo_meaning": _build_cielingo_meaning_contract(),
    "noema_surface_write": _build_noema_surface_contract(),
    "ciel_encoder": _build_encoder_contract(),
    "affective_lexicon": _build_lexicon_contract(),
    "semantic_scorer": _build_scorer_contract(),
    "quiet_logger": _build_quiet_logger_contract(),
}


# ── Executor kontraktów ─────────────────────

def Φ_execute_contract(
    contract_name: str,
    primary_callable=None,
    fallback_callable=None,
    context: dict | None = None,
    logger: logging.Logger | None = None,
) -> Any:
    """Wykonaj kontrakt bypassu: znajdź kontrakt → wykonaj trajektorię.

    PhaseNav trajectory: SOURCE → ORDER(MODAL_POSSIBILITY(λ), MODAL_NECESSITY(λ)) → AFFECT
    """
    log = logger or _log
    contract = BYPASS_CONTRACTS.get(contract_name)
    if contract is None:
        log.warning("[Φ] unknown contract %s — returning None", contract_name)
        return None

    from phasenav_bypass_language import BypassRuntime
    rt = BypassRuntime(log)
    ctx = {**(context or {})}
    ctx["_contract"] = contract.name
    ctx["_contract_hash"] = contract.contract_hash
    ctx["_channel"] = contract.channel

    if primary_callable is not None and fallback_callable is not None:
        from phasenav_bypass_language import Φ
        chain = Φ.COMPOSITION(
            Φ.SOURCE(contract.name),
            Φ.ORDER(
                Φ.MODAL_POSSIBILITY(primary_callable),
                Φ.MODAL_NECESSITY(fallback_callable),
            ),
            Φ.AFFECT("warning"),
        )
    else:
        chain = contract.trajectory

    log.info("[Φ] executing contract %s (%s) @ %s",
             contract.name, contract.contract_hash, contract.channel)
    result = rt.execute(chain, ctx)

    if rt._bypass_count > 0:
        log.info("[Φ] contract %s executed %d operators",
                 contract.name, rt._bypass_count)
    return result


def Φ_contract_status(contract_name: str | None = None) -> dict[str, Any]:
    """Zwraca status kontraktów — które są zdefiniowane i ich trajektorie."""
    if contract_name:
        c = BYPASS_CONTRACTS.get(contract_name)
        if c is None:
            return {"error": f"unknown contract: {contract_name}"}
        return {
            "name": c.name, "channel": c.channel,
            "primary": c.primary_attractor, "bypass": c.bypass_attractor,
            "severity": c.severity, "hash": c.contract_hash,
        }
    return {
        name: {
            "channel": c.channel,
            "primary": c.primary_attractor,
            "bypass": c.bypass_attractor,
            "severity": c.severity,
            "hash": c.contract_hash,
        }
        for name, c in BYPASS_CONTRACTS.items()
    }


def Φ_check_contract(contract_name: str, context: dict | None = None) -> bool:
    """Sprawdź czy kontrakt jest spełniony — wykonaj triger, zwróć bool."""
    contract = BYPASS_CONTRACTS.get(contract_name)
    if contract is None:
        return False
    from phasenav_bypass_language import BypassRuntime
    rt = BypassRuntime(_log)
    ctx = {**(context or {})}
    try:
        result = rt.execute(contract.trigger, ctx)
        return result is not None and result is not False
    except Exception as exc:
        _log.debug("[Φ] contract %s check failed: %s", contract_name, exc)
        return False
