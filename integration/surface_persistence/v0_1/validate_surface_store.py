from __future__ import annotations

import hashlib
import json
from pathlib import Path
import struct
import tempfile

from surface_store import SurfaceStore


def seed(root: Path) -> None:
    (root / "receipts").mkdir(parents=True)
    values = {
        "current_memory.json": {"m": "one"},
        "current_task.json": {"task": "sync"},
        "active_path.json": {"path": "surface"},
        "closed_topics.json": [],
        "timeline_head.json": {"n": 1},
        "provenance.json": {"source": "validator"},
        "receipts/latest.json": {"status": "PASS"},
    }
    for rel, value in values.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")
    (root / "aux_phi").write_bytes(struct.pack("<" + "d" * 36, *([0.125] * 36)))


def main() -> int:
    checks: dict[str, bool] = {}
    with tempfile.TemporaryDirectory(prefix="noema_surface_sync_") as td:
        base = Path(td)
        seed_root = base / "seed"
        seed(seed_root)
        store = SurfaceStore(base / "kanon/noema/library", base / "shm", base / "kanon/runtime/surface-fallback")
        store.initialize()
        store.import_seed(seed_root)
        store.project()
        checks["project_roundtrip"] = json.loads((base / "shm/current_task.json").read_text())["task"] == "sync"

        (base / "shm/current_task.json").write_text(json.dumps({"task": "changed"}), encoding="utf-8")
        store.capture()
        checks["capture_persistent"] = json.loads((base / "kanon/noema/library/surface_store/canonical/current_task.json").read_text())["task"] == "changed"
        checks["fallback_refreshed"] = json.loads((base / "kanon/runtime/surface-fallback/current_task.json").read_text())["task"] == "changed"
        checks["generation_incremented"] = store.read_manifest()["generation"] == 2

    with tempfile.TemporaryDirectory(prefix="noema_surface_sync_conflict_") as td:
        base = Path(td)
        seed_root = base / "seed"
        seed(seed_root)
        store = SurfaceStore(base / "lib", base / "shm", base / "fallback")
        store.initialize(); store.import_seed(seed_root); store.project()
        (base / "shm/current_task.json").write_text(json.dumps({"task": "surface"}), encoding="utf-8")
        canonical = base / "lib/surface_store/canonical/current_task.json"
        raw = json.dumps({"task": "disk"}).encode()
        canonical.write_bytes(raw)
        manifest = store.read_manifest()
        manifest["generation"] = 2
        manifest["files"]["current_task.json"] = {"sha256": hashlib.sha256(raw).hexdigest(), "size": len(raw)}
        store.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        try:
            store.capture()
            conflict = False
        except RuntimeError:
            conflict = True
        checks["conflict_fails_closed"] = conflict
        checks["conflict_quarantined"] = bool(list((base / "lib/surface_store/quarantine").glob("*_conflict.json")))

    status = "PASS" if all(checks.values()) else "FAIL"
    print(json.dumps({"status": status, "checks": checks}, indent=2, sort_keys=True))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
