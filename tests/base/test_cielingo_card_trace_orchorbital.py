from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from cielingo.card_trace_eeg import create_card_trace_snap, snap_similarity
from cielingo.semantic_collatz import route_summary, semantic_collatz_route, semantic_seed
from cielingo.orchorbital_router import route_orchorbital


def test_card_trace_snap_is_deterministic_and_bounded() -> None:
    cards = ["smell:rain", "name:adrian", "place:lab", "sound:hum"]
    a = create_card_trace_snap(cards, context_key="ctx", identity_anchor="id")
    b = create_card_trace_snap(cards, context_key="ctx", identity_anchor="id")
    assert a.layout_hash == b.layout_hash
    assert a.snap_id == b.snap_id
    assert a.nonlocal_claim_allowed is False
    assert a.primary_noema_runtime_available is False
    assert len(a.active_traces) == len(cards)
    for trace in a.active_traces:
        assert 0.0 <= trace["amplitude"] <= 1.0
        assert 0.0 <= trace["semantic_mass"] <= 1.0
        assert "coupled_to" in trace


def test_snap_similarity_detects_related_memory_cluster() -> None:
    cards = ["smell:rain", "name:adrian", "place:lab", "sound:hum"]
    current = create_card_trace_snap(cards, context_key="ctx", identity_anchor="id")
    memory = create_card_trace_snap(cards, context_key="ctx", identity_anchor="id")
    distant = create_card_trace_snap(["taste:sweet", "place:garden"], context_key="other", identity_anchor="id")
    assert snap_similarity(current, memory)["score"] > snap_similarity(current, distant)["score"]


def test_semantic_collatz_route_has_reduce_or_expand_modes() -> None:
    seed = semantic_seed("abc")
    route = semantic_collatz_route(seed, max_steps=16)
    summary = route_summary(route)
    assert summary["steps"] <= 16
    assert summary["reduce_count"] + summary["expand_count"] == summary["steps"]
    assert summary["dominant_mode"] in {"reduce", "expand"}


def test_orchorbital_router_associates_matching_memory() -> None:
    cards = ["smell:rain", "name:adrian", "place:lab", "sound:hum"]
    current = create_card_trace_snap(cards, context_key="ctx", identity_anchor="id")
    memory = create_card_trace_snap(cards, context_key="ctx", identity_anchor="id")
    decision = route_orchorbital(current, [memory])
    assert decision.decision == "associate_memory_snap"
    assert decision.selected_memory_snap_id == memory.snap_id
    assert decision.nonlocal_claim_allowed is False
    assert decision.not_biological_orchor_claim is True


def test_card_trace_orchorbital_cli_writes_report() -> None:
    cmd = [sys.executable, "scripts/cielingo_card_trace_orchorbital.py", "--write"]
    proc = subprocess.run(cmd, cwd=Path.cwd(), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    assert proc.returncode == 0, proc.stderr + proc.stdout[-1000:]
    report = json.loads(proc.stdout)
    assert report["decision"]["operator"] == "ORCHORBITAL_CARD_TRACE_ROUTER"
    assert report["execution_layer"] == "fallback_cpu_ram"
