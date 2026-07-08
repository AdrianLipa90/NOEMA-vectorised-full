from __future__ import annotations

import json
from pathlib import Path

from cielingo.unresolved_realtime import (
    CANDIDATE_CONFIDENCE,
    daily_unresolved_rollup,
    record_realtime_unresolved,
    source_candidates_for_word,
    unresolved_events_from_text,
)


def _write_evidence(root: Path, word: str = "flumbra") -> None:
    base = root / "data" / "cielingo" / "source_evidence"
    base.mkdir(parents=True, exist_ok=True)
    payload = {
        "source_id": "test:supervised:fixture",
        "source_kind": "test_fixture_local_descriptor",
        "source_name": "Local supervised fixture",
        "license_hint": "test_only",
        "retrieval_mode": "local_jsonl_no_network",
        "lemma": word,
        "language": "pl",
        "definition": "Testowe znaczenie używane wyłącznie do walidacji karty kandydata.",
        "part_of_speech": "noun_candidate",
        "synonyms": ["flumbra_syn"],
        "antonyms": ["flumbra_ant"],
        "register": "test",
        "emotional_colour": "neutral_test",
        "emotional_intensity": 0.25,
        "evidence_confidence": 0.75,
    }
    (base / "fixture.jsonl").write_text(json.dumps(payload, ensure_ascii=False) + "\n", encoding="utf-8")


def test_unresolved_events_are_detected_without_canonization(tmp_path: Path) -> None:
    events = unresolved_events_from_text("flumbra", tmp_path, language_hint="pl")
    assert len(events) == 1
    assert events[0].normalized == "flumbra"
    assert events[0].status == "unresolved_observed_realtime"
    assert events[0].candidate_card_id is None


def test_realtime_checker_creates_candidate_card_only_with_source_evidence(tmp_path: Path) -> None:
    _write_evidence(tmp_path)
    report = record_realtime_unresolved("flumbra", tmp_path, language_hint="pl", source_role="unit_test")
    assert report["unresolved_count"] == 1
    assert report["candidate_count"] == 1
    candidate_rel = report["candidate_card_paths"][0]
    candidate = json.loads((tmp_path / candidate_rel).read_text(encoding="utf-8"))
    assert candidate["confidence"] == CANDIDATE_CONFIDENCE
    assert candidate["status"] == "candidate_0_5_pending_supervised_review"
    assert candidate["correction_policy"] == "suggest_only_under_human_supervision_no_auto_canon"
    assert candidate["scalar_context"]["colour"] == "neutral_test"
    assert candidate["potential"]["kappa_info_ln2_over_24pi"] > 0


def test_realtime_checker_keeps_unknown_unresolved_without_source_evidence(tmp_path: Path) -> None:
    report = record_realtime_unresolved("glorbnik", tmp_path, language_hint="pl", source_role="unit_test")
    assert report["unresolved_count"] == 1
    assert report["candidate_count"] == 0
    assert report["candidate_card_paths"] == []


def test_source_evidence_lookup_and_daily_rollup(tmp_path: Path) -> None:
    _write_evidence(tmp_path, word="rzednie")
    matches = source_candidates_for_word("rzednie", tmp_path, language_hint="pl")
    assert len(matches) == 1
    record_realtime_unresolved("rzednie glorbnik", tmp_path, language_hint="pl", source_role="unit_test")
    rollup = daily_unresolved_rollup(tmp_path)
    assert rollup["event_count"] == 2
    assert rollup["unique_unresolved_count"] == 2
    assert rollup["candidate_ready_count"] == 1
