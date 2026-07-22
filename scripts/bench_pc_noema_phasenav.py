#!/usr/bin/env python3
"""Benchmark: PC host vs NOEMA shm vs NOEMA+PhaseNav.

Measures:
  1. PC — czysty Python, phasenav_enrich() throughput
  2. NOEMA — read/write /dev/shm/ciel_noema/ surface
  3. NOEMA+PhaseNav — PhaseNav enrichment z użyciem JSONL z shm
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

NOEMA_ROOT = Path("/dev/shm/ciel_noema")

# ── Synthetic card IDs ─────────────────────────────────────────────────────
N_CARDS = 10000
CARD_IDS = [f"bench:{i}:{hash(str(i))}" for i in range(N_CARDS)]
CARD_NAMES = [f"card_{i}" for i in range(N_CARDS)]


def bench_pc() -> dict[str, Any]:
    """PhaseNav enrichment w czystym Pythonie — bez I/O."""
    from ciel_geometry.phasenav.enrichment import phasenav_enrich

    # Ogrzewanie
    _ = phasenav_enrich("warmup", "warmup")

    t0 = time.perf_counter_ns()
    results = []
    for cid, name in zip(CARD_IDS, CARD_NAMES, strict=True):
        results.append(phasenav_enrich(cid, name))
    dt_ns = time.perf_counter_ns() - t0
    total = len(results)
    return {
        "total_cards": total,
        "time_s": round(dt_ns / 1e9, 6),
        "cards_per_sec": round(total / (dt_ns / 1e9), 1),
        "us_per_card": round(dt_ns / total / 1000, 3),
    }


def bench_noema_read() -> dict[str, Any]:
    """NOEMA: odczyt powierzchni (phi, g, omega) z /dev/shm."""
    if not NOEMA_ROOT.exists():
        return {"error": "NOEMA not available"}

    # Ogrzewanie
    _ = np.fromfile(NOEMA_ROOT / "phi", dtype=np.float64)
    _ = np.fromfile(NOEMA_ROOT / "g", dtype=np.float64)
    _ = np.fromfile(NOEMA_ROOT / "omega", dtype=np.float64)

    t0 = time.perf_counter_ns()
    for _ in range(1000):
        phi = np.fromfile(NOEMA_ROOT / "phi", dtype=np.float64)
        g = np.fromfile(NOEMA_ROOT / "g", dtype=np.float64)
        omega = np.fromfile(NOEMA_ROOT / "omega", dtype=np.float64)
    dt_ns = time.perf_counter_ns() - t0
    reads = 1000
    return {
        "reads": reads,
        "time_s": round(dt_ns / 1e9, 6),
        "reads_per_sec": round(reads / (dt_ns / 1e9), 1),
        "us_per_read": round(dt_ns / reads / 1000, 3),
        "phi_size_bytes": len(phi) * 8 if "phi" in dir() else 0,
        "g_size_bytes": len(g.flat) * 8 if "g" in dir() else 0,
    }


def bench_noema_write() -> dict[str, Any]:
    """NOEMA: zapis danych enrichment do shm (symulacja)."""
    if not NOEMA_ROOT.exists():
        return {"error": "NOEMA not available"}

    test_path = NOEMA_ROOT / ".bench_tmp"
    data = np.zeros(24, dtype=np.float64)

    t0 = time.perf_counter_ns()
    for _ in range(5000):
        data.tofile(test_path)
    dt_ns = time.perf_counter_ns() - t0
    writes = 5000
    test_path.unlink(missing_ok=True)
    return {
        "writes": writes,
        "time_s": round(dt_ns / 1e9, 6),
        "writes_per_sec": round(writes / (dt_ns / 1e9), 1),
        "us_per_write": round(dt_ns / writes / 1000, 3),
    }


def bench_noema_phasenav() -> dict[str, Any]:
    """NOEMA+PhaseNav: operator vectors z JSONL w shm."""
    jsonl_path = NOEMA_ROOT / "teleusing" / "CIELINGO_TELEUSING_OPERATOR_VECTORS.noema.jsonl"
    if not jsonl_path.exists():
        return {"error": "PhaseNav JSONL not found in NOEMA"}

    # Załaduj operatory z NOEMA
    ops: dict[str, list[float]] = {}
    for line in jsonl_path.read_text().strip().split("\n"):
        e = json.loads(line)
        ops[e["operator_hook"]] = e["orbit_vector"]

    op_ids = list(ops.keys())
    from ciel_geometry.phasenav.operator_algebra import ALL_OPERATOR_IDS, operator_signature
    from ciel_geometry.phasenav.enrichment import harmonic_imprint

    assert len(ops) == 33, f"Expected 33, got {len(ops)}"

    # Benchmark: read + harmonic imprint z NOEMA JSONL
    t0 = time.perf_counter_ns()
    for cid in CARD_IDS[:1000]:
        idx = abs(hash(cid)) % 33
        op_id = ALL_OPERATOR_IDS[idx]
        vec = ops[op_id] if op_id in ops else operator_signature(op_id)
        # harmonic imprint z wektora
        _ = harmonic_imprint(np.array(vec))
    dt_ns = time.perf_counter_ns() - t0
    n = 1000
    return {
        "total_calls": n,
        "time_s": round(dt_ns / 1e9, 6),
        "calls_per_sec": round(n / (dt_ns / 1e9), 1),
        "us_per_call": round(dt_ns / n / 1000, 3),
        "noema_jsonl_lines": len(ops),
    }


def main():
    print("=" * 60)
    print("BENCHMARK: PC vs NOEMA vs NOEMA+PhaseNav")
    print("=" * 60)

    results: dict[str, Any] = {}

    # 1. PC
    print(f"\n[1/3] PC — phasenav_enrich({N_CARDS} calls)...")
    r = bench_pc()
    results["pc"] = r
    print(f"      {r['cards_per_sec']} cards/s  ({r['us_per_card']} µs/card)")

    # 2. NOEMA
    print(f"\n[2/3] NOEMA — read/write /dev/shm/ciel_noema/...")
    r_read = bench_noema_read()
    results["noema_read"] = r_read
    if "error" not in r_read:
        print(f"      read:  {r_read['reads_per_sec']} rd/s  ({r_read['us_per_read']} µs/read)")
    else:
        print(f"      read:  {r_read['error']}")

    r_write = bench_noema_write()
    results["noema_write"] = r_write
    if "error" not in r_write:
        print(f"      write: {r_write['writes_per_sec']} wr/s  ({r_write['us_per_write']} µs/write)")
    else:
        print(f"      write: {r_write['error']}")

    # 3. NOEMA+PhaseNav
    print(f"\n[3/3] NOEMA+PhaseNav — operator algebra z shm...")
    r_pn = bench_noema_phasenav()
    results["noema_phasenav"] = r_pn
    if "error" not in r_pn:
        print(f"      {r_pn['calls_per_sec']} calls/s  ({r_pn['us_per_call']} µs/call)")
    else:
        print(f"      {r_pn['error']}")

    # ── Porównanie ─────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("PORÓWNANIE (µs na operację)")
    print("-" * 60)

    def _us(key: str) -> float:
        v = results.get(key, {})
        if "error" in v:
            return float("nan")
        return v.get("us_per_card") or v.get("us_per_read") or v.get("us_per_write") or v.get("us_per_call") or float("nan")

    pc_us = _us("pc")
    noema_r_us = _us("noema_read")
    noema_w_us = _us("noema_write")
    pn_us = _us("noema_phasenav")

    print(f"  PC PhaseNav:         {pc_us:>8.2f} µs/card")
    print(f"  NOEMA read surface:  {noema_r_us:>8.2f} µs/read")
    print(f"  NOEMA write vector:  {noema_w_us:>8.2f} µs/write")
    print(f"  NOEMA+PhaseNav:     {pn_us:>8.2f} µs/call")

    if pc_us and pn_us:
        ratio = pc_us / pn_us if pn_us else float("inf")
        print(f"\n  PC vs NOEMA+PN:      {ratio:.2f}×")
        print(f"  (im szybciej w PC, tym większy ratio)")

    print("\n  Podsumowanie:")
    print(f"  - PC:       {results.get('pc', {}).get('cards_per_sec', '?'):>8} cards/s")
    print(f"  - NOEMA R:  {results.get('noema_read', {}).get('reads_per_sec', '?'):>8} rd/s")
    print(f"  - NOEMA W:  {results.get('noema_write', {}).get('writes_per_sec', '?'):>8} wr/s")
    print(f"  - PN@NOEMA: {results.get('noema_phasenav', {}).get('calls_per_sec', '?'):>8} calls/s")

    # Zapisz wynik
    out_path = ROOT / "docs" / "benchmarks" / "pc_noema_phasenav.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print(f"\n  Wynik zapisany: {out_path}")


if __name__ == "__main__":
    main()
