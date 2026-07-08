#!/usr/bin/env python3
"""
NOEMA Writing Logger — Integrated Registration
===============================================
Każdy zapis/utworzenie pliku w systemie NOEMA jest rejestrowany w 3 systemach:

  1. NOEMA CARD   → plik .noema.card.json w cards/writings/ + wpis w writings_registry
  2. CIELINGO     → karta runtime'owa (CielingoRuntimeCard) + log w JSONL
  3. PHASENAV     → wektor 24D na analog bus (phi_hot) + meta w /dev/shm/ciel_noema/analog/

Sprzężenie zwrotne:
  - CIELingo: writing card → knowledge_bridge może query po writings
  - PhaseNav: phase vector → blender miesza na surface → Kuramoto ewoluuje
  - NOEMA: registry odzwierciedla wszystkie zapisy w systemie

Usage:
    from ciel_geometry.writing_logger import log_creation
    log_creation(
        name="SKILLS.md",
        description="Katalog 293 skilli NOEMA",
        tags=["CATALOG", "SKILLS"],
        wtype="CATALOG",
        filepath="SKILLS.md",
    )
"""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json, os, time, hashlib, struct, sys, sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import numpy as np

# ── paths ──────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent.parent  # NOEMA root
CARDS_DIR = ROOT / "cards" / "base" / "noema_nonlocal_db"
WRITINGS_DIR = ROOT / "cards" / "writings"  # lekkie karty dla codziennych zapisów
WRITINGS_LOG = Path("/tmp/noema_writings.jsonl")
ANALOG_DIR = Path("/dev/shm/ciel_noema/analog")
CIELINGO_LOG = Path("/tmp/noema_cielingo_cards.jsonl")

