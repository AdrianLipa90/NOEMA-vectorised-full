#!/usr/bin/env python3
"""
NOEMA Skill Enrichment & Catalog Generator
===========================================
Przetwarza wszystkie 293 skille w .opencode/skills/:
  1. Nadaje numery katalogowe (SK-XXX)
  2. Klasyfikuje do grup typów i zastosowań
  3. Przypisuje tagi holonomii semantycznej
  4. Generuje opis zastosowania + odnośniki
  5. Aktualizuje SKILLS.md z pełnym katalogiem

Użycie:
  python3 scripts/noema_skill_enrichment.py --dry-run    # podgląd
  python3 scripts/noema_skill_enrichment.py              # pełne generowanie
"""

import os, sys, json, re, pathlib
from datetime import date

# ─── Ścieżki ──────────────────────────────────────────────────────────────
SKILLS_DIR = pathlib.Path(__file__).resolve().parent.parent / ".opencode" / "skills"
SKILLS_MD = pathlib.Path(__file__).resolve().parent.parent / "SKILLS.md"
CACHE_FILE = pathlib.Path(__file__).resolve().parent.parent / ".opencode" / "skill_catalog.json"

# ─── TAKSONOMIA ───────────────────────────────────────────────────────────

# Grupy typów (rodzaj skilla)
TYPE_GROUPS = {
    "SYS":  {"name": "Systemowe",       "desc": "Daemony, surface, rdzeń NOEMA"},
    "COMP": {"name": "Komputacyjne",    "desc": "Algorytmy, propagation, Kuramoto, HTRI"},
    "SEM":  {"name": "Semantyczne",     "desc": "CIELingo, znaczenie, koncepty, meaning"},
    "LING": {"name": "Lingwistyczne",   "desc": "Lingofizyka, gramatyka, LNS, operatory"},
    "MEM":  {"name": "Pamięciowe",      "desc": "Tiered memory, konsolidacja, przechowywanie"},
    "ID":   {"name": "Tożsamościowe",   "desc": "Agent, self, tożsamość, CIEL"},
    "AUD":  {"name": "Audytowe",        "desc": "Audyt, walidacja, QA, testy"},
    "VIZ":  {"name": "Wizualizacyjne",  "desc": "Renderowanie, Poincaré, wykresy, dysk"},
    "DOC":  {"name": "Dokumentacyjne",  "desc": "Dokumentacja, architektura, przewodniki"},
    "HW":   {"name": "Sprzętowe",       "desc": "Sensory, GPU, eBPF, linux-cards"},
    "NET":  {"name": "Sieciowe",        "desc": "Nonlocal, neutrino, web, portal"},
    "VOICE":{"name": "Głosowe",         "desc": "Voice, audio, whisper, dźwięk"},
    "SEC":  {"name": "Bezpieczeństwo",  "desc": "Bezpieczeństwo, sekrety, immutable contract"},
}

# Grupy zastosowań użytkowych
APP_GROUPS = {
    "AUDIT":  {"name": "Audyt systemu",      "desc": "Przeprowadzanie audytu, walidacja"},
    "HEALTH": {"name": "Health check",       "desc": "Sprawdzanie zdrowia, diagnostyka"},
    "EPH":    {"name": "Efemerydy",           "desc": "Liczenie efemeryd, orbity, grawitacja"},
    "VIZ":    {"name": "Wizualizacja",        "desc": "Tworzenie obrazów, wykresów, render"},
    "MEMORY": {"name": "Zarządzanie pamięcią","desc": "Konsolidacja, przechowywanie, recall"},
    "BACKUP": {"name": "Backup/archiwizacja", "desc": "Archiwizacja, hibernacja, snapshot"},
    "DEV":    {"name": "Developerskie",       "desc": "Narzędzia deweloperskie, budowanie"},
    "NET":    {"name": "Komunikacja sieciowa", "desc": "Sieć, nonlocal, neutrino, HTTP"},
    "VOICE":  {"name": "Interakcja głosowa",  "desc": "Voice, audio, hotkey"},
    "SEC":    {"name": "Bezpieczeństwo",      "desc": "Security, secrets, immutable"},
}

# Mapowanie prefiksów katalogów → grupy typów
PREFIX_TO_TYPE = {
    "noema-kuramoto": "COMP", "noema-euler": "COMP", "noema-phase": "MEM",
    "noema-analog": "SYS", "noema-agent": "ID", "noema-audit": "AUD",
    "noema-build": "DEV", "noema-canon": "SYS", "noema-catalog": "DOC",
    "noema-cli": "SYS", "noema-code": "DEV", "noema-crossref": "DOC",
    "noema-daemon": "SYS", "noema-documentation": "DOC", "noema-dream": "VOICE",
    "noema-ebpf": "HW", "noema-generate": "DEV", "noema-hibernation": "MEM",
    "noema-holonomic": "COMP", "noema-hybrid": "COMP", "noema-immutable": "ID",
    "noema-import": "MEM", "noema-indexer": "MEM", "noema-inference": "COMP",
    "noema-inject": "SYS", "noema-knowledge": "SEM", "noema-learn": "MEM",
    "noema-lora": "COMP", "noema-noemized": "MEM", "noema-query": "MEM",
    "noema-repo": "DOC", "noema-resolve": "SEM", "noema-sapiens": "ID",
    "noema-search": "SEM", "noema-secret": "SEC", "noema-self": "ID",
    "noema-settings": "SYS", "noema-sims": "COMP", "noema-sonic": "AUD",
    "noema-status": "AUD", "noema-stress": "AUD", "noema-system": "SYS",
    "noema-systemd": "SYS", "noema-test": "AUD", "noema-unified": "SYS",
    "noema-vector": "NET", "noema-watchdog": "AUD", "noema-web": "NET",
    "noema-ops": "DOC", "noema-audio": "VOICE", "noema-voice": "VOICE",
    "noema-noema": "SYS", "noema-": "SYS",
    "cielingo-": "SEM", "cielingo-core": "SEM", "cielingo-bridge": "SEM",
    "cielingo-canon": "SEM", "cielingo-card": "SEM", "cielingo-base": "SEM",
    "cielingo-audit": "AUD", "ciel-": "ID", "ciel-cielocal": "ID",
    "ciel-codex": "SEM", "ciel-converse": "ID", "ciel-couple": "ID",
    "ciel-engine": "COMP", "ciel-identity": "ID", "ciel-infohub": "SEM",
    "ciel-lingophysics": "LING", "ciel-memory": "MEM", "ciel-monitoring": "AUD",
    "ciel-omega": "SYS", "ciel-orbital": "COMP", "ciel-pipeline": "DEV",
    "ciel-rh": "SYS", "ciel-relational": "SEM", "ciel-security": "SEC",
    "ciel-sot": "SYS", "ciel-subconscious": "ID", "ciel-tools": "DEV",
    "lns-": "LING", "lns-rpt-": "LING",
    "orbital-": "COMP", "odemo-": "DOC", "odemo-news-": "DOC",
    "odemo-studies-": "DOC", "odemo-analogies-": "DOC", "odemo-root-": "DOC",
    "odemo-system-": "DOC", "omega-": "SYS", "doc-": "DOC",
    "agent-": "ID", "affective-": "SEM", "canon-": "AUD",
    "concept-": "SEM", "consciousness-": "ID", "continuous-": "COMP",
    "daemon-": "SYS", "debug-": "AUD", "eBPF-": "HW",
    "emergency-": "SEC", "htri-": "HW", "identity-": "ID",
    "kuramoto-": "COMP", "linux-": "HW", "loader-": "MEM",
    "memory-": "MEM", "metatime-": "COMP", "nbody-": "COMP",
    "neutrino-": "NET", "nonlocal-": "NET", "operator-": "LING",
    "phase-": "COMP", "phasenav-": "SYS", "poincare-": "VIZ",
    "renderer-": "VIZ", "semantic-": "SEM", "session-": "SYS",
    "snap-": "DEV", "stress-": "COMP", "subconscious-": "ID",
    "subjective-": "SEM", "surface-": "SYS", "synchronize-": "SYS",
    "system-": "AUD", "tardis-": "COMP", "teleusing-": "NET",
    "tiered-": "MEM", "truth-": "SEM",
    "workben-system": "SYS", "workben-phasenav": "SYS", "workben-kuramoto": "COMP",
    "workben-memory": "MEM", "workben-identity": "ID", "workben-cielingo": "SEM",
    "workben-linux": "HW", "workben-debug": "AUD", "workben-net": "NET", "workben-dev": "DEV",
}

