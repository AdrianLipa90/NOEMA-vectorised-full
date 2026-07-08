from __future__ import annotations

import json
from pathlib import Path

from cielingo.canonization_audit import decide_infinitive, generate_canonization_audit


def test_decide_infinitive_accepts_only_trusted_local_mapping() -> None:
    accepted = decide_infinitive({
        "mapping_type": "verbal_noun_owanie_to_ować",
        "confidence": 0.45,
        "source_surface": "kodowania",
        "infinitive_candidate": "kodować",
        "source_card_id": "MISSING-POL-X",
    })
    assert accepted.decision == "accept_local_canonical_infinitive_mapping"
    assert accepted.canon_scope == "CIELingo_local_mapping_not_dictionary_canon"
    blocked = decide_infinitive({
        "mapping_type": "verbal_noun_anie_to_ać_low_conf",
        "confidence": 0.32,
        "source_surface": "omijania",
        "infinitive_candidate": "omijać",
    })
    assert blocked.decision == "keep_as_candidate_pending_morphology_source_review"


def test_generate_canonization_audit_outputs_local_canon_files(tmp_path: Path) -> None:
    inf = tmp_path / "inf.jsonl"
    res = tmp_path / "res.jsonl"
    out = tmp_path / "out"
    inf.write_text(
        json.dumps({"mapping_type": "verbal_noun_owanie_to_ować", "confidence": 0.45, "source_surface": "kodowania", "infinitive_candidate": "kodować", "source_card_id": "A"}, ensure_ascii=False) + "\n"
        + json.dumps({"mapping_type": "verbal_noun_anie_to_ać_low_conf", "confidence": 0.32, "source_surface": "omijania", "infinitive_candidate": "omijać", "source_card_id": "B"}, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    res.write_text(json.dumps({"residual_set_id": "pos_meaning_unknown", "surface": "wymóg", "confidence": 0.25, "source_card_id": "C"}, ensure_ascii=False) + "\n", encoding="utf-8")
    report = generate_canonization_audit(infinitive_candidates_path=inf, residual_assignments_path=res, output_dir=out)
    assert report["decision_counts"]["accepted_local_infinitive_mappings"] == 1
    assert report["decision_counts"]["deferred_infinitive_candidates"] == 1
    assert report["decision_counts"]["accepted_local_residual_set_assignments"] == 1
    assert (out / "canonical_infinitive_map.local.jsonl").exists()
    assert (out / "canonical_residual_set_assignments.local.jsonl").exists()
