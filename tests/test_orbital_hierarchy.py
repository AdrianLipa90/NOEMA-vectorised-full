from __future__ import annotations

import json
from pathlib import Path

from ciel_geometry.orbital_hierarchy import OrbitalHierarchy, layer_name_for_depth, orbit_load_order, render_orbital_mermaid


def _write_map(path: Path) -> None:
    payload = {
        "version": "2.0",
        "date": "2026-07-06",
        "author": "Adrian Lipa & NOEMA",
        "description": "Minimal orbital hierarchy fixture",
        "total_cards": 3,
        "total_daemons": 0,
        "total_systems": 3,
        "total_connections": 2,
        "systems": [
            {
                "id": "A",
                "name": "Attractor",
                "ordinal": "001",
                "satellites": [{"from": "B", "type": "depends_on"}],
            },
            {
                "id": "B",
                "name": "Planet",
                "ordinal": "002",
                "depends_on_ids": ["A"],
                "satellites": [{"from": "C", "type": "depends_on"}],
            },
            {
                "id": "C",
                "name": "Satellite",
                "ordinal": "003",
                "depends_on_ids": ["B"],
                "satellites": [],
            },
        ],
        "connections": [
            {"from": "A", "to": "B", "type": "depends_on"},
            {"from": "B", "to": "C", "type": "depends_on"},
        ],
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def test_orbital_hierarchy_orders_layers_and_loads_memory_orbitally(tmp_path: Path) -> None:
    map_path = tmp_path / "system_map_v2.json"
    _write_map(map_path)

    hierarchy = OrbitalHierarchy(map_path=map_path)

    assert hierarchy.root_id == "A"
    assert [node.id for node in hierarchy.nodes] == ["A", "B", "C"]
    assert [node.layer for node in hierarchy.nodes] == ["attractor", "planet", "satellite"]
    assert layer_name_for_depth(3) == "sub-satellite"
    assert [node["id"] for node in orbit_load_order(map_path=map_path)] == ["A", "B", "C"]
    assert hierarchy.validate() == []


def test_orbital_hierarchy_renders_mermaid_flowchart(tmp_path: Path) -> None:
    map_path = tmp_path / "system_map_v2.json"
    _write_map(map_path)

    mermaid = render_orbital_mermaid(map_path=map_path)

    assert "flowchart TB" in mermaid
    assert '"A" --> "B"' in mermaid
    assert '"B" --> "C"' in mermaid