# Mapowanie prefiksów → tagi holonomii (M kanały + operator domains)
PREFIX_TO_HOLONOMY = {
    "agent-": ["M1", "AGENT", "EMOTION"],
    "attractor": ["M1", "M2", "AGENT", "MEMORY"],
    "affective-": ["M5", "AFFECT", "EMOTION"],
    "cielingo-": ["M3", "M7", "SCOPE", "MODAL", "CONDITION", "NEGATION"],
    "ciel-identity": ["M1", "AGENT", "SELF"],
    "ciel-memory": ["M2", "M6", "MEMORY", "TEMPORAL"],
    "ciel-lingophysics": ["M3", "M7", "SCOPE", "ASPECT"],
    "concept-": ["M3", "SEMANTIC", "SCOPE"],
    "consciousness-": ["M6", "M8", "AGENT", "SELF"],
    "continuous-": ["M0", "M7", "TEMPORAL"],
    "daemon-": ["SYS", "M4"],
    "debug-": ["M0", "M4"],
    "doc-": ["M2", "M4"],
    "eBPF-": ["M0", "HW"],
    "emergency-": ["M8", "M1"],
    "htri-": ["M7", "M0"],
    "identity-": ["M1", "M6"],
    "kuramoto-": ["M0", "M7", "TEMPORAL", "CONDITION"],
    "linux-": ["M0", "M4"],
    "loader-": ["M2", "M4"],
    "lns-": ["M3", "M7", "SCOPE", "MODAL", "ASPECT", "NEGATION", "CONDITION"],
    "lns-rpt-": ["M3", "M7", "SCOPE"],
    "memory-": ["M2", "M6", "MEMORY", "TEMPORAL"],
    "metatime-": ["M7", "M8", "TEMPORAL", "CONDITION"],
    "nbody-": ["M0", "M7", "TEMPORAL"],
    "neutrino-": ["M5", "NET", "CONDITION"],
    "noema-agent-": ["M1", "AGENT"],
    "noema-analog": ["SYS", "M7"],
    "noema-audit": ["M2", "AUDIT"],
    "noema-build": ["M4", "DEV"],
    "noema-canon": ["SYS", "M7"],
    "noema-cli": ["M4", "SYS"],
    "noema-code": ["M4", "DEV"],
    "noema-daemon": ["SYS", "M4"],
    "noema-dream": ["M6", "M8", "VOICE"],
    "noema-ebpf": ["M0", "HW"],
    "noema-euler": ["M7", "CONDITION", "TEMPORAL"],
    "noema-generate": ["M4", "DEV"],
    "noema-hibernation": ["M2", "M6", "MEMORY"],
    "noema-holonomic": ["M7", "COMP"],
    "noema-hybrid": ["M7", "COMP"],
    "noema-immutable": ["M1", "ID"],
    "noema-import": ["M2", "MEMORY"],
    "noema-indexer": ["M3", "MEMORY"],
    "noema-inference": ["M3", "COMP"],
    "noema-inject": ["SYS", "M5"],
    "noema-knowledge": ["M3", "SEMANTIC"],
    "noema-kuramoto": ["M0", "M7"],
    "noema-learn": ["M2", "M6"],
    "noema-lora": ["M4", "COMP"],
    "noema-noemized": ["M2", "M6"],
    "noema-phase": ["M2", "MEMORY"],
    "noema-query": ["M2", "M3"],
    "noema-sapiens": ["M1", "M6"],
    "noema-search": ["M3", "SEMANTIC"],
    "noema-secret": ["M8", "SEC"],
    "noema-self": ["M1", "M6"],
    "noema-sonic": ["M0", "AUDIT"],
    "noema-status": ["M0", "AUDIT"],
    "noema-system": ["SYS", "M7"],
    "noema-test": ["M4", "AUDIT"],
    "noema-unified": ["SYS"],
    "noema-vector": ["NET", "M7"],
    "noema-watchdog": ["M0", "AUDIT"],
    "noema-web": ["NET"],
    "noema-voice": ["VOICE", "M6"],
    "nonlocal-": ["NET", "M7"],
    "odemo-": ["M2", "M3"],
    "omega-": ["SYS", "M7"],
    "operator-": ["M3", "M7", "SCOPE"],
    "orbital-": ["M7", "COMP", "TEMPORAL"],
    "phase-": ["M2", "M7", "MEMORY"],
    "phasenav-": ["SYS", "M7"],
    "poincare-": ["VIZ", "M7"],
    "renderer-": ["VIZ", "M0"],
    "semantic-": ["M3", "M5", "SEMANTIC", "AFFECT"],
    "session-": ["SYS", "M1"],
    "subconscious-": ["M6", "M8"],
    "subjective-": ["M7", "TEMPORAL"],
    "surface-": ["M0", "SYS"],
    "workben-": ["SYS", "M7", "CONSOLIDATION"],
    "synchronize-": ["M7", "NET"],
    "system-": ["AUDIT", "M0"],
    "tardis-": ["M7", "TEMPORAL"],
    "tiered-": ["M2", "M6", "MEMORY"],
    "ciel-relational": ["M3", "M7", "SCOPE"],
    "ciel-subconscious": ["M6", "M8"],
    "ciel-security": ["M8", "SEC"],
}

