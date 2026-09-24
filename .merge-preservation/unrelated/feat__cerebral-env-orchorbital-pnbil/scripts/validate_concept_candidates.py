#!/usr/bin/env python3
"""Autonomous concept research over a fixed, no-auth, no-CAPTCHA source whitelist.

Design contract (do not weaken without updating the ethics/provenance policy):
  - Reads pending entries from concepts/registry.jsonl (written by
    autonomous_response.py when a prompt falls outside the verified knowledge
    pack).
  - Queries only sources listed in config/concept_validation_whitelist.json.
  - Writes a *draft* knowledge card per concept to concepts/pending_review/.
  - Never writes to data/cielingo/verified_knowledge/ directly. Promotion to
    canon is a separate, explicit, human-run step (see promote_concept.py).
    This keeps the whole pipeline's fail-closed/no-fallback guarantee intact:
    CIEL may research on its own, but "verified" still means human-reviewed.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

# Kept in sync with cielingo_core.autonomous_response._QUESTION_STEMS — this
# script runs standalone (outside the package) so it can't import that
# module directly. If one changes, update the other.
_QUESTION_STEMS = [
    r"^wyja[sś]nij\s+", r"^wyt[lł]umacz\s+", r"^co to jest\s+", r"^czym jest\s+",
    r"^czym s[aą]\s+", r"^co oznacza\s+", r"^zdefiniuj\s+", r"^opowiedz o\s+",
    r"^opowiedz mi o\s+", r"^powiedz mi o\s+", r"^explain\s+", r"^what is\s+",
    r"^what are\s+", r"^define\s+", r"^tell me about\s+",
]


def _extract_key_term(text: str) -> str:
    for pattern in _QUESTION_STEMS:
        stripped = re.sub(pattern, "", text)
        if stripped != text:
            return stripped.strip() or text
    return text.strip()

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = Path("/media/adrian/NOEMA_SANDBOX/concepts/registry.jsonl")
PENDING_DIR = Path("/media/adrian/NOEMA_SANDBOX/concepts/pending_review")
HOLONOMY_CANDIDATES_PATH = Path("/media/adrian/NOEMA_SANDBOX/concepts/holonomy_candidates.jsonl")
WHITELIST_PATH = ROOT / "config" / "concept_validation_whitelist.json"
USER_AGENT = "NOEMA-CIEL-concept-research/0.1 (local research assistant; no-auth sources only)"
TIMEOUT = 10

# Same relation vocabulary as cielingo/lexical_holonomy.py's RELATION_WEIGHTS
# table. A cross-source research hit with no reviewed lexical evidence yet
# is the weakest, most provisional relation in that table — "unknown_relation"
# — not a synonym/antonym/etc. claim we haven't earned.
_HOLONOMY_RELATION_TYPE = "unknown_relation"
_HOLONOMY_RELATION_WEIGHT = 0.12
_HOLONOMY_FREQUENCY_THRESHOLD = 2

# Kept in sync with cielingo_core.autonomous_response.CROSS_SOURCE_AGREEMENT_THRESHOLD.
CROSS_SOURCE_AGREEMENT_THRESHOLD = 2

# Which whitelist source ids answer in which language — lets a concept's
# research be checked for real PL *and* EN coverage instead of "some source
# answered, who knows which language".
_SOURCE_LANGUAGE = {
    "wikipedia_pl": "pl",
    "wikipedia_en": "en",
    "wiktionary": "en",
    "wikidata": "pl+en",  # server localises label/description per request language param
    "arxiv": "en",
    "dbpedia": "en",
    "crossref": "en",
    "openlibrary": "en",
}


def load_whitelist() -> list[dict]:
    payload = json.loads(WHITELIST_PATH.read_text(encoding="utf-8"))
    return payload["sources"]


def pending_terms() -> list[str]:
    """Concept keys still awaiting research — de-duplicated, term extracted."""
    if not REGISTRY.exists():
        return []
    seen: dict[str, str] = {}
    for line in REGISTRY.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        entry = json.loads(line)
        if entry.get("review_status") == "pending":
            concept = entry.get("concept") or _extract_key_term(entry["text"])
            seen[concept] = concept
    return list(seen.keys())


def concept_frequencies() -> dict[str, int]:
    """How many times each concept key has been observed across the whole
    registry (pending + researched) — 'najczęściej występujące frazy'.
    A one-off question is noise; a phrase seen repeatedly is a candidate the
    holonomy graph should actually know about."""
    counts: dict[str, int] = {}
    if not REGISTRY.exists():
        return counts
    for line in REGISTRY.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        entry = json.loads(line)
        concept = entry.get("concept") or _extract_key_term(entry["text"])
        counts[concept] = counts.get(concept, 0) + 1
    return counts


def mark_researched(concept_terms: set[str], agreement_by_concept: dict[str, int]) -> None:
    """Rewrite registry lines for researched concepts so the loop closes —
    otherwise every run re-researches the same pending backlog forever and
    there is no way to see, from the registry alone, whether learning
    actually happened."""
    if not REGISTRY.exists():
        return
    lines = REGISTRY.read_text(encoding="utf-8").splitlines()
    out_lines = []
    for line in lines:
        if not line.strip():
            continue
        entry = json.loads(line)
        concept = entry.get("concept") or _extract_key_term(entry["text"])
        if entry.get("review_status") == "pending" and concept in concept_terms:
            entry["review_status"] = "researched"
            entry["researched_at"] = datetime.now(timezone.utc).isoformat()
            entry["agreeing_sources"] = agreement_by_concept.get(concept, 0)
        out_lines.append(json.dumps(entry, ensure_ascii=False))
    REGISTRY.write_text("\n".join(out_lines) + "\n", encoding="utf-8")


def fetch(url: str) -> tuple[int, str | None]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status, resp.read(4096).decode("utf-8", errors="replace")
    except Exception as exc:
        return 0, f"__error__:{type(exc).__name__}:{exc}"


# 200-with-empty-results is not a hit. Every source in the whitelist has a
# distinct "found nothing" shape; without checking it, an HTTP 200 on zero
# matches gets counted as agreement, which is worse than no result at all.
_EMPTY_RESULT_MARKERS = (
    '"search":[]',           # wikidata wbsearchentities
    '"numFound":0',          # openlibrary
    '"totalResults">0',      # dbpedia XML totalResults="0"
    '<ArrayOfResults></ArrayOfResults>',  # dbpedia empty XML body
    '"total-results":0',     # crossref
    "<opensearch:totalResults>0<",  # arxiv atom feed
)


def _has_real_content(body: str) -> bool:
    if not body:
        return False
    return not any(marker in body for marker in _EMPTY_RESULT_MARKERS)


_HTML_TAG = re.compile(r"<[^>]+>")


def _strip_html(text: str) -> str:
    """Sources like Wiktionary/DBpedia embed raw HTML in text fields
    (highlighting spans, wikilinks). This is JSON/XML API output, not a
    rendered page, so a regex strip is sufficient — no script execution
    surface, just marker removal for a clean quote."""
    return re.sub(r"\s+", " ", _HTML_TAG.sub(" ", text)).strip()


def _extract_wikipedia(body: str) -> str | None:
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return None
    extract = data.get("extract")
    return _strip_html(extract) if extract else None


def _extract_wiktionary(body: str) -> str | None:
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return None
    for entries in data.values():
        for entry in entries:
            for definition in entry.get("definitions", []):
                text = _strip_html(definition.get("definition", ""))
                if text:
                    return text
    return None


def _extract_wikidata(body: str) -> str | None:
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return None
    hits = data.get("search") or []
    if not hits:
        return None
    top = hits[0]
    label = top.get("label", "")
    description = top.get("description", "")
    return _strip_html(f"{label}: {description}".strip(": "))


def _extract_arxiv(body: str) -> str | None:
    try:
        root = ET.fromstring(body)
    except ET.ParseError:
        return None
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    entry = root.find("atom:entry", ns)
    if entry is None:
        return None
    title = entry.findtext("atom:title", default="", namespaces=ns)
    summary = entry.findtext("atom:summary", default="", namespaces=ns)
    return _strip_html(f"{title.strip()}: {summary.strip()[:400]}")


def _extract_dbpedia(body: str) -> str | None:
    try:
        root = ET.fromstring(body)
    except ET.ParseError:
        return None
    result = root.find("Result")
    if result is None:
        return None
    label = (result.findtext("Label") or "").strip()
    description = (result.findtext("Description") or "").strip()
    return _strip_html(f"{label}: {description}")


def _extract_crossref(body: str) -> str | None:
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return None
    items = data.get("message", {}).get("items") or []
    if not items:
        return None
    titles = items[0].get("title") or []
    return _strip_html(titles[0]) if titles else None


def _extract_openlibrary(body: str) -> str | None:
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return None
    docs = data.get("docs") or []
    if not docs:
        return None
    top = docs[0]
    title = top.get("title", "")
    authors = ", ".join(top.get("author_name", []) or [])
    return _strip_html(f"{title} — {authors}" if authors else title)


# Sources where "returned a result" already means server-side relevance
# matching (entity/lookup search) don't need a client-side recheck — and
# recheck actively hurts them when the result is legitimately translated
# (e.g. Wikidata returning an English label/description for a Polish query).
# arXiv's `all:` query is different: it's a loose boolean/OR match over
# abstract+title+authors and will hand back its "closest" paper even with
# zero real topical overlap, so it needs an explicit relevance guard.
_RELEVANCE_CHECKED_SOURCES = {"arxiv"}


def _is_relevant(term: str, extract: str) -> bool:
    term_tokens = [t for t in re.findall(r"\w+", term.casefold(), flags=re.UNICODE) if len(t) >= 4]
    if not term_tokens:
        return True
    extract_cf = extract.casefold()
    return any(token in extract_cf for token in term_tokens)


_EXTRACTORS = {
    "wikipedia_pl": _extract_wikipedia,
    "wikipedia_en": _extract_wikipedia,
    "wiktionary": _extract_wiktionary,
    "wikidata": _extract_wikidata,
    "arxiv": _extract_arxiv,
    "dbpedia": _extract_dbpedia,
    "crossref": _extract_crossref,
    "openlibrary": _extract_openlibrary,
}


def research_term(term: str, sources: list[dict]) -> dict:
    findings = []
    for source in sources:
        url = source["base_url"].replace("{term}", urllib.parse.quote(term))
        status, body = fetch(url)
        body = body or ""
        raw_ok = status == 200 and _has_real_content(body)
        extract = None
        if raw_ok:
            extractor = _EXTRACTORS.get(source["id"])
            candidate = extractor(body) if extractor else None
            if candidate and (
                source["id"] not in _RELEVANCE_CHECKED_SOURCES or _is_relevant(term, candidate)
            ):
                extract = candidate
        findings.append({
            "source_id": source["id"],
            "source_name": source["name"],
            "license": source["license"],
            "language": _SOURCE_LANGUAGE.get(source["id"], "unknown"),
            "url": url,
            "http_status": status,
            "has_content": bool(extract),
            "extract": extract,
            "snippet": body[:2000],
        })
    languages_covered = sorted({
        lang
        for f in findings
        if f["has_content"]
        for lang in f["language"].split("+")
    })
    return {
        "concept": term,
        "researched_at": datetime.now(timezone.utc).isoformat(),
        "findings": findings,
        "languages_covered": languages_covered,
        "bilingual_pl_en": {"pl", "en"} <= set(languages_covered),
        "canon_status": "draft_pending_human_review",
        "promotion_policy": "requires explicit review — see scripts/promote_concept.py",
    }


def emit_holonomy_candidate(term: str, draft: dict, frequency: int) -> None:
    """Schema-compatible with cielingo.lexical_holonomy.LexicalHolonomyEdge,
    minus the fields only the real formal engine can compute honestly
    (phase_rad/holonomy_phase_delta need an actual language-card lexical
    unit; vector_distance needs the real semantic-axis vectors). Those are
    left null/None — a human or the formal pipeline fills them in when this
    candidate is actually promoted into a card. This file is additive-only:
    it never rewrites the live lexical holonomy edge store."""
    edge = {
        "schema": "noema.holonomy_candidate_edge/v1",
        "source_lexical_id": f"candidate:{term}",
        "target_lexical_id": None,
        "source_surface": term,
        "target_surface": None,
        "languages_covered": draft["languages_covered"],
        "bilingual_pl_en": draft["bilingual_pl_en"],
        "relation_type": _HOLONOMY_RELATION_TYPE,
        "relation_family": "unclassified",
        "weight": _HOLONOMY_RELATION_WEIGHT,
        "holonomy_phase_delta": None,
        "vector_distance": None,
        "evidence_kind": "cross_source_open_api",
        "evidence_paths": [f["url"] for f in draft["findings"] if f["has_content"]],
        "evidence_status": "draft_pending_review",
        "supervision_required": True,
        "observed_frequency": frequency,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    HOLONOMY_CANDIDATES_PATH.parent.mkdir(parents=True, exist_ok=True)
    with HOLONOMY_CANDIDATES_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(edge, ensure_ascii=False) + "\n")


def main() -> int:
    terms = pending_terms()
    if not terms:
        print("no pending concepts to research")
        return 0
    sources = load_whitelist()
    PENDING_DIR.mkdir(parents=True, exist_ok=True)
    frequencies = concept_frequencies()
    agreement_by_concept: dict[str, int] = {}
    for term in terms:
        draft = research_term(term, sources)
        agreement = sum(1 for f in draft["findings"] if f["has_content"])
        agreement_by_concept[term] = agreement
        digest = hashlib.sha256(term.encode("utf-8")).hexdigest()[:16]
        out_path = PENDING_DIR / f"{digest}.json"
        out_path.write_text(json.dumps(draft, ensure_ascii=False, indent=2), encoding="utf-8")
        frequency = frequencies.get(term, 1)
        bilingual = draft["bilingual_pl_en"]
        print(
            f"researched: {term!r} -> agreement={agreement} bilingual_pl_en={bilingual} "
            f"frequency={frequency} -> {out_path}"
        )
        if agreement >= CROSS_SOURCE_AGREEMENT_THRESHOLD and frequency >= _HOLONOMY_FREQUENCY_THRESHOLD:
            emit_holonomy_candidate(term, draft, frequency)
            print(f"  -> holonomy candidate edge emitted (frequency={frequency})")
    mark_researched(set(terms), agreement_by_concept)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
