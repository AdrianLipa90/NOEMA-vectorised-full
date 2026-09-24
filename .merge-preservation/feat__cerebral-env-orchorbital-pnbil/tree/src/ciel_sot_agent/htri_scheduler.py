"""Verified HTRI state access.

The former scheduler mixed resource heuristics, scientific defaults, CPU/GPU
fallbacks, implicit recomputation, and a raw JSON overwrite.  Those behaviors
cannot establish provenance and are intentionally disabled here.  HTRI state
is now read only through the content-addressed publication contract.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from ciel_geometry.htri_computation_contract import (
    summarize_verified_htri_computation,
)
from ciel_geometry.htri_state_contract import summarize_verified_htri_state
from ciel_geometry.paths import P


_STATE_PATH = Path(P.STATE.HTRI_JSON)
_COMPUTATION_PATH = _STATE_PATH.with_name("htri_computation_state.json")
_COMPUTATION_MAX_AGE_SECONDS = 180

# Kept only as an explicit compatibility signal for old imports.  There is no
# verified optimal-thread computation in a runtime-probe publication.
CPU_THREADS: None = None


def run(*args: Any, **kwargs: Any) -> dict[str, Any]:
    """Reject the legacy heuristic scheduler instead of fabricating a result."""
    del args, kwargs
    raise RuntimeError(
        "legacy HTRI scheduler is disabled: publish a verified runtime probe "
        "or implement a separately reviewed computation contract"
    )


def get_state(*, max_age_seconds: float | None = None) -> dict[str, Any]:
    """Read verified state without refresh, recomputation, or fallback values."""
    # A published computation is a distinct observation from the probe.  Once
    # its file exists, verification failure must remain visible; do not hide it
    # by silently falling back to probe-only state.
    if _COMPUTATION_PATH.exists():
        summary = summarize_verified_htri_computation(
            _COMPUTATION_PATH,
            max_age_seconds=(
                _COMPUTATION_MAX_AGE_SECONDS
                if max_age_seconds is None
                else max_age_seconds
            ),
        )
    else:
        summary = summarize_verified_htri_state(
            _STATE_PATH, max_age_seconds=max_age_seconds
        )
    metrics = summary["metrics"]
    runtime = summary["runtime_capability"]
    computation = summary["computation"]
    observation = summary["observation"]
    return {
        "schema": summary["schema"],
        "status": summary["status"],
        "coherence": metrics["coherence"]["value"],
        "soul_invariant": metrics["soul_invariant"]["value"],
        "spectral_radius": metrics["spectral_radius"]["value"],
        "potential": metrics["potential"]["value"],
        "n_oscillators": metrics["oscillator_count"]["value"],
        "n_threads_optimal": metrics["optimal_thread_count"]["value"],
        "power_mode": None,
        "substrate": computation["active_backend"],
        "timestamp": observation["observed_at"],
        "runtime_capability": runtime,
        "computation": computation,
        "metrics": metrics,
        "observation": observation,
        "publication": summary["publication"],
        "inference_used": False,
        "fallback_used": False,
    }


def _unavailable_state(error_type: str) -> dict[str, Any]:
    metrics = {
        name: {
            "value": None,
            "unit": None,
            "definition": None,
            "status": "unavailable",
            "source_pointer": None,
        }
        for name in (
            "coherence",
            "soul_invariant",
            "spectral_radius",
            "potential",
            "oscillator_count",
            "optimal_thread_count",
        )
    }
    return {
        "schema": "noema.htri.consumer-state/v1",
        "status": "unavailable",
        "coherence": None,
        "soul_invariant": None,
        "spectral_radius": None,
        "potential": None,
        "n_oscillators": None,
        "n_threads_optimal": None,
        "power_mode": None,
        "substrate": None,
        "timestamp": None,
        "runtime_capability": None,
        "computation": {
            "status": "unavailable",
            "active": None,
            "active_backend": None,
            "started_at": None,
            "completed_at": None,
            "source": None,
        },
        "metrics": metrics,
        "observation": None,
        "publication": {
            "status": "unavailable",
            "error_code": "verified_htri_state_unavailable",
            "error_type": error_type,
            "freshness_status": "unavailable",
            "stale": None,
        },
        "inference_used": False,
        "fallback_used": False,
    }


def get_state_status(*, max_age_seconds: float | None = None) -> dict[str, Any]:
    """Return verified state or a null-only unavailable projection."""
    try:
        return get_state(max_age_seconds=max_age_seconds)
    except (KeyError, OSError, TypeError, ValueError) as exc:
        return _unavailable_state(type(exc).__name__)


def get_optimal_threads(*, max_age_seconds: float | None = None) -> int:
    """Return only a verified integer thread metric; never select a default."""
    value = get_state(max_age_seconds=max_age_seconds)["n_threads_optimal"]
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise RuntimeError("verified HTRI optimal_thread_count is unavailable")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Read verified HTRI state")
    parser.add_argument(
        "--max-age-seconds",
        type=float,
        default=None,
        help="explicit caller freshness policy; omitted means not evaluated",
    )
    args = parser.parse_args()
    print(
        json.dumps(
            get_state(max_age_seconds=args.max_age_seconds),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["get_optimal_threads", "get_state", "get_state_status", "run"]
