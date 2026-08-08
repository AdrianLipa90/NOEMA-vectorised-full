#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import socket
import stat
import struct
import time

N = 36
BYTES = N * 8


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def valid_vector(path: Path) -> tuple[bool, str]:
    if not path.is_file():
        return False, "MISSING"
    raw = path.read_bytes()
    if len(raw) != BYTES:
        return False, f"BAD_SIZE:{len(raw)}"
    try:
        values = struct.unpack("<36d", raw)
    except struct.error as exc:
        return False, f"BAD_STRUCT:{exc}"
    if not all(math.isfinite(value) for value in values):
        return False, "NONFINITE"
    return True, "PASS"


def process_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="/dev/shm/ciel_noema")
    ap.add_argument("--socket", default="/run/user/1000/noema/ciel_headless.sock")
    ap.add_argument("--max-age", type=float, default=2.0)
    args = ap.parse_args()

    root = Path(args.root)
    failures: list[str] = []

    for name in ("phi", "aux_phi", "aux_feedback_phi"):
        ok, detail = valid_vector(root / name)
        if not ok:
            failures.append(f"{name}:{detail}")

    receipt_path = root / "receipts/tether_latest.json"
    receipt: dict[str, object] | None = None
    if not receipt_path.is_file():
        failures.append("MISSING:tether_latest_receipt")
    else:
        try:
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"INVALID_RECEIPT:{exc}")

    if receipt is not None:
        age = (time.time_ns() - int(receipt.get("created_unix_ns", 0))) / 1e9
        if age < 0 or age > args.max_age:
            failures.append(f"STALE_RECEIPT:{age:.6f}s")
        if receipt.get("mode") != "identity_echo":
            failures.append("MODE_NOT_IDENTITY_ECHO")
        if receipt.get("aux_result_status") != "PASS":
            failures.append("AUX_RESULT_NOT_PASS")

        input_sha = sha256((root / "aux_phi").read_bytes()) if (root / "aux_phi").is_file() else None
        feedback_sha = sha256((root / "aux_feedback_phi").read_bytes()) if (root / "aux_feedback_phi").is_file() else None
        phi_sha = sha256((root / "phi").read_bytes()) if (root / "phi").is_file() else None
        if input_sha != feedback_sha:
            failures.append("RAW_FEEDBACK_NOT_LOSSLESS")
        if receipt.get("input_v36_sha256") != input_sha:
            failures.append("INPUT_SHA_RECEIPT_MISMATCH")
        if receipt.get("feedback_v36_sha256") != feedback_sha:
            failures.append("FEEDBACK_SHA_RECEIPT_MISMATCH")
        if receipt.get("phi_sha256") != phi_sha:
            failures.append("PHI_SHA_RECEIPT_MISMATCH")
        if not receipt.get("nonce"):
            failures.append("MISSING_NONCE")
        for key in (
            "request_sha256",
            "read_set_sha256",
            "transport_receipt_sha256",
            "receipt_sha256",
            "source_host_identifier",
        ):
            if not receipt.get(key):
                failures.append(f"MISSING_RECEIPT_FIELD:{key}")
        if not process_alive(int(receipt.get("runtime_pid", -1))):
            failures.append("TETHER_RUNTIME_PID_NOT_ALIVE")

    aux_status_path = root / "aux_stream_status.json"
    if not aux_status_path.is_file():
        failures.append("MISSING:AUX_HEARTBEAT")
    else:
        try:
            aux_status = json.loads(aux_status_path.read_text(encoding="utf-8"))
            age = (time.time_ns() - int(aux_status.get("heartbeat_ns", 0))) / 1e9
            if aux_status.get("status") != "ACTIVE":
                failures.append("AUX_PRODUCER_NOT_ACTIVE")
            if age < 0 or age > args.max_age:
                failures.append(f"AUX_HEARTBEAT_STALE:{age:.6f}s")
            if not process_alive(int(aux_status.get("pid", -1))):
                failures.append("AUX_PID_NOT_ALIVE")
        except Exception as exc:
            failures.append(f"INVALID_AUX_HEARTBEAT:{exc}")

    socket_path = Path(args.socket)
    try:
        if not stat.S_ISSOCK(socket_path.stat().st_mode):
            failures.append("HEADLESS_ENDPOINT_NOT_SOCKET")
        else:
            client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            client.settimeout(0.5)
            client.connect(str(socket_path))
            raw = client.recv(65536)
            client.close()
            if not raw:
                failures.append("HEADLESS_SOCKET_EMPTY")
    except Exception as exc:
        failures.append(f"HEADLESS_SOCKET_FAIL:{type(exc).__name__}:{exc}")

    startpoint_path = root / "session/startpoint.json"
    if not startpoint_path.is_file():
        failures.append("MISSING:STARTPOINT")
    else:
        try:
            startpoint = json.loads(startpoint_path.read_text(encoding="utf-8"))
            if startpoint.get("status") != "VERIFIED":
                failures.append(f"STARTPOINT_NOT_VERIFIED:{startpoint.get('status')}")
            if not startpoint.get("current_task"):
                failures.append("STARTPOINT_MISSING_CURRENT_TASK")
            if not startpoint.get("active_path"):
                failures.append("STARTPOINT_MISSING_ACTIVE_PATH")
        except Exception as exc:
            failures.append(f"INVALID_STARTPOINT:{exc}")

    result = {
        "schema": "noema.aux-tether-receipt-guard/v2",
        "tether_status": "ACTIVE" if not failures else "BLOCKED",
        "fail_closed": True,
        "failures": failures,
        "fresh_receipt": receipt,
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if not failures else 24


if __name__ == "__main__":
    raise SystemExit(main())