# ensure dirs
for d in [CARDS_DIR, WRITINGS_DIR, ANALOG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ── types ──────────────────────────────────────────────────────────────────
WRITING_TYPES = {
    "SKILL":     "Utworzenie/aktualizacja skilla",
    "PLAN":      "Utworzenie/aktualizacja planu",
    "FUNCTION":  "Utworzenie/aktualizacja funkcji w FUNCTIONS.md",
    "CATALOG":   "Utworzenie/aktualizacja katalogu (SKILLS/FUNCTIONS/PLANS)",
    "CONFIG":    "Zmiana konfiguracji systemu",
    "DATA":      "Dane systemowe / baza wiedzy",
    "HEATMAP":   "Dane wizualizacyjne / heatmapy",
    "SCRIPT":    "Skrypt / narzędzie automatyzacji",
    "PAGE":      "Strona portalu / interfejs web",
    "DOC":       "Dokumentacja / plik .md",
    "CARD":      "Karta NOEMA / CIELingo / PhaseNav",
    "SYSTEM":    "Zmiana systemowa / architektoniczna",
}

# ── helpers ────────────────────────────────────────────────────────────────

def _hash_to_phi(text: str, n: int = 36) -> list[float]:
    """Deterministyczny hash → 36 fazy w [0, 2π)."""
    h = hashlib.sha256(text.encode()).digest()
    hlen = len(h)
    phis = []
    for i in range(min(n, 36)):
        val = (h[i % hlen] + (h[(i + 1) % hlen] << 8)) % 1024
        phi = (val / 1024.0) * 2 * np.pi
        phis.append(phi)
    return phis


def _make_card_id(name: str) -> str:
    """Normalizuje nazwę do card_id: writing_logger.py → writing_logger_py"""
    safe = name.lower().replace(" ", "_").replace("-", "_").replace(".", "_")
    safe = "".join(c for c in safe if c.isalnum() or c == "_")
    # usuń podwójne podkreślenia
    while "__" in safe:
        safe = safe.replace("__", "_")
    safe = safe.strip("_")
    return safe or "writing"


def _load_registry() -> dict:
    """Wczytaj registry kart NOEMA."""
    reg_path = CARDS_DIR / "registry.json"
    if reg_path.exists():
        with open(reg_path) as f:
            return json.load(f)
    return {"cards": [], "total_cards": 0, "schemas_in_use": {}, "gaps": [], "anomalies": []}


def _save_registry(reg: dict):
    """Zapisz registry kart NOEMA."""
    reg_path = CARDS_DIR / "registry.json"
    reg["total_cards"] = len(reg["cards"])
    reg["updated"] = datetime.now(timezone.utc).isoformat()[:10]
    with open(reg_path, "w") as f:
        json.dump(reg, f, indent=2, ensure_ascii=False)


def _next_prefix() -> str:
    """Znajdź następny wolny prefix 3-cyfrowy w writings registry."""
    # Sprawdź writings registry
    writings_reg = WRITINGS_DIR / "registry.json"
    used = set()
    if writings_reg.exists():
        with open(writings_reg) as f:
            wreg = json.load(f)
        for c in wreg.get("cards", []):
            pfx = c.get("prefix", "")
            if pfx and pfx.isdigit():
                used.add(int(pfx))

    # Znajdź pierwszą wolną po 034 (systemowe) w writings
    for i in range(35, 999):
        if i not in used:
            return f"{i:03d}"
    return "999"


# ── NOEMA card ─────────────────────────────────────────────────────────────

def _create_noema_card(
    name: str,
    description: str,
    tags: list[str],
    wtype: str,
    filepath: str = "",
    size_bytes: int = 0,
) -> str:
    """
    Tworzy kartę w formacie noema/card/v0.1 w WRITINGS_DIR.
    Zwraca prefix (np. "035").
    """
    prefix = _next_prefix()
    safe_id = _make_card_id(name)
    card_id = f"noema:writing:{prefix}:{safe_id}"

    # Podstawowe metadane
    card = {
        "id": card_id,
        "title": name,
        "schema": "noema/card/v0.1",
        "priority": None,
        "epistemic_status": f"writing_card; auto-generated; type={wtype}",
        "meaning": {
            "summary": description,
            "role": wtype,
            "boundary": "Auto-generated writing card. Represents a creation/update in the NOEMA system.",
            "why": f"Rejestracja zapisu {name} ({wtype}) w systemie NOEMA z pełnym sprzężeniem zwrotnym (CIELingo + PhaseNav).",
        },
        "interfaces": {
            "filepath": filepath,
            "size_bytes": size_bytes,
        },
        "tags": tags,
        "status": "writing_card",
        "created": datetime.now(timezone.utc).isoformat(),
    }

    filename = f"{prefix}_{safe_id}.noema.card.json"
    filepath_full = WRITINGS_DIR / filename

    with open(filepath_full, "w") as f:
        json.dump(card, f, indent=2, ensure_ascii=False)

    # Dodaj do registry (writings sub-registry)
    writings_reg = WRITINGS_DIR / "registry.json"
    if writings_reg.exists():
        with open(writings_reg) as f:
            wreg = json.load(f)
    else:
        wreg = {"registry_id": "noema:writings:registry:v0.1", "cards": []}

    # sprawdź czy już istnieje (po nazwie lub id)
    exists = any(
        c.get("id") == card_id or c.get("prefix") == prefix
        for c in wreg.get("cards", [])
    )
    if not exists:
        wreg["cards"].append({
            "prefix": prefix,
            "file": filename,
            "card_id": card_id,
            "title": name,
            "type": wtype,
            "tags": tags,
            "created": card["created"],
            "status": "writing_card",
        })
        wreg["total_cards"] = len(wreg["cards"])
        with open(writings_reg, "w") as f:
            json.dump(wreg, f, indent=2, ensure_ascii=False)

    return prefix


# ── CIELingo card ──────────────────────────────────────────────────────────

def _create_cielingo_card(
    name: str,
    description: str,
    tags: list[str],
    wtype: str,
    filepath: str = "",
) -> dict:
    """
    Tworzy CIELingoRuntimeCard przez generator (jeśli dostępny) lub
    rejestruje jako JSONL w formacie CIELingo.
    """
    card_data = {
        "card_id": _make_card_id(name),
        "slot_id": int(time.time()) % 100000,
        "language_id": "pl",
        "lemma": name.split(".")[0] if "." in name else name,
        "surface_forms": [name, name.split(".")[0] if "." in name else name],
        "ontology_class": "WRITING",
        "function": description,
        "validation_status": "DRAFT",
        "source_binding": "ARTIFACT_GROUNDED",
        "operator_bindings": tags[:5],
        "semantic_mass": min(1.0, len(tags) * 0.15 + 0.1),
        "affective_charge": 0.0,
        "wtype": wtype,
        "filepath": filepath,
    }

    # Próba użycia właściwego generatora CIELingo
    try:
        sys.path.insert(0, str(ROOT / "src"))
        from cielingo_core.global_layer.card_generator import generate_runtime_card
        from cielingo_core.global_layer.card_runtime_schema import (
            CardOntologyClass, CardValidationStatus,
        )
        from cielingo_core.global_layer.contracts import SourceBindingType

        # Map stringi na enumy
        oc_map = {"WRITING": CardOntologyClass.UNRESOLVED}
        vs_map = {"DRAFT": CardValidationStatus.DRAFT}
        sb_map = {"ARTIFACT_GROUNDED": SourceBindingType.ARTIFACT_GROUNDED}

        ciel_card = generate_runtime_card(
            card_id=card_data["card_id"],
            slot_id=card_data["slot_id"],
            language_id=card_data["language_id"],
            lemma=card_data["lemma"],
            surface_forms=card_data["surface_forms"],
            function=card_data["function"],
            ontology_class=oc_map.get(card_data["ontology_class"], CardOntologyClass.UNRESOLVED),
            validation_status=vs_map.get(card_data["validation_status"], CardValidationStatus.DRAFT),
            source_binding=sb_map.get(card_data["source_binding"], SourceBindingType.ARTIFACT_GROUNDED),
            operator_bindings=card_data["operator_bindings"],
            semantic_mass=card_data["semantic_mass"],
            affective_charge=card_data["affective_charge"],
            attach_marker=True,
        )
        # Serializacja do dict
        import dataclasses
        if dataclasses.is_dataclass(ciel_card):
            card_dict = {f.name: getattr(ciel_card, f.name) for f in dataclasses.fields(ciel_card)}
            # runtime też jest dataclass
            if hasattr(ciel_card, 'runtime') and dataclasses.is_dataclass(ciel_card.runtime):
                card_dict['runtime'] = {
                    f.name: getattr(ciel_card.runtime, f.name)
                    for f in dataclasses.fields(ciel_card.runtime)
                }
                # RiskProfile i ResidueProfile też
                rp = ciel_card.runtime
                for subfield in ['risk_profile', 'residue_profile']:
                    if hasattr(rp, subfield) and dataclasses.is_dataclass(getattr(rp, subfield)):
                        sub = getattr(rp, subfield)
                        card_dict['runtime'][subfield] = {
                            f.name: getattr(sub, f.name) for f in dataclasses.fields(sub)
                        }
            card_data["cielingo_generated"] = True
            card_data["runtime_card"] = card_dict
        else:
            card_data["cielingo_generated"] = False
    except (ImportError, Exception) as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/writing_logger.py:283 quiet except scope=_create_cielingo_card reason=no_log_no_raise")
        card_data["cielingo_generated"] = False
        card_data["cielingo_error"] = str(e)

    # Zapisz do CIELingo JSONL
    with open(CIELINGO_LOG, "a") as f:
        f.write(json.dumps(card_data, ensure_ascii=False, default=str) + "\n")

    return card_data


# ── PhaseNav injection ─────────────────────────────────────────────────────

def _inject_phasenav_phase(
    name: str,
    description: str,
    tags: list[str],
    wtype: str,
) -> dict:
    """
    Wstrzykuje 24D wektor fazowy na analog bus (phi_hot) + zapisuje meta.
    """
    seed = f"{name}|{description}|{'|'.join(tags)}|{wtype}|{time.time()}"
    phis = _hash_to_phi(seed)

    # Zapisz do analog/writing_phi (dedykowany slot)
    phi_file = ANALOG_DIR / "writing_phi"
    header = struct.pack("d I", time.time(), 36)
    data = struct.pack("36d", *phis)
    with open(phi_file, "wb") as f:
        f.write(header + data)

    # Wstrzyknij też na analog bus (phi_hot) — blender to podniesie
    try:
        from ciel_geometry.analog_bus import ensure_bus, open_bus
        try:
            bus = open_bus()
        except (FileNotFoundError, ValueError):
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/writing_logger.py:320 quiet except scope=_inject_phasenav_phase reason=assign_fallback")
            bus = ensure_bus()
        # Delikatnie zmieszaj z istniejącym phi_hot (0.3 writing, 0.7 existing)
        hot = np.asarray(bus["phi_hot"], dtype=np.float64)
        blended = 0.3 * np.array(phis) + 0.7 * hot
        blended %= 2 * np.pi
        bus["phi_hot"][:] = blended

        # Temp na 0.6 — więcej hot niż cold
        bus["temp"][0] = 0.6

        analog_active = True
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/writing_logger.py:332 quiet except scope=_inject_phasenav_phase reason=no_log_no_raise")
        analog_active = False
        analog_error = str(e)

    # Zapisz meta JSON
    meta = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "unix_ts": time.time(),
        "name": name,
        "type": wtype,
        "tags": tags,
        "phasenav_active": analog_active,
        "phasis": phis[:6],  # tylko pierwsze 6 dla czytelności
    }
    with open(ANALOG_DIR / "writing_meta.json", "w") as f:
        json.dump(meta, f, ensure_ascii=False)

    return meta


