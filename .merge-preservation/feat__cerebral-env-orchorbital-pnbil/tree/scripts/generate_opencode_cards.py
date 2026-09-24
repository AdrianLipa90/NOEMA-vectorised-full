#!/usr/bin/env python3
"""Adapter kart NOEMA dla opencode-noema (TypeScript).

Skany packages/**/*.ts, extractuje: classes, functions, types, interfaces,
exports, keywords z importów. Liczy M_sem tym samym wzorem co
generate_object_cards_py.py. PhaseNav enrichment z ciel_geometry.

Użycie:
    python3 scripts/generate_opencode_cards.py [--all] [--path PKG]
    --all      regeneruj wszystkie
    --path PKG tylko ten package (np. packages/opencode)
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

import hashlib
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

_ROOT = Path("/media/adrian/NOEMA_SANDBOX/opencode-noema")
_OUT  = Path("/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/docs/object_cards/opencode")
_OUT.mkdir(parents=True, exist_ok=True)

# ── Folder → orbital classification (adapted for opencode structure) ──────────
_FOLDER_RULES: list[tuple[str, int, str, str, float, str]] = [
    ("packages/opencode/src",    1, "F", "TRANSMISSIVE", 0.90, "opencode_core"),
    ("packages/core/src",        1, "F", "TRANSMISSIVE", 0.88, "opencode_core"),
    ("packages/server/src",      2, "S", "POROUS",       0.82, "opencode_runtime"),
    ("packages/plugin/src",      2, "S", "POROUS",       0.80, "opencode_plugin"),
    ("packages/app/src",         2, "S", "POROUS",       0.78, "opencode_app"),
    ("packages/protocol/src",    2, "S", "POROUS",       0.76, "opencode_protocol"),
    ("packages/llm/src",         2, "S", "POROUS",       0.85, "opencode_llm"),
    ("packages/schema/src",      3, "F", "OBSERVATIONAL",0.65, "opencode_schema"),
    ("packages/sdk/src",         3, "S", "OBSERVATIONAL",0.60, "opencode_sdk"),
    ("packages/cli/src",         3, "S", "OBSERVATIONAL",0.55, "opencode_cli"),
    ("packages/tui/src",         3, "S", "OBSERVATIONAL",0.50, "opencode_tui"),
    ("packages/ui/src",          3, "S", "OBSERVATIONAL",0.55, "opencode_ui"),
    ("packages/console/src",     3, "S", "OBSERVATIONAL",0.50, "opencode_console"),
    ("packages/desktop/src",     3, "S", "OBSERVATIONAL",0.52, "opencode_desktop"),
    ("packages/web",             4, "S", "OBSERVATIONAL",0.40, "opencode_web"),
    ("packages/stats/src",       4, "S", "OBSERVATIONAL",0.42, "opencode_stats"),
    ("packages/storybook/src",   4, "S", "OBSERVATIONAL",0.35, "opencode_storybook"),
    ("packages/http-recorder/src",4,"S", "OBSERVATIONAL",0.38, "opencode_http"),
    ("packages/codemode/src",    4, "S", "OBSERVATIONAL",0.35, "opencode_codemode"),
    ("packages/session-ui/src",  3, "S", "OBSERVATIONAL",0.48, "opencode_session"),
    ("packages/effect-drizzle-sqlite/src", 3, "S", "OBSERVATIONAL", 0.45, "opencode_db"),
    ("packages/effect-sqlite-node/src",    3, "S", "OBSERVATIONAL", 0.45, "opencode_db"),
    ("packages/containers/src",  3, "S", "OBSERVATIONAL",0.43, "opencode_containers"),
    ("packages/enterprise/src",  3, "S", "OBSERVATIONAL",0.40, "opencode_enterprise"),
    ("packages/function/src",    3, "S", "OBSERVATIONAL",0.42, "opencode_function"),
    ("packages/httpapi-codegen/src", 4, "S", "OBSERVATIONAL",0.35, "opencode_codegen"),
    ("packages/opencode/script", 4, "F", "OBSERVATIONAL",0.30, "opencode_tooling"),
    ("packages/opencode/test",   4, "S", "SEALED",      0.25, "opencode_test"),
]

_SUBSYSTEM_THETA: dict[str, tuple[float, float]] = {
    "opencode_core":     (0.10, 0.00),
    "opencode_runtime":  (0.15, 0.00),
    "opencode_plugin":   (0.18, 0.00),
    "opencode_app":      (0.20, 0.00),
    "opencode_protocol": (0.22, 0.00),
    "opencode_llm":      (0.12, 0.00),
    "opencode_schema":   (0.25, 0.00),
    "opencode_sdk":      (0.28, 0.00),
    "opencode_cli":      (0.30, 0.00),
    "opencode_tui":      (0.32, 0.00),
    "opencode_ui":       (0.34, 0.00),
    "opencode_console":  (0.36, 0.00),
    "opencode_desktop":  (0.38, 0.00),
    "opencode_web":      (0.40, 0.00),
    "opencode_stats":    (0.42, 0.00),
    "opencode_tooling":  (0.50, 0.00),
    "opencode_test":     (0.60, 0.00),
    "opencode_http":     (0.44, 0.00),
    "opencode_codemode": (0.46, 0.00),
    "opencode_session":  (0.35, 0.00),
    "opencode_db":       (0.37, 0.00),
    "opencode_containers": (0.39, 0.00),
    "opencode_enterprise": (0.41, 0.00),
    "opencode_function":   (0.43, 0.00),
    "opencode_codegen":    (0.48, 0.00),
}

# ── M_sem weights (same as generate_object_cards_py.py) ──────────────────────
_ALPHA = 0.30
_BETA  = 0.25
_CHI   = 0.20
_DELTA = 0.15
_EPS   = 0.10

# ── TS extraction (regex, no tree-sitter) ─────────────────────────────────────

_RE_CLASS    = re.compile(r'\b(?:export\s+)?(?:abstract\s+)?class\s+(\w+)', re.MULTILINE)
_RE_FUNCTION = re.compile(r'\b(?:export\s+)?(?:async\s+)?function\s+(\w+)', re.MULTILINE)
_RE_TYPE     = re.compile(r'\b(?:export\s+)?type\s+(\w+)', re.MULTILINE)
_RE_INTERFACE= re.compile(r'\b(?:export\s+)?interface\s+(\w+)', re.MULTILINE)
_RE_CONST    = re.compile(r'\b(?:export\s+)?const\s+(\w+)\s*[=:]', re.MULTILINE)
_RE_IMPORT   = re.compile(r'''(?:import|from)\s+[\s\S]*?['"]([^'"]+)['"]''', re.MULTILINE)
_RE_KEYWORDS = re.compile(r'\b(config|plugin|server|client|handler|middleware|route|schema|validator|transform|encode|decode|parse|serialize|deserialize|connect|disconnect|subscribe|publish|emit|on|off|create|destroy|init|start|stop|open|close|read|write|send|receive|fetch|store|cache|validate|authenticate|authorize|encrypt|decrypt|hash|sign|verify|compress|decompress|spawn|fork|kill|wait|notify|lock|unlock|acquire|release)\b', re.IGNORECASE)

def _extract_ts(path: Path) -> dict[str, Any]:
    """Extract classes, functions, types, interfaces, exports, keywords from .ts."""
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return {"classes": [], "functions": [], "types": [], "interfaces": [],
                "exports": [], "keywords": [], "docstring": ""}

    classes     = list(set(_RE_CLASS.findall(src)))
    functions   = list(set(_RE_FUNCTION.findall(src)))
    types       = list(set(_RE_TYPE.findall(src)))
    interfaces  = list(set(_RE_INTERFACE.findall(src)))
    consts      = list(set(_RE_CONST.findall(src)))
    imports     = list(set(_RE_IMPORT.findall(src)))
    keywords    = list(set(_RE_KEYWORDS.findall(src)))

    # Docstring: first JSDoc block or first comment
    docstring = ""
    jsdoc = re.search(r'/\*\*\s*(.*?)\s*\*/', src, re.DOTALL)
    if jsdoc:
        docstring = re.sub(r'\n\s*\*\s*', ' ', jsdoc.group(1)).strip()[:400]
    elif src.startswith("//"):
        docstring = src.split("\n")[0][:200]

    return {
        "classes": classes[:20],
        "functions": functions[:30],
        "types": types[:20],
        "interfaces": interfaces[:15],
        "exports": consts[:15],
        "keywords": keywords[:20],
        "imports": imports[:15],
        "docstring": docstring,
    }


def _folder_class(rel_path: str) -> tuple[int, str, str, float, str]:
    for prefix, lv, ot, hc, ms, att in _FOLDER_RULES:
        if rel_path.startswith(prefix):
            return lv, ot, hc, ms, att
    return 4, "S", "OBSERVATIONAL", 0.40, "opencode_tooling"


def _phi_from_path(rel_path: str) -> float:
    h = int(hashlib.md5(rel_path.encode()).hexdigest(), 16)
    return round((h % 6283) / 1000.0, 3)


def _slug(rel_path: str) -> str:
    stem = rel_path.replace("/", "_").replace(".ts", "")
    if len(stem) > 240:
        h = hashlib.md5(stem.encode()).hexdigest()[:8]
        stem = stem[:232] + "_" + h
    return stem + ".md"


def _card_id(rel_path: str) -> str:
    stem = Path(rel_path).stem.upper().replace("-", "_")[:20]
    h = hashlib.md5(rel_path.encode()).hexdigest()[:4].upper()
    return f"OC-{stem}-{h}"


# ── Collatz helper ────────────────────────────────────────────────────────────

def _collatz_steps(n: int) -> int:
    if n <= 1:
        return 0
    steps = 0
    while n != 1 and steps < 1000:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps


# ── Card builder ──────────────────────────────────────────────────────────────

def build_card(rel_path: str, parsed: dict[str, Any]) -> str:
    lv, ot, hc, ms_base, att = _folder_class(rel_path)
    theta_info = _SUBSYSTEM_THETA.get(att, (0.785 * lv / 2, 0.0))
    theta = theta_info[0]
    phi = _phi_from_path(rel_path)
    filename = Path(rel_path).name
    cid = _card_id(rel_path)
    today = date.today().isoformat()

    # M_sem from content complexity
    n_classes    = len(parsed["classes"])
    n_functions  = len(parsed["functions"])
    n_types      = len(parsed["types"])
    n_interfaces = len(parsed["interfaces"])
    n_exports    = len(parsed["exports"])
    n_keywords   = len(parsed["keywords"])

    # Euler-Collatz: complexity weight
    total_entities = n_classes + n_functions + n_types + n_interfaces
    M_EC = min(1.0, math.log1p(total_entities) / math.log1p(50))

    # Zeta-Schrödinger: keyword resonance
    M_ZS = min(1.0, n_keywords / 15.0) if n_keywords > 0 else 0.3

    # C_dep: export density (how much is exposed)
    C_dep = min(1.0, n_exports / 10.0) if n_exports > 0 else 0.4

    # C_prov: type/interface density (structural richness)
    C_prov = min(1.0, (n_types + n_interfaces) / 10.0) if (n_types + n_interfaces) > 0 else 0.5

    # C_exec: docstring presence + class richness
    C_exec = 0.8 if parsed["docstring"] else 0.4
    C_exec = min(1.0, C_exec + n_classes * 0.1)

    M_sem = _ALPHA * M_EC + _BETA * M_ZS + _CHI * C_dep + _DELTA * C_prov + _EPS * C_exec
    M_sem = round(min(1.0, max(0.1, M_sem * ms_base)), 5)

    # PhaseNav enrichment
    sys.path.insert(0, str(Path("/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/src")))
    try:
        from ciel_geometry.phasenav.enrichment import phasenav_enrich
        pn = phasenav_enrich(cid, filename)
        R = pn["harmonic_imprint"]
        phasenav_block = (
            f"\n## PhaseNav\n"
            f"- **operator:** `{pn['operator_id']}`\n"
            f"- **harmonic fingerprint:** `{pn['harmonic_fingerprint']}`\n"
            f"- **R₁:** `{R['R_1']}` R₃: `{R['R_3']}` R₆: `{R['R_6']}` R₉: `{R['R_9']}`\n"
            f"- **κ_potential:** `{pn['kappa_potential']}`\n"
            f"- **M_op:** `{pn['semantic_mass']}`\n"
            f"- **24D:** `{' '.join(f'{x:.3f}' for x in pn['operator_vector_24d'][:6])}...`\n"
        )
    except Exception as e:
        print(f"[PhaseNav] fail {cid}: {e}", file=sys.stderr)
        phasenav_block = ""

    classes_str    = ", ".join(parsed["classes"]) or "—"
    funcs_str      = ", ".join(f"`{f}`" for f in parsed["functions"]) or "—"
    types_str      = ", ".join(f"`{t}`" for t in parsed["types"]) or "—"
    interfaces_str = ", ".join(f"`{i}`" for i in parsed["interfaces"]) or "—"
    exports_str    = ", ".join(f"`{e}`" for e in parsed["exports"]) or "—"
    keywords_str   = ", ".join(parsed["keywords"][:12]) or "—"
    imports_str    = ", ".join(f"`{i}`" for i in parsed["imports"][:8]) or "—"

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
- **masa_semantyczna:** `{M_sem}`

## Kotwice
- `{rel_path}`

## Atraktor
- **system:** `{att}`

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | {lv} ({level_label}) |
| typ_orbitalny | `{ot}` |
| θ | `{theta:.3f}` |
| φ | `{phi:.3f}` |
| klasa_horyzontu | **{hc}** |
| masa_semantyczna | `{M_sem}` |
| M_EC (complexity) | `{M_EC:.4f}` |
| M_ZS (keywords) | `{M_ZS:.4f}` |
| C_dep (exports) | `{C_dep:.4f}` |
| C_prov (types) | `{C_prov:.4f}` |
| C_exec (docstring+classes) | `{C_exec:.4f}` |

## Zawartość
- **klasy:** {classes_str}
- **funkcje:** {funcs_str}
- **typy:** {types_str}
- **interfejsy:** {interfaces_str}
- **eksporty:** {exports_str}

## Słowa kluczowe
{keywords_str}

## Importy
{imports_str}

{phasenav_block}

## Opis
{parsed['docstring'] or '—'}
"""
    return card


