from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .memory import utc_now_iso
from .schema import ImmuneDecisionRecord


def _stable_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def record_hash(payload: dict[str, Any]) -> str:
    clean = {k: v for k, v in payload.items() if k != "record_hash"}
    return hashlib.sha256(_stable_json(clean).encode("utf-8")).hexdigest()


def _last_hash(path: Path) -> str | None:
    if not path.exists() or path.stat().st_size == 0:
        return None
    last = None
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                last = json.loads(line)
    if not last:
        return None
    return last.get("record_hash")


def append_audit(path: str | Path, record: ImmuneDecisionRecord) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "pn-bis-audit-v0.2",
        "created_at_utc": utc_now_iso(),
        "previous_record_hash": _last_hash(p),
        **record.to_dict(),
    }
    payload["record_hash"] = record_hash(payload)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, sort_keys=True) + "\n")


def verify_audit_chain(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    previous = None
    count = 0
    errors: list[str] = []
    if not p.exists():
        return {"ok": False, "records": 0, "errors": ["audit file does not exist"]}
    with p.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            if not line.strip():
                continue
            count += 1
            payload = json.loads(line)
            if payload.get("previous_record_hash") != previous:
                errors.append(f"line {lineno}: previous_record_hash mismatch")
            expected = record_hash(payload)
            if payload.get("record_hash") != expected:
                errors.append(f"line {lineno}: record_hash mismatch")
            previous = payload.get("record_hash")
    return {"ok": not errors, "records": count, "head_record_hash": previous, "errors": errors}
