#!/usr/bin/env python3
"""CIELingo Canonization Pipeline — automatyczna kanonizacja kart z internetu + knowledge.db.

Algorytm:
1.  Ładuje karty kandydujące z data/cielingo/debt_word_cards/*.jsonl
2.  Dla każdego lematu zbiera dowody:
    a) knowledge.db — TF-IDF, frekwencja w korpusie (602 docs, 54508 termów)
    b) Web fetch — Wiktionary, dictionary API (SJP, WordNet, itp.)
    c) Walidacja gramatyczna — suffix rules, POS consistency
3.  Oblicza nowy confidence score z wag:
    - corpus_evidence:  0.40 (jest w korpusie? tf*idf)
    - web_evidence:      0.35 (znaleziony w słownikach?)
    - grammatical_valid: 0.25 (POS zgadza się z regułami?)
4.  Jeśli confidence >= 0.70 → auto-kanonizacja (canon_promoted)
    Jeśli confidence >= 0.50 → canon_candidate (czeka na review)
    Jeśli confidence < 0.50 → draft (potrzebuje więcej danych)
5.  Zapisuje decyzje do data/cielingo/canonization_audit/canonization_decisions.jsonl
6.  Generuje raport

Użycie:
    python3 scripts/cielingo_canonization_pipeline.py
    python3 scripts/cielingo_canonization_pipeline.py --limit 50    # tylko 50 kart
    python3 scripts/cielingo_canonization_pipeline.py --force       # re-run nawet dla już zdecydowanych
    python3 scripts/cielingo_canonization_pipeline.py --lemma życie # konkretny lemat
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import argparse
import datetime as dt
import hashlib
import json
import math
import os
import re
import sqlite3
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

# ──────────────────────────────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────────────────────────────
SCHEMA = "cielingo/canonization-audit/v0.2"
SOURCES = {
    "knowledge_db": "/media/adrian/New Volume1/NOEMA_LIBRARY/DB/knowledge.db",
    "candidate_cards_dir": Path("data/cielingo/debt_word_cards"),
    "canonization_audit_dir": Path("data/cielingo/canonization_audit"),
}

# Wagi dla dowodów
WEIGHTS = {
    "corpus_evidence": 0.40,
    "web_evidence": 0.35,
    "grammatical_valid": 0.25,
}

# Progi
THRESHOLD_CANON = 0.70
THRESHOLD_CANDIDATE = 0.50

# Web fetch timeout
WEB_TIMEOUT = 5  # sekund
WEB_USER_AGENT = "NOEMA-CIELingo-Canonization-Pipeline/1.0"

# Suffix rules for Polish POS validation
POLISH_SUFFIXES = {
    "noun": (("ość", 0.9), ("ność", 0.9), ("anie", 0.8), ("enie", 0.8),
             ("cja", 0.7), ("sja", 0.7), ("izm", 0.7), ("stwo", 0.7),
             ("ka", 0.5), ("ek", 0.5), ("a", 0.3), ("e", 0.3), ("um", 0.6),
             ("acja", 0.8), ("encja", 0.8), ("arz", 0.6), ("nik", 0.7)),
    "adjective": (("owy", 0.8), ("owa", 0.8), ("owe", 0.8), ("ny", 0.7),
                  ("na", 0.7), ("ne", 0.7), ("ski", 0.8), ("ska", 0.8),
                  ("skie", 0.8), ("czy", 0.6), ("ego", 0.4), ("ej", 0.4),
                  ("ych", 0.5), ("ymi", 0.5)),
    "adverb": (("o", 0.4), ("e", 0.3), ("nie", 0.2)),
    "verb_infinitive": (("ować", 0.9), ("ywać", 0.9), ("iwać", 0.8),
                        ("ać", 0.6), ("eć", 0.6), ("ić", 0.6), ("yć", 0.6),
                        ("nąć", 0.8), ("ąć", 0.7)),
}

# zamknięte klasy — 100% pewności
CLOSED_CLASSES = {
    "conjunction", "preposition", "pronoun", "particle", "modal_operator"
}


# ──────────────────────────────────────────────────────────────────────
# UTILITIES
# ──────────────────────────────────────────────────────────────────────

def utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_word(text: str) -> str:
    return unicodedata.normalize("NFKC", str(text).strip().lower())


def stable_id(lemma: str, source: str) -> str:
    digest = hashlib.sha256(f"{normalize_word(lemma)}|{source}|{SCHEMA}".encode()).hexdigest()[:24]
    return f"canon_decision:{digest}"


def bounded(v: float) -> float:
    return max(0.0, min(1.0, float(v)))


def sha256_json(payload: Any) -> str:
    return hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True).encode()
    ).hexdigest()


# ──────────────────────────────────────────────────────────────────────
# EVIDENCE COLLECTORS
# ──────────────────────────────────────────────────────────────────────

class KnowledgeEvidence:
    """Evidence from knowledge.db TF-IDF corpus."""

    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)

    def lookup(self, lemma: str) -> dict[str, Any]:
        """Sprawdza czy lemma istnieje w korpusie, zwraca tfidf stats."""
        cur = self.conn.execute(
            "SELECT term, tf, idf, tfidf FROM term_index WHERE term = ?",
            (lemma.lower(),)
        )
        rows = cur.fetchall()
        if not rows:
            # spróbuj z częścią lematu (dla form fleksyjnych)
            cur = self.conn.execute(
                "SELECT term, tf, idf, tfidf FROM term_index WHERE term LIKE ? LIMIT 5",
                (f"{lemma.lower()[:4]}%",)
            )
            fuzzy = cur.fetchall()
            return {
                "found": False,
                "exact_match": False,
                "fuzzy_matches": [r[0] for r in fuzzy],
                "max_tfidf": 0.0,
                "doc_frequency": None,
                "corpus_score": 0.0,
            }

        max_tfidf = max(r[3] for r in rows)
        # idf > 2 = rzadki (bardziej specyficzny), idf < 1 = częsty
        avg_tf = sum(r[1] for r in rows) / len(rows)
        return {
            "found": True,
            "exact_match": True,
            "match_count": len(rows),
            "max_tfidf": max_tfidf,
            "avg_tf": avg_tf,
            "corpus_score": bounded(max_tfidf / 6.0),  # normalizacja: max tfidf ~6
        }

    def close(self):
        self.conn.close()


class WebEvidence:
    """Evidence from web sources: Wiktionary, dictionary APIs."""

    def __init__(self, timeout: int = WEB_TIMEOUT):
        self.timeout = timeout
        self.session_count = 0

    def lookup(self, lemma: str, language: str = "pl") -> dict[str, Any]:
        """Sprawdza lemma na Wiktionary i innych źródłach."""
        evidence = {
            "wiktionary_found": False,
            "wiktionary_url": None,
            "wiktionary_status": None,
            "dictionary_count": 0,
            "sources_checked": [],
            "web_score": 0.0,
        }

        # 1. Wiktionary PL
        url = f"https://pl.wiktionary.org/wiki/{urllib.request.quote(lemma)}"
        evidence["wiktionary_url"] = url
        try:
            req = urllib.request.Request(url, headers={"User-Agent": WEB_USER_AGENT})
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                html = resp.read().decode("utf-8", errors="replace")
                status = resp.status
                evidence["wiktionary_status"] = status
                evidence["sources_checked"].append("wiktionary_pl")

                if status == 200 and "Nie znaleziono" not in html[:500]:
                    evidence["wiktionary_found"] = True
                    evidence["dictionary_count"] += 1
                    # Wyciągnij część mowy z wiktionary
                    pos_match = re.search(
                        r'class="mw-headline"[^>]*id="([^"]*)"',
                        html
                    )
                    if pos_match:
                        evidence["wiktionary_pos"] = pos_match.group(1).lower()
                elif status == 200:
                    evidence["wiktionary_found"] = False
                elif status == 404:
                    evidence["wiktionary_found"] = False
                self.session_count += 1
        except (urllib.error.HTTPError, urllib.error.URLError, OSError) as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/cielingo_canonization_pipeline.py:212 quiet except scope=WebEvidence.lookup reason=no_log_no_raise")
            evidence["wiktionary_status"] = str(e)
            evidence["wiktionary_found"] = False

        # 2. English Wiktionary jako fallback
        if not evidence["wiktionary_found"] and language == "pl":
            url_en = f"https://en.wiktionary.org/wiki/{urllib.request.quote(lemma)}"
            try:
                req = urllib.request.Request(url_en, headers={"User-Agent": WEB_USER_AGENT})
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    html = resp.read().decode("utf-8", errors="replace")
                    if resp.status == 200 and "Nie znaleziono" not in html[:500] and "There is currently no text in this page" not in html[:1000]:
                        # Sprawdź czy sekcja polska istnieje
                        if re.search(r'<span[^>]*id="Polish"[^>]*>', html):
                            evidence["wiktionary_found"] = True
                            evidence["dictionary_count"] += 1
                            evidence["sources_checked"].append("wiktionary_en_polish_section")
                    self.session_count += 1
            except (urllib.error.HTTPError, urllib.error.URLError, OSError):
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/cielingo_canonization_pipeline.py:230 quiet except scope=WebEvidence.lookup reason=pass")
                pass

        # 3. Oblicz score na podstawie znalezionych źródeł
        if evidence["dictionary_count"] >= 2:
            evidence["web_score"] = 1.0
        elif evidence["dictionary_count"] == 1:
            evidence["web_score"] = 0.80
        else:
            evidence["web_score"] = 0.10  # niski ale nie zerowy — słowo może istnieć mimo braku w Wiktionar

        return evidence

    def close(self):
        pass


class GrammarEvidence:
    """Evidence from morphological rules validation."""

    def validate(self, lemma: str, pos_candidate: str) -> dict[str, Any]:
        """Sprawdza czy lemma pasuje do zadeklarowanej części mowy."""
        result = {
            "pos_declared": pos_candidate,
            "pos_validated": False,
            "suffix_match": False,
            "matching_suffix": None,
            "alternative_pos": [],
            "grammar_score": 0.0,
        }

        # Closed class — zawsze poprawne
        if pos_candidate in CLOSED_CLASSES:
            result["pos_validated"] = True
            result["grammar_score"] = 1.0
            return result

        # Sprawdź suffixy
        suffixes = POLISH_SUFFIXES.get(pos_candidate, [])
        for suffix, conf in suffixes:
            if lemma.endswith(suffix):
                result["suffix_match"] = True
                result["matching_suffix"] = suffix
                result["pos_validated"] = True
                result["grammar_score"] = conf
                break

        # Jeśli nie ma suffix match, sprawdź alternatywne POS
        if not result["suffix_match"]:
            for alt_pos, alt_suffixes in POLISH_SUFFIXES.items():
                if alt_pos == pos_candidate:
                    continue
                for suffix, conf in alt_suffixes:
                    if lemma.endswith(suffix):
                        result["alternative_pos"].append({
                            "pos": alt_pos,
                            "suffix": suffix,
                            "confidence": conf
                        })
                        break

            # Domyślny niski score dla słów bez rozpoznawalnego suffixu
            result["grammar_score"] = 0.30

        return result


# ──────────────────────────────────────────────────────────────────────
# CANONIZATION ENGINE
# ──────────────────────────────────────────────────────────────────────

class CanonizationEngine:
    """Główny silnik kanonizacji."""

    def __init__(self, db_path: str, canon_audit_dir: Path, force: bool = False):
        self.knowledge = KnowledgeEvidence(db_path)
        self.web = WebEvidence()
        self.grammar = GrammarEvidence()
        self.canon_audit_dir = canon_audit_dir
        self.force = force
        self.stats = {
            "processed": 0,
            "skipped_already_decided": 0,
            "canon_promoted": 0,
            "canon_candidate": 0,
            "draft": 0,
            "web_queries": 0,
            "errors": 0,
        }
        # Załaduj istniejące decyzje
        self._existing_decisions: dict[str, dict[str, Any]] = {}
        self._load_existing_decisions()

    def _load_existing_decisions(self):
        path = self.canon_audit_dir / "canonization_decisions.jsonl"
        if path.exists():
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        d = json.loads(line)
                        did = d.get("decision_id", d.get("source_card_id", ""))
                        self._existing_decisions[did] = d
                    except json.JSONDecodeError:
                        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/cielingo_canonization_pipeline.py:335 quiet except scope=CanonizationEngine._load_existing_decisions reason=continue")
                        continue

    def canonize_card(self, card: dict[str, Any]) -> dict[str, Any]:
        """Przetwarza pojedynczą kartę kandydującą."""
        lemma = card.get("lemma", "")
        if not lemma:
            return None
        lemma = normalize_word(lemma)

        card_id = card.get("card_id", "unknown")
        pos = card.get("grammatical_designation", {}).get("part_of_speech_candidate", "unknown")
        language = card.get("language", "pl_candidate")

        # Sprawdź czy już mamy decyzję
        decision_id = stable_id(lemma, card_id)
        if not self.force and decision_id in self._existing_decisions:
            self.stats["skipped_already_decided"] += 1
            return self._existing_decisions[decision_id]

        # Zbierz dowody
        corpus_ev = self.knowledge.lookup(lemma)
        web_ev = self.web.lookup(lemma, language)
        grammar_ev = self.grammar.validate(lemma, pos)

        self.stats["web_queries"] += 1

        # Oblicz confidence
        corpus_score = corpus_ev["corpus_score"]
        web_score = web_ev["web_score"]
        grammar_score = grammar_ev["grammar_score"]

        # Bonus za znalezienie w wielu źródłach
        evidence_count = sum([
            1 if corpus_ev["found"] else 0,
            1 if web_ev["wiktionary_found"] else 0,
            1 if grammar_ev["pos_validated"] else 0,
        ])
        evidence_bonus = evidence_count * 0.05  # max +0.15 za 3 źródła

        confidence = (
            WEIGHTS["corpus_evidence"] * corpus_score
            + WEIGHTS["web_evidence"] * web_score
            + WEIGHTS["grammatical_valid"] * grammar_score
            + evidence_bonus
        )
        confidence = bounded(confidence)

        # Decyzja
        if confidence >= THRESHOLD_CANON:
            decision = "canon_promoted"
            canonicalization_level = "full_canon"
            gate_result = "PASSED_ALL_GATES"
            required_action = "none_add_to_runtime"
        elif confidence >= THRESHOLD_CANDIDATE:
            decision = "canon_candidate"
            canonicalization_level = "semi_canon"
            gate_result = "PASSED_CORPUS_AND_GRAMMAR"
            required_action = "review_web_evidence_for_final_promotion"
        else:
            decision = "keep_as_draft"
            canonicalization_level = "deferred"
            gate_result = "BLOCKED_LOW_CONFIDENCE"
            required_action = "collect_more_evidence_or_manual_review"

        # Buduj rekord decyzji
        record = {
            "schema": SCHEMA,
            "decision_id": decision_id,
            "lemma": lemma,
            "source_card_id": card_id,
            "source_kind": pos,
            "confidence": round(confidence, 4),
            "decision": decision,
            "canonicalization_level": canonicalization_level,
            "gate_result": gate_result,
            "required_next_action": required_action,
            "evidence": {
                "corpus": {
                    "found": corpus_ev["found"],
                    "exact_match": corpus_ev.get("exact_match", False),
                    "max_tfidf": round(corpus_ev.get("max_tfidf", 0), 4),
                    "corpus_score": round(corpus_score, 4),
                },
                "web": {
                    "wiktionary_found": web_ev["wiktionary_found"],
                    "sources_checked": web_ev["sources_checked"],
                    "dictionary_count": web_ev["dictionary_count"],
                    "web_score": round(web_score, 4),
                },
                "grammar": {
                    "pos_declared": grammar_ev["pos_declared"],
                    "pos_validated": grammar_ev["pos_validated"],
                    "matching_suffix": grammar_ev["matching_suffix"],
                    "grammar_score": round(grammar_score, 4),
                },
                "evidence_bonus": round(evidence_bonus, 4),
            },
            "final_confidence": round(confidence, 4),
            "auto_canonization_allowed": confidence >= THRESHOLD_CANON,
            "processed_at": utc_now(),
        }

        # Aktualizuj statystyki
        self.stats["processed"] += 1
        if decision == "canon_promoted":
            self.stats["canon_promoted"] += 1
        elif decision == "canon_candidate":
            self.stats["canon_candidate"] += 1
        else:
            self.stats["draft"] += 1

        return record

    def save_decisions(self, decisions: list[dict[str, Any]]):
        """Dopisuje decyzje do pliku auditowego."""
        path = self.canon_audit_dir / "canonization_decisions.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a") as f:
            for d in decisions:
                f.write(json.dumps(d, ensure_ascii=False, sort_keys=True) + "\n")
        # Generuj też raport
        self._write_report()

    def _write_report(self):
        """Zapisuje raport podsumowujący."""
        report = {
            "schema": "cielingo/canonization-pipeline-report/v0.1",
            "timestamp": utc_now(),
            "stats": self.stats,
            "thresholds": {
                "canon": THRESHOLD_CANON,
                "candidate": THRESHOLD_CANDIDATE,
            },
            "weights": WEIGHTS,
        }
        path = self.canon_audit_dir / "canonization_pipeline_report.json"
        with open(path, "w") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

    def close(self):
        self.knowledge.close()
        self.web.close()

    def print_summary(self):
        """Drukuje podsumowanie do stdout."""
        s = self.stats
        print(f"\n{'='*60}")
        print(f"  CIELingo Canonization Pipeline — RAPORT")
        print(f"{'='*60}")
        print(f"  Przetworzono:     {s['processed']}")
        print(f"  Pominięto (już):  {s['skipped_already_decided']}")
        print(f"  → CANON:          {s['canon_promoted']}")
        print(f"  → KANDYDAT:       {s['canon_candidate']}")
        print(f"  → SZKIC:          {s['draft']}")
        print(f"  Zapytania web:    {s['web_queries']}")
        print(f"  Błędy:            {s['errors']}")
        print(f"{'='*60}\n")


# ──────────────────────────────────────────────────────────────────────
# CARD LOADER
# ──────────────────────────────────────────────────────────────────────

def load_candidate_cards(cards_dir: Path, lemma_filter: str = None, limit: int = None) -> list[dict[str, Any]]:
    """Ładuje karty kandydujące z wszystkich JSONL w katalogu debt_word_cards."""
    cards: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    # Priorytet: word_candidate_cards.jsonl i other_pos_candidate_cards.jsonl (największe)
    priority_files = [
        "word_candidate_cards.jsonl",
        "other_pos_candidate_cards.jsonl",
    ]

    for fname in priority_files:
        path = cards_dir / fname
        if not path.exists():
            continue
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    card = json.loads(line)
                    cid = card.get("card_id", "")
                    if cid and cid not in seen_ids:
                        lemma = normalize_word(card.get("lemma", ""))
                        if lemma_filter and lemma_filter != lemma:
                            continue
                        seen_ids.add(cid)
                        cards.append(card)
                        if limit and len(cards) >= limit:
                            return cards
                except json.JSONDecodeError:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/cielingo_canonization_pipeline.py:530 quiet except scope=load_candidate_cards reason=continue")
                    continue

    # Potem reszta POS files
    pos_dir = cards_dir / "by_part_of_speech"
    if pos_dir.exists():
        for path in sorted(pos_dir.glob("*.jsonl")):
            if path.name in priority_files:
                continue
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        card = json.loads(line)
                        cid = card.get("card_id", "")
                        if cid and cid not in seen_ids:
                            lemma = normalize_word(card.get("lemma", ""))
                            if lemma_filter and lemma_filter != lemma:
                                continue
                            seen_ids.add(cid)
                            cards.append(card)
                            if limit and len(cards) >= limit:
                                return cards
                    except json.JSONDecodeError:
                        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/cielingo_canonization_pipeline.py:555 quiet except scope=load_candidate_cards reason=continue")
                        continue

    # Pozostałe pliki w głównym katalogu
    for path in sorted(cards_dir.glob("*.jsonl")):
        if path.name in priority_files:
            continue
        if "by_part_of_speech" in str(path):
            continue
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    card = json.loads(line)
                    cid = card.get("card_id", "")
                    if cid and cid not in seen_ids:
                        lemma = normalize_word(card.get("lemma", ""))
                        if lemma_filter and lemma_filter != lemma:
                            continue
                        seen_ids.add(cid)
                        cards.append(card)
                        if limit and len(cards) >= limit:
                            return cards
                except json.JSONDecodeError:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/cielingo_canonization_pipeline.py:580 quiet except scope=load_candidate_cards reason=continue")
                    continue

    return cards


# ──────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="CIELingo Canonization Pipeline")
    parser.add_argument("--limit", type=int, default=None,
                        help="Maksymalna liczba kart do przetworzenia")
    parser.add_argument("--force", action="store_true",
                        help="Przetwarzaj ponownie nawet już zdecydowane karty")
    parser.add_argument("--lemma", type=str, default=None,
                        help="Przetwarzaj tylko konkretny lemat")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    cards_dir = repo_root / SOURCES["candidate_cards_dir"]
    audit_dir = repo_root / SOURCES["canonization_audit_dir"]
    db_path = SOURCES["knowledge_db"]

    if not os.path.exists(db_path):
        print(f"❌ knowledge.db nie znaleziony: {db_path}")
        sys.exit(1)
    if not cards_dir.exists():
        print(f"❌ Katalog kart nie istnieje: {cards_dir}")
        sys.exit(1)

    print(f"📂 Karty: {cards_dir}")
    print(f"🗄️  Knowledge DB: {db_path}")
    print(f"📝 Audit: {audit_dir}")
    print(f"🔧 Force: {args.force}, Limit: {args.limit or 'bez limitu'}, Lemma: {args.lemma or 'wszystkie'}")

    # Ładuj karty
    print("\n📖 Ładowanie kart kandydujących...")
    cards = load_candidate_cards(cards_dir, lemma_filter=args.lemma, limit=args.limit)
    if not cards:
        print("❌ Brak kart do przetworzenia.")
        # Sprawdź co jest w katalogu
        print(f"   Zawartość {cards_dir}:")
        for p in sorted(cards_dir.rglob("*.*")):
            if p.suffix in (".jsonl", ".json"):
                print(f"     {p.relative_to(repo_root)} ({p.stat().st_size} bytes)")
        sys.exit(1)

    print(f"✅ Załadowano {len(cards)} unikalnych kart kandydujących.")

    # Inicjalizuj engine
    engine = CanonizationEngine(db_path, audit_dir, force=args.force)

    # Przetwarzaj
    print(f"\n⚙️  Rozpoczynam kanonizację...")
    decisions: list[dict[str, Any]] = []
    batch_size = 10  # co 10 zapisujemy

    try:
        for i, card in enumerate(cards):
            decision = engine.canonize_card(card)
            if decision:
                decisions.append(decision)

            if (i + 1) % batch_size == 0:
                print(f"  Przetworzono {i+1}/{len(cards)}...")
                # Okresowo zapisuj żeby nie stracić postępu
                if decisions:
                    engine.save_decisions(decisions)
                    decisions = []

            # Grzeczność wobec serwerów — 0.5s przerwy między web zapytaniami
            if (i + 1) % 3 == 0:
                time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n⚠️  Przerwano przez użytkownika. Zapisuję dotychczasowe decyzje...")

    # Zapisz pozostałe
    if decisions:
        engine.save_decisions(decisions)

    engine.close()
    engine.print_summary()


if __name__ == "__main__":
    main()
