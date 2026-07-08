from __future__ import annotations

from cielingo.triadic_output_vector import TRIAD_VECTOR_DIM, on_vivo_output_test, vectorize_triadic_output


def test_triadic_output_vector_has_three_36d_lanes():
    report = vectorize_triadic_output("być światło strach czas", ".", language_hint="pl")
    assert report["schema"] == "cielingo/triadic-output-vector/v0.1"
    assert report["vector_dim"] == TRIAD_VECTOR_DIM == 108
    assert report["lane_dim"] == 36
    assert len(report["comprehension_lane"]) == 36
    assert len(report["inference_lane"]) == 36
    assert len(report["expression_lane"]) == 36
    assert len(report["output_vector"]) == 108
    assert report["noema_output_document"]["phase_sense_digest"] == report["phase_sense_report"]["phase_sense_digest"]


def test_on_vivo_output_test_reports_runtime_status():
    report = on_vivo_output_test("być światło strach czas", ".", language_hint="pl")
    assert report["schema"] == "cielingo/on-vivo-output-test/v0.1"
    assert report["vector_dim"] == 108
    assert report["matched_token_count"] >= 3
    assert 0.0 <= report["output_readiness"] <= 1.0
    assert 0.0 <= report["phase_lock"] <= 1.0
    assert report["output_digest"] == report["output"]["output_digest"]


def test_unknown_words_reduce_supervision_flag():
    report = on_vivo_output_test("xyznieznaneslowo światło", ".", language_hint="pl")
    assert report["unknown_token_count"] >= 1
    assert report["needs_supervised_grammar_review"] is True
