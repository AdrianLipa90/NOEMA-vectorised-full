from __future__ import annotations

from pathlib import Path

from ciel_geometry.orbital_hierarchy import orbit_load_order
from src.CIEL_OMEGA_COMPLETE_SYSTEM.ciel_omega.memory.tiered_orchestrator import TieredMemoryOrchestrator


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_system_map_exposes_the_tiered_memory_orbital_chain() -> None:
    load_order = orbit_load_order(map_path=REPO_ROOT / "system_map_v2.json", root_id="module:tiered_memory")

    assert [node["id"] for node in load_order] == [
        "module:tiered_memory",
        "module:tiered_memory:orbital_root",
        "module:tiered_memory:fast",
        "module:tiered_memory:medium",
        "module:tiered_memory:deep",
        "module:tiered_memory:async",
    ]


def test_tiered_memory_bootstrap_runs_in_orbital_order(monkeypatch) -> None:
    orch = TieredMemoryOrchestrator(auto_init=False)
    calls: list[str] = []

    monkeypatch.setattr(orch, "_ensure_surface", lambda: calls.append("surface") or {"tick": [0]})
    monkeypatch.setattr(orch, "_ensure_cielingo_memory", lambda: calls.append("cielingo_memory") or True)
    monkeypatch.setattr(orch, "_ensure_channel_orch", lambda: calls.append("channel_orch") or object())
    monkeypatch.setattr(orch, "_ensure_holonomic", lambda: calls.append("holonomic") or object())
    monkeypatch.setattr(orch, "_ensure_bloch", lambda: calls.append("bloch") or object())
    monkeypatch.setattr(orch, "_ensure_state_db", lambda: calls.append("state_db") or object())
    monkeypatch.setattr(orch, "_ensure_unified", lambda: calls.append("unified") or object())

    manifest = orch.bootstrap_orbital_memory(map_path=REPO_ROOT / "system_map_v2.json")

    assert calls == [
        "surface",
        "cielingo_memory",
        "channel_orch",
        "holonomic",
        "bloch",
        "state_db",
        "unified",
    ]
    assert [step["id"] for step in manifest] == [
        "module:tiered_memory",
        "module:tiered_memory:orbital_root",
        "module:tiered_memory:fast",
        "module:tiered_memory:medium",
        "module:tiered_memory:deep",
        "module:tiered_memory:async",
    ]
    assert orch._memory_bootstrap_manifest["root_id"] == "module:tiered_memory"


def test_tiered_memory_snapshot_and_health_include_bootstrap_manifest(monkeypatch) -> None:
    orch = TieredMemoryOrchestrator(auto_init=False)
    monkeypatch.setattr(orch, "_ensure_surface", lambda: {"tick": [0]})
    monkeypatch.setattr(orch, "_ensure_cielingo_memory", lambda: True)
    monkeypatch.setattr(orch, "_ensure_channel_orch", lambda: type("S", (), {"snapshot": lambda self: type("Snap", (), {"cycle_index": 1, "identity_phase": 0.25, "energy": {}, "defects": {}, "counts": {}, "latest_loop_status": {}})()})())
    monkeypatch.setattr(orch, "_ensure_holonomic", lambda: type("H", (), {"stats": lambda self: {}, "edge_stats": lambda self: {}})())
    monkeypatch.setattr(orch, "_ensure_bloch", lambda: object())
    monkeypatch.setattr(orch, "_ensure_unified", lambda: object())
    monkeypatch.setattr(orch, "_ensure_state_db", lambda: object())

    orch.bootstrap_orbital_memory(map_path=REPO_ROOT / "system_map_v2.json")

    snap = orch.snapshot()
    health = orch.health()

    assert snap.memory_bootstrap["root_id"] == "module:tiered_memory"
    assert snap.memory_bootstrap["load_order"][1]["id"] == "module:tiered_memory:orbital_root"
    assert health["bootstrap"]["status"] == "ready"
    assert health["bootstrap"]["shell_count"] == 6
    assert health["bootstrap"]["executed_count"] == 6
