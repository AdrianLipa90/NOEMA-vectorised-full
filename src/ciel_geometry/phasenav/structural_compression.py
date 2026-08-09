"""Auditable structural compression for NOEMA trajectory history.

This is deliberately not free-text summarization. Exact-equivalent trace events
may be represented by one kernel entry plus a reconstruction map, while debt,
pinned events, lineage and provenance remain explicit.

Compression is conservative: events are merged only when every structural
field except `event_id` is identical. Event identifiers must be unique because
they are the lossless reconstruction keys.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field, replace
from typing import Any, Mapping, Sequence

SCHEMA = "NOEMA_STRUCTURAL_COMPRESSION_V1"


@dataclass(frozen=True)
class TraceEvent:
    event_id: str
    kind: str
    status: str
    operation_id: str | None = None
    receipt_id: str | None = None
    debt_id: str | None = None
    parent_ids: tuple[str, ...] = ()
    provenance: tuple[str, ...] = ()
    payload: Mapping[str, Any] = field(default_factory=dict)
    pinned: bool = False


@dataclass(frozen=True)
class CompressionEntry:
    fingerprint: str
    representative: TraceEvent
    member_ids: tuple[str, ...]

    @property
    def multiplicity(self) -> int:
        return len(self.member_ids)


@dataclass(frozen=True)
class CompressedTrace:
    schema: str
    original_event_count: int
    kernel: tuple[CompressionEntry, ...]
    reconstruction_map: Mapping[str, str]
    provenance: tuple[str, ...]
    debt_ids: tuple[str, ...]
    verified_reconstructible: bool

    @property
    def kernel_event_count(self) -> int:
        return len(self.kernel)

    @property
    def compression_ratio(self) -> float:
        if self.original_event_count <= 0:
            return 1.0
        return self.kernel_event_count / self.original_event_count


def _canonical_structural_payload(event: TraceEvent) -> dict[str, Any]:
    data = asdict(event)
    data.pop("event_id", None)
    return data


def structural_fingerprint(event: TraceEvent) -> str:
    raw = json.dumps(
        _canonical_structural_payload(event),
        ensure_ascii=False,
        sort_keys=True,
        default=str,
        separators=(",", ":"),
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def reconstruct_trace(compressed: CompressedTrace) -> tuple[TraceEvent, ...]:
    """Reconstruct normalized events in original insertion order."""

    representatives = {entry.fingerprint: entry.representative for entry in compressed.kernel}
    events: list[TraceEvent] = []
    for event_id, fingerprint in compressed.reconstruction_map.items():
        representative = representatives[fingerprint]
        events.append(replace(representative, event_id=event_id))
    return tuple(events)


def _normalized(events: Sequence[TraceEvent]) -> tuple[dict[str, Any], ...]:
    return tuple(asdict(event) for event in events)


def compress_trace(events: Sequence[TraceEvent]) -> CompressedTrace:
    """Conservatively compact exact-equivalent structural events."""

    originals = tuple(events)
    groups: dict[str, list[TraceEvent]] = {}
    ordered_fingerprints: list[str] = []
    reconstruction: dict[str, str] = {}
    provenance: list[str] = []
    debts: list[str] = []

    for event in originals:
        if not event.event_id:
            raise ValueError("every trace event requires event_id")
        if event.event_id in reconstruction:
            raise ValueError(f"duplicate trace event_id: {event.event_id}")

        # Pinned and debt events must never coalesce. Add identity to the
        # grouping key while retaining exact reconstructibility.
        structural = structural_fingerprint(event)
        grouping = f"{structural}:{event.event_id}" if event.pinned or event.debt_id else structural
        fingerprint = hashlib.sha256(grouping.encode("utf-8")).hexdigest() if grouping != structural else structural
        if fingerprint not in groups:
            groups[fingerprint] = []
            ordered_fingerprints.append(fingerprint)
        groups[fingerprint].append(event)
        reconstruction[event.event_id] = fingerprint
        provenance.extend(event.provenance)
        if event.debt_id:
            debts.append(event.debt_id)

    kernel = tuple(
        CompressionEntry(
            fingerprint=fingerprint,
            representative=groups[fingerprint][0],
            member_ids=tuple(event.event_id for event in groups[fingerprint]),
        )
        for fingerprint in ordered_fingerprints
    )

    provisional = CompressedTrace(
        schema=SCHEMA,
        original_event_count=len(originals),
        kernel=kernel,
        reconstruction_map=reconstruction,
        provenance=tuple(dict.fromkeys(provenance)),
        debt_ids=tuple(dict.fromkeys(debts)),
        verified_reconstructible=False,
    )
    reconstructed = reconstruct_trace(provisional)
    verified = _normalized(reconstructed) == _normalized(originals)
    return replace(provisional, verified_reconstructible=verified)


__all__ = [
    "SCHEMA",
    "TraceEvent",
    "CompressionEntry",
    "CompressedTrace",
    "structural_fingerprint",
    "compress_trace",
    "reconstruct_trace",
]
