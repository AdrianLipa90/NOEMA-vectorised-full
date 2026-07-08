#!/usr/bin/env python3
"""PhaseNav-native repo card generator for CIEL.

It scans src/**/*.py and key JSON artifacts, then writes or refreshes cards
in docs/object_cards/repo/ without changing the underlying scan policy.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

import ast, json, os, sys
from datetime import datetime, timezone
from pathlib import Path

from phasenav_card_language import preserve_note_tail, render_phasenav_block

REPO = Path(__file__).parent.parent
CARDS_DIR = REPO / "docs" / "object_cards" / "repo"
CARDS_DIR.mkdir(parents=True, exist_ok=True)

SCAN_DIRS = [
    REPO / "src" / "ciel_sot_agent",
    REPO / "scripts",
    REPO / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM" / "ciel_omega",
]
SKIP = {"__pycache__", ".venv", "venv", "node_modules"}

KEY_JSONS = [
    REPO / "integration/Orbital/main/manifests/sectors_global.json",
    REPO / "integration/Orbital/main/manifests/couplings_global.json",
    REPO / "integration/reports/orbital_bridge/orbital_bridge_report.json",
    REPO / "integration/reports/ciel_pipeline_report.json",
]


def _extract_py_info(path: Path) -> dict:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/generate_repo_cards.py:34 quiet except scope=_extract_py_info reason=return {}")
        return {}
    classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
    functions = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    docstring = ast.get_docstring(tree) or ""
    return {"classes": classes, "functions": functions[:20], "docstring": docstring[:300]}


def _card_path(src: Path) -> Path:
    rel = src.relative_to(REPO)
    safe = str(rel).replace("/", "_").replace(".py", "").replace(".json", "")
    return CARDS_DIR / f"{safe}.md"


def _write_py_card(src: Path, info: dict) -> None:
    card = _card_path(src)
    rel = src.relative_to(REPO)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    sys.path.insert(0, str(REPO / "src"))
    try:
        from ciel_geometry.phasenav.enrichment import phasenav_enrich
        pn_block = render_phasenav_block(phasenav_enrich(str(rel), src.name))
    except Exception as e:
        print(f"[PhaseNav] enrichment failed for {rel}: {e}", file=sys.stderr)
        pn_block = ""

    existing_note = preserve_note_tail(card.read_text(encoding="utf-8")) if card.exists() else ""
    classes_str = ", ".join(info["classes"]) or "—"
    funcs_str = ", ".join(info["functions"]) or "—"
    content = f"""# {src.name} — {rel}

## Tożsamość
- **ścieżka:** `{rel}`
- **ostatni_indeks:** `{now}`

## Zawartość
- **klasy:** {classes_str}
- **funkcje:** {funcs_str}
{pn_block}
## Opis
{info.get('docstring') or '—'}
{existing_note or ''}"""
    card.write_text(content, encoding="utf-8")


def _write_json_card(src: Path) -> None:
    if not src.exists():
        return
    card = _card_path(src)
    rel = src.relative_to(REPO)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    sys.path.insert(0, str(REPO / "src"))
    try:
        from ciel_geometry.phasenav.enrichment import phasenav_enrich
        pn_block = render_phasenav_block(phasenav_enrich(str(rel), src.name))
    except Exception as e:
        print(f"[PhaseNav] enrichment failed for {rel}: {e}", file=sys.stderr)
        pn_block = ""

    try:
        data = json.loads(src.read_text(encoding="utf-8"))
        keys = list(data.keys())[:15] if isinstance(data, dict) else []
        keys_str = ", ".join(keys)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/generate_repo_cards.py:129 quiet except scope=_write_json_card reason=assign_fallback")
        keys_str = "—"
    content = f"""# {src.name} — {rel}

## Tożsamość
- **ścieżka:** `{rel}`
- **ostatni_indeks:** `{now}`
- **typ:** artefakt JSON

{pn_block}## Klucze najwyższego poziomu
{keys_str}
"""
    card.write_text(content, encoding="utf-8")


def _write_index(cards: list[Path]) -> None:
    idx = CARDS_DIR / "INDEX.md"
    lines = ["# Repo Object Cards — auto-generated\n"]
    for c in sorted(cards):
        lines.append(f"- [{c.stem}](./{c.name})")
    idx.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    cards: list[Path] = []
    count = 0
    for scan_dir in SCAN_DIRS:
        if not scan_dir.exists():
            continue
        for py in scan_dir.rglob("*.py"):
            if any(s in py.parts for s in SKIP):
                continue
            info = _extract_py_info(py)
            _write_py_card(py, info)
            cards.append(_card_path(py))
            count += 1
    for jpath in KEY_JSONS:
        _write_json_card(jpath)
        cards.append(_card_path(jpath))
        count += 1
    _write_index(cards)
    print(f"[generate_repo_cards] {count} kart wygenerowanych → {CARDS_DIR}", file=sys.stderr)


if __name__ == "__main__":
    main()
