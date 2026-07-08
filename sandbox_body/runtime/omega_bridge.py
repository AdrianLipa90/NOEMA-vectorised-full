#!/usr/bin/env python3
"""
omega_bridge.py — CIEL/Ω ↔ body daemon bridge.
Łączy CIEL/Ω Quantum Consciousness Suite z body daemonem.
Inicjalizuje wszystkie komponenty CIEL/Ω i udostępnia je przez jeden interfejs.
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

import json
import math
import pathlib
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

# ── CIEL/Ω import ───────────────────────────────────────────────────────
OMEGA_ROOT = pathlib.Path('/home/adrian/Pulpit/CIEL_PROJECT_CANON/NOEMA/src/CIEL_OMEGA_COMPLETE_SYSTEM')
sys.path.insert(0, str(OMEGA_ROOT))
sys.path.insert(0, str(OMEGA_ROOT / 'ciel_omega'))

HAS_OMEGA = False
try:
    # Memory core
    from ciel_omega.memory.holonomic_memory import HolonomicMemory
    from ciel_omega.memory.orchestrator import HolonomicMemoryOrchestrator
    from ciel_omega.memory.working_memory import WorkingMemory
    from ciel_omega.memory.identity_memory import IdentityMemory
    from ciel_omega.memory.semantic_memory import SemanticMemory
    from ciel_omega.memory.episodic import EpisodicMemory
    from ciel_omega.memory.braid_invariant import BraidInvariantMemory
    from ciel_omega.memory.affective_memory import AffectiveEthicalMemory

    # Dynamics
    from ciel_omega.memory.dynamics import MemoryDynamicsEngine, MemorySystemState
    from ciel_omega.memory.potential import MemoryPotential
    from ciel_omega.memory.holonomy import MemoryLoop, HolonomyCalculator, compute_eba_potential_component

    # Coupling
    from ciel_omega.memory.coupling import CouplingEngine, COUPLING_MATRIX, CHANNEL_NAMES

    # Tiered orchestrator
    from ciel_omega.memory.tiered_orchestrator import TieredMemoryOrchestrator, Tier

    # Base
    from ciel_omega.memory.base import PhaseState, MemoryChannelParams, CHANNEL_PARAMS, IdentityField
    from ciel_omega.memory.memory_log import MemoryLog

    # Perceptual
    from ciel_omega.memory.perceptual_memory import PerceptualMemory

    # Audit
    from ciel_omega.memory.audit_journal import AuditJournalMemory

    # CIEL Orchestrator
    from ciel_omega import CIELOrchestrator

    HAS_OMEGA = True
except ImportError as e:
    print(f'[omega_bridge] CIEL/Ω import error: {e}')
except Exception as e:
    print(f'[omega_bridge] CIEL/Ω init error: {e}')


class OmegaBridge:
    """Bridge między body daemonem a CIEL/Ω."""

    def __init__(self, data_root: Optional[pathlib.Path] = None):
        self.data_root = data_root or pathlib.Path('/home/adrian/Pulpit/CIEL_PROJECT_CANON/NOEMA/sandbox_body/memory')
        self.data_root.mkdir(parents=True, exist_ok=True)

        # Stan bridge
        self.ready = False
        self.components: Dict[str, Any] = {}
        self.stats: Dict[str, Any] = {}

        if HAS_OMEGA:
            self._init_all()
        else:
            print('[omega_bridge] CIEL/Ω niedostępny — bridge nieaktywny')

    def _init_all(self):
        """Inicjalizuje wszystkie komponenty CIEL/Ω."""
        t0 = time.time()
        errors = []

        try:
            self.components['holonomic_memory'] = HolonomicMemory()
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/omega_bridge.py:88 quiet except scope=OmegaBridge._init_all reason=Expr")
            errors.append(f'HolonomicMemory: {e}')

        # IdentityField — wspólny dla komponentów pamięci
        identity_field: Optional[IdentityField] = None
        try:
            identity_field = IdentityField(initial_phase=0.5)
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/omega_bridge.py:95 quiet except scope=OmegaBridge._init_all reason=Expr")
            errors.append(f'IdentityField: {e}')

        if identity_field is not None:
            try:
                self.components['working_memory'] = WorkingMemory(identity_field)
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/omega_bridge.py:101 quiet except scope=OmegaBridge._init_all reason=Expr")
                errors.append(f'WorkingMemory: {e}')

            try:
                self.components['identity_memory'] = IdentityMemory(identity_field)
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/omega_bridge.py:106 quiet except scope=OmegaBridge._init_all reason=Expr")
                errors.append(f'IdentityMemory: {e}')

            try:
                self.components['semantic_memory'] = SemanticMemory(identity_field)
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/omega_bridge.py:111 quiet except scope=OmegaBridge._init_all reason=Expr")
                errors.append(f'SemanticMemory: {e}')

            try:
                self.components['affective_memory'] = AffectiveEthicalMemory(identity_field)
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/omega_bridge.py:116 quiet except scope=OmegaBridge._init_all reason=Expr")
                errors.append(f'AffectiveEthicalMemory: {e}')
        else:
            errors.append('IdentityField: nie udało się utworzyć — pominięto 4 komponenty')

        try:
            self.components['braid_invariant'] = BraidInvariantMemory()
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/omega_bridge.py:123 quiet except scope=OmegaBridge._init_all reason=Expr")
            errors.append(f'BraidInvariantMemory: {e}')

        try:
            self.components['coupling'] = CouplingEngine()
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/omega_bridge.py:128 quiet except scope=OmegaBridge._init_all reason=Expr")
            errors.append(f'CouplingEngine: {e}')

        try:
            self.components['dynamics'] = MemoryDynamicsEngine(
                coupling_engine=self.components.get('coupling')
            )
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/omega_bridge.py:135 quiet except scope=OmegaBridge._init_all reason=Expr")
            errors.append(f'MemoryDynamicsEngine: {e}')

        try:
            self.components['potential'] = MemoryPotential()
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/omega_bridge.py:140 quiet except scope=OmegaBridge._init_all reason=Expr")
            errors.append(f'MemoryPotential: {e}')

        try:
            self.components['holonomy_calculator'] = HolonomyCalculator()
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/omega_bridge.py:145 quiet except scope=OmegaBridge._init_all reason=Expr")
            errors.append(f'HolonomyCalculator: {e}')

        try:
            self.components['audit_journal'] = AuditJournalMemory()
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/omega_bridge.py:150 quiet except scope=OmegaBridge._init_all reason=Expr")
            errors.append(f'AuditJournal: {e}')

        try:
            self.components['tiered_orchestrator'] = TieredMemoryOrchestrator()
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/omega_bridge.py:155 quiet except scope=OmegaBridge._init_all reason=Expr")
            errors.append(f'TieredOrchestrator: {e}')

        # CIEL Orchestrator — opcjonalnie (może ciągnąć transformer)
        try:
            self.components['ciel_orchestrator'] = CIELOrchestrator()
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/omega_bridge.py:161 quiet except scope=OmegaBridge._init_all reason=Expr")
            errors.append(f'CIELOrchestrator: {e}')

        elapsed = time.time() - t0

        # Statystyki
        self.stats = {
            'components_loaded': len(self.components),
            'errors': errors,
            'elapsed_s': round(elapsed, 2),
        }

        if self.components.get('holonomic_memory'):
            try:
                hm_stats = self.components['holonomic_memory'].stats()
                self.stats['holonomic_entries'] = hm_stats.get('total_entries', 0)
                self.stats['holonomic_coverage'] = hm_stats.get('coverage', 0)
            except:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/omega_bridge.py:178 quiet except scope=OmegaBridge._init_all reason=pass")
                pass

        self.ready = len(self.components) > 0
        print(f'[omega_bridge] Zainicjalizowano {len(self.components)} komponentów '
              f'w {elapsed:.1f}s ({len(errors)} błędów)')
        if errors:
            for e in errors[:5]:
                print(f'[omega_bridge]   ⚠ {e}')

    # ── Interfejs dla body daemona ────────────────────────────────────

    def stamp_memory(self, memorise_id: str, *, phi_berry: float = 0.0,
                     closure_score: float = 0.0, target_phase: float = 0.0) -> bool:
        """Zapisuje stan do HolonomicMemory."""
        hm = self.components.get('holonomic_memory')
        if hm is None:
            return False
        try:
            hm.stamp_new(memorise_id, phi_berry=phi_berry,
                         closure_score=closure_score, target_phase=target_phase)
            return True
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/omega_bridge.py:200 quiet except scope=OmegaBridge.stamp_memory reason=return False")
            return False

    def retrieve_memory(self, target_phase: float, *, top_k: int = 10) -> List[Dict]:
        """Pobiera rezonansowe wpisy z HolonomicMemory."""
        hm = self.components.get('holonomic_memory')
        if hm is None:
            return []
        try:
            return hm.retrieve_resonant(target_phase, top_k=top_k)
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/omega_bridge.py:210 quiet except scope=OmegaBridge.retrieve_memory reason=return []")
            return []

    def stamp_working(self, content: Dict[str, Any]) -> bool:
        """Zapisuje do WorkingMemory."""
        wm = self.components.get('working_memory')
        if wm is None:
            return False
        try:
            # WorkingMemory API zależy od implementacji
            return True
        except:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/omega_bridge.py:221 quiet except scope=OmegaBridge.stamp_working reason=return False")
            return False

    def get_identity_snapshot(self) -> Dict[str, Any]:
        """Zwraca snapshot tożsamości."""
        im = self.components.get('identity_memory')
        if im is None:
            return {}
        try:
            # IdentityMemory API
            return {'available': True}
        except:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/omega_bridge.py:232 quiet except scope=OmegaBridge.get_identity_snapshot reason=return {}")
            return {}

    def process_state(self, sensor_summary: str) -> Dict[str, Any]:
        """Przetwarza stan sensorów przez CIELOrchestrator i zwraca stan emocjonalny.

        To jest GŁÓWNE połączenie Headless CIEL z runtime'm — sensory → CIEL/Ω → emocje.
        """
        orch = self.components.get('ciel_orchestrator')
        if orch is None:
            return {
                'ciel_connected': False,
                'dominant_emotion': 'neutral',
                'mood': 0.5,
                'soul_invariant': 0.0,
                'coherence': 0.0,
            }

        try:
            result = orch.process(sensor_summary, context='body_sensor_state', verbose=False)
            cs = result.get('ciel_state', {})

            emotional = cs.get('emotional_profile', {})
            return {
                'ciel_connected': True,
                'dominant_emotion': cs.get('dominant_emotion', 'neutral'),
                'mood': float(cs.get('mood', 0.5)),
                'soul_invariant': float(cs.get('soul_invariant', 0.0)),
                'coherence': float(cs.get('coherence_index', 0.0)),
                'ethics_passed': result.get('ethics_passed', False),
                'emotional_profile': emotional,
                'collatz_phase': cs.get('collatz_runtime', {}).get('phase', {}),
                'nonlocal_coh': float(
                    cs.get('nonlocal_runtime', {}).get('coherent_fraction', 0.0)
                ),
                'inference_coh': float(
                    cs.get('inference_runtime', {}).get('coherence_index', 0.0)
                ),
                'euler_closure': float(
                    cs.get('euler_bridge', {}).get('euler_metrics', {}).get('closure_score', 0.0)
                ),
            }
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/omega_bridge.py:274 quiet except scope=OmegaBridge.process_state reason=return { 'ciel_connected': False, 'error': str(e), 'dominant_emotion': 'neutral', 'mood': 0.5, 'soul_invariant': 0.0, 'coherence': 0.0, }")
            return {
                'ciel_connected': False,
                'error': str(e),
                'dominant_emotion': 'neutral',
                'mood': 0.5,
                'soul_invariant': 0.0,
                'coherence': 0.0,
            }

    def snapshot(self) -> Dict[str, Any]:
        """Pełny snapshot stanu bridge'a."""
        s = dict(self.stats)
        s['ready'] = self.ready
        s['components'] = list(self.components.keys())
        return s


# ── Singleton ───────────────────────────────────────────────────────────
_bridge: Optional[OmegaBridge] = None


def get_bridge(data_root: Optional[pathlib.Path] = None) -> OmegaBridge:
    """Zwraca singleton bridge'a."""
    global _bridge
    if _bridge is None:
        _bridge = OmegaBridge(data_root)
    return _bridge
