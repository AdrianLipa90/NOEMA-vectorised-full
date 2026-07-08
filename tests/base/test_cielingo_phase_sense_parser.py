from __future__ import annotations

from cielingo.phase_sense_parser import parse_text_to_phase_sense, phase_sense_for_token, tokenize_surface


def test_tokenize_polish_surface():
    assert tokenize_surface("Być światło, strach i czas!") == ["Być", "światło", "strach", "i", "czas"]


def test_phase_sense_matches_known_language_cards():
    report = parse_text_to_phase_sense("być światło strach czas", ".", language_hint="pl")
    assert report["schema"] == "cielingo/phase-sense-report/v0.1"
    assert report["token_count"] == 4
    assert report["matched_token_count"] >= 3
    assert 0.0 <= report["mean_density"] <= 1.0
    assert 0.0 <= report["mean_viscosity"] <= 1.0
    assert report["phase_sense_digest"]
    assert any(t["card_id"] == "concept:light" for t in report["tokens"])


def test_unknown_token_is_supervised_candidate():
    tok = phase_sense_for_token("xyznieznaneslowo", position=0, repo_root=".", language_hint="pl")
    assert tok.matched is False
    assert tok.supervision_required is True
    assert tok.parse_status == "unmatched_needs_supervised_language_card"
    assert tok.vector_digest is None
