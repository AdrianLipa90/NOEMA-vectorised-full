#!/usr/bin/env python3
"""Read-only audit of the canonical metatime -> Ω/CQCL -> Orbital -> NOEMA -> Apocalypos stack.

The audit is intentionally static: it parses Python imports and package
metadata, records path/hash facts, and never imports or executes project code.
Reports are written below ``runtime/audits`` on the canonical New Volume tree.
"""
from __future__ import annotations

import ast
import hashlib
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_ROOT = ROOT / "runtime" / "audits" / "layer_consolidation"

LAYER_PATHS: dict[str, tuple[str, ...]] = {
    "metatime": (
        "src/ciel_metatime",
        "src/ciel_geometry/phasenav/metatime_contract.py",
        "scripts/metatime_v8_redteam_validator.py",
    ),
    "omega_cqcl": (
        "src/CIEL_OMEGA_COMPLETE_SYSTEM",
        "src/ciel_sot_agent/ciel_pipeline.py",
    ),
    "orbital": (
        "integration/Orbital",
        "src/ciel_sot_agent/orbital_bridge.py",
        "src/ciel_sot_agent/orch_orbital.py",
    ),
    "noema": (
        "src/ciel_geometry",
        "src/cielingo_core",
        "src/cielingo",
        "scripts/ciel_noema_kuramoto_daemon.py",
        "scripts/ciel_headless_daemon.py",
        "scripts/noema_portal_daemon.py",
        "scripts/noema_db_refresh_orchestrator.py",
    ),
    "apocalypos": (
        "src/apocalypos",
        "config/systemd/noema-phasenav-ebpf.service",
    ),
    "packages": (
        "pyproject.toml",
        "setup.py",
        "requirements.txt",
        "requirements-cuda.txt",
        "requirements-htri.txt",
        "packages",
        "packaging",
        "src/ciel-omega-demo-main/pyproject.toml",
        "src/ciel_rh_control_mini_repo/pyproject.toml",
    ),
}

INTERNAL_PREFIX_TO_LAYER = {
    "ciel_metatime": "metatime",
    "ciel_geometry": "metatime",
    "ciel_omega": "omega_cqcl",
    "ciel_sot_agent": "orbital",
    "integration": "orbital",
    "cielingo_core": "noema",
    "cielingo": "noema",
    "apocalypos": "apocalypos",
    "noema_htri": "noema",
    "noema_nonlocal_db": "noema",
}

LAYER_ORDER = ("metatime", "omega_cqcl", "orbital", "noema", "apocalypos", "packages")
LAYER_RANK = {name: index for index, name in enumerate(LAYER_ORDER)}

FORBIDDEN_PATH_TOKENS = ("/tmp/", "new_volume_rw", "New Volume1")
VENDOR_PREFIXES = ("packages/opencode/", "packages/opencode-sandbox/")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def files_for(path_text: str) -> list[Path]:
    path = ROOT / path_text
    if path.is_file():
        return [path]
    if path.is_dir():
        return sorted(p for p in path.rglob("*") if p.is_file())
    return []


def layer_inventory() -> dict[str, Any]:
    result: dict[str, Any] = {}
    for layer, paths in LAYER_PATHS.items():
        file_count = 0
        total_bytes = 0
        samples: list[str] = []
        anchor_hashes: dict[str, str] = {}
        missing: list[str] = []
        for path_text in paths:
            selected = files_for(path_text)
            if not selected:
                missing.append(path_text)
                continue
            path = ROOT / path_text
            file_count += len(selected)
            total_bytes += sum(item.stat().st_size for item in selected)
            samples.extend(str(item.relative_to(ROOT)) for item in selected[:12])
            if path.is_file():
                anchor_hashes[path_text] = sha256(path)
        result[layer] = {
            "declared_paths": list(paths),
            "missing_paths": missing,
            "file_count": file_count,
            "bytes": total_bytes,
            "sample_files": samples[:24],
            "anchor_hashes": anchor_hashes,
        }
    return result


def top_level(module: str) -> str:
    return module.split(".", 1)[0]


def module_layer(module: str) -> str | None:
    return INTERNAL_PREFIX_TO_LAYER.get(top_level(module))


