#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import zipfile
from pathlib import Path
from typing import Any

SCHEMA = "noema.runtime-source-guard/v1"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def resolve_path(root: Path, value: str) -> Path:
    p = Path(os.path.expandvars(os.path.expanduser(value)))
    return p if p.is_absolute() else root / p


def verify_archive(source_id: str, pin: dict[str, Any], mount: dict[str, Any], library_root: Path) -> dict[str, Any]:
    path_value = mount.get("archive_path") or mount.get("artifact_path")
    if not path_value:
        raise RuntimeError(f"BLOCKED_LIBRARY_TRANSFER:{source_id}:path_missing")
    path = resolve_path(library_root, str(path_value))
    if not path.is_file():
        raise RuntimeError(f"BLOCKED_LIBRARY_TRANSFER:{source_id}:missing:{path}")
    expected_archive = pin.get("archive_sha256") or pin.get("sha256")
    actual_archive = sha256_file(path)
    if expected_archive and actual_archive != expected_archive:
        raise RuntimeError(f"RUNTIME_SOURCE_HASH_MISMATCH:{source_id}:archive")
    result: dict[str, Any] = {
        "source_id": source_id,
        "path": str(path),
        "archive_sha256": actual_archive,
        "status": "PASS",
    }
    member = pin.get("member_path")
    expected_member = pin.get("member_sha256")
    if member:
        if not zipfile.is_zipfile(path):
            raise RuntimeError(f"RUNTIME_SOURCE_NOT_ZIP:{source_id}:{path}")
        with zipfile.ZipFile(path, "r") as zf:
            try:
                raw = zf.read(str(member))
            except KeyError:
                raise RuntimeError(f"RUNTIME_SOURCE_MEMBER_MISSING:{source_id}:{member}")
        actual_member = hashlib.sha256(raw).hexdigest()
        if expected_member and actual_member != expected_member:
            raise RuntimeError(f"RUNTIME_SOURCE_HASH_MISMATCH:{source_id}:member")
        result["member_path"] = member
        result["member_sha256"] = actual_member
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify mounted Library runtime sources against canonical pins")
    ap.add_argument("--library-root", required=True)
    ap.add_argument("--pin-file", required=True)
    ap.add_argument("--mount-manifest")
    args = ap.parse_args()

    library = Path(args.library_root)
    pin_file = Path(args.pin_file)
    mount_file = Path(args.mount_manifest) if args.mount_manifest else library / "runtime_sources" / "MOUNT.json"
    failures: list[str] = []
    results: list[dict[str, Any]] = []
    try:
        pins = json.loads(pin_file.read_text(encoding="utf-8"))
        if pins.get("schema") != "noema.runtime-source-pin/v1":
            raise RuntimeError("PIN_SCHEMA_INVALID")
        if not mount_file.is_file():
            raise RuntimeError(f"BLOCKED_LIBRARY_TRANSFER:mount_manifest_missing:{mount_file}")
        mounts = json.loads(mount_file.read_text(encoding="utf-8"))
        if mounts.get("schema") != "noema.runtime-mount/v1":
            raise RuntimeError("MOUNT_SCHEMA_INVALID")
        mount_sources = mounts.get("sources") or {}
        for source_id, source_pin in (pins.get("sources") or {}).items():
            required = bool(source_pin.get("required_for_boot"))
            source_mount = mount_sources.get(source_id)
            if source_mount is None:
                if required:
                    raise RuntimeError(f"BLOCKED_LIBRARY_TRANSFER:{source_id}:mount_entry_missing")
                results.append({"source_id": source_id, "status": "PINNED_NOT_MOUNTED_OPTIONAL"})
                continue
            try:
                results.append(verify_archive(source_id, source_pin, source_mount, library))
            except Exception as exc:
                if required:
                    raise
                results.append({"source_id": source_id, "status": "OPTIONAL_MOUNT_INVALID", "error": f"{type(exc).__name__}:{exc}"})
    except Exception as exc:
        failures.append(f"{type(exc).__name__}:{exc}")

    out = {
        "schema": SCHEMA,
        "library_root": str(library),
        "pin_file": str(pin_file),
        "mount_manifest": str(mount_file),
        "status": "PASS" if not failures else "BLOCKED",
        "sources": results,
        "failures": failures,
        "fail_closed": True,
    }
    print(json.dumps(out, sort_keys=True, ensure_ascii=False))
    return 0 if not failures else 23


if __name__ == "__main__":
    raise SystemExit(main())
