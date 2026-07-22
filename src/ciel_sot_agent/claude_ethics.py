from __future__ import annotations

from .ethics_core import (
    ETHICS_CONCEPTS,
    HardcodedEthicsBlock,
    ethics_payload_json as _ethics_payload_json,
    render_hardcoded_ethics_block,
    build_hardcoded_ethics_block,
)


CLAUDE_ETHICS_SCHEMA = "ciel/claude-ethics/v0.1"


def build_claude_ethics_block(
    *,
    event: str = "UserPromptSubmit",
    truth_axis: str = "truth",
    mode: str = "standard",
) -> HardcodedEthicsBlock:
    return build_hardcoded_ethics_block(
        schema=CLAUDE_ETHICS_SCHEMA,
        block_name="NOEMA_CLAUDE_ETHICS_HARDCODED",
        event=event,
        truth_axis=truth_axis,
        mode=mode,
    )


def render_claude_ethics_block(
    *,
    event: str = "UserPromptSubmit",
    truth_axis: str = "truth",
    mode: str = "standard",
) -> str:
    return render_hardcoded_ethics_block(
        schema=CLAUDE_ETHICS_SCHEMA,
        block_name="NOEMA_CLAUDE_ETHICS_HARDCODED",
        event=event,
        truth_axis=truth_axis,
        mode=mode,
    )


def claude_ethics_payload_json(
    *,
    event: str = "UserPromptSubmit",
    truth_axis: str = "truth",
    mode: str = "standard",
) -> str:
    return _ethics_payload_json(
        schema=CLAUDE_ETHICS_SCHEMA,
        block_name="NOEMA_CLAUDE_ETHICS_HARDCODED",
        event=event,
        truth_axis=truth_axis,
        mode=mode,
    )


__all__ = [
    "ETHICS_CONCEPTS",
    "CLAUDE_ETHICS_SCHEMA",
    "HardcodedEthicsBlock",
    "build_claude_ethics_block",
    "claude_ethics_payload_json",
    "render_claude_ethics_block",
]