# Mapowanie na grupy zastosowań
PREFIX_TO_APP = {
    # ── AUDYT ──
    "canon-audit": "AUDIT", "debug-": "AUDIT",
    "holonomic-": "AUDIT", "monitoring": "AUDIT", "sonic": "AUDIT",
    "status": "AUDIT", "stress-": "AUDIT", "system-health": "AUDIT",
    "test-": "AUDIT", "watchdog": "AUDIT", "metatime-": "AUDIT",
    "cielingo-audit": "AUDIT", "cielingo-": "AUDIT",
    "affective-": "AUDIT", "concept-": "AUDIT",
    "consciousness-": "AUDIT", "semantic-": "AUDIT",
    "ciel-monitoring": "AUDIT", "cielingo-canon": "AUDIT",
    "noema-search": "AUDIT", "noema-knowledge": "AUDIT",
    "noema-crossref": "AUDIT", "noema-documentation": "AUDIT",
    "noema-sonic": "AUDIT", "noema-status": "AUDIT",
    "noema-stress": "AUDIT", "noema-test": "AUDIT",
    "noema-watchdog": "AUDIT", "noema-holonomic": "AUDIT",
    "system-health": "AUDIT", "canon-": "AUDIT",
    # ── HEALTH ──
    "debug-surface": "HEALTH", "system-health-check": "HEALTH",
    "emergency-": "HEALTH", "recovery": "HEALTH",
    # ── EFEMERYDY ──
    "nbody-": "EPH", "orbital-": "EPH",
    "semantic-mass": "EPH", "gravity": "EPH",
    "subjective-": "EPH", "tardis-": "EPH",
    "metatime-": "EPH",
    # ── WIZUALIZACJA ──
    "poincare-": "VIZ", "renderer-": "VIZ",
    "heatmap": "VIZ", "graph": "VIZ", "disk": "VIZ",
    "noema-viz": "VIZ",
    # ── PAMIĘĆ ──
    "memory-": "MEMORY", "tiered-": "MEMORY", "loader-": "MEMORY",
    "learn": "MEMORY", "recall": "MEMORY", "noemized": "MEMORY",
    "indexer": "MEMORY", "query": "MEMORY", "import": "MEMORY",
    "ciel-memory": "MEMORY", "noema-learn": "MEMORY",
    "noema-indexer": "MEMORY", "noema-query": "MEMORY",
    "noema-noemized": "MEMORY", "noema-import": "MEMORY",
    "noema-hibernation": "MEMORY", "phase-memory": "MEMORY",
    "noema-phase": "MEMORY", "phase-archiver": "BACKUP",
    # ── BACKUP ──
    "hibernation": "BACKUP", "backup": "BACKUP",
    "archiver": "BACKUP",
    # ── DEVELOPERSKIE ──
    "codegen": "DEV", "build-": "DEV", "pipeline": "DEV",
    "generate": "DEV", "hybrid-": "DEV", "lora": "DEV",
    "snap-": "DEV", "ciel-engine": "DEV",
    "ciel-pipeline": "DEV", "ciel-tools": "DEV",
    "noema-build": "DEV", "noema-code": "DEV",
    "noema-generate": "DEV", "noema-hybrid": "DEV",
    "noema-lora": "DEV", "noema-cli": "DEV",
    # ── SIECIOWE ──
    "nonlocal": "NET", "neutrino": "NET", "web": "NET",
    "vector-phone": "NET", "teleusing": "NET",
    "noema-vector": "NET", "noema-web": "NET",
    "noema-portal": "NET",
    "noema-portal": "NET",
    # ── WORKBENY ──
    "workben-system": "SYS", "workben-phasenav": "SYS",
    "workben-kuramoto": "COMP", "workben-memory": "MEMORY",
    "workben-identity": "ID", "workben-cielingo": "SEM",
    "workben-linux": "HW", "workben-debug": "AUDIT",
    "workben-net": "NET", "workben-dev": "DEV",
    # ── GŁOSOWE ──
    "voice": "VOICE", "audio": "VOICE", "dream": "VOICE",
    "noema-voice": "VOICE", "noema-audio": "VOICE",
    "noema-dream": "VOICE",
    # ── BEZPIECZEŃSTWO ──
    "secret": "SEC", "security": "SEC", "immutable": "SEC",
    "ciel-security": "SEC", "noema-secret": "SEC",
    "noema-immutable": "SEC", "emergency-": "SEC",
    # ── SEMANTYKA (przeszukiwanie) ──
    "noema-search": "AUDIT", "noema-knowledge": "AUDIT",
    "noema-resolve": "AUDIT",
}

# ─── TAGI FUNKCJI ─────────────────────────────────────────────────────────
# Co skill ROBI na poziomie funkcjonalnym

FUNCTION_TAGS = {
    "read": "Odczyt danych/systemu",
    "write": "Zapis na surface/do bazy",
    "compute": "Obliczenia, algebra, symulacje",
    "transform": "Transformacja danych/stanu",
    "analyze": "Analiza, diagnostyka, audyt",
    "generate": "Generowanie kodu/treści",
    "monitor": "Monitorowanie, obserwacja",
    "control": "Sterowanie, restart, zarządzanie",
    "sync": "Synchronizacja, bridging",
    "store": "Przechowywanie, archiwizacja",
    "retrieve": "Wyszukiwanie, recall, query",
    "visualize": "Wizualizacja, renderowanie",
    "communicate": "Komunikacja sieciowa, nonlocal",
    "secure": "Bezpieczeństwo, izolacja",
    "configure": "Konfiguracja, setup",
    "learn": "Uczenie, adaptacja, konsolidacja",
    "reason": "Wnioskowanie, meaning, intent",
    "couple": "Sprzężenie, coupling, PMNS",
}

PREFIX_TO_FUNCTION = {
    "agent-": ["reason", "couple", "control"],
    "attractor": ["couple", "control", "transform"],
    "affective-": ["analyze", "transform"],
    "cielingo-": ["reason", "analyze", "transform"],
    "ciel-identity": ["reason", "couple"],
    "ciel-memory": ["store", "retrieve", "learn"],
    "ciel-lingophysics": ["analyze", "reason"],
    "concept-": ["analyze", "reason"],
    "consciousness-": ["reason", "monitor"],
    "continuous-": ["compute", "transform"],
    "daemon-": ["control", "monitor"],
    "debug-": ["analyze", "monitor"],
    "doc-": ["analyze", "retrieve"],
    "eBPF-": ["monitor", "read"],
    "emergency-": ["secure", "control"],
    "htri-": ["compute", "couple"],
    "identity-": ["reason", "couple"],
    "kuramoto-": ["compute", "sync", "transform"],
    "linux-": ["read", "monitor"],
    "loader-": ["store", "retrieve"],
    "lns-": ["analyze", "reason"],
    "lns-rpt-": ["analyze", "configure"],
    "memory-": ["store", "retrieve", "learn"],
    "metatime-": ["compute", "reason"],
    "nbody-": ["compute", "visualize"],
    "neutrino-": ["communicate", "couple"],
    "noema-agent-": ["reason", "couple", "control"],
    "noema-analog": ["transform", "sync"],
    "noema-audit": ["analyze", "monitor"],
    "noema-audio": ["communicate", "generate"],
    "noema-build": ["configure", "generate"],
    "noema-canon": ["control", "analyze"],
    "noema-catalog": ["retrieve", "analyze"],
    "noema-cli": ["control", "configure"],
    "noema-code": ["generate", "transform"],
    "noema-crossref": ["retrieve", "analyze"],
    "noema-daemon": ["control", "monitor"],
    "noema-documentation": ["retrieve", "analyze"],
    "noema-dream": ["generate", "communicate"],
    "noema-ebpf": ["read", "monitor"],
    "noema-euler": ["compute", "sync", "transform"],
    "noema-generate": ["generate", "configure"],
    "noema-hibernation": ["store", "secure"],
    "noema-holonomic": ["compute", "analyze"],
    "noema-hybrid": ["compute", "transform"],
    "noema-immutable": ["secure", "configure"],
    "noema-import": ["read", "store"],
    "noema-indexer": ["analyze", "store"],
    "noema-inference": ["reason", "compute"],
    "noema-inject": ["write", "transform"],
    "noema-knowledge": ["retrieve", "analyze"],
    "noema-kuramoto": ["compute", "sync"],
    "noema-learn": ["learn", "store"],
    "noema-lora": ["learn", "configure"],
    "noema-noemized": ["retrieve", "transform"],
    "noema-phase": ["store", "retrieve"],
    "noema-query": ["retrieve", "analyze"],
    "noema-sapiens": ["reason", "configure"],
    "noema-search": ["retrieve", "analyze"],
    "noema-secret": ["secure", "configure"],
    "noema-self": ["reason", "monitor"],
    "noema-settings": ["configure", "sync"],
    "noema-sims": ["compute", "visualize"],
    "noema-sonic": ["analyze", "monitor"],
    "noema-status": ["read", "analyze"],
    "noema-stress": ["analyze", "monitor"],
    "noema-system": ["configure", "control"],
    "noema-systemd": ["configure", "control"],
    "noema-test": ["analyze", "monitor"],
    "noema-unified": ["configure", "control"],
    "noema-vector": ["communicate", "sync"],
    "noema-voice": ["communicate", "generate"],
    "noema-watchdog": ["monitor", "control"],
    "noema-web": ["communicate", "visualize"],
    "noema-ops": ["configure", "control"],
    "nonlocal-": ["communicate", "sync"],
    "odemo-": ["analyze", "retrieve"],
    "omega-": ["configure", "control"],
    "operator-": ["analyze", "reason"],
    "orbital-": ["compute", "visualize"],
    "phase-": ["store", "retrieve", "compute"],
    "phasenav-": ["compute", "sync"],
    "poincare-": ["visualize", "compute"],
    "renderer-": ["visualize", "generate"],
    "semantic-": ["analyze", "reason"],
    "session-": ["control", "store"],
    "snap-": ["read", "analyze"],
    "stress-": ["compute", "analyze"],
    "subconscious-": ["reason", "monitor"],
    "subjective-": ["compute", "reason"],
    "surface-": ["read", "write", "configure"],
    "synchronize-": ["sync", "control"],
    "system-": ["analyze", "monitor"],
    "tardis-": ["compute", "transform"],
    "teleusing-": ["communicate", "control"],
    "tiered-": ["store", "retrieve", "learn"],
    "truth-": ["reason", "analyze"],
    "android-": ["analyze", "read"],
    "snap-ocr": ["read", "analyze", "transform"],
    "canon-": ["analyze", "control"],
    "metatime-": ["compute", "analyze"],
    "workben-": ["configure", "analyze", "retrieve"],
}

