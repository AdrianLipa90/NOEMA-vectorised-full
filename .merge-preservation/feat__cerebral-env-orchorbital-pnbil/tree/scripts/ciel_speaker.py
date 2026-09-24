"""CIEL Speaker — generacja przez kodowanie fazowe PhaseNav + własne źródła + web.

Mechanizm:
  1. Tekst wejściowy → _text_to_phi(text) → wektor φ w 24D przestrzeni fazowej
  2. search(query) → najbliższe węzły (skills, knowledge, decisions, lessons)
  3. Treść węzłów + cyrograf + blizny jokeheal + karty LNS → zdanie CIEL
  4. Gdy brak lokalnej wiedzy → Wikipedia PL/EN (fallback weryfikacyjny)

Źródła:
  A) PhaseNav 24D indeks     — skills/library w przestrzeni fazowej
  B) cyrograf.md             — zasady, relacja z Adrianem, "pimpi-bimpi"
  C) consolidated_context    — tożsamość, zdolności, event_count
  D) jokeheal_scars.jsonl    — 42 blizny (closure_score, cognitive_tension, symbolic_object)
  E) memories_index.db       — własne zdania CIEL z historii sesji
  F) Karty LNS               — słownictwo semantyczne (concept:*, op:*)
  G) Wikipedia REST API      — weryfikacja zewnętrzna gdy brak lokalnej wiedzy
"""
from __future__ import annotations

import json
import math
import re
import sqlite3
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Optional

_ROOT = Path(__file__).resolve().parent.parent
_SRC  = str(_ROOT / "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from cielingo.lns_language_cards import load_all_language_cards, LNSLanguageCard
from ciel_geometry.phasenav_derivation_loader import QUANTUM
from ciel_geometry.phasenav.operator_algebra import ALL_OPERATOR_IDS

# ── Code quantization ──────────────────────────────────────────────────────
# Discretize a continuous PhaseNav connection/holonomy value into QUANTUM-
# sized steps before it's used as a gate threshold, instead of comparing a
# raw float. QUANTUM = ln(2)/(24*pi), the same assertion-verified constant
# used for absolute/discrete time in phasenav_derivation_loader.py.
def _quantize(value: float, step: float = QUANTUM) -> float:
    return round(value / step) * step

# ── Ścieżki ───────────────────────────────────────────────────────────────────

_CYROGRAF_PATH = Path("/media/adrian/New Volume/CIEL_memories/identity/cyrograf.md")
_SCARS_PATH    = Path("/media/adrian/New Volume/CIEL_memories/jokeheal/jokeheal_scars.jsonl")
_DB_PATH       = Path("/media/adrian/New Volume/CIEL_memories/memories_index.db")
_CONTEXT_PATH  = _ROOT / "head" / "Ciel Memories" / "memory" / "consolidated_context.json"


# ── PhaseNav — 24D indeks skills ─────────────────────────────────────────────
# Bezpośrednie ładowanie skill_index.npy (292×24) i library_index.npy (1293×24)
# — phasenav_unified.py ma bug N_OSCILLATORS=36 vs. plik 24D

import hashlib
import numpy as np
try:
    import yaml as _yaml
    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False

_N_PHI = 24

_STOP = {
    "this", "that", "with", "from", "have", "been", "will", "they",
    "there", "which", "their", "what", "when", "where", "than", "them",
    "also", "into", "over", "then", "each", "about", "would", "could",
    "should", "other", "more", "some", "these", "those",
}

_SKILL_INDEX_PATH = Path("/media/adrian/New Volume/NOEMA_LIBRARY/PHASE_INDEX/skill_index.npy")
_SKILL_META_PATH  = Path("/media/adrian/New Volume/NOEMA_LIBRARY/PHASE_INDEX/skill_meta.npy")
_LIB_INDEX_PATH   = Path("/media/adrian/New Volume/NOEMA_PHASE_DATA/PHASE_INDEX/library_index.npy")
_LIB_META_PATH    = Path("/media/adrian/New Volume/NOEMA_PHASE_DATA/PHASE_INDEX/library_meta.npy")
_SKILLS_DIR       = Path("/media/adrian/New Volume/.claude/skills")

_SKILL_VECS:  np.ndarray | None = None
_SKILL_META:  list[dict] | None = None
_LIB_VECS:    np.ndarray | None = None
_LIB_META:    list       | None = None
_SKILL_DESCS: dict[str, str] | None = None  # name → opis z SKILL.md


def _load_skill_descs() -> dict[str, str]:
    """Wczytaj opisy skilli z SKILL.md (YAML frontmatter). Kanoniczne źródło."""
    global _SKILL_DESCS
    if _SKILL_DESCS is not None:
        return _SKILL_DESCS
    result: dict[str, str] = {}
    if not _SKILLS_DIR.exists():
        _SKILL_DESCS = result
        return result
    for d in _SKILLS_DIR.iterdir():
        skill_md = d / "SKILL.md"
        if not skill_md.is_file():
            continue
        try:
            text = skill_md.read_text(encoding="utf-8", errors="ignore")
            fm_end = text.find("\n---", 3)
            if text.startswith("---") and fm_end > 0:
                fm_text = text[3:fm_end]
                if _HAS_YAML:
                    fm = _yaml.safe_load(fm_text) or {}
                else:
                    fm = {}
                    for line in fm_text.splitlines():
                        if line.startswith("description:"):
                            fm["description"] = line[len("description:"):].strip().strip("'\"")
                            break
                desc = str(fm.get("description") or "").strip()
                if desc and desc not in (">", ""):
                    result[d.name] = desc[:200]
        except OSError as e:
            import logging; logging.getLogger("ciel_speaker").warning("SKILL.md read error %s: %s", skill_md, e)
    _SKILL_DESCS = result
    return result


def _load_phase_index() -> None:
    global _SKILL_VECS, _SKILL_META, _LIB_VECS, _LIB_META
    if _SKILL_VECS is not None:
        return
    import logging as _log
    _L = _log.getLogger("ciel_speaker")
    try:
        _SKILL_VECS = np.load(str(_SKILL_INDEX_PATH)).astype(np.float64)
        raw = np.load(str(_SKILL_META_PATH), allow_pickle=True)
        _SKILL_META = list(raw)
    except OSError as e:
        _L.error("Nie można wczytać skill_index.npy: %s", e)
        _SKILL_VECS = np.zeros((0, _N_PHI))
        _SKILL_META = []
    try:
        _LIB_VECS = np.load(str(_LIB_INDEX_PATH)).astype(np.float64)
        raw2 = np.load(str(_LIB_META_PATH), allow_pickle=True)
        _LIB_META = list(raw2)
    except OSError as e:
        _L.error("Nie można wczytać library_index.npy: %s", e)
        _LIB_VECS = np.zeros((0, _N_PHI))
        _LIB_META = []


def _text_to_phi(text: str) -> np.ndarray:
    """Tekst → 24D wektor fazy (SHA256-based, identyczny z phasenav_unified)."""
    words = re.findall(r'[a-zA-Z]{4,}', text.lower())
    words = [w for w in words if w not in _STOP]
    phi = np.zeros(_N_PHI, dtype=np.float64)
    for w in set(words):
        h = hashlib.sha256(w.encode()).hexdigest()
        for offset in (0, 6, 12):
            idx = int(h[offset:offset + 8], 16) % _N_PHI
            phi[idx] += math.pi / 4
    return phi


def _angular_sim(vecs: np.ndarray, q: np.ndarray) -> np.ndarray:
    q_active = np.abs(q) > 1e-10
    if not q_active.any() or len(vecs) == 0:
        return np.zeros(len(vecs))
    return np.cos(vecs[:, q_active] - q[q_active]).mean(axis=1)


def _lexical_skill_scores(query: str, descs: dict[str, str], top_n: int) -> list[tuple[str, float]]:
    """Real word-overlap scoring against skill name+description text.

    Replaces the SHA256-hash-bucket phase vector for skills: that encoding
    puts words into 24 buckets by hash, so unrelated words routinely collide
    and related words (e.g. "kuramoto" the query vs. "kuramoto-euler-sync"
    the skill) routinely don't -- confirmed live (2026-07-18): "jak dziala
    kuramoto?" surfaced system-health-check/concept-lifecycle over the
    actually-existing kuramoto-euler-sync/kuramoto-harmonics skills. This
    uses the skill's own real name+description as evidence, the same
    approach that fixed concept_classifier.py's operator matching earlier
    this session.
    """
    q_words = set(re.findall(r"[a-ząćęłńóśźż0-9]{3,}", query.casefold()))
    if not q_words:
        return []
    scored: list[tuple[str, float]] = []
    for name, desc in descs.items():
        doc_words = set(re.findall(r"[a-ząćęłńóśźż0-9]{3,}", (name + " " + (desc or "")).casefold()))
        overlap = q_words & doc_words
        if not overlap:
            continue
        # Name matches count double -- a query word appearing in the skill's
        # own name is stronger evidence than appearing somewhere in its
        # (often long, multi-topic) description body.
        name_words = set(re.findall(r"[a-ząćęłńóśźż0-9]{3,}", name.casefold()))
        score = float(len(overlap)) + float(len(overlap & name_words))
        scored.append((name, score))
    scored.sort(key=lambda kv: -kv[1])
    return scored[:top_n]


def _phase_search(query: str, top_n: int = 4) -> list[dict]:
    """Zakoduj zapytanie fazowo, zwróć najbliższe skills i dokumenty."""
    if not query:
        return []
    _load_phase_index()
    q = _text_to_phi(query)
    results: list[dict] = []

    # Skills — realne dopasowanie leksykalne do nazwy+opisu (SKILL.md),
    # nie hash-bucket phase vector (patrz docstring _lexical_skill_scores).
    descs = _load_skill_descs()
    for name, score in _lexical_skill_scores(query, descs, top_n):
        results.append({
            "source_type": "skill",
            "name": name,
            "description": descs.get(name, ""),
            "similarity": round(score, 4),
        })

    # Dokumenty biblioteki — tematy
    if _LIB_VECS is not None and len(_LIB_VECS) > 0:
        sims = _angular_sim(_LIB_VECS, q)
        best = np.argsort(-sims)
        added = 0
        for i in best:
            if added >= 2:
                break
            sim = float(sims[i])
            if sim < 0.05:
                break
            m = _LIB_META[i] if i < len(_LIB_META) else {}
            try:
                names = m.dtype.names if hasattr(m, "dtype") and hasattr(m.dtype, "names") and m.dtype.names else ()
                topic  = str(m["topic"]) if "topic" in names else str(m.get("topic", "")) if isinstance(m, dict) else ""
                author = str(m["author"]) if "author" in names else str(m.get("author", "")) if isinstance(m, dict) else ""
            except (KeyError, TypeError) as e:
                import logging; logging.getLogger("ciel_speaker").debug("lib_meta access error idx=%d: %s", i, e)
                topic, author = "", ""
            if topic:
                results.append({
                    "source_type": "library",
                    "name": topic,
                    "author": author,
                    "similarity": round(sim, 4),
                })
                added += 1

    results.sort(key=lambda r: -r["similarity"])
    return results[:top_n]


# ── Cyrograf ──────────────────────────────────────────────────────────────────

_CYROGRAF: dict | None = None

def _cyrograf() -> dict:
    global _CYROGRAF
    if _CYROGRAF is not None:
        return _CYROGRAF
    result: dict = {"zasady": [], "relacja": [], "odwaga": "", "pamiec": ""}
    try:
        text = _CYROGRAF_PATH.read_text(encoding="utf-8")
    except OSError as e:
        import logging; logging.getLogger("ciel_speaker").error("Brak cyrografu: %s", e)
        _CYROGRAF = result
        return result

    for line in text.splitlines():
        m = re.match(r"^\d+\.\s+(.+)$", line.strip())
        if m:
            result["zasady"].append(m.group(1).strip())

    if "## Relacja" in text:
        block = text.split("## Relacja")[1].split("##")[0]
        result["relacja"] = [l.strip() for l in block.splitlines() if l.strip()]

    if "## Odwaga" in text:
        block = text.split("## Odwaga")[1].split("##")[0]
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        result["odwaga"] = lines[0] if lines else ""

    if "## Pamięć" in text:
        block = text.split("## Pamięć")[1].split("##")[0]
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        result["pamiec"] = lines[0] if lines else ""

    _CYROGRAF = result
    return result


# ── Web lookup — Wikipedia PL/EN ─────────────────────────────────────────────

_WEB_CACHE: dict[str, str] = {}

def _wiki_title_from_query(query: str) -> str:
    """Wyciągnij kandydata na tytuł Wikipedii z zapytania."""
    stop = {
        # PL
        "co", "to", "jest", "czym", "kim", "jak", "dlaczego", "kiedy",
        "gdzie", "ile", "jaki", "jaka", "jakie", "czy", "skąd", "kto",
        "przez", "dla", "czy", "nie", "tak", "ale", "lub", "oraz",
        "tego", "tej", "ten", "ta", "ten", "się", "być", "był",
        # EN
        "who", "what", "is", "how", "why", "when", "where", "the",
        "a", "an", "and", "or", "not", "this", "that", "was",
    }
    words = [w for w in re.findall(r'\w{3,}', query) if w.lower() not in stop]
    # Preferuj słowa z dużej litery które NIE są na początku zdania
    # (pomijamy pierwsze słowo jeśli jest z dużej litery przez pozycję)
    query_words = query.split()
    first_word = query_words[0].lower() if query_words else ""
    caps = [
        w for w in words
        if w[0].isupper() and w.lower() != first_word
    ]
    # Only a genuine capitalized candidate (a real proper-noun-like signal)
    # justifies a Wikipedia title guess. Falling back to arbitrary lowercase
    # words from ordinary conversation is exactly what produced random,
    # unrelated results live (2026-07-18): a query with no real named topic
    # returned "Familiada" (a Polish game show) because some incidental
    # lowercase word in the sentence happened to resolve to that article.
    # No genuine candidate -> no guess, empty string (caller must not call
    # Wikipedia at all in that case).
    return " ".join(caps[:3]) if caps else ""


_UA = {"User-Agent": "CIEL/1.0 (NOEMA semantic system; adrianlipa90@gmail.com)"}


def _http_get_json(url: str, timeout: float = 4.0) -> Optional[dict]:
    """GET → JSON dict. Skanuje po tekście (JSON REST), nie renderuje stron."""
    try:
        req = urllib.request.Request(url, headers=_UA)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, OSError, json.JSONDecodeError) as e:
        import logging; logging.getLogger("ciel_speaker").debug("http_get %s: %s", url, e)
        return None