# ── Scanner ───────────────────────────────────────────────────────────────────

def scan_package(pkg_path: Path, force: bool = False) -> dict[str, int]:
    excludes = {"node_modules", "__pycache__", ".git", "dist", "build", ".next", "coverage"}
    created, updated, skipped = 0, 0, 0

    for ts in pkg_path.rglob("*.ts"):
        parts = set(ts.parts)
        if parts & excludes:
            continue
        if ".test.ts" in ts.name or ".spec.ts" in ts.name:
            continue

        try:
            rel = ts.relative_to(_ROOT).as_posix()
        except ValueError:
            continue

        card_path = _OUT / _slug(rel)
        if not force and card_path.exists():
            if ts.stat().st_mtime <= card_path.stat().st_mtime:
                skipped += 1
                continue

        parsed = _extract_ts(ts)
        total = (len(parsed["classes"]) + len(parsed["functions"]) +
                 len(parsed["types"]) + len(parsed["interfaces"]))
        if total == 0 and not parsed["docstring"]:
            skipped += 1
            continue

        content = build_card(rel, parsed)
        card_path.write_text(content, encoding="utf-8")
        if card_path.stat().st_size > 100:
            created += 1
        else:
            skipped += 1

    return {"created": created, "updated": updated, "skipped": skipped}


