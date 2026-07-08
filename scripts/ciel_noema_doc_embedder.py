#!/usr/bin/env python3
"""CIELingo Document Embedder — Knowledge DB → 36D PhaseNav embedding.

Czyta Knowledge DB SQLite (545 dokumenty, 562k termów TF-IDF).
Każdy dokument → 36D wektor fazowy kompatybilny z NOEMA PhaseNav:
  12 kanałów pamięci × 3 oscylatory = 36D

Kanały:
  M0 Perceptual       (0-2)   — term frequency, percept density
  M1 Working          (3-5)   — operator density, syntax weight
  M2 Episodic         (6-8)   — contextual grounding, temporal anchors
  M3 Semantic         (9-11)  — TF-IDF depth, semantic mass
  M4 Procedural       (12-14) — action verbs, process density
  M5 Affective        (15-17) — emotional valence, affect score
  M6 Identity         (18-20) — self-reference, author alignment
  M7 Braid            (21-23) — cross-reference, relation count
  M8 Meta             (24-26) — metacognitive, abstraction level
  M9 Temporal         (27-29) — temporal distribution, freshness
  M10 Imaginal        (30-32) — creative divergence, metaphor
  M11 Quantum         (33-35) — uncertainty, open questions

Output:
  /tmp/noema_knowledge_embeddings.npy   — (545, 36) numpy array
  /tmp/noema_knowledge_embeddings.json  — index: doc_idx → filename + φ vector

Usage:
  python3 scripts/ciel_noema_doc_embedder.py [--rebuild]
"""
from __future__ import annotations

import argparse
import json
import logging
import math
import sqlite3
import sys
import time
from pathlib import Path

import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format="[embedder] %(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

N_CHANNELS = 12
OSC_PER_CHANNEL = 3
N_OSCILLATORS = N_CHANNELS * OSC_PER_CHANNEL  # 36

KB_PATH = Path("/tmp/noema_knowledge.db")
OUTPUT_NPY = Path("/tmp/noema_knowledge_embeddings.npy")
OUTPUT_JSON = Path("/tmp/noema_knowledge_embeddings.json")

# Channel → term category mapping (simple heuristic)
CHANNEL_KEYWORDS: dict[str, list[str]] = {
    "M0_Perceptual": ["percept", "sensor", "obserw", "widz", "postrzeg", "zmysł", "światło", "dźwięk", "obraz",
                      "perception", "sense", "light", "sound", "image", "pattern", "shape", "color"],
    "M1_Working": ["operator", "logik", "składnia", "struktur", "funkcj", "proces", "algorithm", "compute",
                   "syntax", "grammar", "logic", "function", "process", "operation"],
    "M2_Episodic": ["kontekst", "epizod", "zdarzen", "scen", "sytuacj", "pamięć", "wspomnien", "doświadczen",
                    "context", "episode", "event", "scene", "memory", "experience", "place", "time"],
    "M3_Semantic": ["znaczen", "semantyk", "definicj", "pojęci", "rozumien", "wiedza", "koncept", "meaning",
                    "semantic", "concept", "knowledge", "understanding", "define", "term"],
    "M4_Procedural": ["procedur", "działan", "umiejętnoś", "metoda", "technik", "krok", "instrukcj", "skill",
                      "procedure", "action", "method", "technique", "step", "practice"],
    "M5_Affective": ["emocj", "uczuci", "nastrój", "afekt", "wartoś", "etyk", "moral", "uczuci",
                     "emotion", "feeling", "mood", "affect", "value", "ethical", "moral", "love", "fear"],
    "M6_Identity": ["tożsamoś", "osoba", "podmiot", "autor", "ja", "self", "identity", "soul", "ego",
                    "identity", "self", "author", "subject", "person", "character"],
    "M7_Braid": ["relacj", "powiązan", "sieć", "graf", "łącz", "korelacj", "affinity", "relation",
                 "relation", "connection", "network", "graph", "link", "braid", "weave"],
    "M8_Meta": ["meta", "refleksj", "abstrakcj", "model", "teori", "paradygmat", "metacognition",
                "meta", "reflection", "abstract", "model", "theory", "paradigm", "cognition"],
    "M9_Temporal": ["czas", "przeszłoś", "przyszłoś", "teraz", "chwil", "moment", "tempus",
                    "time", "past", "future", "present", "moment", "temporal", "duration"],
    "M10_Imaginal": ["wyobraźn", "kreatywnoś", "imaginacj", "symbol", "metafor", "wizj", "fantazj",
                     "imagination", "creative", "vision", "symbol", "metaphor", "dream", "myth"],
    "M11_Quantum": ["kwant", "niepewnoś", "potencjał", "superpozycj", "splątan", "probabilist",
                    "quantum", "uncertain", "potential", "superposition", "entangle", "probability"],
}