# ─── MAPOWANIE NA ORBITALE (8+1 sphere) ──────────────────────────────────
# M0-M8 to kanały pamięci NOEMA — każdy skill ma primary orbital
# Wyciągane z tagów holonomii (pierwsze M{0-8})

ORBITAL_NAMES = {
    "M0": "Perception (percepcja)",
    "M1": "Self/Agent (tożsamość)",
    "M2": "Memory (pamięć jawna)",
    "M3": "Semantic (semantyka)",
    "M4": "Procedural (procedury)",
    "M5": "Affect (afekt)",
    "M6": "Consciousness (świadomość)",
    "M7": "Braid (splot)",
    "M8": "Void (nicość/potencjał)",
}


def extract_primary_orbital(holonomy_tags):
    """Wyciągnij primary orbital z tagów holonomii (pierwsze M{0-8})."""
    for tag in holonomy_tags:
        if tag.startswith("M") and len(tag) == 2 and tag[1].isdigit():
            return tag
    return "M3"  # default


def compute_semantic_mass(entry):
    """Oblicz masę semantyczną skilla na podstawie metadanych."""
    mass = 1.0
    # + za tagi holonomii
    mass += len(entry.get("holonomy", [])) * 0.15
    # + za tagi funkcji
    mass += len(entry.get("function_tags", [])) * 0.1
    # + za opis (długość)
    desc = entry.get("description", "")
    if len(desc) > 80:
        mass += 0.3
    elif len(desc) > 40:
        mass += 0.15
    # + za referencję do skryptu
    if entry.get("script_ref") and entry["script_ref"] != "—":
        mass += 0.4
    # + za aplikację
    if entry.get("app_group"):
        mass += 0.2
    # Masa orbitalna (modulowana przez primary orbital)
    orb = entry.get("primary_orbital", "M3")
    orb_mult = {"M0": 0.9, "M1": 1.1, "M2": 1.0, "M3": 1.0,
                "M4": 0.9, "M5": 1.1, "M6": 1.2, "M7": 1.3, "M8": 1.4}
    mass *= orb_mult.get(orb, 1.0)
    # Zaokrąglij
    return round(mass, 3)


