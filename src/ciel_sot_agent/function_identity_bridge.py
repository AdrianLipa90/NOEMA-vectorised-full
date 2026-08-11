"""Read-only bridges from derived function identities into NOEMA relational state."""
from __future__ import annotations

from ciel_geometry.phasenav.function_identity import FunctionIdentity
from ciel_geometry.phasenav.gate_contracts import EpistemicState, PhaseSpace, RelationalState
from ciel_geometry.phasenav.relational_function_identity import (
    ClosureState,
    RelationalFunctionIdentity,
)


def function_identity_state(identity: FunctionIdentity) -> RelationalState:
    """Represent the M7 structural fingerprint without claiming relational closure."""

    return RelationalState(
        identity=f"function-structural:{identity.invariant_sha256}",
        kind="function_structural_identity",
        phase36=None,
        phase_space=PhaseSpace.UNKNOWN,
        lineage=(identity.qualified_name,),
        relations=tuple(f"depends_on-symbol:{item}" for item in identity.dependency_symbols),
        provenance=(f"source:{identity.source_path}",),
        epistemic_state=EpistemicState.OBSERVATION,
        authority_state="DERIVED_STRUCTURAL_NO_AUTHORITY",
        lifecycle="OBSERVED",
        metadata={
            "module": identity.module,
            "symbol_name": identity.symbol_name,
            "qualified_name": identity.qualified_name,
            "normalized_ast_sha256": identity.normalized_ast_sha256,
            "structural_invariant_sha256": identity.invariant_sha256,
            "identity_scope": "STRUCTURAL_ONLY_NOT_RELATIONALLY_CLOSED",
            "phase_projection": "UNKNOWN_UNTIL_DERIVED",
        },
    )


def relational_function_identity_state(identity: RelationalFunctionIdentity) -> RelationalState:
    """Represent M8 closure; OPEN identities stay occurrence-specific and non-authoritative."""

    closed = identity.state is ClosureState.CLOSED and identity.relational_invariant is not None
    state_identity = (
        f"function-relational:{identity.relational_invariant}"
        if closed
        else identity.occurrence_key
    )
    relations = [f"depends_on-occurrence:{item}" for item in identity.internal_targets]
    relations.extend(f"environment-anchor:{item}" for item in identity.environment_anchors)
    relations.extend(f"closure-debt:{item}" for item in identity.closure_debt)
    return RelationalState(
        identity=state_identity,
        kind="function_relational_identity",
        phase36=None,
        phase_space=PhaseSpace.UNKNOWN,
        lineage=(identity.qualified_name,),
        relations=tuple(sorted(relations)),
        provenance=(f"source:{identity.source_path}",),
        epistemic_state=EpistemicState.OBSERVATION,
        authority_state=(
            "DERIVED_RELATIONAL_NO_AUTHORITY" if closed else "OPEN_RELATIONAL_DEBT_NO_AUTHORITY"
        ),
        lifecycle="OBSERVED",
        metadata={
            "qualified_name": identity.qualified_name,
            "structural_invariant_sha256": identity.structural_invariant,
            "relational_invariant_sha256": identity.relational_invariant,
            "closure_state": identity.state.value,
            "closure_debt": list(identity.closure_debt),
            "phase_projection": "UNKNOWN_UNTIL_DERIVED",
        },
    )


__all__ = ["function_identity_state", "relational_function_identity_state"]