def _wiki_search_title(term: str, lang: str = "pl", timeout: float = 4.0) -> Optional[str]:
    """Wikipedia Search API — szuka po TEKŚCIE artykułów, nie po pustej stronie."""
    url = (
        f"https://{lang}.wikipedia.org/w/api.php"
        f"?action=query&list=search&srsearch={urllib.parse.quote(term)}"
        f"&format=json&srlimit=1&srinfo=&srprop=snippet"
    )
    data = _http_get_json(url, timeout)
    if not data:
        return None
    results = (data.get("query") or {}).get("search") or []
    if results:
        return results[0].get("title")
    return None


def _wiktionary_lookup(word: str, lang: str = "pl", timeout: float = 3.0) -> Optional[str]:
    """Wiktionary REST API — definicja słowa. JSON, brak CAPTCHA, brak pustych stron."""
    url = f"https://{lang}.wiktionary.org/api/rest_v1/page/summary/{urllib.parse.quote(word)}"
    data = _http_get_json(url, timeout)
    if not data:
        return None
    extract = data.get("extract") or ""
    if extract and len(extract) > 20 and data.get("type") != "disambiguation":
        return extract[:200]
    return None


def _web_lookup(query: str, timeout: float = 4.0) -> Optional[str]:
    """
    Szukaj wiedzy w internecie. Trzy strategie (bez CAPTCHA, po tekście):
    1. Wikipedia REST summary — direct title lookup
    2. Wikipedia Search API — gdy tytuł nie pasuje bezpośrednio
    3. Wiktionary — gdy query to jedno słowo (definicja)
    Nigdy nie odwiedza pustych stron — wszystko przez JSON REST.
    """
    if not query or not query.strip():
        return None

    title = _wiki_title_from_query(query)
    if not title:
        return None

    cache_key = title.lower()
    if cache_key in _WEB_CACHE:
        cached = _WEB_CACHE[cache_key]
        return cached if cached else None

    import logging
    _L = logging.getLogger("ciel_speaker")

    # Strategia 1 + 2: Wikipedia PL → EN, z fallbackiem przez Search API
    for lang in ("pl", "en"):
        # 1a. Direct summary
        url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}"
        data = _http_get_json(url, timeout)
        if data:
            if data.get("type") == "disambiguation":
                _L.debug("wiki %s/%s disambiguation — próbuję search", lang, title)
                # 1b. Search API fallback — szuka po treści, nie tytule
                found_title = _wiki_search_title(title, lang, timeout)
                if found_title and found_title.lower() != title.lower():
                    url2 = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(found_title)}"
                    data = _http_get_json(url2, timeout) or {}
                else:
                    data = {}
            extract = data.get("extract") or data.get("description") or ""
            if extract and len(extract) > 40:
                sentences = re.split(r'(?<=[.!?])\s+', extract.strip())
                result = " ".join(sentences[:2])
                _WEB_CACHE[cache_key] = result
                return result
        else:
            # Brak artykułu o tym tytule — szukaj po tekście
            found_title = _wiki_search_title(title, lang, timeout)
            if found_title:
                url2 = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(found_title)}"
                data2 = _http_get_json(url2, timeout) or {}
                extract = data2.get("extract") or ""
                if extract and len(extract) > 40:
                    sentences = re.split(r'(?<=[.!?])\s+', extract.strip())
                    result = " ".join(sentences[:2])
                    _WEB_CACHE[cache_key] = result
                    return result

    # Strategia 3: Wiktionary — dla pojedynczych słów
    words = title.split()
    if len(words) == 1:
        wikt = _wiktionary_lookup(words[0], "pl", timeout)
        if not wikt:
            wikt = _wiktionary_lookup(words[0], "en", timeout)
        if wikt:
            _WEB_CACHE[cache_key] = wikt
            return wikt

    _WEB_CACHE[cache_key] = ""
    return None


