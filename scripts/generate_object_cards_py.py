"""Natywny generator kart obiektow PhaseNav dla plikow .py.

For each .py file (filtered by path), the script parses AST, extracts
classes/functions, assigns orbital_level/theta/horizon_class from folder
rules, links the file to the correct attractor sector, and writes or updates
docs/object_cards/repo/<slug>.md.

Usage:
    python scripts/generate_object_cards_py.py [--all] [--path SRC_PATH]
    --all        regenerate every card, not just new or changed files
    --path PATH  process only this specific file (relative to project root)
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import ast
import hashlib
import sys
from datetime import date
from pathlib import Path
from typing import Any

from phasenav_card_language import preserve_note_tail, render_phasenav_block

# ── Project root ───────────────────────────────────────────────────────────────
_ROOT = Path(__file__).parent.parent
_CARDS_DIR = _ROOT / "docs" / "object_cards" / "repo"
_SECTORS_JSON = _ROOT / "integration" / "Orbital" / "main" / "manifests" / "sectors_global.json"

# ── Folder → orbital classification ──────────────────────────────────────────
# (folder_prefix, orbital_level, orbital_type, horizon_class, M_sem_base, attractor_system)
_FOLDER_RULES: list[tuple[str, int, str, str, float, str]] = [
    ("src/ciel_sot_agent",                        1, "F", "TRANSMISSIVE", 0.90, "noema_registry"),
    ("integration/Orbital/main",                  1, "F", "TRANSMISSIVE", 0.90, "orbital_bridge_core"),
    ("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega", 2, "S", "POROUS",       0.80, "ciel_omega_core"),
    ("src/ciel_geometry",                         2, "S", "POROUS",       0.82, "orbital_bridge_core"),
    ("src/ciel_rh_control_mini_repo",             2, "S", "POROUS",       0.79, "orbital_bridge_core"),
    ("scripts",                                   3, "F", "OBSERVATIONAL",0.65, "noema_registry"),
    ("src/ciel-omega-demo-main",                  3, "S", "OBSERVATIONAL",0.60, "ciel_omega_core"),
    ("tests",                                     4, "S", "OBSERVATIONAL",0.40, "sync_core"),
    ("app",                                       4, "S", "OBSERVATIONAL",0.40, "noema_registry"),
]

# ── Subsystem → (theta, phi) from sectors_global ─────────────────────────────
_SUBSYSTEM_THETA: dict[str, tuple[float, float]] = {
    "noema_registry":      (0.10, 0.00),
    "ciel_omega_core":     (0.15, 0.00),
    "orbital_bridge_core": (0.20, 0.00),
    "sync_core":           (0.30, 0.00),
    "orch_orbital_core":   (0.35, 0.00),
    "db_orchestrator":     (0.40, 0.00),
}

# ── Attractor → primary attractor label ──────────────────────────────────────
_ATTRACTOR_LABEL = {
    "noema_registry":      "ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry",
    "orbital_bridge_core": "ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core",
    "ciel_omega_core":     "ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core",
    "sync_core":           "orbital_bridge_core → ent_Mr_Ciel_Apocalyptos",
    "db_orchestrator":     "orbital_bridge_core → TSM memory",
}


def _folder_class(rel_path: str) -> tuple[int, str, str, float, str]:
    """Return (orbital_level, orbital_type, horizon_class, M_sem, attractor) for a path."""
    for prefix, lv, ot, hc, ms, att in _FOLDER_RULES:
        if rel_path.startswith(prefix):
            return lv, ot, hc, ms, att
    return 4, "S", "OBSERVATIONAL", 0.40, "noema_registry"


def _phi_from_path(rel_path: str) -> float:
    """Deterministic phi from path hash (spreads nodes within level)."""
    h = int(hashlib.md5(rel_path.encode()).hexdigest(), 16)
    return round((h % 6283) / 1000.0, 3)  # 0 … 2π


def _parse_py(path: Path) -> dict[str, Any]:
    """Extract module docstring, classes, functions via AST."""
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/generate_object_cards_py.py:80 quiet except scope=_parse_py reason=return {\"docstring\": \"\", \"classes\": [], \"functions\": []}")
        raise
        return {"docstring": "", "classes": [], "functions": []}

    docstring = ast.get_docstring(tree) or ""
    classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
    functions = [
        n.name for n in ast.walk(tree)
        if isinstance(n, ast.FunctionDef) and not n.name.startswith("__")
    ]
    return {
        "docstring": docstring[:400].strip(),
        "classes": classes[:20],
        "functions": functions[:30],
    }


def _slug(rel_path: str) -> str:
    """Convert relative path to card filename slug. Truncate to 240 chars max (ext4 limit = 255)."""
    stem = rel_path.replace("/", "_").replace(".py", "")
    if len(stem) > 240:
        h = hashlib.md5(stem.encode()).hexdigest()[:8]
        stem = stem[:232] + "_" + h
    return stem + ".md"


def _card_path(rel_path: str) -> Path:
    return _CARDS_DIR / _slug(rel_path)


def _card_id(rel_path: str) -> str:
    stem = Path(rel_path).stem.upper().replace("-", "_")[:20]
    h = hashlib.md5(rel_path.encode()).hexdigest()[:4].upper()
    return f"REPO-{stem}-{h}"


def build_card(rel_path: str, parsed: dict[str, Any], force: bool = False) -> str:
    """Build markdown card content for a .py file in native PhaseNav format."""
    lv, ot, hc, ms, att = _folder_class(rel_path)
    theta_info = _SUBSYSTEM_THETA.get(att, (0.785 * lv / 2, 0.0))
    theta = theta_info[0]
    phi = _phi_from_path(rel_path)
    attractor_label = _ATTRACTOR_LABEL.get(att, att)
    filename = Path(rel_path).name
    cid = _card_id(rel_path)
    today = date.today().isoformat()

    doc_first_line = (parsed["docstring"].split("\n")[0] if parsed["docstring"] else "—")
    classes_str = ", ".join(parsed["classes"]) or "—"
    funcs_str = ", ".join(f"`{f}`" for f in parsed["functions"]) or "—"

    sys.path.insert(0, str(_ROOT / "src"))
    try:
        from ciel_geometry.phasenav.enrichment import phasenav_enrich
        pn_block = render_phasenav_block(phasenav_enrich(cid, filename))
    except Exception as e:
        print(f"[PhaseNav] enrichment failed for {cid}: {e}", file=sys.stderr)
        pn_block = ""

    level_names = {1: "CORE", 2: "STRUCTURE", 3: "RELATIONAL", 4: "SATELLITE"}
    level_label = level_names.get(lv, str(lv))

    card = f"""# {filename} — {rel_path}

