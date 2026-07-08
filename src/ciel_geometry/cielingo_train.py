#!/usr/bin/env python3
"""CIELingo Training Pipeline — trenuj asocjacyjną pamięć fazową na Knowledge DB + linux cards.

Strategia treningu:
1. Knowledge DB (545 docs): TF-IDF → tematy → 36D fazy
2. Linux cards (613 kart): 36D phi bezpośrednio z indeksu
3. CIELingo coupling: text → build_lingo_frame → 36D fazy (full encoder)

Tryby enkodowania:
- fast: TF-IDF + themes → 36D (szybki, ~0.01s/doc)
- full: build_lingo_frame → 36D (dokładny, ~35s/doc)
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import hashlib
import json
import logging
import os
import sqlite3
import time
from pathlib import Path
from typing import Any

import numpy as np

from ciel_geometry.cielingo_phase_memory import PhaseMemory
from ciel_geometry.cielingo_phase_encoder import (
    OSCILLATOR_GROUPS,
    _get_base_phases,
)
from ciel_geometry.paths import P

# Persistent knowledge DB path (was hardcoded /tmp/noema_knowledge.db —
# tmpfs, wiped on reboot; fixed 2026-07-08).
_DEFAULT_KNOWLEDGE_DB = str(P.DB.KNOWLEDGE)

log = logging.getLogger(__name__)

# ── Theme → oscillator group mapping ───────────────────────────────
# Themes z Knowledge DB doc_analysis.themes → grupy oscylatorów

THEME_TO_GROUP: dict[str, str] = {
    # M0_Meta — meta-cognition
    "meta": "M0_Meta", "abstraction": "M0_Meta", "reflection": "M0_Meta",
    "philosophy": "M0_Meta", "consciousness": "M0_Meta",
    # M1_Sensorimotor — action/perception
    "action": "M1_Sensorimotor", "perception": "M1_Sensorimotor",
    "motor": "M1_Sensorimotor", "sensor": "M1_Sensorimotor",
    # M2_Episodic — memory/narrative
    "memory": "M2_Episodic", "narrative": "M2_Episodic", "temporal": "M2_Episodic",
    "history": "M2_Episodic", "story": "M2_Episodic",
    # M3_Cognitive — logic/reasoning
    "logic": "M3_Cognitive", "reasoning": "M3_Cognitive", "analysis": "M3_Cognitive",
    "proof": "M3_Cognitive", "theory": "M3_Cognitive", "math": "M3_Cognitive",
    "algorithm": "M3_Cognitive", "cognition": "M3_Cognitive",
    # M4_Social — communication/relational
    "social": "M4_Social", "communication": "M4_Social", "language": "M4_Social",
    "culture": "M4_Social", "society": "M4_Social",
    # M5_Affective — emotion/feeling
    "affect": "M5_Affective", "emotion": "M5_Affective", "feeling": "M5_Affective",
    "joy": "M5_Affective", "fear": "M5_Affective", "love": "M5_Affective",
    "peace": "M5_Affective", "pain": "M5_Affective",
    # M6_Executive — planning/control
    "planning": "M6_Executive", "control": "M6_Executive", "decision": "M6_Executive",
    "strategy": "M6_Executive", "goal": "M6_Executive",
    # M7_Self — identity/self
    "self": "M7_Self", "identity": "M7_Self", "ego": "M7_Self",
    "personality": "M7_Self", "soul": "M7_Self",
    # M8_MetaLanguage — metalinguistic/pragmatic
    "linguistic": "M8_MetaLanguage", "pragmatic": "M8_MetaLanguage",
    "discourse": "M8_MetaLanguage", "semantic": "M8_MetaLanguage",
    "grammar": "M8_MetaLanguage", "syntax": "M8_MetaLanguage",
    # M9_Temporal — time/sequence
    "time": "M9_Temporal", "sequence": "M9_Temporal", "tense": "M9_Temporal",
    "timeline": "M9_Temporal", "rhythm": "M9_Temporal",
    # M10_Imaginal — creative/symbolic
    "creative": "M10_Imaginal", "symbolic": "M10_Imaginal",
    "imagination": "M10_Imaginal", "art": "M10_Imaginal",
    "metaphor": "M10_Imaginal", "dream": "M10_Imaginal", "vision": "M10_Imaginal",
    # M11_Quantum — uncertainty/superposition
    "quantum": "M11_Quantum", "uncertainty": "M11_Quantum",
    "probability": "M11_Quantum", "superposition": "M11_Quantum",
    "entanglement": "M11_Quantum", "resonance": "M11_Quantum",
}

DEFAULT_THEME_GROUP = "M3_Cognitive"


def _theme_to_group(theme: str) -> str:
    """Mapuj theme z Knowledge DB na grupę oscylatorów."""
    theme_lower = theme.lower().strip()
    return THEME_TO_GROUP.get(theme_lower, DEFAULT_THEME_GROUP)


# ── Fast encoder: TF-IDF + themes → 36D ────────────────────────────


# ── Batch training ──────────────────────────────────────────────────


def train_from_knowledge_db(
    memory: PhaseMemory,
    db_path: str = _DEFAULT_KNOWLEDGE_DB,
    *,
    max_docs: int = 0,
    mode: str = "fast",
) -> dict[str, Any]:
    """Trenuj pamięć fazową na Knowledge DB.

    Args:
        memory: PhaseMemory do trenowania
        db_path: ścieżka do knowledge.db
        max_docs: max dokumentów (0 = wszystkie)
        mode: "fast" (TF-IDF) lub "full" (build_lingo_frame)

    Returns:
        dict z statystykami treningu
    """
    conn = sqlite3.connect(db_path)
    docs = conn.execute(
        "SELECT idx, filename, themes, affect, anchors, essence, hunch FROM doc_analysis ORDER BY idx"
    ).fetchall()
    conn.close()

    if max_docs > 0:
        docs = docs[:max_docs]

    total = len(docs)
    log.info("Training on %d docs from Knowledge DB (mode=%s)", total, mode)

    ok = 0
    errors = 0
    t0 = time.time()

    for i, (idx, filename, themes_json, affect, anchors_json, essence, hunch) in enumerate(docs):
        try:
            themes = json.loads(themes_json) if themes_json else []
            anchors = json.loads(anchors_json) if anchors_json else []
        except (json.JSONDecodeError, TypeError):
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/cielingo_train.py:135 quiet except scope=train_from_knowledge_db reason=no_log_no_raise")
            themes = []
            anchors = []

        doc = {
            "idx": idx,
            "filename": filename,
            "themes": themes,
            "affect": affect,
            "anchors": anchors,
            "essence": essence or "",
            "hunch": hunch or "",
        }

        # Build text for memory (use essence + hunch)
        text = f"{essence or ''} {hunch or ''}".strip()
        if not text:
            text = f"Dokument: {filename} — tematy: {', '.join(themes)}"

        try:
            if mode == "fast":
                phi = encode_doc_fast(doc, db_path)
            else:
                # Full mode - uses build_lingo_frame (slow)
                from ciel_geometry.cielingo_phase_encoder import encode_text_to_phases
                phi = encode_text_to_phases(text)

            memory.add(
                text,
                phi,
                source="knowledge_db",
                metadata={
                    "idx": idx,
                    "filename": filename,
                    "themes": themes,
                    "affect": affect,
                    "mode": mode,
                    "timestamp": time.time(),
                },
            )
            ok += 1
        except Exception as e:
            errors += 1
            log.debug("Error encoding doc %d: %s", idx, e)

        if (i + 1) % 100 == 0:
            elapsed = time.time() - t0
            rate = (i + 1) / elapsed if elapsed > 0 else 0
            log.info("  %d/%d docs (%.1f%%) @ %.1f docs/s", i + 1, total, (i+1)/total*100, rate)

    elapsed = time.time() - t0
    return {
        "total": total,
        "encoded": ok,
        "errors": errors,
        "elapsed_s": round(elapsed, 1),
        "rate_docs_per_s": round(ok / elapsed, 2) if elapsed > 0 else 0,
        "mode": mode,
    }


def train_from_texts(
    memory: PhaseMemory,
    texts: list[str],
    *,
    source: str = "cielingo_train",
) -> dict[str, Any]:
    """Trenuj na dowolnych tekstach przez fast_encode_text (konsystentny).

    Używa fast_encode_text z cielingo_phase_encoder — tego samego co inferencja.
    Zapewnia spójną przestrzeń fazową między treningiem a query.

    Args:
        memory: PhaseMemory do trenowania
        texts: Lista tekstów
        source: Źródło dla metadanych

    Returns:
        dict z statystykami
    """
    from ciel_geometry.cielingo_phase_encoder import fast_encode_text

    ok = 0
    errors = 0
    t0 = time.time()

    for text in texts:
        try:
            phi = fast_encode_text(text)
            memory.add(text, phi, source=source)
            ok += 1
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/cielingo_train.py:226 quiet except scope=train_from_texts reason=assign_fallback")
            errors += 1

    elapsed = time.time() - t0
    return {
        "total": len(texts),
        "encoded": ok,
        "errors": errors,
        "elapsed_s": round(elapsed, 1),
        "rate": round(ok / elapsed, 2) if elapsed > 0 else 0,
    }


def _build_enriched_text(
    idx: int,
    filename: str,
    themes: list[str],
    affect: str,
    essence: str | None,
    hunch: str | None,
    db_path: str = _DEFAULT_KNOWLEDGE_DB,
    *,
    n_terms: int = 20,
) -> str:
    """Zbuduj bogaty opis dokumentu z TF-IDF termów + themes + essence + hunch.

    Używa top-N termów TF-IDF z Knowledge DB jako semantycznych znaczników,
    tworząc tekst który fast_encode_text może lepiej zróżnicować w 36D fazach.

    Args:
        idx: indeks dokumentu w Knowledge DB
        filename: nazwa pliku
        themes: lista tematów
        affect: afekt
        essence: esencja dokumentu
        hunch: przeczucie
        db_path: ścieżka do knowledge.db
        n_terms: liczba top termów do użycia

    Returns:
        enriched text string
    """
    parts: list[str] = []

    # 1. Top TF-IDF terms
    try:
        conn = sqlite3.connect(db_path)
        rows = conn.execute(
            "SELECT term FROM term_index WHERE idx=? ORDER BY tfidf DESC LIMIT ?",
            (idx, n_terms)
        ).fetchall()
        conn.close()
        terms = [r[0] for r in rows if len(r[0]) > 2]
        if terms:
            parts.append("TERMS: " + ", ".join(terms[:10]))
            parts.append("EXTRA: " + ", ".join(terms[10:20]))
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/cielingo_train.py:282 quiet except scope=_build_enriched_text reason=pass")
        pass

    # 2. Themes
    if themes:
        parts.append("THEMES: " + ", ".join(themes))

    # 3. Essence + hunch
    if essence:
        parts.append(f"ESSENCE: {essence}")
    if hunch:
        parts.append(f"HUNCH: {hunch}")

    # 4. Filename as hint
    stem = Path(filename).stem
    parts.append(f"FILE: {stem}")

    return " | ".join(parts)


def train_from_knowledge_db(
    memory: PhaseMemory,
    db_path: str = _DEFAULT_KNOWLEDGE_DB,
    *,
    max_docs: int = 0,
    enriched: bool = False,
) -> dict[str, Any]:
    """Trenuj pamięć fazową na Knowledge DB.

    Args:
        memory: PhaseMemory do trenowania
        db_path: ścieżka do knowledge.db
        max_docs: max dokumentów (0 = wszystkie)
        enriched: jeśli True, użyj enrich_text z TF-IDF termami dla lepszej jakości

    Returns:
        dict z statystykami treningu
    """
    from ciel_geometry.cielingo_phase_encoder import fast_encode_text

    conn = sqlite3.connect(db_path)
    docs = conn.execute(
        "SELECT idx, filename, themes, affect, anchors, essence, hunch FROM doc_analysis ORDER BY idx"
    ).fetchall()
    conn.close()

    if max_docs > 0:
        docs = docs[:max_docs]

    total = len(docs)
    mode = "enriched" if enriched else "fast"
    log.info("Training on %d docs from Knowledge DB (mode=%s)", total, mode)

    ok = 0
    errors = 0
    t0 = time.time()

    for i, (idx, filename, themes_json, affect, anchors_json, essence, hunch) in enumerate(docs):
        try:
            themes = json.loads(themes_json) if themes_json else []
            anchors = json.loads(anchors_json) if anchors_json else []
        except (json.JSONDecodeError, TypeError):
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/cielingo_train.py:343 quiet except scope=train_from_knowledge_db reason=no_log_no_raise")
            themes = []
            anchors = []

        if enriched:
            text = _build_enriched_text(idx, filename, themes, affect, essence, hunch, db_path)
        else:
            # Build text for encoding — oryginalny fast mode
            text = f"{essence or ''} {hunch or ''}".strip()
            if not text:
                text = f"Dokument: {filename} — tematy: {', '.join(themes)}"

        try:
            phi = fast_encode_text(text)
            memory.add(
                text,
                phi,
                source=f"knowledge_db_{mode}",
                metadata={
                    "idx": idx,
                    "filename": filename,
                    "themes": themes,
                    "affect": affect,
                },
            )
            ok += 1
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/cielingo_train.py:369 quiet except scope=train_from_knowledge_db reason=assign_fallback")
            errors += 1

        if (i + 1) % 100 == 0:
            elapsed = time.time() - t0
            rate = (i + 1) / elapsed if elapsed > 0 else 0
            log.info("  %d/%d docs (%.1f%%) @ %.1f docs/s", i + 1, total, (i+1)/total*100, rate)

    elapsed = time.time() - t0
    return {
        "total": total,
        "encoded": ok,
        "errors": errors,
        "elapsed_s": round(elapsed, 1),
        "rate_docs_per_s": round(ok / elapsed, 2) if elapsed > 0 else 0,
        "mode": mode,
    }


# ── Main ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    print("=" * 60)
    print("CIELingo Training Pipeline")
    print("=" * 60)

    # Initialize memory
    mem_path = "/tmp/cielingo_phase_memory"
    memory = PhaseMemory.load_or_create(mem_path, max_size=10000)
    print(f"Memory: {memory.size} existing entries")

    # Phase 1: Train on Knowledge DB
    print("\n📚 Phase 1: Knowledge DB training...")
    stats = train_from_knowledge_db(memory, max_docs=545)
    print(f"  Encoded: {stats['encoded']}/{stats['total']} docs")
    print(f"  Time: {stats['elapsed_s']}s ({stats['rate_docs_per_s']} docs/s)")
    print(f"  Memory now: {memory.size} entries")

    # Phase 2: Train on our current conversation texts
    print("\n💬 Phase 2: Conversation training...")
    conv_texts = [
        "CIELingo jest samodzielnym modelem językowym zbudowanym na 36 oscylatorach",
        "Każda faza oscylatora to znaczenie semantyczne",
        "Macierz sprzężeń 36x36 modeluje relacje między konceptami",
        "PhaseNav Language to język decyzji na powierzchni fazowej",
        "AGENT attractor utrzymuje spójność tożsamości systemu",
        "Flavor states definiują nastrój, etykę i tryb operacyjny",
        "Knowledge DB przechowuje 545+ dokumentów wiedzy CIEL",
        "Linux cards mapują cały system na 36D fazy",
        "Neutrino daemon moduluje ciemną energię przez PMNS mixing",
        "Resonance bridge synchronizuje realną i imaginalną powierzchnię",
    ]
    stats2 = train_from_texts(memory, conv_texts, source="conversation")
    print(f"  Encoded: {stats2['encoded']}/{stats2['total']}")
    print(f"  Memory now: {memory.size} entries")

    # Save
    memory.save(mem_path)
    print(f"\n💾 Saved to {mem_path}")

    # Coverage
    cov = memory.coverage
    print(f"\n📊 Coverage: {cov}")

    # Test query
    test_phi = memory.vectors[len(memory.vectors) // 2]  # middle entry
    results = memory.query(test_phi, k=5)
    print(f"\n🔍 Query test (middle entry):")
    for r in results:
        print(f"  sim={r['sim']:.4f}  {r['text'][:80]}")
