#!/usr/bin/env python3
"""Deterministic audit of the Metatime -> NOEMA phase chain.

The script is intentionally read-only with respect to source repositories.  It
only writes generated audit artifacts below the canonical NOEMA root when
invoked with ``--write``.  A single explicit SOT is declared for every layer;
all other trees are classified as reference, legacy, or patch evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CANON = Path(__file__).resolve().parents[1]
OUTPUT_DIR = CANON / "manifests" / "phase_chain"


def sha256(path: Path) -> str | None:
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_state(path: Path) -> dict[str, Any]:
    if not (path / ".git").exists():
        return {"repository": False, "commit": None, "dirty": None}
    def run(*args: str) -> str | None:
        try:
            result = subprocess.run(
                ["git", *args], cwd=path, capture_output=True, text=True, timeout=10
            )
        except (OSError, subprocess.SubprocessError):
            return None
        return result.stdout.strip() if result.returncode == 0 else None
    status = run("status", "--porcelain")
    return {
        "repository": True,
        "commit": run("rev-parse", "HEAD"),
        "dirty": bool(status) if status is not None else None,
    }


def source(path: str, role: str, anchors: list[str] | None = None) -> dict[str, Any]:
    p = Path(path)
    record: dict[str, Any] = {
        "path": str(p),
        "role": role,
        "exists": p.exists(),
        "kind": "directory" if p.is_dir() else "file" if p.is_file() else "missing",
        "git": git_state(p if p.is_dir() else p.parent),
    }
    if anchors:
        record["anchors"] = {
            rel: {"exists": (p / rel).is_file(), "sha256": sha256(p / rel)}
            for rel in anchors
        }
    if p.is_file():
        record["sha256"] = sha256(p)
    return record


def read_json(path: Path) -> dict[str, Any] | list[Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def omega_import_probe(general_root: Path, embedded_root: Path, timeout: float = 8.0) -> dict[str, Any]:
    """Probe the two import surfaces without importing them into this process."""
    code = "import ciel.engine as e; print(e.__file__)"
    result: dict[str, Any] = {}
    for name, root in (("general", general_root), ("embedded", embedded_root)):
        try:
            proc = subprocess.run(
                [sys.executable, "-c", code], cwd=root, capture_output=True,
                text=True, timeout=timeout,
            )
            result[name] = {
                "status": "pass" if proc.returncode == 0 else "fail",
                "returncode": proc.returncode,
                "module": proc.stdout.strip() or None,
                "stderr": proc.stderr.strip()[-500:] or None,
            }
        except subprocess.TimeoutExpired:
            result[name] = {"status": "timeout", "timeout_seconds": timeout}
        except OSError as exc:
            result[name] = {"status": "error", "error": str(exc)}
    return result


def build_audit() -> dict[str, Any]:
    clean = Path("/media/adrian/REPOZYTORIA_GIT/NOEMA_REPOS_CLEAN")
    apocalypso = Path("/media/adrian/New Volume/CIEL_PROJECT_CANON/CIEL-Omega-ApokalypOS")
    noema_pkg = CANON / "NOEMA_HTRI_PHASENAV_CIELINGO_v0.8"

    layers = [
        {
            "id": "metatime",
            "sot": str(clean / "Metatime-Relation_of_Information_Framework"),
            "sources": [
                source(str(clean / "Metatime-Relation_of_Information_Framework"), "canonical-research", ["README.md", "CURRENT_STATUS.md"]),
                source(str(clean / "Metatime"), "legacy-historical", ["README.md"]),
            ],
            "boundary": "research foundation; validation debts remain open",
        },
        {
            "id": "omega_cqcl",
            "sot": str(clean / "CIEL-Omega-General-Quantum-Consciousness"),
            "sources": [
                source(str(clean / "CIEL-Omega-General-Quantum-Consciousness"), "canonical-engine", ["README.md", "setup.py"]),
                source(str(apocalypso / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM"), "embedded-runtime-mirror"),
                source(str(clean / "CIEL-Omega-GQC"), "legacy-reference", ["README.md"]),
                source(str(clean / "CielOmegaNew"), "legacy-reference", ["README.md"]),
            ],
            "boundary": "CQCL/CIEL engine; no direct physical claim",
        },
        {
            "id": "orchorbital",
            "sot": str(clean / "Orbital-System-base"),
            "sources": [
                source(str(clean / "Orbital-System-base"), "canonical-orbital-model", ["README.md"]),
                source(str(clean / "SapiensOrbital"), "client-projection", ["README.md"]),
                source(str(noema_pkg / "ORCHORBITAL_RULES_MAPPING_V0_9.json"), "bounded-rules-evidence"),
            ],
            "boundary": "classical orbital mapping; evidence boundary is explicit",
        },
        {
            "id": "noema",
            "sot": str(CANON),
            "sources": [
                source(str(CANON), "active-runtime", ["system_map_v2.json", "config/noema_paths.json", "NOEMA/task_queue.noema.json"]),
                source(str(clean / "noema-surface"), "thin-source-marker", ["README.md"]),
                source(str(clean / "noema-surface-mcp"), "thin-source-marker", ["README.md"]),
                source(str(clean / "noema-runtime-daemons"), "thin-source-marker", ["README.md"]),
            ],
            "boundary": "active runtime and contracts live only under canonical New Volume root",
        },
        {
            "id": "apokalypos",
            "sot": str(apocalypso),
            "sources": [
                source(str(apocalypso), "integration-host", ["CIEL_CANON.py", "README.md", "pyproject.toml"]),
                source(str(clean / "ApocalyptOS"), "legacy-operational-reference", ["README.md"]),
            ],
            "boundary": "integration host; must consume NOEMA contracts rather than shadow them",
        },
        {
            "id": "patches",
            "sot": str(CANON / "patches"),
            "sources": [
                source(str(CANON / "patches"), "canonical-patch-surface"),
                source(str(noema_pkg / "PATCH_NOTES.md"), "package-patch-evidence"),
                source(str(clean / "ApocalyptOS" / "wrappers"), "legacy-snapshot-patches"),
            ],
            "boundary": "patches are proposals/evidence until receipt-backed promotion",
        },
    ]

    edges = [
        {"from": "metatime", "to": "omega_cqcl", "protocol": "research-input", "status": "declared-not-runtime-import"},
        {"from": "omega_cqcl", "to": "orchorbital", "protocol": "phase-state-contract", "status": "implemented-in-apokalypos-bridge"},
        {"from": "orchorbital", "to": "noema", "protocol": "orbital-state-and-contracts", "status": "implemented", "path": "manifests/orbital"},
        {"from": "noema", "to": "apokalypos", "protocol": "canonical-paths-and-phase-bus", "status": "partial"},
        {"from": "apokalypos", "to": "patches", "protocol": "receipt-backed-promotion", "status": "not-promoted"},
    ]

    unresolved = None
    system_map = read_json(CANON / "system_map_v2.json")
    if isinstance(system_map, dict):
        unresolved = len(system_map.get("unresolved_references", []))

    package_validation = read_json(noema_pkg / "COMPREHENSIVE_VALIDATION_REPORT_V0_5.json")
    release_manifest = read_json(noema_pkg / "RELEASE_MANIFEST.noema.json")
    omega_probe = omega_import_probe(
        clean / "CIEL-Omega-General-Quantum-Consciousness",
        apocalypso / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM" / "ciel_omega",
    )
    repository_registry = read_json(apocalypso / "integration" / "repository_registry.json")
    registry_records = repository_registry.get("repositories", []) if isinstance(repository_registry, dict) else []
    metatime_record = next((item for item in registry_records if item.get("key") == "metatime"), {})
    metatime_bound = bool(metatime_record.get("canonical_path")) and Path(metatime_record.get("canonical_path", "")).exists()
    migration = apocalypso / "integration" / "MIGRATION_INDEX_V2.md"
    migration_text = migration.read_text(encoding="utf-8", errors="ignore") if migration.exists() else ""

    blockers = [
        {
            "id": "metatime-path-not-machine-bound",
            "fact": "repository_registry must bind Metatime to a verified filesystem path",
            "status": "resolved" if metatime_bound else "open",
            "severity": "clear" if metatime_bound else "high",
        },
        {
            "id": "omega-multiple-implementations",
            "fact": "General-Quantum-Consciousness, embedded Omega, GQC and CielOmegaNew coexist",
            "severity": "high",
            "import_probe": omega_probe,
        },
        {
            "id": "legacy-index-switch-incomplete",
            "fact": "MIGRATION_INDEX_V2 still marks legacy integration indices as active mirrors",
            "severity": "medium" if migration_text else "unknown",
        },
        {
            "id": "system-map-unresolved-reference",
            "fact": "system_map_v2 unresolved reference count",
            "value": unresolved,
            "severity": "medium" if unresolved else "clear",
        },
        {
            "id": "package-not-canon",
            "fact": "NOEMA-HTRI package declares canon_allowed=false and external_noema_sot_verified=false",
            "severity": "policy-boundary",
            "package_validation": package_validation.get("tests") if isinstance(package_validation, dict) else None,
            "release": release_manifest.get("release_id") if isinstance(release_manifest, dict) else None,
        },
    ]

    return {
        "schema": "NOEMA_PHASE_CHAIN_AUDIT_V1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "canonical_root": str(CANON),
        "phase_vector": {"phi": "metatime→omega_cqcl→orchorbital→noema→apokalypos→patches", "R": 0.987, "tau": "audit", "decision": "truth_first"},
        "policy": {
            "single_sot_per_layer": True,
            "source_repositories_read_only": True,
            "no_deletion": True,
            "patch_promotion_requires_receipt": True,
        },
        "layers": layers,
        "runtime_probes": {"omega_cqcl_import": omega_probe},
        "edges": edges,
        "blockers": blockers,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write generated artifacts under canonical NOEMA")
    args = parser.parse_args()
    audit = build_audit()
    if args.write:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        (OUTPUT_DIR / "phase_chain_audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (OUTPUT_DIR / "phase_chain_manifest.json").write_text(json.dumps({
            "schema": "NOEMA_PHASE_CHAIN_MANIFEST_V1",
            "canonical_root": str(CANON),
            "layers": [{"id": layer["id"], "sot": layer["sot"]} for layer in audit["layers"]],
            "edges": audit["edges"],
            "blocker_ids": [b["id"] for b in audit["blockers"]],
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(audit, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
