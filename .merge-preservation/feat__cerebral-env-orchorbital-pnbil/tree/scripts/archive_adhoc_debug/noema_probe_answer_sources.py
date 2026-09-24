#!/usr/bin/env python3
"""Diagnostyka: ile sources zwraca answer() i co przechodzi przez daemon NL filter."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.cielingo_inference import CIELingoInference

engine = CIELingoInference()

def _is_natural_language_daemon(t: str) -> bool:
    """Kopia daemon's _is_natural_language filter."""
    t = t.strip()
    if len(t) < 30:
        return False
    if t.startswith(("#", "{", "[", "```", "- **")):
        return False
    if "**id_karty:**" in t or '"method":' in t or '"samples":' in t:
        return False
    if t.startswith("REPO-") or "## Tożsamość" in t or "poziom_orbitalny" in t:
        return False
    _REPO_MARKERS = ("**Purpose**:", "**Imports**:", "**Exports**:",
                     "**Active**:", "**Uses**:", "**Status**:",
                     "**Entry points**:", "**Optional deps**:",
                     "**Dependencies**:", "**Description**:")
    if any(m in t for m in _REPO_MARKERS):
        return False
    non_ascii = sum(1 for c in t if ord(c) > 127 and not c.isalpha())
    if non_ascii > len(t) * 0.25:
        return False
    return True

QUESTIONS = [
    "Czym jest system NOEMA i jak działa jego architektura?",
    "Opowiedz mi o PhaseNav i fazach w systemie.",
]

for q in QUESTIONS:
    print(f"\nPYTANIE: {q}")
    result = engine.answer(q, k=15)
    sources = result.get("sources", [])
    confidence = result.get("decision", {}).get("confidence", "?")
    action = result.get("decision", {}).get("action", "?")
    print(f"  Confidence: {confidence}  Action: {action}")
    print(f"  Sources count: {len(sources)}")

    prose_count = sum(1 for s in sources if s.get("source_type") == "prose_sentence")
    print(f"  prose_sentence entries: {prose_count}")

    memory_entries = []
    for src in sources[:15]:
        txt = src.get("text", "").strip()
        src_source = src.get("source", "?")
        sim_val = float(src.get("sim") or 0)
        sim_threshold = 0.0 if src_source == "noema_docs" else 0.20
        if txt and sim_val >= sim_threshold and _is_natural_language_daemon(txt):
            memory_entries.append({"text": txt, "source": "phasememory",
                                   "source_type": src.get("source_type", ""), "sim": sim_val})

    noema_docs_count = sum(1 for e in memory_entries)
    print(f"  memory_entries after daemon NL filter: {noema_docs_count}")
    print(f"  knowledge_tfidf will be added: {noema_docs_count == 0}")

    print(f"\n  SOURCES po daemon NL filter (pierwsze 18):")
    for i, e in enumerate(memory_entries[:18]):
        stype = e.get("source_type", "")
        label = " [PROSE]" if stype == "prose_sentence" else ""
        print(f"  [{i}] sim={e['sim']:.4f}{label} | {repr(e['text'][:100])}")
