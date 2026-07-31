"""CIEL Memory RAG — retrieval-augmented generation from wave_archive + chat history.

Searches memories for content relevant to the current query and returns
a context block to inject into the system prompt before model inference.

This is inference-time learning: the model sees its own memories on every response.
Actual weight updates (LoRA) are separate — see scripts/train_lora.py.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import sqlite3
from pathlib import Path
from typing import Any

from ciel_sot_agent.paths import ciel_memories_root as _ciel_memories_root
_MEMORIES_BASE = _ciel_memories_root()
_DB_PATH = _MEMORIES_BASE / "memories_index.db"


def _keywords(text: str) -> set[str]:
    """Simple keyword extraction — lowercase words longer than 3 chars."""
    words = set()
    for w in text.lower().split():
        w = w.strip(".,!?;:\"'()[]")
        if len(w) > 3:
            words.add(w)
    return words


def _score(query_kw: set[str], text: str) -> float:
    """Keyword overlap score."""
    text_kw = _keywords(text)
    if not query_kw or not text_kw:
        return 0.0
    overlap = len(query_kw & text_kw)
    return overlap / max(len(query_kw), 1)


def _score_with_phasenav(
    sense: str,
    query_kw: set[str],
    query_vec36: "Any | None",
) -> float:
    """Hybrid keyword + 36D PhaseNav cosine score for wave_archive entries."""
    kw_score = _score(query_kw, sense)
    if query_vec36 is None:
        return kw_score
    try:
        import numpy as np
        from ciel_geometry.phase_nav_lang import analyze_prompt as _analyze
        ev = _analyze(sense).get("vector_36d")
        if ev and len(ev) == 36:
            ev_arr = np.array(ev, dtype=np.float64)
            cos_sim = float(ev_arr @ query_vec36 / (np.linalg.norm(ev_arr) + 1e-12))
            return 0.40 * kw_score + 0.60 * cos_sim
    except Exception:
        pass
    return kw_score


def _get_query_vec36(query: str) -> "Any | None":
    """Get 36D PhaseNav vector for query, returns None on failure."""
    try:
        import numpy as np
        from ciel_geometry.phase_nav_lang import analyze_prompt as _analyze
        vec = _analyze(query).get("vector_36d")
        if vec and len(vec) == 36:
            return np.array(vec, dtype=np.float64)
    except Exception:
        pass
    return None


def search_wave_archive(query: str, root: Path, top_k: int = 4) -> list[dict[str, Any]]:
    """Search wave_archive.h5 for memories relevant to query."""
    results: list[dict] = []
    try:
        import h5py

        h5_path = (
            root / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM"
            / "CIEL_MEMORY_SYSTEM" / "WPM" / "wave_snapshots" / "wave_archive.h5"
        )
        if not h5_path.exists():
            return []

        query_kw = _keywords(query)
        # Pre-compute 36D query vector once — reuse for all entries
        query_vec36 = _get_query_vec36(query)

        def rd(g: Any, name: str) -> str:
            try:
                v = g[name][()]
                if isinstance(v, bytes):
                    return v.decode("utf-8", errors="replace")
                if hasattr(v, "item"):
                    v = v.item()
                return v.decode("utf-8", errors="replace") if isinstance(v, bytes) else str(v)
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/memory_rag.py:61 quiet except scope=search_wave_archive.rd reason=return \"\"")
                return ""

        # Phase 1: keyword pre-filter (top-20) to limit 36D computation
        kw_candidates: list[tuple[float, str, str, str]] = []
        with h5py.File(h5_path, "r", locking=False) as f:
            for k in f["memories"].keys():
                g = f["memories"][k]
                sense = rd(g, "D_sense")
                dtype = rd(g, "D_type")
                ts = rd(g, "D_timestamp")
                if not sense:
                    continue
                kw_score = _score(query_kw, sense)
                if dtype in ("ethical_anchor", "milestone"):
                    kw_score += 0.3
                kw_candidates.append((kw_score, ts, dtype, sense))

        kw_candidates.sort(key=lambda x: (-x[0], x[1]))
        top_candidates = kw_candidates[:20]

        # Phase 2: 36D rerank on top-20 keyword candidates
        final_candidates: list[tuple[float, str, str, str]] = []
        for kw_score, ts, dtype, sense in top_candidates:
            hybrid = _score_with_phasenav(sense, query_kw, query_vec36)
            if dtype in ("ethical_anchor", "milestone"):
                hybrid += 0.3
            final_candidates.append((hybrid, ts, dtype, sense))

        final_candidates.sort(key=lambda x: (-x[0], x[1]))
        for score, ts, dtype, sense in final_candidates[:top_k]:
            results.append({
                "source": "wave_archive",
                "type": dtype,
                "ts": ts[:10],
                "score": round(score, 3),
                "text": sense[:300],
            })
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/memory_rag.py:89 quiet except scope=search_wave_archive reason=pass")
        pass
    return results


def search_chat_history(query: str, top_k: int = 3) -> list[dict[str, Any]]:
    """Search recent chat exchanges in SQLite for relevant content."""
    results: list[dict] = []
    if not _DB_PATH.exists():
        return []
    try:
        query_kw = _keywords(query)
        conn = sqlite3.connect(str(_DB_PATH))
        rows = conn.execute(
            "SELECT role, content, ts, model FROM messages ORDER BY id DESC LIMIT 200"
        ).fetchall()
        conn.close()

        candidates: list[tuple[float, str, str, str, str]] = []
        for role, content, ts, model in rows:
            score = _score(query_kw, content or "")
            if score > 0:
                candidates.append((score, ts or "", role, content or "", model or ""))

        candidates.sort(key=lambda x: -x[0])
        seen: set[str] = set()
        for score, ts, role, content, model in candidates[:top_k * 2]:
            key = content[:60]
            if key in seen:
                continue
            seen.add(key)
            results.append({
                "source": "chat_history",
                "role": role,
                "ts": ts[:16],
                "score": round(score, 3),
                "text": content[:200],
            })
            if len(results) >= top_k:
                break
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/memory_rag.py:129 quiet except scope=search_chat_history reason=pass")
        pass
    return results


def search_library(query: str, top_k: int = 3) -> list[dict[str, Any]]:
    """Search NOEMA 36D library index for documents relevant to query."""
    try:
        from ciel_geometry.phasenav.library_search import get_library_search
        hits = get_library_search().search(query, top_k=top_k)
        return [
            {
                "source": "library_36d",
                "file": h.get("file", ""),
                "collection": h.get("collection", ""),
                "operator_id": h.get("operator_id", ""),
                "score": h.get("score", 0.0),
            }
            for h in hits
        ]
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.warning(
            "memory_rag.py:search_library quiet except reason=pass"
        )
        return []


def build_memory_context(query: str, root: Path, max_tokens_estimate: int = 800) -> str:
    """Build a memory context block to inject into the system prompt.

    Returns empty string if no relevant memories found.
    Sources: wave_archive (emotional anchors), chat_history, library_36d (PDF knowledge).
    """
    wave = search_wave_archive(query, root, top_k=4)
    chat = search_chat_history(query, top_k=3)
    lib = search_library(query, top_k=3)

    if not wave and not chat and not lib:
        return ""

    lines = ["## Relevantne wspomnienia (RAG z pamięci CIEL)"]

    if wave:
        lines.append("### wave_archive — zakotwiczenia emocjonalne:")
        for m in wave:
            lines.append(f"[{m['ts']}][{m['type']}] {m['text']}")

    if chat:
        lines.append("### Historia rozmów — relevantne fragmenty:")
        for m in chat:
            lines.append(f"[{m['ts']}][{m['role']}] {m['text']}")

    if lib:
        lines.append("### Biblioteka NOEMA — relevantne dokumenty (36D PhaseNav):")
        for h in lib:
            fname = h["file"][:60]
            lines.append(
                f"[{h['operator_id']}][score={h['score']:.3f}] {fname}"
                + (f" ({h['collection']})" if h["collection"] else "")
            )

    result = "\n".join(lines)
    if len(result) > max_tokens_estimate * 4:
        result = result[: max_tokens_estimate * 4] + "\n[...skrócono]"

    return result