def _write_index(all_cards: list[Path]) -> None:
    idx = _OUT / "INDEX.md"
    lines = [
        "# OpenCode-NOEMA Object Cards — Index",
        f"*Generated: {date.today().isoformat()}*",
        f"*Total: {len(all_cards)}*",
        "",
    ]
    by_pkg: dict[str, list[Path]] = {}
    for c in sorted(set(all_cards)):
        # Extract package name from slug: packages_{pkg}_...
        parts = c.stem.split("_")
        pkg = parts[1] if len(parts) > 1 and parts[0] == "packages" else "other"
        by_pkg.setdefault(pkg, []).append(c)

    for pkg, cards in sorted(by_pkg.items()):
        lines.append(f"## {pkg} ({len(cards)})")
        for c in cards[:40]:
            lines.append(f"- [{c.stem}](./{c.name})")
        if len(cards) > 40:
            lines.append(f"- *...{len(cards)-40} more*")
        lines.append("")

    idx.write_text("\n".join(lines), encoding="utf-8")


# ── Main ──────────────────────────────────────────────────────────────────────

import math

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--path", type=str, default=None)
    args = parser.parse_args()

    force = args.all
    targets = [_ROOT / args.path] if args.path else sorted(_ROOT.glob("packages/*"))

    total_created = 0
    all_cards = []

    for pkg in targets:
        if not pkg.is_dir():
            continue
        print(f"  Scanning {pkg.name}...", end=" ", flush=True)
        result = scan_package(pkg, force=force)
        total_created += result["created"]
        print(f"{result['created']} created, {result['skipped']} skipped")
        all_cards.extend(_OUT.rglob("*.md"))

    _write_index(all_cards)
    print(f"\nTotal: {total_created} cards → {_OUT}")
