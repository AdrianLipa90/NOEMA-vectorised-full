#!/usr/bin/env python3
"""Apply batch 2 quiet-except raise injection."""
import os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ["APPLY"] = "1"
sys.argv = ["noema_inject_raise_batch2.py"]
exec((ROOT / "scripts/noema_inject_raise_batch2.py").read_text(encoding="utf-8"))
