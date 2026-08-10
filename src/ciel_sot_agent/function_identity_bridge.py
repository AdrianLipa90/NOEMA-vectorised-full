"""Read-only bridge from derived function identities into NOEMA relational state."""
from __future__ import annotations

from ciel_geometry.phasenav.function_identity import FunctionIdentity
from ciel_geometry.phasenav.gate_contracts import EpistemicState, PhaseSpace, RelationalState


def function_identity_state(identity: FunctionIdentity) -> RelationalState:
    """Represent a derived function identity without fabricating PhaseNav coordinates.

    The invariant SHA is the relational identity. Different symbols that are
    proven aliases therefore resolve to the same identity. Source path and
    qualified symbol remain provenance/lineage, not identity primitives.
    """

    return RelationalState(
        identity=f"function:{identity.invariant_sha256}",
        kind="function_identity",
        phase36=None,
        phase_space=PhaseSpace.UNKNOWN,
        lineage=(identity.qualified_name,),
        relations=tuple(f"depends_on:{item}" for item in identity.dependency_symbols),
        provenance=(f"source:{identity.source_path}",),
        epistemic_state=EpistemicState.OBSERVATION,
        authority_state="DERIVED_STATIC_NO_AUTHORITY",
        lifecycle="OBSERVED",
        metadata={
            "module": identity.module,
            "symbol_name": identity.symbol_name,
            "qualified_name": identity.qualified_name,
            "normalized_ast_sha256": identity.normalized_ast_sha256,
            "invariant_sha256": identity.invariant_sha256,
            "phase_projection": "UNKNOWN_UNTIL_DERIVED",
        },
    )


__all__ = ["function_identity_state"]
