#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import os
import socket
import struct
import sys
from pathlib import Path

N = 36
BYTES = N * 8


def check_f64_vector(path: Path) -> tuple[bool, str]:
    if not path.is_file():
        return False, f"MISSING:{path}"
    data = path.read_bytes()
    if len(data) != BYTES:
        return False, f"BAD_SIZE:{path}:{len(data)}!=288"
    vals = struct.unpack("<36d", data)
    if not all(math.isfinite(x) for x in vals):
        return False, f"NONFINITE:{path}"
    return True, "PASS"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="/dev/shm/ciel_noema")
    ap.add_argument("--socket", default="/run/user/1000/noema/ciel_headless.sock")
    ap.add_argument("--require-socket", action="store_true")
    args = ap.parse_args()

    root = Path(args.root)
    failures: list[str] = []

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
        ok, detail = check_f64_vector(root / name)
        if not ok:
            failures.append(detail)

    for rel in ("session/startpoint.json", "session/system_message.txt"):
        p = root / rel
        if not p.is_file():
            failures.append(f"MISSING:{p}")

    sock_path = Path(args.socket)
    if args.require_socket:
        try:
            mode = sock_path.stat().st_mode
            if not sock_path.exists() or not socket.S_ISSOCK(mode):
                failures.append(f"NOT_UNIX_SOCKET:{sock_path}")
        except FileNotFoundError:
            failures.append(f"MISSING_SOCKET:{sock_path}")
        except AttributeError:
            import stat
            try:
                if not stat.S_ISSOCK(sock_path.stat().st_mode):
                    failures.append(f"NOT_UNIX_SOCKET:{sock_path}")
            except FileNotFoundError:
                failures.append(f"MISSING_SOCKET:{sock_path}")

    status = {
        "schema": "noema.aux-tether-guard/v1",
        "root": str(root),
        "tether_status": "ACTIVE" if not failures else "BLOCKED",
        "failures": failures,
        "fail_closed": True,
    }
    print(json.dumps(status, sort_keys=True, ensure_ascii=False))
    return 0 if not failures else 23


if __name__ == "__main__":
    raise SystemExit(main())