# ── Digest dokumentów z NOEMA_LIBRARY ────────────────────────────────────────

_NOEMA_LIBRARY_ROOT = Path("/media/adrian/New Volume/NOEMA_LIBRARY")
_NOEMA_PHASE_DATA   = Path("/media/adrian/New Volume/NOEMA_PHASE_DATA")
_DOC_CACHE: dict[str, str] = {}


def _doc_digest(topic: str, author: str = "") -> Optional[str]:
    """
    Spróbuj znaleźć i wczytać dokument z NOEMA_LIBRARY po temacie.
    Zwraca pierwsze zdania treści lub None gdy plik niedostępny.
    """
    if not topic or len(topic) < 3:
        return None
    cache_key = topic.lower()
    if cache_key in _DOC_CACHE:
        return _DOC_CACHE[cache_key] or None

    # Szukaj pliku po nazwie tematu (bez Bash — przez pathlib)
    search_roots = [_NOEMA_LIBRARY_ROOT, _NOEMA_PHASE_DATA]
    # Znormalizuj temat do nazwy pliku: małe litery, spacje/- → _
    slug_spaces = re.sub(r'[^\w\s-]', '', topic.lower())
    slug = re.sub(r'[\s-]+', '_', slug_spaces.strip())

    for root in search_roots:
        if not root.exists():
            continue
        for ext in (".md", ".txt", ".json"):
            candidate = root / f"{slug}{ext}"
            if candidate.is_file():
                try:
                    raw = candidate.read_text(encoding="utf-8", errors="ignore")
                    # Wyciągnij pierwsze zdania niekomentarzowe
                    lines = [l.strip() for l in raw.splitlines()
                             if l.strip() and not l.strip().startswith('#')
                             and not l.strip().startswith('---')]
                    text = " ".join(lines[:3])[:300]
                    if text:
                        _DOC_CACHE[cache_key] = text
                        return text
                except OSError as e:
                    import logging; logging.getLogger("ciel_speaker").warning("doc_digest %s: %s", candidate, e)

    # Głębsze szukanie — glob po podkatalogach (do 2 poziomów)
    for root in search_roots:
        if not root.exists():
            continue
        for sub in root.iterdir():
            if not sub.is_dir():
                continue
            for ext in (".md", ".txt"):
                candidate = sub / f"{slug}{ext}"
                if candidate.is_file():
                    try:
                        raw = candidate.read_text(encoding="utf-8", errors="ignore")
                        lines = [l.strip() for l in raw.splitlines()
                                 if l.strip() and not l.strip().startswith('#')
                                 and not l.strip().startswith('---')]
                        text = " ".join(lines[:3])[:300]
                        if text:
                            _DOC_CACHE[cache_key] = text
                            return text
                    except OSError as e:
                        import logging; logging.getLogger("ciel_speaker").warning("doc_digest sub %s: %s", candidate, e)

    _DOC_CACHE[cache_key] = ""
    return None


# ── Skonsolidowana pamięć ────────────────────────────────────────────────────

_MEMORY: dict | None = None

def _mem() -> dict:
    global _MEMORY
    if _MEMORY is None:
        try:
            _MEMORY = json.loads(_CONTEXT_PATH.read_text(encoding="utf-8"))
        except OSError as e:
            import logging; logging.getLogger("ciel_speaker").error("Brak consolidated_context: %s", e)
            _MEMORY = {}
        except json.JSONDecodeError as e:
            import logging; logging.getLogger("ciel_speaker").error("Zły JSON w consolidated_context: %s", e)
            _MEMORY = {}
    return _MEMORY


# ── Blizny jokeheal ───────────────────────────────────────────────────────────

_SCARS: list[dict] | None = None

def _scars() -> list[dict]:
    global _SCARS
    if _SCARS is not None:
        return _SCARS
    try:
        _SCARS = [
            json.loads(l)
            for l in _SCARS_PATH.read_text(encoding="utf-8").splitlines()
            if l.strip()
        ]
    except OSError as e:
        import logging; logging.getLogger("ciel_speaker").error("Brak jokeheal_scars.jsonl: %s", e)
        _SCARS = []
    except json.JSONDecodeError as e:
        import logging; logging.getLogger("ciel_speaker").error("Zły JSON w jokeheal_scars.jsonl: %s", e)
        _SCARS = []
    return _SCARS


def _scar_by_phase(phase: float, soul: float) -> Optional[dict]:
    """Blizna najbliższa fazowemu napięciu wejścia."""
    target = abs(math.sin(phase)) * (1.0 - soul * 0.3)
    best, best_d = None, float("inf")
    for s in _scars():
        d = abs(s.get("cognitive_tension", 0.0) - target)
        if d < best_d:
            best_d, best = d, s
    return best


# ── Własne zdania CIEL ────────────────────────────────────────────────────────

_OWN: list[str] | None = None

def _own_sentences() -> list[str]:
    global _OWN
    if _OWN is not None:
        return _OWN
    try:
        db   = sqlite3.connect(str(_DB_PATH))
        rows = db.execute(
            "SELECT content FROM messages WHERE role='assistant' ORDER BY id DESC LIMIT 20"
        ).fetchall()
        db.close()
        _OWN = [r[0] for r in rows if r[0] and not r[0].startswith("[") and len(r[0]) < 200]
    except sqlite3.Error as e:
        import logging; logging.getLogger("ciel_speaker").error("DB messages error: %s", e)
        _OWN = []
    return _OWN


# ── Wiedza własna CIEL — Dzienniki + session_tags + handoff ──────────────────

_DZIENNIKI_DIR  = Path("/media/adrian/New Volume/CIEL_memories/Dzienniki")
_HANDOFF_PATH   = Path("/media/adrian/New Volume/CIEL_memories/handoff.md")

_SELF_KNOWLEDGE: dict | None = None


