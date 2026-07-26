#!/usr/bin/env python3
"""Integrate governed memory and orbital runtime policy into CielEngine."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def replace_once(relative: str, before: str, after: str) -> None:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    if before not in text:
        if after in text:
            return
        raise RuntimeError(f"Unexpected source state in {relative}: {before!r}")
    path.write_text(text.replace(before, after, 1), encoding="utf-8")


def main() -> int:
    replace_once(
        "src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/__init__.py",
        "from .orchestrator import HolonomicMemoryOrchestrator",
        "from .governed_orchestrator import HolonomicMemoryOrchestrator",
    )

    engine = "src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/ciel/engine.py"
    replace_once(
        engine,
        "    from ..memory.orchestrator import HolonomicMemoryOrchestrator",
        "    from ..memory import HolonomicMemoryOrchestrator",
    )
    replace_once(
        engine,
        "    from memory.orchestrator import HolonomicMemoryOrchestrator",
        "    from memory import HolonomicMemoryOrchestrator",
    )
    replace_once(
        engine,
        "    from ..ciel.orbital_memory_loop import OrbitalLoopConfig, RuntimeOrbitalSignals, build_runtime_policy, run_orbital_loop",
        "    from ..ciel.orbital_memory_loop import (\n"
        "        OrbitalLoopConfig,\n"
        "        RuntimeOrbitalSignals,\n"
        "        build_memory_meta,\n"
        "        build_runtime_policy,\n"
        "        run_orbital_loop,\n"
        "    )",
    )
    replace_once(
        engine,
        "    from ciel.orbital_memory_loop import OrbitalLoopConfig, RuntimeOrbitalSignals, build_runtime_policy, run_orbital_loop",
        "    from ciel.orbital_memory_loop import (\n"
        "        OrbitalLoopConfig,\n"
        "        RuntimeOrbitalSignals,\n"
        "        build_memory_meta,\n"
        "        build_runtime_policy,\n"
        "        run_orbital_loop,\n"
        "    )",
    )

    replace_once(
        engine,
        "        D = self.memory.capture(context=context, sense=cleaned)\n"
        "        tmp_out = self.memory.run_tmp(D)\n"
        "        memorised = self.memory.promote_if_bifurcated(D, tmp_out)\n"
        "        braid_runtime = None",
        "        D = self.memory.capture(context=context, sense=cleaned)\n"
        "        tmp_out: Dict[str, Any] = {\"OUT\": {\"verdict\": \"HOLD\", \"bifurcation\": 0}}\n"
        "        memorised = None\n"
        "        braid_runtime = None",
    )

    replace_once(
        engine,
        "        memory_governor: Dict[str, Any] = {}\n"
        "        sector_memory: Dict[str, Any] = {}\n"
        "        try:",
        "        orbital = None\n"
        "        runtime_policy: Dict[str, Any] = {}\n"
        "        memory_meta: Dict[str, Any] = {}\n"
        "        memory_governor: Dict[str, Any] = {}\n"
        "        sector_memory: Dict[str, Any] = {}\n"
        "        try:",
    )
    replace_once(
        engine,
        '                simulation_coherence=float(nonlocal_runtime.get("coherent_fraction", braid_runtime.get("coherence", 0.0))),',
        '                simulation_coherence=float(nonlocal_runtime.get("coherent_fraction", (braid_runtime or {}).get("coherence", 0.0))),',
    )

    replace_once(
        engine,
        "        except Exception:\n"
        "            _NOEMA_QUIET_EXCEPT_LOGGER.exception(\"src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/ciel/engine.py:379 quiet except scope=CielEngine.step reason=no_log_no_raise\")\n"
        "            memory_governor = memory_governor or {}\n"
        "            sector_memory = sector_memory or {}\n\n"
        "        # 11b) CIELingo semantic signal bridge — real scars from engine state",
        "        except Exception:\n"
        "            _NOEMA_QUIET_EXCEPT_LOGGER.exception(\"src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/ciel/engine.py:379 quiet except scope=CielEngine.step reason=no_log_no_raise\")\n"
        "            memory_governor = memory_governor or {}\n"
        "            sector_memory = sector_memory or {}\n\n"
        "        if orbital is not None:\n"
        "            memory_meta = build_memory_meta(\n"
        "                text=cleaned,\n"
        "                context=context,\n"
        "                mood=float(mood),\n"
        "                ethical_score=float(ethical_score),\n"
        "                soul_invariant=float(sigma),\n"
        "                orbital=orbital,\n"
        "                runtime_policy=runtime_policy,\n"
        "            )\n"
        "        else:\n"
        "            memory_meta = {\n"
        "                \"context\": context,\n"
        "                \"orbital_status\": \"degraded\",\n"
        "                \"orbital_control_mode\": runtime_policy.get(\"control_mode\", \"safe\"),\n"
        "                \"durable_write_allowed\": bool(runtime_policy.get(\"durable_write_allowed\", False)),\n"
        "            }\n"
        "        if isinstance(D.D_M, dict):\n"
        "            D.D_M.update(memory_meta)\n"
        "            D.D_M[\"memory_governor\"] = memory_governor\n"
        "        tmp_out = self.memory.run_tmp(D)\n"
        "        memorised = self.memory.promote_if_bifurcated(\n"
        "            D,\n"
        "            tmp_out,\n"
        "            runtime_policy=runtime_policy,\n"
        "        )\n\n"
        "        # 11b) CIELingo semantic signal bridge — real scars from engine state",
    )

    replace_once(
        engine,
        '            "memory_governor": memory_governor,\n'
        '            "sector_memory": sector_memory,\n'
        '            "runtime_policy": runtime_policy if "runtime_policy" in locals() else {},',
        '            "orbital": orbital.to_dict() if orbital is not None else {"status": "degraded"},\n'
        '            "memory_meta": memory_meta,\n'
        '            "memory_governor": memory_governor,\n'
        '            "sector_memory": sector_memory,\n'
        '            "runtime_policy": runtime_policy,',
    )

    print("Omega runtime integration migration applied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