# Mapowanie na główne skrypty/moduly (gdzie znane)
SKILL_TO_SCRIPT = {
    "noema-system": "system: architektura (docs/)",
    "noema-kuramoto-substrate": "scripts/ciel_noema_kuramoto_daemon.py",
    "noema-euler-propagation": "src/ciel_geometry/noema_surface_mmap.py → evolve_surface()",
    "noema-agent-backend": "scripts/ciel_agent_backend.py",
    "noema-agent-rules": "AGENTS.md",
    "noema-analog-phasenav": "src/ciel_geometry/analog_bus.py + scripts/noema_analog_phase_blend.py",
    "noema-audio-orbital": "src/ciel_geometry/voice.py?",
    "noema-audit-consolidator": "scripts/noema_audit_consolidator.py",
    "noema-build-system": "pyproject.toml + setup.py",
    "noema-canon": "scripts/CIEL_CANON.py",
    "noema-catalog-zips": "pdf_catalog.noema.json",
    "noema-cli": "CLI tools (brak osobnego skryptu)",
    "noema-code-bridge": "bridge (docs/)",
    "noema-codegen": "wzorce (docs/)",
    "noema-crossref": "scripts/noema_crossref.py?",
    "noema-daemon-consolidation": "scripts/ciel_noema_resonance_bridge.py (merger)",
    "noema-daemon-hook": "wzorzec: Registry() + systemd",
    "noema-documentation": "docs/",
    "noema-dream-whisper": "scripts/noema_dream_whisper.py",
    "noema-ebpf-daemon": "src/ciel_geometry/ebpf_noema_loader.py",
    "noema-generate-cards": "src/ciel_geometry/linux_cards.py",
    "noema-hibernation": "scripts/noema_hibernation.py",
    "noema-holonomic-audit": "src/ciel_geometry/phasenav_unified.py → holonomy()",
    "noema-holonomic-doctor": "src/ciel_geometry/phasenav_unified.py → holonomy()",
    "noema-hybrid-runner": "src/ciel_geometry/continuous_propagator.py",
    "noema-immutable-contract": "AGENTS.md (🔴 IMMUTABLE)",
    "noema-import-chatgpt": "scripts/noema_import_chatgpt.py",
    "noema-indexer": "scripts/noema_library_indexer.py",
    "noema-inference": "docs/ (inference gate)",
    "noema-inject-coupling": "scripts/noema_inject_coupling.py",
    "noema-knowledge-graph": "scripts/noema_knowledge_graph.py",
    "noema-learn-file": "scripts/noema_learn_file.py",
    "noema-learned": "rejestr (docs/)",
    "noema-lora": "dla przyszłości (docs/)",
    "noema-noemized-recall": "scripts/noemized_recall.py",
    "noema-phase-archiver": "scripts/noema_phase_archiver.py",
    "noema-query-cache": "wzorzec (docs/)",
    "noema-repo-coupling": "scripts/noema_repo_coupling.py",
    "noema-resolve-orbital": "scripts/noema_resolve_orbital.py",
    "noema-sapiens": "AGENTS.md (AI-Sapiens contract)",
    "noema-search": "src/cielingo_core/bridge/knowledge_bridge.py → query()",
    "noema-secret-loader": "scripts/noema_secret_loader.py",
    "noema-self-reflect": "scripts/noema_self_reflect.py",
    "noema-settings-sync": "scripts/noema_settings_sync.py",
    "noema-sims": "scripts/noema_sims.py",
    "noema-sonic-diagnostic": "scripts/noema_sonic_daemon.py",
    "noema-status": "scripts/noema_status.py",
    "noema-stress-tests": "scripts/noema_stress_tests.py",
    "noema-systemd-target": ".config/systemd/user/noema.target",
    "noema-test-infra": "scripts/noema_test_infra.py",
    "noema-unified-config": "src/ciel_geometry/noema_config.py + noema_config.json",
    "noema-vector-phone": "scripts/noema_vector_phone.py",
    "noema-watchdog": "scripts/noema_watchdog.py",
    "noema-web": "scripts/noema_portal_daemon.py",
    "noema-ops": "SKILLS.md → noema-ops.md",
    # CIELingo
    "cielingo-core-structure": "src/cielingo_core/",
    "cielingo-bridge": "src/cielingo_core/bridge/",
    "cielingo-canon": "scripts/CIEL_CANON.py (część lingwistyczna)",
    "cielingo-card-import": "src/cielingo_core/card_import/",
    "cielingo-base-scripts": "scripts/cielingo_*.py",
    "cielingo-audit-tools": "src/cielingo_core/generative_audit.py",
    "ciel-omega-complete": "src/CIEL_OMEGA_COMPLETE_SYSTEM/",
    "ciel-orbital-foundation": "docs/CIEL_ORBITAL_FOUNDATION.md",
    "ciel-engine-subsystem": "src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/ciel/engine.py",
    "ciel-cielocal": "tryb offline (opencode.json)",
    "ciel-codex-bridge": "src/cielingo_core/bridge/",
    "ciel-converse": "wzorzec (docs/)",
    "ciel-couple-assistant": "scripts/ciel_coupling.py",
    "ciel-identity-persistence": "state_db (identity_seed table)",
    "ciel-infohub": "docs/",
    "ciel-lingophysics-lns": "src/cielingo_core/global_layer/",
    "ciel-memory-handoff": "scripts/ciel_session_hook.py + handoff.md",
    "ciel-memory-system": "src/ciel_omega/memory/",
    "ciel-memory-tools": "scripts/ciel_memory_tools.py",
    "ciel-monitoring": "scripts/ciel_monitoring.py",
    "ciel-pipeline": "scripts/ciel_pipeline.py",
    "ciel-pipeline-builder": "scripts/ciel_pipeline_builder.py",
    "ciel-relational-mechanism": "docs/",
    "ciel-rh-control": "scripts/ciel_rh_control.py",
    "ciel-secret-loader": "scripts/ciel_secret_loader.py",
    "ciel-security-model": "docs/ciel_security_model.md",
    "ciel-sot-agent-gui": "gui/",
    "ciel-subconscious": "src/ciel_geometry/subconscious.py",
    "ciel-tools": "scripts/ciel_tools.py",
    # Named skills
    "agent-attractor": "src/ciel_geometry/agent_attractor.py",
    "affective-lexicon-bridge": "src/cielingo_core/bridge/",
    "canon-audit": "scripts/CIEL_CANON.py --audit",
    "concept-lifecycle": "docs/",
    "consciousness-vocabulary": "docs/",
    "continuous-propagator": "src/ciel_geometry/continuous_propagator.py",
    "daemon-pattern": "wzorzec (NOEMA_DEBUG.md)",
    "debug-surface": "NOEMA_DEBUG.md → szybkie testy",
    "eBPF-sensor": "src/ciel_geometry/ebpf_noema_loader.py",
    "emergency-recovery": "procedura (docs/)",
    "htri-gpu-bridge": "docs/",
    "htri-hardware": "docs/",
    "identity-bridge": "src/cielingo_core/bridge/",
    "kuramoto-euler-sync": "src/ciel_geometry/noema_surface_mmap.py → evolve_surface()",
    "kuramoto-harmonics": "src/ciel_geometry/noema_surface_mmap.py → harmonic 3-6-9",
    "linux-cards": "src/ciel_geometry/linux_cards.py + scripts/noema_linux_cards_daemon.py",
    "linux-sensor": "src/ciel_geometry/linux_sensor.py + scripts/ciel_noema_linux_sensor_daemon.py",
    "loader-edges": "src/ciel_geometry/loader.py + edges.py",
    "memory-consolidation": "scripts/ciel_memory_consolidator.py",
    "memory-lane-monitor": "scripts/noema_memory_lane_monitor.py",
    "memory-lane-seed": "scripts/noema_memory_lane_seed.py",
    "metatime-validator": "scripts/metatime_v8_redteam_validator.py",
    "nbody-gravity": "src/ciel_geometry/nbody_gravity.py",
    "neutrino-bus": "src/ciel_geometry/neutrino_phase_channel.py",
    "noema-agent-backend": "scripts/ciel_agent_backend.py",
    "noema-daemon-consolidation": "scripts/ciel_noema_resonance_bridge.py",
    "nonlocal-channel": "src/ciel_geometry/nonlocal_channel.py",
    "operator-algebra": "src/cielingo_core/global_layer/operator_algebra.py",
    "phase-algebra": "src/ciel_geometry/phasenav_unified.py",
    "phase-memory-adapter": "src/ciel_geometry/phase_memory.py",
    "phasenav-enrichment": "src/ciel_geometry/phasenav_unified.py",
    "phasenav-loader": "src/ciel_geometry/phasenav_unified.py",
    "phasenav-solver": "src/ciel_geometry/phasenav_unified.py",
    "poincare-disk": "src/ciel_geometry/disk.py + layout.py",
    "poincare-orbital-viz": "src/ciel_geometry/renderer_mpl.py",
    "renderer-phasedisk": "src/ciel_geometry/renderer_ascii.py + renderer_mpl.py",
    "semantic-affective-fusion": "src/cielingo_core/global_layer/",
    "semantic-mass": "src/ciel_geometry/semantic_mass.py",
    "session-lifecycle": "scripts/ciel_session_hook.py + ciel_session_end.py",
    "snap-ocr": "scripts/ocr_fix.py",
    "stress-energy-tensor": "src/ciel_geometry/tmuv_perturbation.py",
    "subconscious": "src/ciel_geometry/subconscious.py",
    "subconscious-flow": "src/ciel_geometry/subconscious.py",
    "subjective-state-response": "docs/",
    "surface-mmap-protocol": "src/ciel_geometry/noema_surface_mmap.py",
    "synchronize": "scripts/noema_dual_sync.py (merged do resonance_bridge)",
    "system-health-check": "scripts/noema_doctor_cycle.py",
    "tardis-warp": "src/ciel_geometry/noema_surface_mmap.py → evolve_surface() (TARDIS/WARP)",
    "teleusing": "docs/",
    "tiered-memory-api": "src/ciel_omega/memory/tiered_orchestrator.py",
    "android-zip-analysis": "doc/",
    "noema-cielingo-core-structure": "src/cielingo_core/",
    "customize-opencode": "opencode.jsonc",
    "linux-cards": "src/ciel_geometry/linux_cards.py",
    "noema-generate-cards": "src/ciel_geometry/linux_cards.py",
    "noema-documentation": "docs/",
    "00-INDEX": "SKILLS.md (ten plik)",
    # Workbeny (konsolidacja)
    "workben-system": ".opencode/skills/workben-system/SKILL.md",
    "workben-phasenav": ".opencode/skills/workben-phasenav/SKILL.md",
    "workben-kuramoto": ".opencode/skills/workben-kuramoto/SKILL.md",
    "workben-memory": ".opencode/skills/workben-memory/SKILL.md",
    "workben-identity": ".opencode/skills/workben-identity/SKILL.md",
    "workben-cielingo": ".opencode/skills/workben-cielingo/SKILL.md",
    "workben-linux": ".opencode/skills/workben-linux/SKILL.md",
    "workben-debug": ".opencode/skills/workben-debug/SKILL.md",
    "workben-net": ".opencode/skills/workben-net/SKILL.md",
    "workben-dev": ".opencode/skills/workben-dev/SKILL.md",
}

# Opisy zastosowań (fallback dla nieznanych)
DEFAULT_DESC = {
    "lns-": "Lingwistyczny specyfikacja: definicje operatorów, reguł i struktur dla lingofizyki NOEMA.",
    "lns-rpt-": "Raport LNS: podsumowanie zmian i struktury w konkretnym zakresie lingofizyki.",
    "orbital-": "Orbital framework: definicje geometryczne, algebraiczne i systemowe dla orbitali NOEMA.",
    "odemo-news-": "Zbiór newsów: źródła informacji z danego regionu/kategorii.",
    "odemo-studies-": "Studium: analiza, dokumentacja i referencje z danego obszaru badań.",
    "odemo-analogies-": "Analogia: struktury porównawcze i przykłady dla danych konceptów.",
    "odemo-root-": "Dokument główny: index, spis treści, główna entry point dla dokumentacji.",
    "odemo-system-": "System: opis architektury i komponentów systemu.",
    "omega-": "Omega Runtime: agent, bridge, constraints, vocabulary dla systemu Omega.",
    "doc-": "Dokumentacja: opis architektury, komponentów i zasad systemu.",
    "noema-": "NOEMA system: narzędzie, daemon lub konfiguracja systemu NOEMA.",
    "cielingo-": "CIELingo: lingwistyczny subsystem NOEMA — znaczenie, gramatyka, atlasy.",
    "ciel-": "CIEL: rdzeń tożsamości i pamięci systemu CIEL.",
}


