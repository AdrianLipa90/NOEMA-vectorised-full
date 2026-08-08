from __future__ import annotations

import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import struct
import tempfile
import time
from typing import Any

AUX_DIM = 36
AUX_BYTES = 288
CANONICAL_FILES = (
    "current_memory.json",
    "current_task.json",
    "active_path.json",
    "closed_topics.json",
    "timeline_head.json",
    "provenance.json",
    "receipts/latest.json",
    "aux_phi",
)
JSON_FILES = frozenset(x for x in CANONICAL_FILES if x.endswith(".json"))
MARKER = ".noema_projection.json"


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def atomic_write(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    tmp = Path(name)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(raw)
            fh.flush()
            os.fsync(fh.fileno())
        os.chmod(tmp, 0o600)
        os.replace(tmp, path)
        dfd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(dfd)
        finally:
            os.close(dfd)
    finally:
        tmp.unlink(missing_ok=True)


def validate(rel: str, raw: bytes) -> None:
    if rel in JSON_FILES:
        json.loads(raw.decode("utf-8"))
    elif rel == "aux_phi":
        if len(raw) != AUX_BYTES:
            raise ValueError(f"aux_phi size {len(raw)} != {AUX_BYTES}")
        if not all(math.isfinite(x) for x in struct.unpack("<" + "d" * AUX_DIM, raw)):
            raise ValueError("aux_phi contains non-finite values")


class PersistentSurfaceSync:
    def __init__(self, library_root: str | Path, surface_root: str | Path, fallback_root: str | Path):
        self.library_root = Path(library_root)
        self.store = self.library_root / "surface_store"
        self.canonical = self.store / "canonical"
        self.journal = self.store / "journal/events.jsonl"
        self.receipts = self.store / "sync_receipts"
        self.quarantine = self.store / "quarantine"
        self.lock_path = self.store / "locks/surface.lock"
        self.manifest_path = self.store / "manifest.json"
        self.surface = Path(surface_root)
        self.fallback = Path(fallback_root)

    def init(self) -> dict[str, Any]:
        for p in (self.canonical, self.receipts, self.quarantine, self.lock_path.parent, self.fallback):
            p.mkdir(parents=True, exist_ok=True)
        if not self.manifest_path.exists():
            atomic_write(self.manifest_path, json_bytes({
                "schema": "noema.persistent-surface-store/v2",
                "generation": 0,
                "files": {},
                "surface_root": str(self.surface),
                "fallback_root": str(self.fallback),
                "created_ns": time.time_ns(),
            }))
        return self.manifest()

    @contextmanager
    def locked(self):
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(self.lock_path, os.O_CREAT | os.O_RDWR, 0o600)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX)
            yield
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
            os.close(fd)

    def manifest(self) -> dict[str, Any]:
        if not self.manifest_path.exists():
            return self.init()
        return json.loads(self.manifest_path.read_text(encoding="utf-8"))

    def log(self, event: dict[str, Any]) -> None:
        self.journal.parent.mkdir(parents=True, exist_ok=True)
        with self.journal.open("ab", buffering=0) as fh:
            fh.write(json_bytes(event))
            os.fsync(fh.fileno())

    def receipt(self, op: str, payload: dict[str, Any]) -> dict[str, Any]:
        body = dict(payload)
        body["receipt_sha256"] = sha256(json_bytes(payload))
        atomic_write(self.receipts / f"{time.time_ns()}_{op}.json", json_bytes(body))
        atomic_write(self.receipts / "latest.json", json_bytes(body))
        return body

    def canonical_conflicts(self, manifest: dict[str, Any]) -> list[dict[str, Any]]:
        out = []
        for rel, meta in manifest.get("files", {}).items():
            p = self.canonical / rel
            if not p.is_file():
                out.append({"file": rel, "reason": "MISSING", "expected": meta["sha256"]})
                continue
            actual = sha256(p.read_bytes())
            if actual != meta["sha256"]:
                out.append({"file": rel, "reason": "DRIFT", "expected": meta["sha256"], "actual": actual})
        return out

    def assert_canonical(self, manifest: dict[str, Any]) -> None:
        conflicts = self.canonical_conflicts(manifest)
        if not conflicts:
            return
        event = {
            "op": "CANONICAL_DRIFT",
            "generation": manifest["generation"],
            "conflicts": conflicts,
            "timestamp_ns": time.time_ns(),
        }
        atomic_write(self.quarantine / f"{time.time_ns()}_canonical_drift.json", json_bytes(event))
        self.log(event)
        raise RuntimeError("persistent canonical drift")

    def refresh_fallback(self, manifest: dict[str, Any]) -> None:
        for rel, meta in manifest["files"].items():
            raw = (self.canonical / rel).read_bytes()
            if sha256(raw) != meta["sha256"]:
                raise RuntimeError(f"canonical hash mismatch: {rel}")
            atomic_write(self.fallback / rel, raw)
        atomic_write(self.fallback / MARKER, json_bytes({
            "schema": "noema.surface-fallback/v2",
            "generation": manifest["generation"],
            "files": manifest["files"],
            "updated_ns": time.time_ns(),
        }))

    def import_seed(self, seed_root: str | Path) -> dict[str, Any]:
        seed = Path(seed_root)
        with self.locked():
            self.init()
            manifest = self.manifest()
            if manifest["generation"] != 0 or manifest["files"]:
                raise RuntimeError("seed import allowed only into empty store")
            files = {}
            for rel in CANONICAL_FILES:
                p = seed / rel
                if not p.is_file():
                    continue
                raw = p.read_bytes()
                validate(rel, raw)
                atomic_write(self.canonical / rel, raw)
                files[rel] = {"sha256": sha256(raw), "size": len(raw)}
            if not files:
                raise RuntimeError("seed contained no canonical inputs")
            manifest["generation"] = 1
            manifest["files"] = files
            manifest["seed_source"] = str(seed)
            manifest["updated_ns"] = time.time_ns()
            atomic_write(self.manifest_path, json_bytes(manifest))
            self.refresh_fallback(manifest)
            event = {"op": "IMPORT_SEED", "generation": 1, "files": sorted(files), "timestamp_ns": time.time_ns()}
            self.log(event)
            return self.receipt("import_seed", event)

    def project(self) -> dict[str, Any]:
        with self.locked():
            self.init()
            manifest = self.manifest()
            self.assert_canonical(manifest)
            self.surface.mkdir(parents=True, exist_ok=True)
            projected = {}
            for rel, meta in manifest["files"].items():
                raw = (self.canonical / rel).read_bytes()
                validate(rel, raw)
                if sha256(raw) != meta["sha256"]:
                    raise RuntimeError(f"canonical hash mismatch: {rel}")
                atomic_write(self.surface / rel, raw)
                projected[rel] = {"sha256": meta["sha256"], "size": meta["size"]}
            atomic_write(self.surface / MARKER, json_bytes({
                "schema": "noema.ephemeral-projection/v2",
                "source_generation": manifest["generation"],
                "projected_files": projected,
                "manifest_sha256": sha256(self.manifest_path.read_bytes()),
                "projected_ns": time.time_ns(),
            }))
            self.refresh_fallback(manifest)
            event = {"op": "PROJECT", "generation": manifest["generation"], "files": sorted(projected), "timestamp_ns": time.time_ns()}
            self.log(event)
            return self.receipt("project", event)

    def _surface_changes(self, marker: dict[str, Any]) -> dict[str, bytes]:
        changes = {}
        base = marker.get("projected_files", {})
        for rel in CANONICAL_FILES:
            p = self.surface / rel
            if not p.is_file():
                continue
            raw = p.read_bytes()
            validate(rel, raw)
            if sha256(raw) != (base.get(rel) or {}).get("sha256"):
                changes[rel] = raw
        return changes

    def capture(self) -> dict[str, Any]:
        with self.locked():
            self.init()
            marker_path = self.surface / MARKER
            if not marker_path.is_file():
                raise RuntimeError("surface projection marker missing")
            marker = json.loads(marker_path.read_text(encoding="utf-8"))
            manifest = self.manifest()
            self.assert_canonical(manifest)
            changes = self._surface_changes(marker)
            base_generation = int(marker["source_generation"])
            conflicts = []
            for rel, raw in changes.items():
                projected = (marker.get("projected_files", {}).get(rel) or {}).get("sha256")
                persistent = (manifest["files"].get(rel) or {}).get("sha256")
                if projected is None or persistent is None:
                    conflicts.append({
                        "file": rel,
                        "reason": "UNPROJECTED_SURFACE_FILE",
                        "surface": sha256(raw),
                        "projected": projected,
                        "persistent": persistent,
                    })
                elif manifest["generation"] != base_generation and persistent != projected:
                    conflicts.append({
                        "file": rel,
                        "reason": "CONCURRENT_SAME_FILE_CHANGE",
                        "surface": sha256(raw),
                        "projected": projected,
                        "persistent": persistent,
                    })
            if conflicts:
                event = {
                    "op": "CONFLICT",
                    "base_generation": base_generation,
                    "generation": manifest["generation"],
                    "conflicts": conflicts,
                    "timestamp_ns": time.time_ns(),
                }
                atomic_write(self.quarantine / f"{time.time_ns()}_conflict.json", json_bytes(event))
                self.log(event)
                raise RuntimeError("surface/persistent conflict")
            if not changes:
                return {"op": "CAPTURE_NOOP", "generation": manifest["generation"]}

            for rel, raw in changes.items():
                atomic_write(self.canonical / rel, raw)
                manifest["files"][rel] = {"sha256": sha256(raw), "size": len(raw)}
            manifest["generation"] += 1
            manifest["updated_ns"] = time.time_ns()
            atomic_write(self.manifest_path, json_bytes(manifest))
            self.refresh_fallback(manifest)

            projected = {}
            for rel, meta in manifest["files"].items():
                raw = (self.canonical / rel).read_bytes()
                atomic_write(self.surface / rel, raw)
                projected[rel] = {"sha256": meta["sha256"], "size": meta["size"]}
            atomic_write(self.surface / MARKER, json_bytes({
                "schema": "noema.ephemeral-projection/v2",
                "source_generation": manifest["generation"],
                "projected_files": projected,
                "manifest_sha256": sha256(self.manifest_path.read_bytes()),
                "projected_ns": time.time_ns(),
            }))
            event = {
                "op": "CAPTURE_COMMIT",
                "base_generation": base_generation,
                "generation": manifest["generation"],
                "changed_files": sorted(changes),
                "timestamp_ns": time.time_ns(),
            }
            self.log(event)
            return self.receipt("capture", event)

    def sync_once(self) -> dict[str, Any]:
        self.init()
        manifest = self.manifest()
        self.assert_canonical(manifest)
        marker_path = self.surface / MARKER
        if not marker_path.is_file():
            return {"decision": "PROJECT", "receipt": self.project()}
        marker = json.loads(marker_path.read_text(encoding="utf-8"))
        if self._surface_changes(marker):
            return {"decision": "CAPTURE", "receipt": self.capture()}
        if int(marker.get("source_generation", -1)) != int(manifest["generation"]):
            return {"decision": "PROJECT", "receipt": self.project()}
        return {"decision": "NOOP", "generation": manifest["generation"]}

    def watch(self, interval: float = 0.25) -> None:
        if interval <= 0:
            raise ValueError("interval must be positive")
        while True:
            self.sync_once()
            time.sleep(interval)

    def status(self) -> dict[str, Any]:
        self.init()
        manifest = self.manifest()
        marker_path = self.surface / MARKER
        marker = json.loads(marker_path.read_text(encoding="utf-8")) if marker_path.is_file() else None
        return {
            "schema": "noema.surface-sync-status/v2",
            "generation": manifest["generation"],
            "projection_generation": marker.get("source_generation") if marker else None,
            "canonical_conflicts": self.canonical_conflicts(manifest),
            "surface_changed": bool(self._surface_changes(marker)) if marker else None,
        }


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--library-root", required=True)
    p.add_argument("--surface-root", default="/dev/shm/ciel_noema")
    p.add_argument("--fallback-root", required=True)
    sub = p.add_subparsers(dest="op", required=True)
    sub.add_parser("init")
    seed = sub.add_parser("import-seed")
    seed.add_argument("--seed-root", required=True)
    sub.add_parser("project")
    sub.add_parser("capture")
    sub.add_parser("sync-once")
    watch = sub.add_parser("watch")
    watch.add_argument("--interval", type=float, default=0.25)
    sub.add_parser("status")
    return p


def main(argv: list[str] | None = None) -> int:
    a = parser().parse_args(argv)
    sync = PersistentSurfaceSync(a.library_root, a.surface_root, a.fallback_root)
    if a.op == "init":
        out = sync.init()
    elif a.op == "import-seed":
        out = sync.import_seed(a.seed_root)
    elif a.op == "project":
        out = sync.project()
    elif a.op == "capture":
        out = sync.capture()
    elif a.op == "sync-once":
        out = sync.sync_once()
    elif a.op == "watch":
        sync.watch(a.interval)
        return 0
    else:
        out = sync.status()
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