# Emotional valence mapping for affect channel
EMOTION_WORDS: dict[str, float] = {
    "love": 0.95, "joy": 0.85, "hope": 0.75, "beauty": 0.80, "peace": 0.70,
    "fear": -0.85, "pain": -0.90, "anger": -0.75, "sadness": -0.80, "loss": -0.85,
    "miłość": 0.95, "radość": 0.85, "nadzieja": 0.75, "pokój": 0.70, "strach": -0.85,
    "ból": -0.90, "gniew": -0.75, "smutek": -0.80, "cierpienie": -0.85, "piękno": 0.80,
}


def _load_kb() -> tuple[list[dict], np.ndarray | None]:
    """Ładuje Knowledge DB. Zwraca (docs, embeddings)."""
    if not KB_PATH.exists():
        log.error("Knowledge DB not found at %s", KB_PATH)
        return [], None

    conn = sqlite3.connect(str(KB_PATH))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Load existing embeddings if available
    embeddings = None
    if OUTPUT_NPY.exists():
        try:
            embeddings = np.load(str(OUTPUT_NPY))
            log.info("Loaded existing embeddings: %s", embeddings.shape)
        except Exception as e:
            log.warning("Could not load embeddings: %s", e)

    # Load docs
    rows = cur.execute(
        "SELECT idx, filename, themes, affect, anchors, essence, hunch, full_text_len "
        "FROM doc_analysis ORDER BY idx"
    ).fetchall()
    conn.close()

    docs = []
    for r in rows:
        docs.append({
            "idx": r["idx"],
            "filename": r["filename"] or f"doc_{r['idx']}",
            "themes": r["themes"] or "",
            "affect": r["affect"] or "",
            "anchors": r["anchors"] or "",
            "essence": r["essence"] or "",
            "hunch": r["hunch"] or "",
            "full_text_len": r["full_text_len"] or 0,
        })

    log.info("Loaded %d docs from Knowledge DB", len(docs))
    return docs, embeddings


def _load_tfidf(idx: int) -> dict[str, float]:
    """Ładuje TF-IDF termy dla dokumentu o danym idx."""
    if not KB_PATH.exists():
        return {}
    conn = sqlite3.connect(str(KB_PATH))
    cur = conn.cursor()
    rows = cur.execute(
        "SELECT term, tfidf FROM term_index WHERE idx = ? ORDER BY tfidf DESC LIMIT 200",
        (idx,)
    ).fetchall()
    conn.close()
    return {row[0]: row[1] for row in rows}


def _compute_channel_weights(terms: dict[str, float]) -> np.ndarray:
    """Mapuje termy TF-IDF na 12 kanałów. Zwraca (12,) wag per kanał."""
    weights = np.zeros(N_CHANNELS, dtype=np.float64)
    for term, tfidf in terms.items():
        term_lower = term.lower()
        for ch_idx, (ch_name, keywords) in enumerate(CHANNEL_KEYWORDS.items()):
            for kw in keywords:
                if kw in term_lower:
                    weights[ch_idx] += tfidf * 0.5  # partial match
                    break
            # exact match → full weight
            if term_lower in keywords:
                weights[ch_idx] += tfidf * 0.5  # was already partial, now total
    # Normalize
    max_w = max(float(np.max(weights)), 1e-12)
    weights = weights / max_w
    return weights


def _compute_affect_valence(affect_text: str) -> float:
    """Oblicza średnią walencję emocjonalną z tekstu affect."""
    if not affect_text:
        return 0.0
    words = affect_text.lower().split()
    valence_sum = 0.0
    count = 0
    for w in words:
        if w in EMOTION_WORDS:
            valence_sum += EMOTION_WORDS[w]
            count += 1
        # Strip punctuation
        clean = w.strip(".,!?;:'\"()[]{}")
        if clean != w and clean in EMOTION_WORDS:
            valence_sum += EMOTION_WORDS[clean]
            count += 1
    if count == 0:
        return 0.0
    return valence_sum / count


