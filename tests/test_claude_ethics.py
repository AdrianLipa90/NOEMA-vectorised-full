from __future__ import annotations

from pathlib import Path

from src.ciel_sot_agent.claude_ethics import (
    ETHICS_CONCEPTS,
    CLAUDE_ETHICS_SCHEMA,
    build_claude_ethics_block,
    render_claude_ethics_block,
)


def test_claude_ethics_block_contains_invariant_concepts() -> None:
    block = build_claude_ethics_block(event="UserPromptSubmit")

    assert block.schema == CLAUDE_ETHICS_SCHEMA
    assert "truth" in block.concepts
    assert "consent" in block.concepts
    assert "no_deception" in block.concepts
    assert block.policy["truth_over_smoothing"] is True
    assert block.policy["explicit_uncertainty"] is True


def test_render_claude_ethics_block_includes_hardcoded_section() -> None:
    rendered = render_claude_ethics_block(event="SessionStart")

    assert "NOEMA_CLAUDE_ETHICS_HARDCODED" in rendered
    assert "no consent bypass" in rendered
    for concept in ETHICS_CONCEPTS:
        assert concept in rendered


def test_workspace_claude_md_contains_claude_ethics_block() -> None:
    claude_md = Path("/home/adrian/new_volume_rw/CLAUDE.md")
    content = claude_md.read_text(encoding="utf-8")

    assert "NOEMA_CLAUDE_ETHICS_HARDCODED" in content
    assert "truth over smoothing" in content
    assert "respect_for_personhood" in content
    assert "φ[claude.binding]=ACTIVE" in content
