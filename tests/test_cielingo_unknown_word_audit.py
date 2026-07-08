from __future__ import annotations

import json
from pathlib import Path

from cielingo.unknown_word_audit import (
    audit_entry_from_card,
    audit_unknown_words,
    classify_unknown_word,
    load_unknown_candidate_cards,
)


def test_classify_closed_class_missed() -> None:
    card = {"surface": "niż", "lemma": "niż", "source_debt_record": {"source_card_id": "x"}}
    debt_type, missing_axis, pos, *_ = classify_unknown_word(card)
    assert debt_type == "closed_class_missed"
    assert missing_axis == "closed_class_operator_axis"
    assert "connector" in pos


def test_audit_entry_keeps_unknown_non_canon() -> None:
    card = {
        "id": "CAND-X",
        "surface": "mnogiej",
        "lemma": "mnogi",
        "semantic_designation": {"word_potential": 0.01, "density_priority_weight": 0.56},
        "source_debt_record": {"source_card_id": "MISSING-POL-X", "source_file": "x.yaml"},
    }
    entry = audit_entry_from_card(card)
    assert entry.productive_failure is True
    assert entry.auto_canonization_allowed is False
    assert entry.classification_status == "audited_unknown_not_canon"
    assert entry.confidence <= 0.55


def test_load_unknown_candidate_cards_from_repo() -> None:
    repo = Path(__file__).resolve().parents[1]
    cards = load_unknown_candidate_cards(repo)
    assert len(cards) >= 600
    assert all((c.get("grammatical_designation") or {}).get("part_of_speech_candidate") == "unknown_word_candidate" for c in cards[:20])


def test_audit_unknown_words_writes_outputs(tmp_path: Path) -> None:
    repo = Path(__file__).resolve().parents[1]
    report = audit_unknown_words(repo, batch_size=100, output_dir=tmp_path)
    assert report.unknown_count >= 600
    assert report.unknown_is_productive is True
    assert report.review_batch_count >= 6
    assert (tmp_path / "unknown_words.audit.jsonl").exists()
    assert (tmp_path / "unknown_clusters.jsonl").exists()
    assert (tmp_path / "source_lookup_queue.jsonl").exists()
    assert (tmp_path / "promotion_candidates_0_5.jsonl").exists()
    assert (tmp_path / "review_batches" / "batch_001.jsonl").exists()
    summary = json.loads((tmp_path / "missing_axes_report.json").read_text(encoding="utf-8"))
    assert summary["unknown_is_productive"] is True
    assert sum(summary["by_debt_type"].values()) == report.unknown_count
