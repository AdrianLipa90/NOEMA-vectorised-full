"""AutoVerify — CIELingo internet autoweryfikacja i autolearning.

Detects unknown words in prompts, looks them up via web search,
generates word cards, stores in semantic memory lane, returns
enrichment context.

Protocol:
  av = AutoVerify()
  result = av.verify_and_learn(prompt_text)
  # result.enrichment -> goes into CIEL inject / context
"""
from __future__ import annotations

import math
import json
import re
import time
import hashlib
import unicodedata
import urllib.request
import urllib.error
import logging
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any

from ciel_geometry.paths import P as _P

from ciel_geometry.phasenav.metatime_contract import INFORMATION_KAPPA
logger = logging.getLogger("auto_verify")

KAPPA = INFORMATION_KAPPA  # ln(2)/(24*pi) — canonical intention/information operator

# Paths: one canonical volume root, never an old home-directory mirror.
VOLUME_ROOT = Path("/media/adrian/New Volume")
CIEL_PROJECT_ROOT = VOLUME_ROOT / "CIEL_PROJECT_CANON"
KNOWN_WORD_DIR = CIEL_PROJECT_ROOT / "NOEMA" / "data" / "unknown_words"
UNKNOWN_WORD_LOG = KNOWN_WORD_DIR / "unknown_words_log.jsonl"
VERIFIED_CARD_DIR = KNOWN_WORD_DIR / "verified_cards"

KNOWN_WORD_DIR.mkdir(parents=True, exist_ok=True)
VERIFIED_CARD_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class AutoVerifyResult:
    """Result of verify_and_learn for a single prompt."""
    prompt_hash: str
    unknown_words_found: list[str]
    verified_new_cards: list[dict[str, Any]]
    stored_card_ids: list[str]
    enrichment: str  # text snippet for CIEL inject

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# Known word cache — built lazily from LNS + meaning-debt + controlled atlas
_WORD_CACHE: set[str] | None = None


def _load_known_words() -> set[str]:
    global _WORD_CACHE
    if _WORD_CACHE is not None:
        return _WORD_CACHE

    words: set[str] = set()
    base = CIEL_PROJECT_ROOT / "CIELINGO_CANON"
    lns = base / "src/ciel_lingophysics_lns_repo_v2_3/data"
    for batch in sorted(lns.glob("concept_cards/batch*/*.json")):
        if batch.name.startswith("batch"):
            continue
        try:
            data = json.loads(batch.read_text(encoding="utf-8"))
            for lang_info in data.get("languages", {}).values():
                lemma = lang_info.get("lemma", "")
                if lemma:
                    words.add(lemma.lower())
                for f in lang_info.get("forms_seed", []):
                    words.add(f.lower())
        except Exception:
            logger.debug("auto_verify.py:76 concept card batch failed to parse: %s", batch, exc_info=True)

    # 2. Operator cards
    for op_path in (lns / "operator_cards").iterdir():
        if not op_path.suffix == ".json":
            continue
        try:
            data = json.loads(op_path.read_text(encoding="utf-8"))
            items = data.get("operator_cards", data.get("cards", []))
            for item in items:
                for surf in item.get("surfaces", {}).values():
                    if isinstance(surf, dict):
                        lemma = surf.get("lemma", "")
                        if lemma:
                            words.add(lemma.lower())
                        for f in surf.get("forms", []):
                            words.add(f.lower())
        except Exception:
            logger.debug("auto_verify.py:94 operator card failed to parse: %s", op_path, exc_info=True)

    # 3. Meaning-debt word cards (PL)
    debt_dir = base / "data/cielingo/debt_word_cards"
    for f in debt_dir.glob("**/*.jsonl"):
        try:
            for line in f.read_text().splitlines():
                if not line.strip():
                    continue
                card = json.loads(line)
                word = card.get("word", card.get("lemma", ""))
                if word:
                    words.add(word.lower())
        except Exception:
            logger.debug("auto_verify.py:108 meaning-debt word card file failed to parse: %s", f, exc_info=True)

    # 4. Controlled atlas (PL/EN/JA)
    for fname in ("controlled_atlas_24.py", "controlled_atlas_48.py"):
        pass  # would need import, skip for now

    # 5. Trilingual slot seed words
    try:
        from cielingo_core.global_layer.trilingual_card_seed import TRILINGUAL_SLOT_SEED
        for slot in TRILINGUAL_SLOT_SEED:
            for entry in slot.get("entries", {}).values():
                lemma = entry.get("lemma", "")
                if lemma:
                    words.add(lemma.lower())
                for f in entry.get("forms", []):
                    words.add(f.lower())
    except Exception:
        logger.debug("auto_verify.py:125 trilingual slot seed import/parse failed", exc_info=True)

    _WORD_CACHE = words
    return words