def ast_imports() -> dict[str, Any]:
    edges: Counter[tuple[str, str]] = Counter()
    files_with_errors: dict[str, str] = {}
    import_sites: defaultdict[tuple[str, str], list[str]] = defaultdict(list)
    roots = [
        ROOT / "src" / "ciel_metatime",
        ROOT / "src" / "ciel_geometry",
        ROOT / "src" / "ciel_sot_agent",
        ROOT / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM" / "ciel_omega",
        ROOT / "src" / "cielingo_core",
        ROOT / "src" / "cielingo",
        ROOT / "src" / "apocalypos",
        ROOT / "integration",
    ]
    for directory in roots:
        if not directory.exists():
            continue
        for path in directory.rglob("*.py"):
            try:
                tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except (OSError, SyntaxError, UnicodeDecodeError) as exc:
                files_with_errors[str(path.relative_to(ROOT))] = f"{type(exc).__name__}: {exc}"
                continue
            source_layer = None
            rel = str(path.relative_to(ROOT))
            for candidate, layer in (
                ("src/ciel_metatime", "metatime"),
                ("src/ciel_geometry", "metatime"),
                ("src/ciel_sot_agent", "orbital"),
                ("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega", "omega_cqcl"),
                ("src/cielingo_core", "noema"),
                ("src/cielingo", "noema"),
                ("src/apocalypos", "apocalypos"),
                ("integration", "orbital"),
            ):
                if rel == candidate or rel.startswith(candidate + "/"):
                    source_layer = layer
                    break
            if source_layer is None:
                continue
            for node in ast.walk(tree):
                names: list[str] = []
                if isinstance(node, ast.Import):
                    names = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module:
                    names = [node.module]
                for module in names:
                    target_layer = module_layer(module)
                    if target_layer is None:
                        continue
                    edges[(source_layer, target_layer)] += 1
                    if len(import_sites[(source_layer, target_layer)]) < 12:
                        import_sites[(source_layer, target_layer)].append(rel)
    layer_edges = [
            {
                "source": source,
                "target": target,
                "count": count,
                "example_files": import_sites[(source, target)],
            }
            for (source, target), count in sorted(edges.items())
        ]
    back_edges = [
        edge for edge in layer_edges
        if edge["source"] != edge["target"]
        and LAYER_RANK.get(edge["target"], -1) < LAYER_RANK.get(edge["source"], -1)
    ]
    return {
        "layer_edges": layer_edges,
        "back_edges_against_declared_order": back_edges,
        "files_with_parse_errors": files_with_errors,
    }


def package_metadata() -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    for rel in (
        "pyproject.toml",
        "setup.py",
        "requirements.txt",
        "requirements-cuda.txt",
        "requirements-htri.txt",
        "src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/setup.py",
        "src/ciel-omega-demo-main/pyproject.toml",
        "src/ciel_rh_control_mini_repo/pyproject.toml",
    ):
        path = ROOT / rel
        if path.exists():
            text = path.read_text(encoding="utf-8", errors="replace")
            metadata[rel] = {
                "sha256": sha256(path),
                "lines": text.count("\n") + 1,
                "declares_ciel_omega": '"ciel_omega*"' in text,
                "declares_ciel_metatime": '"ciel_metatime*"' in text,
                "declares_apocalypos": '"apocalypos*"' in text,
                "declares_cqcl": "cqcl" in text.lower(),
            }
    return metadata


def path_token_audit() -> dict[str, Any]:
    hits: defaultdict[str, list[str]] = defaultdict(list)
    for paths in LAYER_PATHS.values():
        for path_text in paths:
            for path in files_for(path_text):
                rel = str(path.relative_to(ROOT))
                if rel.startswith(VENDOR_PREFIXES):
                    continue
                if path.suffix not in {".py", ".toml", ".txt", ".service", ".timer", ".json"}:
                    continue
                try:
                    text = path.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue
                for token in FORBIDDEN_PATH_TOKENS:
                    if token in text and len(hits[token]) < 80:
                        hits[token].append(rel)
    return {token: sorted(paths) for token, paths in hits.items()}


def duplicate_basenames() -> dict[str, Any]:
    paths_by_name: defaultdict[str, list[Path]] = defaultdict(list)
    roots = [ROOT / "src", ROOT / "integration", ROOT / "packages", ROOT / "packaging"]
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*.py"):
            rel = str(path.relative_to(ROOT))
            if rel.startswith(VENDOR_PREFIXES):
                continue
            paths_by_name[path.name].append(path)
    result: dict[str, Any] = {}
    for name, paths in sorted(paths_by_name.items()):
        if len(paths) <= 1:
            continue
        hashes: set[str] = set()
        for path in paths:
            try:
                hashes.add(sha256(path))
            except OSError:
                pass
        result[name] = {
            "count": len(paths),
            "distinct_sha256": len(hashes),
            "examples": [str(path.relative_to(ROOT)) for path in paths[:12]],
        }
    return result


