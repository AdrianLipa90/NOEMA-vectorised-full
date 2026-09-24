"""MultiskillOrchestrator — 291 skilli jako 36D PhaseNav + kompozycja.

Każdy skill → 36D wektor fazy (jak library_index).
Multiskill = najbliższe wektory w przestrzeni PhaseNav spięte przez operator edges.
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any

import numpy as np

from ciel_geometry.paths import P

SKILLS_DIR = Path(__file__).resolve().parent.parent.parent / ".opencode" / "skills"
PHASE_INDEX_DIR = Path(P.LIBRARY) / "PHASE_INDEX"

N_OSCILLATORS = 36
# kappa z monografii Metatime: ln2/(24*pi). Poprzednio 36*pi (dryft,
# nieautoryzowany — potwierdzone 2026-07-08); przywrócone do derywacji.
OI = math.log(2) / (24 * math.pi)

# ── stopwords ─────────────────────────────────────────────────────────────
_STOP = {
    "this", "that", "with", "from", "have", "been", "will", "they",
    "there", "which", "their", "what", "when", "where", "than", "them",
    "also", "into", "over", "then", "each", "about", "would", "could",
    "should", "other", "more", "some", "these", "those", "after",
    "before", "between", "through", "during", "without", "within",
    "along", "while", "because", "just", "very", "much",
}


class MultiskillOrchestrator:
    """291 skilli jako przestrzeń fazowa. Komponuj, łańcuchuj, wykonuj."""

    def __init__(self):
        self.skills: dict[str, dict] = {}       # name → metadata
        self._vectors: np.ndarray | None = None  # (N, 36) phase vectors
        self._names: list[str] = []              # parallel to _vectors
        self._priorities: np.ndarray | None = None  # (N,) precomputed priority scores
        self._load()

    # ── phase encoding ────────────────────────────────────────────────────

    @staticmethod
    def _text_to_phi(text: str) -> np.ndarray:
        """Tekst → 36D wektor fazy (jak PhaseNav library_index)."""
        words = re.findall(r'[a-zA-Z]{4,}', text.lower())
        words = [w for w in words if w not in _STOP]
        if not words:
            return np.zeros(N_OSCILLATORS, dtype=np.float64)
        phi = np.zeros(N_OSCILLATORS, dtype=np.float64)
        for w in set(words):
            h = hashlib.sha256(w.encode()).hexdigest()
            idx = int(h[:8], 16) % N_OSCILLATORS
            freq = words.count(w) / len(words)
            phi[idx] = (phi[idx] + 2 * math.pi * freq) % (2 * math.pi)
        return phi

    # ── ładowanie ─────────────────────────────────────────────────────────

    def _load(self) -> None:
        """Wczytaj wszystkie 291 skilli → wektory."""
        vectors, names = [], []
        for d in sorted(SKILLS_DIR.iterdir()):
            if not d.is_dir():
                continue
            md_file = d / "SKILL.md"
            if not md_file.exists():
                continue
            text = md_file.read_text(encoding="utf-8", errors="replace")
            # wyciągnij nazwę z frontmatter YAML lub nazwy katalogu
            name = d.name
            # priorytet z YAML header
            priority = 3
            desc = ""
            try:
                import yaml
                parts = text.split("---", 2)
                if len(parts) >= 3:
                    front = yaml.safe_load(parts[1])
                    if front:
                        name = front.get("name", name)
                        priority = front.get("priority", priority)
                        desc = front.get("description", "") or ""
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/multiskill.py:88 quiet except scope=MultiskillOrchestrator._load reason=pass")
                pass
            vec = self._text_to_phi(text)
            vectors.append(vec)
            names.append(name)
            self.skills[name] = {
                "dir": d.name,
                "priority": priority,
                "description": desc.strip(),
                "phi": vec.tolist(),
            }
        self._vectors = np.array(vectors, dtype=np.float64) if vectors else None
        self._names = names
        self._priorities = np.array([
            self.skills.get(n, {}).get("priority", 3) for n in names
        ], dtype=np.float64) if names else None

    @property
    def count(self) -> int:
        return len(self._names)

    # ── resolve — znajdź multiskill dla zadania ──────────────────────────

    def resolve(self, task: str, top_n: int = 5,
                min_similarity: float = 0.1,
                priority_boost: bool = True) -> list[dict]:
        """Znajdź najlepsze skille dla zadania.

        Returns list of {name, similarity, priority, description}.
        """
        if self._vectors is None or len(self._vectors) == 0:
            return []
        q = self._text_to_phi(task)
        cos_sim = np.cos(self._vectors - q).mean(axis=1)
        scores = cos_sim.copy()
        if priority_boost and self._priorities is not None:
            scores += 0.05 * (5.0 - self._priorities)  # wektorowo: P1 → +0.20, P5 → +0.00
        best = np.argsort(-scores)[:top_n]
        results = []
        for idx in best:
            if scores[idx] < min_similarity:
                continue
            name = self._names[idx]
            meta = self.skills.get(name, {})
            results.append({
                "name": name,
                "dir": meta.get("dir", name),
                "similarity": round(float(cos_sim[idx]), 4),
                "score": round(float(scores[idx]), 4),
                "priority": meta.get("priority", 3),
                "description": meta.get("description", ""),
            })
        return results

    def resolve_chain(self, task: str, max_skills: int = 5) -> list[str]:
        """Zwróć sekwencję skilli do wykonania (łańcuch kompozycji)."""
        top = self.resolve(task, top_n=max_skills)
        return [t["name"] for t in top if t["similarity"] > 0.05]

    # ── skill graph — powiązania semantyczne ─────────────────────────────

    def neighbors(self, skill_name: str, top_n: int = 5) -> list[dict]:
        """Znajdź semanticznie bliskie skille."""
        if skill_name not in self.skills:
            return []
        idx = self._names.index(skill_name)
        q = self._vectors[idx]
        cos_sim = np.cos(self._vectors - q).mean(axis=1)
        best = np.argsort(-cos_sim)[1:top_n + 1]  # skip self
        results = []
        for i in best:
            name = self._names[i]
            meta = self.skills.get(name, {})
            results.append({
                "name": name,
                "similarity": round(float(cos_sim[i]), 4),
                "priority": meta.get("priority", 3),
            })
        return results

    def cluster(self, skill_names: list[str]) -> np.ndarray:
        """Średnia fazowa klastra skilli — wektor multiskillu."""
        indices = [self._names.index(n) for n in skill_names if n in self._names]
        if not indices:
            return np.zeros(N_OSCILLATORS)
        cluster_vec = np.mean(np.exp(1j * self._vectors[list(indices)]), axis=0)
        return np.angle(cluster_vec + 1e-12) % (2 * math.pi)

    # ── persist ──────────────────────────────────────────────────────────

    def save_index(self) -> None:
        """Zapisz skill_index.npy (jak library_index)."""
        PHASE_INDEX_DIR.mkdir(parents=True, exist_ok=True)
        if self._vectors is not None:
            np.save(str(PHASE_INDEX_DIR / "skill_index.npy"), self._vectors)
            meta = np.array([
                {"name": name, "priority": self.skills[name]["priority"],
                 "description": self.skills[name]["description"][:64],
                 "dir": self.skills[name]["dir"]}
                for name in self._names
            ], dtype=object)
            np.save(str(PHASE_INDEX_DIR / "skill_meta.npy"), meta)
            # knowledge bridge format
            idx_path = PHASE_INDEX_DIR / "skill_index.json"
            serializable = {
                "skills": [
                    {"name": str(name),
                     "phi": [round(float(v), 6) for v in self.skills[name]["phi"]],
                     "priority": int(self.skills[name]["priority"])}
                    for name in self._names
                ],
                "N": len(self._names),
            }
            idx_path.write_text(json.dumps(serializable, indent=2))

    # ── introspection ────────────────────────────────────────────────────

    def describe(self, skill_name: str) -> str:
        """Opis skillu + najbliżsi sąsiedzi."""
        if skill_name not in self.skills:
            return f"skill '{skill_name}' not found"
        meta = self.skills[skill_name]
        lines = [
            f"Skill: {skill_name}",
            f"  priority: {meta['priority']}",
            f"  dir: {meta['dir']}",
            f"  φ̄: {float(np.mean(meta['phi'])):.3f}",
        ]
        nbrs = self.neighbors(skill_name, top_n=3)
        if nbrs:
            lines.append("  neighbors:")
            for n in nbrs:
                lines.append(f"    {n['name']:30s} sim={n['similarity']:.4f}")
        return "\n".join(lines)


# ── standalone ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    m = MultiskillOrchestrator()
    print(f"loaded {m.count} skills")
    print()
    # top skills for a task
    res = m.resolve("memory consolidation phase synchronisation", top_n=5)
    for r in res:
        print(f"  P{r['priority']}  sim={r['similarity']:.4f}  {r['name']}")
    print()
    # save index
    m.save_index()
    print("saved to PHASE_INDEX/skill_index.*")
