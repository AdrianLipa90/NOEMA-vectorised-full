from __future__ import annotations

import json
from pathlib import Path

from cielingo.infinitive_merge_audit import generate_infinitive_merge_audit, infinitivize_word


def test_infinitivize_safe_forms() -> None:
    assert infinitivize_word("robić")[0] == "robić"
    assert infinitivize_word("kontynuując")[0] == "kontynuować"
    assert infinitivize_word("działanie")[0] == "działać"
    assert infinitivize_word("bytu")[0] is None


def test_generate_infinitive_merge_outputs(tmp_path: Path) -> None:
    unknown = tmp_path / "unknown_words.jsonl"
    rows = [
        {"surface": "robić", "source_card_id": "A", "semantic": {"semantic_rest_mass": 0.5, "density_priority_weight": 0.7, "relation_energy_proxy": 1.0}},
        {"surface": "kontynuując", "source_card_id": "B", "semantic": {"semantic_rest_mass": 0.4, "density_priority_weight": 0.6, "relation_energy_proxy": 0.8}},
        {"surface": "bytu", "source_card_id": "C", "missing_axis": "morphology_and_lemma", "semantic": {}},
    ]
    unknown.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    out = tmp_path / "out"
    report = generate_infinitive_merge_audit(unknown, out)
    assert report["input_unknown_count"] == 3
    assert report["infinitivized_count"] == 2
    assert report["residual_count"] == 1
    assert (out / "infinitive_state_merged.jsonl").exists()
    assert (out / "owned_residual_sets.jsonl").exists()
