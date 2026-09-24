#!/usr/bin/env python3
"""Szybki ingest dokumentacji NOEMA do PhaseMemory.

Różnica od pełnego learn_windowed(): persist=False na każdym oknie,
jeden save na końcu → bez O(n²) zapisów na dysk.
"""
import sys, re, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.cielingo_inference import CIELingoInference

engine = CIELingoInference()
print(f"PhaseMemory przed: {engine.memory.size} entries")

DOC_PATH = ROOT / "NOEMA_DOCUMENTATION.md"
if not DOC_PATH.exists():
    print(f"ERROR: {DOC_PATH} nie istnieje")
    sys.exit(1)

text = DOC_PATH.read_text(encoding="utf-8")
print(f"Dokument: {DOC_PATH.name} ({len(text)} znaków)")

# Podziel na akapity (min 80, max 800 znaków)
paragraphs = []
for block in re.split(r'\n{2,}', text):
    block = block.strip()
    if len(block) < 80:
        continue
    # Odrzuć markdown tabele i nagłówki-only
    lines = [l for l in block.split('\n') if l.strip() and not l.strip().startswith('|') and not l.strip().startswith('#')]
    clean = ' '.join(lines).strip()
    if len(clean) < 80:
        continue
    # Podziel długie bloki
    while len(clean) > 800:
        split_pos = clean.rfind('. ', 0, 800)
        if split_pos < 200:
            split_pos = 800
        paragraphs.append(clean[:split_pos + 1])
        clean = clean[split_pos + 1:].strip()
    if clean:
        paragraphs.append(clean)

print(f"Akapitów do nauczenia: {len(paragraphs)}")

t0 = time.time()
learned = 0
for i, para in enumerate(paragraphs):
    try:
        engine.learn(para, source="noema_docs", metadata={
            "filename": "NOEMA_DOCUMENTATION.md",
            "para_index": i,
        }, persist=False)  # persist=False → bez zapisu na każdym kroku
        learned += 1
        if (i + 1) % 20 == 0:
            print(f"  {i+1}/{len(paragraphs)} akapitów...")
    except Exception as e:
        print(f"  WARN para {i}: {e}")

# Jeden zbiorczy save na końcu
engine.save()
elapsed = time.time() - t0
print(f"\nNauczono: {learned}/{len(paragraphs)} akapitów w {elapsed:.1f}s")
print(f"PhaseMemory po: {engine.memory.size} entries")
print("Gotowe.")
