#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import socket
import struct
import tempfile
import time
from pathlib import Path

N = 36
BYTES = N * 8
SCHEMA = "noema.aux-feedback-receipt/v1"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stable_json(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    tmp = Path(name)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.chmod(tmp, 0o600)
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def read_v36(path: Path) -> bytes:
    if not path.is_file():
        raise FileNotFoundError(str(path))
    raw = path.read_bytes()
    if len(raw) != BYTES:
        raise ValueError(f"{path}:size:{len(raw)}!=288")
    values = struct.unpack("<36d", raw)
    if not all(math.isfinite(x) for x in values):
        raise ValueError(f"{path}:non_finite")
    return raw


def publish_once(root: Path) -> dict[str, object]:
    phi_path = root / "phi"
    aux_path = root / "aux_phi"
    feedback_path = root / "aux_feedback_phi"
    receipt_path = root / "receipts" / "aux_feedback_latest.json"

    # Strict continuity: missing AUX is a blocker. Never seed or synthesize it.
    phi_raw = read_v36(phi_path)
    aux_raw = read_v36(aux_path)

    phi_sha = sha256_bytes(phi_raw)
    aux_sha = sha256_bytes(aux_raw)
    nonce = os.urandom(16).hex()
    created_ns = time.time_ns()
    read_set = stable_json({"phi_sha256": phi_sha, "aux_phi_sha256": aux_sha})
    read_set_sha = sha256_bytes(read_set)
    request_sha = sha256_bytes(stable_json({"nonce": nonce, "read_set_sha256": read_set_sha, "created_ns": created_ns}))

    # Raw feedback is a transport lane only: no residual, dither, smoothing or embedding.
    atomic_write(feedback_path, phi_raw)
    feedback_raw = feedback_path.read_bytes()
    feedback_sha = sha256_bytes(feedback_raw)
    if feedback_raw != phi_raw:
        raise RuntimeError("feedback_not_bitwise_equal_to_phi")

    body: dict[str, object] = {
        "schema": SCHEMA,
        "created_unix_ns": created_ns,
        "nonce": nonce,
        "source_host_identifier": socket.gethostname(),
        "request_sha256": request_sha,
        "read_set_sha256": read_set_sha,
        "input_v36_sha256": phi_sha,
        "aux_input_v36_sha256": aux_sha,
        "feedback_v36_sha256": feedback_sha,
        "lossless_identity": True,
        "aux_result_status": "PASS_TRANSPORT_FEEDBACK",
        "feedback_path": str(feedback_path),
        "aux_phi_overwritten": False,
    }
    transport_sha = sha256_bytes(stable_json(body))
    body["transport_receipt_sha256"] = transport_sha
    atomic_write(receipt_path, stable_json(body))
    return body


def main() -> int:
    ap = argparse.ArgumentParser(description="NOEMA lossless AUX feedback lane")
    ap.add_argument("--root", default="/dev/shm/ciel_noema")
    ap.add_argument("--watch", action="store_true")
    ap.add_argument("--interval", type=float, default=0.25)
    args = ap.parse_args()
    root = Path(args.root)
    if args.interval <= 0:
        raise SystemExit("interval must be positive")
    while True:
        try:
            out = publish_once(root)
            print(json.dumps(out, sort_keys=True, ensure_ascii=False))
        except Exception as exc:
            print(json.dumps({"schema": SCHEMA, "status": "BLOCKED", "error": f"{type(exc).__name__}:{exc}"}, sort_keys=True, ensure_ascii=False))
            if not args.watch:
                return 23
        if not args.watch:
            return 0
        time.sleep(args.interval)


if __name__ == "__main__":
    raise SystemExit(main())
