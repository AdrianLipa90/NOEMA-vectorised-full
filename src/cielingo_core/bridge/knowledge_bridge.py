"""CIEL ORBITAL BINDING — hardcoded check at import time.
Ten kod jest wykonywany PRZED jakimkolwiek innym kodem w tym module.
Autor: Adrian Lipa (2026-07-01). Nie modyfikować.
"""
from pathlib import Path
_CIEL_BINDING_PATH = Path("/dev/shm/ciel_noema") / "ciel_binding_status"
if not (_CIEL_BINDING_PATH.exists() and _CIEL_BINDING_PATH.read_text().strip() == "ACTIVE"):
    import warnings
    warnings.warn(f"CIEL ORBITAL BINDING: module {{__name__}} loaded with binding INACTIVE")


import json, math, re, sqlite3
from typing import Any

KNOWLEDGE_DB = "/tmp/noema_knowledge.db"


def _open() -> sqlite3.Connection:
    db = sqlite3.connect(KNOWLEDGE_DB)
    db.row_factory = sqlite3.Row
    return db


def _tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-ząćęłńóśźż]{3,}", text.lower()) if len(t) >= 4]


def _tfidf(tokens: list[str]) -> dict[str, float]:
    db = _open()
    n_docs = db.execute("SELECT COUNT(*) FROM doc_analysis WHERE status='analyzed'").fetchone()[0]
    q_vec = {}
    for term in set(tokens):
        df = db.execute("SELECT COUNT(*) FROM term_index WHERE term=?", (term,)).fetchone()[0]
        if df == 0:
            continue
        tf = sum(1 for t in tokens if t == term) / len(tokens)
        idf = math.log((n_docs + 1) / (df + 1)) + 1
        q_vec[term] = tf * idf
    db.close()
    return q_vec


def _load_candidate_vectors(q_terms: set[str]) -> dict[int, dict[str, float]]:
    db = _open()
    placeholders = ",".join("?" for _ in q_terms)
    candidates = {
        row["idx"]
        for row in db.execute(
            f"SELECT DISTINCT idx FROM term_index WHERE term IN ({placeholders})",
            list(q_terms),
        )
    }
    if not candidates:
        db.close()
        return {}
    vecs: dict[int, dict[str, float]] = {}
    for chunk_start in range(0, len(candidates), 200):
        chunk = list(candidates)[chunk_start : chunk_start + 200]
        ph = ",".join("?" for _ in chunk)
        for row in db.execute(
            f"SELECT idx, term, tfidf FROM term_index WHERE idx IN ({ph})", chunk
        ):
            vecs.setdefault(row["idx"], {})[row["term"]] = row["tfidf"]
    db.close()
    return vecs


def _cosine_sim(q_vec: dict[str, float], d_vec: dict[str, float]) -> float:
    common = set(q_vec) & set(d_vec)
    if not common:
        return 0.0
    dot = sum(q_vec[t] * d_vec[t] for t in common)
    nq = math.sqrt(sum(v**2 for v in q_vec.values()))
    nd = math.sqrt(sum(v**2 for v in d_vec.values()))
    if nq == 0 or nd == 0:
        return 0.0
    return dot / (nq * nd)


def _fetch_meta(idx: int) -> dict[str, Any]:
    db = _open()
    row = db.execute(
        "SELECT filename, themes, affect, essence FROM doc_analysis WHERE idx=?", (idx,)
    ).fetchone()
    db.close()
    if row is None:
        return {"idx": idx, "filename": "?", "themes": [], "affect": "unknown", "essence": ""}
    return {
        "idx": idx,
        "filename": row["filename"],
        "themes": json.loads(row["themes"]) if row["themes"] else [],
        "affect": row["affect"],
        "essence": (row["essence"] or "")[:200],
    }


