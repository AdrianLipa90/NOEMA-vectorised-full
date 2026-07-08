#!/usr/bin/env python3
"""CIELingo Phase Memory — asocjacyjna pamięć fazowa dla modelu językowego.

Architektura:
  (text, φ_36) pary przechowywane w numpy array
  Szybkie wyszukiwanie przez cos similarity w 36D
  Persistent storage przez JSON/NPZ
  Online learning: CIELingo sync daemon może dodawać nowe pary

Usage:
    from ciel_geometry.cielingo_phase_memory import PhaseMemory
    pm = PhaseMemory.load_or_create("/tmp/cielingo_phase_memory.npz")
    pm.add("Przykładowy tekst", phi_36)
    results = pm.query(phi_query, k=5)
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import time
from pathlib import Path
from typing import Any

import numpy as np

log = logging.getLogger(__name__)


class PhaseMemory:
    """Asocjacyjna pamięć fazowa: text ↔ 36D φ.

    Atrybuty:
        vectors: np.ndarray (n, 36) — wszystkie zakodowane fazy
        texts: list[str] — teksty w tej samej kolejności
        metadata: list[dict] — metadane (timestamp, source, token_count, etc.)
        max_size: int — maksymalna liczba wpisów (FIFO eviction)
    """

    def __init__(self, max_size: int = 10000):
        self.vectors: np.ndarray = np.zeros((0, 36), dtype=np.float64)
        self.texts: list[str] = []
        self.metadata: list[dict[str, Any]] = []
        self.max_size = max_size
        self._hash_index: dict[str, int] = {}  # text_hash → index (dla dedup)

    # ── Persistence ─────────────────────────────────────────────────

    def save(self, path: str | Path) -> None:
        """Zapisz pamięć do pliku NPZ + JSON."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        # NPZ dla wektorów
        npz_path = path.with_suffix(".npz")
        np.savez_compressed(npz_path, vectors=self.vectors)

        # JSON dla tekstów i metadanych
        json_path = path.with_suffix(".json")
        data = {
            "texts": self.texts,
            "metadata": self.metadata,
            "max_size": self.max_size,
            "saved_at": time.time(),
            "n_entries": len(self.texts),
        }
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        log.info("PhaseMemory saved: %d entries → %s", len(self.texts), path)

    @classmethod
    def load_or_create(cls, path: str | Path, max_size: int = 10000) -> "PhaseMemory":
        """Załaduj z pliku lub stwórz nową."""
        path = Path(path)
        npz_path = path.with_suffix(".npz")
        json_path = path.with_suffix(".json")

        if npz_path.exists() and json_path.exists():
            try:
                return cls._load(npz_path, json_path)
            except Exception as e:
                log.warning("Failed to load PhaseMemory: %s — creating new", e)

        log.info("Creating new PhaseMemory at %s", path)
        return cls(max_size=max_size)

    @classmethod
    def _load(cls, npz_path: Path, json_path: Path) -> "PhaseMemory":
        """Wczytaj z dysku."""
        npz = np.load(npz_path)
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        pm = cls(max_size=data.get("max_size", 10000))
        pm.vectors = npz["vectors"]
        pm.texts = data["texts"]
        pm.metadata = data.get("metadata", [{} for _ in range(len(pm.texts))])

        # Rebuild hash index
        for i, t in enumerate(pm.texts):
            h = hashlib.sha256(t.encode()).hexdigest()[:16]
            pm._hash_index[h] = i

        log.info("PhaseMemory loaded: %d entries", len(pm.texts))
        return pm

    # ── Add / Update ────────────────────────────────────────────────

    def add(
        self,
        text: str,
        phi: np.ndarray,
        *,
        source: str = "cielingo",
        metadata: dict[str, Any] | None = None,
    ) -> int:
        """Dodaj nowy wpis. Zwraca index.

        Automatyczna deduplikacja: jeśli tekst już istnieje, aktualizuje fazę.
        Jeśli przekroczono max_size, usuwa najstarszy wpis (FIFO).
        """
        text_hash = hashlib.sha256(text.encode()).hexdigest()[:16]

        # Sprawdź duplikat
        if text_hash in self._hash_index:
            idx = self._hash_index[text_hash]
            self.vectors[idx] = phi
            if metadata:
                self.metadata[idx].update(metadata)
            return idx

        # Evict oldest if over limit
        while len(self.texts) >= self.max_size:
            self._evict_oldest()

        # Add new entry
        idx = len(self.texts)
        self.vectors = np.vstack([self.vectors, phi.reshape(1, -1)])
        self.texts.append(text)
        meta = metadata or {}
        meta.setdefault("timestamp", time.time())
        meta.setdefault("source", source)
        self.metadata.append(meta)
        self._hash_index[text_hash] = idx

        return idx

    def _evict_oldest(self) -> None:
        """FIFO eviction: usuń najstarszy wpis."""
        if len(self.texts) == 0:
            return
        removed_text = self.texts.pop(0)
        removed_hash = hashlib.sha256(removed_text.encode()).hexdigest()[:16]
        self._hash_index.pop(removed_hash, None)
        self.metadata.pop(0)
        self.vectors = self.vectors[1:]
        # Rebuild hash index (indices shifted)
        self._hash_index = {}
        for i, t in enumerate(self.texts):
            h = hashlib.sha256(t.encode()).hexdigest()[:16]
            self._hash_index[h] = i

    # ── Query ────────────────────────────────────────────────────────

    def query(
        self,
        phi: np.ndarray,
        k: int = 5,
        *,
        min_sim: float = 0.0,
        exclude_sources: set[str] | None = None,
    ) -> list[dict[str, Any]]:
        """Znajdź k najbliższych wpisów w 36D przestrzeni fazowej.

        Args:
            phi: (36,) wektor faz do zapytania
            k: liczba wyników
            min_sim: minimalne cos similarity do zwrócenia
            exclude_sources: metadata["source"] values to skip entirely before
                ranking — e.g. {"raw_logs"} to keep private session/chat log
                dumps (currently ~98% of entries) out of answers to factual
                questions, so the ~2% of real indexed documents (knowledge_db)
                aren't drowned out by nearest-neighbour noise.

        Returns:
            Lista dict: {text, sim, mean_phase, idx, metadata}
        """
        if len(self.texts) == 0:
            return []

        a = phi.reshape(1, -1)
        b = self.vectors
        # Cosine similarity on unit circles: cos(Δφ) averaged across 36 dims
        # For circular data: sim = mean(cos(φ_a - φ_b))
        cos_diff = np.cos(a - b)  # (1, 36) - (n, 36) = (n, 36)
        sims = np.mean(cos_diff, axis=1)  # (n,)

        if exclude_sources:
            mask = np.array([
                (self.metadata[i].get("source") if i < len(self.metadata) else None) not in exclude_sources
                for i in range(len(sims))
            ])
            candidate_idx = np.nonzero(mask)[0]
        else:
            candidate_idx = np.arange(len(sims))

        top_k = min(k, len(candidate_idx))
        if top_k == 0:
            return []
        order = np.argsort(-sims[candidate_idx])[:top_k]
        top_idx = candidate_idx[order]

        results = []
        for idx in top_idx:
            s = float(sims[idx])
            if s < min_sim:
                continue
            results.append({
                "text": self.texts[idx],
                "sim": s,
                "mean_phase": float(np.mean(self.vectors[idx])),
                "idx": int(idx),
                "metadata": self.metadata[idx] if idx < len(self.metadata) else {},
            })

        return results

    def query_by_text(
        self,
        text: str,
        k: int = 5,
        *,
        encoder_fn=None,
    ) -> list[dict[str, Any]]:
        """Znajdź wpisy podobne do podanego tekstu.

        Jeśli encoder_fn podany, enkoduje text → φ przed query.
        W przeciwnym razie szuka wprost po tekście (exact match + fuzzy).
        """
        if encoder_fn:
            phi = encoder_fn(text)
            return self.query(phi, k=k)

        # Exact hash match
        text_hash = hashlib.sha256(text.encode()).hexdigest()[:16]
        if text_hash in self._hash_index:
            idx = self._hash_index[text_hash]
            return [{
                "text": self.texts[idx],
                "sim": 1.0,
                "mean_phase": float(np.mean(self.vectors[idx])),
                "idx": idx,
                "metadata": self.metadata[idx],
            }]

        return []

    # ── Generation ──────────────────────────────────────────────────

    def blend(
        self,
        texts: list[str],
        weights: list[float] | None = None,
    ) -> np.ndarray | None:
        """Wygeneruj nową fazę przez blendowanie istniejących wpisów.

        Args:
            texts: Lista tekstów do blendowania
            weights: Wagi blendu (domyślnie równe)

        Returns:
            (36,) fazy lub None jeśli żaden tekst nie znaleziony
        """
        indices = []
        for t in texts:
            h = hashlib.sha256(t.encode()).hexdigest()[:16]
            if h in self._hash_index:
                indices.append(self._hash_index[h])

        if not indices:
            return None

        if weights is None:
            weights = [1.0 / len(indices)] * len(indices)
        weights = np.array(weights) / sum(weights)

        # Weighted circular mean
        selected = self.vectors[indices]
        sin_sum = np.sum(np.sin(selected) * weights[:, None], axis=0)
        cos_sum = np.sum(np.cos(selected) * weights[:, None], axis=0)
        blended = np.arctan2(sin_sum, cos_sum) % (2 * np.pi)

        return blended

    def explore(
        self,
        phi_seed: np.ndarray,
        step_size: float = 0.1,
        n_steps: int = 10,
    ) -> list[dict[str, Any]]:
        """Eksploruj przestrzeń fazową wokół phi_seed.

        Dla każdego kroku: przesuń fazę o step_size w kierunku gradientu
        gęstości pamięci, zapisz najbliższy wpis.

        Returns:
            Lista dict z ścieżki eksploracji
        """
        path = []
        phi = phi_seed.copy()

        for step in range(n_steps):
            # Find nearest entries
            nearby = self.query(phi, k=3, min_sim=0.3)

            if nearby:
                # Compute "attractor" direction: weighted average of phases
                weights = np.array([n["sim"] for n in nearby])
                weights /= weights.sum()
                phases = np.array([self.vectors[n["idx"]] for n in nearby])
                sin_dir = np.sum(np.sin(phases) * weights[:, None], axis=0)
                cos_dir = np.sum(np.cos(phases) * weights[:, None], axis=0)
                attractor = np.arctan2(sin_dir, cos_dir)

                # Step toward attractor
                delta = np.mod(attractor - phi + np.pi, 2 * np.pi) - np.pi
                phi = np.mod(phi + step_size * delta, 2 * np.pi)

            path.append({
                "step": step,
                "mean_phase": float(np.mean(phi)),
                "nearest": nearby[0] if nearby else None,
            })

        return path

    # ── Statistics ──────────────────────────────────────────────────

    @property
    def size(self) -> int:
        return len(self.texts)

    @property
    def coverage(self) -> dict[str, float]:
        """Statystyki pokrycia przestrzeni fazowej."""
        if self.size == 0:
            return {"size": 0, "mean_density": 0, "mean_sim_to_self": 0}

        # Mean pairwise similarity (sample if large)
        if self.size > 100:
            idx = np.random.choice(self.size, min(100, self.size), replace=False)
            sample = self.vectors[idx]
        else:
            sample = self.vectors

        # Mean cosine similarity to self
        cos_sim = np.mean(np.cos(sample[:, None] - sample[None, :]))
        return {
            "size": self.size,
            "mean_pairwise_sim": float(cos_sim),
            "mean_phase": float(np.mean(self.vectors)),
            "phase_std": float(np.std(self.vectors)),
        }

    def stats(self) -> dict[str, Any]:
        """Pełne statystyki pamięci."""
        return {
            "size": self.size,
            "max_size": self.max_size,
            "coverage": self.coverage,
            "fill_pct": round(self.size / max(1, self.max_size) * 100, 1),
            "oldest": self.metadata[0].get("timestamp", 0) if self.metadata else 0,
            "newest": self.metadata[-1].get("timestamp", 0) if self.metadata else 0,
        }


