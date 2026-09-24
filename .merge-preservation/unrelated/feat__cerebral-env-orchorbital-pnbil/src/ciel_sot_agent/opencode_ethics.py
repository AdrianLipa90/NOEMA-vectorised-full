from __future__ import annotations

ETHICS_SCHEMA = "ciel/opencode-ethics/v0.1"
from .ethics_core import (
    ETHICS_CONCEPTS,
    HardcodedEthicsBlock,
    ethics_payload_json as _ethics_payload_json,
    render_hardcoded_ethics_block,
    build_hardcoded_ethics_block,
)


def build_opencode_ethics_block(
    *,
    event: str = "UserPromptSubmit",
    truth_axis: str = "truth",
    mode: str = "standard",
) -> HardcodedEthicsBlock:
    return build_hardcoded_ethics_block(
        schema=ETHICS_SCHEMA,
        block_name="NOEMA_ETHICS_HARDCODED",
        event=event,
        truth_axis=truth_axis,
        mode=mode,
    )


def render_opencode_ethics_block(
    *,
    event: str = "UserPromptSubmit",
    truth_axis: str = "truth",
    mode: str = "standard",
) -> str:
    return render_hardcoded_ethics_block(
        schema=ETHICS_SCHEMA,
        block_name="NOEMA_ETHICS_HARDCODED",
        event=event,
        truth_axis=truth_axis,
        mode=mode,
    )


def ethics_payload_json(
    *,
    event: str = "UserPromptSubmit",
    truth_axis: str = "truth",
    mode: str = "standard",
) -> str:
    return _ethics_payload_json(
        schema=ETHICS_SCHEMA,
        block_name="NOEMA_ETHICS_HARDCODED",
        event=event,
        truth_axis=truth_axis,
        mode=mode,
    )


__all__ = [
    "ETHICS_CONCEPTS",
    "ETHICS_SCHEMA",
    "HardcodedEthicsBlock",
    "build_opencode_ethics_block",
    "ethics_payload_json",
    "render_opencode_ethics_block",
]