# Polish stopwords — never worth looking up
POLISH_STOPWORDS = {
    "i", "w", "na", "z", "do", "się", "nie", "to", "że", "a",
    "o", "ma", "jak", "po", "co", "za", "tak", "ale", "u", "czy",
    "od", "oraz", "przez", "dla", "bez", "nad", "pod", "przed",
    "między", "albo", "lub", "ani", "gdy", "jeżeli", "więc",
    "zatem", "bo", "ponieważ", "też", "no", "tylko", "już",
    "nawet", "właśnie", "być", "był", "była", "będzie", "jest",
    "są", "ma", "mają", "może", "mogą", "trzeba", "należy",
    "można", "bardzo", "bardziej", "coraz", "tu", "tam", "tutaj",
}
ENGLISH_STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
    "for", "of", "with", "by", "from", "is", "are", "was", "were",
    "be", "been", "being", "have", "has", "had", "do", "does", "did",
    "will", "would", "could", "should", "may", "might", "can", "shall",
    "it", "its", "this", "that", "these", "those", "i", "you", "he",
    "she", "we", "they", "me", "him", "her", "us", "them", "my",
    "your", "his", "its", "our", "their", "not", "no", "nor", "so",
    "if", "then", "than", "too", "very", "just", "about", "also",
    "up", "down", "out", "off", "over", "under", "again", "further",
    "once", "here", "there", "all", "each", "every", "both", "few",
    "more", "most", "other", "some", "such", "only", "own", "same",
    "into", "upon", "after", "before", "between", "through", "during",
}
STOPWORDS = POLISH_STOPWORDS | ENGLISH_STOPWORDS

WORD_PATTERN = re.compile(r"[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+(?:[-'][A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+)*")


def extract_unknown_words(text: str) -> list[str]:
    """Return unique, non-stopword, unknown words found in text."""
    known = _load_known_words()
    tokens = WORD_PATTERN.findall(text.lower())
    unique = sorted(set(tokens))
    unknown = []
    for w in unique:
        w2 = w.strip("-\"'")
        if not w2 or len(w2) <= 1:
            continue
        if w2 in STOPWORDS:
            continue
        if w2 in known:
            continue
        unknown.append(w2)
    return unknown


# Known card cache: word -> card_id
_STORED_CARDS: dict[str, str] | None = None


def _load_stored_cards() -> dict[str, str]:
    global _STORED_CARDS
    if _STORED_CARDS is not None:
        return _STORED_CARDS
    found: dict[str, str] = {}
    for f in VERIFIED_CARD_DIR.glob("*.json"):
        try:
            data = json.loads(f.read_text())
            word = data.get("lemma", "").lower()
            if word:
                found[word] = data.get("card_id", f.stem)
        except Exception:
            logger.debug("auto_verify.py:195 verified card file failed to parse: %s", f, exc_info=True)
    # Also scan unknown word log
    if UNKNOWN_WORD_LOG.exists():
        for line in UNKNOWN_WORD_LOG.read_text().splitlines():
            try:
                entry = json.loads(line)
                w = entry.get("word", "").lower()
                if w:
                    found[w] = entry.get("card_id", f"auto:{w}")
            except Exception:
                logger.debug("auto_verify.py:205 unknown word log line failed to parse", exc_info=True)
    _STORED_CARDS = found
    return found


def _card_id(word: str) -> str:
    h = hashlib.sha256(word.encode()).hexdigest()[:12]
    return f"auto-verify-{word}-{h}"


def _search_word(word: str) -> dict[str, Any] | None:
    """Search word via web dictionary APIs (exempt from CHANGE #5 internet ban).

    Tries multiple sources: Free Dictionary API (EN), Wiktionary (multi-lang),
    Wikipedia API (multi-lang). Returns best result or None.
    """
    lang = _infer_language(word)

    sources = [
        ("dictionaryapi_dev", _try_dictionaryapi_dev),
    ]
    if lang == "pl":
        sources.append(("sjp_pl", _try_sjp_pl))
        sources.append(("wiktionary_pl", _try_wiktionary_lookup))

    sources += [
        ("wiktionary_en", _try_wiktionary_lookup),
        ("wikipedia", _try_wikipedia_lookup),
    ]

    last_error = None
    for name, func in sources:
        try:
            result = func(word, lang)
            if result and result.get("definition"):
                return result
        except Exception as e:
            last_error = e
            logger.debug("search %s failed for '%s': %s", name, word, e)

    # Queue for deferred lookup if everything failed
    try:
        queue_path = KNOWN_WORD_DIR / "websearch_queue.jsonl"
        with open(queue_path, "a") as f:
            f.write(json.dumps({"word": word, "timestamp": time.time(),
                               "language": lang, "error": str(last_error)}) + "\n")
    except Exception as e:
        logger.debug("failed to queue word '%s': %s", word, e)

    return None


