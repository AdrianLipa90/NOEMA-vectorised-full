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
    read_ciel_internal_state,
    update_coupling_from_concepts,
    update_coupling_hebbian,
    update_surface_from_ciel_state,
    write_concepts_to_surface,
)


def test_ensure_surface_creates_expected_files(tmp_path: Path):
    surface = ensure_surface(tmp_path, zero_fill=True)

    assert set(surface) == {"phi", "omega", "g", "Z_geom", "R_geom", "psi_geom", "flavor", "tick", "gravity", "holonomy", "tau", "sensor_raw"}
    assert surface["phi"].shape == (N_OSCILLATORS,)
    assert surface["g"].shape == (N_OSCILLATORS, N_OSCILLATORS)
    assert surface["flavor"].shape == (N_FLAVORS,)
    assert surface["tick"].dtype == np.uint64


def test_initialize_surface_populates_deterministic_state(tmp_path: Path):
    surface = initialize_surface(tmp_path, seed=123)

    assert np.all(surface["phi"] >= 0.0)
    assert np.all(surface["phi"] < 2.0 * np.pi)
    assert not np.allclose(surface["g"], np.eye(N_OSCILLATORS))
    assert surface["g"].shape == (N_OSCILLATORS, N_OSCILLATORS)
    assert np.all(np.diag(np.asarray(surface["g"])) == 0.0)
    assert surface["tick"][0] == 0


def test_initialize_coupling_from_memory_channels_structure(tmp_path: Path):
    g = np.zeros((N_OSCILLATORS, N_OSCILLATORS), dtype=np.float64)
    initialize_coupling_from_memory_channels(g)

    assert g.shape == (N_OSCILLATORS, N_OSCILLATORS)
    assert np.allclose(np.diag(g), 0.0)
    for ch in range(8):
        block = g[ch * 3 : ch * 3 + 3, ch * 3 : ch * 3 + 3]
        off_diag = block[~np.eye(3, dtype=bool)]
        assert np.all(off_diag > 0.0), f"within-channel block {ch} has zero off-diagonal"
        assert np.all(off_diag <= 1.0)
    assert g[0, 1] > 0.0
    assert g[0, 4] > 0.0
    assert g[6, 7] > 0.0
    assert g[0, 2] > 0.0
    assert g[3, 5] > 0.0
    assert g[1, 2] > 0.0
    assert g[4, 5] > 0.0


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
    mode_before = float(surface["flavor"][5])

    update_surface_from_ciel_state(
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

    internal = read_ciel_internal_state(tmp_path)
    assert internal["coherence_index"] == 0.9
    assert internal["mode_code"] == 1.0
    assert float(surface["flavor"][5]) == mode_before


def test_describe_surface_returns_json_serializable_metadata(tmp_path: Path):
    initialize_surface(tmp_path, seed=1)
    meta = describe_surface(tmp_path)

    assert meta["root"] == str(tmp_path)
    assert meta["n_oscillators"] == N_OSCILLATORS
    assert "files" in meta
    assert "phi" in meta["files"]


def test_open_surface_reads_existing_state(tmp_path: Path):
    surface = initialize_surface(tmp_path, seed=99)
    original_phi = np.asarray(surface["phi"]).copy()
    del surface

    reopened = open_surface(tmp_path, mode="r")
    assert np.allclose(reopened["phi"], original_phi)


def test_imaginal_surface_evolves_and_projects(tmp_path: Path):
    imaginal_root = tmp_path / "imaginal"
    real_root = tmp_path / "real"
    imaginal = initialize_surface(imaginal_root, seed=1)
    real = initialize_surface(real_root, seed=2)
    real_before = np.asarray(real["phi"]).copy()

    evolve_imaginal_surface(imaginal, dt=0.02)
    project_imaginal_to_real(imaginal, real, projection_strength=0.5)

    assert not np.allclose(real_before, np.asarray(real["phi"]))
    assert compute_zpe(np.asarray(imaginal["g"]), np.asarray(imaginal["phi"])) >= 0.0