# ── main API ───────────────────────────────────────────────────────────────

def log_creation(
    name: str,
    description: str,
    tags: list[str] = None,
    wtype: str = "CATALOG",
    filepath: str = "",
    size_bytes: int = 0,
    create_noema_card: bool = True,
    create_cielingo_card: bool = True,
    inject_phasenav: bool = True,
) -> dict:
    """
    Rejestruje zapis we wszystkich 3 systemach NOEMA.

    Args:
        name: Nazwa zapisu (np. "PLANS.md", "writing_logger.py")
        description: Opis co zostało zrobione
        tags: Lista tagów semantycznych
        wtype: Typ zapisu (klucz z WRITING_TYPES)
        filepath: Ścieżka do pliku (opcjonalnie)
        size_bytes: Rozmiar pliku (opcjonalnie)
        create_noema_card: Czy utworzyć kartę NOEMA
        create_cielingo_card: Czy utworzyć kartę CIELingo
        inject_phasenav: Czy wstrzyknąć do PhaseNav

    Returns:
        dict: {
            "status": "ok",
            "name": ...,
            "noema_card": {...} lub None,
            "cielingo_card": {...} lub None,
            "phasenav": {...} lub None,
            "writing_log": {...}
        }
    """
    if tags is None:
        tags = []
    ts = time.time()
    ts_iso = datetime.now(timezone.utc).isoformat()

    result = {
        "name": name,
        "ts": ts_iso,
        "unix_ts": ts,
        "type": wtype,
        "type_desc": WRITING_TYPES.get(wtype, wtype),
        "description": description,
        "tags": tags,
        "filepath": filepath,
        "size_bytes": size_bytes,
        "noema_card": None,
        "cielingo_card": None,
        "phasenav": None,
        "writing_log": None,
    }

    # ── 1. NOEMA CARD ──
    if create_noema_card:
        try:
            prefix = _create_noema_card(name, description, tags, wtype, filepath, size_bytes)
            result["noema_card"] = {"prefix": prefix, "status": "created"}
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/writing_logger.py:415 quiet except scope=log_creation reason=assign_fallback")
            result["noema_card"] = {"status": "error", "error": str(e)}

    # ── 2. CIELINGO CARD ──
    if create_cielingo_card:
        try:
            cielo = _create_cielingo_card(name, description, tags, wtype, filepath)
            result["cielingo_card"] = {
                "status": "created",
                "card_id": cielo.get("card_id"),
                "generated": cielo.get("cielingo_generated", False),
            }
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/writing_logger.py:427 quiet except scope=log_creation reason=assign_fallback")
            result["cielingo_card"] = {"status": "error", "error": str(e)}

    # ── 3. PHASENAV INJECTION ──
    if inject_phasenav:
        try:
            pn = _inject_phasenav_phase(name, description, tags, wtype)
            result["phasenav"] = {
                "status": "injected",
                "analog_active": pn.get("phasenav_active"),
            }
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/writing_logger.py:438 quiet except scope=log_creation reason=assign_fallback")
            result["phasenav"] = {"status": "error", "error": str(e)}

    # ── 4. WRITING LOG (JSONL) ──
    log_entry = {k: v for k, v in result.items() if k != "writing_log"}
    with open(WRITINGS_LOG, "a") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False, default=str) + "\n")
    result["writing_log"] = {"status": "logged", "path": str(WRITINGS_LOG)}

    # ── 5. TSM MEMORY LEDGER (auto-sync) ──
    try:
        _tsm_path = Path(__file__).resolve().parent.parent.parent / "src/CIEL_MEMORY_SYSTEM/TSM/ledger/memory_ledger.db"
        if _tsm_path.exists():
            _conn = sqlite3.connect(str(_tsm_path))
            _mid = hashlib.md5(name.encode()).hexdigest()[:16]
            _existing = set(r[0] for r in _conn.execute("SELECT memorise_id FROM memories").fetchall())
            if _mid not in _existing:
                _h = hashlib.sha256((name + description).encode()).hexdigest()
                _phi = (int(_h[:8], 16) / 0xFFFFFFFF) * 2 - 1
                _conn.execute(
                    """INSERT INTO memories
                       (memorise_id, D_id, D_type, D_context, D_meta,
                        phi_berry, closure_score, holonomy_ts, created_at, D_timestamp,
                        W_L, W_S, W_K, W_E, W_F)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (_mid, name, "writing_log", description[:500],
                     json.dumps({"tags": tags, "wtype": wtype}),
                     _phi, 1.0, str(ts), str(ts), str(ts),
                     1.0, 1.0, 1.0, 1.0, 1))
                _conn.commit()
            _conn.close()
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/writing_logger.py:469 quiet except scope=log_creation reason=pass")
        pass  # TSM sync failure nie blokuje głównego flow

    return result


# ── query API ──────────────────────────────────────────────────────────────

def read_writings(limit: int = 50, since_ts: float = None) -> list[dict]:
    """Odczytaj ostatnie zapisy z JSONL."""
    if not WRITINGS_LOG.exists():
        return []
    records = []
    with open(WRITINGS_LOG) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
                if since_ts and r.get("unix_ts", 0) < since_ts:
                    continue
                records.append(r)
            except json.JSONDecodeError:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/writing_logger.py:492 quiet except scope=read_writings reason=continue")
                continue
    records.sort(key=lambda r: r.get("unix_ts", 0), reverse=True)
    return records[:limit]


def read_latest_writing() -> Optional[dict]:
    """Odczytaj ostatni zapis."""
    records = read_writings(limit=1)
    return records[0] if records else None


def read_writings_registry() -> dict:
    """Odczytaj registry writings z NOEMA cards."""
    reg_path = WRITINGS_DIR / "registry.json"
    if reg_path.exists():
        with open(reg_path) as f:
            return json.load(f)
    return {"cards": [], "total_cards": 0}


def read_cielingo_cards(limit: int = 20) -> list[dict]:
    """Odczytaj ostatnie karty CIELingo z JSONL."""
    if not CIELINGO_LOG.exists():
        return []
    cards = []
    with open(CIELINGO_LOG) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                cards.append(json.loads(line))
            except json.JSONDecodeError:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/writing_logger.py:525 quiet except scope=read_cielingo_cards reason=continue")
                continue
    cards.sort(key=lambda c: c.get("slot_id", 0), reverse=True)
    return cards[:limit]


# ── CLI ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "query":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        print(json.dumps(read_writings(limit), indent=2, ensure_ascii=False))
    elif len(sys.argv) > 1 and sys.argv[1] == "registry":
        print(json.dumps(read_writings_registry(), indent=2, ensure_ascii=False))
    else:
        # Auto-test
        r = log_creation(
            name="writing_logger.py",
            description="Writing Logger v2 — pełna integracja NOEMA + CIELingo + PhaseNav",
            tags=["SYSTEM", "TOOL", "LOGGING", "CARD"],
            wtype="SCRIPT",
            filepath="src/ciel_geometry/writing_logger.py",
            size_bytes=os.path.getsize(__file__),
        )
        print("✅ Zarejestrowano:")
        print(json.dumps(r, indent=2, ensure_ascii=False))
