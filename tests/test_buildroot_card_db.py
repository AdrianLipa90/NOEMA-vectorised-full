from __future__ import annotations

import json
from pathlib import Path

from ciel_sot_agent import buildroot_card_db


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _make_buildroot_tree(root: Path) -> None:
    for rel in [
        "boot",
        "linux",
        "toolchain",
        "system",
        "fs",
        "package",
    ]:
        (root / rel).mkdir(parents=True, exist_ok=True)

    _write_text(root / "boot" / "Config.in", 'menu "Boot"\nsource "boot/one.in"\nendmenu\n')
    _write_text(root / "linux" / "Config.in", 'menu "Linux"\nsource "linux/one.in"\nendmenu\n')
    _write_text(root / "toolchain" / "Config.in", 'menu "Toolchain"\nsource "toolchain/one.in"\nendmenu\n')
    _write_text(root / "system" / "Config.in", 'menu "System"\nsource "system/one.in"\nendmenu\n')
    _write_text(root / "fs" / "Config.in", 'menu "FS"\nsource "fs/one.in"\nendmenu\n')
    _write_text(
        root / "package" / "Config.in",
        'menu "Target packages"\nsource "package/foo/Config.in"\nsource "package/bar/Config.in"\nendmenu\n',
    )
    _write_text(root / "Config.in", 'source "package/Config.in"\n')
    _write_text(root / "package" / "foo" / "Config.in", 'config FOO\n')
    _write_text(root / "package" / "bar" / "Config.in", 'config BAR\n')


def test_buildroot_card_bundle_has_facets(tmp_path: Path) -> None:
    buildroot_root = tmp_path / "buildroot"
    _make_buildroot_tree(buildroot_root)

    bundle = buildroot_card_db.build_buildroot_card_bundle(buildroot_root)

    assert bundle["registry"]["registry_id"] == "noema:buildroot_nonlocal_db:registry:v0.1"
    assert len(bundle["facet_cards"]) == 7
    assert bundle["root_card"]["card_id"] == "noema:buildroot_db:000_root"
    assert bundle["main_bridge_card"]["card_id"] == "noema:nonlocal_db:047_BUILDROOT_CARD_DB"
    assert bundle["main_bridge_card"]["interfaces"]["subregistry"].endswith("buildroot_nonlocal_db/registry.json")
    assert bundle["facet_cards"][5]["runtime_semantics"]["package_dir_count"] == 2
    assert bundle["facet_cards"][6]["card_type"] == "analysis"


def test_buildroot_card_db_writer_updates_registry_and_system_map(tmp_path: Path, monkeypatch) -> None:
    repo_root = tmp_path / "repo"
    buildroot_root = tmp_path / "buildroot"
    _make_buildroot_tree(buildroot_root)

    main_cards_dir = repo_root / "cards" / "base" / "noema_nonlocal_db"
    main_cards_dir.mkdir(parents=True, exist_ok=True)
    _write_json(
        main_cards_dir / "registry.json",
        {
            "registry_id": "noema:nonlocal_db:registry:v0.2",
            "title": "NOEMA Nonlocal DB Master Registry",
            "description": "test registry",
            "total_cards": 0,
            "updated": "2026-01-01",
            "cards": [],
            "gaps": [],
            "anomalies": [],
            "schemas_in_use": {},
            "last_update": "2026-01-01T00:00:00Z",
        },
    )
    _write_json(
        repo_root / "system_map_v2.json",
        {
            "version": 3,
            "date": "2026-01-01",
            "author": "Adrian Lipa",
            "description": "test system map",
            "total_cards": 0,
            "total_daemons": 0,
            "total_systems": 3,
            "total_connections": 0,
            "systems": [
                {"id": "noema:workben:37:workben-system", "name": "Workben SYSTEM", "ordinal": "28"},
                {"id": "noema:workben:43:workben-linux", "name": "Workben LINUX", "ordinal": "34"},
                {"id": "noema:workben:46:workben-dev", "name": "Workben DEV", "ordinal": "37"},
            ],
            "connections": [],
        },
    )

    monkeypatch.setattr(buildroot_card_db, "ROOT", repo_root)
    monkeypatch.setattr(buildroot_card_db, "MAIN_CARDS_DIR", main_cards_dir)
    monkeypatch.setattr(buildroot_card_db, "BUILDROOT_DB_DIR", repo_root / "cards" / "base" / "buildroot_nonlocal_db")
    monkeypatch.setattr(buildroot_card_db, "BUILDROOT_REGISTRY_FILE", repo_root / "cards" / "base" / "buildroot_nonlocal_db" / "registry.json")
    monkeypatch.setattr(buildroot_card_db, "MAIN_BRIDGE_FILE", main_cards_dir / "047_BUILDROOT_CARD_DB.noema.card.json")
    monkeypatch.setattr(buildroot_card_db, "SYSTEM_MAP_PATH", repo_root / "system_map_v2.json")

    bundle = buildroot_card_db.build_buildroot_card_bundle(buildroot_root)
    result = buildroot_card_db.write_buildroot_card_bundle(bundle)

    assert (repo_root / "cards" / "base" / "buildroot_nonlocal_db" / "registry.json").exists()
    assert (repo_root / "cards" / "base" / "buildroot_nonlocal_db" / "000_ROOT.noema.card.json").exists()
    assert (repo_root / "cards" / "base" / "buildroot_nonlocal_db" / "006_PACKAGE_GRAPH.noema.card.json").exists()
    assert (main_cards_dir / "047_BUILDROOT_CARD_DB.noema.card.json").exists()
    assert result["updated_main_registry"] is True
    assert result["updated_system_map"] is True

    main_registry = json.loads((main_cards_dir / "registry.json").read_text(encoding="utf-8"))
    assert main_registry["total_cards"] == 1
    assert main_registry["cards"][0]["card_id"] == "noema:nonlocal_db:047_BUILDROOT_CARD_DB"

    system_map = json.loads((repo_root / "system_map_v2.json").read_text(encoding="utf-8"))
    assert system_map["total_systems"] == 4
    assert system_map["total_connections"] == 3
    assert any(item["id"] == "noema:card:047:buildroot_card_db" for item in system_map["systems"])
