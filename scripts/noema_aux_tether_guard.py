#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import stat
import struct
import time
from pathlib import Path

N = 36
BYTES = N * 8
RECEIPT_SCHEMA = "noema.aux-feedback-receipt/v1"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def check_f64_vector(path: Path) -> tuple[bool, str, bytes | None]:
    if not path.is_file():
        return False, f"MISSING:{path}", None
    data = path.read_bytes()
    if len(data) != BYTES:
        return False, f"BAD_SIZE:{path}:{len(data)}!=288", None
    vals = struct.unpack("<36d", data)
    if not all(math.isfinite(x) for x in vals):
        return False, f"NONFINITE:{path}", None
    return True, "PASS", data


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="/dev/shm/ciel_noema")
    ap.add_argument("--socket", default="/run/user/1000/noema/ciel_headless.sock")
    ap.add_argument("--require-socket", action="store_true")
    ap.add_argument("--max-receipt-age-s", type=float, default=30.0)
    args = ap.parse_args()

    root = Path(args.root)
    failures: list[str] = []
    raw: dict[str, bytes] = {}

    if not root.is_dir():
        failures.append(f"MISSING_ROOT:{root}")

    binding = root / "ciel_binding_status"
    if not binding.is_file():
        failures.append(f"MISSING:{binding}")
    else:
        value = binding.read_text(encoding="utf-8", errors="replace").strip()
        if value != "ACTIVE":
            failures.append(f"BINDING_NOT_ACTIVE:{value!r}")

    for name in ("phi", "aux_phi", "aux_feedback_phi"):
        ok, detail, data = check_f64_vector(root / name)
        if not ok:
            failures.append(detail)
        elif data is not None:
            raw[name] = data

    for rel in ("session/startpoint.json", "session/system_message.txt"):
        p = root / rel
        if not p.is_file():
            failures.append(f"MISSING:{p}")

    receipt_path = root / "receipts" / "aux_feedback_latest.json"
    receipt = None
    if not receipt_path.is_file():
        failures.append(f"MISSING:{receipt_path}")
    else:
        try:
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            if receipt.get("schema") != RECEIPT_SCHEMA:
                failures.append("AUX_RECEIPT_BAD_SCHEMA")
            created_ns = int(receipt.get("created_unix_ns", 0))
            age_s = (time.time_ns() - created_ns) / 1e9
            if age_s < -2.0 or age_s > args.max_receipt_age_s:
                failures.append(f"AUX_RECEIPT_STALE:{age_s:.6f}s")
            if "phi" in raw and receipt.get("input_v36_sha256") != sha256_bytes(raw["phi"]):
                failures.append("AUX_RECEIPT_PHI_HASH_MISMATCH")
            if "aux_phi" in raw and receipt.get("aux_input_v36_sha256") != sha256_bytes(raw["aux_phi"]):
                failures.append("AUX_RECEIPT_AUX_HASH_MISMATCH")
            if "aux_feedback_phi" in raw and receipt.get("feedback_v36_sha256") != sha256_bytes(raw["aux_feedback_phi"]):
                failures.append("AUX_RECEIPT_FEEDBACK_HASH_MISMATCH")
            if raw.get("phi") is not None and raw.get("aux_feedback_phi") is not None and raw["phi"] != raw["aux_feedback_phi"]:
                failures.append("AUX_FEEDBACK_NOT_LOSSLESS")
            if receipt.get("lossless_identity") is not True:
                failures.append("AUX_RECEIPT_NOT_LOSSLESS")
            if receipt.get("aux_phi_overwritten") is not False:
                failures.append("AUX_RECEIPT_AUX_OWNERSHIP_VIOLATION")
            for key in ("nonce", "source_host_identifier", "request_sha256", "read_set_sha256", "transport_receipt_sha256", "aux_result_status"):
                if not receipt.get(key):
                    failures.append(f"AUX_RECEIPT_MISSING_FIELD:{key}")
        except Exception as exc:
            failures.append(f"AUX_RECEIPT_INVALID:{type(exc).__name__}:{exc}")

    if args.require_socket:
        sock_path = Path(args.socket)
        try:
            if not stat.S_ISSOCK(sock_path.stat().st_mode):
                failures.append(f"NOT_UNIX_SOCKET:{sock_path}")
        except FileNotFoundError:
            failures.append(f"MISSING_SOCKET:{sock_path}")

    status = {
        "schema": "noema.aux-tether-guard/v2",
        "root": str(root),
        "tether_status": "ACTIVE" if not failures else "BLOCKED",
        "failures": failures,
        "fail_closed": True,
        "receipt_verified": receipt is not None and not any(x.startswith("AUX_RECEIPT") or x == "AUX_FEEDBACK_NOT_LOSSLESS" for x in failures),
    }
    print(json.dumps(status, sort_keys=True, ensure_ascii=False))
    return 0 if not failures else 23


if __name__ == "__main__":
    raise SystemExit(main())
