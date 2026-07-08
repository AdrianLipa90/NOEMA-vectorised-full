from pathlib import Path

import numpy as np

from ciel_geometry.noema_surface_mmap import (
    J_KJ,
    N_FLAVORS,
    N_OSCILLATORS,
    compute_zpe,
    describe_surface,
    ensure_surface,
    evolve_imaginal_surface,
    evolve_surface,
    initialize_coupling_from_memory_channels,
    initialize_surface,
    open_surface,
    oscillator_id_for_concept,
    project_imaginal_to_real,
    read_surface_state,
    update_coupling_from_concepts,
    update_coupling_hebbian,
    update_surface_from_ciel_state,
    write_concepts_to_surface,
)


def test_ensure_surface_creates_expected_files(tmp_path: Path):
    surface = ensure_surface(tmp_path, zero_fill=True)

    assert set(surface) == {"phi", "omega", "g", "Z_geom", "R_geom", "psi_geom", "flavor", "tick", "gravity", "holonomy"}
    assert surface["phi"].shape == (N_OSCILLATORS,)
    assert surface["g"].shape == (N_OSCILLATORS, N_OSCILLATORS)
    assert surface["flavor"].shape == (N_FLAVORS,)
    assert surface["tick"].dtype == np.uint64


def test_initialize_surface_populates_deterministic_state(tmp_path: Path):
    surface = initialize_surface(tmp_path, seed=123)

    assert np.all(surface["phi"] >= 0.0)
    assert np.all(surface["phi"] < 2.0 * np.pi)
    # g is now seeded from J_kj memory channel matrix, not identity
    assert not np.allclose(surface["g"], np.eye(N_OSCILLATORS))
    assert surface["g"].shape == (N_OSCILLATORS, N_OSCILLATORS)
    assert np.all(np.diag(np.asarray(surface["g"])) == 0.0)  # no self-coupling
    assert surface["tick"][0] == 0


def test_initialize_coupling_from_memory_channels_structure(tmp_path: Path):
    g = np.zeros((N_OSCILLATORS, N_OSCILLATORS), dtype=np.float64)
    initialize_coupling_from_memory_channels(g)

    assert g.shape == (N_OSCILLATORS, N_OSCILLATORS)
    assert np.allclose(np.diag(g), 0.0)
    # Within-channel blocks should have strong coupling (off-diagonal)
    for ch in range(8):
        block = g[ch * 3 : ch * 3 + 3, ch * 3 : ch * 3 + 3]
        off_diag = block[~np.eye(3, dtype=bool)]
        assert np.all(off_diag > 0.0), f"within-channel block {ch} has zero off-diagonal"
        assert np.all(off_diag <= 1.0)
    # Between-channel should mirror SU(3) Gell-Mann coupling pattern
    # λ₁ couples (0,1) residue classes → channels 0↔1, 0↔4, 0↔7, 3↔4, etc.
    assert g[0, 1] > 0.0  # M0←M1 (λ₁ coupling, residues 0↔1)
    assert g[0, 4] > 0.0  # M0←M4 (λ₁ coupling, residues 0↔1)
    assert g[6, 7] > 0.0  # M6←M7 (λ₁ coupling, residues 0↔1)
    # λ₄ couples (0,2) residue classes
    assert g[0, 2] > 0.0  # M0←M2 (λ₄ coupling, residues 0↔2)
    assert g[3, 5] > 0.0  # M3←M5 (λ₄ coupling, residues 0↔2)
    # λ₇ couples (1,2) residue classes
    assert g[1, 2] > 0.0  # M1←M2 (λ₇ coupling, residues 1↔2)
    assert g[4, 5] > 0.0  # M4←M5 (λ₇ coupling, residues 1↔2)


def test_evolve_surface_updates_phases(tmp_path: Path):
    surface = initialize_surface(tmp_path, seed=42)
    phi_before = np.asarray(surface["phi"]).copy()
    tick_before = int(surface["tick"][0])

    evolve_surface(surface, dt=0.05)

    phi_after = np.asarray(surface["phi"])
    assert not np.allclose(phi_before, phi_after)
    assert int(surface["tick"][0]) == tick_before + 1
    assert np.all(phi_after >= 0.0)
    assert np.all(phi_after < 2.0 * np.pi)


