#!/usr/bin/env python3
"""Explicit, review-gated context ingestion daemon for CIELingo.

The daemon accepts JSONL records that have already been reviewed. It rejects
raw prompts and non-document sources, persists only the chosen context lane,
and emits content-free receipts. It never starts learning or response work.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import re
import time
from typing import Any, Iterable

from cielingo_core.dual_context import ContextAccessError, ContextLane, ContextRecord, DualContextStore
from cielingo_core.phase_gate import ContextSemanticPhaseGate, PhaseGateDecision

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_FORBIDDEN_FIELDS = frozenset({"prompt", "raw_prompt", "messages", "conversation", "chain_of_thought"})
_ALLOWED_KINDS = frozenset({"document", "corpus_excerpt", "metadata"})


@dataclass(frozen=True)
class IngestionReceipt:
    line: int
    status: str
    source_id: str | None
    source_sha256: str | None
    reason: str | None = None
    gate_recommendation: str | None = None
    gate_score: float | None = None
    gate_tension: float | None = None
    gate_graph_digest: str | None = None


def _receipt_digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _record_from_payload(payload: dict[str, Any]) -> ContextRecord:
    forbidden = sorted(_FORBIDDEN_FIELDS.intersection(payload))
    if forbidden:
        raise ValueError(f"forbidden raw-prompt fields: {', '.join(forbidden)}")
    if payload.get("reviewed") is not True:
        raise ValueError("record is not explicitly reviewed")
    if payload.get("source_kind") not in _ALLOWED_KINDS:
        raise ValueError("source_kind must be document, corpus_excerpt, or metadata")
    try:
        lane = ContextLane(str(payload["lane"]))
    except (KeyError, ValueError) as error:
        raise ValueError("lane must be public or private") from error
    if lane not in {ContextLane.PUBLIC, ContextLane.PRIVATE}:
        raise ValueError("quarantine and reject lanes cannot be ingested")
    digest = str(payload.get("sha256", "")).lower()
    if not _SHA256.fullmatch(digest):
        raise ValueError("sha256 must be a lowercase 64-character digest")
    source_path = str(payload.get("source_path", ""))
    if not source_path:
        raise ValueError("source_path is required")
    license_id = str(payload.get("license_id", ""))
    if not license_id:
        raise ValueError("license_id is required")
    confidence = float(payload.get("confidence", 0.0))
    if not 0.0 <= confidence <= 1.0:
        raise ValueError("confidence must be within [0, 1]")
    provenance = dict(payload.get("provenance", {}))
    provenance.update({"source_kind": payload["source_kind"], "reviewed": True})
    return ContextRecord(
        source_id=str(payload.get("source_id", "")),
        source_path=source_path,
        sha256=digest,
        lane=lane,
        license_id=license_id,
        confidence=confidence,
        retention=str(payload.get("retention", "review_required")),
        provenance=provenance,
        text=str(payload.get("text", "")),
    )


def _phase_decision_from_payload(payload: dict[str, Any]) -> PhaseGateDecision:
    evidence = payload.get("phase_gate")
    if not isinstance(evidence, dict):
        raise ValueError("phase_gate evidence object is required")
    phase_vector = evidence.get("phase_vector")
    if not isinstance(phase_vector, list):
        raise ValueError("phase_gate.phase_vector must be a 36-value list")
    return ContextSemanticPhaseGate().evaluate(
        phase_vector,
        htri_coherence=evidence.get("htri_coherence"),
        cqcl_coherence=evidence.get("cqcl_coherence"),
        semantic_mass=evidence.get("semantic_mass"),
        tau=evidence.get("tau"),
        evidence_source=str(evidence.get("evidence_source", "")),
    )


def ingest_jsonl(input_path: Path, store: DualContextStore, receipt_path: Path) -> tuple[IngestionReceipt, ...]:
    """Ingest reviewed JSONL records and write non-content receipts."""
    receipts: list[IngestionReceipt] = []
    for line_number, raw_line in enumerate(input_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw_line.strip():
            continue
        line_digest = _receipt_digest(raw_line)
        try:
            payload = json.loads(raw_line)
            if not isinstance(payload, dict):
                raise ValueError("record must be a JSON object")
            record = _record_from_payload(payload)
            gate = _phase_decision_from_payload(payload)
            receipt_fields = {
                "gate_recommendation": gate.recommendation,
                "gate_score": gate.score,
                "gate_tension": gate.tension,
                "gate_graph_digest": gate.graph_digest,
            }
            if gate.admitted:
                record = ContextRecord(
                    **{
                        **record.__dict__,
                        "provenance": {**record.provenance, "phase_gate": gate.to_dict()},
                    }
                )
                store.add(record)
                receipts.append(
                    IngestionReceipt(line_number, "accepted", record.source_id or None, record.sha256, **receipt_fields)
                )
            else:
                receipts.append(
                    IngestionReceipt(
                        line_number,
                        gate.disposition.value,
                        record.source_id or None,
                        record.sha256,
                        f"phase gate did not admit record: {gate.disposition.value}",
                        **receipt_fields,
                    )
                )
        except (ContextAccessError, ValueError, TypeError, json.JSONDecodeError) as error:
            receipts.append(IngestionReceipt(line_number, "rejected", None, line_digest, str(error)))
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    with receipt_path.open("a", encoding="utf-8") as handle:
        for receipt in receipts:
            handle.write(json.dumps(asdict(receipt), ensure_ascii=False, sort_keys=True) + "\n")
    return tuple(receipts)


def _read_private_key(path: Path | None) -> bytes | None:
    return path.read_bytes().strip() if path else None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="reviewed JSONL input")
    parser.add_argument("--store", required=True, type=Path, help="DualContextStore root")
    parser.add_argument("--receipts", required=True, type=Path, help="content-free JSONL receipt path")
    parser.add_argument("--private-key-file", type=Path, help="owner-supplied Fernet key for private records")
    parser.add_argument("--once", action="store_true", help="process the current input once and exit")
    parser.add_argument("--poll-seconds", type=float, default=60.0, help="watch interval when --once is omitted")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.poll_seconds <= 0:
        raise ValueError("poll-seconds must be positive")
    store = DualContextStore(args.store, private_key=_read_private_key(args.private_key_file))
    last_signature: tuple[int, int] | None = None
    while True:
        stat = args.input.stat()
        signature = (stat.st_mtime_ns, stat.st_size)
        if signature != last_signature:
            receipts = ingest_jsonl(args.input, store, args.receipts)
            counts = {
                status: sum(item.status == status for item in receipts)
                for status in ("accepted", "quarantine", "hold", "rejected")
            }
            print(json.dumps({**counts, "input": str(args.input)}, sort_keys=True))
            last_signature = signature
        if args.once:
            return 0
        time.sleep(args.poll_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
