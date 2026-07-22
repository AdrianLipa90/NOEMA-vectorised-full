#!/usr/bin/env python3
"""Audit the PhaseNav source-of-truth boundary.

The audit is intentionally narrow: it detects duplicate runtime copies and
hash-derived semantic routing in the four canonical classification paths.
It writes only to the canonical runtime audit directory.
"""
from __future__ import annotations

import ast
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "src" / "ciel_geometry" / "phasenav"
RUNTIME_DUPLICATE = ROOT / "runtime" / "cielingo_core" / "phasenav"
AUDIT_DIR = ROOT / "runtime" / "audits" / "phasenav_surface"
SEMANTIC_FILES = (
    CANON / "operator_algebra.py",
    ROOT / "src" / "ciel_geometry" / "phase_nav_lang.py",
    CANON / "surface_bridge.py",
    CANON / "enrichment.py",
)


def _hash_calls(path: Path) -> list[int]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    lines: list[int] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "hash":
            lines.append(node.lineno)
    return sorted(lines)


def run() -> dict[str, object]:
    findings: list[dict[str, object]] = []
    if not CANON.is_dir():
        findings.append({"kind": "missing_canonical_surface", "path": str(CANON)})
    if RUNTIME_DUPLICATE.exists():
        findings.append({"kind": "duplicate_runtime_surface", "path": str(RUNTIME_DUPLICATE)})
    hash_calls: dict[str, list[int]] = {}
    for path in SEMANTIC_FILES:
        if not path.exists():
            findings.append({"kind": "missing_semantic_file", "path": str(path)})
            continue
        lines = _hash_calls(path)
        if lines:
            hash_calls[str(path.relative_to(ROOT))] = lines
            findings.append({"kind": "hash_derived_semantics", "path": str(path), "lines": lines})

    # Import from the canonical source tree, never from a runtime copy.
    sys.path.insert(0, str(ROOT / "src"))
    try:
        from ciel_geometry.phasenav.operator_algebra import concept_to_operator

        known, _ = concept_to_operator("source provenance")
        unknown, _ = concept_to_operator("__no_registered_anchor__")
        classification = {"known": known, "unknown": unknown}
    except Exception as exc:  # audit must report, not hide, import failures
        classification = {"error": f"{type(exc).__name__}: {exc}"}
        findings.append({"kind": "canonical_import_error", "error": classification["error"]})

    return {
        "schema": "NOEMA_PHASENAV_SURFACE_AUDIT_V1",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "canonical_surface": str(CANON),
        "runtime_duplicate_present": RUNTIME_DUPLICATE.exists(),
        "hash_calls": hash_calls,
        "classification": classification,
        "findings": findings,
        "status": "clean" if not findings else "findings",
    }


def main() -> int:
    report = run()
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    out = AUDIT_DIR / "CURRENT.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "path": str(out), "findings": len(report["findings"])}))
    return 0 if report["status"] == "clean" else 2


if __name__ == "__main__":
    raise SystemExit(main())