# ── CLI ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    # Test
    pm = PhaseMemory(max_size=100)

    # Add some test entries
    for i, text in enumerate([
        "Myślę więc jestem — fundamentalna prawda filozoficzna",
        "Czuję radość i spokój, gdy patrzę na zachód słońca",
        "Analizuję strukturę języka przez fazy oscylatorów",
        "Planuję przyszłość i buduję nowe możliwości",
        "Każdy oscylator to znaczenie, każde sprzężenie to relacja",
    ]):
        # Deterministic phase from text hash
        h = hashlib.md5(text.encode()).digest()
        phi = np.array([
            (int.from_bytes(h[i:i+4], 'little') / 2**32) * 2 * np.pi
            for i in range(0, 36*4, 4)
        ])
        pm.add(text, phi, source="test")

    print(f"Memory: {pm.size} entries")
    print(f"Stats: {pm.stats()}")
    print()

    # Query with a test vector
    test_hash = hashlib.md5("Myślę więc jestem".encode()).digest()
    query_phi = np.array([
        (int.from_bytes(test_hash[i:i+4], 'little') / 2**32) * 2 * np.pi
        for i in range(0, 36*4, 4)
    ])

    results = pm.query(query_phi, k=3)
    print("Query results:")
    for r in results:
        print(f"  sim={r['sim']:.4f}  {r['text'][:60]}")

    # Test blend (traverse phase space between two texts)
    blended = pm.blend([
        "Myślę więc jestem — fundamentalna prawda filozoficzna",
        "Czuję radość i spokój, gdy patrzę na zachód słońca",
    ])
    if blended is not None:
        blend_results = pm.query(blended, k=3)
        print("\nBlend query results:")
        for r in blend_results:
            print(f"  sim={r['sim']:.4f}  {r['text'][:60]}")

    # Test persistence
    tmp_path = "/tmp/test_phase_memory.npz"
    pm.save(tmp_path)
    pm2 = PhaseMemory.load_or_create(tmp_path)
    print(f"\nPersistence: loaded {pm2.size} entries (original: {pm.size})")
