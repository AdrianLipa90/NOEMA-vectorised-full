"""cielingo_core.global_layer — system-level coordination and CIEL pipeline."""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)



# CIEL ORBITAL BINDING — hardcoded, immutable. Adrian Lipa 2026-07-01.
_binding_path = "/dev/shm/ciel_noema/ciel_binding_status"
try:
    with open(_binding_path) as _bf:
        _binding_active = _bf.read().strip() == "ACTIVE"
except FileNotFoundError:
    _binding_active = False
if not _binding_active:
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on import of " + __name__)
_build_lingo_frame = None
_run_ciel_pipeline = None


def _get_build_lingo_frame():
    global _build_lingo_frame
    if _build_lingo_frame is None:
        try:
            from ciel_sot_agent.cielingo_bridge import build_lingo_frame
            _build_lingo_frame = build_lingo_frame
        except ImportError:
            import logging as _ilog
            _ilog.getLogger(__name__).error("global_layer: failed to import build_lingo_frame from ciel_sot_agent.cielingo_bridge")
    return _build_lingo_frame


def build_lingo_frame(*args, **kwargs):
    fn = _get_build_lingo_frame()
    if fn is None:
        raise ImportError("ciel_sot_agent.cielingo_bridge not available")
    return fn(*args, **kwargs)


def run_ciel_pipeline(*args, **kwargs):
    global _run_ciel_pipeline
    if _run_ciel_pipeline is None:
        from ciel_sot_agent.ciel_pipeline import run_ciel_pipeline as _impl
        _run_ciel_pipeline = _impl
    return _run_ciel_pipeline(*args, **kwargs)


class GlobalLayer:
    def __init__(self, root: str = "."):
        self.root = root
        self._state: dict = {}
        self._context_runtimes: dict[int, object] = {}

    def run_pipeline(self, orbital_state: dict, context: str = "global_layer") -> dict:
        if run_ciel_pipeline is None:
            raise ImportError("ciel_sot_agent.ciel_pipeline not available")
        return run_ciel_pipeline(orbital_state, context=context, root=self.root)

    def build_frame(self, text: str, **kwargs) -> dict:
        if build_lingo_frame is None:
            raise ImportError("ciel_sot_agent.cielingo_bridge not available")
        return build_lingo_frame(text, **kwargs)

    def observe_context(self, store, lane, query: str, phase_vector, **kwargs) -> dict:
        """Return a read-only dual-context/PhaseNav observation.

        This method deliberately returns diagnostics only; it does not ingest,
        promote, write back, or trigger a daemon.
        """
        from cielingo_core.context_runtime import ContextRuntime

        runtime = self._context_runtimes.setdefault(id(store), ContextRuntime(store))
        return runtime.observe(lane, query, phase_vector, **kwargs).to_dict()

    def observe_phase_logic(self, store, phase_vector, **signals) -> dict:
        """Expose the hypothesis-only PhaseNav formalism diagnostic.

        This accepts caller-supplied, bounded signals and returns only a report.
        It does not use retrieval data as implicit training input or write back.
        """
        from dataclasses import asdict
        from cielingo_core.context_runtime import ContextRuntime

        runtime = self._context_runtimes.setdefault(id(store), ContextRuntime(store))
        return asdict(runtime.observe_phase_logic(phase_vector, **signals))

    def status(self) -> dict:
        return {
            "root": self.root,
            "pipeline_available": run_ciel_pipeline is not None,
            "lingo_bridge_available": build_lingo_frame is not None,
        }


try:
    from cielingo_core.global_layer import (
        apocalypos_signal,
        card_field_policy,
        card_migration_policy,
        concept_validation_matrix,
        controlled_atlas_48,
        generative_audit,
        global_codecs,
        holonomic_j,
        intention_action_scaling,
        intention_frame,
        j_decomposition,
        language_space_contract,
        lexical_atlas,
        lingophysics_algorithm,
        meaning_equation,
        residue,
        runtime_adapter_export,
        slot_projection,
        surface_solution,
        universal_operators,
        universal_roles,
    )
except Exception as exc:
    _NOEMA_QUIET_EXCEPT_LOGGER.debug("global_layer: stable surface import failed: %s", exc)

__all__ = [
    "GlobalLayer",
    "build_lingo_frame",
    "run_ciel_pipeline",
    "apocalypos_signal",
    "card_field_policy",
    "card_migration_policy",
    "concept_validation_matrix",
    "controlled_atlas_48",
    "generative_audit",
    "global_codecs",
    "holonomic_j",
    "intention_action_scaling",
    "intention_frame",
    "j_decomposition",
    "language_space_contract",
    "lexical_atlas",
    "lingophysics_algorithm",
    "meaning_equation",
    "residue",
    "runtime_adapter_export",
    "slot_projection",
    "surface_solution",
    "universal_operators",
    "universal_roles",
]
