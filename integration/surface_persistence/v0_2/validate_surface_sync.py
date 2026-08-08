from __future__ import annotations

import json
from pathlib import Path
import struct
import tempfile

from surface_sync import PersistentSurfaceSync, atomic_write, json_bytes, sha256


def seed(root: Path) -> None:
    (root / "receipts").mkdir(parents=True)
    for rel, value in {
        "current_memory.json": {"m": "one"},
        "current_task.json": {"task": "sync"},
        "active_path.json": {"path": "surface"},
        "closed_topics.json": [],
        "timeline_head.json": {"n": 1},
        "provenance.json": {"source": "validator"},
        "receipts/latest.json": {"status": "PASS"},
    }.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(value), encoding="utf-8")
    (root / "aux_phi").write_bytes(struct.pack("<" + "d" * 36, *([0.125] * 36)))


def main() -> int:
    checks = {}
    with tempfile.TemporaryDirectory() as td:
        b = Path(td); s = b / "seed"; seed(s)
        x = PersistentSurfaceSync(b / "kanon/noema/library", b / "shm", b / "kanon/runtime/surface-fallback")
        x.init(); x.import_seed(s); x.project()
        checks["project"] = json.loads((b / "shm/current_task.json").read_text())["task"] == "sync"
        (b / "shm/current_task.json").write_text(json.dumps({"task": "ram"}))
        checks["ram_capture"] = x.sync_once()["decision"] == "CAPTURE"
        checks["capture_persistent"] = json.loads((b / "kanon/noema/library/surface_store/canonical/current_task.json").read_text())["task"] == "ram"
        checks["fallback"] = json.loads((b / "kanon/runtime/surface-fallback/current_task.json").read_text())["task"] == "ram"

    with tempfile.TemporaryDirectory() as td:
        b = Path(td); s = b / "seed"; seed(s)
        x = PersistentSurfaceSync(b / "lib", b / "shm", b / "fallback")
        x.init(); x.import_seed(s); x.project()
        (b / "shm/current_task.json").write_text(json.dumps({"task": "ram"}))
        raw = json.dumps({"task": "disk"}).encode()
        atomic_write(b / "lib/surface_store/canonical/current_task.json", raw)
        m = x.manifest(); m["generation"] = 2
        m["files"]["current_task.json"] = {"sha256": sha256(raw), "size": len(raw)}
        atomic_write(x.manifest_path, json_bytes(m))
        try:
            x.capture(); conflict = False
        except RuntimeError:
            conflict = True
        checks["same_file_conflict"] = conflict
        checks["quarantine"] = bool(list((b / "lib/surface_store/quarantine").glob("*_conflict.json")))

    with tempfile.TemporaryDirectory() as td:
        b = Path(td); s = b / "seed"; seed(s)
        x = PersistentSurfaceSync(b / "lib", b / "shm", b / "fallback")
        x.init(); x.import_seed(s); x.project()
        (b / "lib/surface_store/canonical/current_task.json").write_text(json.dumps({"task": "illegal"}))
        try:
            x.sync_once(); drift = False
        except RuntimeError:
            drift = True
        checks["direct_disk_drift_fails"] = drift

    with tempfile.TemporaryDirectory() as td:
        b = Path(td); s = b / "seed"; seed(s)
        x = PersistentSurfaceSync(b / "lib", b / "shm", b / "fallback")
        x.init(); x.import_seed(s); x.project()
        raw = json.dumps({"task": "disk-generation"}).encode()
        atomic_write(b / "lib/surface_store/canonical/current_task.json", raw)
        m = x.manifest(); m["generation"] = 2
        m["files"]["current_task.json"] = {"sha256": sha256(raw), "size": len(raw)}
        atomic_write(x.manifest_path, json_bytes(m))
        checks["disk_generation_project"] = x.sync_once()["decision"] == "PROJECT"
        checks["projected_new_disk"] = json.loads((b / "shm/current_task.json").read_text())["task"] == "disk-generation"

    status = "PASS" if all(checks.values()) else "FAIL"
    print(json.dumps({"status": status, "checks": checks}, indent=2, sort_keys=True))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
