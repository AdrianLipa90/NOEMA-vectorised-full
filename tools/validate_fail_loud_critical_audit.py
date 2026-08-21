#!/usr/bin/env python3
"""Validation gate for critical fail-loud continuity changes."""
from __future__ import annotations

import importlib
import json
import os
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def assert_source_contract() -> None:
    targets = {
        "surface": ROOT / "src/ciel_geometry/noema_surface_mmap.py",
        "memory_palace": ROOT / "src/ciel_geometry/memory_palace.py",
        "nonlocal": ROOT / "src/ciel_geometry/nonlocal_channel.py",
        "phasenav": ROOT / "src/ciel_geometry/phasenav_unified.py",
        "tether": ROOT / "scripts/noema_tether_runtime.py",
    }
    forbidden = {
        "surface": [
            "reason=assign_fallback",
            "scope=read_ciel_internal_state reason=return {}",
            "cannot mmap {path} after 3 attempts",
        ],
        "memory_palace": ["scope=MentalistMemoryPalace.__init__ reason=pass"],
        "nonlocal": [
            "scope=NonlocalChannel.__init__ reason=assign_fallback",
            "scope=NonlocalChannel._load_rag_cache reason=pass",
            "scope=NonlocalChannel._save_rag_cache reason=pass",
        ],
    }
    for name, path in targets.items():
        source = path.read_text(encoding="utf-8")
        compile(source, str(path), "exec")
        for marker in forbidden.get(name, []):
            if marker in source:
                raise AssertionError(f"forbidden quiet marker remains: {name}:{marker}")

    surface = targets["surface"].read_text(encoding="utf-8")
    required_surface = [
        "class SurfaceStateIntegrityError",
        "refusing truncate",
        "refusing silent Kuramoto substitution",
        "refusing synthetic zero holonomy",
    ]
    for marker in required_surface:
        if marker not in surface:
            raise AssertionError(f"missing surface fail-loud marker: {marker}")

    tether = targets["tether"].read_text(encoding="utf-8")
    for marker in ("self.failure: BaseException | None = None", "health socket thread failed"):
        if marker not in tether:
            raise AssertionError(f"missing tether fail-loud marker: {marker}")


def test_config() -> None:
    module = importlib.import_module("ciel_geometry.noema_config")
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        missing = root / "missing.json"
        cfg = module.load_config(missing)
        if cfg.kuramoto.dt <= 0:
            raise AssertionError("missing-config defaults invalid")

        corrupt = root / "corrupt.json"
        corrupt.write_text("{not-json", encoding="utf-8")
        try:
            module.load_config(corrupt)
        except module.NoemaConfigError:
            pass
        else:
            raise AssertionError("corrupt existing config did not fail loud")

        nested = root / "nested.json"
        nested.write_text(json.dumps({
            "system": {"surface_root": "/tmp/noema-test-surface"},
            "daemons": {"kuramoto": {"dt": 0.123}},
        }), encoding="utf-8")
        nested_cfg = module.load_config(nested)
        if nested_cfg.surface_root != "/tmp/noema-test-surface" or nested_cfg.kuramoto.dt != 0.123:
            raise AssertionError("nested v2 config not honored")


def test_phase_memory() -> None:
    module = importlib.import_module("ciel_geometry.cielingo_phase_memory")
    with tempfile.TemporaryDirectory() as td:
        base = Path(td) / "phase_memory"
        base.with_suffix(".json").write_text("{}", encoding="utf-8")
        try:
            module.PhaseMemory.load_or_create(base)
        except module.PhaseMemoryPersistenceError:
            pass
        else:
            raise AssertionError("partial PhaseMemory pair did not fail loud")

        base.with_suffix(".json").unlink()
        pm = module.PhaseMemory.load_or_create(base)
        if pm.size != 0:
            raise AssertionError("clean first-run PhaseMemory not empty")


def test_surface_preserves_corrupt_bytes() -> None:
    module = importlib.import_module("ciel_geometry.noema_surface_mmap")
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "surface"
        surface = module.ensure_surface(root)
        module.flush_surface(surface)
        del surface

        phi = root / "phi"
        original = phi.read_bytes()
        corrupt = original[:-8]
        phi.write_bytes(corrupt)
        before = phi.read_bytes()
        try:
            module.open_surface(root)
        except module.SurfaceStateIntegrityError:
            pass
        else:
            raise AssertionError("wrong-size existing surface did not fail loud")
        after = phi.read_bytes()
        if before != after:
            raise AssertionError("open_surface mutated corrupt existing bytes")

        state = root / "ciel_state.json"
        state.write_text("{broken", encoding="utf-8")
        try:
            module.read_ciel_internal_state(root)
        except module.SurfaceStateIntegrityError:
            pass
        else:
            raise AssertionError("corrupt existing CIEL state did not fail loud")


def main() -> int:
    assert_source_contract()
    test_config()
    test_phase_memory()
    test_surface_preserves_corrupt_bytes()
    print("PASS: critical fail-loud continuity validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
