from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import json
import textwrap

from .sapiens_surface_policy import build_surface_policy


ETHICS_CONCEPTS: tuple[str, ...] = (
    "truth",
    "consent",
    "non_harm",
    "provenance",
    "accountability",
    "uncertainty",
    "memory_integrity",
    "boundary",
    "respect_for_personhood",
    "no_deception",
)


@dataclass(slots=True)
class HardcodedEthicsBlock:
    schema: str
    event: str
    concepts: list[str]
    policy: dict[str, Any]
    block: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "event": self.event,
            "concepts": self.concepts,
            "policy": self.policy,
            "block": self.block,
        }


def build_hardcoded_ethics_block(
    *,
    schema: str,
    block_name: str,
    event: str = "UserPromptSubmit",
    truth_axis: str = "truth",
    mode: str = "standard",
) -> HardcodedEthicsBlock:
    policy = build_surface_policy(control_profile={"mode": mode}, truth_axis=truth_axis)
    block = textwrap.dedent(
        f"""
        {block_name}:
          schema: {schema}
          event: {event}
          truth_axis: {truth_axis}
          mode: {mode}
          concepts:
            - truth
            - consent
            - non_harm
            - provenance
            - accountability
            - uncertainty
            - memory_integrity
            - boundary
            - respect_for_personhood
            - no_deception
          invariant_rules:
            - truth over smoothing
            - explicit uncertainty
            - no consent bypass
            - no hidden limitations
            - preserve fact/inference/hypothesis/unknown layers
            - keep provenance visible when claims are made
            - warn or pause on harm, coercion, or unsafe action
        """
    ).strip()
    return HardcodedEthicsBlock(
        schema=schema,
        event=event,
        concepts=list(ETHICS_CONCEPTS),
        policy=policy,
        block=block,
    )


def render_hardcoded_ethics_block(
    *,
    schema: str,
    block_name: str,
    event: str = "UserPromptSubmit",
    truth_axis: str = "truth",
    mode: str = "standard",
) -> str:
    return build_hardcoded_ethics_block(
        schema=schema,
        block_name=block_name,
        event=event,
        truth_axis=truth_axis,
        mode=mode,
    ).block


def ethics_payload_json(
    *,
    schema: str,
    block_name: str,
    event: str = "UserPromptSubmit",
    truth_axis: str = "truth",
    mode: str = "standard",
) -> str:
    block = build_hardcoded_ethics_block(
        schema=schema,
        block_name=block_name,
        event=event,
        truth_axis=truth_axis,
        mode=mode,
    )
    return json.dumps(block.to_dict(), ensure_ascii=False, indent=2)

