from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ciel_geometry.phasenav.structural_compression import TraceEvent, compress_trace, reconstruct_trace


def test_exact_equivalent_events_compress_and_reconstruct():
    events = [
        TraceEvent(event_id="e1", kind="gate", status="HOLD", provenance=("p1",), payload={"x": 1}),
        TraceEvent(event_id="e2", kind="gate", status="HOLD", provenance=("p1",), payload={"x": 1}),
        TraceEvent(event_id="e3", kind="return", status="PASS", provenance=("p2",), payload={"x": 2}),
    ]
    compressed = compress_trace(events)
    assert compressed.original_event_count == 3
    assert compressed.kernel_event_count == 2
    assert compressed.compression_ratio == 2 / 3
    assert compressed.verified_reconstructible is True
    assert reconstruct_trace(compressed) == tuple(events)
    assert compressed.provenance == ("p1", "p2")


def test_debt_events_are_never_coalesced():
    events = [
        TraceEvent(event_id="d1", kind="debt", status="DEBT", debt_id="debt:x", payload={"reason": "x"}),
        TraceEvent(event_id="d2", kind="debt", status="DEBT", debt_id="debt:x", payload={"reason": "x"}),
    ]
    compressed = compress_trace(events)
    assert compressed.kernel_event_count == 2
    assert compressed.debt_ids == ("debt:x",)
    assert compressed.verified_reconstructible is True


def test_pinned_events_are_never_coalesced():
    events = [
        TraceEvent(event_id="p1", kind="receipt", status="PASS", payload={"same": True}, pinned=True),
        TraceEvent(event_id="p2", kind="receipt", status="PASS", payload={"same": True}, pinned=True),
    ]
    compressed = compress_trace(events)
    assert compressed.kernel_event_count == 2


def test_different_lineage_does_not_compress():
    events = [
        TraceEvent(event_id="e1", kind="memory", status="PASS", parent_ids=("a",)),
        TraceEvent(event_id="e2", kind="memory", status="PASS", parent_ids=("b",)),
    ]
    compressed = compress_trace(events)
    assert compressed.kernel_event_count == 2


def test_duplicate_event_id_is_rejected_before_reconstruction_map_can_collapse():
    events = [
        TraceEvent(event_id="dup", kind="gate", status="HOLD"),
        TraceEvent(event_id="dup", kind="return", status="PASS"),
    ]
    with pytest.raises(ValueError, match="duplicate trace event_id"):
        compress_trace(events)
