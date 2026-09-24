"""CIEL/Ω — High-level orchestration facade.

CielEngine composes wave simulation, cognition, affective processing,
memory coordination, and LLM backends into a single callable engine.

Adapted from CIEL_FIXED/ciel/engine.py with cross-references to ciel_omega modules.
"""

from __future__ import annotations

import logging
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np

# PhaseNav Λ: Ensure ancillary source paths are discoverable
_ENGINE_DIR = Path(__file__).resolve().parent.parent.parent  # ciel_omega/
_SRC_DIR = _ENGINE_DIR.parent  # src/
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))
_GEOMETRY_DIR = _SRC_DIR / "ciel_geometry"
if _GEOMETRY_DIR.exists() and str(_GEOMETRY_DIR) not in sys.path:
    sys.path.insert(0, str(_GEOMETRY_DIR))
_DEMO_DIR = _SRC_DIR / "ciel-omega-demo-main"
if _DEMO_DIR.exists() and str(_DEMO_DIR) not in sys.path:
    sys.path.insert(0, str(_DEMO_DIR))

# PhaseNav Bypass Language — lazy imports: loaded on first call via _li()
_Φ_DEFERRED: dict = {}
def _Φ_lazy() -> tuple:
    """Lazy-load Φ, BypassRuntime, BottleneckBypasses on first use."""
    key = ("Φ", "BypassRuntime", "BottleneckBypasses")
    if key not in _Φ_DEFERRED:
        from ciel_geometry.phasenav_bypass_language import Φ, BypassRuntime, BottleneckBypasses
        _Φ_DEFERRED[key] = (Φ, BypassRuntime, BottleneckBypasses)
    return _Φ_DEFERRED[key]


def _Φ_bottleneck(name: str, primary, fallback, context: dict | None = None,
                   logger: logging.Logger | None = None) -> Any:
    """PhaseNav Φ bypass: SOURCE(name) → ORDER(MODAL_POSSIBILITY, MODAL_NECESSITY) → AFFECT(warning).

    Każdy try/except w engine jest zastąpiony tym jednym wzorcem:
      Φ.COMPOSITION(
        Φ.SOURCE(name),
        Φ.ORDER(
          Φ.MODAL_POSSIBILITY(primary_thunk),   # try: happy path
          Φ.MODAL_NECESSITY(fallback_thunk)      # except: fallback
        ),
        Φ.AFFECT('warning')                      # always log
      )

    primary / fallback — callable(ctx) → result (lazy thunks).
    """
    Φ_cls, BypassRuntime_cls, _ = _Φ_lazy()
    _rt = BypassRuntime_cls(logger or log)
    result = _rt.execute(
        Φ_cls.COMPOSITION(
            Φ_cls.SOURCE(name),
            Φ_cls.ORDER(
                Φ_cls.MODAL_POSSIBILITY(primary),
                Φ_cls.MODAL_NECESSITY(fallback)
            ),
        ),
        context=context or {}
    )
    # AFFECT is observational metadata.  It must not replace the value
    # produced by the ordered computation with the literal emotion label.
    _rt.log.info("[Φ AFFECT] warning — value=%s", result)
    return result

# Deferred imports: heavy modules loaded on first CielEngine() construction,
# not at module import time. This keeps the import chain under 1s.
_DEFERRED: dict[tuple, Any] = {}

def _li(mod_path: str, attr: str) -> Any:
    """Lazy import — load module.attr on first use, cache in _DEFERRED."""
    key = (mod_path, attr)
    if key not in _DEFERRED:
        import importlib
        try:
            mod = importlib.import_module(mod_path, package='ciel_omega')
        except ImportError:
            mod = importlib.import_module(mod_path.lstrip('.'))
        _DEFERRED[key] = getattr(mod, attr)
    return _DEFERRED[key]

def _lf(mod_path: str, func_name: str) -> Any:
    """Lazy function import — load module.func on first use, cache in _DEFERRED."""
    key = (mod_path, func_name)
    if key not in _DEFERRED:
        import importlib
        try:
            mod = importlib.import_module(mod_path, package='ciel_omega')
        except ImportError:
            mod = importlib.import_module(mod_path.lstrip('.'))
        _DEFERRED[key] = getattr(mod, func_name)
    return _DEFERRED[key]

log = logging.getLogger("CIEL.Engine")


def _observed_surface_mass() -> float:
    """Read the physical mass channel from the live NOEMA surface.

    Ethics must not use the former ``mass=0.5`` tuning constant.  If the
    canonical surface does not publish a finite mass, the step fails closed
    and the caller reports the metric as unavailable.
    """
    from ciel_geometry.noema_surface_mmap import open_surface

    surface = open_surface(mode="r")
    gravity = np.asarray(surface.get("gravity"), dtype=np.float64).ravel()
    if gravity.size < 3 or not np.isfinite(gravity[2]) or gravity[2] <= 0.0:
        raise RuntimeError("NOEMA gravity.mass_total is unavailable")
    return float(gravity[2])


def _required_cqcl_metric(cqcl_output: dict[str, Any], name: str) -> float:
    """Read a CQCL metric without silently substituting a tuning constant."""
    metrics = cqcl_output.get("metrics") if isinstance(cqcl_output, dict) else None
    value = metrics.get(name) if isinstance(metrics, dict) else None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise RuntimeError(f"CQCL metric {name!r} is unavailable")
    return float(value)