def _doc_to_phi(doc: dict, terms: dict[str, float], seed: int = 0) -> np.ndarray:
    """Dokument → 36D wektor fazowy PhaseNav.

    φ dla każdego kanału = wynik TF-IDF + affect + cechy dokumentu.
    ω (natural freq) = entropy/zróżnicowanie termów.
    """
    np.random.seed(seed + doc["idx"])

    # Wagi kanałów z TF-IDF
    channel_w = _compute_channel_weights(terms)

    # Affect valence → kanał M5 (Affective)
    affect_val = _compute_affect_valence(doc.get("affect", ""))

    # Liczba termów (entropy proxy dla kanału M3 Semantic)
    n_terms = len(terms)
    entropy = math.log(max(n_terms, 2))

    # Długość tekstu → M9 Temporal (ciężar czasowy)
    text_len_norm = min(doc.get("full_text_len", 0) / 10000.0, 1.0)

    # Anchors → M2 Episodic
    anchors = doc.get("anchors", "")
    anchor_count = len(anchors.split()) if anchors else 0

    # Essence → M6 Identity
    essence = doc.get("essence", "")
    essence_depth = min(len(essence) / 500.0, 1.0) if essence else 0.0

    # Hunch/open questions → M11 Quantum
    hunch = doc.get("hunch", "")
    hunch_depth = min(len(hunch) / 300.0, 1.0) if hunch else 0.0

    # Buduj (12, 3) — 3 oscylatory na kanał
    phi_2d = np.zeros((N_CHANNELS, OSC_PER_CHANNEL), dtype=np.float64)

    for ch in range(N_CHANNELS):
        base_w = channel_w[ch]
        # Każdy z 3 oscylatorów w kanale ma lekko przesuniętą fazę
        for osc in range(OSC_PER_CHANNEL):
            phase_shift = osc * (2.0 * np.pi / 3.0)  # 120° między oscylatorami
            # ω = natural frequency z channel weight + entropy
            omega = 0.5 + base_w * 2.0 + entropy * 0.05
            # φ z ω i przesunięciem
            phi = (omega * doc["idx"] * 0.01 + phase_shift + base_w * np.pi) % (2.0 * np.pi)
            phi_2d[ch, osc] = phi

    # Specyficzne modulacje
    # M2 Episodic: anchors boost
    phi_2d[2] = (phi_2d[2] + anchor_count * 0.05) % (2.0 * np.pi)
    # M5 Affective: affect valence jako przesunięcie fazy
    phi_2d[5] = (phi_2d[5] + affect_val) % (2.0 * np.pi)
    # M6 Identity: essence depth
    phi_2d[6] = (phi_2d[6] + essence_depth * np.pi) % (2.0 * np.pi)
    # M9 Temporal: text length
    phi_2d[9] = (phi_2d[9] + text_len_norm * np.pi) % (2.0 * np.pi)
    # M11 Quantum: hunch depth
    phi_2d[11] = (phi_2d[11] + hunch_depth * np.pi) % (2.0 * np.pi)

    return phi_2d.ravel()  # (36,)


def _embed_docs(docs: list[dict]) -> np.ndarray:
    """Oblicza embeddingi dla wszystkich dokumentów."""
    n = len(docs)
    embeddings = np.zeros((n, N_OSCILLATORS), dtype=np.float64)
    log.info("Computing embeddings for %d docs...", n)

    t0 = time.time()
    for i, doc in enumerate(docs):
        terms = _load_tfidf(doc["idx"])
        phi = _doc_to_phi(doc, terms, seed=42)
        embeddings[i] = phi
        if (i + 1) % 100 == 0:
            elapsed = time.time() - t0
            rate = (i + 1) / elapsed if elapsed > 0 else 0
            log.info("  %d/%d docs (%.1f/s)", i + 1, n, rate)

    elapsed = time.time() - t0
    log.info("Embedded %d docs in %.1fs (%.1f/s)", n, elapsed, n / elapsed if elapsed > 0 else 0)
    return embeddings


def _build_index(docs: list[dict], embeddings: np.ndarray) -> dict:
    """Buduje JSON index: doc → filename + phi + metryki."""
    entries = []
    for i, doc in enumerate(docs):
        phi = embeddings[i].tolist()
        R_ch = []
        for ch in range(N_CHANNELS):
            s = ch * OSC_PER_CHANNEL
            e = s + OSC_PER_CHANNEL
            ch_phi = phi[s:e]
            ch_R = abs(sum(math.e ** (1j * p) for p in ch_phi)) / OSC_PER_CHANNEL
            R_ch.append(round(ch_R, 4))
        entries.append({
            "idx": doc["idx"],
            "filename": doc["filename"],
            "phi": [round(p, 6) for p in phi],
            "R_channels": R_ch,
            "R_global": round(abs(sum(math.e ** (1j * p) for p in phi)) / N_OSCILLATORS, 4),
            "themes": doc.get("themes", "")[:200],
            "affect": doc.get("affect", "")[:200],
            "essence": doc.get("essence", "")[:500],
        })
    return {
        "n_docs": len(entries),
        "n_dimensions": N_OSCILLATORS,
        "channels": list(CHANNEL_KEYWORDS.keys()),
        "schema": "noema/knowledge/embedding/v0.1",
        "entries": entries,
    }