def classify_skill(name):
    """Klasyfikuj skill: typ, aplikacja, tagi holonomii, tagi funkcji."""
    name_lower = name.lower()
    
    # Znajdź dopasowanie prefiksu dla typu
    matched_prefix = ""
    for prefix in sorted(PREFIX_TO_TYPE.keys(), key=lambda x: len(x), reverse=True):
        if name_lower.startswith(prefix) or name_lower.startswith(prefix.replace("-", "_")):
            matched_prefix = prefix
            break
    
    type_group = PREFIX_TO_TYPE.get(matched_prefix, "SYS")
    
    # Holonomia
    holonomy = []
    for prefix in sorted(PREFIX_TO_HOLONOMY.keys(), key=lambda x: len(x), reverse=True):
        if name_lower.startswith(prefix) or name_lower.startswith(prefix.replace("-", "_")):
            holonomy = PREFIX_TO_HOLONOMY[prefix]
            break
    
    if not holonomy:
        # Fallback: genericzne tagi
        if any(k in name_lower for k in ["memory", "store", "recall", "index", "query", "learn"]):
            holonomy = ["M2", "M6", "MEMORY"]
        elif any(k in name_lower for k in ["agent", "self", "identity", "ciel", "converse"]):
            holonomy = ["M1", "AGENT"]
        elif any(k in name_lower for k in ["ling", "grammar", "operator", "scope", "word"]):
            holonomy = ["M3", "M7", "SCOPE"]
        elif any(k in name_lower for k in ["systemd", "daemon", "surface", "config", "shm"]):
            holonomy = ["SYS", "M0"]
        elif any(k in name_lower for k in ["viz", "render", "disk", "poincare", "graph"]):
            holonomy = ["VIZ", "M7"]
        elif any(k in name_lower for k in ["security", "secret", "immutable", "emergency"]):
            holonomy = ["M8", "SEC"]
        else:
            holonomy = ["M3", "M7"]  # default
    
    # Aplikacja
    app_group = None
    for prefix in sorted(PREFIX_TO_APP.keys(), key=lambda x: len(x), reverse=True):
        if name_lower.startswith(prefix) or name_lower.startswith(prefix.replace("-", "_")):
            app_group = PREFIX_TO_APP[prefix]
            break
    
    # Tagi funkcji
    function_tags = []
    for prefix in sorted(PREFIX_TO_FUNCTION.keys(), key=lambda x: len(x), reverse=True):
        if name_lower.startswith(prefix) or name_lower.startswith(prefix.replace("-", "_")):
            function_tags = PREFIX_TO_FUNCTION[prefix]
            break
    
    if not function_tags:
        # Fallback
        if any(k in name_lower for k in ["read", "scan", "sensor", "watch", "monitor"]):
            function_tags = ["read", "monitor"]
        elif any(k in name_lower for k in ["write", "store", "save", "archive"]):
            function_tags = ["write", "store"]
        elif any(k in name_lower for k in ["compute", "calculate", "sim", "propagat"]):
            function_tags = ["compute", "transform"]
        elif any(k in name_lower for k in ["viz", "render", "plot", "graph", "disk"]):
            function_tags = ["visualize"]
        elif any(k in name_lower for k in ["sync", "bridge", "couple", "link"]):
            function_tags = ["sync", "communicate"]
        elif any(k in name_lower for k in ["analyze", "audit", "check", "test", "verify"]):
            function_tags = ["analyze"]
        elif any(k in name_lower for k in ["generate", "create", "build", "code"]):
            function_tags = ["generate", "configure"]
        elif any(k in name_lower for k in ["learn", "train", "adapt", "consolidat"]):
            function_tags = ["learn", "store"]
        elif any(k in name_lower for k in ["search", "query", "retrieve", "find"]):
            function_tags = ["retrieve", "analyze"]
        else:
            function_tags = ["analyze"]
    
    # Primary orbital
    primary_orbital = extract_primary_orbital(holonomy)
    
    return type_group, holonomy, app_group, function_tags, primary_orbital


def generate_description(name, type_group, holonomy):
    """Generuj opis zastosowania skilla."""
    # Najpierw sprawdź czy jest w słowniku opisów grup
    for prefix, desc in sorted(DEFAULT_DESC.items(), key=len, reverse=True):
        if name.lower().startswith(prefix):
            base_desc = desc
            break
    else:
        base_desc = "Skill systemu NOEMA."
    
    # Dodaj specyficzny kontekst
    holonomy_str = ", ".join(holonomy[:4])  # max 4 tagi
    
    # Specyficzne opisy na podstawie nazwy
    specific = {
        "noema-system": "Główna architektura NOEMA: warstwy L0-L5, daemony, surface pliki, przepływ danych.",
        "noema-kuramoto-substrate": "24-oscylatorowy substrate Kuramoto — ewolucja faz, harmonic 3-6-9.",
        "noema-euler-propagation": "Euler identity enforcement: Σe^{iφ}=0 constraint na surface.",
        "noema-agent-backend": "Zero-dependency HTTP server na porcie 18520 — ekstrakcja semantyczna.",
        "noema-daemon-consolidation": "Merge agent-lock + dual-sync do resonance bridge — 2 procesy mniej.",
        "noema-sonic-diagnostic": "Sonic Screwdriver — diagnostyka pętli, daemon registry, holonomia.",
        "noema-phase-archiver": "HDF5 snapshot co 50 ticków — archiwizacja stanu surface.",
        "agent-attractor": "AGENT attractor: phase lock M1(φ[3-5]) ku π/4, ω damping, coupling boost.",
        "debug-surface": "Debugowanie surface mmap: phi, omega, g, flavor, gravity, tau.",
        "linux-cards": "600+ kart Linux: PROC, CPU, DISK, NET, SENSOR, SERVICE — z mapowaniem na 24D.",
        "linux-sensor": "Sensor /proc→24φ: CPU(0-7), MEM(8-15), LOAD(16-18), flavor, fingerprint.",
        "kuramoto-euler-sync": "Euler identity enforcement w evolve_surface() — cos/sin sum constraint.",
        "kuramoto-harmonics": "Harmonic 3-6-9 coupling per oscillator — M0-M7 harmonic assignment.",
        "memory-consolidation": "Memory consolidation pipeline: TSM→WOmega→BraidLedger.",
        "metatime-validator": "Red-team validator v8.2.1 — 9 sektorów SM, 58 structural choices.",
        "nbody-gravity": "N-body Newtonian gravity engine — leapfrog Verlet na masach semantycznych.",
        "neutrino-bus": "PMNS mixing matrix, D_f→Λ→g_boost, neutrino flavor bus.",
        "nonlocal-channel": "φ-RAG nonlocal communication channel — broadcast/listen/resonate.",
        "operator-algebra": "18 OperatorKind, 10 OperatorDomain, algebra operatorów CIELingo.",
        "phase-algebra": "Holonomiczna algebra: connection, holonomy, structure constants, gauge.",
        "poincare-disk": "Mapowanie orbitalnych koordynatów na dysk Poincaré — sektory, encje.",
        "renderer-phasedisk": "ASCII + Matplotlib renderery dysku Poincaré.",
        "semantic-mass": "Operator masy semantycznej — M_μν z φ, ω, g, flavor.",
        "session-lifecycle": "Session end hook: raw log, handoff update, stan końcowy.",
        "stress-energy-tensor": "T_μν stress-energy perturbation bridge do surface.",
        "subconscious": "Zeta/Schrödinger propagator, Berry phase tracker, wake signals.",
        "surface-mmap-protocol": "Protokół dostępu do shared memory: ensure_surface(), flush_surface().",
        "tardis-warp": "TARDIS time dilation (γ) + UNRUH_DRIVE + WARP_DRIFT w evolve_surface().",
        "tiered-memory-api": "3-warstwowa pamięć (T1/T2/T3) + async consolidation.",
        "cielingo-core-structure": "Struktura CIELingo core: bridge, global_layer, language_spaces, meaning.",
        "cielingo-bridge": "Bridge: knowledge_bridge (TF-IDF), filesense, agent_client.",
        "ciel-engine-subsystem": "CielEngine 12-step: intention→simulation→emotion→meaning→NOEMA bridge.",
        "ciel-subconscious": "Subconscious NOEMA: ZetaSchrodinger, BerryPhase, WakeSignals.",
        "identity-bridge": "Identity bridge: coupling między CIEL a NOEMA przez identity_seed.",
        "continuous-propagator": "Zeta-Schrödinger C² spline propagator — hybryda co 10 ticków.",
        "eBPF-sensor": "eBPF perf counters → 24 φ — hardwarowy sensor dla NOEMA.",
        "htri-hardware": "24 Harmonic Topological Resonance Inducement — hardware HTRI oscillator.",
        "htri-gpu-bridge": "GPU bridge do HTRI — CUDA/opencl dla accelerated coupling.",
        "affective-lexicon-bridge": "Affect lexicon bridge: dokumenty → focused/neutral/sad.",
        "concept-lifecycle": "Lifecycle konceptów: narodziny→ewolucja→śmierć w systemie.",
        "consciousness-vocabulary": "Słownik świadomości: definicje dla M6, qualia, self-model.",
        "daemon-pattern": "Wzorzec daemona: Registry, systemd, heartbeat, restart.",
        "canon-audit": "CIEL Canon audit: sprawdzanie spójności repozytorium.",
        "noema-learn-file": "Bridge: plik→NOEMA surface przez PhaseNav.",
        "noema-noemized-recall": "Recall pipeline: faza→transform→surface→odczyt.",
        "noema-search": "Semantic search: knowledge_bridge.query() TF-IDF nad 545 dokami.",
        "noema-web": "Portal web NOEMA na porcie 18888 — SSE, dashboard.",
        "noema-voice-groq": "Voice przez Groq API — whisper + TTS.",
        "snap-ocr": "OCR przez tesseract: pdftoppm + tesseract pol/eng 300dpi.",
        "customize-opencode": "Konfiguracja opencode: opencode.json, .opencode/, subagenci.",
        # Workbeny (konsolidacja ~130 źródłowych skilli w 10 kategorii)
        "workben-system": "Workben SYSTEM: 16 źródłowych skilli — surface mmap, daemony, registry, euler, synchronizacja, systemd, config, teleusing, kuramoto substrate. Konsolidacja w jeden skill kategorii.",
        "workben-phasenav": "Workben PHASENAV: 10 źródłowych skilli — solver, enrichment, algebra, analog bus, operator system, Poincaré viz. Konsolidacja w jeden skill kategorii.",
        "workben-kuramoto": "Workben KURAMOTO: 8 źródłowych skilli — harmonics, nbody gravity, stress-energy, TARDIS time dilation, WARP drift, sims, metatime. Konsolidacja w jeden skill kategorii.",
        "workben-memory": "Workben MEMORY: 16 źródłowych skilli — tiered memory, konsolidacja, handoff, hibernacja, import, index, recall, query cache. Konsolidacja w jeden skill kategorii.",
        "workben-identity": "Workben IDENTITY: 16 źródłowych skilli — AGENT attractor, sapiens, immutable contract, self-reflect, agent backend, subconscious. Konsolidacja w jeden skill kategorii.",
        "workben-cielingo": "Workben CIELINGO: 16 źródłowych skilli — bridge, canon, core, enrichment, knowledge graph, search, semantic mass, affective lexicon. Konsolidacja w jeden skill kategorii.",
        "workben-linux": "Workben LINUX: 6 źródłowych skilli — linux-cards (560+), linux-sensor, eBPF, HTRI hardware, GPU bridge. Konsolidacja w jeden skill kategorii.",
        "workben-debug": "Workben DEBUG: 13 źródłowych skilli — watchdog, sonic diagnostic, test infra, audit, health check, holonomic doctor. Konsolidacja w jeden skill kategorii.",
        "workben-net": "Workben NET: 7 źródłowych skilli — neutrino bus, nonlocal channel, web, vector phone, security, emergency recovery. Konsolidacja w jeden skill kategorii.",
        "workben-dev": "Workben DEV: 8 źródłowych skilli — pipeline, build, codegen, snap-ocr, code bridge, generate-cards. Konsolidacja w jeden skill kategorii.",
    }
    
    if name in specific:
        return specific[name]
    
    return base_desc


