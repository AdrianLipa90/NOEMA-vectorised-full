"""Hard contract guard for AI-SAPIENS interaction packets.

This module turns the relational-formal contract into executable checks.  It is
intentionally strict: missing truth discipline is a runtime error, not a note.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


EPISTEMIC_LAYERS = ("fact", "inference", "hypothesis", "unknown")


class ContractViolation(RuntimeError):
    """Raised when a packet or policy violates a required contract field."""


@dataclass(frozen=True)
class GuardResult:
    ok: bool
    checked: tuple[str, ...]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractViolation(message)


def validate_surface_policy(policy: Mapping[str, Any]) -> GuardResult:
    """Validate the SAPIENS surface policy contract.

    Required fields come from `governance/contracts/SAPIENS_PACKET_PROTOCOL.md`
    and the relational-formal AGENTS contract: truth over smoothing, explicit
    uncertainty, epistemic separation, distortion avoidance, and formal relation
    geometry.
    """
    _require(bool(policy.get("truth_over_smoothing")) is True, "truth_over_smoothing must be true")
    _require(bool(policy.get("explicit_uncertainty")) is True, "explicit_uncertainty must be true")
    _require(tuple(policy.get("epistemic_separation", ())) == EPISTEMIC_LAYERS,
             "epistemic_separation must be fact/inference/hypothesis/unknown")
    _require(bool(policy.get("relation_geometry_terms_formal")) is True,
             "relation_geometry_terms_formal must be true")
    _require(policy.get("response_axis") == "truth-aligned-user-intent",
             "response_axis must be truth-aligned-user-intent")

    distortion = policy.get("distortion_avoidance", {})
    _require(bool(distortion.get("no_hallucination")) is True, "no_hallucination must be true")
    _require(bool(distortion.get("no_unmarked_guessing")) is True, "no_unmarked_guessing must be true")
    _require(bool(distortion.get("no_hidden_limitations")) is True, "no_hidden_limitations must be true")
    _require(bool(distortion.get("no_softening_without_basis")) is True,
             "no_softening_without_basis must be true")

    formatting = policy.get("formatting_contract", {})
    for layer in EPISTEMIC_LAYERS:
        key = f"preserve_{layer}_layer"
        _require(bool(formatting.get(key)) is True, f"{key} must be true")

    return GuardResult(
        ok=True,
        checked=(
            "truth_over_smoothing",
            "explicit_uncertainty",
            "epistemic_separation",
            "distortion_avoidance",
            "relation_geometry_terms_formal",
            "response_axis",
            "formatting_contract",
        ),
    )


def validate_inference_contract(contract: Mapping[str, Any]) -> GuardResult:
    """Validate inference discipline carried by SAPIENS packets."""
    _require(bool(contract.get("relation_before_identity")) is True,
             "relation_before_identity must be true")
    _require(bool(contract.get("identity_before_memory")) is True,
             "identity_before_memory must be true")
    _require(contract.get("truth_axis") == "truth", "truth_axis must be truth")
    _require(tuple(contract.get("epistemic_separation", ())) == EPISTEMIC_LAYERS,
             "inference_contract epistemic separation is incomplete")
    _require("projection_required" in contract, "projection_required must be explicit")
    _require("private_state_export_allowed" in contract,
             "private_state_export_allowed must be explicit")
    return GuardResult(
        ok=True,
        checked=(
            "relation_before_identity",
            "identity_before_memory",
            "truth_axis",
            "epistemic_separation",
            "projection_required",
            "private_state_export_allowed",
        ),
    )


def validate_sapiens_packet(packet: Mapping[str, Any]) -> GuardResult:
    """Validate the complete AI-SAPIENS packet before it can be emitted."""
    _require("surface_policy" in packet, "packet is missing surface_policy")
    _require("inference_contract" in packet, "packet is missing inference_contract")
    validate_surface_policy(packet["surface_policy"])
    validate_inference_contract(packet["inference_contract"])
    return GuardResult(ok=True, checked=("surface_policy", "inference_contract"))
