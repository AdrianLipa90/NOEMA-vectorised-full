#!/usr/bin/env python3
"""Apply batch 1 quiet-except raise injection."""
import os, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ["APPLY"] = "1"

# Import i wywołaj batch1 z APPLY=1
import sys
sys.argv = ["noema_inject_raise_batch1.py"]
exec((ROOT / "scripts/noema_inject_raise_batch1.py").read_text(encoding="utf-8"))
