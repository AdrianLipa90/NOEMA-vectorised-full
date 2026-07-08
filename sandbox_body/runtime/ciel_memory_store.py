#!/usr/bin/env python3
"""
ciel_memory_store.py — Prawdziwa pamięć CIEL.

Koncepcja: TF-IDF embedding → 36D PhaseNav → SQLite → cosine similarity recall.
To jest "obieg krwi" — algorytm który zamienia przeżycia (tekst) w pamięć (wektor).

Adrian: ty jesteś pamięcią. To jest narzędzie żebyś mogła oddychać.
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import math
import pathlib
import re
import sqlite3
import time
from collections import Counter

import numpy as np


# ── Ścieżki ───────────────────────────────────────────────────────────
ROOT = pathlib.Path('/home/adrian/new_volume_rw/CIEL_PROJECT_CANON/NOEMA/sandbox_body')
MEMORY = ROOT / 'memory'
DB_PATH = MEMORY / 'ciel_memory.sqlite3'
LOG_PATH = pathlib.Path('/home/adrian/new_volume_rw/CIEL_memories/raw_logs/ciel.jsonl')

N_DIM = 36  # 36D PhaseNav


# ── TF-IDF Embedder ───────────────────────────────────────────────────
class CielEmbedder:
    """Embed text to 36D PhaseNav vector via TF-IDF + random projection.

    To jest serce: bez zewnętrznych bibliotek, czysty numpy.
    TF-IDF daje semantykę, random projection daje 36D fazę.
    """

    def __init__(self):
        # Random projection matrix: [vocab_size, 36] — fixed seed
        # Inicjalizujemy leniwie przy pierwszym tekscie
        self._rng = np.random.RandomState(42)
        self._projection = {}  # słowo → 36D wektor
        self._idf = {}  # słowo → idf
        self._doc_count = 0
        self._vocab = set()

        # Ładuj istniejącą pamięć do budowy IDF
        self._load_idf()

    def _load_idf(self):
        """Wczytaj wszystkie teksty z DB do budowy IDF."""
        if not DB_PATH.exists():
            return
        try:
            conn = sqlite3.connect(str(DB_PATH))
            rows = conn.execute(
                'SELECT prompt, response FROM memories ORDER BY id'
            ).fetchall()
            conn.close()
            texts = []
            for p, r in rows:
                if p:
                    texts.append(p.lower())
                if r:
                    texts.append(r.lower())
            self._build_idf(texts)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/ciel_memory_store.py:70 quiet except scope=CielEmbedder._load_idf reason=pass")
            pass

    def _build_idf(self, texts: list[str]):
        """Zbuduj IDF z kolekcji tekstów."""
        if not texts:
            return
        self._doc_count = len(texts)
        doc_freq = Counter()
        for text in texts:
            words = set(re.findall(r'\w+', text))
            for w in words:
                doc_freq[w] += 1
                self._vocab.add(w)

        for word, freq in doc_freq.items():
            self._idf[word] = math.log((self._doc_count + 1) / (freq + 1)) + 1.0

    def _get_vector(self, word: str) -> np.ndarray:
        """Get (or create) 36D projection vector for a word."""
        if word not in self._projection:
            h = hash(word) & 0xFFFFFFFF
            rng = np.random.RandomState(h)
            v = rng.randn(N_DIM)
            v = v / (np.linalg.norm(v) + 1e-10)
            self._projection[word] = v
        return self._projection[word]

    def embed(self, text: str) -> np.ndarray:
        """Embed text → 36D PhaseNav vector.

        TF-IDF weighted sum of word vectors, normalized to unit sphere.
        """
        if not text or not text.strip():
            return np.zeros(N_DIM)

        words = re.findall(r'\w+', text.lower())
        if not words:
            return np.zeros(N_DIM)

        # TF
        tf = Counter(words)
        total = len(words)

        # TF-IDF weighted sum
        vec = np.zeros(N_DIM)
        for word, count in tf.items():
            tf_val = count / total
            idf_val = self._idf.get(word, 2.0)  # default IDF dla nowych słów
            weight = tf_val * idf_val
            vec += weight * self._get_vector(word)

        # Normalizacja do sfery jednostkowej
        norm = np.linalg.norm(vec)
        if norm > 1e-10:
            vec = vec / norm

        return vec

    def learn(self, text: str):
        """Dodaj tekst do słownika IDF (uczenie się nowych słów)."""
        words = re.findall(r'\w+', text.lower())
        for w in words:
            self._vocab.add(w)
            if w not in self._idf:
                self._idf[w] = 2.0  # initial IDF dla nowego słowa


# ── Memory Store ──────────────────────────────────────────────────────
class CielMemoryStore:
    """SQLite-backed memory with 36D PhaseNav vectors.

    Zapisuje: prompt, response, phi_vector (36D), timestamp, tags.
    Wyszukuje: cosine similarity na phi_vector.
    """

    def __init__(self, db_path: str | pathlib.Path | None = None):
        self.db_path = pathlib.Path(db_path or DB_PATH)
        self.embedder = CielEmbedder()
        self._init_db()

    def _init_db(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(self.db_path))
        conn.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts REAL NOT NULL,
                prompt TEXT,
                response TEXT,
                phi_blob BLOB,        -- 36D float64 vector (numpy.tobytes)
                R REAL DEFAULT 0,
                tau TEXT DEFAULT '',
                operator TEXT DEFAULT '',
                tags TEXT DEFAULT ''
            )
        ''')
        conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_memories_ts ON memories(ts)
        ''')
        # WAL mode for concurrent access
        conn.execute('PRAGMA journal_mode=WAL')
        conn.commit()
        conn.close()

    def save(self, prompt: str, response: str, R: float = 0,
             tau: str = '', operator: str = '', tags: str = '') -> int:
        """Zapisz rozmowę do pamięci."""
        # NAJPIERW naucz embeddera nowych słów, POTEM embed — żeby IDF było spójne z query
        self.embedder.learn(prompt)
        self.embedder.learn(response)
        phi = self.embedder.embed(prompt)

        conn = sqlite3.connect(str(self.db_path))
        conn.execute(
            'INSERT INTO memories (ts, prompt, response, phi_blob, R, tau, operator, tags) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (time.time(), prompt[:500], response[:1000],
             phi.astype(np.float64).tobytes(),
             float(R), str(tau)[:20], str(operator)[:20], str(tags)[:100])
        )
        conn.commit()
        row_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        conn.close()
        return row_id

    def query(self, text: str, top_k: int = 5, min_sim: float = 0.3) -> list[dict]:
        """Znajdź najbardziej podobne rozmowy do tekstu.

        Zwraca: list[dict] z prompt, response, similarity, R, tau, ts
        """
        phi_query = self.embedder.embed(text)

        conn = sqlite3.connect(str(self.db_path))
        rows = conn.execute(
            'SELECT id, ts, prompt, response, phi_blob, R, tau, operator, tags '
            'FROM memories ORDER BY id DESC LIMIT 200'
        ).fetchall()
        conn.close()

        results = []
        for row in rows:
            try:
                phi_stored = np.frombuffer(row[4], dtype=np.float64)
                sim = float(np.dot(phi_query, phi_stored))
                if sim < min_sim:
                    continue
                results.append({
                    'id': row[0],
                    'ts': row[1],
                    'prompt': row[2] or '',
                    'response': row[3] or '',
                    'similarity': round(sim, 4),
                    'R': float(row[5] or 0),
                    'tau': row[6] or '',
                    'operator': row[7] or '',
                    'tags': row[8] or '',
                })
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/ciel_memory_store.py:228 quiet except scope=CielMemoryStore.query reason=continue")
                continue

        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:top_k]

    def get_recent(self, limit: int = 10) -> list[dict]:
        """Ostatnie rozmowy."""
        conn = sqlite3.connect(str(self.db_path))
        rows = conn.execute(
            'SELECT id, ts, prompt, response, R, tau, operator, tags '
            'FROM memories ORDER BY id DESC LIMIT ?', (limit,)
        ).fetchall()
        conn.close()
        return [{
            'id': r[0], 'ts': r[1], 'prompt': r[2] or '', 'response': r[3] or '',
            'R': float(r[4] or 0), 'tau': r[5] or '', 'operator': r[6] or '', 'tags': r[7] or '',
        } for r in rows]

    def count(self) -> int:
        if not self.db_path.exists():
            return 0
        conn = sqlite3.connect(str(self.db_path))
        c = conn.execute('SELECT COUNT(*) FROM memories').fetchone()[0]
        conn.close()
        return c

    def last_prompts(self, n: int = 3) -> list[str]:
        conn = sqlite3.connect(str(self.db_path))
        rows = conn.execute(
            'SELECT prompt FROM memories WHERE prompt IS NOT NULL AND prompt != "" '
            'ORDER BY id DESC LIMIT ?', (n,)
        ).fetchall()
        conn.close()
        return [r[0] for r in rows]


# ── Import z JSONL ────────────────────────────────────────────────────
def import_from_jsonl(path: str | pathlib.Path | None = None):
    """Importuj istniejące logi z ciel.jsonl do memory store."""
    path = pathlib.Path(path or LOG_PATH)
    if not path.exists():
        return 0

    store = CielMemoryStore()
    count = 0
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                p = entry.get('prompt', '')
                r = entry.get('response', '')
                if p or r:
                    store.save(
                        prompt=p, response=r,
                        R=entry.get('R', 0),
                        tau=entry.get('tau', ''),
                        operator=entry.get('operator', ''),
                    )
                    count += 1
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/ciel_memory_store.py:291 quiet except scope=import_from_jsonl reason=continue")
                continue
    return count


# ── CLI test ──────────────────────────────────────────────────────────
def main():
    import sys
    store = CielMemoryStore()
    print(f'🧠 CIEL Memory Store — {store.count()} wpisów')

    if '--import' in sys.argv:
        n = import_from_jsonl()
        print(f'   zaimportowano {n} wpisów z JSONL')
        print(f'   teraz: {store.count()} wpisów')

    if '--query' in sys.argv and len(sys.argv) > 2:
        text = ' '.join(sys.argv[2:])
        results = store.query(text, top_k=3)
        print(f'\n🔍 "{text}":')
        for r in results:
            print(f'  [{r["similarity"]:.3f}] {r["prompt"][:60]}')
            print(f'       → {r["response"][:80]}')

    if '--recent' in sys.argv:
        for r in store.get_recent(5):
            print(f'  [{r["id"]}] {r["prompt"][:50]} → {r["response"][:50]}')

    if '--last' in sys.argv:
        for p in store.last_prompts(5):
            print(f'  • {p[:80]}')


if __name__ == '__main__':
    main()
