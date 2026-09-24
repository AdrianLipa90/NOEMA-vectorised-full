"""Buildroot -> PhaseNav probe and benchmark helpers for ResEnta RT."""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
from pathlib import Path
from statistics import median
from typing import Any, Callable

from ciel_geometry.weighting import canonical_weighting
from ciel_geometry.paths import P

from .gguf_manager import get_model_path

log = logging.getLogger(__name__)

PROBE_SCHEMA_V01 = "ciel-sot-agent/buildroot-phasenav-probe/v0.1"
IR_SCHEMA_V01 = "ciel-sot-agent/buildroot-phasenav-ir/v0.1"
BENCH_SCHEMA_V01 = "ciel-sot-agent/buildroot-phasenav-benchmark/v0.1"
DEFAULT_BUILDROOT = Path("/media/adrian/REPOZYTORIA_GIT1/NOEMA_REPOS_CLEAN/buildroot")
DEFAULT_SYSTEM_MAP_CANDIDATES = (
    Path(P.NOEMA) / "system_map_v2.json",
)

BUILDROOT_TOPLEVEL_SEMANTICS: dict[str, dict[str, Any]] = {
    "boot": {
        "role": "boot_chain",
        "query_terms": ("boot", "startup", "root", "surface"),
    },
    "linux": {
        "role": "kernel_runtime",
        "query_terms": ("linux", "kernel", "daemon", "sensor", "workben-linux"),
    },
    "toolchain": {
        "role": "build_toolchain",
        "query_terms": ("toolchain", "compiler", "build", "dev", "workben-dev"),
    },
    "system": {
        "role": "control_plane",
        "query_terms": ("system", "surface", "registry", "workben-system"),
    },
    "fs": {
        "role": "filesystem_plane",
        "query_terms": ("filesystem", "flash", "storage", "image", "workben-system"),
    },
    "package": {
        "role": "package_plane",
        "query_terms": ("package", "project", "module", "workben-dev"),
    },
}

BUILDROOT_MENU_SEMANTICS: tuple[tuple[str, tuple[str, ...], str], ...] = (
    ("target packages", ("project", "package", "module", "workben-dev"), "package_root"),
    ("development tools", ("development", "tools", "build", "workben-dev"), "dev_tooling"),
    ("debugging, profiling and benchmark", ("debugging", "profiling", "benchmark", "workben-dev"), "validation"),
    ("filesystem and flash utilities", ("filesystem", "flash", "storage", "workben-system"), "storage"),
    ("hardware handling", ("hardware", "sensor", "linux", "workben-linux"), "hardware"),
    ("firmware", ("firmware", "boot", "linux", "workben-linux"), "firmware"),
    ("interpreter languages and scripting", ("interpreter", "scripting", "language", "workben-dev"), "runtime_lang"),
    ("libraries", ("libraries", "library", "workben-dev"), "libraries"),
    ("compression", ("compress", "archive", "zip", "workben-system"), "compression"),
)

BUILDROOT_WORKBEN_TARGETS: dict[str, dict[str, Any]] = {
    "workben-system": {
        "semantic_role": "control_plane",
        "query_terms": ("workben-system", "surface", "registry", "euler", "synchronizacja"),
    },
    "workben-linux": {
        "semantic_role": "kernel_runtime",
        "query_terms": ("workben-linux", "linux", "sensor", "ebpf", "hardware"),
    },
    "workben-dev": {
        "semantic_role": "build_toolchain",
        "query_terms": ("workben-dev", "pipeline", "build", "codegen", "debug"),
    },
}

_ROOT = Path(__file__).resolve().parents[1]
_OMEGA_ROOT = _ROOT / "CIEL_OMEGA_COMPLETE_SYSTEM"
if _OMEGA_ROOT.exists():
    text = str(_OMEGA_ROOT)
    if text not in sys.path:
        sys.path.insert(0, text)


def _clamp01(value: Any, default: float = 0.0) -> float:
    try:
        return max(0.0, min(1.0, float(value)))
    except Exception:
        return float(default)


def _normalize_label(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(text).lower()).strip()


def _parse_json_object(text: str) -> dict[str, Any]:
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = text[start : end + 1]
        try:
            return json.loads(candidate)
        except Exception:
            log.debug("buildroot_phasenav_probe.py:107 candidate JSON slice failed to parse, falling back to raw text", exc_info=True)
    return {"raw": text.strip()}


