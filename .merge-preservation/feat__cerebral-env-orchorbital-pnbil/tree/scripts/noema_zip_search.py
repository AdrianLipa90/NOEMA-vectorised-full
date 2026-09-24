#!/usr/bin/env python3
"""PhaseNav ZIP Search — szukaj archiwów po operator fingerprint + surface state.

Usage:
    python scripts/noema_zip_search.py                           # surface → top 5 matching ZIPS
    python scripts/noema_zip_search.py --operator MEMORY         # ręczny operator
    python scripts/noema_zip_search.py --fingerprint HHHL        # ręczny fingerprint
    python scripts/noema_zip_search.py --list-operators          # lista wszystkich operatorów
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

ZIP_INDEX = Path("/dev/shm/ciel_noema/zip_catalog/index.jsonl")


def load_index(path: Path = ZIP_INDEX) -> list[dict]:
    entries = []
    with open(path) as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))
    return entries


def surface_phasenav() -> dict:
    from ciel_geometry.noema_surface_mmap import open_surface, DEFAULT_SURFACE_ROOT
    from ciel_geometry.linux_sensor import LinuxSensor
    surface = open_surface(DEFAULT_SURFACE_ROOT)
    sensor = LinuxSensor()
    snap = sensor.snapshot()
    return sensor.process_phasenav(snap)


def operator_distribution(entries: list[dict]) -> Counter:
    return Counter(e.get("phasenav", {}).get("operator_id", "UNKNOWN") for e in entries)


def fingerprint_distribution(entries: list[dict]) -> Counter:
    return Counter(e.get("phasenav", {}).get("harmonic_fingerprint", "????") for e in entries)


def search_by_operator(entries: list[dict], operator: str, top: int = 10) -> list[dict]:
    matches = [e for e in entries if e.get("phasenav", {}).get("operator_id") == operator]
    matches.sort(key=lambda e: -e.get("total_files", 0))
    return matches[:top]


def search_by_fingerprint(entries: list[dict], fp: str, top: int = 10) -> list[dict]:
    matches = [e for e in entries if e.get("phasenav", {}).get("harmonic_fingerprint") == fp]
    matches.sort(key=lambda e: -e.get("total_files", 0))
    return matches[:top]


def search_surface_match(entries: list[dict], surface_pn: dict, top: int = 10) -> list[dict]:
    """Znajdź ZIPS których operator/fingerprint pasuje do stanu powierzchni."""
    op = surface_pn["operator"]
    fp = surface_pn["harmonic_fingerprint"]

    exact_op = [e for e in entries if e.get("phasenav", {}).get("operator_id") == op]
    exact_fp = [e for e in entries if e.get("phasenav", {}).get("harmonic_fingerprint") == fp]

    # Score: exact match operator = 2pts, fingerprint = 1pt
    scored = {}
    for e in exact_op:
        scored[id(e)] = (2, e)
    for e in exact_fp:
        fid = id(e)
        if fid in scored:
            scored[fid] = (scored[fid][0] + 1, e)
        else:
            scored[fid] = (1, e)

    ranked = sorted(scored.values(), key=lambda x: -x[0])
    return [e for score, e in ranked][:top]


def format_entry(entry: dict) -> str:
    pn = entry.get("phasenav", {})
    path = entry.get("zip_path", "?")
    name = Path(path).name if path != "?" else "?"
    files = entry.get("total_files", 0)
    size = entry.get("size_mb", 0)
    op = pn.get("operator_id", "?")
    fp = pn.get("harmonic_fingerprint", "?")
    R = pn.get("harmonic_imprint", {})
    R_str = " ".join(f"{k}={R.get(k,0):.3f}" for k in ("R_1","R_3","R_6","R_9"))
    return f"  {op:<22} {fp:<5} | {name:<64} | {files:>5} files {size:>7.1f}MB | {R_str}"


def main():
    ap = argparse.ArgumentParser(description="PhaseNav ZIP Search")
    ap.add_argument("--operator", type=str, default=None, help="Szukaj po operatorze")
    ap.add_argument("--fingerprint", type=str, default=None, help="Szukaj po fingerprint HHHH/LLHL etc")
    ap.add_argument("--top", type=int, default=5, help="Liczba wyników")
    ap.add_argument("--list-operators", action="store_true", help="Lista operatorów + częstość")
    ap.add_argument("--list-fingerprints", action="store_true", help="Lista fingerprintów + częstość")
    args = ap.parse_args()

    print("[ZIP Search] loading index...", file=sys.stderr)
    entries = load_index()
    print(f"[ZIP Search] {len(entries)} entries loaded", file=sys.stderr)

    if args.list_operators:
        dist = operator_distribution(entries)
        print(f"\n=== Operator Distribution ({len(dist)} types) ===\n")
        for op, count in dist.most_common():
            print(f"  {op:<24} {count:>4}")
        return

    if args.list_fingerprints:
        dist = fingerprint_distribution(entries)
        print(f"\n=== Fingerprint Distribution ({len(dist)} types) ===\n")
        for fp, count in dist.most_common():
            print(f"  {fp:<5} {count:>4}")
        return

    if args.operator:
        results = search_by_operator(entries, args.operator, args.top)
        print(f"\n=== Top {len(results)} ZIPS for operator: {args.operator} ===\n")
    elif args.fingerprint:
        results = search_by_fingerprint(entries, args.fingerprint, args.top)
        print(f"\n=== Top {len(results)} ZIPS for fingerprint: {args.fingerprint} ===\n")
    else:
        pn = surface_phasenav()
        print(f"\n=== Surface state ===")
        print(f"  Operator: {pn['operator']} (cos={pn['cos_similarity']})")
        print(f"  Fingerprint: {pn['harmonic_fingerprint']}")
        print(f"  R: {pn['R']}")
        print(f"  δΦ: {pn['thinking_delta']}")
        print(f"  Flavor: {pn['flavor']}")
        print()
        results = search_surface_match(entries, pn, args.top)
        print(f"=== Top {len(results)} ZIPS matching surface state ===\n")

    for i, e in enumerate(results, 1):
        print(f"[{i:>2}] {format_entry(e)}")


if __name__ == "__main__":
    main()