def _try_dictionaryapi_dev(word: str, lang: str) -> dict[str, Any] | None:
    """Free Dictionary API (English only)."""
    if lang != "en":
        return None
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{urllib.request.quote(word)}"
    req = urllib.request.Request(url, headers={"User-Agent": "AutoVerify/1.0"})
    with urllib.request.urlopen(req, timeout=8) as resp:
        data = json.loads(resp.read())
    if isinstance(data, list) and len(data) > 0:
        entry = data[0]
        meanings = entry.get("meanings", [])
        parts_of_speech = []
        definitions = []
        for m in meanings[:3]:
            pos = m.get("partOfSpeech", "")
            if pos:
                parts_of_speech.append(pos)
            for d in m.get("definitions", [])[:2]:
                def_text = d.get("definition", "")
                if def_text:
                    definitions.append(def_text)
        return {
            "word": word,
            "definition": "; ".join(definitions[:3])[:500],
            "source": "dictionaryapi.dev",
            "source_url": url,
            "confidence": 0.7,
            "pos_candidate": parts_of_speech[0] if parts_of_speech else "unknown",
        }
    return None


def _try_sjp_pl(word: str, lang: str) -> dict[str, Any] | None:
    """SJP Polish dictionary lookup via simple HTTP."""
    if lang != "pl":
        return None
    url = f"https://sjp.pl/{urllib.request.quote(word)}"
    req = urllib.request.Request(url, headers={"User-Agent": "AutoVerify/1.0"})
    with urllib.request.urlopen(req, timeout=8) as resp:
        html = resp.read().decode("utf-8")
    # SJP returns 200 on any word; presence in page body tells us if it exists
    # Simplified: extract definition from meta description or body
    import re as _re
    m = _re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html)
    if m:
        desc = m.group(1).strip()
        if desc and "nie znaleziono" not in desc.lower():
            return {
                "word": word,
                "definition": desc[:500],
                "source": "sjp.pl",
                "source_url": url,
                "confidence": 0.65,
                "pos_candidate": _pos_suffix_heuristic(word),
            }
    return None


