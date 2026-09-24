#!/usr/bin/env python3
"""CIELingo uczy się przez PhaseNav — CLI.

Usage:
    .venv/bin/python3 scripts/noema_cielingo_learn_phasenav.py [options]

Options:
    --trace CARD_ID CARD_ID ...    Trace ścieżki konceptów przez PhaseNav → CIELingo
    --enrich TEXT                  Enrich tekst przez PhaseNav → CIELingo
    --scan                         Skanuj blizny CIELingo przez PhaseNav
    --self-cycle                   Wykonaj jeden cykl self-cycle z PhaseNav
    --status                       Status PhaseNav + CIELingo
    --watch [interval]             Tryb ciągły: co N sekund cykl + scan (domyślnie 30s)
"""

from __future__ import annotations
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from cielingo_core.bridge.phasenav_learning_bridge import (
    PhaseNavLearningBridge,
    phasenav_learn_trace,
    phasenav_enrich_text,
    phasenav_scan_scars,
)
from cielingo_core.cycle.self_cycle import CIELingoSelfCycle


def cmd_trace(args: list[str]) -> None:
    if len(args) < 2:
        print("Usage: --trace CARD_ID CARD_ID [CARD_ID ...]")
        sys.exit(1)
    result = phasenav_learn_trace(args)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_enrich(args: list[str]) -> None:
    text = " ".join(args) if args else sys.stdin.read().strip()
    if not text:
        print("Usage: --enrich TEXT or pipe text to stdin")
        sys.exit(1)
    result = phasenav_enrich_text(text)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_scan() -> None:
    result = phasenav_scan_scars()
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_self_cycle() -> None:
    cycle = CIELingoSelfCycle()
    result = cycle.cycle()
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_status() -> None:
    bridge = PhaseNavLearningBridge()
    pn = bridge.count()
    cycle = CIELingoSelfCycle()
    state = cycle.surface_state()
    print(json.dumps({
        "phasenav": {
            "available": bridge.solver is not None,
            "concepts": pn.get("concepts", 0),
            "edges": pn.get("edges", 0),
            "operators": pn.get("operators", 0),
        },
        "cielingo": state,
    }, indent=2, ensure_ascii=False))


def cmd_watch(interval: int = 30) -> None:
    print(f"PhaseNav CIELingo watch mode — every {interval}s")
    cycle = CIELingoSelfCycle()
    bridge = PhaseNavLearningBridge()
    while True:
        ts = time.strftime("%H:%M:%S")
        cyc = cycle.cycle()
        scan = bridge.scan_scars_via_phasenav()
        pn = bridge.count()
        print(f"[{ts}] cycle={cyc['cycle']} scars={cyc.get('scars_reviewed', 0)} "
              f"repair_paths={scan.get('n_repair_paths', 0)} "
              f"PN={pn.get('concepts', 0)}c/{pn.get('edges', 0)}e")
        sys.stdout.flush()
        time.sleep(interval)


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]
    rest = sys.argv[2:]

    if cmd == "--trace":
        cmd_trace(rest)
    elif cmd == "--enrich":
        cmd_enrich(rest)
    elif cmd == "--scan":
        cmd_scan()
    elif cmd == "--self-cycle":
        cmd_self_cycle()
    elif cmd == "--status":
        cmd_status()
    elif cmd == "--watch":
        interval = int(rest[0]) if rest else 30
        cmd_watch(interval)
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