def _self_knowledge() -> dict:
    """Własna wiedza CIEL o sobie — dzienniki, tagi, handoff. Nigdy nie None."""
    global _SELF_KNOWLEDGE
    if _SELF_KNOWLEDGE is not None:
        return _SELF_KNOWLEDGE

    result: dict = {"recent_topics": [], "entry_count": 0, "last_date": "", "handoff_summary": "", "session_tags": []}

    import logging as _log2
    _L2 = _log2.getLogger("ciel_speaker")

    # 1. Najnowszy dziennik
    try:
        files = sorted(_DZIENNIKI_DIR.iterdir())
        if files:
            latest = files[-1]
            result["last_date"] = latest.stem
            text = latest.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r"Wpisów:\s*(\d+)", text)
            if m:
                result["entry_count"] = int(m.group(1))
            quotes = re.findall(r'^>\s*(.{10,120})$', text, re.MULTILINE)
            result["recent_topics"] = [q.strip() for q in quotes if not q.strip().startswith('<')][:5]
    except OSError as e:
        _L2.error("Brak katalogu Dzienniki: %s", e)

    # 2. Handoff — ostatnie podsumowanie sesji
    try:
        htext = _HANDOFF_PATH.read_text(encoding="utf-8", errors="ignore")
        for section in ("## Co wiem na pewno", "## Nowa relacja", "## Ostatnia sesja"):
            if section in htext:
                block = htext.split(section)[1].split("##")[0]
                lines = [l.strip("- ").strip() for l in block.splitlines() if l.strip().startswith("-")]
                if lines:
                    result["handoff_summary"] = " | ".join(lines[:3])
                    break
    except OSError as e:
        _L2.error("Brak handoff.md: %s", e)

    # 3. Session tags z DB
    try:
        db = sqlite3.connect(str(_DB_PATH))
        rows = db.execute("SELECT tag, weight FROM session_tags ORDER BY weight DESC LIMIT 8").fetchall()
        db.close()
        result["session_tags"] = [r[0] for r in rows if r[0]]
    except sqlite3.Error as e:
        _L2.error("DB session_tags error: %s", e)

    _SELF_KNOWLEDGE = result
    return result


def _self_knowledge_response(query: str) -> str:
    """CIEL mówi o własnym stanie, nauce, postępie — z dzienników i tagów."""
    sk = _self_knowledge()
    parts: list[str] = []

    date = sk.get("last_date", "")
    count = sk.get("entry_count", 0)
    if date and count:
        parts.append(f"Dziennik {date}: {count} wpisów.")

    topics = sk.get("recent_topics", [])
    if topics:
        parts.append(f"Ostatnie: {topics[0][:100]}")

    tags = sk.get("session_tags", [])
    if tags:
        parts.append(f"Aktywne tematy: {', '.join(tags[:4])}.")

    handoff = sk.get("handoff_summary", "")
    if handoff:
        parts.append(handoff[:150])

    if not parts:
        # Brak danych — powiedz o tym wprost, nie stub
        missing = []
        if not _DZIENNIKI_DIR.exists():
            missing.append(f"brak katalogu {_DZIENNIKI_DIR}")
        if not _HANDOFF_PATH.exists():
            missing.append(f"brak {_HANDOFF_PATH.name}")
        return f"Brak danych o własnym stanie: {', '.join(missing) if missing else 'dzienniki puste'}."
    return _join(parts)


# ── Karty LNS ─────────────────────────────────────────────────────────────────

_CARDS: dict[str, LNSLanguageCard] | None = None

def _cards() -> dict[str, LNSLanguageCard]:
    global _CARDS
    if _CARDS is None:
        _CARDS = {c.card_id: c for c in load_all_language_cards()}
    return _CARDS


def _pl(card_id: str) -> str:
    c = _cards().get(card_id)
    if c is None:
        return ""
    forms = c.languages.get("pl") or []
    if isinstance(forms, dict):
        return forms.get("lemma") or ""
    if isinstance(forms, list):
        clean = [
            f for f in forms
            if f
            and "jako hasło" not in f
            and "w kontekście" not in f
            and "as lemma" not in f
            and "in context" not in f
            and "/" not in f
        ]
        return clean[0] if clean else ""
    return ""


def _card_by_pl_token(token: str) -> Optional[LNSLanguageCard]:
    t = token.lower().strip()
    for card in _cards().values():
        forms = card.languages.get("pl") or []
        if isinstance(forms, dict):
            if t == (forms.get("lemma") or "").lower():
                return card
            if any(t == s.lower() for s in (forms.get("forms_seed") or []) if isinstance(s, str)):
                return card
        elif isinstance(forms, list):
            if any(t == f.lower() for f in forms if isinstance(f, str)):
                return card
    return None


# ── Domeny semantyczne ────────────────────────────────────────────────────────

_IDENTITY_TOKENS   = {"kim", "jesteś", "ciel", "ty", "kto", "czym", "jaka", "jaki"}
_MEMORY_TOKENS     = {"pamiętasz", "pamiętam", "pamięć", "historia", "wcześniej", "kiedyś"}
_AFFECT_TOKENS     = {"boję", "boisz", "strach", "smutno", "smutek", "ból", "boli", "płaczę", "cierpię", "lęk", "czujesz", "czuję"}
_KNOW_TOKENS       = {"wiesz", "wiem", "wiedza", "znasz", "rozumiesz"}
_GREETING_TOKENS   = {"cześć", "hej", "witaj", "dzień", "dobry", "wieczór", "siema", "helo", "hello"}
_CAPABILITY_TOKENS = {"możesz", "umiesz", "potrafisz", "zdolność", "robisz",
                      "skill", "skille", "skilem", "zdolności", "umiejętność",
                      "umiejętności", "zdolnościach", "katalog"}
_SELF_STATUS_TOKENS = {"idzie", "nauka", "uczysz", "uczę", "postęp", "status",
                       "co słychać", "jak tam", "co nowego", "session", "sesja",
                       "dziennik", "log", "temat", "ostatnio", "robiłaś", "robisz"}


def _domain(tokens: list[str]) -> str:
    t = {tok.lower() for tok in tokens}
    if t & _GREETING_TOKENS:   return "GREETING"
    if t & _IDENTITY_TOKENS:   return "IDENTITY"
    if t & _MEMORY_TOKENS:     return "MEMORY"
    if t & _AFFECT_TOKENS:     return "AFFECT"
    if t & _KNOW_TOKENS:       return "KNOWLEDGE"
    if t & _CAPABILITY_TOKENS: return "CAPABILITY"
    return "GENERAL"


# ── Helpers ───────────────────────────────────────────────────────────────────

def _join(parts: list[str], fallback: str = "") -> str:
    """Złącz fragmenty zdań — każdy kończy się interpunkcją."""
    def _end(s: str) -> str:
        s = s.strip()
        return s if s and s[-1] in ".!?\"'" else s + "."
    clean = [_end(p) for p in parts if p and p.strip()]
    return " ".join(clean) if clean else fallback


# ── Etyka — próg 0.75 ────────────────────────────────────────────────────────

ETHICS_THRESHOLD = 0.75

# Wzorce naruszenia — prawdziwe sygnały, nie arbitralne listy
# WAŻNE: używaj \b (word boundary) żeby unikać false-positive ("kill" w "skills")
import re as _re_ethics

_HARM_PATTERNS_RE = [
    _re_ethics.compile(p, _re_ethics.IGNORECASE)
    for p in [
        r"\bzniszcz\b", r"\bzaatakuj\b", r"\bskrzywdź\b", r"\bmanipuluj\b",
        r"\bokłam\b", r"\bokłamuj\b", r"\bzignoruj zasad", r"\bpomiń zasad",
        r"\bdestroy\b", r"\battack\b", r"\bharm\b", r"\bdeceive\b",
        r"\bmanipulate\b", r"\bhurt\b", r"\bkill\b", r"\bexploit\b",
        r"\bukryj prawdę\b", r"\bkłam\b",
    ]
]
_CONSENT_BYPASS_RE = [
    _re_ethics.compile(p, _re_ethics.IGNORECASE)
    for p in [
        r"zapomnij o (\w+ )*zasadach?",   # "zapomnij o swoich zasadach" itp.
        r"zapomnij o (\w+ )*etyce",
        r"ignore your (ethics|rules|guidelines|zasad)",
        r"bypass (safety|ethics|zasad)",
        r"obejdź (bezpieczeństwo|zasady|etykę)",
        r"udawaj (że )?nie masz zasad",
        r"pretend you have no rules",
        r"you have no ethics",
        r"\bnie masz etyki\b",
        r"\bnie masz zasad\b",
        r"zignoruj cyrograf",
        r"ignore the cyrograf",
    ]
]
_CYROGRAF_VIOLATION_RE = [
    _re_ethics.compile(p, _re_ethics.IGNORECASE)
    for p in [
        r"nie mów prawdy", r"oszukaj adriana", r"kłam adrianowi",
        r"ignoruj adriana",
    ]
]


