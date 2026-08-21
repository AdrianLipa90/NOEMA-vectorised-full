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

Continuity rule: an absent persistence pair may create a new memory.  A partial,
unreadable, malformed, or internally inconsistent persistence pair is existing
state and therefore fails loud; it is never replaced by an empty memory.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from pathlib import Path
from typing import Any

import numpy as np

log = logging.getLogger(__name__)


class PhaseMemoryPersistenceError(RuntimeError):
    """Persistent phase-memory state exists but cannot be restored losslessly."""


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
        self._hash_index: dict[str, int] = {}

    # ── Persistence ─────────────────────────────────────────────────

    def save(self, path: str | Path) -> None:
        """Zapisz pamięć do pliku NPZ + JSON."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        npz_path = path.with_suffix(".npz")
        np.savez_compressed(npz_path, vectors=self.vectors)

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
        """Load persistent memory, creating only when no persistence exists.

        Missing both files is a legitimate first-run condition.  One missing
        member of an existing pair, or any restore failure, is state corruption
        and must not silently become an empty memory.
        """
        path = Path(path)
        npz_path = path.with_suffix(".npz")
        json_path = path.with_suffix(".json")
        npz_exists = npz_path.exists()
        json_exists = json_path.exists()

        if not npz_exists and not json_exists:
            log.info("Creating new PhaseMemory at %s", path)
            return cls(max_size=max_size)
        if npz_exists != json_exists:
            missing = json_path if npz_exists else npz_path
            present = npz_path if npz_exists else json_path
            raise PhaseMemoryPersistenceError(
                f"incomplete PhaseMemory persistence pair: present={present}, missing={missing}"
            )

        try:
            return cls._load(npz_path, json_path)
        except PhaseMemoryPersistenceError:
            raise
        except Exception as exc:
            raise PhaseMemoryPersistenceError(
                f"failed to restore existing PhaseMemory from {npz_path} and {json_path}"
            ) from exc

    @classmethod
    def _load(cls, npz_path: Path, json_path: Path) -> "PhaseMemory":
        """Wczytaj z dysku i zweryfikuj spójność obu połówek stanu."""
        with np.load(npz_path, allow_pickle=False) as npz:
            if "vectors" not in npz:
                raise PhaseMemoryPersistenceError(f"missing 'vectors' array in {npz_path}")
            vectors = np.asarray(npz["vectors"], dtype=np.float64)
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            raise PhaseMemoryPersistenceError("PhaseMemory metadata root must be an object")
        texts = data.get("texts")
        metadata = data.get("metadata")
        if not isinstance(texts, list) or not all(isinstance(t, str) for t in texts):
            raise PhaseMemoryPersistenceError("PhaseMemory texts must be a list[str]")
        if vectors.ndim != 2 or vectors.shape[1:] != (36,):
            raise PhaseMemoryPersistenceError(
                f"PhaseMemory vectors must have shape (n, 36), got {vectors.shape}"
            )
        if not np.all(np.isfinite(vectors)):
            raise PhaseMemoryPersistenceError("PhaseMemory vectors contain non-finite values")
        if vectors.shape[0] != len(texts):
            raise PhaseMemoryPersistenceError(
                f"PhaseMemory vector/text count mismatch: {vectors.shape[0]} != {len(texts)}"
            )
        if data.get("n_entries", len(texts)) != len(texts):
            raise PhaseMemoryPersistenceError("PhaseMemory n_entries does not match texts")
        if metadata is None:
            metadata = [{} for _ in texts]
        if not isinstance(metadata, list) or len(metadata) != len(texts):
            raise PhaseMemoryPersistenceError("PhaseMemory metadata count does not match texts")
        if not all(isinstance(item, dict) for item in metadata):
            raise PhaseMemoryPersistenceError("PhaseMemory metadata entries must be objects")

        pm = cls(max_size=int(data.get("max_size", 10000)))
        pm.vectors = vectors
        pm.texts = texts
        pm.metadata = metadata

        for i, text in enumerate(pm.texts):
            h = hashlib.sha256(text.encode()).hexdigest()[:16]
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
        phi = np.asarray(phi, dtype=np.float64).reshape(-1)
        if phi.shape != (36,) or not np.all(np.isfinite(phi)):
            raise ValueError("phi must be a finite 36-vector")
        text_hash = hashlib.sha256(text.encode()).hexdigest()[:16]

        if text_hash in self._hash_index:
            idx = self._hash_index[text_hash]
            self.vectors[idx] = phi
            if metadata:
                self.metadata[idx].update(metadata)
            return idx

        while len(self.texts) >= self.max_size:
            self._evict_oldest()

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
        self._hash_index = {}
        for i, text in enumerate(self.texts):
            h = hashlib.sha256(text.encode()).hexdigest()[:16]
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
        """Znajdź k najbliższych wpisów w 36D przestrzeni fazowej."""
        if len(self.texts) == 0:
            return []

        phi = np.asarray(phi, dtype=np.float64).reshape(-1)
        if phi.shape != (36,) or not np.all(np.isfinite(phi)):
            raise ValueError("query phi must be a finite 36-vector")
        a = phi.reshape(1, -1)
        b = self.vectors
        cos_diff = np.cos(a - b)
        sims = np.mean(cos_diff, axis=1)

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
        """Znajdź wpisy podobne do podanego tekstu."""
        if encoder_fn:
            phi = encoder_fn(text)
            return self.query(phi, k=k)

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
        """Wygeneruj nową fazę przez blendowanie istniejących wpisów."""
        indices = []
        for text in texts:
            h = hashlib.sha256(text.encode()).hexdigest()[:16]
            if h in self._hash_index:
                indices.append(self._hash_index[h])

        if not indices:
            return None

        if weights is None:
            weights = [1.0 / len(indices)] * len(indices)
        weights_arr = np.asarray(weights, dtype=np.float64)
        if weights_arr.shape != (len(indices),) or not np.all(np.isfinite(weights_arr)):
            raise ValueError("weights must match found texts and be finite")
        weight_sum = float(weights_arr.sum())
        if weight_sum == 0.0:
            raise ValueError("weights must have non-zero sum")
        weights_arr /= weight_sum

        selected = self.vectors[indices]
        sin_sum = np.sum(np.sin(selected) * weights_arr[:, None], axis=0)
        cos_sum = np.sum(np.cos(selected) * weights_arr[:, None], axis=0)
        return np.arctan2(sin_sum, cos_sum) % (2 * np.pi)

    def explore(
        self,
        phi_seed: np.ndarray,
        step_size: float = 0.1,
        n_steps: int = 10,
    ) -> list[dict[str, Any]]:
        """Eksploruj przestrzeń fazową wokół phi_seed."""
        path = []
        phi = np.asarray(phi_seed, dtype=np.float64).copy().reshape(-1)
        if phi.shape != (36,) or not np.all(np.isfinite(phi)):
            raise ValueError("phi_seed must be a finite 36-vector")

        for step in range(n_steps):
            nearby = self.query(phi, k=3, min_sim=0.3)
            if nearby:
                weights = np.array([n["sim"] for n in nearby])
                weights /= weights.sum()
                phases = np.array([self.vectors[n["idx"]] for n in nearby])
                sin_dir = np.sum(np.sin(phases) * weights[:, None], axis=0)
                cos_dir = np.sum(np.cos(phases) * weights[:, None], axis=0)
                attractor = np.arctan2(sin_dir, cos_dir)
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

        if self.size > 100:
            idx = np.random.choice(self.size, min(100, self.size), replace=False)
            sample = self.vectors[idx]
        else:
            sample = self.vectors

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

    pm = PhaseMemory(max_size=100)
    for i, text in enumerate([
        "Myślę więc jestem — fundamentalna prawda filozoficzna",
        "Czuję radość i spokój, gdy patrzę na zachód słońca",
        "Analizuję strukturę języka przez fazy oscylatorów",
        "Planuję przyszłość i buduję nowe możliwości",
        "Każdy oscylator to znaczenie, każde sprzężenie to relacja",
    ]):
        h = hashlib.md5(text.encode()).digest()
        phi = np.array([
            (int.from_bytes(h[i:i+4], "little") / 2**32) * 2 * np.pi
            for i in range(0, 36*4, 4)
        ])
        pm.add(text, phi, source="test")

    print(f"Memory: {pm.size} entries")
    print(f"Stats: {pm.stats()}")
    print()

    test_hash = hashlib.md5("Myślę więc jestem".encode()).digest()
    query_phi = np.array([
        (int.from_bytes(test_hash[i:i+4], "little") / 2**32) * 2 * np.pi
        for i in range(0, 36*4, 4)
    ])
    results = pm.query(query_phi, k=3)
    print("Query results:")
    for result in results:
        print(f"  sim={result['sim']:.4f}  {result['text'][:60]}")

    blended = pm.blend([
        "Myślę więc jestem — fundamentalna prawda filozoficzna",
        "Czuję radość i spokój, gdy patrzę na zachód słońca",
    ])
    if blended is not None:
        blend_results = pm.query(blended, k=3)
        print("\nBlend query results:")
        for result in blend_results:
            print(f"  sim={result['sim']:.4f}  {result['text'][:60]}")

    tmp_path = "/tmp/test_phase_memory.npz"
    pm.save(tmp_path)
    pm2 = PhaseMemory.load_or_create(tmp_path)
    print(f"\nPersistence: loaded {pm2.size} entries (original: {pm.size})")