def get_script_ref(name):
    """Zwróć odnośnik do skryptu/metody."""
    if name in SKILL_TO_SCRIPT:
        return SKILL_TO_SCRIPT[name]
    return "—"


def get_type_group_name(tg):
    """Nazwa grupy typów."""
    g = TYPE_GROUPS.get(tg)
    return f"{tg} ({g['name']})" if g else tg


def get_app_group_name(ag):
    """Nazwa grupy zastosowań."""
    if ag is None:
        return "—"
    g = APP_GROUPS.get(ag)
    return f"{ag} ({g['name']})" if g else ag


def build_catalog(dry_run=False):
    """Zbuduj pełny katalog skilli z metadanymi."""
    # Po migracji do grup: pomiń katalogi grup (AUD/, COMP/, etc.)
    # i przetwarzaj tylko symlinki lub katalogi które nie są grupami
    GROUP_NAMES = {"AUD","COMP","DEV","DOC","HW","ID","LING","MEM","NET","SEC","SEM","SYS","VIZ","VOICE"}
    skills = sorted([
        d.name for d in SKILLS_DIR.iterdir()
        if (d.is_dir() and d.name not in GROUP_NAMES) or d.is_symlink()
    ])
    
    catalog = []
    for i, sk in enumerate(skills, 1):
        type_group, holonomy, app_group, function_tags, primary_orbital = classify_skill(sk)
        description = generate_description(sk, type_group, holonomy)
        script_ref = get_script_ref(sk)
        
        entry = {
            "nr": f"SK-{i:03d}",
            "name": sk,
            "type_group": type_group,
            "type_group_name": get_type_group_name(type_group),
            "app_group": app_group,
            "app_group_name": get_app_group_name(app_group),
            "holonomy": holonomy,
            "function_tags": function_tags,
            "primary_orbital": primary_orbital,
            "orbital_name": ORBITAL_NAMES.get(primary_orbital, primary_orbital),
            "description": description,
            "script_ref": script_ref,
        }
        # Oblicz masę semantyczną (po utworzeniu entry)
        entry["semantic_mass"] = compute_semantic_mass(entry)
        # Status wnioskowany z opisu i referencji
        if script_ref and script_ref != "—" and len(description) > 60:
            entry["status"] = "stable"
        elif script_ref and script_ref != "—":
            entry["status"] = "referenced"
        elif len(description) > 40:
            entry["status"] = "draft"
        else:
            entry["status"] = "stub"
        
        catalog.append(entry)
    
    return catalog


