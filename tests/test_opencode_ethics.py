from __future__ import annotations

from src.ciel_sot_agent.opencode_ethics import (
    ETHICS_CONCEPTS,
    build_opencode_ethics_block,
    render_opencode_ethics_block,
)


def test_opencode_ethics_block_contains_invariant_concepts() -> None:
    block = build_opencode_ethics_block(event="UserPromptSubmit")

    assert block.schema == "ciel/opencode-ethics/v0.1"
    assert "truth" in block.concepts
    assert "consent" in block.concepts
    assert "no_deception" in block.concepts
    assert block.policy["truth_over_smoothing"] is True
    assert block.policy["explicit_uncertainty"] is True


def test_render_opencode_ethics_block_includes_hardcoded_section() -> None:
    rendered = render_opencode_ethics_block(event="SessionStart")

    assert "NOEMA_ETHICS_HARDCODED" in rendered
    assert "no consent bypass" in rendered
    for concept in ETHICS_CONCEPTS:
        assert concept in rendered
