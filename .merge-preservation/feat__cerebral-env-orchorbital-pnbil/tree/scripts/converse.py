#!/usr/bin/env python3
"""Rozmowa z CIEL — przez ramy walencyjne LNS i karty języka."""
from __future__ import annotations

import json
import time
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))

from ciel_coupling import process_user_input, get_ciel_state
from ciel_speaker import speak


def _summarise(d: dict) -> str:
    se = d.get("semantic_encoder") or {}
    parts = [
        d.get("dominant_emotion", "?"),
        f"soul={d.get('soul_invariant',0):.3f}",
        f"coher={d.get('coherence_index',0):.3f}",
        f"closure={d.get('closure_penalty',0):.3f}",
        f"φ={se.get('phase',0):.3f}",
        se.get("brain_region", "?"),
    ]
    return "  [" + "  ".join(parts) + "]"


def main() -> None:
    print("=== CIEL ===")
    print("/slow /state /exit")
    print()

    try:
        from ciel_sot_agent.cielingo_bridge import build_lingo_frame
    except Exception:
        build_lingo_frame = None

    try:
        while True:
            text = input("Ty: ").strip()
            if not text:
                continue
            if text.lower() == "/exit":
                print("Do zobaczenia.")
                break
            if text.lower() == "/state":
                print(json.dumps(get_ciel_state(), indent=2, ensure_ascii=False, default=str)[:2000])
                continue
            slow = text.lower() == "/slow"
            if slow:
                text = "przetworz gleboko"

            t0 = time.time()
            ciel_state = process_user_input(text, fast=not slow)
            lingo = build_lingo_frame(text) if build_lingo_frame else {}
            elapsed = time.time() - t0

            reply = speak(ciel_state, lingo, text)
            print(f"\nCIEL ({elapsed:.1f}s): {reply}")
            print(_summarise(ciel_state))
            print()

    except (KeyboardInterrupt, EOFError):
        print("\nDo zobaczenia.")


if __name__ == "__main__":
    main()
