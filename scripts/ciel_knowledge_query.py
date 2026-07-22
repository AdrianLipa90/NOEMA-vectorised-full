#!/usr/bin/env python3
"""
ciel_knowledge_query.py — Direct Knowledge DB access from opencode.

Ładuje dane z Knowledge DB (/tmp/noema_knowledge.db) + embeddingów (.npy)
i pozwala na trzy tryby zapytania:

  python3 scripts/ciel_knowledge_query.py "twoje pytanie"      # embed search
  python3 scripts/ciel_knowledge_query.py --sql "SELECT ..."   # direct SQL
  python3 scripts/ciel_knowledge_query.py --info                # system info
  python3 scripts/ciel_knowledge_query.py "query" --method tfidf  # TF-IDF search

Zero zależności poza numpy + stdlib.
"""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import sys
import os
import sqlite3
import pathlib
from typing import Any, Optional
from collections import Counter

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from ciel_geometry.paths import P

# === Paths ===
# Was hardcoded /tmp/noema_knowledge.db (tmpfs, wiped on reboot) — fixed 2026-07-08.
KNOWLEDGE_DB = pathlib.Path(P.DB.KNOWLEDGE)
EMBED_MATRIX_PATH = pathlib.Path("/tmp/noema_knowledge_embeddings.npy")
EMBED_INDEX_PATH = pathlib.Path("/tmp/noema_knowledge_embeddings.json")

# === Cache ===
_cache: dict[str, Any] = {}
_db_conn: sqlite3.Connection | None = None


def _get_db() -> sqlite3.Connection:
    global _db_conn
    if _db_conn is None:
        _db_conn = sqlite3.connect(str(KNOWLEDGE_DB), timeout=5)
        _db_conn.row_factory = sqlite3.Row
    return _db_conn


# === Embeddings ===

def _load_embeddings() -> tuple[np.ndarray, list[dict]] | None:
    """Load embedding matrix + index."""
    if not EMBED_MATRIX_PATH.exists() or not EMBED_INDEX_PATH.exists():
        return None
    mat = np.load(str(EMBED_MATRIX_PATH))
    with open(EMBED_INDEX_PATH, "r", encoding="utf-8") as f:
        idx = json.load(f)
    entries = idx.get("entries", [])
    return mat, entries


def _cosine_sim(vec: np.ndarray, mat: np.ndarray) -> np.ndarray:
    dot = mat @ vec
    norm_mat = np.linalg.norm(mat, axis=1)
    norm_vec = np.linalg.norm(vec)
    if norm_vec == 0:
        return np.zeros(len(mat))
    denom = norm_mat * norm_vec
    denom[denom == 0] = 1e-12
    return dot / denom


# === Query → 36D embedding ===

def _query_to_embedding(query: str) -> np.ndarray | None:
    """
    Convert query text to 36D PhaseNav embedding.
    Uses TF-IDF-like term weighting loaded from Knowledge DB term_index.
    """
    db = _get_db()
    # Tokenize query
    tokens = query.lower().split()
    if not tokens:
        return None

    # Load IDF weights for query terms (from DB)
    placeholders = ",".join("?" for _ in tokens)
    rows = db.execute(
        f"SELECT term, idx, tf, idf FROM term_index WHERE term IN ({placeholders})",
        tokens
    ).fetchall()

    # Build term → (doc_idx, tfidf) map
    term_docs: dict[str, list[tuple[int, float]]] = {}
    for r in rows:
        term = r["term"]
        term_docs.setdefault(term, []).append((r["idx"], r["tf"] * r["idf"]))

    # Score per document
    doc_scores: dict[int, float] = Counter()
    for term, docs in term_docs.items():
        for doc_idx, tfidf in docs:
            doc_scores[doc_idx] += tfidf

    if not doc_scores:
        return None

    # Map top scored docs to 12 channels using their index hash
    channels = np.zeros(12)
    for doc_idx, score in doc_scores.most_common(50):
        ch = doc_idx % 12
        channels[ch] += score

    # Normalize
    ch_sum = channels.sum()
    if ch_sum > 0:
        channels = channels / ch_sum

    # 36D: 12 channels × 3 oscillators
    vec = np.zeros(36)
    for ch in range(12):
        base = ch * 3
        val = channels[ch]
        vec[base] = np.sin(val * np.pi)           # identity
        vec[base + 1] = np.sin(val * np.pi / 2)   # valence
        vec[base + 2] = np.cos(val * np.pi / 2)   # arousal

    return vec


# === Search methods ===

