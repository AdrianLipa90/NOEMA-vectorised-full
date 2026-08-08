#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import secrets
import socket
import struct
import sys
import threading
import time

import numpy as np

N = 36
BYTES = N * 8


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def atomic_write(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.{time.time_ns()}.tmp")
    with tmp.open("wb") as fh:
        fh.write(raw)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def valid_v36(raw: bytes) -> bool:
    if len(raw) != BYTES:
        return False
    try:
        values = struct.unpack("<36d", raw)
    except struct.error:
        return False
    return all(math.isfinite(value) for value in values)


def save_npy_atomic(path: Path, value: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with tmp.open("wb") as fh:
        np.save(fh, np.asarray(value, dtype=np.float64))
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def load_phi(path: Path) -> np.ndarray | None:
    if not path.is_file():
        return None
    value = np.asarray(np.load(path, allow_pickle=False), dtype=np.float64).reshape(-1)
    if value.size != N or not np.all(np.isfinite(value)):
        raise RuntimeError("invalid persistent phi")
    return value


def process_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


class HealthSocket(threading.Thread):
    daemon = True

    def __init__(self, path: Path, status_path: Path):
        super().__init__()
        self.path = path
        self.status_path = status_path

    def run(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.unlink(missing_ok=True)
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(str(self.path))
        os.chmod(self.path, 0o600)
        server.listen(4)
        server.settimeout(0.5)
        while True:
            try:
                client, _ = server.accept()
            except socket.timeout:
                continue
            except Exception:
                return
            try:
                payload = self.status_path.read_bytes() if self.status_path.is_file() else b'{"status":"STARTING"}'
                client.sendall(payload + b"\n")
            finally:
                client.close()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--surface-root", default="/dev/shm/ciel_noema")
    ap.add_argument("--persistent-root", required=True)
    ap.add_argument("--geometry-root")
    ap.add_argument("--socket", default="/run/user/1000/noema/ciel_headless.sock")
    ap.add_argument("--interval", type=float, default=0.2)
    args = ap.parse_args()

    if args.geometry_root:
        sys.path.insert(0, args.geometry_root)
    from ciel_geometry.noema_surface_mmap import (
        evolve_surface,
        flush_surface,
        initialize_surface,
        open_surface,
    )

    root = Path(args.surface_root)
    persistent = Path(args.persistent_root)
    root.mkdir(parents=True, exist_ok=True)
    persistent.mkdir(parents=True, exist_ok=True)
    phi_store = persistent / "surface/phi.npy"
    restored = load_phi(phi_store)
    init_mode = "RESTORED_PERSISTENT_PHI"

    if not (root / "phi").is_file():
        initialize_surface(root, seed=42)
        surface = open_surface(root)
        if restored is not None:
            surface["phi"][...] = restored
            flush_surface(surface)
        else:
            init_mode = "INITIALIZED_NATIVE_SURFACE_SEED_42"
            save_npy_atomic(phi_store, np.asarray(surface["phi"], dtype=np.float64))
    else:
        surface = open_surface(root)

    status_path = root / "tether_runtime_status.json"
    receipt_path = root / "receipts/tether_latest.json"
    binding_path = root / "ciel_binding_status"
    HealthSocket(Path(args.socket), status_path).start()
    seq = 0
    last_persist = 0.0

    while True:
        try:
            coherence = float(evolve_surface(surface, dt=0.01, flush=True))
            phi_raw = (root / "phi").read_bytes()
            if not valid_v36(phi_raw):
                raise RuntimeError("native phi invalid")

            aux_status_path = root / "aux_stream_status.json"
            if not aux_status_path.is_file():
                raise RuntimeError("AUX producer heartbeat missing")
            aux_status = json.loads(aux_status_path.read_text(encoding="utf-8"))
            aux_age = (time.time_ns() - int(aux_status.get("heartbeat_ns", 0))) / 1e9
            if (
                aux_status.get("status") != "ACTIVE"
                or aux_age > 2.0
                or not process_alive(int(aux_status.get("pid", -1)))
            ):
                raise RuntimeError(f"AUX producer is not fresh ACTIVE: age={aux_age:.3f}s")

            aux_raw = (root / "aux_phi").read_bytes()
            if not valid_v36(aux_raw):
                raise RuntimeError("aux_phi invalid")

            # The hard contract permits an explicit lossless identity/echo mode.
            # This is a distinct producer path; aux_phi itself is never overwritten.
            atomic_write(root / "aux_feedback_phi", aux_raw)
            feedback_raw = (root / "aux_feedback_phi").read_bytes()
            if feedback_raw != aux_raw:
                raise RuntimeError("lossless identity feedback mismatch")

            input_sha = sha256(aux_raw)
            feedback_sha = sha256(feedback_raw)
            phi_sha = sha256(phi_raw)
            read_rows = []
            for rel in ("current_memory.json", "current_task.json", "active_path.json", "provenance.json"):
                path = root / rel
                if not path.is_file():
                    raise RuntimeError(f"missing canonical input {rel}")
                read_rows.append({"path": rel, "sha256": sha256(path.read_bytes())})
            read_set_sha = sha256(canonical_bytes(read_rows))

            nonce = secrets.token_hex(16)
            host = socket.gethostname()
            created_ns = time.time_ns()
            request = {
                "schema": "noema.aux-tether-request/v1",
                "mode": "identity_echo",
                "nonce": nonce,
                "source_host_identifier": host,
                "input_v36_sha256": input_sha,
                "read_set_sha256": read_set_sha,
                "created_unix_ns": created_ns,
            }
            request_sha = sha256(canonical_bytes(request))
            transport = {
                "nonce": nonce,
                "mode": "identity_echo",
                "request_sha256": request_sha,
                "input_v36_sha256": input_sha,
                "feedback_v36_sha256": feedback_sha,
                "phi_sha256": phi_sha,
                "source_host_identifier": host,
                "seq": seq,
            }
            receipt = {
                "schema": "noema.aux-live-feedback-receipt/v1",
                "mode": "identity_echo",
                "nonce": nonce,
                "created_utc": datetime.now(timezone.utc).isoformat(),
                "created_unix_ns": created_ns,
                "source_host_identifier": host,
                "request_sha256": request_sha,
                "read_set_sha256": read_set_sha,
                "input_v36_sha256": input_sha,
                "feedback_v36_sha256": feedback_sha,
                "phi_sha256": phi_sha,
                "transport_receipt_sha256": sha256(canonical_bytes(transport)),
                "aux_result_status": "PASS",
                "lossless_identity": input_sha == feedback_sha,
                "surface_tick": int(np.asarray(surface["tick"])[0]),
                "surface_coherence": coherence,
                "aux_producer_pid": int(aux_status["pid"]),
                "aux_producer_heartbeat_age_s": aux_age,
                "runtime_pid": os.getpid(),
                "runtime_init_mode": init_mode,
                "seq": seq,
            }
            receipt["receipt_sha256"] = sha256(canonical_bytes(receipt))
            atomic_write(receipt_path, (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode())
            atomic_write(persistent / "receipts/tether_latest.json", receipt_path.read_bytes())
            status = {
                "schema": "noema.tether-runtime-status/v1",
                "status": "ACTIVE",
                "pid": os.getpid(),
                "heartbeat_ns": time.time_ns(),
                "seq": seq,
                "phi_sha256": phi_sha,
                "aux_phi_sha256": input_sha,
                "aux_feedback_phi_sha256": feedback_sha,
                "receipt_sha256": receipt["receipt_sha256"],
                "socket": args.socket,
            }
            atomic_write(status_path, (json.dumps(status, indent=2, sort_keys=True) + "\n").encode())
            atomic_write(binding_path, b"ACTIVE\n")
            if time.monotonic() - last_persist >= 1.0:
                save_npy_atomic(phi_store, np.asarray(surface["phi"], dtype=np.float64))
                last_persist = time.monotonic()
            seq += 1
        except Exception as exc:
            status = {
                "schema": "noema.tether-runtime-status/v1",
                "status": "BLOCKED",
                "pid": os.getpid(),
                "heartbeat_ns": time.time_ns(),
                "seq": seq,
                "error": f"{type(exc).__name__}:{exc}",
            }
            atomic_write(status_path, (json.dumps(status, indent=2, sort_keys=True) + "\n").encode())
            atomic_write(binding_path, b"BLOCKED\n")
        time.sleep(args.interval)


if __name__ == "__main__":
    raise SystemExit(main())