def _try_wiktionary_lookup(word: str, lang: str) -> dict[str, Any] | None:
    """Wiktionary API — works for any language."""
    api_lang = "pl" if lang == "pl" else "en"
    url = (
        f"https://{api_lang}.wiktionary.org/w/api.php"
        f"?action=query&prop=extracts&exintro=1&explaintext=1"
        f"&titles={urllib.request.quote(word)}&format=json"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "AutoVerify/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
    pages = data.get("query", {}).get("pages", {})
    for page_id, page in pages.items():
        if page_id == "-1":
            continue
        extract = page.get("extract", "")
        if extract:
            return {
                "word": word,
                "definition": extract[:500].strip(),
                "source": f"wiktionary.{api_lang}",
                "source_url": f"https://{api_lang}.wiktionary.org/wiki/{urllib.request.quote(word)}",
                "confidence": 0.7,
                "pos_candidate": _pos_suffix_heuristic(word),
            }
    return None


def _try_wikipedia_lookup(word: str, lang: str) -> dict[str, Any] | None:
    """Wikipedia API — tries EN first, falls back to PL."""
    api_lang = lang if lang in ("en", "pl") else "en"
    url = (
        f"https://{api_lang}.wikipedia.org/w/api.php"
        f"?action=query&prop=extracts&exintro=1&explaintext=1"
        f"&titles={urllib.request.quote(word)}&format=json"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "AutoVerify/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
    pages = data.get("query", {}).get("pages", {})
    for page_id, page in pages.items():
        if page_id == "-1":
            continue
        extract = page.get("extract", "")
        if extract:
            return {
                "word": word,
                "definition": extract[:500].strip(),
                "source": f"wikipedia.{api_lang}",
                "source_url": f"https://{api_lang}.wikipedia.org/wiki/{urllib.request.quote(word)}",
                "confidence": 0.6,
                "pos_candidate": _pos_suffix_heuristic(word),
            }
    return None


def _infer_language(word: str) -> str:
    """Heuristic: if contains Polish letters, guess PL else EN."""
    if re.search(r"[ąćęłńóśźż]", word):
        return "pl"
    return "en"


def _pos_suffix_heuristic(word: str) -> str:
    """Rough POS guess based on suffix."""
    w = word.lower()
    if w.endswith(("ować", "ywać", "ać", "eć", "ić", "yć", "nąć", "ąć")):
        return "verb"
    if w.endswith(("ość", "ność", "anie", "enie", "cja", "sja", "izm")):
        return "noun"
    if w.endswith(("owy", "owa", "owe", "ny", "na", "ne", "ski")):
        return "adjective"
    if w.endswith(("o", "e")):
        return "adverb"
    return "unknown"


def generate_card_from_search(word: str,
                               search_result: dict[str, Any] | None) -> dict[str, Any]:
    """Turn a search result into a CIELingo word card."""
    from cielingo_core.global_layer.card_generator import generate_runtime_card
    from cielingo_core.global_layer.card_runtime_schema import CardOntologyClass, CardValidationStatus

    lang = _infer_language(word)
    pos = _pos_suffix_heuristic(word)

    if search_result:
        definition = search_result.get("definition", "")
        source = search_result.get("source", "unknown")
        confidence = min(search_result.get("confidence", 0.3) + 0.1, 0.95)
    else:
        definition = ""
        source = "structural_heuristic_only"
        confidence = 0.15

    cid = _card_id(word)
    card = generate_runtime_card(
        card_id=cid,
        slot_id=hash(word) % 1000,
        language_id=lang,
        lemma=word,
        surface_forms=[word],
        function=f"{pos}:{definition[:200]}" if definition else pos,
        ontology_class=CardOntologyClass.UNRESOLVED,
        validation_status=CardValidationStatus.DRAFT,
    )

    card_dict = {
        "card_id": cid,
        "lemma": word,
        "language": lang,
        "pos": pos,
        "definition": definition[:500],
        "source": source,
        "confidence": confidence,
        "validated": False,
        "timestamp": time.time(),
    }

    # Write to verified cards
    card_path = VERIFIED_CARD_DIR / f"{cid}.json"
    card_path.write_text(json.dumps(card_dict, indent=2))

    # Append runtime card to CIELingo cards JSONL
    try:
        runtime_card_path = Path(_P.DATA_FILES.CIELINGO_CARDS)
        with open(runtime_card_path, "a") as _f:
            _f.write(json.dumps(card.to_dict(), ensure_ascii=False) + "\n")
    except Exception as _e:
        import logging as _log
        _log.getLogger(__name__).debug("CIELingo runtime card JSONL write failed: %s", _e)

    # Append to unknown word log
    log_entry = {
        "timestamp": time.time(),
        "word": word,
        "card_id": cid,
        "language": lang,
        "source": source,
        "confidence": confidence,
        "definition": definition[:200],
    }
    with open(UNKNOWN_WORD_LOG, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    return card_dict


class AutoVerify:
    """Auto-verify unknown words and learn them into CIELingo."""

    def __init__(self):
        self._session_count = 0

    def verify_and_learn(self, text: str) -> AutoVerifyResult:
        """Main pipeline: extract -> search -> generate cards -> return."""
        prompt_hash = hashlib.sha256(text.encode()).hexdigest()[:16]
        unknown = extract_unknown_words(text)

        # Filter already stored
        stored = _load_stored_cards()
        new_words = [w for w in unknown if w not in stored]

        if not new_words:
            return AutoVerifyResult(
                prompt_hash=prompt_hash,
                unknown_words_found=[],
                verified_new_cards=[],
                stored_card_ids=[],
                enrichment="",
            )

        self._session_count += 1
        cards = []
        card_ids = []

        for word in new_words[:10]:  # max 10 per prompt
            result = _search_word(word)
            card = generate_card_from_search(word, result)
            cards.append(card)
            card_ids.append(card["card_id"])

        # Build enrichment text
        if cards:
            enrichment = (
                f"AutoVerify[new={len(cards)}]: "
                + "; ".join(f"{c['lemma']}({c['language']},{c['source']})"
                          for c in cards)
            )
        else:
            enrichment = ""

        # Update cache
        global _STORED_CARDS
        if _STORED_CARDS is not None:
            for c in cards:
                _STORED_CARDS[c["lemma"]] = c["card_id"]

        return AutoVerifyResult(
            prompt_hash=prompt_hash,
            unknown_words_found=new_words,
            verified_new_cards=cards,
            stored_card_ids=card_ids,
            enrichment=enrichment,
        )

    def inventory(self) -> dict[str, Any]:
        """Return inventory of stored verified cards."""
        cards = _load_stored_cards()
        total = len(cards)
        by_lang: dict[str, int] = {}
        for f in VERIFIED_CARD_DIR.glob("*.json"):
            try:
                data = json.loads(f.read_text())
                lang = data.get("language", "unknown")
                by_lang[lang] = by_lang.get(lang, 0) + 1
            except Exception:
                logger.debug("auto_verify.py:523 verified card file failed to parse during inventory: %s", f, exc_info=True)
        return {
            "total_cards": total,
            "by_language": by_lang,
            "session_count": self._session_count,
            "verified_cards_dir": str(VERIFIED_CARD_DIR),
            "unknown_word_log": str(UNKNOWN_WORD_LOG),
        }
