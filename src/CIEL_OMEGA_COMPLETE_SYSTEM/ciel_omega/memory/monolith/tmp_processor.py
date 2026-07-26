"""CIEL/Ω TMP kernel with runtime policy threshold support."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from memory.monolith.unified_memory import TMPKernel as _BaseTMPKernel


def _clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, float(value)))


class TMPKernel(_BaseTMPKernel):
    """TMP analysis that honours thresholds carried in ``DataVector.D_M``."""

    def second_analysis(self, D, D_TYPE: str, D_ATTR: Dict[str, Any]) -> Dict[str, Any]:
        result = dict(super().second_analysis(D, D_TYPE, D_ATTR))
        metadata = D.D_M if isinstance(D.D_M, dict) else {}
        hold_threshold = _clamp(metadata.get("tmp_hold_threshold", 0.40), 0.0, 1.0)
        pass_threshold = _clamp(metadata.get("tmp_pass_threshold", 0.70), hold_threshold, 1.0)
        result["thresholds"] = {"hold": hold_threshold, "pass": pass_threshold}

        if result.get("verdict") == "REJECT" and "weights" not in result:
            return result

        weights = result.get("weights", {})
        if not weights:
            return result
        score = sum(float(weights.get(key, 0.0)) for key in ("W_L", "W_S", "W_K", "W_E")) / 4.0
        result["score"] = score

        if score < hold_threshold:
            result.update(verdict="REJECT", reason="Below runtime hold threshold.", bifurcation=0)
        elif score < pass_threshold:
            result.update(verdict="HOLD", reason="Below runtime pass threshold.", bifurcation=0)
        else:
            result.update(verdict="PASS", reason="Runtime threshold pass.", bifurcation=1)
        return result


__all__ = ["TMPKernel"]
