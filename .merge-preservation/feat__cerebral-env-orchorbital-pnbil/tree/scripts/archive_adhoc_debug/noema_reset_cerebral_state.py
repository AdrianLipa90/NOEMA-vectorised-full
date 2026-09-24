#!/usr/bin/env python3
"""Reset cerebral_state.json i cerebral_continuity.json — kasuje stary kontekst testowy."""
from pathlib import Path
import json, time

ROOT = Path("/home/adrian/noema")
STATE = ROOT / "runtime/cerebral_state.json"
CONT = ROOT / "runtime/cerebral_continuity.json"

for p in [STATE, CONT]:
    if p.exists():
        bak = p.with_suffix(".json.bak_reset")
        p.rename(bak)
        print(f"Backed up: {p.name} -> {bak.name}")
    else:
        print(f"Not found (ok): {p.name}")

print("Done. Cerebral state reset — nowa sesja zacznie od czystego kontekstu.")
print("Nastepna wiadomosc od Adriana ustawi nowy aktywny temat.")