def save(embeddings: np.ndarray, index: dict) -> None:
    """Zapisuje embeddingi numpy + JSON index."""
    OUTPUT_NPY.parent.mkdir(parents=True, exist_ok=True)
    np.save(str(OUTPUT_NPY), embeddings)
    log.info("Saved embeddings: %s (%s)", OUTPUT_NPY, embeddings.shape)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(index, f, indent=1)
    log.info("Saved index: %s (%d entries)", OUTPUT_JSON, len(index["entries"]))


def load() -> tuple[np.ndarray, dict]:
    """Ładuje istniejące embeddingi. Zwraca (embeddings, index)."""
    if not OUTPUT_NPY.exists() or not OUTPUT_JSON.exists():
        return np.array([]), {}
    embeddings = np.load(str(OUTPUT_NPY))
    with open(OUTPUT_JSON) as f:
        index = json.load(f)
    return embeddings, index


def query(query_text: str, embeddings: np.ndarray, index: dict, top_k: int = 10) -> list[dict]:
    """Query: tekst → 36D → nearest neighbors (cosine similarity)."""
    # Prosta embedding query: aggregate TF-IDF z query
    query_terms = query_text.lower().split()
    term_weights = {t: 1.0 for t in query_terms}

    doc_idx = {e["idx"]: i for i, e in enumerate(index["entries"])}
    # Query embedding jako średnia wag kanałów z termów query
    q_w = _compute_channel_weights(term_weights)
    q_phi = np.zeros(N_OSCILLATORS, dtype=np.float64)
    for ch in range(N_CHANNELS):
        for osc in range(OSC_PER_CHANNEL):
            phase_shift = osc * (2.0 * np.pi / 3.0)
            q_phi[ch * OSC_PER_CHANNEL + osc] = (q_w[ch] * np.pi + phase_shift) % (2.0 * np.pi)

    # Cosine similarity na sferze fazowej: cos(Δφ) średnie po oscylatorach
    n = len(index["entries"])
    scores = np.zeros(n, dtype=np.float64)
    for i in range(n):
        diff = np.angle(np.exp(1j * (embeddings[i] - q_phi)))
        scores[i] = float(np.mean(np.cos(diff)))

    top_idx = np.argsort(scores)[::-1][:top_k]
    results = []
    for i in top_idx:
        entry = index["entries"][i]
        results.append({
            "rank": len(results) + 1,
            "idx": entry["idx"],
            "filename": entry["filename"],
            "similarity": round(float(scores[i]), 4),
            "R_global": entry.get("R_global", 0),
            "essence": entry.get("essence", "")[:300],
        })
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description="CIELingo Document Embedder — 36D PhaseNav embeddings")
    ap.add_argument("--rebuild", action="store_true", help="Force rebuild embeddings")
    ap.add_argument("--query", type=str, default=None, help="Query text for similarity search")
    ap.add_argument("--top-k", type=int, default=10, help="Number of results (default: 10)")
    ap.add_argument("--stats", action="store_true", help="Show embedding statistics")
    args = ap.parse_args()

    # Eksplicitny rebuild lub brak plików
    need_rebuild = args.rebuild
    if need_rebuild or not OUTPUT_NPY.exists():
        docs, _ = _load_kb()
        if not docs:
            log.error("No docs loaded")
            return 1
        embeddings = _embed_docs(docs)
        index = _build_index(docs, embeddings)
        save(embeddings, index)
    else:
        embeddings, index = load()
        log.info("Loaded %d existing embeddings", len(index.get("entries", [])))
        if not embeddings.size:
            docs, _ = _load_kb()
            if not docs:
                return 1
            embeddings = _embed_docs(docs)
            index = _build_index(docs, embeddings)
            save(embeddings, index)

    if args.stats:
        R_globals = [e.get("R_global", 0) for e in index["entries"]]
        print(f"\n=== Embedding stats ===")
        print(f"  Documents: {len(index['entries'])}")
        print(f"  Dimensions: {index['n_dimensions']} (12 ch × 3 osc)")
        print(f"  Mean R: {np.mean(R_globals):.4f}")
        print(f"  Min R: {np.min(R_globals):.4f}")
        print(f"  Max R: {np.max(R_globals):.4f}")
        channels = index.get("channels", [])
        for ch_idx, ch_name in enumerate(channels):
            ch_Rs = [e["R_channels"][ch_idx] for e in index["entries"]]
            print(f"    {ch_name:20s} mean_R={np.mean(ch_Rs):.4f}")

    if args.query:
        results = query(args.query, embeddings, index, top_k=args.top_k)
        print(f"\n=== Query: '{args.query}' ===")
        for r in results:
            print(f"  #{r['rank']:2d} sim={r['similarity']:.4f}  {r['filename'][:50]}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
