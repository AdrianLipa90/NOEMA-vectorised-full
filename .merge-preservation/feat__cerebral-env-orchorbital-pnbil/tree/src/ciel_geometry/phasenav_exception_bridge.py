"""PhaseNav exception bridge — represent failures as PhaseNav operator
vectors instead of bare Python log strings, then propagate.

Origin (2026-07-11): Adrian's standing rule is absolute — no quiet-except
anywhere in NOEMA, ever (see OPEN_ISSUES id
"quiet-except-pattern-banned-systemwide" in scripts/noema_repair_cycle.py).
Separately, Adrian gave explicit permission to build real PhaseNav-native
infrastructure rather than keep writing bare Python around this: "MASZ
POZWOLENIE NA NAPISANIE JĘZYKA KODOWANIA WEKTOROWEGO NA BAZIE PHASENAV."

This is an honest, bounded first piece of that, not a claim that PhaseNav
can replace Python's control flow (verified directly this session: no
execution engine exists anywhere in this repo for that — see
docs/... conversation record). What IS honestly buildable: the
REPRESENTATION and SIGNALLING of a failure uses PhaseNav's own,
already-existing 36-operator vocabulary (operator_algebra.py's
ALL_OPERATOR_IDS — REFUSAL, PAUSE, CANON_BLOCK, RISK, BOUNDARY are all
real, pre-existing operators, not invented for this) and 36D phase-vector
encoding (fast_encode_text), instead of a bare log string. The `raise`
itself stays in Python because that is what actually executes on this
hardware — no deception about that.

Every call site converts:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception(msg); <silently continue>
into:
    phase_signal_exception(scope, exc, operator_id=...); raise
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

import json
import time
import traceback
from pathlib import Path

import numpy as np

_SIGNAL_LOG = Path("/media/adrian/New Volume/CIEL_memories/state/phasenav_exception_signals.jsonl")


def phase_signal_exception(
    scope: str,
    exc: BaseException,
    *,
    operator_id: str = "REFUSAL",
) -> np.ndarray:
    """Encode a failure as a PhaseNav operator-tagged 36D vector, append it
    to the exception-signal log (native format: phi + operator + scope +
    traceback text, not a bare log line), and return the vector.

    Does NOT swallow or suppress anything — this is the SIGNAL step only.
    Callers MUST still `raise` immediately after calling this (this
    function does not raise itself, so it composes cleanly with an
    existing `except` clause's own re-raise).

    operator_id: one of operator_algebra.ALL_OPERATOR_IDS. Default REFUSAL
    (the operator NOEMA already uses for "this cannot proceed as
    requested" per its own semantic dictionary) — pass e.g. "PAUSE" for a
    recoverable/retryable condition, "CANON_BLOCK" for a policy-level
    rejection, "RISK" for a degraded-but-continuing condition.
    """
    from ciel_geometry.phasenav.operator_algebra import operator_signature
    from ciel_geometry.cielingo_phase_encoder import fast_encode_text

    tb_text = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    error_text = f"{scope}: {type(exc).__name__}: {exc}"

    # Blend the operator's canonical signature with the actual error
    # content's own phase encoding — same blend pattern used throughout
    # this codebase (e.g. apply_operator() in cielingo_inference.py),
    # not a new mechanism.
    op_vec = operator_signature(operator_id)
    content_vec = fast_encode_text(error_text)
    signal_phi = np.angle(0.5 * np.exp(1j * op_vec) + 0.5 * np.exp(1j * content_vec)) % (2 * np.pi)

    record = {
        "ts": time.time(),
        "scope": scope,
        "operator": operator_id,
        "exception_type": type(exc).__name__,
        "exception_message": str(exc),
        "phi": [round(float(x), 6) for x in signal_phi],
        "traceback": tb_text,
    }
    _SIGNAL_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(_SIGNAL_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return signal_phi