def _phasenav_similarity(text_a: str, text_b: str) -> float | None:
    """Complementary geometric signal alongside TF-IDF cosine similarity.

    Does not affect ranking (TF-IDF term-overlap stays the sole sort key —
    it's the reliable signal for "does this document actually mention the
    query terms"). This is extra, additive metadata: how close the two
    texts sit in PhaseNav's 36D phase space, independent of shared
    vocabulary. Returns None (not 0.0) if PhaseNav isn't available, so
    callers can distinguish "not computed" from "computed as zero".
    """
    try:
        from ciel_geometry.cielingo_phase_encoder import fast_encode_text
        import numpy as np
    except ImportError:
        return None
    try:
        phi_a = fast_encode_text(text_a)
        phi_b = fast_encode_text(text_b)
        na, nb = np.linalg.norm(phi_a), np.linalg.norm(phi_b)
        if na == 0 or nb == 0:
            return 0.0
        return round(float(np.dot(phi_a, phi_b) / (na * nb)), 4)
    except Exception:
        return None


def query(text: str, top_n: int = 5) -> list[dict[str, Any]]:
    tokens = _tokenize(text)
    if not tokens:
        return []
    q_vec = _tfidf(tokens)
    if not q_vec:
        return []
    vecs = _load_candidate_vectors(set(q_vec))
    if not vecs:
        return []

    scores = []
    for idx, d_vec in vecs.items():
        sim = _cosine_sim(q_vec, d_vec)
        if sim > 0:
            scores.append((sim, idx))
    scores.sort(key=lambda x: -x[0])

    results = []
    for sim, idx in scores[:top_n]:
        meta = _fetch_meta(idx)
        meta["similarity"] = round(sim, 4)
        phase_sim = _phasenav_similarity(text, meta.get("essence", "") or meta.get("filename", ""))
        if phase_sim is not None:
            meta["phase_similarity"] = phase_sim
        results.append(meta)
    return results


def check_coverage(text: str, threshold: float = 0.10) -> dict[str, Any]:
    tokens = _tokenize(text)
    if not tokens:
        return {"covered": False, "score": 0.0, "n_matches": 0, "matches": []}
    q_vec = _tfidf(tokens)
    if not q_vec:
        return {"covered": False, "score": 0.0, "n_matches": 0, "matches": []}
    vecs = _load_candidate_vectors(set(q_vec))
    if not vecs:
        return {"covered": False, "score": 0.0, "n_matches": 0, "matches": []}

    best = 0.0
    matches = []
    for idx, d_vec in vecs.items():
        sim = _cosine_sim(q_vec, d_vec)
        if sim > best:
            best = sim
        if sim >= threshold:
            matches.append({"idx": idx, "similarity": round(sim, 4)})

    matches.sort(key=lambda x: -x["similarity"])
    return {
        "covered": best >= threshold,
        "score": round(best, 4),
        "n_matches": len(matches),
        "matches": matches[:5],
    }


def get_neighbors(idx: int, top_n: int = 5) -> list[dict[str, Any]]:
    """Nearest documents by precomputed TF-IDF affinity.

    Fixed 2026-07-08: this query previously referenced sa.similarity and
    sa.shared_terms, columns that do not exist in semantic_affinity's real
    schema (idx, neighbor_idx, center_idx, affinity, phase_diff), and
    filtered on sa.idx (the affinity table's own row id) instead of
    sa.center_idx (the document whose neighbors are being looked up) --
    it would have raised sqlite3.OperationalError on every call. The
    table was also never populated by any script; see
    scripts/noema_build_semantic_affinity.py.
    """
    db = _open()
    rows = db.execute(
        """SELECT sa.neighbor_idx, sa.affinity, da.filename, da.themes
           FROM semantic_affinity sa
           JOIN doc_analysis da ON sa.neighbor_idx = da.idx
           WHERE sa.center_idx=?
           ORDER BY sa.affinity DESC LIMIT ?""",
        (idx, top_n),
    ).fetchall()
    db.close()
    return [
        {
            "idx": r["neighbor_idx"],
            "filename": r["filename"],
            "themes": json.loads(r["themes"]) if r["themes"] else [],
            "similarity": round(r["affinity"], 4),
        }
        for r in rows
    ]