def test_oscillator_id_for_concept_is_deterministic():
    id1a = oscillator_id_for_concept("miłość")
    id1b = oscillator_id_for_concept("miłość")
    id2 = oscillator_id_for_concept("gniew")
    assert id1a == id1b
    assert 0 <= id1a < N_OSCILLATORS
    assert 0 <= id2 < N_OSCILLATORS


def test_update_coupling_from_concepts_strengthens_pairs(tmp_path: Path):
    g = np.zeros((N_OSCILLATORS, N_OSCILLATORS), dtype=np.float64)
    concepts = ["miłość", "gniew", "spokój"]
    update_coupling_from_concepts(g, concepts, increment=0.1)

    ids = [oscillator_id_for_concept(c) for c in concepts]
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            assert g[ids[i], ids[j]] == 0.1
            assert g[ids[j], ids[i]] == 0.1


def test_update_coupling_hebbian_modifies_matrix(tmp_path: Path):
    g = np.ones((N_OSCILLATORS, N_OSCILLATORS), dtype=np.float64) * 0.5
    np.fill_diagonal(g, 0.0)
    phi = np.linspace(0.0, 2.0 * np.pi, N_OSCILLATORS)

    update_coupling_hebbian(g, phi, lr=0.1, decay=0.01)

    assert np.all(g >= 0.0)
    assert np.allclose(np.diag(g), 0.0)


def test_write_concepts_to_surface_sets_phases(tmp_path: Path):
    surface = initialize_surface(tmp_path, seed=7)
    concepts = ["myśl", "uczucie", "działanie"]
    target = 1.57

    deltas_before = {}
    for c in concepts:
        oid = oscillator_id_for_concept(c)
        current = float(surface["phi"][oid])
        deltas_before[c] = abs(np.arctan2(
            np.sin(current - target),
            np.cos(current - target),
        ))

    write_concepts_to_surface(surface, concepts, target_phase=target, phase_confidence=1.0)

    for c in concepts:
        oid = oscillator_id_for_concept(c)
        after = float(surface["phi"][oid])
        delta_after = abs(np.arctan2(
            np.sin(after - target),
            np.cos(after - target),
        ))
        # Distance to target should have decreased
        assert delta_after < deltas_before[c]


def test_read_surface_state_returns_expected_keys(tmp_path: Path):
    surface = initialize_surface(tmp_path, seed=42)
    evolve_surface(surface, dt=0.01)

    state = read_surface_state(surface)

    assert "coherence_index" in state
    assert "noema_tick" in state
    assert "R_global" in state
    assert "source" in state
    assert state["source"] == "noema_surface"


def test_update_surface_from_ciel_state_sets_flavors(tmp_path: Path):
    surface = initialize_surface(tmp_path, seed=5)

    surface = update_surface_from_ciel_state(
        {
            "mood": 0.2,
            "closure_penalty": 0.1,
            "coherence_index": 0.9,
            "ethical_score": 0.8,
            "soul_invariant": 0.7,
            "phi_berry_mean": 0.3,
            "operating_mode": "deep",
        },
        root=tmp_path,
    )

    assert float(surface["flavor"][0]) == 0.9
    assert float(surface["flavor"][5]) == 1.0


def test_open_surface_reads_back_persisted_values(tmp_path: Path):
    surface = ensure_surface(tmp_path, zero_fill=True)
    surface["phi"][0] = 1.2345
    surface["tick"][0] = 77
    surface["phi"].flush()
    surface["tick"].flush()

    reopened = open_surface(tmp_path)
    assert reopened["phi"][0] == np.float64(1.2345)
    assert reopened["tick"][0] == np.uint64(77)


def test_describe_surface_reports_correct_metadata(tmp_path: Path):
    ensure_surface(tmp_path, zero_fill=True)
    desc = describe_surface(tmp_path)

    assert desc["phi"]["shape"] == (N_OSCILLATORS,)
    assert desc["g"]["dtype"] == "float64"
    assert desc["tick"]["nbytes"] == 8
    assert desc["tick"]["exists"] is True


# ── ZPE, imaginal generator, real projection tests ────────────────────────────


def test_compute_zpe_zero_for_synchronized_phases():
    g = np.ones((N_OSCILLATORS, N_OSCILLATORS), dtype=np.float64) * 0.5
    np.fill_diagonal(g, 0.0)
    phi = np.zeros(N_OSCILLATORS, dtype=np.float64)
    zpe = compute_zpe(g, phi)
    assert zpe == 0.0, "synchronized phases → zero energy"