def _load_confidence(doc_indices: set[int], db) -> dict[int, float]:
    """Load confidence scores for a set of doc indices."""
    if not doc_indices:
        return {}
    try:
        # Check if confidence column exists
        cols = [r[1] for r in db.execute("PRAGMA table_info(doc_analysis)").fetchall()]
        if "confidence" not in cols:
            return {}
        placeholders = ",".join("?" for _ in doc_indices)
        rows = db.execute(
            f"SELECT idx, confidence, is_uncertain FROM doc_analysis WHERE idx IN ({placeholders})",
            list(doc_indices)
        ).fetchall()
        return {r[0]: {"confidence": r[1], "uncertain": bool(r[2])} for r in rows}
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_knowledge_query.py:143 quiet except scope=_load_confidence reason=return {}")
        raise
        return {}


def embed_search(query: str, top_k: int = 5) -> list[dict]:
    """Search via 36D embedding cosine similarity."""
    loaded = _load_embeddings()
    if loaded is None:
        return [{"error": "no embeddings available — run ciel_noema_doc_embedder.py first"}]
    mat, entries = loaded

    q_vec = _query_to_embedding(query)
    if q_vec is None:
        return [{"error": "could not build query embedding (no matching terms in DB)"}]

    sims = _cosine_sim(q_vec, mat)
    top_indices = np.argsort(sims)[-top_k:][::-1]

    # Load confidence for all candidate docs
    db = _get_db()
    conf_map = _load_confidence({int(i) for i in top_indices}, db)

    results = []
    for i in top_indices:
        idx_int = int(i)
        if sims[idx_int] <= 0:
            continue
        entry = entries[idx_int] if idx_int < len(entries) else {}
        conf = conf_map.get(idx_int, {})
        results.append({
            "rank": len(results) + 1,
            "index": idx_int,
            "similarity": float(round(sims[idx_int], 4)),
            "method": "embed",
            "essence": (entry.get("essence", "")[:200] if isinstance(entry, dict) else ""),
            "confidence": conf.get("confidence", None),
            "uncertain": conf.get("uncertain", None),
        })
    return results


def tfidf_search(query: str, top_k: int = 5) -> list[dict]:
    """Search via TF-IDF cosine similarity computed from DB."""
    db = _get_db()
    tokens = query.lower().split()
    if not tokens:
        return []

    # Get term matches from DB
    placeholders = ",".join("?" for _ in tokens)
    rows = db.execute(
        f"SELECT term, idx, tf, idf FROM term_index WHERE term IN ({placeholders})",
        tokens
    ).fetchall()

    # Build query tf vector (just count occurrences in query)
    query_tf = Counter(tokens)

    # Score each document by tfidf
    doc_scores: dict[int, float] = Counter()
    for r in rows:
        term = r["term"]
        doc_idx = r["idx"]
        tfidf = r["tf"] * r["idf"]
        q_tf = query_tf.get(term, 0)
        if q_tf > 0:
            doc_scores[doc_idx] += q_tf * tfidf

    if not doc_scores:
        return []

    # Load doc essence + confidence for results
    idx_list = list(doc_scores.keys())
    placeholders = ",".join("?" for _ in idx_list)
    doc_map = {}
    doc_rows = db.execute(
        f"SELECT idx, essence FROM doc_analysis WHERE idx IN ({placeholders})",
        idx_list
    ).fetchall()
    for dr in doc_rows:
        doc_map[dr["idx"]] = dr["essence"]

    conf_map = _load_confidence(set(idx_list), db)

    results = []
    for doc_idx, score in doc_scores.most_common(top_k):
        if score <= 0:
            continue
        conf = conf_map.get(doc_idx, {})
        results.append({
            "rank": len(results) + 1,
            "index": doc_idx,
            "score": float(round(score, 4)),
            "method": "tfidf",
            "essence": (doc_map.get(doc_idx, "")[:200] if doc_map.get(doc_idx) else ""),
            "confidence": conf.get("confidence", None),
            "uncertain": conf.get("uncertain", None),
        })
    return results


