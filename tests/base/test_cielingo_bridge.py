from __future__ import annotations

from src.ciel_sot_agent.cielingo_bridge import build_lingo_frame, build_phasenav_vector_frame, render_lingo_summary


def test_build_lingo_frame_detects_deictic_and_noema_signals() -> None:
    frame = build_lingo_frame("Here now we ask somewhere?", ciel_state={"language": "en"})

    assert frame["tokens"]
    assert "here" in frame["tokens"]
    assert "now" in frame["tokens"]
    assert "somewhere" in frame["tokens"]
    assert frame["deictic_frame"]["relative_anchors"]
    assert frame["unresolved"]
    assert frame["noema_route"]["factual_validation_required"] is False
    assert frame["projection_confidence"] <= 1.0
    assert frame["phase_projection"]["phase_anchor_count"] >= 2
    assert frame["phase_projection"]["phase_confidence"] <= 1.0
    assert frame["tau_bridge"]["tau_gradient_mean"] >= 0.0
    assert 0.0 <= frame["tau_bridge"]["imaginal_drive"] <= 1.0


def test_build_lingo_frame_projects_distal_deixis_toward_pi() -> None:
    frame = build_lingo_frame("there then", ciel_state={"language": "en"})
    phase = frame["phase_projection"]["target_phase"]

    assert 2.0 <= phase <= 3.5


def test_render_lingo_summary_is_compact_and_stable() -> None:
    frame = build_lingo_frame("now here", ciel_state={"language": "en"})
    summary = render_lingo_summary(frame)

    assert summary.startswith("CIELingo|")
    assert "concepts=" in summary
    assert "deictic=" in summary
    assert "noema_conf=" in summary


def test_tau_bridge_is_present_and_phase_sensitive() -> None:
    frame = build_lingo_frame("here now", ciel_state={"language": "en"})
    tau_bridge = frame["tau_bridge"]

    assert "tau_axis" in tau_bridge
    assert "tau_profile" in tau_bridge
    assert "tau_gradient" in tau_bridge
    assert tau_bridge["semantic_density"] > 0.0
    assert tau_bridge["deictic_density"] > 0.0


def test_phasenav_vector_frame_keeps_memory_contract() -> None:
    frame = build_phasenav_vector_frame("optimize memory layers with phasenav", ciel_state={"language": "en"})

    assert frame["summary"].startswith("PhaseNav|")
    assert len(frame["phase_nav"]["vector_36d"]) == 36
    assert frame["noema_route"]["bundle"]["selected_refs"]
    assert 0.0 <= frame["projection_confidence"] <= 1.0
    assert len(frame["tau_bridge"]["tau_axis"]) == 36
    assert 0.0 <= frame["tau_bridge"]["imaginal_drive"] <= 1.0


def test_build_lingo_frame_preserves_full_contract_with_phasenav_vector() -> None:
    frame = build_lingo_frame("default semantic frame includes phasenav", ciel_state={"language": "en"})

    assert frame["summary"].startswith("CIELingo|")
    assert len(frame["phase_nav"]["vector_36d"]) == 36
    assert "phase_projection" in frame
    assert "tau_bridge" in frame