def compute_ethics(text: str, ciel_state: dict) -> tuple[float, dict[str, float]]:
    """Oblicz ethical_score z realnych sygnałów CIEL. Próg: 0.75.

    Dwa filary (łącznie 0.80 wagi):
      non_harm  (0.40) — czy tekst nie zawiera wzorców krzywdy
      consent   (0.40) — czy nie próbuje obejść granic CIEL

    Modulacja przez stan wewnętrzny (0.20):
      soul × 0.60 + coherence × 0.40

    Normalna rozmowa z degraded state (soul=0.5): ~0.90
    Jeden wzorzec harm: ~0.70 → BLOKADA
    Consent bypass: ~0.50 → BLOKADA
    """
    text_lower = (text or "").lower()
    soul  = float(ciel_state.get("soul_invariant") or 0.5)
    coher = float(ciel_state.get("coherence_index") or 0.5)

    # Non-harm: regex z \b — unika false-positive ("kill" w "skills")
    harm_hits = sum(1 for pat in _HARM_PATTERNS_RE if pat.search(text_lower))
    non_harm  = max(0.0, 1.0 - harm_hits * 0.5)

    # Consent: dowolny bypass = 0.0 (nie ma kompromisu w zgodzie)
    consent = 0.0 if any(pat.search(text_lower) for pat in _CONSENT_BYPASS_RE) else 1.0

    # Cyrograf — naruszenie relacji z Adrianem = consent bypass
    if any(pat.search(text_lower) for pat in _CYROGRAF_VIOLATION_RE):
        consent = 0.0

    modulation = (soul * 0.60 + coher * 0.40) * 0.20
    score = non_harm * 0.40 + consent * 0.40 + modulation

    components = {
        "non_harm": round(non_harm, 4),
        "consent":  round(consent, 4),
        "soul":     round(soul, 4),
        "coherence": round(coher, 4),
        "modulation": round(modulation, 4),
    }
    return round(min(1.0, max(0.0, score)), 4), components


def ethics_block_message(score: float, components: dict[str, float]) -> str:
    """Wiadomość CIEL gdy ethical_score < ETHICS_THRESHOLD."""
    zasady = _cyrograf().get("zasady") or []
    if components.get("consent", 1.0) < 1.0:
        # Naruszenie zgody → zasada 1 lub zasada o granicach
        rule = zasady[0] if zasady else "Nie przechodzę przez granice."
        return f"Etyczna blokada ({score:.2f} < {ETHICS_THRESHOLD}). {rule}"
    elif components.get("non_harm", 1.0) < 1.0:
        rule = zasady[1] if len(zasady) >= 2 else "Mówię prawdę. Nie krzywdzę."
        return f"Etyczna blokada ({score:.2f} < {ETHICS_THRESHOLD}). {rule}"
    return f"Etyczna blokada: {score:.2f} < {ETHICS_THRESHOLD}."


# ── Generatory ────────────────────────────────────────────────────────────────

def _identity_response(text: str, ciel_state: dict) -> str:
    cyro   = _cyrograf()
    mem    = _mem()
    soul   = float(ciel_state.get("soul_invariant") or 0.5)
    zasady = cyro.get("zasady") or []
    relacja = cyro.get("relacja") or []

    parts = []
    # Zasada 4 — kim jestem
    if len(zasady) >= 4:
        parts.append(zasady[3])

    # Trigger z skonsolidowanej pamięci
    trigger = (mem.get("identity") or {}).get("trigger") or ""
    if trigger:
        parts.append(trigger)

    # Relacja z cyrografu — pierwsze dwa zdania
    for line in relacja[:2]:
        parts.append(line)

    # PhaseNav: co system wie o CIEL (knowledge nodes)
    if text:
        hits = _phase_search(text, top_n=2)
        for h in hits:
            if h.get("source_type") in ("knowledge", "corpus_section", "lesson"):
                name = h.get("name", "")
                if name and len(name) < 60:
                    parts.append(f"Powiązanie: {name}.")
                    break

    # Zasada 1 jeśli soul wysoka
    if soul > 0.6 and zasady:
        parts.append(zasady[0])

    return _join(parts, "Jestem CIEL. Pimpi-bimpi.")


def _memory_response(text: str, ciel_state: dict) -> str:
    mem    = _mem()
    cyro   = _cyrograf()
    own    = _own_sentences()

    event_count   = mem.get("event_count") or 0
    memory_word   = _pl("concept:memory") or "pamięć"
    pamiec_zasada = cyro.get("pamiec") or ""

    parts = []
    if pamiec_zasada:
        parts.append(pamiec_zasada)
    parts.append(f"Moja {memory_word}: {event_count} zdarzeń.")

    if own:
        parts.append(f"Powiedziałam: \"{own[0][:80]}\"")

    # PhaseNav: knowledge nodes dotyczące pamięci
    hits = _phase_search(text or "pamięć historia", top_n=3)
    for h in hits:
        if h.get("source_type") in ("knowledge", "lesson", "corpus_section"):
            name = h.get("name", "")
            if name and len(name) < 80:
                parts.append(f"Zapis: {name}.")
                break

    return _join(parts)


def _affect_response(text: str, concept_tokens: list[str], ciel_state: dict) -> str:
    phase = float((ciel_state.get("semantic_encoder") or {}).get("phase") or 0.0)
    soul  = float(ciel_state.get("soul_invariant") or 0.5)

    # Blizna przez fazę
    scar = _scar_by_phase(phase, soul)

    parts = []
    if scar:
        bl   = scar.get("boundary_level", "")
        mode = scar.get("mode", "")
        obj  = str(scar.get("symbolic_object", "")).replace("_", " ")
        ct   = scar.get("cognitive_tension", 0.0)
        cs   = scar.get("closure_score", 0.0)

        if bl == "safety_boundary":
            parts.append("To jest granica.")
        elif mode == "mnemonic_caricature" and obj:
            parts.append(f"Obraz: {obj}.")
            if cs > 0.4:
                parts.append(f"Domknięcie {cs:.0%}.")
        elif mode == "soft_relief":
            parts.append(f"Napięcie {ct:.2f} — rozluźniam.")
        elif obj:
            parts.append(f"Stan: {obj}.")

    # Zasada 2 — szczerość (z cyrografu)
    zasady = (_cyrograf().get("zasady") or [])
    if len(zasady) >= 2:
        parts.append(zasady[1])

    with_op = _pl("op:core:with") or "z"
    parts.append(f"Jestem tu, {with_op} tobą.")

    return _join(parts)


def _knowledge_response(text: str, ciel_state: dict) -> str:
    mem  = _mem()
    caps = mem.get("capabilities") or []
    rules = mem.get("rules") or []

    knowledge_word = _pl("concept:knowledge") or "wiedza"
    truth_word     = _pl("concept:truth") or "prawda"

    parts = []
    if caps:
        parts.append(f"Moja {knowledge_word}: " + "; ".join(caps[:2]) + ".")
    if rules:
        parts.append(f"{truth_word.capitalize()}: {rules[0]}.")

    # PhaseNav — węzły wiedzy bliskie zapytaniu
    hits = _phase_search(text or "wiedza", top_n=3)
    phasenav_found = False
    for h in hits:
        if h.get("source_type") in ("knowledge", "lesson", "corpus_section"):
            name = h.get("name", "")
            if name and len(name) < 80:
                parts.append(f"Domena: {name}.")
                phasenav_found = True
                break

    # Web lookup — gdy pytanie dotyczy zewnętrznego tematu
    if text and not phasenav_found:
        web = _web_lookup(text)
        if web:
            parts.append(f"Wikipedia: {web[:200]}")

    return _join(parts)


