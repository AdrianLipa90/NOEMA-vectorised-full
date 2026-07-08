from pathlib import Path

from ciel_geometry.noema_surface_mmap import initialize_surface, open_surface
from ciel_geometry.phase_memory_adapter import (
    bind_phase_memory,
    encode_text_to_binary_vector,
    ensure_phase_memory,
    query_phase_memory,
)


def test_encode_text_to_binary_vector_is_deterministic():
    a = encode_text_to_binary_vector("Adrian maps NOEMA")
    b = encode_text_to_binary_vector("Adrian maps NOEMA")
    c = encode_text_to_binary_vector("Different phrase entirely")

    assert a.shape == (256,)
    assert a.tolist() == b.tolist()
    assert a.tolist() != c.tolist()


def test_bind_phase_memory_persists_slot(tmp_path: Path):
    surface_root = tmp_path / "surface"
    memory_root = tmp_path / "memory"
    initialize_surface(surface_root, seed=42)

    slot = bind_phase_memory(
        "Adrian establishes a phase anchor",
        surface_root=surface_root,
        memory_root=memory_root,
        slots=8,
    )

    memory = ensure_phase_memory(memory_root, slots=8)
    assert slot == 0
    assert int(memory["occupied"][slot]) == 1
    assert int(memory["write_head"][0]) == 1


def test_query_phase_memory_returns_best_match_first(tmp_path: Path):
    surface_root = tmp_path / "surface"
    memory_root = tmp_path / "memory"
    initialize_surface(surface_root, seed=7)

    bind_phase_memory("Adrian builds ERB memory bridge", surface_root=surface_root, memory_root=memory_root, slots=8)
    surface = open_surface(surface_root)
    surface["tick"][0] = 9
    surface["tick"].flush()
    bind_phase_memory("Another unrelated memory", surface_root=surface_root, memory_root=memory_root, slots=8)

    rows = query_phase_memory(
        "Adrian builds ERB memory bridge",
        surface_root=surface_root,
        memory_root=memory_root,
        slots=8,
        top_k=2,
    )

    assert len(rows) == 2
    assert rows[0].vector_similarity >= rows[1].vector_similarity
    assert rows[0].score >= rows[1].score
    assert rows[0].tick in {0, 9}