def _iter_system_map_records(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return []
    for key in ("systems", "records", "nodes", "items", "subsystems"):
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    nested_records = [value for value in payload.values() if isinstance(value, dict)]
    if nested_records and len(nested_records) <= 256:
        return nested_records
    return []


def _record_text_fields(record: dict[str, Any]) -> list[str]:
    fields: list[str] = []
    for key in (
        "id",
        "name",
        "label",
        "slug",
        "path",
        "ordinal",
        "ordinal_name",
        "type",
        "kind",
        "description",
        "orbital_ref",
        "canonical_ref",
        "card_ref",
        "search_text",
    ):
        value = record.get(key)
        if value is None:
            continue
        text = str(value).strip().lower()
        if text:
            fields.append(text)
    return fields


def _record_names(record: dict[str, Any]) -> list[str]:
    names: list[str] = []
    for key in ("name", "id", "label", "slug", "path", "orbital_ref", "canonical_ref"):
        value = record.get(key)
        if value is None:
            continue
        text = str(value).strip()
        if text:
            names.append(text)
            names.append(text.split("/")[-1])
            names.append(text.split("#")[-1])
    return list(dict.fromkeys(names))


def _match_system_map_records(query: str, records: list[dict[str, Any]], *, limit: int = 3) -> list[dict[str, Any]]:
    token = re.sub(r"[^a-z0-9]+", " ", str(query).lower()).strip()
    if not token:
        return []
    query_terms = [part for part in token.split() if part]
    scored: list[tuple[int, dict[str, Any]]] = []
    for record in records:
        fields = _record_text_fields(record)
        if not fields:
            continue
        score = 0
        for term in query_terms:
            if any(field == term for field in fields):
                score = max(score, 3)
            elif any(term in field or field in term for field in fields):
                score = max(score, 2)
        if score:
            scored.append((score, record))
    scored.sort(
        key=lambda item: (
            -item[0],
            str(item[1].get("ordinal") or item[1].get("id") or item[1].get("name") or ""),
        )
    )
    matches: list[dict[str, Any]] = []
    for _, record in scored[:limit]:
        matches.append(_summarize_system_map_record(record))
    return matches


def _summarize_system_map_record(record: dict[str, Any]) -> dict[str, Any]:
    subsystems = record.get("subsystems")
    satellites = record.get("satellites")
    description = str(record.get("description") or "").strip()
    search_parts = [
        str(record.get("id") or ""),
        str(record.get("name") or ""),
        str(record.get("ordinal") or ""),
        str(record.get("ordinal_name") or ""),
        str(record.get("type") or ""),
        str(record.get("kind") or ""),
        str(record.get("card_ref") or ""),
        description,
    ]
    if isinstance(satellites, list):
        for sat in satellites[:8]:
            if isinstance(sat, dict):
                search_parts.extend(
                    [
                        str(sat.get("from") or ""),
                        str(sat.get("type") or ""),
                        str(sat.get("protocol") or ""),
                        str(sat.get("desc") or ""),
                    ]
                )
    return {
        "id": record.get("id"),
        "name": record.get("name"),
        "ordinal": record.get("ordinal"),
        "ordinal_name": record.get("ordinal_name"),
        "type": record.get("type"),
        "kind": record.get("kind"),
        "description": description[:240] if description else None,
        "lp": record.get("lp") or record.get("ordinal") or record.get("order"),
        "satellite_count": len(satellites) if isinstance(satellites, list) else 0,
        "subsystem_count": len(subsystems) if isinstance(subsystems, list) else 0,
        "search_text": " ".join(part for part in search_parts if part).lower(),
    }


def _parse_buildroot_menu_tree(root: Path) -> dict[str, Any]:
    path = root / "package" / "Config.in"
    if not path.exists():
        return {
            "exists": False,
            "path": str(path),
            "menu_count": 0,
            "source_count": 0,
            "top_menus": [],
        }

    top_menus: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    stack: list[dict[str, Any]] = []
    source_count = 0
    menu_depth = 0
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception:
        lines = []

    for raw in lines:
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("menu "):
            label = stripped.split("\"", 2)[1] if "\"" in stripped else stripped[5:].strip()
            node = {
                "label": label,
                "kind": "menu",
                "depth": menu_depth,
                "direct_sources": [],
                "source_count": 0,
                "query_terms": [],
            }
            if stack:
                stack[-1].setdefault("children", []).append(node)
            else:
                top_menus.append(node)
            stack.append(node)
            current = node
            menu_depth += 1
            continue
        if stripped.startswith("endmenu"):
            if stack:
                stack.pop()
            menu_depth = max(0, menu_depth - 1)
            current = stack[-1] if stack else None
            continue
        if stripped.startswith("source "):
            source = stripped.split("\"", 2)[1] if "\"" in stripped else stripped[6:].strip()
            source_count += 1
            if current is not None:
                current["direct_sources"].append(source)
                current["source_count"] = len(current["direct_sources"])
            continue
        if current is not None:
            current["body_lines"] = int(current.get("body_lines", 0)) + 1

    def _finalize(node: dict[str, Any]) -> None:
        label = str(node.get("label") or "")
        node["query_terms"] = _build_query_terms(label, node.get("kind", "menu"))
        children = node.get("children")
        if isinstance(children, list):
            for child in children:
                if isinstance(child, dict):
                    _finalize(child)

    for node in top_menus:
        _finalize(node)

    return {
        "exists": True,
        "path": str(path),
        "menu_count": len(top_menus),
        "source_count": source_count,
        "top_menus": top_menus,
    }


def _build_query_terms(label: str, kind: str = "menu") -> list[str]:
    token = _normalize_label(label)
    terms = [part for part in token.split() if part]
    if kind == "dir":
        extra = BUILDROOT_TOPLEVEL_SEMANTICS.get(label.lower(), {}).get("query_terms", ())
        terms.extend(extra)
    for menu_label, aliases, _semantic_role in BUILDROOT_MENU_SEMANTICS:
        if _normalize_label(menu_label) in token:
            terms.extend(aliases)
            break
    return list(dict.fromkeys(terms))


def _build_semantic_subtrees(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    top_level = snapshot.get("top_level_dirs", []) if isinstance(snapshot.get("top_level_dirs"), list) else []
    menu_tree = snapshot.get("menu_tree", {}) if isinstance(snapshot.get("menu_tree"), dict) else {}
    top_menus = menu_tree.get("top_menus", []) if isinstance(menu_tree.get("top_menus"), list) else []
    nodes: list[dict[str, Any]] = []

    for name in top_level:
        label = str(name)
        semantics = BUILDROOT_TOPLEVEL_SEMANTICS.get(label.lower(), {})
        nodes.append(
            {
                "kind": "dir",
                "name": label,
                "semantic_role": semantics.get("role", "subtree"),
                "source_count": 0,
                "query_terms": _build_query_terms(label, "dir"),
            }
        )

    for menu in top_menus:
        if not isinstance(menu, dict):
            continue
        label = str(menu.get("label") or "").strip()
        if not label:
            continue
        semantic_role = "package_menu"
        query_terms = list(menu.get("query_terms", []))
        lowered = _normalize_label(label)
        for menu_label, aliases, role in BUILDROOT_MENU_SEMANTICS:
            if _normalize_label(menu_label) in lowered:
                semantic_role = role
                query_terms.extend(aliases)
                break
        nodes.append(
            {
                "kind": "menu",
                "name": label,
                "semantic_role": semantic_role,
                "source_count": int(menu.get("source_count", 0) or 0),
                "query_terms": list(dict.fromkeys(query_terms)),
                "sample_sources": list(menu.get("direct_sources", []))[:6],
            }
        )

    return nodes


def _build_workben_alignment(system_map: dict[str, Any]) -> list[dict[str, Any]]:
    records = system_map.get("records", []) if isinstance(system_map.get("records"), list) else []
    alignment: list[dict[str, Any]] = []
    for target, meta in BUILDROOT_WORKBEN_TARGETS.items():
        query = " ".join(meta.get("query_terms", ()))
        matches = _match_system_map_records(query, records, limit=3)
        alignment.append(
            {
                "target": target,
                "semantic_role": meta.get("semantic_role"),
                "query_terms": list(meta.get("query_terms", ())),
                "matches": matches,
                "best_match": matches[0] if matches else None,
                "matched": bool(matches),
            }
        )
    return alignment


def _resolve_system_map_path() -> Path | None:
    for candidate in DEFAULT_SYSTEM_MAP_CANDIDATES:
        if candidate.exists():
            return candidate
    return None


def _load_system_map() -> dict[str, Any] | None:
    path = _resolve_system_map_path()
    if path is None:
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"schema": "unreadable", "path": str(path), "records": [], "matches": []}

    records = _iter_system_map_records(payload)
    anchor_terms = ("root", "project", "system", "linux", "daemon", "surface", "bridge")
    anchors: list[dict[str, Any]] = []
    seen_anchor_ids: set[str] = set()
    for term in anchor_terms:
        for match in _match_system_map_records(term, records, limit=2):
            match_id = str(match.get("id") or match.get("name") or "")
            if not match_id or match_id in seen_anchor_ids:
                continue
            seen_anchor_ids.add(match_id)
            anchors.append(match)

    record_summaries = [_summarize_system_map_record(record) for record in records[:96]]
    schema = "system-map-list" if isinstance(payload, list) else str(payload.get("schema") or "system-map-unknown")
    return {
        "schema": schema,
        "path": str(path),
        "record_count": len(records),
        "records": record_summaries,
        "matches": record_summaries,
        "anchors": anchors,
    }


def _read_immune_surface_state() -> dict[str, Any]:
    try:
        from ciel_geometry.noema_surface_mmap import DEFAULT_SURFACE_ROOT, open_surface, read_surface_state

        surface = open_surface(DEFAULT_SURFACE_ROOT, mode="r")
        state = read_surface_state(surface)
        return {
            "exists": True,
            "root": str(DEFAULT_SURFACE_ROOT),
            "coherence_index": state.get("coherence_index"),
            "soul_invariant": state.get("soul_invariant"),
            "ethical_score": state.get("ethical_score"),
            "closure_penalty": state.get("closure_penalty"),
            "operating_mode": state.get("operating_mode"),
            "noema_tick": state.get("noema_tick"),
        }
    except Exception:
        return {
            "exists": False,
            "root": str(DEFAULT_BUILDROOT.parent / "surface"),
        }


def _count_files(root: Path, suffixes: tuple[str, ...]) -> int:
    total = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        if Path(dirpath).name == ".git":
            dirnames[:] = []
            continue
        for filename in filenames:
            lower = filename.lower()
            if any(lower.endswith(suffix) for suffix in suffixes):
                total += 1
    return total


def summarize_buildroot(root: Path) -> dict[str, Any]:
    root = Path(root)
    top_level_dirs = sorted(
        p.name for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")
    )
    package_root = root / "package"
    package_dirs = []
    if package_root.is_dir():
        package_dirs = sorted(
            p.name for p in package_root.iterdir() if p.is_dir() and not p.name.startswith(".")
        )

    counts = {
        "config_in": _count_files(root, ("config.in",)),
        "mk": _count_files(root, (".mk",)),
        "hash": _count_files(root, (".hash",)),
        "patch": _count_files(root, (".patch",)),
        "service": _count_files(root, (".service",)),
        "defconfig": _count_files(root, ("defconfig",)),
        "readme": _count_files(root, ("readme",)),
    }

    sample_packages = package_dirs[:24]
    sample_configs = []
    for rel in (
        "Config.in",
        "package/Config.in",
        "toolchain/Config.in",
        "system/Config.in",
        "boot/Config.in",
        "fs/Config.in",
        "linux/Config.in",
        "arch/Config.in",
    ):
        candidate = root / rel
        if candidate.exists():
            sample_configs.append(rel)

    menu_tree = _parse_buildroot_menu_tree(root)
    semantic_subtrees = _build_semantic_subtrees(
        {
            "top_level_dirs": top_level_dirs,
            "menu_tree": menu_tree,
        }
    )
    return {
        "root": str(root),
        "top_level_dirs": top_level_dirs,
        "package_dir_count": len(package_dirs),
        "sample_packages": sample_packages,
        "sample_configs": sample_configs,
        "counts": counts,
        "menu_tree": menu_tree,
        "semantic_subtrees": semantic_subtrees,
        "workben_alignment": [],
        "rt_surface": {
            "boot": "present" if (root / "boot").exists() else "missing",
            "kernel": "present" if (root / "linux").exists() else "missing",
            "toolchain": "present" if (root / "toolchain").exists() else "missing",
            "filesystem": "present" if (root / "fs").exists() else "missing",
            "system": "present" if (root / "system").exists() else "missing",
        },
    }


def build_phase_prompt(snapshot: dict[str, Any]) -> str:
    surface_state = snapshot.get("immune_surface", {}) if isinstance(snapshot.get("immune_surface"), dict) else {}
    system_map = snapshot.get("system_map", {}) if isinstance(snapshot.get("system_map"), dict) else {}
    payload = json.dumps(snapshot, indent=2, ensure_ascii=False, sort_keys=True)
    return (
        "Translate this Buildroot snapshot into a PhaseNav specification for a "
        "vectorized real-time OS named ResEnta.\n"
        "Return strict JSON only. No markdown, no commentary.\n"
        "The JSON must include: system_name, translation_mode, buildroot_characterization, "
        "subsystems, boot_chain, continuity_plan, rt_constraints, memory_plan, ipc_plan, "
        "risks, next_steps, and confidence.\n"
        "Prefer deterministic structure over prose. Mention continuity, RT, scheduler, "
        "boot chain, memory pressure, and recovery explicitly.\n\n"
        f"IMMUNE SURFACE:\n{json.dumps(surface_state, indent=2, ensure_ascii=False, sort_keys=True)}\n\n"
        f"SYSTEM MAP:\n{json.dumps(system_map, indent=2, ensure_ascii=False, sort_keys=True)}\n\n"
        f"BUILDROOT SNAPSHOT:\n{payload}\n"
    )


def _deterministic_phase_ir(snapshot: dict[str, Any]) -> dict[str, Any]:
    counts = snapshot.get("counts", {}) if isinstance(snapshot.get("counts"), dict) else {}
    top_level = snapshot.get("top_level_dirs", []) if isinstance(snapshot.get("top_level_dirs"), list) else []
    sample_packages = snapshot.get("sample_packages", []) if isinstance(snapshot.get("sample_packages"), list) else []
    system_map = snapshot.get("system_map", {}) if isinstance(snapshot.get("system_map"), dict) else {}
    system_matches = system_map.get("records", []) if isinstance(system_map.get("records"), list) else []
    system_anchors = system_map.get("anchors", []) if isinstance(system_map.get("anchors"), list) else []
    immune_surface = snapshot.get("immune_surface", {}) if isinstance(snapshot.get("immune_surface"), dict) else {}
    semantic_subtrees = snapshot.get("semantic_subtrees", []) if isinstance(snapshot.get("semantic_subtrees"), list) else []
    workben_alignment = snapshot.get("workben_alignment", []) if isinstance(snapshot.get("workben_alignment"), list) else []

    subsystem_map = []
    for node in semantic_subtrees[:18]:
        if not isinstance(node, dict):
            continue
        name = str(node.get("name") or "").strip()
        if not name:
            continue
        query_terms = node.get("query_terms", [])
        query = " ".join(str(term) for term in query_terms if term)
        if not query:
            query = name
        match = _match_system_map_records(query, system_matches, limit=2)
        anchor_hits = _match_system_map_records(query, system_anchors, limit=2)
        subsystem_map.append(
            {
                "name": name,
                "kind": node.get("kind"),
                "semantic_role": node.get("semantic_role", "subtree"),
                "phase_label": f"phase:{name.lower().replace(' ', '-')}",
                "source_count": node.get("source_count", 0),
                "rt_role": "core"
                if node.get("semantic_role") in {"boot_chain", "kernel_runtime", "control_plane"}
                else "support",
                "continuity_role": "persistent"
                if node.get("semantic_role") in {"boot_chain", "kernel_runtime", "control_plane", "package_root"}
                else "auxiliary",
                "risk": "high" if node.get("kind") == "dir" and name in {"linux", "toolchain"} else "moderate",
                "system_map_ref": match[0].get("id") if match else None,
                "system_map_lp": match[0].get("lp") if match else None,
                "system_map_matches": match,
                "system_map_anchors": anchor_hits,
                "semantic_query": query,
            }
        )

    matched_subsystem_count = sum(1 for entry in subsystem_map if entry.get("system_map_matches"))
    continuity_plan = [
        "Preserve boot chain invariants across cold start and warm restart.",
        "Keep package selection, kernel config, and filesystem layout under a single PhaseNav IR.",
        "Treat runtime recovery as a first-class continuity path, not an afterthought.",
    ]
    rt_constraints = [
        "Bound boot latency and make scheduling choices explicit.",
        "Separate control-plane invariants from payload packages.",
        "Minimize untracked side effects in package hooks.",
    ]
    memory_plan = [
        "Use deterministic memory budgets for boot, kernel, userland, and recovery paths.",
        "Make model-assisted suggestions advisory, not canonical.",
    ]
    ipc_plan = [
        "Represent build phases as structured messages with stable IDs.",
        "Keep validator output machine-readable for downstream codegen.",
    ]
    risks = [
        "Package explosion can hide boot-chain coupling.",
        "Real-time constraints may conflict with feature breadth.",
        "Deterministic regeneration must survive partial tree updates.",
    ]
    next_steps = [
        "Normalize Buildroot directories into PhaseNav modules.",
        "Generate a ResEnta RT skeleton from the IR.",
        "Add continuity and recovery tests around boot and scheduler paths.",
    ]

    return {
        "schema": IR_SCHEMA_V01,
        "system_name": "ResEnta RT",
        "translation_mode": "PhaseNav",
        "buildroot_characterization": {
            "package_dir_count": snapshot.get("package_dir_count", 0),
            "package_sample": sample_packages,
            "top_level_dirs": top_level,
            "counts": counts,
            "menu_count": snapshot.get("menu_tree", {}).get("menu_count", 0) if isinstance(snapshot.get("menu_tree"), dict) else 0,
            "menu_source_count": snapshot.get("menu_tree", {}).get("source_count", 0) if isinstance(snapshot.get("menu_tree"), dict) else 0,
            "semantic_subtree_count": len(semantic_subtrees),
            "workben_alignment_count": sum(1 for entry in workben_alignment if isinstance(entry, dict) and entry.get("matched")),
        },
        "system_map_alignment": {
            "source_path": system_map.get("path"),
            "record_count": system_map.get("record_count", 0),
            "matched_count": matched_subsystem_count,
            "anchor_count": len(system_anchors),
            "anchors": system_anchors[:24],
            "workben_alignment": workben_alignment,
        },
        "immune_surface": immune_surface,
        "subsystems": subsystem_map,
        "boot_chain": [
            "boot",
            "linux",
            "system",
            "package",
            "fs",
            "toolchain",
        ],
        "continuity_plan": continuity_plan,
        "rt_constraints": rt_constraints,
        "memory_plan": memory_plan,
        "ipc_plan": ipc_plan,
        "risks": risks,
        "next_steps": next_steps,
        "confidence": 0.58 if subsystem_map else 0.42,
    }


def _score_phase_ir(parsed: dict[str, Any], raw_text: str, snapshot: dict[str, Any]) -> dict[str, Any]:
    required_keys = [
        "system_name",
        "translation_mode",
        "buildroot_characterization",
        "subsystems",
        "boot_chain",
        "continuity_plan",
        "rt_constraints",
        "memory_plan",
        "ipc_plan",
        "risks",
        "next_steps",
        "confidence",
    ]
    present = sum(1 for key in required_keys if parsed.get(key) is not None)
    completeness = present / len(required_keys)
    subsystem_count = len(parsed.get("subsystems", []) if isinstance(parsed.get("subsystems"), list) else [])
    rt_focus = 1.0 if "rt" in raw_text.lower() or "real-time" in raw_text.lower() else 0.5
    continuity_focus = 1.0 if "continuity" in raw_text.lower() else 0.5
    parse_success = 0.0 if parsed.get("raw") is not None else 1.0
    structural_mass = min(1.0, (snapshot.get("package_dir_count", 0) or 0) / 300.0)
    model_confidence = _clamp01(parsed.get("confidence", 0.5), default=0.5)
    immune_surface = snapshot.get("immune_surface", {}) if isinstance(snapshot.get("immune_surface"), dict) else {}
    surface_coherence = _clamp01(immune_surface.get("coherence_index", 0.5))
    surface_closure = _clamp01(1.0 - float(immune_surface.get("closure_penalty", 0.5) or 0.5))
    surface_ethics = _clamp01(immune_surface.get("ethical_score", 0.5))
    surface_mode = str(immune_surface.get("operating_mode", "") or "").lower()
    surface_guard = _clamp01((surface_coherence + surface_closure + surface_ethics) / 3.0)

    weights = canonical_weighting(
        semantic_mass=_clamp01(structural_mass, default=0.5),
        phase_alignment=rt_focus,
        coherence_index=continuity_focus,
        closure_score=completeness,
        projection_confidence=parse_success,
        htri_coherence=_clamp01((rt_focus + continuity_focus) / 2.0),
        cqcl_signal=rt_focus,
        phase_nav_similarity=1.0 if parsed.get("translation_mode") == "PhaseNav" else 0.5,
        affective_similarity=surface_ethics,
        euler_alignment=surface_closure,
        novelty=_clamp01(min(1.0, subsystem_count / 12.0)),
        contradiction_risk=_clamp01(1.0 - completeness + (0.15 if surface_mode == "safe" else 0.0)),
        signal_count=float(subsystem_count),
    )
    quality_score = _clamp01(0.55 * weights["composite"] + 0.15 * model_confidence + 0.15 * completeness + 0.15 * surface_guard)
    return {
        "quality_score": round(quality_score, 4),
        "quality_breakdown": {
            **weights,
            "required_key_count": len(required_keys),
            "present_key_count": present,
            "completeness": round(completeness, 4),
            "subsystem_count": subsystem_count,
            "rt_focus": round(rt_focus, 4),
            "continuity_focus": round(continuity_focus, 4),
            "parse_success": round(parse_success, 4),
            "model_confidence": round(model_confidence, 4),
            "surface_coherence": round(surface_coherence, 4),
            "surface_closure": round(surface_closure, 4),
            "surface_ethics": round(surface_ethics, 4),
            "surface_guard": round(surface_guard, 4),
            "surface_mode": surface_mode,
        },
    }


def _run_probe_once(
    buildroot_root: str | Path,
    *,
    model_path: str | Path | None = None,
    use_gguf: bool = True,
    n_ctx: int = 4096,
    n_threads: int = 4,
    n_gpu_layers: int = 0,
    max_new_tokens: int = 512,
    temperature: float = 0.2,
    backend_factory: Callable[..., Any] | None = None,
) -> tuple[dict[str, Any], float]:
    import time

    start = time.perf_counter()
    report = run_buildroot_probe(
        buildroot_root,
        model_path=model_path,
        use_gguf=use_gguf,
        n_ctx=n_ctx,
        n_threads=n_threads,
        n_gpu_layers=n_gpu_layers,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        backend_factory=backend_factory,
    )
    elapsed_ms = (time.perf_counter() - start) * 1000.0
    return report, elapsed_ms


def _summarize_samples(samples: list[dict[str, Any]], *, backend_mode: str) -> dict[str, Any]:
    if not samples:
        return {
            "backend_mode": backend_mode,
            "runs": 0,
            "mean_quality_score": 0.0,
            "median_quality_score": 0.0,
            "p95_quality_score": 0.0,
            "mean_elapsed_ms": 0.0,
            "median_elapsed_ms": 0.0,
            "p95_elapsed_ms": 0.0,
            "samples": [],
        }
    qualities = [float(sample["quality_score"]) for sample in samples]
    elapsed = [float(sample["elapsed_ms"]) for sample in samples]
    qualities_sorted = sorted(qualities)
    elapsed_sorted = sorted(elapsed)
    p95_idx = max(0, int(len(samples) * 0.95) - 1)
    return {
        "backend_mode": backend_mode,
        "runs": len(samples),
        "mean_quality_score": round(sum(qualities) / len(samples), 4),
        "median_quality_score": round(float(median(qualities)), 4),
        "p95_quality_score": round(float(qualities_sorted[p95_idx]), 4),
        "mean_elapsed_ms": round(sum(elapsed) / len(samples), 3),
        "median_elapsed_ms": round(float(median(elapsed)), 3),
        "p95_elapsed_ms": round(float(elapsed_sorted[p95_idx]), 3),
        "samples": samples,
    }


def run_buildroot_phase_benchmark(
    buildroot_root: str | Path,
    *,
    model_path: str | Path | None = None,
    use_gguf: bool = True,
    runs: int = 5,
    n_ctx: int = 4096,
    n_threads: int = 4,
    n_gpu_layers: int = 0,
    max_new_tokens: int = 512,
    temperature: float = 0.2,
    backend_factory: Callable[..., Any] | None = None,
) -> dict[str, Any]:
    runs = max(1, int(runs))
    deterministic_samples = []
    for _ in range(runs):
        deterministic_report, deterministic_ms = _run_probe_once(
            buildroot_root,
            model_path=None,
            use_gguf=False,
            n_ctx=n_ctx,
            n_threads=n_threads,
            n_gpu_layers=n_gpu_layers,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            backend_factory=backend_factory,
        )
        deterministic_samples.append(
            {
                "quality_score": float(deterministic_report.get("quality_score", 0.0)),
                "elapsed_ms": deterministic_ms,
                "backend_mode": deterministic_report.get("backend_mode"),
                "system_map_matches": deterministic_report.get("parsed_ir", {}).get("system_map_alignment", {}).get("matched_count", 0),
            }
        )

    gguf_report: dict[str, Any] | None = None
    gguf_samples: list[dict[str, Any]] = []
    resolved_model = _resolve_model_path(model_path) if use_gguf else None
    if resolved_model is not None:
        for _ in range(runs):
            gguf_report, gguf_ms = _run_probe_once(
                buildroot_root,
                model_path=resolved_model,
                use_gguf=True,
                n_ctx=n_ctx,
                n_threads=n_threads,
                n_gpu_layers=n_gpu_layers,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                backend_factory=backend_factory,
            )
            gguf_samples.append(
                {
                    "quality_score": float(gguf_report.get("quality_score", 0.0)),
                    "elapsed_ms": gguf_ms,
                    "backend_mode": gguf_report.get("backend_mode"),
                    "system_map_matches": gguf_report.get("parsed_ir", {}).get("system_map_alignment", {}).get("matched_count", 0),
                }
            )

    deterministic_summary = _summarize_samples(deterministic_samples, backend_mode="deterministic")
    gguf_summary = _summarize_samples(gguf_samples, backend_mode="gguf") if gguf_samples else None
    deterministic_quality = float(deterministic_summary["mean_quality_score"])
    gguf_quality = float(gguf_summary["mean_quality_score"]) if gguf_summary else None
    quality_delta = None if gguf_quality is None else round(gguf_quality - deterministic_quality, 4)
    latency_delta = None if gguf_summary is None else round(gguf_summary["median_elapsed_ms"] - deterministic_summary["median_elapsed_ms"], 3)

    return {
        "schema": BENCH_SCHEMA_V01,
        "buildroot_root": str(buildroot_root),
        "model_path": str(resolved_model) if resolved_model else None,
        "deterministic": deterministic_summary,
        "gguf": gguf_summary,
        "quality_delta": quality_delta,
        "latency_delta_ms": latency_delta,
        "winner": "gguf"
        if gguf_quality is not None and gguf_quality > deterministic_quality
        else "deterministic",
    }


def _resolve_model_path(requested: str | Path | None = None) -> Path | None:
    if requested:
        path = Path(requested).expanduser()
        if path.exists():
            return path
    env = os.environ.get("CIEL_GGUF_PATH") or os.environ.get("CIEL_GGUF_MODEL")
    if env:
        path = Path(env).expanduser()
        if path.exists():
            return path
    path = get_model_path()
    if path and path.exists():
        return path
    return None


def _build_gguf_backend(
    model_path: Path,
    *,
    n_ctx: int,
    n_threads: int,
    n_gpu_layers: int,
    max_new_tokens: int,
    temperature: float,
    system_prompt: str,
) -> Any:
    from ciel_omega.ciel.llm_registry import build_gguf_primary_backend

    return build_gguf_primary_backend(
        model_path=str(model_path),
        n_ctx=n_ctx,
        n_threads=n_threads,
        n_gpu_layers=n_gpu_layers,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        system_prompt=system_prompt,
    )


def _generate_reply(
    *,
    snapshot: dict[str, Any],
    prompt: str,
    model_path: Path | None,
    n_ctx: int,
    n_threads: int,
    n_gpu_layers: int,
    max_new_tokens: int,
    temperature: float,
    backend_factory: Callable[..., Any] | None = None,
) -> tuple[str, str]:
    if model_path is None:
        return json.dumps(_deterministic_phase_ir(snapshot), ensure_ascii=False, indent=2), "deterministic"

    factory = backend_factory or _build_gguf_backend
    backend = factory(
        model_path=model_path,
        n_ctx=n_ctx,
        n_threads=n_threads,
        n_gpu_layers=n_gpu_layers,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        system_prompt=(
            "You are a strict PhaseNav translator. Return only JSON for a Buildroot-to-ResEnta RT "
            "translation. Do not explain."
        ),
    )
    backend_name = type(backend).__name__.lower()
    if "stub" in backend_name or not hasattr(backend, "generate_reply"):
        return json.dumps(_deterministic_phase_ir(snapshot), ensure_ascii=False, indent=2), "stub"

    reply = backend.generate_reply([{"role": "user", "content": prompt}], {"buildroot_snapshot": snapshot})
    return str(reply), "gguf"


def run_buildroot_probe(
    buildroot_root: str | Path,
    *,
    model_path: str | Path | None = None,
    use_gguf: bool = True,
    n_ctx: int = 4096,
    n_threads: int = 4,
    n_gpu_layers: int = 0,
    max_new_tokens: int = 512,
    temperature: float = 0.2,
    backend_factory: Callable[..., Any] | None = None,
) -> dict[str, Any]:
    root = Path(buildroot_root)
    snapshot = summarize_buildroot(root)
    snapshot["system_map"] = _load_system_map() or {}
    snapshot["immune_surface"] = _read_immune_surface_state()
    snapshot["workben_alignment"] = _build_workben_alignment(snapshot["system_map"])
    prompt = build_phase_prompt(snapshot)
    resolved_model = _resolve_model_path(model_path) if use_gguf else None
    raw_reply, backend_mode = _generate_reply(
        snapshot=snapshot,
        prompt=prompt,
        model_path=resolved_model,
        n_ctx=n_ctx,
        n_threads=n_threads,
        n_gpu_layers=n_gpu_layers,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        backend_factory=backend_factory,
    )
    parsed = _parse_json_object(raw_reply)
    score = _score_phase_ir(parsed, raw_reply, snapshot)
    return {
        "schema": PROBE_SCHEMA_V01,
        "buildroot_root": str(root),
        "buildroot_snapshot": snapshot,
        "model_path": str(resolved_model) if resolved_model else None,
        "backend_mode": backend_mode,
        "prompt": prompt,
        "raw_reply": raw_reply,
        "parsed_ir": parsed,
        "quality_score": score["quality_score"],
        "quality_breakdown": score["quality_breakdown"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Probe Buildroot -> PhaseNav translation with optional GGUF.")
    parser.add_argument("--buildroot", type=Path, default=DEFAULT_BUILDROOT, help="Path to the Buildroot tree.")
    parser.add_argument("--model", default=None, help="Optional path to a local GGUF model.")
    parser.add_argument("--no-gguf", action="store_true", help="Force deterministic fallback.")
    parser.add_argument("--benchmark", action="store_true", help="Run a deterministic vs GGUF benchmark report.")
    parser.add_argument("--benchmark-runs", type=int, default=5, help="Number of rounds for benchmark mode.")
    parser.add_argument("--n-ctx", type=int, default=4096)
    parser.add_argument("--n-threads", type=int, default=4)
    parser.add_argument("--n-gpu-layers", type=int, default=0)
    parser.add_argument("--max-new-tokens", type=int, default=512)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--output", type=Path, default=None, help="Optional JSON output path.")
    args = parser.parse_args(argv)

    if args.benchmark:
        report = run_buildroot_phase_benchmark(
            args.buildroot,
            model_path=args.model,
            use_gguf=not args.no_gguf,
            runs=args.benchmark_runs,
            n_ctx=args.n_ctx,
            n_threads=args.n_threads,
            n_gpu_layers=args.n_gpu_layers,
            max_new_tokens=args.max_new_tokens,
            temperature=args.temperature,
        )
    else:
        report = run_buildroot_probe(
            args.buildroot,
            model_path=args.model,
            use_gguf=not args.no_gguf,
            n_ctx=args.n_ctx,
            n_threads=args.n_threads,
            n_gpu_layers=args.n_gpu_layers,
            max_new_tokens=args.max_new_tokens,
            temperature=args.temperature,
        )
    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output is not None:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
