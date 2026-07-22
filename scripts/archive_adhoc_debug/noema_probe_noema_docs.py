#!/usr/bin/env python3
"""Diagnostyka: ile wpisów noema_docs przechodzi filtr NL i co zawierają."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.cielingo_inference import CIELingoInference

engine = CIELingoInference()
mem = engine.memory

total = mem.size
noema_doc_entries = []
for i in range(total):
    meta = mem.metadata[i] if i < len(mem.metadata) else {}
    if meta.get("source") == "noema_docs":
        noema_doc_entries.append((i, mem.texts[i]))

print(f"PhaseMemory total: {total}")
print(f"noema_docs entries: {len(noema_doc_entries)}")
print()

# Sprawdź filtr NL
_REPO_MARKERS = ("**Purpose**:", "**Imports**:", "**Exports**:", "**Active**:",
                 "**Uses**:", "**Status**:", "**Entry points**:", "**Optional deps**:",
                 "**Dependencies**:", "**id_karty:**", '"method":', '"samples":')

nl_pass = []
nl_fail = []
for idx, text in noema_doc_entries:
    t = text.strip()
    fail_reason = None
    if t.startswith(("#", "{", "[", "```", "- **")):
        fail_reason = f"starts_with_special: {t[:30]!r}"
    elif any(m in t for m in _REPO_MARKERS):
        fail_reason = f"repo_marker: {next(m for m in _REPO_MARKERS if m in t)}"
    elif t.startswith("REPO-") or "## Tożsamość" in t or "poziom_orbitalny" in t:
        fail_reason = "special_term"
    else:
        non_ascii = sum(1 for c in t if ord(c) > 127 and not c.isalpha())
        if non_ascii > len(t) * 0.25:
            fail_reason = f"dingbats: {non_ascii}/{len(t)}"

    if fail_reason:
        nl_fail.append((idx, text[:80], fail_reason))
    else:
        nl_pass.append((idx, text[:120]))

print(f"Przechodzi NL filtr: {len(nl_pass)}")
print(f"Odpada:              {len(nl_fail)}")
print()

print("=== PRZECHODZĄCE (pierwsze 20) ===")
for idx, t in nl_pass[:20]:
    print(f"  [{idx}] {t!r}")
print()

print("=== ODPADY (powody) ===")
from collections import Counter
reasons = Counter(r for _, _, r in nl_fail)
for reason, count in reasons.most_common(10):
    # show reason prefix
    r_key = reason.split(":")[0]
    print(f"  {r_key}: {count}")
print()

# Teraz sprawdź similarity dla typowego pytania
phi_q = engine.encode("Czym jest system NOEMA i jak działa jego architektura?")
results = engine.memory.query(phi_q, k=30, min_sim=0.05, include_sources={"noema_docs"})
print(f"Wyniki include_sources=noema_docs, min_sim=0.05: {len(results)}")
for r in results[:10]:
    print(f"  sim={r['sim']:.4f} | {r['text'][:100]!r}")