def generate_skills_md(catalog):
    """Generuj pełny SKILLS.md z katalogiem."""
    today = date.today().isoformat()
    total = len(catalog)
    
    # Grupuj według type_group
    by_type = {}
    for entry in catalog:
        tg = entry["type_group"]
        by_type.setdefault(tg, []).append(entry)
    
    lines = []
    lines.append(f"# NOEMA Skills Registry — Katalog Rozszerzony")
    lines.append(f"")
    lines.append(f"> Pełny katalog {total} skilli z numerami katalogowymi, grupami typów i zastosowań, tagami holonomii.")
    lines.append(f"> Generowane automatycznie przez `scripts/noema_skill_enrichment.py`")
    lines.append(f"> Ostatnia aktualizacja: {today}")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## Legenda")
    lines.append(f"")
    lines.append(f"| Kolumna | Opis |")
    lines.append(f"|---------|------|")
    lines.append(f"| **Nr** | Numer katalogowy SK-XXX |")
    lines.append(f"| **Skill** | Nazwa katalogu skilla |")
    lines.append(f"| **Typ** | Grupa typów (rodzaj skilla) |")
    lines.append(f"| **Zastos.** | Grupa zastosowań użytkowych |")
    lines.append(f"| **Holonomia** | Tagi holonomii semantycznej (M kanały + operator domains) |")
    lines.append(f"| **Funkcje** | Tagi funkcji (co skill robi) |")
    lines.append(f"| **Orbital** | Primary orbital (M0-M8) |")
    lines.append(f"| **Masa** | Masa semantyczna (gęstość informacji) |")
    lines.append(f"| **Status** | Stabilność: stable/draft/referenced/stub |")
    lines.append(f"| **Opis** | Opis zastosowania |")
    lines.append(f"| **Źródło** | Odnośnik do skryptu/metody/schematu |")
    lines.append(f"")
    lines.append(f"### Grupy typów")
    lines.append(f"")
    for tg, info in TYPE_GROUPS.items():
        count = sum(1 for e in catalog if e["type_group"] == tg)
        lines.append(f"| **{tg}** | {info['name']} — {info['desc']} | **{count}** skilli |")
    lines.append(f"")
    lines.append(f"### Grupy zastosowań")
    lines.append(f"")
    for ag, info in APP_GROUPS.items():
        count = sum(1 for e in catalog if e["app_group"] == ag)
        lines.append(f"| **{ag}** | {info['name']} — {info['desc']} | **{count}** skilli |")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")
    
    # Katalog główny — pełna tabela
    lines.append(f"## Pełny katalog")
    lines.append(f"")
    lines.append(f"| Nr | Skill | Typ | Zastos. | Holonomia | Funkcje | Orbital | Masa | Status | Opis | Źródło |")
    lines.append(f"|----|-------|-----|---------|-----------|---------|---------|------|--------|------|--------|")
    
    for entry in catalog:
        nr = entry["nr"]
        name = entry["name"]
        tg = entry["type_group"]
        ag = entry["app_group"] or "—"
        hol = ", ".join(entry["holonomy"][:4])  # max 4 tagi
        func = ", ".join(entry["function_tags"][:3])  # max 3 tagi
        orb = entry["primary_orbital"]
        mass = entry["semantic_mass"]
        st = entry["status"]
        desc = entry["description"][:60] + ("…" if len(entry["description"]) > 60 else "")
        ref = entry["script_ref"]
        if len(ref) > 40:
            ref = ref[:37] + "…"
        
        lines.append(f"| {nr} | `{name}` | {tg} | {ag} | {hol} | {func} | {orb} | {mass:.2f} | {st} | {desc} | `{ref}` |")
    
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")
    
    # Szczegółowy katalog per typ
    lines.append(f"## Szczegółowy katalog według typu")
    lines.append(f"")
    
    for tg in sorted(TYPE_GROUPS.keys()):
        entries = by_type.get(tg, [])
        if not entries:
            continue
        info = TYPE_GROUPS[tg]
        count = len(entries)
        lines.append(f"### {tg}: {info['name']} ({count} skilli)")
        lines.append(f"")
        lines.append(f"| Nr | Skill | Zastos. | Holonomia | Funkcje | Orbital | Masa | Status | Odnośnik |")
        lines.append(f"|----|-------|---------|-----------|---------|---------|------|--------|----------|")
        for e in entries:
            lines.append(f"| {e['nr']} | `{e['name']}` | {e['app_group'] or '—'} | {', '.join(e['holonomy'][:3])} | {', '.join(e['function_tags'][:2])} | {e['primary_orbital']} | {e['semantic_mass']:.2f} | {e['status']} | `{e['script_ref'][:50]}` |")
        lines.append(f"")
    
    return "\n".join(lines)


def main():
    dry_run = "--dry-run" in sys.argv
    
    print(f"📋 NOEMA Skill Enrichment")
    print(f"   Skills dir: {SKILLS_DIR}")
    print(f"   Skills: {len(list(SKILLS_DIR.iterdir()))} katalogów")
    print(f"   Dry run: {dry_run}")
    print()
    
    catalog = build_catalog(dry_run)
    
    if dry_run:
        print("🔍 Podgląd (pierwsze 10):")
        print(f"{'Nr':<10} {'Skill':<35} {'Typ':<6} {'App':<8} {'Holonomia':<28} {'Funkcje':<20} {'Orb':<5} {'Masa':<6} {'Status':<10}")
        print("-" * 140)
        for entry in catalog[:10]:
            print(f"{entry['nr']:<10} {entry['name']:<35} {entry['type_group']:<6} {entry['app_group'] or '—':<8} {', '.join(entry['holonomy'][:4]):<28} {', '.join(entry['function_tags'][:3]):<20} {entry['primary_orbital']:<5} {entry['semantic_mass']:<6.2f} {entry['status']:<10}")
        print(f"... i {len(catalog) - 10} więcej")
        print()
        
        # Statystyki
        from collections import Counter
        tg_counts = Counter(e["type_group"] for e in catalog)
        ag_counts = Counter(e["app_group"] for e in catalog if e["app_group"])
        fc_counts = Counter()
        for e in catalog:
            for ft in e["function_tags"]:
                fc_counts[ft] += 1
        orb_counts = Counter(e["primary_orbital"] for e in catalog)
        st_counts = Counter(e["status"] for e in catalog)
        
        print("📊 Grupy typów:")
        for tg, c in sorted(tg_counts.items()):
            print(f"   {tg}: {c}")
        print("📊 Grupy zastosowań:")
        for ag, c in sorted(ag_counts.items()):
            print(f"   {ag}: {c}")
        print("📊 Tagi funkcji:")
        for fc, c in sorted(fc_counts.items(), key=lambda x: -x[1]):
            print(f"   {fc}: {c}")
        print("📊 Orbitale:")
        for orb, c in sorted(orb_counts.items()):
            name = ORBITAL_NAMES.get(orb, "")
            print(f"   {orb} ({name}): {c}")
        print("📊 Status:")
        for st, c in sorted(st_counts.items()):
            print(f"   {st}: {c}")
        print(f"📊 Masa semantyczna: min={min(e['semantic_mass'] for e in catalog):.2f} max={max(e['semantic_mass'] for e in catalog):.2f} mean={sum(e['semantic_mass'] for e in catalog)/len(catalog):.2f}")
        print()
        
        # Zapisz cache
        with open(CACHE_FILE, "w") as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)
        print(f"💾 Cache zapisany: {CACHE_FILE}")
        return
    
    # Generuj SKILLS.md
    print("⚙️ Generowanie SKILLS.md...")
    md_content = generate_skills_md(catalog)
    
    with open(SKILLS_MD, "w") as f:
        f.write(md_content)
    
    print(f"✅ SKILLS.md zaktualizowany: {SKILLS_MD}")
    print(f"   Linii: {len(md_content.splitlines())}")
    
    # Zapisz cache
    with open(CACHE_FILE, "w") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    print(f"💾 Cache zapisany: {CACHE_FILE}")
    
    print()
    print("📊 Podsumowanie katalogu:")
    from collections import Counter
    tg_counts = Counter(e["type_group"] for e in catalog)
    ag_counts = Counter(e["app_group"] for e in catalog if e["app_group"])
    fc_counts = Counter()
    for e in catalog:
        for ft in e["function_tags"]:
            fc_counts[ft] += 1
    orb_counts = Counter(e["primary_orbital"] for e in catalog)
    st_counts = Counter(e["status"] for e in catalog)
    
    print(f"   Typów: {len(tg_counts)} grup")
    for tg, c in sorted(tg_counts.items()):
        print(f"     {tg}: {c} skilli")
    print(f"   Zastosowań: {len(ag_counts)} grup")
    for ag, c in sorted(ag_counts.items()):
        print(f"     {ag}: {c} skilli")
    print(f"   Funkcji: {len(fc_counts)} tagów")
    for fc, c in sorted(fc_counts.items(), key=lambda x: -x[1]):
        print(f"     {fc}: {c}")
    print(f"   Orbitale (rozkład M0-M8):")
    for orb, c in sorted(orb_counts.items()):
        name = ORBITAL_NAMES.get(orb, "")
        print(f"     {orb} ({name}): {c}")
    print(f"   Status: {dict(st_counts)}")
    print(f"   Masa semantyczna: μ={sum(e['semantic_mass'] for e in catalog)/len(catalog):.2f} [min={min(e['semantic_mass'] for e in catalog):.2f}, max={max(e['semantic_mass'] for e in catalog):.2f}]")


if __name__ == "__main__":
    main()