## Tożsamość
- **id_karty:** `{cid}`
- **ścieżka:** `{rel_path}`
- **ostatni_indeks:** `{today}`
- **poziom_orbitalny:** {lv} ({level_label})
- **typ_orbitalny:** `{ot}`
- **θ (theta):** `{theta:.3f}`
- **φ (phi):** `{phi:.3f}`
- **masa_semantyczna:** `{ms:.2f}`

## Kotwice
- `{rel_path}`

## Atraktor
- **system:** `{att}`
- **główny_atraktor:** {attractor_label}

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | {lv} ({level_label}) |
| typ_orbitalny | {ot} |
| θ | {theta:.3f} |
| φ | {phi:.3f} |
| klasa_horyzontu | **{hc}** |
| masa_semantyczna | {ms:.2f} |

## Relacja horyzontu
`{hc}` — poziom orbitalny {lv}, system `{att}`.

{pn_block}

## Rola
{doc_first_line}

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem {att}*
- **wyjście:** *wywnioskowane z folderu — podsystem {att}*

## Zawartość
- **klasy:** {classes_str}
- **funkcje:** {funcs_str}

## Opis
{parsed['docstring'] or '—'}
"""
    return card


def _should_update(card_path: Path, py_path: Path, force: bool) -> bool:
    if force or not card_path.exists():
        return True
    # Update if .py is newer than card
    return py_path.stat().st_mtime > card_path.stat().st_mtime


def _iter_py_files() -> list[Path]:
    excludes = {".venv", "venv", "site-packages", "__pycache__", ".git", "node_modules"}
    result = []
    for p in _ROOT.rglob("*.py"):
        parts = set(p.parts)
        if parts & excludes:
            continue
        result.append(p)
    return result


def run(force: bool = False, single_path: str | None = None) -> None:
    _CARDS_DIR.mkdir(parents=True, exist_ok=True)

    if single_path:
        targets = [_ROOT / single_path]
    else:
        targets = _iter_py_files()

    created, updated, skipped = 0, 0, 0

    for py_path in targets:
        try:
            rel = py_path.relative_to(_ROOT).as_posix()
        except ValueError:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/generate_object_cards_py.py:241 quiet except scope=run reason=continue")
            raise
            continue

        card_p = _card_path(rel)
        if not _should_update(card_p, py_path, force):
            skipped += 1
            continue

        parsed = _parse_py(py_path)
        content = build_card(rel, parsed, force)

        # Jesli karta juz istnieje, zachowaj dolna sekcje notatek.
        try:
            card_exists = card_p.exists()
        except OSError:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/generate_object_cards_py.py:255 quiet except scope=run reason=no_log_no_raise")
            raise
            skipped += 1
            continue
        if card_exists:
            existing = card_p.read_text(encoding="utf-8")
            note_tail = preserve_note_tail(existing)
            if note_tail:
                content = content.rstrip() + "\n\n" + note_tail.strip() + "\n"
            updated += 1
        else:
            created += 1

        card_p.write_text(content, encoding="utf-8")

    print(f"Object cards: {created} created, {updated} updated, {skipped} skipped (up to date)")
    print(f"Cards directory: {_CARDS_DIR}")


if __name__ == "__main__":
    force_flag = "--all" in sys.argv
    single = None
    for i, arg in enumerate(sys.argv):
        if arg == "--path" and i + 1 < len(sys.argv):
            single = sys.argv[i + 1]
    run(force=force_flag, single_path=single)
