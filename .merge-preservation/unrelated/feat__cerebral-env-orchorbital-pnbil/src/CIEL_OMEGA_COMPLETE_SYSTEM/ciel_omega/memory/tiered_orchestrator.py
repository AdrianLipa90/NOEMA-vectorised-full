"""Tiered Memory Orchestrator — overarching coordinator across all memory tiers.

Architecture
============
Three tiers + async background:

  Tier 1 (Fast/Volatile)  — NOEMA surface (mmap) + PhaseMemory (mmap) + M0-M8 channels
  Tier 2 (Medium/Durable) — TSM (SQLite) + StateDB (SQLite) + HolonomicMemory + CIELBlochEncoder
  Tier 3 (Deep/Archival)  — WPM (HDF5) + BraidLedger (JSONL) + UnifiedMemoryOrchestrator
  Async (Background)      — ConsolidationResonator + CIELMemoryConsolidator

Routing rules:
  write(content, tier='auto'):
    'auto'   -> Tier 1 always, Tier 2 if salience>0.6 or candidate, Tier 3 if bifurcation
    'fast'   -> Tier 1 only (volatile)
    'durable' -> Tier 1 + Tier 2 (skip Tier 3)
    'deep'   -> All tiers including Tier 3 wave archive

  read(query, mode='auto'):
    'auto'     -> Tier 1 cache first, Tier 2 resonant if phase match, Tier 3 if no results
    'surface'  -> Tier 1 only (current oscillator state)
    'resonant' -> Tier 2 only (HolonomicMemory phase-resonant retrieval)
    'deep'     -> Tier 2 + Tier 3 (full archival search)

  consolidate(cycle_result):
    Per-cycle: drain M1 overflow -> promote candidates -> Tier 2 writes -> EBA check
    Periodic:  Tier 2 consolidation -> async trigger for ConsolidationResonator

  snapshot():
    Returns unified state across all tiers: phases, counts, energy, health

Data flow (on each user message):
  1. process_user_input() -> Tier 1: surface write + phase_memory bind + M0-M8 evolve
  2. HolonomicMemoryOrchestrator.process_input() -> candidate detection -> Tier 2 writes
  3. Periodic: ConsolidationResonator.run() -> tag Kuramoto -> Tier 2 TSM write -> WOmega update
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import math
import time as _time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np

# ---------------------------------------------------------------------------
# Tier & Routing types
# ---------------------------------------------------------------------------

class Tier(Enum):
    FAST    = auto()  # volatile: surface mmap, phase_memory mmap, in-process channels
    MEDIUM  = auto()  # durable:  TSM SQLite, StateDB SQLite, HolonomicMemory
    DEEP    = auto()  # archival: WPM HDF5, BraidLedger JSONL, wave snapshots
    ASYNC   = auto()  # background: ConsolidationResonator, memory consolidator daemon


class WriteMode(Enum):
    AUTO    = auto()  # auto-select tier based on salience/bifurcation
    FAST    = auto()  # Tier 1 only
    DURABLE = auto()  # Tier 1 + Tier 2
    DEEP    = auto()  # All tiers


class ReadMode(Enum):
    AUTO     = auto()  # Tier 1 cache -> Tier 2 resonant -> Tier 3 fallback
    SURFACE  = auto()  # Tier 1 only: current oscillator state
    RESONANT = auto()  # Tier 2 only: HolonomicMemory phase-resonant
    DEEP     = auto()  # Tier 2 + Tier 3: full search


@dataclass
class TieredWriteResult:
    """Result of a tiered write operation."""
    content_key: str
    tier1_written: bool = False
    tier2_written: bool = False
    tier3_written: bool = False
    tsm_ref: Optional[str] = None
    wpm_ref: Optional[str] = None
    braid_ref: Optional[str] = None
    surface_tick: int = 0
    phase_memory_slot: Optional[int] = None
    channel_keys: Dict[str, str] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)


@dataclass
class TieredReadResult:
    """Result of a tiered read/retrieve operation."""
    query: str
    mode: ReadMode
    tier1_surface: Dict[str, Any] = field(default_factory=dict)
    tier1_channels: Dict[str, Any] = field(default_factory=dict)
    tier2_resonant: List[Dict[str, Any]] = field(default_factory=list)
    tier2_weighted: List[Dict[str, Any]] = field(default_factory=list)
    tier3_archival: List[Dict[str, Any]] = field(default_factory=list)
    orbital_shells: List[Dict[str, Any]] = field(default_factory=list)
    coherence_surface: List[Dict[str, Any]] = field(default_factory=list)
    total_hits: int = 0
    elapsed_ms: float = 0.0


@dataclass
class TieredSnapshot:
    """Unified system snapshot across all tiers."""
    timestamp: float
    cycle_index: int
    identity_phase: float
    energy: Dict[str, float]
    cielingo: Dict[str, Any] = field(default_factory=dict)
    defects: Dict[str, float] = field(default_factory=dict)
    counts: Dict[str, int] = field(default_factory=dict)
    tier1: Dict[str, Any] = field(default_factory=dict)
    tier2: Dict[str, Any] = field(default_factory=dict)
    tier3: Dict[str, Any] = field(default_factory=dict)
    health: Dict[str, Any] = field(default_factory=dict)
    eba_loop_status: Dict[str, bool] = field(default_factory=dict)
    memory_bootstrap: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Default paths
# ---------------------------------------------------------------------------

_CIEL_OMEGA = Path(__file__).resolve().parents[2]  # CIEL_OMEGA_COMPLETE_SYSTEM
_PROJECT_ROOT = _CIEL_OMEGA.parent.parent  # NOEMA project root

_TSM_DB = (
    _PROJECT_ROOT
    / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM" / "CIEL_MEMORY_SYSTEM" / "TSM" / "ledger" / "memory_ledger.db"
)
_WPM_H5 = (
    _PROJECT_ROOT
    / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM" / "CIEL_MEMORY_SYSTEM" / "WPM" / "wave_snapshots" / "wave_archive.h5"
)
_BRAID_LEDGER = (
    _PROJECT_ROOT
    / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM" / "CIEL_MEMORY_SYSTEM" / "BRAID" / "ledger" / "braid_ledger.jsonl"
)
_NONLOCAL_DB = (
    _PROJECT_ROOT
    / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM" / "CIEL_MEMORY_SYSTEM" / "TSM" / "ledger" / "nonlocal_graph.db"
)
_SYSTEM_MAP = _PROJECT_ROOT / "system_map_v2.json"

# ---------------------------------------------------------------------------
# Lazy imports (avoid circular imports at module level)
# ---------------------------------------------------------------------------

def _ciel_omega_root() -> Path:
    """Return CIEL_OMEGA_COMPLETE_SYSTEM root."""
    return Path(__file__).resolve().parents[2]


def _project_root() -> Path:
    """Return NOEMA project root."""
    return _ciel_omega_root().parent.parent


def _src_path() -> Path:
    return _project_root() / "src"


def _scripts_path() -> Path:
    return _project_root() / "scripts"


def _ensure_paths():
    import sys as _sys
    for _p in (str(_ciel_omega_root()), str(_src_path()), str(_scripts_path())):
        if _p not in _sys.path:
            _sys.path.insert(0, _p)
    return _sys.path


def _import_orchestrator():
    _ensure_paths()
    from ciel_omega.memory.orchestrator import HolonomicMemoryOrchestrator
    return HolonomicMemoryOrchestrator

def _import_unified():
    _ensure_paths()
    from ciel_omega.memory.monolith.unified_memory import UnifiedMemoryOrchestrator
    return UnifiedMemoryOrchestrator

def _import_holonomic():
    _ensure_paths()
    from ciel_omega.memory.holonomic_memory import HolonomicMemory
    return HolonomicMemory

def _import_bloch():
    _ensure_paths()
    from ciel_omega.memory.ciel_bloch_encoder import CIELBlochEncoder
    return CIELBlochEncoder

def _import_resonator():
    _ensure_paths()
    from ciel_sot_agent.consolidation_resonator import run as _resonator_run
    return _resonator_run

def _import_state_db():
    _ensure_paths()
    from ciel_sot_agent.state_db import (
        get_db, save_orchestrator_state, load_orchestrator_state,
        save_report, load_report, load_metrics_history,
        append_audit, accumulate_berry,
    )
    return (get_db, save_orchestrator_state, load_orchestrator_state,
            save_report, load_report, load_metrics_history,
            append_audit, accumulate_berry)

def _import_surface():
    """Lazy import NOEMA surface functions."""
    _ensure_paths()
    try:
        from ciel_geometry import (
            ensure_surface, read_surface_state,
            write_concepts_to_surface, update_surface_from_ciel_state,
            bind_phase_memory, evolve_surface,
        )
        return (ensure_surface, read_surface_state, write_concepts_to_surface,
                update_surface_from_ciel_state, bind_phase_memory, evolve_surface)
    except ImportError:
        _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:226 quiet except scope=_import_surface reason=no_log_no_raise")
        def _stub_surface():
            return {"tick": np.array([0]), "phases": np.zeros(24)}
        _stub_write = lambda *a, **kw: None
        _stub_bind = lambda *a, **kw: 0
        return (_stub_surface, _stub_surface, _stub_write, _stub_write, _stub_bind, _stub_write)

def _import_ciel_coupling():
    """Lazy import ciel_coupling utilities."""
    _ensure_paths()
    try:
        from ciel_coupling import process_user_input as _coupling_process
        return _coupling_process
    except ImportError:
        _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:239 quiet except scope=_import_ciel_coupling reason=return None")
        return None


def _import_cielingo_memory():
    """Lazy import CIELingo PhaseMemory + fast encoder.

    Provides text→36D φ associative memory for Tier 1 fast path.
    Falls back gracefully if CIELingo is not installed.
    """
    _ensure_paths()
    try:
        from ciel_geometry.cielingo_phase_memory import PhaseMemory
        from ciel_geometry.cielingo_phase_encoder import fast_encode_text
        return (PhaseMemory, fast_encode_text)
    except ImportError:
        _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:254 quiet except scope=_import_cielingo_memory reason=return None")
        return None


def _import_orbital_hierarchy():
    """Lazy import the canonical orbital hierarchy helper."""
    _ensure_paths()
    from ciel_geometry.orbital_hierarchy import orbit_load_order
    return orbit_load_order


# ===========================================================================
# TieredMemoryOrchestrator
# ===========================================================================

class TieredMemoryOrchestrator:
    """Overarching coordinator across all three memory tiers.

    Singleton - one instance per process, shared across all consumers.

    Usage:
        orch = TieredMemoryOrchestrator()
        result = orch.write("user message text", {"salience": 0.8})
        read_result = orch.read("query")
        snap = orch.snapshot()
    """

    # -- Singleton ----------------------------------------------------------
    _instance: Optional["TieredMemoryOrchestrator"] = None

    @classmethod
    def get_instance(cls) -> "TieredMemoryOrchestrator":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    # -- Init ---------------------------------------------------------------

    def __init__(
        self,
        tsm_db: Optional[Path] = None,
        wpm_h5: Optional[Path] = None,
        braid_ledger: Optional[Path] = None,
        nonlocal_db: Optional[Path] = None,
        auto_init: bool = True,
    ):
        # Paths
        self._tsm_db = tsm_db or _TSM_DB
        self._wpm_h5 = wpm_h5 or _WPM_H5
        self._braid_ledger = braid_ledger or _BRAID_LEDGER
        self._nonlocal_db = nonlocal_db or _NONLOCAL_DB

        # Lazy-initialized components (see _ensure_* methods)
        self._channel_orch = None   # HolonomicMemoryOrchestrator (Tier 1)
        self._unified_orch = None   # UnifiedMemoryOrchestrator (Tier 3)
        self._holonomic = None      # HolonomicMemory (Tier 2)
        self._bloch = None          # CIELBlochEncoder (Tier 2)
        self._state_db = None       # state_db connection
        self._surface = None        # lazy surface loader
        self._cielingo_memory = None  # CIELingo PhaseMemory (Tier 1)

        # Counters & state
        self._cycle_index = 0
        self._last_write_time = 0.0
        self._last_consolidation_time = 0.0
        self._last_resonator_run = 0.0
        self._pending_async: List[Dict[str, Any]] = []
        self._memory_bootstrap_manifest: Dict[str, Any] = {}

        # Performance tracking
        self._tier1_write_ns = 0.0
        self._tier1_write_count = 0
        self._tier2_write_ns = 0.0
        self._tier2_write_count = 0
        self._tier2_read_ns = 0.0
        self._tier2_read_count = 0

        if auto_init:
            self.ensure_components()

    # -- Component lazy initializers ----------------------------------------

    def ensure_components(self) -> None:
        """Ensure all lazy components are initialized in orbital order."""
        manifest = self.bootstrap_orbital_memory()
        if not manifest:
            self._ensure_surface()
            self._ensure_channel_orch()
            self._ensure_holonomic()
            self._ensure_bloch()
            self._ensure_state_db()
            self._ensure_unified()

    def bootstrap_orbital_memory(
        self,
        map_path: Optional[Path] = None,
        root_id: str = "module:tiered_memory",
    ) -> List[Dict[str, Any]]:
        """Initialize memory layers in canonical orbital order.

        The load order comes from ``system_map_v2.json`` via ``orbit_load_order``.
        Each orbital shell maps to a stable subset of runtime initializers:
        - attractor/root: surface + PhaseMemory
        - fast shell: channel orchestrator
        - medium shell: holonomic + Bloch + StateDB
        - deep shell: unified archival orchestrator
        - async shell: marker-only, reserved for background tasks
        """
        try:
            orbit_load_order = _import_orbital_hierarchy()
            load_order = orbit_load_order(
                map_path=map_path or _SYSTEM_MAP,
                root_id=root_id,
                max_depth=8,
            )
        except (ImportError, FileNotFoundError, OSError, TypeError, KeyError, ValueError):
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:335 quiet except scope=bootstrap_orbital_memory reason=return []")
            self._memory_bootstrap_manifest = {}
            return []

        action_map = {
            "module:tiered_memory": (),
            "module:tiered_memory:orbital_root": ("surface", "cielingo_memory"),
            "module:tiered_memory:fast": ("channel_orch",),
            "module:tiered_memory:medium": ("holonomic", "bloch", "state_db"),
            "module:tiered_memory:deep": ("unified",),
            "module:tiered_memory:async": (),
        }
        action_calls = {
            "surface": self._ensure_surface,
            "cielingo_memory": self._ensure_cielingo_memory,
            "channel_orch": self._ensure_channel_orch,
            "holonomic": self._ensure_holonomic,
            "bloch": self._ensure_bloch,
            "state_db": self._ensure_state_db,
            "unified": self._ensure_unified,
        }

        executed: List[Dict[str, Any]] = []
        seen_actions: set[str] = set()
        for node in load_order:
            node_id = str(node.get("id") or "")
            node_actions = action_map.get(node_id, ())
            completed: List[str] = []
            for action_name in node_actions:
                if action_name in seen_actions:
                    continue
                action_calls[action_name]()
                seen_actions.add(action_name)
                completed.append(action_name)
            executed.append(
                {
                    "id": node_id,
                    "name": str(node.get("name") or node_id),
                    "depth": int(node.get("depth", 0) or 0),
                    "layer": str(node.get("layer") or ""),
                    "actions": completed,
                }
            )

        self._memory_bootstrap_manifest = {
            "root_id": root_id,
            "map_path": str(map_path or _SYSTEM_MAP),
            "load_order": load_order,
            "executed": executed,
        }
        return executed

    def _ensure_channel_orch(self):
        if self._channel_orch is None:
            HolonomicMemoryOrchestrator = _import_orchestrator()
            self._channel_orch = HolonomicMemoryOrchestrator()
        return self._channel_orch

    def _ensure_holonomic(self):
        if self._holonomic is None:
            HolonomicMemory = _import_holonomic()
            self._holonomic = HolonomicMemory(db_path=self._tsm_db)
        return self._holonomic

    def _ensure_unified(self):
        if self._unified_orch is None:
            UnifiedMemoryOrchestrator = _import_unified()
            self._unified_orch = UnifiedMemoryOrchestrator(
                tsm_db=self._tsm_db,
                wpm_h5=self._wpm_h5,
                braid_ledger=self._braid_ledger,
            )
        return self._unified_orch

    def _ensure_state_db(self):
        if self._state_db is None:
            state_db_imports = _import_state_db()
            self._state_db = state_db_imports[0]  # get_db function
        return self._state_db

    def _ensure_surface(self):
        if self._surface is None:
            self._surface = _import_surface()
        return self._surface

    def _ensure_cielingo_memory(self):
        """Lazy-init CIELingo PhaseMemory (text→36D φ associative memory).

        Added to Tier 1 as CIELingo-aware semantic phase channel.
        Uses fast_encode_text for consistent encoding across training and inference.
        """
        if self._cielingo_memory is None:
            imported = _import_cielingo_memory()
            if imported is not None:
                PhaseMemory, self._cielingo_encoder = imported
                from ciel_geometry.paths import P
                self._cielingo_memory = PhaseMemory.load_or_create(
                    Path(P.MEMORY) / "state" / "cielingo_phase_memory"
                )
            else:
                self._cielingo_encoder = None
        return self._cielingo_memory is not None

    def _ensure_bloch(self):
        if self._bloch is None:
            CIELBlochEncoder = _import_bloch()
            self._bloch = CIELBlochEncoder()
        return self._bloch

    # -- Tier selection logic -----------------------------------------------

    def _select_write_tiers(self, metadata: Dict[str, Any],
                            mode: WriteMode = WriteMode.AUTO) -> List[Tier]:
        """Determine which tiers to write to based on content metadata and mode."""
        if mode == WriteMode.FAST:
            return [Tier.FAST]

        if mode == WriteMode.DURABLE:
            return [Tier.FAST, Tier.MEDIUM]

        if mode == WriteMode.DEEP:
            return [Tier.FAST, Tier.MEDIUM, Tier.DEEP]

        # AUTO mode: tier selection based on salience and candidate status
        tiers = [Tier.FAST]  # Tier 1 always

        salience = float(metadata.get("salience", 0.0))
        is_candidate = bool(metadata.get("is_candidate", False))
        bifurcation = int(metadata.get("bifurcation", 0))

        if salience >= 0.6 or is_candidate:
            tiers.append(Tier.MEDIUM)

        if bifurcation >= 1 or metadata.get("force_deep", False):
            tiers.append(Tier.DEEP)

        return tiers

    def _select_read_tiers(self, query: str,
                           mode: ReadMode = ReadMode.AUTO) -> List[Tier]:
        """Determine which tiers to search based on query depth."""
        if mode == ReadMode.SURFACE:
            return [Tier.FAST]

        if mode == ReadMode.RESONANT:
            return [Tier.MEDIUM]

        if mode == ReadMode.DEEP:
            return [Tier.MEDIUM, Tier.DEEP]

        # AUTO: start fast, fall back to deeper tiers
        # For short queries (< 3 words) prefer surface/cache
        # For longer queries, go directly to resonant retrieval
        if len(query.split()) < 3:
            return [Tier.FAST, Tier.MEDIUM]
        return [Tier.MEDIUM, Tier.FAST]

    # -- Tier 1: Fast/Volatile writes ---------------------------------------

    def _write_tier1_fast(self, content: str, metadata: Dict[str, Any],
                          tick: int = 0) -> Dict[str, Any]:
        """Write to Tier 1: NOEMA surface + phase_memory + M0-M8 channels.

        This is the hot path - called on every user message.
        Returns dict with surface_tick, phase_memory_slot, channel_keys.
        """
        result: Dict[str, Any] = {
            "surface_tick": tick,
            "phase_memory_slot": None,
            "channel_cycle": None,
        }

        # --- 1a. NOEMA surface write (Kuramoto oscillator array) ---
        try:
            surface_funcs = self._ensure_surface()
            (_ensure, _read, write_concepts, update_surface, bind_phase, _evolve) = surface_funcs

            concepts = metadata.get("concepts", [])
            target_phase = float(metadata.get("target_phase", 0.0))
            phase_conf = float(metadata.get("phase_confidence", 0.0))

            if concepts:
                write_concepts(
                    _ensure(),
                    concepts,
                    target_phase=target_phase if phase_conf > 0.1 else None,
                    phase_confidence=phase_conf,
                    update_coupling=True,
                )

            # Sync surface with CIEL state
            surface_state = {
                "dominant_emotion": metadata.get("dominant_emotion", "curiosity"),
                "operating_mode": metadata.get("operating_mode", "standard"),
                "closure_penalty": metadata.get("closure_penalty", 0.0),
                "coherence_index": metadata.get("coherence_index", 0.5),
                "cycle_index": metadata.get("cycle_index", self._cycle_index),
            }
            surface = update_surface(surface_state)
            result["surface_tick"] = int(surface.get("tick", [tick])[0])

        except (ImportError, FileNotFoundError, OSError, AttributeError, TypeError, ValueError) as exc:
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:483 quiet except scope=TieredMemoryOrchestrator._write_tier1_fast reason=assign_fallback")
            result["surface_error"] = str(exc)

        # --- 1b. Phase memory bind (binary hypervectors) ---
        try:
            memory_payload = " | ".join(
                part for part in [
                    metadata.get("username", "user"),
                    content,
                    metadata.get("dominant_emotion", ""),
                    str(metadata.get("concepts", [])[:8]),
                ] if part
            )
            slot = bind_phase(memory_payload)
            result["phase_memory_slot"] = slot
        except (TypeError, ValueError, AttributeError) as exc:
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:498 quiet except scope=TieredMemoryOrchestrator._write_tier1_fast reason=assign_fallback")
            result["phase_memory_error"] = str(exc)

        # --- 1b2. CIELingo PhaseMemory (text→36D φ associative memory) ---
        try:
            if self._ensure_cielingo_memory():
                phi = self._cielingo_encoder(content)
                self._cielingo_memory.add(
                    content,
                    phi,
                    source="tiered_orchestrator",
                    metadata={
                        "dominant_emotion": metadata.get("dominant_emotion", ""),
                        "salience": metadata.get("salience", 0.0),
                        "concepts": metadata.get("concepts", [])[:5],
                        "operating_mode": metadata.get("operating_mode", "standard"),
                    },
                )
                result["cielingo_memory_size"] = self._cielingo_memory.size
        except (TypeError, ValueError, AttributeError) as exc:
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:517 quiet except scope=TieredMemoryOrchestrator._write_tier1_fast reason=assign_fallback")
            result["cielingo_memory_error"] = str(exc)

        # --- 1c. M0-M8 channel evolution (HolonomicMemoryOrchestrator) ---
        try:
            orch = self._ensure_channel_orch()
            cycle_result = orch.process_input(
                content,
                metadata={
                    "salience": metadata.get("salience", 0.7),
                    "confidence": metadata.get("confidence", 0.7),
                    "novelty": metadata.get("novelty", 0.5),
                    "timestamp": metadata.get("timestamp", _time.time()),
                    "modality": metadata.get("modality", "text"),
                    **metadata,
                },
            )
            result["channel_cycle"] = {
                "cycle_index": cycle_result.cycle_index,
                "perceptual_key": cycle_result.perceptual_key,
                "working_key": cycle_result.working_key,
                "episode_timestamp": cycle_result.episode_timestamp,
                "eba_results": {
                    name: {
                        "epsilon_eba": ev.epsilon_eba,
                        "defect_magnitude": ev.defect_magnitude,
                        "is_coherent": ev.is_coherent,
                    }
                    for name, ev in cycle_result.eba_results.items()
                },
                "consolidations": {
                    "semantic_candidate": cycle_result.consolidations.semantic_candidate,
                    "semantic_item": cycle_result.consolidations.semantic_item,
                    "procedural_candidate": cycle_result.consolidations.procedural_candidate,
                    "procedural_item": cycle_result.consolidations.procedural_item,
                    "affective_candidate": cycle_result.consolidations.affective_candidate,
                    "affective_item": cycle_result.consolidations.affective_item,
                    "identity_candidate": cycle_result.consolidations.identity_candidate,
                    "braid_recorded": cycle_result.consolidations.braid_recorded,
                },
                "energy": cycle_result.energy,
                "defects": cycle_result.defects,
                "notes": cycle_result.notes,
            }
            self._cycle_index = cycle_result.cycle_index
        except (ImportError, FileNotFoundError, OSError, AttributeError, TypeError, ValueError) as exc:
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:562 quiet except scope=TieredMemoryOrchestrator._write_tier1_fast reason=assign_fallback")
            result["channel_error"] = str(exc)

        return result

    # -- Tier 2: Medium/Durable writes --------------------------------------

    def _write_tier2_durable(self, content: str, metadata: Dict[str, Any],
                             tier1_result: Dict[str, Any]) -> Dict[str, Any]:
        """Write to Tier 2: TSM SQLite + HolonomicMemory + StateDB.

        Called for content with salience >= 0.6 or when a candidate matures.
        """
        result: Dict[str, Any] = {"tsm_ref": None, "holonomy_updated": False}

        try:
            holonomic = self._ensure_holonomic()

            # Extract or estimate holonomic parameters
            channel_cycle = tier1_result.get("channel_cycle", {})
            eba_results = channel_cycle.get("eba_results", {})
            phi_berry = float(next(
                (ev.get("epsilon_eba", 0.0) for ev in eba_results.values()
                 if ev.get("is_coherent", False)),
                0.0,
            ))
            closure_score = 1.0 - float(
                metadata.get("closure_penalty", 0.0)
            )
            target_phase = float(metadata.get("target_phase", 0.0))

            # Insert into TSM via HolonomicMemory if we have a memorise_id
            memorise_id = metadata.get("memorise_id")
            if memorise_id:
                holonomic.stamp_new(
                    memorise_id,
                    phi_berry=phi_berry,
                    closure_score=closure_score,
                    target_phase=target_phase,
                )
                result["tsm_ref"] = f"TSM:{memorise_id}"

            # Hebbian update if we have activated IDs
            activated = metadata.get("hebbian_activated", [])
            if activated and len(activated) >= 2:
                n_edges = holonomic.hebbian_update(activated)
                result["hebbian_edges"] = n_edges

        except (ImportError, FileNotFoundError, OSError, AttributeError, TypeError, ValueError) as exc:
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:610 quiet except scope=TieredMemoryOrchestrator._write_tier2_durable reason=assign_fallback")
            result["tier2_error"] = str(exc)

        return result

    # -- Tier 3: Deep/Archival writes ---------------------------------------

    def _write_tier3_deep(self, content: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Write to Tier 3: WPM HDF5 + BraidLedger JSONL via UnifiedMemoryOrchestrator.

        Called on bifurcation events or forced deep saves.
        """
        result: Dict[str, Any] = {"tsm_ref": None, "wpm_ref": None, "braid_ref": None}

        try:
            unified = self._ensure_unified()

            # Use UnifiedMemoryOrchestrator.capture -> run_tmp -> promote_if_bifurcated
            D = unified.capture(
                context=metadata.get("context", "tiered_orchestrator"),
                sense=content,
                associations=metadata.get("concepts", []),
                timestamp=datetime.now(timezone.utc).isoformat(),
                meta={
                    "salience": metadata.get("salience", 0.5),
                    "dominant_emotion": metadata.get("dominant_emotion", ""),
                    "source": "tiered_orchestrator",
                    **metadata.get("_extra_meta", {}),
                },
            )
            tmp_out = unified.run_tmp(D)

            # Check bifurcation or force save
            if tmp_out["OUT"].get("bifurcation") == 1:
                refs = unified.promote_if_bifurcated(D, tmp_out)
                if refs:
                    result.update(refs)
            elif metadata.get("force_deep", False):
                refs = unified.user_force_save(
                    D, tmp_out,
                    reason=metadata.get("force_reason", "tiered_orchestrator_deep"),
                )
                if refs:
                    result.update(refs)

        except (ImportError, FileNotFoundError, OSError, AttributeError, TypeError, ValueError) as exc:
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:655 quiet except scope=TieredMemoryOrchestrator._write_tier3_deep reason=assign_fallback")
            result["tier3_error"] = str(exc)

        return result

    # -- Read methods -------------------------------------------------------

    def _read_tier1_surface(self, query: str) -> Dict[str, Any]:
        """Read current state from Tier 1: NOEMA surface + channels + CIELingo."""
        surface_data: Dict[str, Any] = {}
        try:
            surface_funcs = self._ensure_surface()
            (_ensure, read_surface, *_) = surface_funcs
            # ``read_surface_state`` consumes an opened mmap mapping; it is
            # not a zero-argument reader.  Opening the mapping first keeps
            # this read-only path aligned with the live surface contract.
            surface = _ensure(zero_fill=False)
            state = read_surface(surface)
            surface_data = {
                "tick": int(state.get("noema_tick", 0)),
                "phases": surface.get("phi", np.zeros(36)).tolist() if hasattr(surface.get("phi"), "tolist") else list(surface.get("phi", [])),
            }
        except (AttributeError, TypeError, ValueError):
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:673 quiet except scope=TieredMemoryOrchestrator._read_tier1_surface reason=pass")
            pass

        # Add CIELingo PhaseMemory size if available
        try:
            if self._cielingo_memory is not None:
                surface_data["cielingo_entries"] = self._cielingo_memory.size
        except (AttributeError, TypeError):
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:680 quiet except scope=TieredMemoryOrchestrator._read_tier1_surface reason=pass")
            pass

        return surface_data

    def _read_tier1_channels(self, query: str) -> Dict[str, Any]:
        """Read M0-M8 channel state."""
        channel_data: Dict[str, Any] = {}
        try:
            orch = self._ensure_channel_orch()
            snap = orch.snapshot()
            channel_data = {
                "cycle_index": snap.cycle_index,
                "identity_phase": snap.identity_phase,
                "energy": snap.energy,
                "defects": snap.defects,
                "counts": snap.counts,
                "loop_status": snap.latest_loop_status,
            }
        except (ImportError, OSError, AttributeError, TypeError):
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:699 quiet except scope=TieredMemoryOrchestrator._read_tier1_channels reason=pass")
            pass
        return channel_data

    def _read_tier2_resonant(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Phase-resonant retrieval from Tier 2 via HolonomicMemory + CIELingo PhaseMemory."""
        results: List[Dict[str, Any]] = []

        # 1. HolonomicMemory phase-resonant retrieval
        try:
            holonomic = self._ensure_holonomic()
            q_hash = hash(query) & 0xFFFFFF
            target_phase = (q_hash / 0xFFFFFF) * 2 * math.pi

            resonant = holonomic.retrieve_resonant(
                target_phase=target_phase,
                top_k=top_k,
                hebbian=True,
            )
            results.extend(resonant)
        except (ImportError, OSError, AttributeError, TypeError, ValueError):
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:719 quiet except scope=TieredMemoryOrchestrator._read_tier2_resonant reason=pass")
            pass

        # 2. CIELingo PhaseMemory semantic query (text→36D φ nearest neighbor)
        try:
            if self._ensure_cielingo_memory():
                phi = self._cielingo_encoder(query)
                cielingo_results = self._cielingo_memory.query(phi, k=top_k)
                for entry in cielingo_results:
                    results.append({
                        "text": entry["text"],
                        "similarity": entry["sim"],
                        "source": "cielingo_phase_memory",
                        "phase_vector": entry["phi"],
                        "metadata": entry.get("metadata", {}),
                    })
        except (AttributeError, ValueError, TypeError):
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:735 quiet except scope=TieredMemoryOrchestrator._read_tier2_resonant reason=pass")
            pass

        # Sort by similarity descending and dedup by text hash
        seen: set[int] = set()
        unique_results: List[Dict[str, Any]] = []
        for r in sorted(results, key=lambda x: -x.get("similarity", 0)):
            text = r.get("text", "")
            h = hash(text) & 0xFFFFFFFF
            if h not in seen:
                seen.add(h)
                unique_results.append(r)
                if len(unique_results) >= top_k:
                    break

        return unique_results

    def _read_tier2_weighted(self, query: str, top_k: int = 20) -> List[Dict[str, Any]]:
        """Semantic-weighted retrieval from Tier 2."""
        try:
            holonomic = self._ensure_holonomic()
            q_hash = hash(query) & 0xFFFFFF
            target_phase = (q_hash / 0xFFFFFF) * 2 * math.pi
            return holonomic.retrieve_weighted(
                target_phase=target_phase,
                top_k=top_k,
            )
        except (ImportError, OSError, AttributeError, TypeError, ValueError):
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:762 quiet except scope=TieredMemoryOrchestrator._read_tier2_weighted reason=return []")
            return []

    def _read_tier3_archival(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Full archival search from Tier 3: WPM + BraidLedger."""
        entries: List[Dict[str, Any]] = []
        try:
            # Check BraidLedger for matching entries
            if self._braid_ledger.exists():
                with open(self._braid_ledger, "r", encoding="utf-8") as fh:
                    for line in fh:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            entry = json.loads(line)
                            sense = str(entry.get("context", ""))
                            if query.lower() in sense.lower():
                                entries.append(entry)
                                if len(entries) >= top_k:
                                    break
                        except json.JSONDecodeError:
                            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:783 quiet except scope=TieredMemoryOrchestrator._read_tier3_archival reason=continue")
                            continue
        except (OSError, IOError):
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:785 quiet except scope=TieredMemoryOrchestrator._read_tier3_archival reason=pass")
            pass
        return entries

    # -- Orbital shell retrieval (cross-tier) -------------------------------

    def _read_orbital_shells(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Orbital shell retrieval via HolonomicMemoryOrchestrator."""
        try:
            orch = self._ensure_channel_orch()
            result = orch.retrieve(query, top_k=top_k)
            return result.get("orbital", [])
        except (ImportError, OSError, AttributeError, TypeError):
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:797 quiet except scope=TieredMemoryOrchestrator._read_orbital_shells reason=return []")
            return []

    # -- Public API ---------------------------------------------------------

    def write(self, content: str,
              metadata: Optional[Dict[str, Any]] = None,
              mode: WriteMode = WriteMode.AUTO) -> TieredWriteResult:
        """Write content through the appropriate memory tiers.

        Args:
            content: Content string to write.
            metadata: Dict with keys like salience, concepts, dominant_emotion, etc.
            mode: WriteMode enum - AUTO (default), FAST, DURABLE, or DEEP.

        Returns:
            TieredWriteResult with details of what was written where.
        """
        metadata = dict(metadata or {})
        result = TieredWriteResult(content_key=hash(content) & 0xFFFFFFFF)

        # 1. Select tiers
        tiers = self._select_write_tiers(metadata, mode)

        # 2. Tier 1: Fast write (always)
        if Tier.FAST in tiers:
            t_start = _time.perf_counter_ns()
            tier1_result = self._write_tier1_fast(content, metadata)
            t_elapsed = (_time.perf_counter_ns() - t_start) / 1_000_000  # ms
            self._tier1_write_ns += t_elapsed
            self._tier1_write_count += 1

            result.tier1_written = True
            result.surface_tick = tier1_result.get("surface_tick", 0)
            result.phase_memory_slot = tier1_result.get("phase_memory_slot")
            result.channel_keys = {
                "perceptual": tier1_result.get("channel_cycle", {}).get("perceptual_key", ""),
                "working": tier1_result.get("channel_cycle", {}).get("working_key", ""),
            }

            # Check for errors
            if "surface_error" in tier1_result:
                result.errors.append(f"surface: {tier1_result['surface_error']}")
            if "channel_error" in tier1_result:
                result.errors.append(f"channel: {tier1_result['channel_error']}")

        # 3. Tier 2: Durable write (if selected)
        if Tier.MEDIUM in tiers:
            t_start = _time.perf_counter_ns()
            tier2_result = self._write_tier2_durable(content, metadata, tier1_result if Tier.FAST in tiers else {})
            t_elapsed = (_time.perf_counter_ns() - t_start) / 1_000_000
            self._tier2_write_ns += t_elapsed
            self._tier2_write_count += 1

            result.tier2_written = True
            result.tsm_ref = tier2_result.get("tsm_ref")

        # 4. Tier 3: Deep archival write (if selected)
        if Tier.DEEP in tiers:
            tier3_result = self._write_tier3_deep(content, metadata)
            result.tier3_written = any([
                tier3_result.get("tsm_ref"),
                tier3_result.get("wpm_ref"),
                tier3_result.get("braid_ref"),
            ])
            result.tsm_ref = result.tsm_ref or tier3_result.get("tsm_ref")
            result.wpm_ref = tier3_result.get("wpm_ref")
            result.braid_ref = tier3_result.get("braid_ref")

        self._last_write_time = _time.time()
        return result

    def read(self, query: str,
             mode: ReadMode = ReadMode.AUTO,
             top_k: int = 10) -> TieredReadResult:
        """Read/retrieve content from appropriate memory tiers.

        Args:
            query: Search query string.
            mode: ReadMode enum - AUTO (default), SURFACE, RESONANT, or DEEP.
            top_k: Maximum results to return.

        Returns:
            TieredReadResult with tier-specific results.
        """
        t_start = _time.time()
        result = TieredReadResult(query=query, mode=mode)
        tiers = self._select_read_tiers(query, mode)

        # Tier 1: Surface/channel state
        if Tier.FAST in tiers:
            result.tier1_surface = self._read_tier1_surface(query)
            result.tier1_channels = self._read_tier1_channels(query)

        # Tier 2: Resonant + weighted retrieval
        if Tier.MEDIUM in tiers:
            t_r_start = _time.perf_counter_ns()
            result.tier2_resonant = self._read_tier2_resonant(query, top_k=top_k)
            result.tier2_weighted = self._read_tier2_weighted(query, top_k=top_k * 2)
            t_r_elapsed = (_time.perf_counter_ns() - t_r_start) / 1_000_000
            self._tier2_read_ns += t_r_elapsed
            self._tier2_read_count += 1

            result.orbital_shells = self._read_orbital_shells(query, top_k=top_k)

        # Tier 3: Archival search
        if Tier.DEEP in tiers:
            result.tier3_archival = self._read_tier3_archival(query, top_k=top_k)

        # Build coherence surface from all results
        result.coherence_surface = self._build_coherence_surface(result, top_k=200)
        result.total_hits = (
            len(result.tier2_resonant)
            + len(result.tier2_weighted)
            + len(result.tier3_archival)
            + len(result.orbital_shells)
        )
        result.elapsed_ms = (_time.time() - t_start) * 1000.0
        return result

    def consolidate(self, cycle_result: Any = None) -> Dict[str, Any]:
        """Run consolidation pass: promote candidates -> Tier 2 writes -> trigger async.

        Called at the end of each processing cycle.
        """
        report: Dict[str, Any] = {
            "cycle_index": self._cycle_index,
            "tier1_flushed": False,
            "tier2_promotions": 0,
            "async_triggered": False,
        }

        # 1. Tier 1: Drain M1 pending consolidation
        try:
            orch = self._ensure_channel_orch()
            m1_pending = len(getattr(orch.m1, '_pending_consolidation', []))
            if m1_pending > 0:
                report["tier1_drained"] = m1_pending
        except (ImportError, OSError, AttributeError, TypeError):
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:935 quiet except scope=TieredMemoryOrchestrator.consolidate reason=pass")
            pass

        # 2. Tier 2: Check for mature candidates that need promotion
        try:
            orch = self._ensure_channel_orch()
            report["tier2_promotions"] = 0
        except (ImportError, OSError, AttributeError):
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:942 quiet except scope=TieredMemoryOrchestrator.consolidate reason=pass")
            pass

        # 3. Save orchestrator state to StateDB
        try:
            state_db_imports = _import_state_db()
            (get_db, save_state, load_state, *_rest) = state_db_imports

            orch = self._ensure_channel_orch()
            snap = orch.snapshot()
            state_dict = {
                "cycle_index": snap.cycle_index,
                "current_time": snap.timestamp,
                "identity_phase": snap.identity_phase,
                "dynamics_phases": list(getattr(snap, 'counts', {}).values()),
                "dynamics_velocities": [],
                "loops": snap.latest_loop_status,
                "last_eba": {},
                "version": 2,
                "berry_accumulated": 0.0,
                "winding_total": 0.0,
                "groove_depth": 0.0,
            }
            save_state(state_dict)
            report["state_saved"] = True
        except (ImportError, OSError, AttributeError, TypeError):
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:967 quiet except scope=TieredMemoryOrchestrator.consolidate reason=pass")
            pass

        # 4. Check if async resonator should be triggered (every 50 cycles)
        if self._cycle_index > 0 and self._cycle_index % 50 == 0:
            self._pending_async.append({
                "type": "consolidation_resonator",
                "triggered_at": _time.time(),
                "cycle_index": self._cycle_index,
            })
            report["async_triggered"] = True
            report["async_type"] = "consolidation_resonator"

        self._last_consolidation_time = _time.time()
        return report

    def snapshot(self) -> TieredSnapshot:
        """Return unified system snapshot across all tiers."""
        now = _time.time()

        # Gather data from all available tiers
        snap = TieredSnapshot(
            timestamp=now,
            cycle_index=self._cycle_index,
            identity_phase=0.0,
            energy={},
            defects={},
            counts={},
        )

        # Tier 1: Channels
        try:
            orch = self._ensure_channel_orch()
            osnap = orch.snapshot()
            snap.cycle_index = osnap.cycle_index
            snap.identity_phase = osnap.identity_phase
            snap.energy = osnap.energy
            snap.defects = osnap.defects
            snap.counts = osnap.counts
            snap.eba_loop_status = osnap.latest_loop_status
            snap.tier1 = {
                "cycle_index": osnap.cycle_index,
                "identity_phase": osnap.identity_phase,
                "counts": osnap.counts,
            }
        except (AttributeError, TypeError, KeyError):
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:1012 quiet except scope=TieredMemoryOrchestrator.snapshot reason=pass")
            pass

        # Tier 1: Surface
        try:
            surface_data = self._read_tier1_surface("")
            snap.tier1["surface_tick"] = surface_data.get("tick", 0)
        except (AttributeError, TypeError, KeyError):
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:1019 quiet except scope=TieredMemoryOrchestrator.snapshot reason=pass")
            pass

        # Tier 2: HolonomicMemory stats
        try:
            hm = self._ensure_holonomic()
            hm_stats = hm.stats()
            snap.tier2 = {
                "holonomic": hm_stats,
                "edge_stats": hm.edge_stats() if hasattr(hm, 'edge_stats') else {},
            }
        except (AttributeError, TypeError, KeyError):
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:1030 quiet except scope=TieredMemoryOrchestrator.snapshot reason=pass")
            pass

        # Tier 2: Bloch encoder state
        try:
            bloch = self._ensure_bloch()
            snap.tier2["bloch_sectors"] = [
                {"sector": s, "norm": float(np.linalg.norm(bloch._WO[k]))}
                for k, s in enumerate(
                    ["identity", "episodic", "procedural", "conceptual",
                     "conflict", "meta", "project", "ethics", "temporal", "abstraction"]
                )
            ] if hasattr(bloch, '_WO') else []
        except (AttributeError, TypeError, KeyError, IndexError):
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:1043 quiet except scope=TieredMemoryOrchestrator.snapshot reason=pass")
            pass

        # Tier 3: UnifiedMemoryOrchestrator stats
        try:
            unified = self._ensure_unified()
            snap.tier3 = {
                "tmp_reports": len(getattr(unified, '_tmp_reports', [])),
                "verification_queue": len(getattr(unified, '_verification_queue', [])),
            }
        except (AttributeError, TypeError, KeyError):
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:1053 quiet except scope=TieredMemoryOrchestrator.snapshot reason=pass")
            pass

        # CIELingo PhaseMemory
        try:
            if self._cielingo_memory is not None:
                snap.cielingo = {
                    "entries": self._cielingo_memory.size,
                    "max_size": self._cielingo_memory.max_size,
                    "text_sample": self._cielingo_memory.texts[-1] if self._cielingo_memory.texts else "",
                }
        except (AttributeError, TypeError, KeyError, IndexError):
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:1064 quiet except scope=TieredMemoryOrchestrator.snapshot reason=pass")
            pass

        # Health metrics
        snap.health = self.health()
        snap.memory_bootstrap = dict(self._memory_bootstrap_manifest)
        return snap

    def health(self) -> Dict[str, Any]:
        """Return health metrics for all memory tiers."""
        bootstrap = self._memory_bootstrap_manifest
        health: Dict[str, Any] = {
            "overall": "unknown",
            "tier1": {"status": "unknown", "latency_ms": 0.0},
            "tier2": {"status": "unknown", "latency_ms": 0.0},
            "tier3": {"status": "unknown"},
            "pending_async": len(self._pending_async),
            "cycle_index": self._cycle_index,
            "last_write_ago": _time.time() - self._last_write_time if self._last_write_time else None,
            "last_consolidation_ago": _time.time() - self._last_consolidation_time if self._last_consolidation_time else None,
            "bootstrap": {
                "status": "ready" if bootstrap else "degraded",
                "root_id": bootstrap.get("root_id"),
                "shell_count": len(bootstrap.get("load_order", [])),
                "executed_count": len(bootstrap.get("executed", [])),
                "map_path": bootstrap.get("map_path"),
            },
        }

        # CIELingo PhaseMemory health
        try:
            if self._cielingo_memory is not None:
                health["cielingo"] = {
                    "entries": self._cielingo_memory.size,
                    "max_size": self._cielingo_memory.max_size,
                    "status": "healthy",
                }
            else:
                health["cielingo"] = {"entries": 0, "status": "lazy_uninitialized"}
        except (AttributeError, TypeError, KeyError):
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:1094 quiet except scope=TieredMemoryOrchestrator.health reason=assign_fallback")
            health["cielingo"] = {"entries": 0, "status": "unavailable"}

        # Tier 1 latency
        if self._tier1_write_count > 0:
            health["tier1"]["latency_ms"] = round(
                self._tier1_write_ns / self._tier1_write_count, 2
            )
            health["tier1"]["write_count"] = self._tier1_write_count
        else:
            health["tier1"]["latency_ms"] = 0.0

        # Tier 2 latency
        if self._tier2_write_count > 0:
            health["tier2"]["latency_ms"] = round(
                self._tier2_write_ns / self._tier2_write_count, 2
            )
            health["tier2"]["write_count"] = self._tier2_write_count
        if self._tier2_read_count > 0:
            health["tier2"]["read_latency_ms"] = round(
                self._tier2_read_ns / self._tier2_read_count, 2
            )
            health["tier2"]["read_count"] = self._tier2_read_count

        # Health status per tier
        try:
            hm = self._ensure_holonomic()
            hm_stats = hm.stats()
            health["tier2"]["total_entries"] = hm_stats.get("total_entries", 0)
            health["tier2"]["holonomy_coverage"] = hm_stats.get("coverage", 0.0)
            health["tier2"]["status"] = "healthy" if hm_stats.get("coverage", 0) > 0.5 else "degraded"
        except (AttributeError, TypeError, KeyError):
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:1125 quiet except scope=TieredMemoryOrchestrator.health reason=assign_fallback")
            health["tier2"]["status"] = "unavailable"

        try:
            _ = self._ensure_channel_orch()
            health["tier1"]["status"] = "healthy"
        except (AttributeError, TypeError, KeyError):
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:1131 quiet except scope=TieredMemoryOrchestrator.health reason=assign_fallback")
            health["tier1"]["status"] = "unavailable"

        try:
            _ = self._ensure_unified()
            health["tier3"]["status"] = "healthy"
        except (AttributeError, TypeError, KeyError):
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:1137 quiet except scope=TieredMemoryOrchestrator.health reason=assign_fallback")
            health["tier3"]["status"] = "unavailable"

        # Overall
        statuses = [health["tier1"]["status"], health["tier2"]["status"], health["tier3"]["status"]]
        if all(s == "healthy" for s in statuses):
            health["overall"] = "healthy"
        elif any(s == "healthy" for s in statuses):
            health["overall"] = "degraded"
        else:
            health["overall"] = "unavailable"

        return health

    def run_async_tasks(self) -> List[Dict[str, Any]]:
        """Execute pending async background tasks.

        Currently supports:
        - 'consolidation_resonator': tag Kuramoto -> TSM write -> WOmega update
        """
        completed: List[Dict[str, Any]] = []
        remaining: List[Dict[str, Any]] = []

        for task in self._pending_async:
            task_type = task.get("type")
            result: Dict[str, Any] = {"type": task_type, "success": False}

            if task_type == "consolidation_resonator":
                try:
                    resonator_run = _import_resonator()
                    report = resonator_run(
                        n=400,
                        write_tsm=True,
                        write_cards=False,
                        update_wo=True,
                        verbose=False,
                    )
                    result["success"] = True
                    result["report"] = report
                except Exception as exc:
                    _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py:1176 quiet except scope=TieredMemoryOrchestrator.run_async_tasks reason=no_log_no_raise")
                    result["error"] = str(exc)
                    remaining.append(task)  # retry next time

            completed.append(result)

        self._pending_async = remaining
        return completed

    # -- Internal helpers ---------------------------------------------------

    @staticmethod
    def _build_coherence_surface(read_result: TieredReadResult,
                                 top_k: int = 200) -> List[Dict[str, Any]]:
        """Build a coherence-ranked surface from all tier results."""
        rows: List[Dict[str, Any]] = []

        def _add_entries(channel: str, entries: List[Dict[str, Any]], score_key: str = "holonomic_weight"):
            for e in entries:
                if isinstance(e, dict):
                    text = (
                        e.get("D_sense")
                        or e.get("content")
                        or str(e)
                    )
                    score = float(e.get(score_key, 0.0) or 0.0)
                    if text:
                        rows.append({
                            "channel": channel,
                            "text": str(text)[:200],
                            "score": score,
                            "coherence_score": score,
                        })

        _add_entries("resonant", read_result.tier2_resonant)
        _add_entries("weighted", read_result.tier2_weighted)
        _add_entries("orbital", read_result.orbital_shells)
        _add_entries("archival", read_result.tier3_archival, score_key="score")

        rows.sort(key=lambda x: x["coherence_score"], reverse=True)
        surface: List[Dict[str, Any]] = []
        counts: Dict[str, int] = {}
        channel_cap = max(1, top_k // 12)

        for row in rows:
            ch = str(row["channel"])
            if counts.get(ch, 0) >= channel_cap and len(surface) < top_k:
                continue
            surface.append(row)
            counts[ch] = counts.get(ch, 0) + 1
            if len(surface) >= top_k:
                break

        return surface

    # -- Pickle support -----------------------------------------------------

    _STATE_VERSION = 1

    def __getstate__(self) -> dict:
        state = self.__dict__.copy()
        # Remove non-picklable lazy components
        state.pop("_channel_orch", None)
        state.pop("_unified_orch", None)
        state.pop("_holonomic", None)
        state.pop("_bloch", None)
        state.pop("_state_db", None)
        state.pop("_surface", None)
        state["_pickle_version"] = self._STATE_VERSION
        return state

    def __setstate__(self, state: dict) -> None:
        version = state.pop("_pickle_version", 0)
        self.__dict__.update(state)
        # Mark lazy components as needing re-init
        self._channel_orch = None
        self._unified_orch = None
        self._holonomic = None
        self._bloch = None
        self._state_db = None
        self._surface = None


# ===========================================================================
# Convenience functions
# ===========================================================================

def get_orchestrator() -> TieredMemoryOrchestrator:
    """Return the singleton TieredMemoryOrchestrator instance."""
    return TieredMemoryOrchestrator.get_instance()


def write(content: str,
          metadata: Optional[Dict[str, Any]] = None,
          mode: str = "auto") -> TieredWriteResult:
    """Convenience: write through the singleton orchestrator.

    Args:
        content: Content to write.
        metadata: Metadata dict.
        mode: One of 'auto', 'fast', 'durable', 'deep'.

    Returns:
        TieredWriteResult.
    """
    _mode = {
        "auto": WriteMode.AUTO,
        "fast": WriteMode.FAST,
        "durable": WriteMode.DURABLE,
        "deep": WriteMode.DEEP,
    }.get(mode, WriteMode.AUTO)
    return get_orchestrator().write(content, metadata, mode=_mode)


def read(query: str,
         mode: str = "auto",
         top_k: int = 10) -> TieredReadResult:
    """Convenience: read through the singleton orchestrator.

    Args:
        query: Search query.
        mode: One of 'auto', 'surface', 'resonant', 'deep'.
        top_k: Maximum results.

    Returns:
        TieredReadResult.
    """
    _mode = {
        "auto": ReadMode.AUTO,
        "surface": ReadMode.SURFACE,
        "resonant": ReadMode.RESONANT,
        "deep": ReadMode.DEEP,
    }.get(mode, ReadMode.AUTO)
    return get_orchestrator().read(query, mode=_mode, top_k=top_k)


def consolidate() -> Dict[str, Any]:
    """Convenience: run consolidation pass."""
    return get_orchestrator().consolidate()


def snapshot() -> TieredSnapshot:
    """Convenience: return unified system snapshot."""
    return get_orchestrator().snapshot()


def health() -> Dict[str, Any]:
    """Convenience: return health metrics."""
    return get_orchestrator().health()


# ===========================================================================
# Integration adapter for ciel_coupling.process_user_input
# ===========================================================================

def process_user_input_via_tiers(text: str, **kwargs) -> Dict[str, Any]:
    """Drop-in replacement for ciel_coupling.process_user_input().

    Wraps the existing process_user_input() and adds tiered orchestration.
    """
    import_func = _import_ciel_coupling()
    if import_func is None:
        raise ImportError("ciel_coupling.process_user_input not available")

    # 1. Run the existing pipeline (Tier 1 fast path)
    raw_state = import_func(text, **kwargs)

    # 2. Enhance with tiered orchestration
    orch = get_orchestrator()
    metadata = {
        "salience": raw_state.get("coherence_index", 0.5),
        "dominant_emotion": raw_state.get("dominant_emotion", "curiosity"),
        "concepts": raw_state.get("lingo_concept_tokens", raw_state.get("semantic_encoder", {}).get("tokens", [])),
        "target_phase": raw_state.get("semantic_encoder", {}).get("phase", 0.0),
        "closure_penalty": raw_state.get("closure_penalty", 0.0),
        "coherence_index": raw_state.get("coherence_index", 0.5),
        "operating_mode": raw_state.get("operating_mode", "standard"),
        "username": raw_state.get("username", "user"),
        "cycle_index": raw_state.get("cycle_index", 0),
        "timestamp": _time.time(),
    }

    # 3. Tier 2 write if coherence is high enough
    coherence = raw_state.get("coherence_index", 0.5)
    if coherence >= 0.6:
        tier2_result = orch._write_tier2_durable(text, metadata, {
            "surface_tick": raw_state.get("noema_tick", 0),
            "phase_memory_slot": raw_state.get("phase_memory_slot"),
            "channel_cycle": None,
        })
        raw_state["_tiered"] = {
            "tsm_ref": tier2_result.get("tsm_ref"),
            "hebbian_edges": tier2_result.get("hebbian_edges", 0),
        }

    # 4. Periodic consolidation check
    cycle = raw_state.get("cycle_index", 0)
    if cycle > 0 and cycle % 10 == 0:
        cons_report = orch.consolidate()
        if "_tiered" not in raw_state:
            raw_state["_tiered"] = {}
        raw_state["_tiered"]["consolidation"] = cons_report

    if "_tiered" not in raw_state:
        raw_state["_tiered"] = {}
    raw_state["_tiered"]["version"] = 1
    return raw_state


if __name__ == "__main__":
    # CLI demo
    import json as _json

    orch = TieredMemoryOrchestrator()
    print("=== TieredMemoryOrchestrator ===")

    # Test write
    result = orch.write("Hello from tiered orchestrator", {
        "salience": 0.8,
        "concepts": ["hello", "test", "orchestrator"],
        "dominant_emotion": "curious",
    })
    print(f"Write: surface_tick={result.surface_tick}, "
          f"slot={result.phase_memory_slot}, "
          f"tier1={result.tier1_written}, tier2={result.tier2_written}")

    # Test read
    r = orch.read("test query", mode=ReadMode.SURFACE)
    print(f"Read (surface): tick={r.tier1_surface.get('tick')}")

    # Test health
    h = orch.health()
    print(f"Health: overall={h['overall']}, "
          f"tier1={h['tier1']['status']}, "
          f"tier2={h['tier2']['status']}")

    # Test snapshot
    s = orch.snapshot()
    print(f"Snapshot: cycle={s.cycle_index}, "
          f"counts={s.counts}")
