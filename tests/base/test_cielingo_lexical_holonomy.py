from __future__ import annotations

from pathlib import Path

import pytest

from cielingo.lexical_holonomy import (
    build_lexical_holonomy_edges,
    build_word_knowledge_notes,
    extract_lexical_units,
    lexical_holonomy_report,
    list_language_card_files,
    read_language_card_file,
)


ROOT = Path(__file__).resolve().parents[2]


def test_extracts_lexical_units_and_relations():
    units = extract_lexical_units(ROOT)
    assert units
    assert any(u.language == "pl" for u in units)
    edges = build_lexical_holonomy_edges(ROOT)
    assert edges
    assert any(e.relation_type in {"near_synonym", "antonym"} for e in edges)
    assert any(e.relation_family == "opposition_or_divergence" for e in edges)


def test_word_knowledge_notes_have_confidence_and_sources():
    notes = build_word_knowledge_notes(ROOT)
    assert notes
    sample = notes[0]
    assert 0.0 <= sample.knowledge_confidence <= 1.0
    assert sample.open_source_sources_to_check
    assert sample.correction_policy.startswith("suggest_only")


def test_language_card_file_access_is_guarded():
    files = list_language_card_files(ROOT)
    assert files
    concept = next(f for f in files if f.path.endswith("air.json"))
    text = read_language_card_file(concept.path, ROOT)
    assert "concept:air" in text
    with pytest.raises(ValueError):
        read_language_card_file("README.md", ROOT)


def test_report_contains_relation_counts_and_access_surface():
    report = lexical_holonomy_report(ROOT, language="pl", query="światło")
    assert report["schema"] == "cielingo/lexical-holonomy/v0.1"
    assert report["own_language_card_file_count"] > 0
    assert report["relation_counts"]
    assert report["word_notes"]
