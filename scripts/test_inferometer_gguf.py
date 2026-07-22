#!/usr/bin/env python3
"""Test inferometer.py z GGUF validator na 11 zdaniach."""
import sys, json
sys.path.insert(0, "/home/adrian/Pulpit/Adrian'sReq")

from inferometer import Orchestrator

SENTENCES = [
    "CIEL to system inferencji semantycznej.",
    "Nie każdy człowiek wie, że prawda jest atraktorem.",
    "Jan widzi Marię na macierzy operatorów.",
    "Kot siedzi na macie i rozważa holonomię.",
    "Prawda jest atraktorem w przestrzeni fazowej.",
    "Źródło danych wymaga weryfikacji przed kanonizacją.",
    "Każdy token przechodzi przez bramę fazową.",
    "Zgoda użytkownika jest wymagana przed akcją.",
    "Hipoteza nie może być traktowana jako fakt.",
    "Runtime nie ma dostępu do zewnętrznych źródeł.",
    "Semantyczna blizna pojawia się gdy źródło jest nieznane.",
]

orch = Orchestrator()

results = []
for i, sentence in enumerate(SENTENCES, 1):
    r = orch.run(sentence)
    results.append({
        "n": i,
        "text": sentence,
        "fingerprint": r.fingerprint,
        "J_surface": round(r.J_surface, 4),
        "gate": r.gate_verdict,
        "errors": r.errors,
        "time_ms": r.processing_time_ms,
    })
    print(f"[{i:02d}] FP={r.fingerprint} J_s={r.J_surface:.4f} gate={r.gate_verdict} err={r.errors} t={r.processing_time_ms}ms")
    print(f"      {sentence}")

print()
gates = {}
for res in results:
    gates[res["gate"]] = gates.get(res["gate"], 0) + 1
print(f"Gate summary: {gates}")
errors_total = sum(len(r["errors"]) for r in results)
print(f"Errors total: {errors_total}")
avg_t = sum(r["time_ms"] for r in results) / len(results)
print(f"Avg time: {avg_t:.1f}ms")
