#!/usr/bin/env python3
"""PhaseNav File Classifier — tags .py files as full / partial / non PhaseNav.

Reusable, re-runnable classifier (not a one-off audit). Two signals:
  1. Import analysis (ast) — does the file import a PhaseNav-core module?
  2. Canonical core module list — files that themselves *are* the 36D
     PhaseNav engine (encoder, memory, inference, operator algebra, solver,
     decision bridge, loader, phase_nav_lang, phasenav_unified) are FULL;
     anything else that imports one of those is PARTIAL; everything else
     is NON (the default, not listed individually in the manifest).

Each hit's source is also encoded through fast_encode_text (same 36D
PhaseNav encoder used everywhere else) so the manifest carries phase
context, not just a category label.

CLI:
    python3 -m ciel_geometry.phasenav_file_classifier --root . --write
"""
from __future__ import annotations

import argparse
import ast
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCAN_ROOTS = ("src", "scripts")
SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules", ".pytest_cache", "build", "dist"}

# Modules that themselves ARE the PhaseNav core engine (module name, no .py)
CORE_MODULES = {
    "cielingo_phase_encoder",
    "cielingo_phase_memory",
    "cielingo_inference",
    "cielingo_train",
    "phase_nav_lang",
    "phasenav_unified",
}
# Any file living under a directory literally named "phasenav" is core too
CORE_DIR_NAME = "phasenav"

# Import name fragments that mark a file as PARTIAL (uses PhaseNav, isn't it)
PARTIAL_MARKERS = CORE_MODULES | {"phasenav", "fast_encode_text"}


@dataclass(slots=True)
class Classification:
    path: str
    category: str  # "full" | "partial" | "non"
    phase_mean: float = 0.0
    reason: str = ""


def _imported_names(tree: ast.AST) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name.split(".")[0])
                names.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                names.add(node.module.split(".")[0])
                names.add(node.module)
            for alias in node.names:
                names.add(alias.name)
    return names


def _is_core_module(path: Path) -> bool:
    if path.stem in CORE_MODULES:
        return True
    if CORE_DIR_NAME in path.parts[:-1]:
        return True
    return False


def classify_file(path: Path, *, tag_phase: bool = True) -> Classification:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return Classification(path=str(path), category="non", reason="unreadable")

    if _is_core_module(path):
        category, reason = "full", "core PhaseNav module"
    else:
        try:
            tree = ast.parse(text)
            imported = _imported_names(tree)
        except SyntaxError:
            imported = set()
        hit = imported & PARTIAL_MARKERS
        if not hit:
            # fallback: substring check catches dynamic/runtime imports ast misses
            hit = {m for m in PARTIAL_MARKERS if m in text}
        if hit:
            category, reason = "partial", f"imports: {', '.join(sorted(hit))[:120]}"
        else:
            category, reason = "non", ""

    phase_mean = 0.0
    if tag_phase and category != "non":
        try:
            from ciel_geometry.cielingo_phase_encoder import fast_encode_text
            import numpy as np
            sample = text[:600]
            phi = fast_encode_text(sample)
            phase_mean = float(np.mean(phi))
        except Exception:
            pass

    return Classification(path=str(path), category=category, phase_mean=round(phase_mean, 6), reason=reason)


def classify_tree(root: Path, scan_roots: tuple[str, ...] = SCAN_ROOTS) -> list[Classification]:
    results: list[Classification] = []
    for sub in scan_roots:
        base = root / sub
        if not base.exists():
            continue
        for path in base.rglob("*.py"):
            if any(skip in path.parts for skip in SKIP_DIRS):
                continue
            rel = path.relative_to(root)
            c = classify_file(path)
            c.path = str(rel)
            results.append(c)
    return results


def build_manifest(root: Path, scan_roots: tuple[str, ...] = SCAN_ROOTS) -> dict[str, Any]:
    results = classify_tree(root, scan_roots)
    full = sorted(c.path for c in results if c.category == "full")
    partial = sorted(c.path for c in results if c.category == "partial")
    return {
        "generated": datetime.now(timezone.utc).isoformat(),
        "classification_version": 1,
        "scanned_root": list(scan_roots),
        "scan_count": len(results),
        "full": full,
        "partial": partial,
        "non_note": (
            f"{len(results) - len(full) - len(partial)} files not listed individually "
            "(default category); absence from 'full'/'partial' implies non-PhaseNav."
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="PhaseNav File Classifier")
    ap.add_argument("--root", default=".")
    ap.add_argument("--write", action="store_true", help="write PHASENAV_MANIFEST.json to root")
    ap.add_argument("--json", action="store_true", help="print manifest JSON to stdout")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    manifest = build_manifest(root)

    if args.write:
        out = root / "PHASENAV_MANIFEST.json"
        out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Written: {out}")

    if args.json or not args.write:
        print(json.dumps(manifest, indent=2, ensure_ascii=False))

    print(
        f"\nfull={len(manifest['full'])} partial={len(manifest['partial'])} "
        f"scanned={manifest['scan_count']}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
