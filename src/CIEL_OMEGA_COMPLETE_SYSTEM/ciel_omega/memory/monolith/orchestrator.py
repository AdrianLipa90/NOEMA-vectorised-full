"""CIEL/Ω unified memory orchestrator with runtime write policy."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from memory.monolith.tmp_processor import TMPKernel
from memory.monolith.unified_memory import UnifiedMemoryOrchestrator as _BaseOrchestrator


class UnifiedMemoryOrchestrator(_BaseOrchestrator):
    """Public orchestrator that enforces TMP and durable-write runtime policy."""

    def __init__(
        self,
        cfg_dir: Path = _BaseOrchestrator.__init__.__defaults__[0],
        tsm_db: Path = _BaseOrchestrator.__init__.__defaults__[1],
        wpm_h5: Path = _BaseOrchestrator.__init__.__defaults__[2],
        braid_ledger: Path = _BaseOrchestrator.__init__.__defaults__[3],
    ):
        super().__init__(cfg_dir=cfg_dir, tsm_db=tsm_db, wpm_h5=wpm_h5, braid_ledger=braid_ledger)
        self.tmp = TMPKernel(cfg_dir)

    def promote_if_bifurcated(
        self,
        D,
        tmp_out: Dict[str, Any],
        wave_arrays: Optional[Dict[str, Any]] = None,
        wave_attrs: Optional[Dict[str, Any]] = None,
        runtime_policy: Dict[str, Any] | None = None,
    ):
        policy = runtime_policy or {}
        if policy.get("durable_write_allowed") is False:
            return None
        if policy.get("require_trusted_source_for_promotion") and not bool(
            isinstance(D.D_M, dict) and D.D_M.get("trusted_source")
        ):
            return None
        return super().promote_if_bifurcated(
            D,
            tmp_out,
            wave_arrays=wave_arrays,
            wave_attrs=wave_attrs,
        )


__all__ = ["UnifiedMemoryOrchestrator"]