def build_report() -> dict[str, Any]:
    inventory = layer_inventory()
    return {
        "schema": "noema/layer-consolidation-audit/v0.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "canonical_root": str(ROOT),
        "scope": ["metatime", "omega_cqcl", "orbital", "noema", "apocalypos", "packages"],
        "declared_layer_order": list(LAYER_ORDER),
        "excluded_vendor_prefixes": list(VENDOR_PREFIXES),
        "facts": {
            "inventory": inventory,
            "imports": ast_imports(),
            "package_metadata": package_metadata(),
            "path_token_audit": path_token_audit(),
            "duplicate_python_basenames": duplicate_basenames(),
        },
        "inference": {
            "metatime_shim": "src/ciel_metatime/__init__.py re-exports ciel_geometry.phasenav.metatime_contract",
            "omega_packaging_boundary": "ciel_omega is a separately packaged subtree with its own setup.py; the root pyproject intentionally packages the SOT/geometry surface only",
            "orbital_boundary": "integration/Orbital and ciel_sot_agent.orbital_bridge are the active orbital boundary",
            "apocalypos_boundary": "src/apocalypos is the kernel/eBPF boundary and must remain privileged only there",
        },
        "unknowns": [
            "runtime import precedence depends on PYTHONPATH/sitecustomize and was not changed by this read-only audit",
            "disabled/archive packages require contract tests before promotion into the canonical runtime",
        ],
    }


def markdown(report: dict[str, Any]) -> str:
    facts = report["facts"]
    lines = [
        "# NOEMA Layer Consolidation Audit",
        "",
        f"- generated_at: {report['generated_at']}",
        f"- canonical_root: {report['canonical_root']}",
        "- mode: read-only static AST/import/package audit",
        "",
        "## Layer inventory",
        "",
        "| layer | files | bytes | missing declared paths |",
        "|---|---:|---:|---:|",
    ]
    for layer, payload in facts["inventory"].items():
        lines.append(f"| {layer} | {payload['file_count']} | {payload['bytes']} | {len(payload['missing_paths'])} |")
    lines += ["", "## Import layer edges", "", "| source | target | count |", "|---|---|---:|"]
    for edge in facts["imports"]["layer_edges"]:
        lines.append(f"| {edge['source']} | {edge['target']} | {edge['count']} |")
    lines += ["", "## Back-edges against declared order", ""]
    back_edges = facts["imports"]["back_edges_against_declared_order"]
    if back_edges:
        for edge in back_edges:
            lines.append(
                f"- `{edge['source']} -> {edge['target']}` ({edge['count']} imports); "
                f"examples: {', '.join('`'+p+'`' for p in edge['example_files'][:6])}"
            )
    else:
        lines.append("- none")
    lines += ["", "## Package metadata facts", ""]
    for path, payload in facts["package_metadata"].items():
        flags = ", ".join(key.removeprefix("declares_") for key, value in payload.items() if key.startswith("declares_") and value)
        lines.append(f"- `{path}` sha256 `{payload['sha256']}`; declarations: {flags or 'none'}")
    lines += ["", "## Forbidden path tokens", ""]
    token_hits = facts["path_token_audit"]
    if token_hits:
        for token, paths in token_hits.items():
            lines.append(f"- `{token}`: {len(paths)} files; examples: {', '.join('`'+p+'`' for p in paths[:8])}")
    else:
        lines.append("- none in audited layer files")
    lines += ["", "## Interpretation", ""]
    for key, value in report["inference"].items():
        lines.append(f"- **{key}**: {value}")
    lines += ["", "## Unknowns", ""]
    for value in report["unknowns"]:
        lines.append(f"- {value}")
    return "\n".join(lines) + "\n"


def main() -> int:
    report = build_report()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_dir = REPORT_ROOT / stamp
    output_dir.mkdir(parents=True, exist_ok=False)
    (output_dir / "audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output_dir / "audit.md").write_text(markdown(report), encoding="utf-8")
    (REPORT_ROOT / "CURRENT.json").write_text(json.dumps({"path": str(output_dir), "sha256": sha256(output_dir / "audit.json")}, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output_dir": str(output_dir), "layers": {k: v["file_count"] for k, v in report["facts"]["inventory"].items()}, "edges": len(report["facts"]["imports"]["layer_edges"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