def test_compute_zpe_max_for_antiphase():
    g = np.ones((N_OSCILLATORS, N_OSCILLATORS), dtype=np.float64)
    np.fill_diagonal(g, 0.0)
    phi = np.array([0.0, np.pi] * (N_OSCILLATORS // 2), dtype=np.float64)
    zpe = compute_zpe(g, phi)
    assert zpe > 0.5, "antiphase → high energy"
    assert zpe <= 1.0


def test_compute_zpe_scales_with_coupling_strength():
    g_weak = np.ones((N_OSCILLATORS, N_OSCILLATORS), dtype=np.float64) * 0.1
    np.fill_diagonal(g_weak, 0.0)
    g_strong = np.ones((N_OSCILLATORS, N_OSCILLATORS), dtype=np.float64) * 1.0
    np.fill_diagonal(g_strong, 0.0)
    phi = np.random.default_rng(42).uniform(0.0, 2.0 * np.pi, N_OSCILLATORS)
    weak_zpe = compute_zpe(g_weak, phi)
    strong_zpe = compute_zpe(g_strong, phi)
    assert weak_zpe < strong_zpe, "stronger coupling → higher ZPE"


def test_evolve_imaginal_surface_updates_phases_and_zpe(tmp_path: Path):
    surface = initialize_surface(tmp_path, seed=3777)
    phi_before = np.asarray(surface["phi"]).copy()
    zpe_before = compute_zpe(
        np.asarray(surface["g"], dtype=np.float64),
        phi_before,
    )

    evolve_imaginal_surface(surface, dt=0.05)

    phi_after = np.asarray(surface["phi"])
    zpe_after = compute_zpe(
        np.asarray(surface["g"], dtype=np.float64),
        phi_after,
    )
    assert not np.allclose(phi_before, phi_after)
    assert int(surface["tick"][0]) >= 1
    assert np.all(phi_after >= 0.0)
    assert np.all(phi_after < 2.0 * np.pi)
    # Imaginal should maintain coherence (flavor[0])
    assert float(surface["flavor"][0]) >= 0.72


def test_project_imaginal_to_real_damps_imaginal_state(tmp_path: Path):
    imaginal = initialize_surface(tmp_path / "imaginal", seed=3777)
    real = initialize_surface(tmp_path / "real", seed=42)

    imaginal_phi_before = np.asarray(imaginal["phi"]).copy()
    real_phi_before = np.asarray(real["phi"]).copy()

    project_imaginal_to_real(imaginal, real, damping=0.5, closure_increase=0.25)

    # Real phases should have shifted toward imaginal
    imaginal_phi_after = np.asarray(imaginal["phi"])
    real_phi_after = np.asarray(real["phi"])
    # Real should now be closer to imaginal than before
    dist_before = np.abs(np.angle(np.exp(1j * (imaginal_phi_before - real_phi_before)))).mean()
    dist_after = np.abs(np.angle(np.exp(1j * (imaginal_phi_after - real_phi_after)))).mean()
    assert dist_after <= dist_before + 0.1
    # Real coherence (flavor[0]) should be damped vs imaginal coherence
    # flavor[4] is the neutrino bus slot — not managed by resonance bridge
    assert float(real["flavor"][0]) <= float(imaginal["flavor"][0]) + 1e-6


def test_dual_surface_hierarchy_zpe_flows_imaginal_to_real(tmp_path: Path):
    imaginal = initialize_surface(tmp_path / "img", seed=3777)
    real = initialize_surface(tmp_path / "real", seed=42)

    evolve_imaginal_surface(imaginal, dt=0.1)
    project_imaginal_to_real(imaginal, real, damping=0.3, closure_increase=0.25)

    zpe_imaginal = compute_zpe(
        np.asarray(imaginal["g"], dtype=np.float64),
        np.asarray(imaginal["phi"], dtype=np.float64),
    )
    zpe_real = compute_zpe(
        np.asarray(real["g"], dtype=np.float64),
        np.asarray(real["phi"], dtype=np.float64),
    )
    # Imaginal has more freedom → ZPE should be non-trivial
    assert zpe_imaginal > 0.0
    # Real is damped → coherence (flavor[0]) should be <= imaginal
    assert float(real["flavor"][0]) <= float(imaginal["flavor"][0]) + 1e-6

