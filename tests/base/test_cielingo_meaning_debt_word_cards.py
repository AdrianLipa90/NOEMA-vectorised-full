from __future__ import annotations

import csv
from pathlib import Path

from cielingo.meaning_debt_word_cards import (
    CANDIDATE_CONFIDENCE,
    build_candidate_cards,
    generate_debt_word_cards,
    is_polish_infinitive,
    read_debt_index,
)


def _write_index(path: Path) -> None:
    rows = [
        {
            "card_id": "MISSING-POL-0001",
            "surface": "robić",
            "lemma": "robić",
            "source_file": "cards/robić.yaml",
            "debt_flags": "meaning_english_or_technical;representation_PASS_not_valid_as_polish_word_card",
            "debt_flag_count": "2",
            "recommended_state": "DEBT_RECORDED__DO_NOT_USE_AS_POLISH_WORD_CARD",
        },
        {
            "card_id": "MISSING-POL-0002",
            "surface": "i",
            "lemma": "i",
            "source_file": "cards/i.yaml",
            "debt_flags": "meaning_english_or_technical",
            "debt_flag_count": "1",
            "recommended_state": "DEBT_RECORDED__DO_NOT_USE_AS_POLISH_WORD_CARD",
        },
        {
            "card_id": "MISSING-POL-0003",
            "surface": "semantic",
            "lemma": "semantic",
            "source_file": "cards/semantic.yaml",
            "debt_flags": "surface_english_or_project_term;meaning_english_or_technical",
            "debt_flag_count": "2",
            "recommended_state": "DEBT_RECORDED__DO_NOT_USE_AS_POLISH_WORD_CARD",
        },
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def test_infinitive_heuristic_excludes_abstract_nouns_and_participles() -> None:
    assert is_polish_infinitive("robić", {"lemma": "robić"})
    assert is_polish_infinitive("móc", {"lemma": "móc"})
    assert not is_polish_infinitive("bliskość", {"lemma": "bliskość"})
    assert not is_polish_infinitive("kontynuując", {"lemma": "kontynuując"})


def test_build_candidate_cards_marks_every_word(tmp_path: Path) -> None:
    idx = tmp_path / "affected_cards_index.csv"
    _write_index(idx)
    records = read_debt_index(idx)
    cards = build_candidate_cards(records)
    assert len(cards) == 3
    assert all(card.confidence == CANDIDATE_CONFIDENCE for card in cards)
    assert all(card.grammatical_designation["part_of_speech_candidate"] for card in cards)
    assert all(card.grammatical_designation["sentence_part_candidate"] for card in cards)
    assert all(card.ordinal_semantics["filename_or_sequence_number_has_no_semantic_rank"] for card in cards)
    by_lemma = {card.lemma: card for card in cards}
    assert by_lemma["robić"].grammatical_designation["part_of_speech_candidate"] == "verb_infinitive"
    assert by_lemma["i"].grammatical_designation["part_of_speech_candidate"] == "conjunction"
    assert by_lemma["semantic"].grammatical_designation["part_of_speech_candidate"] == "technical_label_or_foreign_word"


def test_generate_outputs_infinitives_and_other_pos(tmp_path: Path) -> None:
    idx = tmp_path / "affected_cards_index.csv"
    out = tmp_path / "cards"
    _write_index(idx)
    report = generate_debt_word_cards(idx, output_dir=out)
    assert report.total_records == 3
    assert report.candidate_cards == 3
    assert report.infinitive_cards == 1
    assert (out / "word_candidate_cards.jsonl").exists()
    assert (out / "infinitive_candidate_cards.jsonl").exists()
    assert (out / "other_pos_candidate_cards.jsonl").exists()
    assert (out / "by_part_of_speech" / "verb_infinitive.jsonl").exists()
