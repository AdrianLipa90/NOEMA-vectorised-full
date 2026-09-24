#!/usr/bin/env python3
"""Ingestuje dokumentację NOEMA do PhaseMemory.

Czyta kluczowe pliki .md z repo NOEMA i uczy je do PhaseMemory
przez learn_windowed() z source='noema_docs'.
"""
import sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.cielingo_inference import CIELingoInference
from ciel_sot_agent.phasenav_learning_gate import learn_windowed

DOC_FILES = [
    ROOT / "NOEMA_DOCUMENTATION.md",
    ROOT / "NOEMA_DEBUG.md",
]
# Dodaj pliki jeśli istnieją
for extra in [
    ROOT / "README.md",
    ROOT / "docs" / "architecture.md",
    ROOT / "docs" / "phasenav.md",
]:
    if extra.exists():
        DOC_FILES.append(extra)

engine = CIELingoInference()
print(f"PhaseMemory przed: {engine.memory.size} entries")

total_windows = 0
for doc_path in DOC_FILES:
    if not doc_path.exists():
        print(f"SKIP (nie istnieje): {doc_path.name}")
        continue
    text = doc_path.read_text(encoding="utf-8")
    print(f"\nINGEST: {doc_path.name} ({len(text)} znaków)")
    t0 = time.time()
    result = learn_windowed(
        engine, text,
        source="noema_docs",
        source_type="documentation",
        metadata={"filename": doc_path.name, "path": str(doc_path)},
        dry_run=False,
    )
    elapsed = time.time() - t0
    if result.get("skipped"):
        print(f"  SKIP: {result['skipped']}")
    else:
        n = result.get("n_windows", 0)
        total_windows += n
        print(f"  Nauczono: {n} okien konceptualnych ({elapsed:.1f}s)")

print(f"\nPhaseMemory po: {engine.memory.size} entries (+{total_windows} nowych)")
print("Gotowe.")
