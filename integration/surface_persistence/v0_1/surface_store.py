from __future__ import annotations

import argparse
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
AUX_BYTES = AUX_DIM * 8
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
PROJECTION_MARKER = ".noema_projection.json"
MANIFEST_NAME = "manifest.json"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def fsync_dir(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def atomic_write(path: Path, raw: bytes, mode: int = 0o600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    tmp_path = Path(tmp)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(raw)
            fh.flush()
            os.fsync(fh.fileno())
        os.chmod(tmp_path, mode)
        os.replace(tmp_path, path)
        fsync_dir(path.parent)
    finally:
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)


def validate_payload(rel: str, raw: bytes) -> None:
    if rel in JSON_FILES:
        try:
            json.loads(raw.decode("utf-8"))
        except Exception as exc:
            raise ValueError(f"{rel}: invalid JSON: {exc}") from exc
        return
    if rel == "aux_phi":
        if len(raw) != AUX_BYTES:
            raise ValueError(f"aux_phi: size {len(raw)} != {AUX_BYTES}")
        vals = struct.unpack("<" + "d" * AUX_DIM, raw)
        if not all(math.isfinite(v) for v in vals):
            raise ValueError("aux_phi: non-finite value")


class SurfaceStore:
    def __init__(self, library_root: str | Path, surface_root: str | Path, fallback_root: str | Path):
        self.library_root = Path(library_root)
        self.store_root = self.library_root / "surface_store"
        self.canonical_root = self.store_root / "canonical"
        self.journal_root = self.store_root / "journal"
        self.receipt_root = self.store_root / "sync_receipts"
        self.quarantine_root = self.store_root / "quarantine"
        self.lock_root = self.store_root / "locks"
        self.surface_root = Path(surface_root)
        self.fallback_root = Path(fallback_root)
        self.manifest_path = self.store_root / MANIFEST_NAME
        self.lock_path = self.lock_root / "surface.lock"

    def initialize(self) -> dict[str, Any]:
        for path in (self.canonical_root, self.journal_root, self.receipt_root, self.quarantine_root, self.lock_root, self.fallback_root):
            path.mkdir(parents=True, exist_ok=True)
        if not self.manifest_path.exists():
            manifest = {
                "schema": "noema.persistent-surface-store/v1",
                "generation": 0,
                "files": {},
                "surface_root": str(self.surface_root),
                "fallback_root": str(self.fallback_root),
                "created_ns": time.time_ns(),
            }
            atomic_write(self.manifest_path, canonical_json_bytes(manifest))
        return self.read_manifest()

    def _locked(self):
        self.lock_root.mkdir(parents=True, exist_ok=True)
        fd = os.open(self.lock_path, os.O_CREAT | os.O_RDWR, 0o600)
        class Lock:
            def __enter__(inner):
                fcntl.flock(fd, fcntl.LOCK_EX)
                return inner
            def __exit__(inner, exc_type, exc, tb):
                fcntl.flock(fd, fcntl.LOCK_UN)
                os.close(fd)
        return Lock()

    def read_manifest(self) -> dict[str, Any]:
        if not self.manifest_path.exists():
            return self.initialize()
        return json.loads(self.manifest_path.read_text(encoding="utf-8"))

    def _append_journal(self, event: dict[str, Any]) -> None:
        path = self.journal_root / "events.jsonl"
        with path.open("ab", buffering=0) as fh:
            fh.write(canonical_json_bytes(event))
            os.fsync(fh.fileno())
        fsync_dir(path.parent)

    def _receipt(self, name: str, payload: dict[str, Any]) -> dict[str, Any]:
        body = dict(payload)
        body["receipt_sha256"] = sha256_bytes(canonical_json_bytes(payload))
        filename = f"{time.time_ns()}_{name}.json"
        atomic_write(self.receipt_root / filename, canonical_json_bytes(body))
        atomic_write(self.receipt_root / "latest.json", canonical_json_bytes(body))
        return body

    def import_seed(self, seed_root: str | Path) -> dict[str, Any]:
        seed_root = Path(seed_root)
        with self._locked():
            self.initialize()
            manifest = self.read_manifest()
            if manifest["generation"] != 0 or manifest["files"]:
                raise RuntimeError("persistent store is not empty; seed import refused")
            files = {}
            imported = []
            for rel in CANONICAL_FILES:
                src = seed_root / rel
                if not src.is_file():
                    continue
                raw = src.read_bytes()
                validate_payload(rel, raw)
                atomic_write(self.canonical_root / rel, raw)
                files[rel] = {"sha256": sha256_bytes(raw), "size": len(raw)}
                imported.append(rel)
            new = dict(manifest)
            new["generation"] = 1
            new["files"] = files
            new["seed_source"] = str(seed_root)
            new["updated_ns"] = time.time_ns()
            atomic_write(self.manifest_path, canonical_json_bytes(new))
            event = {"op": "IMPORT_SEED", "generation": 1, "files": imported, "timestamp_ns": time.time_ns()}
            self._append_journal(event)
            self._refresh_fallback(new)
            return self._receipt("import_seed", event)

    def _refresh_fallback(self, manifest: dict[str, Any]) -> None:
        for rel, meta in manifest.get("files", {}).items():
            src = self.canonical_root / rel
            if not src.is_file():
                continue
            raw = src.read_bytes()
            if sha256_bytes(raw) != meta["sha256"]:
                raise RuntimeError(f"persistent canonical drift for {rel}")
            atomic_write(self.fallback_root / rel, raw)
        marker = {
            "schema": "noema.surface-fallback/v1",
            "generation": manifest["generation"],
            "files": manifest.get("files", {}),
            "source": str(self.canonical_root),
            "updated_ns": time.time_ns(),
        }
        atomic_write(self.fallback_root / PROJECTION_MARKER, canonical_json_bytes(marker))

    def project(self) -> dict[str, Any]:
        with self._locked():
            self.initialize()
            manifest = self.read_manifest()
            self.surface_root.mkdir(parents=True, exist_ok=True)
            projected = {}
            for rel, meta in manifest.get("files", {}).items():
                raw = (self.canonical_root / rel).read_bytes()
                validate_payload(rel, raw)
                digest = sha256_bytes(raw)
                if digest != meta["sha256"]:
                    raise RuntimeError(f"canonical hash mismatch: {rel}")
                atomic_write(self.surface_root / rel, raw)
                projected[rel] = {"sha256": digest, "size": len(raw)}
            marker = {
                "schema": "noema.ephemeral-projection/v1",
                "source_generation": manifest["generation"],
                "projected_files": projected,
                "persistent_manifest_sha256": sha256_bytes(self.manifest_path.read_bytes()),
                "projected_ns": time.time_ns(),
            }
            atomic_write(self.surface_root / PROJECTION_MARKER, canonical_json_bytes(marker))
            self._refresh_fallback(manifest)
            event = {"op": "PROJECT", "generation": manifest["generation"], "files": sorted(projected), "timestamp_ns": time.time_ns()}
            self._append_journal(event)
            return self._receipt("project", event)

    def capture(self) -> dict[str, Any]:
        with self._locked():
            self.initialize()
            marker_path = self.surface_root / PROJECTION_MARKER
            if not marker_path.is_file():
                raise RuntimeError("surface has no projection marker; capture refused")
            marker = json.loads(marker_path.read_text(encoding="utf-8"))
            manifest = self.read_manifest()
            base_generation = int(marker["source_generation"])
            base = marker.get("projected_files", {})
            changed: dict[str, bytes] = {}
            conflicts = []
            for rel in CANONICAL_FILES:
                surface_path = self.surface_root / rel
                if not surface_path.is_file():
                    continue
                raw = surface_path.read_bytes()
                validate_payload(rel, raw)
                surface_sha = sha256_bytes(raw)
                projected_sha = (base.get(rel) or {}).get("sha256")
                if surface_sha == projected_sha:
                    continue
                persistent_sha = (manifest.get("files", {}).get(rel) or {}).get("sha256")
                if manifest["generation"] != base_generation and persistent_sha != projected_sha:
                    conflicts.append({
                        "file": rel,
                        "surface_sha256": surface_sha,
                        "projected_sha256": projected_sha,
                        "persistent_sha256": persistent_sha,
                    })
                else:
                    changed[rel] = raw
            if conflicts:
                q = {
                    "schema": "noema.surface-sync-conflict/v1",
                    "base_generation": base_generation,
                    "current_generation": manifest["generation"],
                    "conflicts": conflicts,
                    "timestamp_ns": time.time_ns(),
                }
                atomic_write(self.quarantine_root / f"{time.time_ns()}_conflict.json", canonical_json_bytes(q))
                self._append_journal({"op": "CONFLICT", **q})
                raise RuntimeError(f"surface capture conflict: {[x['file'] for x in conflicts]}")
            if not changed:
                event = {"op": "CAPTURE_NOOP", "generation": manifest["generation"], "timestamp_ns": time.time_ns()}
                self._append_journal(event)
                return self._receipt("capture_noop", event)
            new_files = dict(manifest.get("files", {}))
            for rel, raw in changed.items():
                atomic_write(self.canonical_root / rel, raw)
                new_files[rel] = {"sha256": sha256_bytes(raw), "size": len(raw)}
            new = dict(manifest)
            new["generation"] = int(manifest["generation"]) + 1
            new["files"] = new_files
            new["updated_ns"] = time.time_ns()
            atomic_write(self.manifest_path, canonical_json_bytes(new))
            self._refresh_fallback(new)
            event = {
                "op": "CAPTURE_COMMIT",
                "base_generation": base_generation,
                "generation": new["generation"],
                "changed_files": sorted(changed),
                "timestamp_ns": time.time_ns(),
            }
            self._append_journal(event)
            receipt = self._receipt("capture", event)
            projected = {}
            for rel, meta in new_files.items():
                raw = (self.canonical_root / rel).read_bytes()
                atomic_write(self.surface_root / rel, raw)
                projected[rel] = {"sha256": meta["sha256"], "size": meta["size"]}
            marker = {
                "schema": "noema.ephemeral-projection/v1",
                "source_generation": new["generation"],
                "projected_files": projected,
                "persistent_manifest_sha256": sha256_bytes(self.manifest_path.read_bytes()),
                "projected_ns": time.time_ns(),
            }
            atomic_write(self.surface_root / PROJECTION_MARKER, canonical_json_bytes(marker))
            return receipt


def build_parser() -> argparse.ArgumentParser:
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
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    store = SurfaceStore(args.library_root, args.surface_root, args.fallback_root)
    if args.op == "init":
        out = store.initialize()
    elif args.op == "import-seed":
        out = store.import_seed(args.seed_root)
    elif args.op == "project":
        out = store.project()
    else:
        out = store.capture()
    print(json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
