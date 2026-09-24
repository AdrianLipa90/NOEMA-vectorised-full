"""Canonical unified surface for the merged CIEL/Ω system.

This module binds the canonical Omega surfaces into one minimal composite object:
    CIELOrchestrator + CIELClient + MemoryCorePhaseBridge
It supports both package-style imports and direct local script execution.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional
import json
import sys

from bootstrap_runtime import ensure_runtime_paths

_THIS_DIR = ensure_runtime_paths(__file__)

try:
    from ciel_omega.bridge.memory_core_phase_bridge import MemoryCorePhaseBridge  # type: ignore
    from ciel_omega.ciel_client import CIELClient  # type: ignore
    from ciel_omega.ciel_orchestrator import CIELOrchestrator  # type: ignore
except Exception:
    _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/unified_system.py:23 quiet except scope=<module> reason=no_log_no_raise")
    from bridge.memory_core_phase_bridge import MemoryCorePhaseBridge
    from ciel_client import CIELClient
    from ciel_orchestrator import CIELOrchestrator


def _build_braid_nonlocal_coupling(ciel_state: Dict[str, Any]) -> Dict[str, Any]:
    """Build braid_nonlocal_coupling payload from ciel_state nonlocal_runtime."""
    nr = ciel_state.get('nonlocal_runtime', {})
    loops = nr.get('loops', {})
    cards = [
        {'loop_type': k, 'phi_ab': v.get('phi_ab', 0.0),
         'phi_berry': v.get('phi_berry', 0.0), 'is_coherent': v.get('is_coherent', False),
         'defect': v.get('defect_magnitude', 0.0)}
        for k, v in loops.items()
    ]
    defects = [v.get('defect_magnitude', 0.0) for v in loops.values()]
    braid_weighted_closure = 1.0 - (sum(defects) / len(defects)) if defects else 0.0
    # Inject braid_weighted_closure into euler_bridge euler_metrics if present
    eb = ciel_state.get('euler_bridge', {})
    if eb and 'euler_metrics' in eb:
        eb['euler_metrics']['braid_weighted_closure'] = braid_weighted_closure
    return {
        'cards': cards,
        'braid_weighted_closure': braid_weighted_closure,
        'coherent_fraction': nr.get('coherent_fraction', 0.0),
        'phi_ab_mean': nr.get('phi_ab_mean', 0.0),
        'phi_berry_mean': nr.get('phi_berry_mean', 0.0),
    }


@dataclass
class UnifiedSystem:
    orchestrator: CIELOrchestrator
    client: CIELClient
    bridge: MemoryCorePhaseBridge

    @classmethod
    def create(
        cls,
        config: Optional[Dict[str, Any]] = None,
        *,
        identity_phase: float = 0.0,
        grid_size: int = 24,
        model_path: Optional[str] = None,
        boot: bool = True,
    ) -> "UnifiedSystem":
        orchestrator = CIELOrchestrator(config=config or {}, boot=boot)
        client = CIELClient(model_path=model_path, boot=False)
        client.orchestrator = orchestrator
        bridge = MemoryCorePhaseBridge(identity_phase=identity_phase, grid_size=grid_size)
        return cls(orchestrator=orchestrator, client=client, bridge=bridge)

    def shutdown(self) -> None:
        self.client.shutdown()

    def handshake(self) -> Dict[str, Any]:
        data = self.client.handshake()
        data['surface'] = 'UnifiedSystem'
        return data

    def status(self) -> Dict[str, Any]:
        snap = self.orchestrator.status_snapshot()
        snap['surface'] = 'UnifiedSystem'
        snap['client_surface'] = 'CIELClient'
        snap['client_status'] = self.client.status()
        return snap

    def process(self, text: str, *, use_llm: bool = False) -> Dict[str, Any]:
        result = self.client.process(text, use_llm=use_llm)
        result['surface'] = 'UnifiedSystem'
        return result

    def run_text_cycle(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None,
        *,
        use_llm: bool = False,
    ) -> Dict[str, Any]:
        cycle = self.bridge.step(text, metadata=metadata or {})
        process_result = self.client.process(text, use_llm=use_llm)
        ciel_state = process_result.get('ciel_state', {})
        return {
            'surface': 'UnifiedSystem',
            'input_text': cycle.input_text,
            'memory_semantic_key': cycle.memory_semantic_key,
            'memory_cycle_index': cycle.memory_cycle_index,
            'core_metrics': cycle.core_metrics,
            'vocabulary_metrics': cycle.vocabulary_metrics,
            'euler_metrics': cycle.euler_metrics,
            'orchestrator_status': process_result.get('status', 'unknown'),
            'dominant_emotion': ciel_state.get('dominant_emotion', '?'),
            'soul_measure': process_result.get('soul_measure', 0.0),
            'ethics_passed': process_result.get('ethics_passed', False),
            'collatz_runtime': ciel_state.get('collatz_runtime', {}),
            'nonlocal_runtime': ciel_state.get('nonlocal_runtime', {}),
            'engine_euler_bridge': ciel_state.get('euler_bridge', {}),
            'llm_response': process_result.get('llm_response'),
            'llm_overlay': process_result.get('llm_overlay'),
            'braid_nonlocal_coupling': _build_braid_nonlocal_coupling(ciel_state),
        }

    def communicate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        action = str(payload.get('action', 'status')).strip().lower()
        if action == 'handshake':
            return self.handshake()
        if action == 'status':
            return self.status()
        if action == 'process':
            return self.process(str(payload.get('text', '')), use_llm=bool(payload.get('use_llm', False)))
        if action == 'cycle':
            return self.run_text_cycle(
                str(payload.get('text', '')),
                metadata=payload.get('metadata'),
                use_llm=bool(payload.get('use_llm', False)),
            )
        return {'status': 'error', 'error': f'unsupported action: {action}', 'surface': 'UnifiedSystem'}


def main(argv: Optional[list[str]] = None) -> int:
    import argparse

    p = argparse.ArgumentParser(description='CIEL/Ω unified system surface')
    p.add_argument('--mode', choices=['handshake', 'status', 'process', 'cycle', 'json'], default='status')
    p.add_argument('--text', type=str, help='Text for process/cycle modes')
    p.add_argument('--json-payload', type=str, help='JSON payload for json mode')
    p.add_argument('--model-path', type=str, help='Optional GGUF model path for the client overlay')
    p.add_argument('--use-llm', action='store_true', help='Enable GGUF overlay generation when a model is available')
    args = p.parse_args(argv)

    system = UnifiedSystem.create(model_path=args.model_path)
    try:
        if args.mode == 'handshake':
            print(json.dumps(system.handshake(), ensure_ascii=False, indent=2))
            return 0
        if args.mode == 'status':
            print(json.dumps(system.status(), ensure_ascii=False, indent=2))
            return 0
        if args.mode == 'process':
            if not args.text:
                p.error('--text is required in process mode')
            print(json.dumps(system.process(args.text, use_llm=args.use_llm), ensure_ascii=False, indent=2))
            return 0
        if args.mode == 'cycle':
            if not args.text:
                p.error('--text is required in cycle mode')
            print(json.dumps(system.run_text_cycle(args.text, use_llm=args.use_llm), ensure_ascii=False, indent=2))
            return 0
        if not args.json_payload:
            p.error('--json-payload is required in json mode')
        print(json.dumps(system.communicate(json.loads(args.json_payload)), ensure_ascii=False, indent=2))
        return 0
    finally:
        system.shutdown()


if __name__ == '__main__':
    raise SystemExit(main())