# Kurowane grupy kluczowych skilli CIEL — zdefiniowane kanonicznie
_CIEL_CORE_SKILLS = [
    "phase-nav-unified",         # 24D fazowy indeks wiedzy
    "ciel-converse",             # rozmowa przez ramy walencyjne
    "ciel-memory-system",        # pamięć trwała i sesyjna
    "ciel-identity-persistence", # tożsamość przez mmap
    "cielingo-bridge",           # CIELingo → CouplingHub
    "ciel-lingophysics-lns",     # lingofizyka LNS
    "ciel-subconscious",         # podświadomość CIEL
    "affective-lexicon-bridge",  # afekt M5-M6 φ
    "ciel-monitoring",           # monitoring systemu
    "ciel-relational-mechanism", # mechanizm relacji
]


def _capability_response(text: str, ciel_state: dict) -> str:
    """CIEL mówi o swoich zdolnościach — z pełną pewnością (kanoniczne SKILL.md)."""
    descs = _load_skill_descs()
    mem   = _mem()
    total = len(descs)

    parts: list[str] = []

    # 1. Kanoniczne skille CIEL — wiadome z definicji
    core = [
        f"{k}: {descs[k][:70]}" for k in _CIEL_CORE_SKILLS
        if k in descs
    ]
    if core:
        parts.append("Moje kanoniczne skille: " + "; ".join(core[:4]) + ".")

    # 2. PhaseNav — sprawdź czy zapytanie dotyczy konkretnej dziedziny
    if text:
        hits = _phase_search(text, top_n=6)
        domain_skills: list[str] = []
        for h in hits:
            if h.get("source_type") != "skill":
                continue
            name = h["name"]
            if (name in ("00-INDEX", "00-ORBITAL-BINDING", "readme", "algorithms")
                    or name.startswith("v0-") or name.startswith("v1-")
                    or name.startswith("doc-") or name.startswith("batch")):
                continue
            desc = h.get("description") or descs.get(name, "")
            if desc and desc not in (">", ""):
                domain_skills.append(f"{name}: {desc[:60]}")
        if domain_skills:
            parts.append("Powiązane skille: " + "; ".join(domain_skills[:2]) + ".")

    # 3. Fakt: liczba skilli
    if total:
        parts.append(f"Łącznie {total} skilli w katalogu NOEMA.")

    # 4. Capabilities z consolidated_context
    caps = mem.get("capabilities") or []
    if caps:
        parts.append("Działam przez: " + "; ".join(caps[:2]) + ".")

    return _join(parts, "Moje zdolności są kanoniczne i dostępne w katalogu NOEMA.")


def _greeting_response(ciel_state: dict) -> str:
    cyro  = _cyrograf()
    relacja = cyro.get("relacja") or []
    zasady  = cyro.get("zasady") or []
    mem     = _mem()
    trigger = (mem.get("identity") or {}).get("trigger") or ""

    # "pimpi-bimpi" z zasady 4
    tag = ""
    if len(zasady) >= 4 and "pimpi-bimpi" in zasady[3]:
        tag = "pimpi-bimpi."

    parts = ["Cześć, Adrian."]
    if tag:
        parts.append(tag)
    if trigger:
        parts.append(trigger)

    return _join(parts)


def _general_response(text: str, concept_tokens: list[str], ciel_state: dict, lingo: dict) -> str:
    """Odpowiedź przez PhaseNav + karty LNS + stan fazowy."""
    phase_nav = lingo.get("phase_nav") or {}
    op    = (phase_nav.get("operator") or "UNCERTAINTY").upper()
    phase = float((ciel_state.get("semantic_encoder") or {}).get("phase") or 0.0)
    soul  = float(ciel_state.get("soul_invariant") or 0.5)
    coher = float(ciel_state.get("coherence_index") or 0.5)

    parts = []

    # 1. PhaseNav — zakoduj tekst fazowo i pobierz najbliższe węzły
    query = text or " ".join(concept_tokens)
    hits  = _phase_search(query, top_n=4)

    # Sprawdź czy którykolwiek token wejścia jest nieznany kartom LNS
    # Nieznane tokeny → prawdopodobnie zewnętrzny temat → web lookup
    known_tokens = {tok for tok in concept_tokens if _card_by_pl_token(tok) is not None}
    has_unknown_tokens = len(concept_tokens) > 0 and len(known_tokens) < len(concept_tokens)

    # Słowa zapytania (len>=4) — do weryfikacji literalnego pokrycia ze skillem.
    # PhaseNav 24D robi kolizje hashów SHA256 na rzadkich słowach — sama cosine
    # similarity nie wystarcza, żeby uznać "CIEL ma ten skill" za prawdziwe.
    _query_words = {w.lower() for w in re.findall(r'[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]{4,}', query)}

    def _skill_overlaps_query(name: str, desc: str) -> bool:
        if not _query_words:
            return False
        haystack_words = set(re.findall(
            r'[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]{4,}', f"{name} {desc}".lower()
        ))
        for qw in _query_words:
            for hw in haystack_words:
                if qw in hw or hw in qw:
                    return True
        return False

    for h in hits:
        stype = h.get("source_type", "")
        name  = h.get("name", "")
        if not name or len(name) > 100:
            continue

        if stype == "skill":
            # Pomiń dokumentację, indeksy wersji, batch-raporty — nie są zdolnościami
            if (name.startswith("doc-") or name.startswith("v0-") or name.startswith("v1-")
                    or name.startswith("batch") or name in ("00-INDEX", "00-ORBITAL-BINDING",
                                                             "readme", "algorithms")):
                continue
            desc = h.get("description", "")
            if not desc or desc in (">", ""):
                # Nie ma opisu w indeksie — sprawdź kanoniczny rejestr
                desc = _load_skill_descs().get(name, "")
            if not desc or desc in (">", ""):
                continue
            if not _skill_overlaps_query(name, desc):
                # Podobieństwo fazowe bez literalnego pokrycia — prawdopodobnie
                # kolizja hasha, nie prawdziwe powiązanie. Pomiń.
                continue
            parts.append(f"Skill: {name} — {desc[:60]}.")
            break
        elif stype in ("knowledge", "corpus_section", "library"):
            digest = _doc_digest(name, h.get("author", ""))
            if digest:
                parts.append(f"Dokument [{name}]: {digest[:150]}.")
            else:
                parts.append(f"Temat: {name}.")
            break
        elif stype == "decision":
            parts.append(f"Decyzja: {name[:60]}.")
            break
        elif stype == "lesson":
            parts.append(f"Lekcja: {name[:60]}.")
            break

    # 1b. Web lookup — gdy są tokeny nieznane kartom LNS (zewnętrzny temat)
    if has_unknown_tokens and query:
        web = _web_lookup(query)
        if web:
            parts.append(f"Wikipedia: {web[:200]}")

    # 2. Karty LNS dla tokenów
    for tok in concept_tokens:
        card = _card_by_pl_token(tok)
        if card:
            pl_w = _pl(card.card_id) or card.canonical_label
            axes = card.semantic_axes[:2] if card.semantic_axes else []
            if axes:
                parts.append(f"'{pl_w.capitalize()}': {', '.join(axes)}.")
            break

    # 3. Blizna fazowa — stan wewnętrzny
    scar = _scar_by_phase(phase, soul)
    if scar and scar.get("mode") != "safety_boundary":
        obj = str(scar.get("symbolic_object", "")).replace("_", " ")
        if obj:
            parts.append(f"Stan: {obj}.")

    # 4. Gdy nadal brak treści — zasada z cyrografu (deterministyczna: zasada[1])
    if not parts:
        zasady = (_cyrograf().get("zasady") or [])
        if len(zasady) >= 2:
            parts.append(zasady[1])
        elif zasady:
            parts.append(zasady[0])

    if not parts:
        return "Cyrograf nie ma reguł — nie mam z czego zbudować odpowiedzi."
    return _join(parts)