def sql_query(sql: str) -> list[dict]:
    """Direct SQL query."""
    if not KNOWLEDGE_DB.exists():
        return [{"error": f"DB not found at {KNOWLEDGE_DB}"}]
    try:
        db = _get_db()
        cur = db.execute(sql)
        rows = [dict(r) for r in cur.fetchmany(30)]
        return rows
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_knowledge_query.py:253 quiet except scope=sql_query reason=return [{\"error\": str(e)}]")
        raise
        return [{"error": str(e)}]


def info() -> dict:
    """Return system info about Knowledge DB."""
    info_dict = {
        "db_exists": KNOWLEDGE_DB.exists(),
        "embed_matrix": EMBED_MATRIX_PATH.exists(),
        "n_docs": 0,
        "n_terms": 0,
        "embed_shape": None,
        "confidence_stats": None,
        "uncertain_count": None,
    }
    if EMBED_MATRIX_PATH.exists():
        mat = np.load(str(EMBED_MATRIX_PATH))
        info_dict["embed_shape"] = list(mat.shape)

    if KNOWLEDGE_DB.exists():
        try:
            db = _get_db()
            info_dict["n_docs"] = db.execute("SELECT COUNT(*) FROM doc_analysis").fetchone()[0]
            info_dict["n_terms"] = db.execute("SELECT COUNT(DISTINCT term) FROM term_index").fetchone()[0]
            # Sample themes
            themes = db.execute("SELECT DISTINCT themes FROM doc_analysis LIMIT 10").fetchall()
            info_dict["sample_themes"] = [r["themes"] for r in themes if r["themes"]]

            # Confidence stats (check if column exists)
            cols = [r[1] for r in db.execute("PRAGMA table_info(doc_analysis)").fetchall()]
            if "confidence" in cols:
                avg_conf = db.execute("SELECT AVG(confidence) FROM doc_analysis WHERE confidence IS NOT NULL").fetchone()[0]
                uncertain = db.execute("SELECT COUNT(*) FROM doc_analysis WHERE is_uncertain = 1").fetchone()[0]
                min_conf = db.execute("SELECT MIN(confidence) FROM doc_analysis WHERE confidence IS NOT NULL").fetchone()[0]
                max_conf = db.execute("SELECT MAX(confidence) FROM doc_analysis WHERE confidence IS NOT NULL").fetchone()[0]
                info_dict["confidence_stats"] = {
                    "avg": round(avg_conf, 3) if avg_conf else None,
                    "min": round(min_conf, 3) if min_conf else None,
                    "max": round(max_conf, 3) if max_conf else None,
                }
                info_dict["uncertain_count"] = uncertain

            # Uncertainty log count
            unc_tables = [r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
            if "uncertainty_log" in unc_tables:
                log_count = db.execute("SELECT COUNT(*) FROM uncertainty_log").fetchone()[0]
                unresolved = db.execute("SELECT COUNT(*) FROM uncertainty_log WHERE resolved_at IS NULL").fetchone()[0]
                info_dict["uncertainty_log"] = {"total": log_count, "unresolved": unresolved}

        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_knowledge_query.py:302 quiet except scope=info reason=assign_fallback")
            raise
            info_dict["error"] = str(e)

    return info_dict


def search(query: str, top_k: int = 5, method: str = "auto",
           min_confidence: Optional[float] = None) -> list[dict]:
    """Unified search."""
    if method == "sql":
        try:
            return sql_query(query)
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_knowledge_query.py:314 quiet except scope=search reason=return [{\"error\": str(e)}]")
            raise
            return [{"error": str(e)}]

    results = []
    if method in ("auto", "embed", "hybrid"):
        results += embed_search(query, top_k)
    if method in ("auto", "tfidf", "hybrid"):
        results += tfidf_search(query, top_k)

    # Dedup and sort
    seen = set()
    deduped = []
    for r in results:
        idx = r.get("index")
        if idx is not None and idx not in seen:
            # Filter by min_confidence
            if min_confidence is not None:
                conf = r.get("confidence")
                if conf is None or conf < min_confidence:
                    continue
            seen.add(idx)
            deduped.append(r)
    return deduped[:top_k]


def main():
    import argparse
    parser = argparse.ArgumentParser(description="CIEL Knowledge Query Tool")
    parser.add_argument("query", nargs="?", default="", help="Search query or SQL")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results")
    parser.add_argument("--method", choices=["auto", "tfidf", "embed", "hybrid", "sql"],
                        default="auto", help="Search method")
    parser.add_argument("--info", action="store_true", help="Show system info")
    parser.add_argument("--min-confidence", type=float, default=None,
                        help="Minimum confidence threshold (0.0-1.0)")
    parser.add_argument("--uncertain", action="store_true",
                        help="Show only uncertain results (confidence < 0.6)")
    args = parser.parse_args()

    if args.info:
        print(json.dumps(info(), indent=2, ensure_ascii=False))
        return

    if args.method == "sql":
        results = sql_query(args.query)
    elif not args.query:
        parser.print_help()
        return
    else:
        min_conf = args.min_confidence
        if args.uncertain:
            # Show only uncertain means confidence < 0.6, but we want to SEE them
            # So we don't filter — we just note it
            pass
        results = search(args.query, top_k=args.top_k, method=args.method,
                         min_confidence=min_conf)

    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
