"""Buildroot card DB generator and registry writer for NOEMA.

This module turns a Buildroot snapshot into two card surfaces:

* a dedicated Buildroot subregistry under ``cards/base/buildroot_nonlocal_db/``
* a bridge card in ``cards/base/noema_nonlocal_db/`` that points to that DB

The Buildroot DB is intentionally small and structured around the real
Buildroot tree: root, boot, linux, toolchain, system, filesystem, package
graph, and probe/benchmark surfaces.  The generator is deterministic and can
be run again whenever the Buildroot tree changes.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .buildroot_phasenav_probe import DEFAULT_BUILDROOT, summarize_buildroot

ROOT = Path(__file__).resolve().parent.parent.parent
MAIN_CARDS_DIR = ROOT / "cards" / "base" / "noema_nonlocal_db"
BUILDROOT_DB_DIR = ROOT / "cards" / "base" / "buildroot_nonlocal_db"
MAIN_BRIDGE_FILE = MAIN_CARDS_DIR / "047_BUILDROOT_CARD_DB.noema.card.json"
BUILDROOT_REGISTRY_FILE = BUILDROOT_DB_DIR / "registry.json"
SYSTEM_MAP_PATH = ROOT / "system_map_v2.json"

MAIN_BRIDGE_ID = "noema:nonlocal_db:047_BUILDROOT_CARD_DB"
MAIN_BRIDGE_ORBITAL_ID = "noema:card:047:buildroot_card_db"
MAIN_BRIDGE_LP = "38"

BUILDROOT_CARD_PREFIX = "noema:buildroot_db"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _slug(text: str) -> str:
    safe = text.lower().replace(" ", "_").replace("-", "_").replace(".", "_")
    while "__" in safe:
        safe = safe.replace("__", "_")
    return "".join(ch for ch in safe if ch.isalnum() or ch == "_").strip("_")


def _card_id(ordinal: str, name: str) -> str:
    return f"{BUILDROOT_CARD_PREFIX}:{ordinal}_{_slug(name)}"


def _card_file(ordinal: str, name: str) -> str:
    return f"{ordinal}_{_slug(name).upper()}.noema.card.json"


def _facet_specifications(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    top_dirs = snapshot.get("top_level_dirs", []) if isinstance(snapshot.get("top_level_dirs"), list) else []
    counts = snapshot.get("counts", {}) if isinstance(snapshot.get("counts"), dict) else {}
    menu_tree = snapshot.get("menu_tree", {}) if isinstance(snapshot.get("menu_tree"), dict) else {}
    top_menus = menu_tree.get("top_menus", []) if isinstance(menu_tree.get("top_menus"), list) else []
    package_dir_count = int(snapshot.get("package_dir_count", 0) or 0)
    sample_packages = snapshot.get("sample_packages", []) if isinstance(snapshot.get("sample_packages"), list) else []
    sample_configs = snapshot.get("sample_configs", []) if isinstance(snapshot.get("sample_configs"), list) else []
    semantic_subtrees = snapshot.get("semantic_subtrees", []) if isinstance(snapshot.get("semantic_subtrees"), list) else []

    menu_label = str(top_menus[0].get("label") if top_menus else "Package graph")
    menu_source_count = int(top_menus[0].get("source_count", 0) if top_menus else 0)

    specs: list[dict[str, Any]] = [
        {
            "ordinal": "001",
            "name": "BOOT",
            "title": "Buildroot boot chain",
            "role": "boot_chain",
            "summary": "Boot chain slice anchored on boot/Config.in and the startup surface.",
            "why": "Boot is the first continuity boundary for RT and recovery.",
            "source_paths": ["boot", "boot/Config.in"],
            "metrics": {"config_in": counts.get("config_in", 0), "menu_sources": 0},
            "orbital_lp": f"{MAIN_BRIDGE_LP}.01",
        },
        {
            "ordinal": "002",
            "name": "LINUX",
            "title": "Buildroot Linux kernel/runtime surface",
            "role": "kernel_runtime",
            "summary": "Kernel and runtime slice anchored on linux/Config.in and kernel-facing packages.",
            "why": "Linux determines runtime, drivers, and hardware continuity.",
            "source_paths": ["linux", "linux/Config.in"],
            "metrics": {"defconfig": counts.get("defconfig", 0), "patch": counts.get("patch", 0)},
            "orbital_lp": f"{MAIN_BRIDGE_LP}.02",
        },
        {
            "ordinal": "003",
            "name": "TOOLCHAIN",
            "title": "Buildroot toolchain and compiler surface",
            "role": "build_toolchain",
            "summary": "Toolchain slice anchored on toolchain/Config.in and compiler selection.",
            "why": "Toolchain stability drives reproducible images and code generation.",
            "source_paths": ["toolchain", "toolchain/Config.in"],
            "metrics": {"mk": counts.get("mk", 0), "hash": counts.get("hash", 0)},
            "orbital_lp": f"{MAIN_BRIDGE_LP}.03",
        },
        {
            "ordinal": "004",
            "name": "SYSTEM",
            "title": "Buildroot system control plane",
            "role": "control_plane",
            "summary": "System slice for init, supervision, runtime control and base system services.",
            "why": "System services bind boot, persistence, supervision and recovery.",
            "source_paths": ["system", "system/Config.in"],
            "metrics": {"service": counts.get("service", 0)},
            "orbital_lp": f"{MAIN_BRIDGE_LP}.04",
        },
        {
            "ordinal": "005",
            "name": "FS",
            "title": "Buildroot filesystem and image surface",
            "role": "filesystem_plane",
            "summary": "Filesystem slice anchored on fs/Config.in and image assembly paths.",
            "why": "Image and filesystem choices define deployment and recovery boundaries.",
            "source_paths": ["fs", "fs/Config.in"],
            "metrics": {"readme": counts.get("readme", 0)},
            "orbital_lp": f"{MAIN_BRIDGE_LP}.05",
        },
        {
            "ordinal": "006",
            "name": "PACKAGE_GRAPH",
            "title": "Buildroot package graph and menu tree",
            "role": "package_plane",
            "summary": f"Package/menu graph anchored on {menu_label} with {package_dir_count} packages.",
            "why": "Package graph is the main implementation surface for Buildroot cards.",
            "source_paths": ["package", "package/Config.in"],
            "metrics": {
                "package_dir_count": package_dir_count,
                "menu_count": int(menu_tree.get("menu_count", 0) or 0),
                "menu_source_count": menu_source_count,
            },
            "sample_packages": list(sample_packages[:16]),
            "sample_configs": list(sample_configs),
            "top_menu_labels": [str(node.get("label") or "") for node in top_menus[:8]],
            "semantic_subtrees": [str(node.get("name") or "") for node in semantic_subtrees[:8]],
            "orbital_lp": f"{MAIN_BRIDGE_LP}.06",
        },
        {
            "ordinal": "007",
            "name": "PROBE_BENCH",
            "title": "Buildroot PhaseNav probe and GGUF benchmark",
            "role": "analysis_surface",
            "summary": "Probe and benchmark surface for deterministic PhaseNav IR and optional GGUF translation.",
            "why": "The probe is the bridge between Buildroot snapshots and ResEnta RT synthesis.",
            "source_paths": ["src/ciel_sot_agent/buildroot_phasenav_probe.py"],
            "metrics": {
                "probe_schema": "ciel-sot-agent/buildroot-phasenav-probe/v0.1",
                "ir_schema": "ciel-sot-agent/buildroot-phasenav-ir/v0.1",
                "bench_schema": "ciel-sot-agent/buildroot-phasenav-benchmark/v0.1",
            },
            "orbital_lp": f"{MAIN_BRIDGE_LP}.07",
        },
    ]
    return specs


def _make_facet_card(snapshot: dict[str, Any], spec: dict[str, Any], *, root_paths: dict[str, str]) -> dict[str, Any]:
    ordinal = spec["ordinal"]
    name = spec["name"]
    title = spec["title"]
    card_id = _card_id(ordinal, name)
    depends_on = [f"{BUILDROOT_CARD_PREFIX}:000_root"]
    if name == "PROBE_BENCH":
        depends_on.extend(
            [
                f"{BUILDROOT_CARD_PREFIX}:001_boot",
                f"{BUILDROOT_CARD_PREFIX}:002_linux",
                f"{BUILDROOT_CARD_PREFIX}:003_toolchain",
                f"{BUILDROOT_CARD_PREFIX}:004_system",
                f"{BUILDROOT_CARD_PREFIX}:005_fs",
                f"{BUILDROOT_CARD_PREFIX}:006_package_graph",
            ]
        )

    focus_paths = list(spec.get("source_paths", []))
    metrics = dict(spec.get("metrics", {}))
    metrics["source_count"] = len(focus_paths)

    card = {
        "schema": "noema/card/v0.1",
        "id": card_id,
        "card_file": _card_file(ordinal, name),
        "title": title,
        "layer": "buildroot",
        "status": "active",
        "source_role": "buildroot_subregistry",
        "depends_on": depends_on,
        "description": spec["summary"],
        "meaning": {
            "summary": spec["summary"],
            "role": spec["role"],
            "boundary": "This card is a buildroot facet. It summarises one stable slice of the Buildroot tree and does not claim runtime writes.",
            "why": spec["why"],
        },
        "interfaces": {
            "generator": "ciel_sot_agent.buildroot_card_db:main",
            "probe_module": "src/ciel_sot_agent/buildroot_phasenav_probe.py",
            "probe_command": "ciel-sot-buildroot-phase-probe",
            "source_root": root_paths["buildroot_root"],
            "registry_root": str(BUILDROOT_DB_DIR.relative_to(ROOT)),
        },
        "runtime_semantics": {
            "source_paths": focus_paths,
            "metrics": metrics,
        },
        "orbital_ref": {
            "orbital_map": "system_map_v2.json",
            "lp": spec["orbital_lp"],
            "name": title,
            "id": card_id,
        },
        "card_id": card_id,
        "card_type": "module" if name != "PROBE_BENCH" else "analysis",
        "ordinal": ordinal,
        "ordinal_name": _slug(name),
    }
    if name == "PACKAGE_GRAPH":
        card["runtime_semantics"]["package_dir_count"] = int(spec.get("metrics", {}).get("package_dir_count", 0) or 0)
        card["runtime_semantics"]["menu_count"] = int(spec.get("metrics", {}).get("menu_count", 0) or 0)
        card["runtime_semantics"]["top_menu_labels"] = spec.get("top_menu_labels", [])
        card["runtime_semantics"]["sample_packages"] = spec.get("sample_packages", [])
        card["runtime_semantics"]["sample_configs"] = spec.get("sample_configs", [])
        card["runtime_semantics"]["semantic_subtrees"] = spec.get("semantic_subtrees", [])
    if name == "PROBE_BENCH":
        card["runtime_semantics"]["probe_notes"] = [
            "Deterministic IR fallback remains canonical.",
            "GGUF is optional and only augments the probe when available.",
            "Benchmark compares deterministic vs GGUF quality/latency.",
        ]
    return card


def _make_root_card(snapshot: dict[str, Any], *, root_paths: dict[str, str]) -> dict[str, Any]:
    top_level_dirs = snapshot.get("top_level_dirs", []) if isinstance(snapshot.get("top_level_dirs"), list) else []
    counts = snapshot.get("counts", {}) if isinstance(snapshot.get("counts"), dict) else {}
    facets = [
        "001_BOOT",
        "002_LINUX",
        "003_TOOLCHAIN",
        "004_SYSTEM",
        "005_FS",
        "006_PACKAGE_GRAPH",
        "007_PROBE_BENCH",
    ]
    card_id = _card_id("000", "ROOT")
    return {
        "schema": "noema/card/v0.1",
        "id": card_id,
        "title": "Buildroot root — package tree, boot chain, RT, recovery",
        "layer": "buildroot",
        "status": "active",
        "source_role": "buildroot_snapshot_root",
        "depends_on": [f"{BUILDROOT_CARD_PREFIX}:{ordinal.lower()}" for ordinal in facets],
        "description": (
            "Canonical Buildroot snapshot for NOEMA: top-level dirs, menu tree, package volume, "
            "boot continuity, and GGUF fallback."
        ),
        "meaning": {
            "summary": (
                "Root card for the Buildroot NOEMA DB. It gathers the actual Buildroot tree "
                "snapshot, the section cards, and the probe/benchmark surface."
            ),
            "role": "buildroot_root",
            "boundary": "Read-only snapshot of the Buildroot tree. The card DB documents the tree; it does not mutate it.",
            "why": "Buildroot is the most direct host for a vectorized RT image and needs a stable card anchor before implementation work starts.",
        },
        "interfaces": {
            "generator": "ciel_sot_agent.buildroot_card_db:main",
            "probe_module": "src/ciel_sot_agent/buildroot_phasenav_probe.py",
            "probe_command": "ciel-sot-buildroot-phase-probe",
            "bridge_command": "ciel-sot-buildroot-card-db",
            "registry_root": str(BUILDROOT_DB_DIR.relative_to(ROOT)),
            "main_bridge_card": str(MAIN_BRIDGE_FILE.relative_to(ROOT)),
        },
        "runtime_semantics": {
            "buildroot_root": root_paths["buildroot_root"],
            "top_level_dirs": list(top_level_dirs),
            "counts": counts,
            "package_dir_count": snapshot.get("package_dir_count", 0),
            "sample_packages": list(snapshot.get("sample_packages", [])[:16]),
            "sample_configs": list(snapshot.get("sample_configs", [])),
            "rt_surface": snapshot.get("rt_surface", {}),
            "facet_cards": facets,
        },
        "orbital_ref": {
            "orbital_map": "system_map_v2.json",
            "lp": MAIN_BRIDGE_LP,
            "name": "Buildroot Card DB — snapshots, PhaseNav, GGUF, ResEnta RT",
            "id": MAIN_BRIDGE_ORBITAL_ID,
        },
        "card_id": card_id,
        "card_type": "database",
    }


def _make_main_bridge_card(snapshot: dict[str, Any], registry: dict[str, Any], *, root_paths: dict[str, str]) -> dict[str, Any]:
    top_level_dirs = snapshot.get("top_level_dirs", []) if isinstance(snapshot.get("top_level_dirs"), list) else []
    counts = snapshot.get("counts", {}) if isinstance(snapshot.get("counts"), dict) else {}
    menu_tree = snapshot.get("menu_tree", {}) if isinstance(snapshot.get("menu_tree"), dict) else {}
    package_dir_count = int(snapshot.get("package_dir_count", 0) or 0)
    menu_count = int(menu_tree.get("menu_count", 0) or 0)
    return {
        "id": "047_BUILDROOT_CARD_DB",
        "title": "Buildroot Card DB — snapshots, PhaseNav, GGUF, ResEnta RT",
        "schema": "noema/card/v0.1",
        "priority": 47,
        "epistemic_status": "bridge_card; deterministic Buildroot snapshot registry with optional GGUF translation",
        "depends_on": [
            "noema:nonlocal_db:046_WORKBEN-DEV",
            "noema:nonlocal_db:043_WORKBEN-LINUX",
            "noema:nonlocal_db:037_WORKBEN-SYSTEM",
        ],
        "meaning": {
            "summary": (
                "Bridge card for a dedicated Buildroot card database. It exposes the generated "
                "subregistry, the Buildroot probe, and the RT-oriented slices used by NOEMA."
            ),
            "role": "buildroot_card_db",
            "boundary": "Read-only DB bridge. The Buildroot tree itself remains external; NOEMA keeps only the generated card surface and probes.",
            "why": "Having Buildroot cards as first-class NOEMA artifacts makes ResEnta RT implementation much easier to reason about and test.",
        },
        "interfaces": {
            "runtime_file": "src/ciel_sot_agent/buildroot_card_db.py",
            "generator_command": "ciel-sot-buildroot-card-db",
            "probe_module": "src/ciel_sot_agent/buildroot_phasenav_probe.py",
            "probe_command": "ciel-sot-buildroot-phase-probe",
            "subregistry": str(BUILDROOT_REGISTRY_FILE.relative_to(ROOT)),
            "buildroot_root": root_paths["buildroot_root"],
        },
        "index_policy": {
            "metadata_for": "Buildroot directories, menu tree, package graph and probe/benchmark slices",
            "canonical_source": "Buildroot tree plus deterministic snapshot",
            "fallback": "Deterministic probe output if GGUF is absent",
        },
        "runtime_semantics": {
            "top_level_dirs": list(top_level_dirs),
            "counts": counts,
            "package_dir_count": package_dir_count,
            "menu_count": menu_count,
            "facet_count": len(registry.get("cards", [])),
        },
        "doctor_hooks": [
            "missing_buildroot_card",
            "package_graph_drift",
            "menu_tree_drift",
            "rt_surface_gap",
            "gguf_fallback_only",
        ],
        "status": "active_candidate",
        "orbital_ref": {
            "orbital_map": "system_map_v2.json",
            "lp": MAIN_BRIDGE_LP,
            "name": "Buildroot Card DB — snapshots, PhaseNav, GGUF, ResEnta RT",
            "id": MAIN_BRIDGE_ORBITAL_ID,
        },
        "card_file": str(MAIN_BRIDGE_FILE.relative_to(ROOT)),
        "card_id": MAIN_BRIDGE_ID,
        "card_type": "database",
    }


def build_buildroot_card_bundle(buildroot_root: str | Path) -> dict[str, Any]:
    root = Path(buildroot_root)
    snapshot = summarize_buildroot(root)
    root_paths = {"buildroot_root": str(root)}
    specs = _facet_specifications(snapshot)
    facet_cards = [_make_facet_card(snapshot, spec, root_paths=root_paths) for spec in specs]
    root_card = _make_root_card(snapshot, root_paths=root_paths)
    registry_cards = [
        {
            "prefix": "000",
            "file": "000_ROOT.noema.card.json",
            "card_id": root_card["card_id"],
            "title": root_card["title"],
            "card_type": root_card["card_type"],
            "ordinal": "0",
            "role": "root",
        },
    ]
    for spec in specs:
        ordinal = spec["ordinal"]
        registry_cards.append(
            {
                "prefix": ordinal,
                "file": _card_file(ordinal, spec["name"]),
                "card_id": _card_id(ordinal, spec["name"]),
                "title": spec["title"],
                "card_type": "analysis" if spec["name"] == "PROBE_BENCH" else "module",
                "ordinal": int(ordinal),
                "role": spec["role"],
            }
        )

    registry = {
        "registry_id": "noema:buildroot_nonlocal_db:registry:v0.1",
        "title": "NOEMA Buildroot Card DB",
        "description": (
            "Generated Buildroot card database derived from the live Buildroot tree and "
            "the PhaseNav probe/benchmark helpers."
        ),
        "source_root": str(root),
        "generated_at": _now(),
        "generated_by": "ciel_sot_agent.buildroot_card_db",
        "main_bridge_card": str(MAIN_BRIDGE_FILE.relative_to(ROOT)),
        "root_card": "000_ROOT.noema.card.json",
        "cards": registry_cards,
        "summary": {
            "top_level_dirs": list(snapshot.get("top_level_dirs", [])),
            "package_dir_count": snapshot.get("package_dir_count", 0),
            "menu_count": snapshot.get("menu_tree", {}).get("menu_count", 0) if isinstance(snapshot.get("menu_tree"), dict) else 0,
            "semantic_subtree_count": len(snapshot.get("semantic_subtrees", [])) if isinstance(snapshot.get("semantic_subtrees"), list) else 0,
        },
    }

    system_map_record = _make_system_map_record(root_card, facet_cards, snapshot, root_paths=root_paths)
    connections = _make_system_map_connections(root_card)

    return {
        "snapshot": snapshot,
        "root_card": root_card,
        "facet_cards": facet_cards,
        "registry": registry,
        "main_bridge_card": _make_main_bridge_card(snapshot, registry, root_paths=root_paths),
        "system_map_record": system_map_record,
        "system_map_connections": connections,
    }


def _make_system_map_record(
    root_card: dict[str, Any],
    facet_cards: list[dict[str, Any]],
    snapshot: dict[str, Any],
    *,
    root_paths: dict[str, str],
) -> dict[str, Any]:
    subsystems = []
    for card in facet_cards:
        orbital_ref = card.get("orbital_ref", {})
        subsystems.append(
            {
                "id": card.get("card_id"),
                "name": card.get("title"),
                "type": card.get("card_type"),
                "status": card.get("status", "active"),
                "parent_ordinal": str(orbital_ref.get("lp") or MAIN_BRIDGE_LP),
                "card_ref": "047_BUILDROOT_CARD_DB",
            }
        )

    satellites = [
        {
            "from": "ciel-sot-buildroot-card-db",
            "type": "generated_by",
            "protocol": "cli",
            "desc": "Buildroot card DB generator command",
        },
        {
            "from": "ciel-sot-buildroot-phase-probe",
            "type": "probe_surface",
            "protocol": "cli",
            "desc": "Buildroot PhaseNav probe and benchmark surface",
        },
    ]
    return {
        "id": MAIN_BRIDGE_ORBITAL_ID,
        "name": root_card["title"],
        "type": "database",
        "layer": "buildroot",
        "status": "active",
        "description": root_card["meaning"]["summary"],
        "port": None,
        "runtime_file": "src/ciel_sot_agent/buildroot_card_db.py",
        "sources": [
            "cards/base/buildroot_nonlocal_db/registry.json",
            "src/ciel_sot_agent/buildroot_phasenav_probe.py",
        ],
        "api_endpoints": [],
        "depends_on_ids": [
            "noema:workben:46:workben-dev",
            "noema:workben:43:workben-linux",
            "noema:workben:37:workben-system",
        ],
        "runtime_hooks": [
            "ciel-sot-buildroot-card-db",
            "ciel-sot-buildroot-phase-probe",
        ],
        "card_file": str(MAIN_BRIDGE_FILE.relative_to(ROOT)),
        "protocols": ["json", "card"],
        "ordinal": MAIN_BRIDGE_LP,
        "ordinal_name": "buildroot-card-db",
        "subsystems": subsystems,
        "satellites": satellites,
    }


def _make_system_map_connections(root_card: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "from": MAIN_BRIDGE_ORBITAL_ID,
            "to": "noema:workben:46:workben-dev",
            "type": "depends_on",
            "protocol": "card_ref",
            "description": "Buildroot Card DB zależy od Workben DEV",
            "path": "",
            "weight": 0.85,
        },
        {
            "from": MAIN_BRIDGE_ORBITAL_ID,
            "to": "noema:workben:43:workben-linux",
            "type": "depends_on",
            "protocol": "card_ref",
            "description": "Buildroot Card DB zależy od Workben LINUX",
            "path": "",
            "weight": 0.72,
        },
        {
            "from": MAIN_BRIDGE_ORBITAL_ID,
            "to": "noema:workben:37:workben-system",
            "type": "depends_on",
            "protocol": "card_ref",
            "description": "Buildroot Card DB zależy od Workben SYSTEM",
            "path": "",
            "weight": 0.75,
        },
    ]


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _upsert_main_registry(main_bridge_card: dict[str, Any]) -> dict[str, Any]:
    registry = _load_json(MAIN_CARDS_DIR / "registry.json")
    if not registry:
        registry = {
            "registry_id": "noema:nonlocal_db:registry:v0.2",
            "title": "NOEMA Nonlocal DB Master Registry",
            "description": "Master index of all NOEMA nonlocal database cards.",
            "total_cards": 0,
            "updated": _now().split("T", 1)[0],
            "cards": [],
            "gaps": [],
            "anomalies": [],
            "schemas_in_use": {},
        }

    cards = registry.setdefault("cards", [])
    file_name = Path(main_bridge_card["card_file"]).name
    existing = None
    for idx, card in enumerate(cards):
        if card.get("prefix") == "047" or card.get("file") == file_name or card.get("card_id") == main_bridge_card["card_id"]:
            existing = idx
            break

    entry = {
        "prefix": "047",
        "file": file_name,
        "card_id": main_bridge_card["card_id"],
        "schema": main_bridge_card["schema"],
        "title": main_bridge_card["title"],
        "layer": main_bridge_card["status"] and "buildroot",
        "status": main_bridge_card["status"],
        "priority": main_bridge_card.get("priority"),
    }
    if existing is None:
        cards.append(entry)
    else:
        cards[existing] = entry

    def _prefix_key(item: dict[str, Any]) -> tuple[int, str]:
        raw = str(item.get("prefix") or "999")
        try:
            return int(raw), raw
        except Exception:
            return 999, raw

    cards.sort(key=_prefix_key)
    registry["total_cards"] = len(cards)
    registry["updated"] = _now().split("T", 1)[0]
    registry["last_update"] = _now()
    return registry


def _upsert_system_map(system_map_record: dict[str, Any], connections: list[dict[str, Any]]) -> dict[str, Any]:
    payload = _load_json(SYSTEM_MAP_PATH)
    if not payload:
        payload = {
            "version": 3,
            "date": _now().split("T", 1)[0],
            "author": "Adrian Lipa",
            "description": "NOEMA system map",
            "total_cards": 0,
            "total_daemons": 0,
            "total_systems": 0,
            "total_connections": 0,
            "systems": [],
            "connections": [],
        }

    systems = payload.setdefault("systems", [])
    connections_payload = payload.setdefault("connections", [])

    existing = None
    for idx, system in enumerate(systems):
        if system.get("id") == system_map_record["id"]:
            existing = idx
            break
    if existing is None:
        insert_at = None
        for idx, system in enumerate(systems):
            if system.get("id") == "noema:workben:46:workben-dev":
                insert_at = idx + 1
                break
        if insert_at is None:
            systems.append(system_map_record)
        else:
            systems.insert(insert_at, system_map_record)
    else:
        systems[existing] = system_map_record

    existing_connections = {
        (c.get("from"), c.get("to"), c.get("protocol"), c.get("type"))
        for c in connections_payload
        if isinstance(c, dict)
    }
    for connection in connections:
        key = (connection.get("from"), connection.get("to"), connection.get("protocol"), connection.get("type"))
        if key not in existing_connections:
            connections_payload.append(connection)
            existing_connections.add(key)

    payload["total_systems"] = len(systems)
    payload["total_connections"] = len(connections_payload)
    payload["date"] = _now().split("T", 1)[0]
    return payload


def write_buildroot_card_bundle(
    bundle: dict[str, Any],
    *,
    update_main_registry: bool = True,
    update_system_map: bool = True,
) -> dict[str, Any]:
    BUILDROOT_DB_DIR.mkdir(parents=True, exist_ok=True)
    MAIN_CARDS_DIR.mkdir(parents=True, exist_ok=True)

    _write_json(BUILDROOT_DB_DIR / "000_ROOT.noema.card.json", bundle["root_card"])
    for card in bundle["facet_cards"]:
        _write_json(BUILDROOT_DB_DIR / card["card_file"], card)

    _write_json(BUILDROOT_REGISTRY_FILE, bundle["registry"])
    _write_json(MAIN_BRIDGE_FILE, bundle["main_bridge_card"])

    if update_main_registry:
        main_registry = _upsert_main_registry(bundle["main_bridge_card"])
        _write_json(MAIN_CARDS_DIR / "registry.json", main_registry)
    if update_system_map:
        system_map = _upsert_system_map(bundle["system_map_record"], bundle["system_map_connections"])
        _write_json(SYSTEM_MAP_PATH, system_map)

    return {
        "buildroot_registry": str(BUILDROOT_REGISTRY_FILE.relative_to(ROOT)),
        "main_bridge_card": str(MAIN_BRIDGE_FILE.relative_to(ROOT)),
        "updated_main_registry": update_main_registry,
        "updated_system_map": update_system_map,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate the Buildroot NOEMA card DB.")
    parser.add_argument("--buildroot", type=Path, default=DEFAULT_BUILDROOT, help="Path to the Buildroot tree.")
    parser.add_argument("--no-main-registry", action="store_true", help="Do not update cards/base/noema_nonlocal_db/registry.json.")
    parser.add_argument("--no-system-map", action="store_true", help="Do not update system_map_v2.json.")
    parser.add_argument("--dry-run", action="store_true", help="Print the generated bundle as JSON and do not write files.")
    args = parser.parse_args(argv)

    bundle = build_buildroot_card_bundle(args.buildroot)
    if args.dry_run:
        print(json.dumps(bundle["registry"], indent=2, ensure_ascii=False))
        return 0

    result = write_buildroot_card_bundle(
        bundle,
        update_main_registry=not args.no_main_registry,
        update_system_map=not args.no_system_map,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