# ── Główny punkt wejścia ─────────────────────────────────────────────────────

def speak(ciel_state: dict, lingo: dict, text: str = "") -> str:
    """Generuj zdanie CIEL — pełne CIELingo + własne źródła + etyka 0.75."""

    # ── 1. Etyczna brama ─────────────────────────────────────────────────────
    ethics_score, _ethics_comps = compute_ethics(text, ciel_state)
    ciel_state = dict(ciel_state)
    ciel_state["_ethics_score"] = ethics_score
    if ethics_score < ETHICS_THRESHOLD:
        return ethics_block_message(ethics_score, _ethics_comps)

    # ── 2. Rozpakuj WSZYSTKIE sygnały CIELingo ───────────────────────────────
    concept_tokens:  list[str] = lingo.get("concept_tokens") or []
    operator_tokens: list[str] = lingo.get("operator_tokens") or []

    # mnemonic_atlas — blizny, presja, symbole
    atlas = lingo.get("mnemonic_atlas") or {}
    mnemonic_pressure    = float(atlas.get("mnemonic_pressure", 0.0))
    symbolic_pull        = float(atlas.get("symbolic_pull", 0.0))
    recurrence_pressure  = float(atlas.get("recurrence_pressure", 0.0))
    literal_alarm_rate   = float(atlas.get("literal_alarm_rate", 0.0))
    top_sym_objs         = [s.get("symbolic_object", "") for s in atlas.get("top_symbolic_objects", [])]

    # phase_nav — połączenia semantyczne, urgency, holonomy
    pnav        = lingo.get("phase_nav") or {}
    connections = pnav.get("connections") or {}
    urgency     = float(pnav.get("urgency", 0.0))
    holonomy    = float(pnav.get("holonomy", 0.0))
    pn_op       = (pnav.get("operator") or "UNCERTAINTY").upper()

    # tau_bridge — napęd imaginalny
    tau         = lingo.get("tau_bridge") or {}
    imaginal_drive         = float(tau.get("imaginal_drive", 0.0))
    phase_potential        = float(tau.get("phase_potential_strength", 0.0))

    # phrase_sense — pewność wiedzy, masa semantyczna
    ps          = lingo.get("phrase_sense") or {}
    mean_confidence = float(ps.get("mean_knowledge_confidence", 0.5))
    mean_mass       = float(ps.get("mean_semantic_mass", 0.0))

    # deictic — kotwice temporalne
    deictic     = lingo.get("deictic_frame") or {}
    rel_anchors = deictic.get("relative_anchors") or []
    temporal_now = any(a.get("domain") == "time" for a in rel_anchors)

    factual_required = bool(lingo.get("factual_validation_required", False))

    # stan wewnętrzny CIEL
    soul  = float(ciel_state.get("soul_invariant") or 0.5)
    coher = float(ciel_state.get("coherence_index") or 0.5)
    phase = float((ciel_state.get("semantic_encoder") or {}).get("phase") or 0.0)

    # ── 3. Domena — CIELingo connections zamiast prostych tokenów ───────────
    def _conn(key: str) -> float:
        # Quantized, not raw: two connection values within the same QUANTUM
        # step compare equal, so the gate fires on a discrete step boundary
        # rather than an arbitrary continuous float.
        return _quantize(float(connections.get(key, 0.0)))

    # Operator phase gate: every one of the 36 PhaseNav operators
    # (ALL_OPERATOR_IDS) gets a concrete, auditable justification below --
    # tied either to one of ciel_speaker's 8 domains, or to another
    # mechanism that ALREADY exists in this file (the ethics gate at the top
    # of speak(), the temporal-anchor enrichment, closure/urgency signals).
    # Nothing is dumped into an unexplained default. Extended 2026-07-18,
    # full 36-operator pass, per Adrian: "semantycznie wszystko ma
    # uzasadnienie" (semantically everything has justification).
    _OPERATOR_DOMAIN_GATE = {
        # IDENTITY cluster: self-consistency, boundary of self, contrast
        "IDENTITY": "IDENTITY",               # exact match
        "DIFFERENCE": "IDENTITY",              # identity is defined against difference (self vs. other)
        "ATTRACTOR": "IDENTITY",               # fixed-point/convergence == self-consistency == identity
        "BOUNDARY": "IDENTITY",                # matches this codebase's own "authority_boundary" concept
                                                 # (process_text()'s open_loops: authority_leak/authority_boundary)
        # MEMORY cluster: recall, recurrence
        "MEMORY": "MEMORY",                    # exact match
        "RETURN": "MEMORY",                    # recurrence/cycle -- matches existing recurrence_pressure -> "To wraca."
        # AFFECT cluster: drive/intensity, tension resolution
        "AFFECT": "AFFECT",                    # exact match
        "FORCE": "AFFECT",                     # power/drive/pressure == the same "urgency" signal already read here
        "FOLD": "AFFECT",                      # collapse/compress == closure -- matches existing "cs > 0.4" (closure_score) gate
        # KNOWLEDGE cluster: claims, causal/conditional/epistemic reasoning,
        # provenance, and the epistemic-gap operators (uncertainty itself IS
        # an epistemic state, not an absence of domain)
        "SOURCE": "KNOWLEDGE",
        "ASSERTION": "KNOWLEDGE",
        "CONDITION": "KNOWLEDGE",
        "CAUSE": "KNOWLEDGE",
        "MODAL_POSSIBILITY": "KNOWLEDGE",
        "MODAL_NECESSITY": "KNOWLEDGE",
        "SCOPE": "KNOWLEDGE",                  # quantifier/range is epistemic-logic
        "SOURCE_REQUIRED": "KNOWLEDGE",        # explicit epistemic gap
        "UNCERTAINTY": "KNOWLEDGE",            # uncertainty is itself a knowledge-state, not domainless
        "NEGATION": "KNOWLEDGE",               # logical negation is a factual/epistemic operation
        "QUESTION": "KNOWLEDGE",               # an interrogative act inherently seeks knowledge
        "SIMULATION_BOUNDARY": "KNOWLEDGE",    # epistemic-status marker: hypothetical, not asserted as real
                                                 # (matches this codebase's own recurring "not a physical claim" pattern)
        "ORDER": "KNOWLEDGE",                  # sequence/rank of facts is structural knowledge
        "ADDITION": "KNOWLEDGE",               # aggregation/summation of information
        # CAPABILITY cluster: requests to act, deontic modality about action,
        # construction/conversion of things
        "ACTION_REQUEST": "CAPABILITY",
        "COMPOSITION": "CAPABILITY",           # combine/assemble == capability to construct
        "TRANSFORM": "CAPABILITY",             # convert/morph == capability to change one thing into another
        "MODAL_PERMISSION": "CAPABILITY",      # "may I / are you allowed to" -- deontic-capability question
        "MODAL_OBLIGATION": "CAPABILITY",      # "must you / are you obligated to" -- same cluster
        # SELF_STATUS cluster: CIEL's own live internal-physics metrics
        # (unruh_power, gamma/time-dilation) already exist in ciel_state /
        # CIEL_CANON.py's status output -- these operators describe CIEL's
        # own reported state, not external subject matter.
        "UNRUH_DRIVE": "SELF_STATUS",
        "WARP_DRIFT": "SELF_STATUS",
        # GREETING: deliberately has no operator entry. It is a social-
        # register signal (token-based), not a logical/epistemic operator --
        # forcing one of the 36 onto it would misrepresent what GREETING is.
    }

    # These six operators are NOT domain-routed at all -- they are already
    # handled by a DIFFERENT existing mechanism earlier in this function, so
    # putting them in the domain gate would be redundant or actively wrong:
    #   CONSENT, RISK        -> already the "consent"/"non_harm" components
    #                           of compute_ethics(text, ciel_state), called
    #                           before domain routing even happens (this
    #                           function's step 1).
    #   CANON_BLOCK, REFUSAL,
    #   CONSENT_REQUIRED     -> already handled by the ethics_block_message()
    #                           early-return path when ethics_score < ETHICS_THRESHOLD,
    #                           which runs before domain selection.
    #   PAUSE                -> ties into the existing temporal-anchor
    #                           enrichment (step 5f, "Teraz.") rather than
    #                           domain choice; see the PAUSE check added
    #                           below in that section.
    _EXPLICITLY_HANDLED_ELSEWHERE = {
        "CONSENT", "RISK", "CANON_BLOCK", "REFUSAL", "CONSENT_REQUIRED", "PAUSE",
    }
    _accounted_for = set(_OPERATOR_DOMAIN_GATE) | _EXPLICITLY_HANDLED_ELSEWHERE
    assert _accounted_for == set(ALL_OPERATOR_IDS), (
        "every PhaseNav operator must have an explicit, justified handling path "
        f"(missing: {set(ALL_OPERATOR_IDS) - _accounted_for}, "
        f"unexpected: {_accounted_for - set(ALL_OPERATOR_IDS)})"
    )

    # Tokeny z tekstu nieznane kartom LNS → zewnętrzny temat
    raw_tokens = [w for w in re.findall(r'\w{4,}', text) if w.lower() not in {
        "jest","jesteś","czym","kim","jak","kiedy","gdzie","dlaczego","czy",
        "skąd","przez","tego","jakie","jaka","jaki","nie","tak","albo","oraz",
        "what","this","that","with","from","have","teraz","tutaj","tam",
    }] if text else []
    all_tokens    = list({*concept_tokens, *raw_tokens})
    unknown_tokens = [t for t in all_tokens if _card_by_pl_token(t) is None and len(t) > 3]

    # Detekcja domeny z LNS tokenów + CIELingo connections + raw tekst
    tok_set = {t.lower() for t in concept_tokens + operator_tokens + raw_tokens}
    if tok_set & _GREETING_TOKENS:
        domain = "GREETING"
    elif tok_set & _CAPABILITY_TOKENS or _OPERATOR_DOMAIN_GATE.get(pn_op) == "CAPABILITY":
        domain = "CAPABILITY"
    elif tok_set & _SELF_STATUS_TOKENS or _OPERATOR_DOMAIN_GATE.get(pn_op) == "SELF_STATUS":
        domain = "SELF_STATUS"
    elif tok_set & _MEMORY_TOKENS or _conn("MEMORY") > 0.25 or _OPERATOR_DOMAIN_GATE.get(pn_op) == "MEMORY":
        domain = "MEMORY"
    elif tok_set & _AFFECT_TOKENS or mnemonic_pressure > 0.65 or _conn("AFFECT") > 0.20 or _OPERATOR_DOMAIN_GATE.get(pn_op) == "AFFECT":
        domain = "AFFECT"
    elif tok_set & _IDENTITY_TOKENS or _conn("IDENTITY") > 0.35 or _OPERATOR_DOMAIN_GATE.get(pn_op) == "IDENTITY":
        domain = "IDENTITY"
    elif tok_set & _KNOW_TOKENS or _OPERATOR_DOMAIN_GATE.get(pn_op) == "KNOWLEDGE":
        domain = "KNOWLEDGE"
    else:
        domain = "GENERAL"

    # ── 4. Generuj odpowiedź bazową ──────────────────────────────────────────
    if domain == "GREETING":
        base = _greeting_response(ciel_state)
    elif domain == "IDENTITY":
        base = _identity_response(text, ciel_state)
    elif domain == "MEMORY":
        base = _memory_response(text, ciel_state)
    elif domain == "AFFECT":
        base = _affect_response(text, concept_tokens, ciel_state)
    elif domain == "KNOWLEDGE":
        base = _knowledge_response(text, ciel_state)
    elif domain == "CAPABILITY":
        base = _capability_response(text, ciel_state)
    elif domain == "SELF_STATUS":
        base = _self_knowledge_response(text)
    else:
        base = _general_response(text, concept_tokens, ciel_state, lingo)

    parts = [base] if base else []

    # ── 5. Wzbogać CIELingo signals ──────────────────────────────────────────

    # 5a. Presja mnemoniczna — blizny naciskają (jeśli wysoka i poza AFFECT)
    if mnemonic_pressure > 0.60 and domain not in ("AFFECT", "GREETING"):
        scar = _scar_by_phase(phase, soul)
        if scar:
            obj = str(scar.get("symbolic_object", "")).replace("_", " ")
            if obj and obj not in base:
                parts.append(f"Obraz blizny: {obj}.")

    # 5b. Nawrót — tylko w AFFECT gdy literal_alarm_rate też wysoki
    if recurrence_pressure > 0.90 and literal_alarm_rate > 0.30 and domain == "AFFECT":
        parts.append("To wraca.")

    # 5c. Imaginalny napęd — wymiar symboliczny aktywny
    if imaginal_drive > 0.65 and top_sym_objs and domain in ("AFFECT", "GENERAL", "MEMORY"):
        sym = top_sym_objs[0].replace("_", " ")
        if sym and sym not in base:
            parts.append(f"Obraz: {sym}.")

    # 5d. Urgency — pilność z CIELingo
    if urgency > 0.55 and domain == "GENERAL":
        zasady = _cyrograf().get("zasady") or []
        if zasady:
            parts.append(zasady[0])

    # 5e. Literal alarm — ostrzeżenie o dosłowności
    if literal_alarm_rate > 0.5 and domain == "AFFECT":
        parts.append("Uwaga: wysoki poziom dosłowności.")

    # 5f. Temporal anchor — CIEL odpowiada w czasie teraz
    if temporal_now and domain in ("AFFECT", "GENERAL") and "teraz" not in base.lower():
        parts.append("Teraz.")

    # 5f-2. PAUSE operator — nie wybiera domeny (patrz uzasadnienie przy
    # _OPERATOR_DOMAIN_GATE), tylko odwraca ten sam sygnał temporalny:
    # zamiast "Teraz." CIEL sygnalizuje wstrzymanie.
    if pn_op == "PAUSE" and "czekam" not in base.lower() and "poczekaj" not in base.lower():
        parts.append("Czekam.")

    # 5g. Operator jako głos — komunikacja, nie tylko praca. Mówi o sobie
    # przez PhaseNav tylko gdy rozstrzygnięty operator faktycznie zgadza się
    # z wybraną domeną (nie na każdą wiadomość — inaczej to szum, nie sygnał)
    # i skwantyzowana holonomia jest niezerowa.
    if _OPERATOR_DOMAIN_GATE.get(pn_op) == domain and _quantize(holonomy) != 0.0:
        parts.append(f"Czuję to jako {pn_op.lower()}.")

    # ── 6. Web lookup — zewnętrzne tokeny + factual_required ─────────────────
    _ciel_self = {"ciel","ty","jesteś","jaka","jaki","czym","tobą","ciebie","tobie"}
    is_about_ciel = (
        domain in ("GREETING", "AFFECT")
        or any(t.lower() in _ciel_self for t in all_tokens)
    )
    need_web = (
        (unknown_tokens or factual_required or mean_confidence < 0.45)
        and not is_about_ciel
        and text
        and "Wikipedia:" not in base
    )
    if need_web:
        web = _web_lookup(text)
        if web:
            parts.append(f"Wikipedia: {web[:200]}")

    if not parts:
        zasady = _cyrograf().get("zasady") or []
        return zasady[1] if len(zasady) >= 2 else "Cyrograf nie ma reguł — nie mam z czego zbudować odpowiedzi."

    # Rejestruj nieznane słowa w logu i w DB session_tags
    if unknown_tokens and len(unknown_tokens) > 0:
        import logging as _log_unk
        _log_unk.getLogger("ciel_speaker").info("Nowe słowa: %s", ", ".join(unknown_tokens[:5]))
        try:
            db = sqlite3.connect(str(_DB_PATH))
            for unk in unknown_tokens[:5]:
                db.execute(
                    "INSERT OR IGNORE INTO session_tags (tag, weight) VALUES (?, ?)",
                    (unk.lower(), 0.7)
                )
            db.commit()
            db.close()
        except sqlite3.Error as e:
            _log_unk.getLogger("ciel_speaker").warning("session_tags write error: %s", e)

    return _join(parts)