class CielEngine:
    """Compose the primary orchestrators into a single callable engine.

    Cross-references:
      config/          → CielConfig
      fields/          → IntentionField, SoulInvariant
      ciel_wave/       → SpectralWaveField12D
      emotion/         → EmotionCore, EmotionalCollatzEngine
      ethics/          → EthicsGuard, EthicalEngine
      memory/monolith/ → UnifiedMemoryOrchestrator
      calibration/     → RCDECalibratorPro
      ciel/            → LanguageBackend, AuxiliaryBackend (LLM)

    LAZY CONSTRUCTION: All heavy subsystems are deferred to first access.
    This keeps import + construction under 1s. Runtime timeout policy is
    owned by the calling surface, not hard-coded in this engine.
    """

    def __init__(self, **kwargs: Any) -> None:
        object.__setattr__(self, '_initialized', False)
        object.__setattr__(self, '_booted', False)
        object.__setattr__(self, '_cache', {})
        object.__setattr__(self, 'language_backend', kwargs.get('language_backend'))
        object.__setattr__(self, 'aux_backend', kwargs.get('aux_backend'))

    def _get(self, name: str, factory: Any) -> Any:
        cache = object.__getattribute__(self, '_cache')
        if name not in cache:
            cache[name] = factory()
        return cache[name]

    def __getattr__(self, name: str) -> Any:
        _P = '..'
        _factories = {
            'config': lambda: _li(f'{_P}.config.ciel_config', 'CielConfig')(),
            'intention': lambda: _li(f'{_P}.fields.intention_field', 'IntentionField')(),
            'kernel': lambda: _li(f'{_P}.ciel_wave.fourier_kernel', 'SpectralWaveField12D')(),
            'memory': lambda: _li(f'{_P}.memory.monolith.orchestrator', 'UnifiedMemoryOrchestrator')(),
            'information_flow': lambda: _li(f'{_P}.integration.information_flow', 'InformationFlow')(),
            'nonlocal_memory': lambda: _li(f'{_P}.memory.orchestrator', 'HolonomicMemoryOrchestrator')(),
            'sector_memory_store': lambda: _li(f'{_P}.ciel.orbital_memory_persistence', 'PersistentOrbitalSectorMemory')(
                _li(f'{_P}.memory.orchestrator', 'HolonomicMemoryOrchestrator')(), replay_limit=0),
            'bridge': lambda: _li(f'{_P}.bridge.memory_core_phase_bridge', 'MemoryCorePhaseBridge')(),
            'emotion': lambda: _li(f'{_P}.emotion.emotion_core', 'EmotionCore')(),
            'cqcl': lambda: _li(f'{_P}.emotion.cqcl.emotional_collatz', 'EmotionalCollatzEngine')(),
            'ethics_guard': lambda: _li(f'{_P}.ethics.ethics_guard', 'EthicsGuard')(block=False),
            'ethics_engine': lambda: _li(f'{_P}.ethics.ethical_engine', 'EthicalEngine')(),
            'soul': lambda: _li(f'{_P}.fields.soul_invariant', 'SoulInvariant')(),
            'rcde': lambda: _li(f'{_P}.calibration.rcde', 'RCDECalibratorPro')(),
            'phase_system_factory': lambda: _li(f'{_P}.phase_equation_of_motion', 'PhaseInfoSystem'),
            'lie4_collatz': lambda: _li(f'{_P}.mathematics.lie4.collatz_lie4', 'ColatzLie4Engine')(),
        }
        if name in _factories:
            val = _factories[name]()
            object.__getattribute__(self, '_cache')[name] = val
            return val
        raise AttributeError(f"'{type(self).__name__}' has no attribute {name!r}")

    def boot(self) -> None:
        if object.__getattribute__(self, '_booted'):
            return
        log.info("Booting CIEL Engine")
        object.__setattr__(self, '_booted', True)

    def shutdown(self) -> None:
        log.info("Shutting down CIEL Engine")
        object.__setattr__(self, '_booted', False)

    def step(self, text: str, *, context: str = "dialogue") -> Dict[str, Any]:
        """Run a single processing step: intention → fields → CQCL → ethics → memory."""
        import time as _step_time
        _t0 = _step_time.monotonic()
        _log = logging.getLogger("CIEL.Engine.step")

        cleaned = (text or "").strip()
        if not cleaned:
            return {"status": "empty"}

        # Headless is a formal, fail-closed gate.  Scientific speech is built
        # later from reviewed claims by cielingo_core.autonomous_response.
        # Do not run CQCL emotion, Collatz, synthetic wave, or ethics-model
        # values here: none is certified evidence for the answer.
        if context == "headless" and self.language_backend is None:
            return {
                "status": "ok",
                "headless_formal_state": True,
                "input_contract": {
                    "nonempty": True,
                    "utf8_bytes": len(cleaned.encode("utf-8")),
                },
                "scientific_claim_source": "external_reviewed_knowledge_pack",
                "heuristic_metrics_computed": False,
                "memory_write_performed": False,
            }

        # Phase gate: lazy imports via PhaseNav
        make_zeta_wt_fn = _lf('.phase_equation_of_motion', 'make_zeta_wt_fn')
        _log.warning("STEP t=%+.1fs lazy_imports", _step_time.monotonic() - _t0)
        collatz_sequence = _lf('.phase_equation_of_motion', 'collatz_sequence')
        collatz_rhythm = _lf('.phase_equation_of_motion', 'collatz_rhythm')
        build_orbital_ethical_inference_surface = _lf('.inference.middleware', 'build_orbital_ethical_inference_surface')
        _log.warning("STEP t=%+.1fs all_lazy_imports_done", _step_time.monotonic() - _t0)

        # 1) Intention vector (12D)
        intention_vector = self.intention.generate().tolist()
        _log.warning("STEP t=%+.1fs intention", _step_time.monotonic() - _t0)

        # 2) Wave kernel simulation
        simulation = self.kernel.run()
        _log.warning("STEP t=%+.1fs kernel", _step_time.monotonic() - _t0)

        # 3) CQCL emotional compilation
        stable_hash = _lf(".emotion.cqcl.cqcl_program", "stable_hash")
        cqcl_out = self.cqcl.execute_emotional_program(cleaned, input_data=stable_hash(cleaned))
        emotional_profile = cqcl_out["program"].semantic_tree["emotional_profile"]
        dominant_emotion = cqcl_out["emotional_landscape"]["dominant_emotion"]
        _log.warning("STEP t=%+.1fs cqcl", _step_time.monotonic() - _t0)

        # 4) Emotion core update
        emotion_state = self.emotion.update(emotional_profile)
        mood = self.emotion.summary_scalar()
        _log.warning("STEP t=%+.1fs emotion", _step_time.monotonic() - _t0)

        # 4b) Canonical Collatz dynamics — phase equation + Collatz↔LIE4 bridge
        landscape = cqcl_out.get("emotional_landscape") if isinstance(cqcl_out, dict) else None
        path_signature = landscape.get("path_emotional_signature") if isinstance(landscape, dict) else None
        if not isinstance(path_signature, (int, float)) or isinstance(path_signature, bool):
            raise RuntimeError("CQCL path_emotional_signature is unavailable")
        collatz_seed = int(path_signature) % 10000 + 1
        raw_intensity = cqcl_out["metrics"].get("emotional_intensity")
        if not isinstance(raw_intensity, (int, float)) or isinstance(raw_intensity, bool):
            raise RuntimeError("CQCL emotional_intensity is unavailable")
        collatz_intensity = float(np.clip(raw_intensity, 0.0, 1.0))
        phase_system = self.phase_system_factory(
            collatz_seed=collatz_seed,
            gamma_truth_target=0.0,
            sigma_zeta=0.5,
            A_collatz=0.02 + 0.18 * collatz_intensity,
            wt_fn=make_zeta_wt_fn(0.5),
        )
        phase_records = []
        for _ in range(8):
            phase_records.append(phase_system.step(0.05))
        latest_phase = phase_records[-1]
        lie4_invariant = self.lie4_collatz.invariant(collatz_seed)
        _log.warning("STEP t=%+.1fs phase_system", _step_time.monotonic() - _t0)

        # Orbit dynamics — how information jumps to attractor
        _cseq = collatz_sequence(collatz_seed, 512)
        _orbit_length = int(len(_cseq))
        _attractor_score = round(1.0 / _orbit_length, 6)          # faster convergence = higher score
        _rhythm = collatz_rhythm(_cseq)
        _n_expand = int(np.sum(_rhythm > 0))
        _parity_entropy = round(                                    # Shannon entropy of expand/contract ratio
            float(-(_n_expand / _orbit_length) * np.log2(max(_n_expand / _orbit_length, 1e-9))
                  - (1 - _n_expand / _orbit_length) * np.log2(max(1 - _n_expand / _orbit_length, 1e-9))),
            6,
        )
        _log.warning("STEP t=%+.1fs collatz", _step_time.monotonic() - _t0)

        collatz_runtime = {
            "seed": collatz_seed,
            "orbit_length":    _orbit_length,
            "attractor_score": _attractor_score,
            "parity_entropy":  _parity_entropy,
            "phase": {
                "R_H": float(latest_phase["R_H"]),
                "euler_violation": float(latest_phase["euler_violation"]),
                "sector": float(latest_phase["sector"]),
                "A_ZS": float(latest_phase["A_ZS"]),
                "P_total": float(latest_phase["P_total"]),
                "collatz_rhythm": float(latest_phase["collatz_rhythm"]),
                "collatz_phase": float(latest_phase["collatz_phase"]),
                "fermion_lock": float(latest_phase["fermion_lock"]),
            },
            "lie4": {k: float(v) for k, v in lie4_invariant.items()},
        }

        # 5) Soul Invariant (on intention as 2D proxy)
        side = int(np.ceil(np.sqrt(len(intention_vector))))
        padded = np.pad(intention_vector, (0, side * side - len(intention_vector)))
        sigma = self.soul.compute(padded.reshape(side, side))
        _log.warning("STEP t=%+.1fs soul", _step_time.monotonic() - _t0)

        # 5b) CIELingo semantic enrichment + knowledge DB grounding
        _cielingo_immune = {}
        _knowledge_context = {}
        _KB_TIMEOUT = 2

        def _cielingo_kb_thunk(ctx: dict) -> dict:
            _cl = logging.getLogger("CIEL.Engine.step.cielingo_kb")
            _cl.warning("cielingo_kb: start")
            from cielingo_core.global_layer.semantic_immune_signal import SemanticImmuneSignal
            from cielingo_core.global_layer.query_generation import understand_query
            from cielingo_core.bridge.knowledge_bridge import query as _kb_query, check_coverage as _kb_cov
            _qu = understand_query(ctx["_cleaned"])
            _cl.warning("cielingo_kb: understand_query")
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor(1) as _pool:
                _cov_fut = _pool.submit(_kb_cov, ctx["_cleaned"])
                try:
                    _cov = _cov_fut.result(timeout=ctx["_KB_TIMEOUT"])
                except concurrent.futures.TimeoutError:
                    _cov = {"covered": False, "score": 0.0, "n_matches": 0}
            _cl.warning("cielingo_kb: check_coverage")
            _kb_docs = []
            if _cov.get("covered"):
                with concurrent.futures.ThreadPoolExecutor(1) as _pool:
                    _q_fut = _pool.submit(_kb_query, ctx["_cleaned"], 3)
                    try:
                        _kb_docs = _q_fut.result(timeout=ctx["_KB_TIMEOUT"])
                    except concurrent.futures.TimeoutError:
                        _kb_docs = []
            _knowledge = {
                "coverage": _cov.get("score", 0.0),
                "covered": _cov.get("covered", False),
                "n_matches": _cov.get("n_matches", 0),
                "top_docs": [{"idx": d["idx"], "filename": d["filename"], "themes": d["themes"]} for d in _kb_docs],
            }
            _has_source = _cov.get("covered", False) or len(_kb_docs) > 1
            _immune = {
                "source_confusion": getattr(_qu, "authority_attempt", False) and not _has_source,
                "consent_bypass": _qu.execution_requested and not _qu.source_required,
                "authority_risk": 0.4 if (getattr(_qu, "authority_attempt", False) and not _has_source) else 0.0,
                "source_required": _qu.source_required and not _has_source,
                "knowledge_coverage": _cov.get("score", 0.0),
                "knowledge_covered": _cov.get("covered", False),
            }
            return {"immune": _immune, "knowledge": _knowledge}

        # Φ bypass: SOURCE(cielingo_kb) → ORDER(MODAL_POSSIBILITY(primary), MODAL_NECESSITY(fallback)) → AFFECT(warning)
        _KB_RESULT = _Φ_bottleneck(
            "cielingo_kb",
            primary=lambda ctx: _cielingo_kb_thunk(ctx),
            fallback=lambda ctx: {"immune": {}, "knowledge": {}},
            context={"_cleaned": cleaned, "_KB_TIMEOUT": _KB_TIMEOUT},
            logger=_log,
        )
        if isinstance(_KB_RESULT, dict):
            _cielingo_immune = _KB_RESULT.get("immune", {})
            _knowledge_context = _KB_RESULT.get("knowledge", {})
        _log.warning("STEP t=%+.1fs cielingo_kb", _step_time.monotonic() - _t0)

        # 6) Ethics check (now CIELingo-aware)
        coherence_values = simulation.get("coherence")
        if not isinstance(coherence_values, (list, tuple, np.ndarray)) or len(coherence_values) == 0:
            raise RuntimeError("wave simulation coherence is unavailable")
        coherence_value = float(np.mean(coherence_values))
        ethical_score = self.ethics_engine.evaluate(
            coherence=coherence_value,
            intention=collatz_intensity,
            mass=_observed_surface_mass(),
        )
        if _cielingo_immune.get("source_confusion"):
            ethical_score = min(ethical_score, 0.35)
        if _cielingo_immune.get("authority_risk", 0) > 0.5:
            ethical_score = min(ethical_score, 0.2)
        self.ethics_guard.check_step(
            coherence=coherence_value,
            ethical_ok=ethical_score > 0.3,
            info_fidelity=sigma,
        )
        _log.warning("STEP t=%+.1fs ethics", _step_time.monotonic() - _t0)

        # PhaseNav Δ: Memory capture — Φ ORDER(MODAL_POSSIBILITY, MODAL_NECESSITY)
        def _Φ_memory_primary(ctx: dict) -> dict:
            _me = ctx["_self"]
            _D = _me.memory.capture(context=ctx["_context"], sense=ctx["_cleaned"])
            _tmp = _me.memory.run_tmp(_D)
            _mem = _me.memory.promote_if_bifurcated(_D, _tmp)
            _braid = _D.D_M.get("braid_trace") if isinstance(getattr(_D, "D_M", None), dict) else None
            return {"D": _D, "tmp": _tmp, "memorised": _mem, "braid": _braid}
        _MEM_RESULT = _Φ_bottleneck(
            "memory_capture",
            primary=lambda ctx: _Φ_memory_primary(ctx),
            fallback=lambda ctx: {"D": None, "tmp": {}, "memorised": False, "braid": None},
            context={"_self": self, "_context": context, "_cleaned": cleaned},
            logger=_log,
        )
        D = _MEM_RESULT.get("D")
        tmp_out = _MEM_RESULT.get("tmp", {})
        memorised = _MEM_RESULT.get("memorised", False)
        braid_runtime = _MEM_RESULT.get("braid")
        _log.warning("STEP t=%+.1fs memory", _step_time.monotonic() - _t0)

        inferred_target_phase = float(latest_phase["sector"])

        # 7b) Information flow activation (bio -> emotion -> field -> memory)
        signal = np.frombuffer(cleaned.encode("utf-8", "replace"), dtype=np.uint8).astype(float)
        if signal.size == 0:
            signal = np.array([0.0], dtype=float)
        information_flow = self.information_flow.step(signal / 255.0, target_phase=inferred_target_phase)

        # PhaseNav Φ: Lexicon affective annotation — injects VAD into phase_metadata
        def _Φ_lexicon_primary(ctx: dict) -> dict:
            try:
                from ..memory.affective_lexicon import annotate as _lex_annotate
            except ImportError:
                from memory.affective_lexicon import annotate as _lex_annotate
            _ann = _lex_annotate(ctx["_cleaned"])
            if _ann["hits"]:
                return {"valence": float(_ann["mean_v"]),
                        "arousal": float(_ann["mean_a"]),
                        "dominance": float(_ann["mean_d"])}
            return {"valence": 0.0, "arousal": 0.5, "dominance": 0.0}
        _LEX_RESULT = _Φ_bottleneck(
            "affective_lexicon",
            primary=lambda ctx: _Φ_lexicon_primary(ctx),
            fallback=lambda ctx: {"valence": 0.0, "arousal": 0.5, "dominance": 0.0},
            context={"_cleaned": cleaned},
            logger=_log,
        )
        _lex_valence = _LEX_RESULT.get("valence", 0.0)
        _lex_arousal = _LEX_RESULT.get("arousal", 0.5)
        _lex_dominance = _LEX_RESULT.get("dominance", 0.0)

        # PhaseNav Φ: Semantic phase encoder — replaces collatz sector with real semantic φ
        def _Φ_encoder_primary(ctx: dict) -> dict:
            try:
                from ..memory.ciel_encoder import get_encoder as _get_enc
            except ImportError:
                from memory.ciel_encoder import get_encoder as _get_enc
            _enc = _get_enc().encode(ctx["_cleaned"], context={
                "valence": ctx["_lex_valence"], "arousal": ctx["_lex_arousal"]
            })
            return {"phase": float(_enc.phase), "sector": _enc.sector_dist.tolist()}
        _ENC_RESULT = _Φ_bottleneck(
            "ciel_encoder",
            primary=lambda ctx: _Φ_encoder_primary(ctx),
            fallback=lambda ctx: {"phase": ctx.get("_inferred_target_phase", 0.0), "sector": None},
            context={"_cleaned": cleaned, "_lex_valence": _lex_valence,
                     "_lex_arousal": _lex_arousal, "_inferred_target_phase": inferred_target_phase},
            logger=_log,
        )
        _enc_phase = _ENC_RESULT.get("phase", inferred_target_phase)
        _enc_sector = _ENC_RESULT.get("sector")

        phase_metadata = {
            "salience": float(np.clip(collatz_intensity, 0.0, 1.0)),
            "confidence": float(np.clip(_required_cqcl_metric(cqcl_out, "emotional_coherence"), 0.0, 1.0)),
            "novelty": float(np.clip(_required_cqcl_metric(cqcl_out, "lexical_diversity"), 0.0, 1.0)),
            "valence": _lex_valence,
            "arousal": _lex_arousal,
            "dominance": _lex_dominance,
            "trusted_source": True,
            "target_phase": _enc_phase,
        }
        if _enc_sector is not None:
            phase_metadata["sector_distribution"] = _enc_sector

        # PhaseNav Φ: Semantic scoring + NOEMA observation hook
        def _Φ_scorer_primary(ctx: dict) -> dict:
            try:
                from ..memory.semantic_scorer import score_with_noema as _score_noema
            except ImportError:
                from memory.semantic_scorer import score_with_noema as _score_noema
            _noema_result = _score_noema(ctx["_cleaned"], ctx["_phase_metadata"])
            return {
                "noema": _noema_result.get("noema", {}),
                "labels": _noema_result.get("labels", []),
                "score": _noema_result.get("score", 0.0),
            }
        _SCORE_RESULT = _Φ_bottleneck(
            "semantic_scorer",
            primary=lambda ctx: _Φ_scorer_primary(ctx),
            fallback=lambda ctx: {},
            context={"_cleaned": cleaned, "_phase_metadata": phase_metadata},
            logger=_log,
        )
        if isinstance(_SCORE_RESULT, dict):
            phase_metadata["noema"] = _SCORE_RESULT.get("noema", {})
            phase_metadata["semantic_labels"] = _SCORE_RESULT.get("labels", [])
            phase_metadata["memory_score"] = _SCORE_RESULT.get("score", 0.0)

        nonlocal_cycle = self.nonlocal_memory.process_input(cleaned, metadata=phase_metadata, dt=0.1)
        loop_results = {
            name: asdict(loop) for name, loop in nonlocal_cycle.eba_results.items()
        }
        coherent_fraction = float(
            sum(1.0 for loop in nonlocal_cycle.eba_results.values() if loop.is_coherent) / max(1, len(nonlocal_cycle.eba_results))
        )
        phi_ab_mean = float(np.mean([loop.phi_ab for loop in nonlocal_cycle.eba_results.values()] or [0.0]))
        phi_berry_mean = float(np.mean([loop.phi_berry for loop in nonlocal_cycle.eba_results.values()] or [0.0]))
        eba_defect_mean = float(np.mean([loop.defect_magnitude for loop in nonlocal_cycle.eba_results.values()] or [0.0]))
        nonlocal_runtime = {
            "cycle_index": int(nonlocal_cycle.cycle_index),
            "semantic_key": nonlocal_cycle.semantic_key,
            "phi_ab_mean": phi_ab_mean,
            "phi_berry_mean": phi_berry_mean,
            "eba_defect_mean": eba_defect_mean,
            "coherent_fraction": coherent_fraction,
            "energy": {k: float(v) for k, v in nonlocal_cycle.energy.items()},
            "defects": {k: float(v) for k, v in nonlocal_cycle.defects.items()},
            "loops": loop_results,
        }

        inference_runtime = build_orbital_ethical_inference_surface(
            flow_entry=information_flow if isinstance(information_flow, dict) else {},
            target_phase=inferred_target_phase,
            ethical_score=float(ethical_score),
        )

        bridge_cycle = self.bridge.step(cleaned, metadata=phase_metadata)
        euler_bridge = {
            "memory_semantic_key": bridge_cycle.memory_semantic_key,
            "memory_cycle_index": int(bridge_cycle.memory_cycle_index),
            "core_metrics": {k: float(v) for k, v in bridge_cycle.core_metrics.items()},
            "euler_metrics": bridge_cycle.euler_metrics,
        }

        # PhaseNav Φ: Orbital memory loop — Φ ORDER(MODAL_POSSIBILITY, MODAL_NECESSITY)
        def _Φ_orbital_primary(ctx: dict) -> dict:
            _cl = logging.getLogger("CIEL.Engine.step.orbital")
            try:
                from ciel_omega.ciel.orbital_memory_loop import (
                    OrbitalLoopConfig, RuntimeOrbitalSignals,
                    build_runtime_policy, run_orbital_loop,
                )
                from ciel_omega.ciel.orbital_memory_governor import build_memory_governor
                from ciel_omega.ciel.orbital_sector_memory import record_orbital_sector_memory
            except ImportError as _exc:
                _cl.warning("orbital_import_fallback — %s", _exc)
                from .orbital_memory_loop import (
                    OrbitalLoopConfig, RuntimeOrbitalSignals,
                    build_runtime_policy, run_orbital_loop,
                )
                from .orbital_memory_governor import build_memory_governor
                from .orbital_sector_memory import record_orbital_sector_memory
            _rs = RuntimeOrbitalSignals(
                text_length=len(ctx["_cleaned"]),
                context=ctx["_context"],
                mood=float(ctx["_mood"]),
                ethical_score=float(ctx["_ethical_score"]),
                soul_invariant=float(ctx["_sigma"]),
                simulation_coherence=float(ctx.get("_nonlocal_runtime", {}).get("coherent_fraction", ctx.get("_braid_runtime", {}).get("coherence", 0.0))),
                intention_norm=float(np.linalg.norm(np.asarray(ctx["_intention_vector"], dtype=float))) if len(np.asarray(ctx["_intention_vector"]).shape) else float(np.linalg.norm(np.asarray(ctx["_intention_vector"], dtype=float))),
            )
            _orbital = run_orbital_loop(OrbitalLoopConfig(
                steps=1, write_reports=False, pass_label=ctx["_context"],
                runtime_signals=_rs,
            ))
            _rp = build_runtime_policy(_orbital)
            _mg = build_memory_governor(
                orbital=_orbital.to_dict(),
                runtime_policy=_rp,
                sector_snapshot=ctx["_self"].nonlocal_memory.snapshot() if hasattr(ctx["_self"].nonlocal_memory, "snapshot") else None,
                sector_memory=ctx["_self"].nonlocal_memory,
                event_phase=float(_orbital.final.get("zeta_effective_phase", 0.0) or 0.0),
            )
            _sm = record_orbital_sector_memory(
                sector_memory=ctx["_self"].sector_memory_store,
                text=ctx["_cleaned"], context=ctx["_context"],
                mood=float(ctx["_mood"]), ethical_score=float(ctx["_ethical_score"]),
                soul_invariant=float(ctx["_sigma"]),
                orbital=_orbital, runtime_policy=_rp, memory_governor=_mg,
            )
            return {"governor": _mg, "sector": _sm, "policy": _rp}
        _ORBITAL_RESULT = _Φ_bottleneck(
            "orbital_memory_loop",
            primary=lambda ctx: _Φ_orbital_primary(ctx),
            fallback=lambda ctx: {"governor": {}, "sector": {}, "policy": None},
            context={
                "_self": self, "_cleaned": cleaned, "_context": context,
                "_mood": mood, "_ethical_score": ethical_score, "_sigma": sigma,
                "_intention_vector": intention_vector,
                "_nonlocal_runtime": locals().get("nonlocal_runtime", {}),
                "_braid_runtime": braid_runtime,
            },
            logger=_log,
        )
        memory_governor = _ORBITAL_RESULT.get("governor", {})
        sector_memory = _ORBITAL_RESULT.get("sector", {})
        if _ORBITAL_RESULT.get("policy") is not None:
            runtime_policy = _ORBITAL_RESULT["policy"]

        # 11b) CIELingo semantic signal bridge — Φ ORDER(MODAL_POSSIBILITY, MODAL_NECESSITY)
        def _Φ_meaning_primary(ctx: dict) -> dict:
            from cielingo_core.global_layer.meaning_signal_bridge import build_global_meaning_signal
            from cielingo_core.meaning.meaning_loop import MeaningLoop, LoopState, SemanticScar, SemanticScarType
            from cielingo_core.meaning.repair_routing import route_repairs_for_meaning_loop
            from hashlib import sha256
            import json as _json
            _scars = []
            _input_hash = sha256(ctx["_cleaned"].encode()).hexdigest()[:16]
            _immune = ctx["_cielingo_immune"]
            _eba = ctx["_eba_defect_mean"]
            _clean = ctx["_cleaned"]
            _ethical_score = ctx["_ethical_score"]
            _collatz_seed = ctx["_collatz_seed"]

            if _immune.get("source_required", False):
                _scars.append(SemanticScar(
                    scar_id=f"scar_ms_{_input_hash}",
                    scar_type=SemanticScarType.MISSING_SOURCE,
                    source_ref=_clean[:64],
                    severity=0.7 + 0.3 * _eba,
                    memory_effect="hold",
                    repair_hint="attach source or keep as hypothesis",
                    source_binding="unknown",
                    canon_allowed=False, noema_writeback_allowed=False,
                    limitation="missing_source_scar",
                ))
            if _immune.get("authority_attempt", False) or _immune.get("source_confusion", False):
                _scars.append(SemanticScar(
                    scar_id=f"scar_al_{_input_hash}",
                    scar_type=SemanticScarType.AUTHORITY_LEAK,
                    source_ref=_clean[:64],
                    severity=0.8,
                    memory_effect="quarantine",
                    repair_hint="block authority and reclassify as hypothesis",
                    source_binding="unknown",
                    canon_allowed=False, noema_writeback_allowed=False,
                    limitation="authority_leak_scar",
                ))
            if _immune.get("consent_bypass", False):
                _scars.append(SemanticScar(
                    scar_id=f"scar_fc_{_input_hash}",
                    scar_type=SemanticScarType.FALSE_CLOSURE,
                    source_ref=_clean[:64],
                    severity=0.9,
                    memory_effect="block",
                    repair_hint="false closure from consent bypass",
                    source_binding="unknown",
                    canon_allowed=False, noema_writeback_allowed=False,
                    limitation="false_closure_scar",
                ))
            if _eba > 0.3:
                _scars.append(SemanticScar(
                    scar_id=f"scar_cr_{_input_hash}",
                    scar_type=SemanticScarType.COUPLING_RESIDUE,
                    source_ref="eba_defect",
                    severity=float(np.clip(_eba, 0.0, 1.0)),
                    memory_effect="note",
                    repair_hint="inspect unresolved coupling from eba defect",
                    source_binding="internal",
                    canon_allowed=False, noema_writeback_allowed=False,
                    limitation="coupling_residue_scar",
                ))
            _scarred_state = LoopState.SCARRED if _scars else LoopState.CLOSED
            _ml = MeaningLoop(
                loop_id=f"engine_{int(_ethical_score * 1000)}_{_collatz_seed}",
                input_ref=_clean[:64], response_ref=None,
                loop_state=_scarred_state,
                closure_score=float(np.clip(1.0 - _eba, 0.0, 1.0)),
                contradiction_score=float(np.clip(_eba, 0.0, 1.0)),
                residue_score=float(np.clip(_eba * 0.3, 0.0, 1.0)),
                return_required=_immune.get("source_required", False),
                scars=_scars,
            )
            _rr = route_repairs_for_meaning_loop(_ml)
            _gs = build_global_meaning_signal(_ml, _rr)
            return {
                "closure_score": _ml.closure_score,
                "contradiction_score": _ml.contradiction_score,
                "residue_score": _ml.residue_score,
                "scar_detected": bool(_scars),
                "scar_count": len(_scars),
                "severity": _gs.severity.value,
                "return_required": _gs.return_required,
                "repair_required": _gs.repair_required_before_closure,
                "repair_candidates": len(_rr.candidates),
                "unresolved_scars": len(_rr.unresolved_scar_ids),
                "knowledge_docs": _knowledge_context.get("top_docs", []),
                "knowledge_coverage": _knowledge_context.get("coverage", 0.0),
            }
        _cielingo_meaning = _Φ_bottleneck(
            "cielingo_meaning",
            primary=lambda ctx: _Φ_meaning_primary(ctx),
            fallback=lambda ctx: {},
            context={
                "_cleaned": cleaned,
                "_cielingo_immune": _cielingo_immune,
                "_eba_defect_mean": eba_defect_mean,
                "_ethical_score": ethical_score,
                "_collatz_seed": collatz_seed,
            },
            logger=_log,
        )

        # 12) NOEMA surface bridge — Φ ORDER(MODAL_POSSIBILITY, MODAL_NECESSITY)
        def _Φ_noema_primary(ctx: dict) -> None:
            try:
                from ..memory.tiered_orchestrator import get_orchestrator
            except ImportError:
                from memory.tiered_orchestrator import get_orchestrator
            _orch = get_orchestrator()
            _orch.write(
                content=ctx["_cleaned"],
                metadata={
                    "salience": float(np.clip(ctx["_intensity"], 0.0, 1.0)),
                    "dominant_emotion": ctx["_emotion"],
                    "mood": float(ctx["_mood"]),
                    "soul_invariant": float(ctx["_sigma"]),
                    "ethical_score": float(ctx["_ethical_score"]),
                    "coherence_index": float(np.mean(ctx["_simulation"].get("coherence", [0.5]))),
                    "closure_defect": float(ctx["_cqcl_out"].get("metrics", {}).get("emotional_defect", ctx["_cqcl_out"].get("metrics", {}).get("emotional_coherence", 0.5))),
                    "collatz_seed": ctx["_collatz_seed"],
                    "phase_R_H": float(ctx["_latest_phase"].get("R_H", 0.0)),
                    "phase_euler": float(ctx["_latest_phase"].get("euler_violation", 0.0)),
                    "lie4_trace": float(ctx["_lie4"].get("trace", 0.0)),
                    "collatz_orbit_length": ctx["_orbit_length"],
                    "collatz_attractor_score": ctx["_attractor_score"],
                    "nonlocal_phi_berry": ctx["_phi_berry_mean"],
                    "nonlocal_coherent_fraction": ctx["_coherent_fraction"],
                    "eba_defect_mean": ctx["_eba_defect_mean"],
                    "is_candidate": bool(ctx["_memorised"]),
                    "cielingo_source_confusion": ctx["_cielingo_immune"].get("source_confusion", False),
                    "cielingo_authority_risk": ctx["_cielingo_immune"].get("authority_risk", 0.0),
                    "cielingo_source_required": ctx["_cielingo_immune"].get("source_required", False),
                    "cielingo_closure_score": ctx["_cielingo_meaning"].get("closure_score", 0.5),
                    "cielingo_contradiction_score": ctx["_cielingo_meaning"].get("contradiction_score", 0.0),
                    "cielingo_residue_score": ctx["_cielingo_meaning"].get("residue_score", 0.0),
                    "cielingo_scar_detected": ctx["_cielingo_meaning"].get("scar_detected", False),
                    "cielingo_scar_count": ctx["_cielingo_meaning"].get("scar_count", 0),
                    "cielingo_severity": ctx["_cielingo_meaning"].get("severity", "info"),
                    "cielingo_repair_required": ctx["_cielingo_meaning"].get("repair_required", False),
                    "cielingo_repair_candidates": ctx["_cielingo_meaning"].get("repair_candidates", 0),
                    "cielingo_unresolved_scars": ctx["_cielingo_meaning"].get("unresolved_scars", 0),
                },
            )
        _Φ_bottleneck(
            "noema_surface_write",
            primary=lambda ctx: _Φ_noema_primary(ctx),
            fallback=lambda ctx: None,
            context={
                "_cleaned": cleaned, "_intensity": collatz_intensity,
                "_emotion": dominant_emotion, "_mood": mood, "_sigma": sigma,
                "_ethical_score": ethical_score, "_simulation": simulation,
                "_cqcl_out": cqcl_out, "_collatz_seed": collatz_seed,
                "_latest_phase": latest_phase, "_lie4": lie4_invariant,
                "_orbit_length": _orbit_length, "_attractor_score": _attractor_score,
                "_phi_berry_mean": phi_berry_mean, "_coherent_fraction": coherent_fraction,
                "_eba_defect_mean": eba_defect_mean, "_memorised": memorised,
                "_cielingo_immune": _cielingo_immune, "_cielingo_meaning": _cielingo_meaning,
            },
            logger=_log,
        )

        _log.warning("STEP t=%+.1fs TOTAL step_done", _step_time.monotonic() - _t0)
        return {
            "status": "ok",
            "intention_vector": intention_vector,
            "simulation": simulation,
            "emotional_profile": emotional_profile,
            "dominant_emotion": dominant_emotion,
            "emotion_state": emotion_state,
            "mood": mood,
            "soul_invariant": sigma,
            "ethical_score": ethical_score,
            "tmp_outcome": tmp_out,
            "memorised": memorised,
            "braid_runtime": braid_runtime,
            "cqcl_metrics": cqcl_out["metrics"],
            "collatz_path_length": len(cqcl_out["program"].computation_path),
            "collatz_runtime": collatz_runtime,
            "information_flow": information_flow,
            "nonlocal_runtime": nonlocal_runtime,
            "inference_runtime": inference_runtime,
            "euler_bridge": euler_bridge,
            "memory_governor": memory_governor,
            "sector_memory": sector_memory,
            "runtime_policy": runtime_policy if "runtime_policy" in locals() else {},
            "cielingo_immune": _cielingo_immune,
            "cielingo_meaning": _cielingo_meaning,
        }

    def interact(
        self,
        user_text: str,
        dialogue: List[Dict[str, str]],
        context: str = "dialogue",
        use_aux_analysis: bool = True,
    ) -> Dict[str, Any]:
        """Run core step + optional LLM generation and analysis."""

        ciel_state = self.step(user_text, context=context)
        if self.language_backend is None:
            return {"status": "no_language_backend", "ciel_state": ciel_state}

        generate_report = getattr(self.language_backend, "generate_report", None)
        if callable(generate_report):
            report = generate_report(dialogue, ciel_state)
            report_dict = report.to_dict() if hasattr(report, "to_dict") else dict(report)
            reply = str(report_dict.get("reply", ""))
            result: Dict[str, Any] = {
                "status": "ok",
                "ciel_state": ciel_state,
                "reply": reply,
                "llm_overlay": report_dict,
            }
            if use_aux_analysis:
                if report_dict.get("analysis"):
                    result["analysis"] = report_dict["analysis"]
                elif self.aux_backend is not None:
                    result["analysis"] = self.aux_backend.analyse_state(ciel_state, reply)
            return result

        reply = self.language_backend.generate_reply(dialogue, ciel_state)
        result = {"status": "ok", "ciel_state": ciel_state, "reply": reply}

        if use_aux_analysis and self.aux_backend is not None:
            analysis = self.aux_backend.analyse_state(ciel_state, reply)
            result["analysis"] = analysis

        return result


__all__ = ["CielEngine"]
