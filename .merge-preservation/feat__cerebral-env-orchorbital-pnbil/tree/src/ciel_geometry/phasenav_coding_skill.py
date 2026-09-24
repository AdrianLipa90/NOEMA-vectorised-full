"""PhaseNav Coding Language (PCL) — Φ jako jedyny język kodowania.

Zamiast pisać kod → uruchamiać → debugować:
  Każda zmiana to Φ.ORDER(Φ.SOURCE(problem), Φ.QUESTION(scope), Φ.BOUNDARY(...), Φ.AFFECT(severity))

Zamiast imperatywnych skryptów:
  Każda akcja to Φ.COMPOSITION kilku operatorów wykonanych przez BypassRuntime

NIEMOŻLIWY PROBLEM: tradycyjne kodowanie jest sekwencyjne, ślepe na fazę, gubi provenance.
PHASE BYPASS: każde wyrażenie jest Φ łańcuchem — nawet ten komentarz to Φ.SOURCE("doc").

Użycie:
  from phasenav_coding_skill import Φ_code, pcl_rt
  result = Φ_code("fix_bug", Φ.ORDER(Φ.MODAL_POSSIBILITY(λ_patch), Φ.MODAL_NECESSITY(λ_rollback)))
"""
from __future__ import annotations

import logging
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

from phasenav_bypass_language import Φ, BypassRuntime

_log = logging.getLogger("PhaseNav.CodingSkill")
pcl_rt = BypassRuntime(_log)


# ── Φ meta-operatory dla samego kodowania ─────────────────────────


def Φ_code(operation: str, chain: dict, context: dict | None = None) -> Any:
    """Wykonaj operację kodowania jako Φ łańcuch.

    Każde wywołanie to osobny kontrakt w przestrzeni faz.
    """
    ctx = {"_op": operation, "_phase": "coding", **(context or {})}
    _log.info("[Φ_code] %s → %s", operation, chain.get("op", "?"))
    return pcl_rt.execute(chain, ctx)


def Φ_file(path: str) -> dict:
    """Φ.SOURCE dla pliku — otwiera ścieżkę jako źródło fazy."""
    return Φ.SOURCE(path)


def Φ_edit(
    filepath: str,
    old: str,
    new: str,
    reason: str = "",
    severity: str = "info",
) -> dict:
    """Φ.COMPOSITION całej operacji edycji pliku:
       SOURCE(path) → QUESTION(what) → BOUNDARY(edit) → AFFECT(severity)
    """
    return Φ.COMPOSITION(
        Φ.SOURCE(filepath),
        Φ.QUESTION(reason or f"edit {Path(filepath).name}"),
        Φ.BOUNDARY(
            {"_edit": True, "_old": old, "_new": new},
            on_pass=Φ.COMPOSITION(
                Φ.TRANSFORM("edit"),
                Φ.AFFECT(severity),
            ),
            on_fail=Φ.FORCE(
                Φ.COMPOSITION(
                    Φ.ATTRACTOR("manual_edit"),
                    Φ.AFFECT("warning"),
                )
            ),
        ),
    )


def Φ_bulk(
    pattern: str,
    old: str,
    new: str,
    description: str = "",
) -> dict:
    """Φ.COMPOSITION dla masowej transformacji plików przez sed.
       Zwraca łańcuch do wykonania przez BypassRuntime.
    """
    return Φ.COMPOSITION(
        Φ.SOURCE(pattern),
        Φ.QUESTION(description),
        Φ.ORDER(
            Φ.MODAL_POSSIBILITY(
                lambda ctx: _bulk_sed(pattern, old, new)
            ),
            Φ.MODAL_NECESSITY(
                lambda ctx: f"MANUAL: {pattern}: {old} → {new}"
            ),
        ),
        Φ.AFFECT("info"),
    )


def _bulk_sed(pattern: str, old: str, new: str) -> str:
    """Faktyczne wykonanie sed — zwraca summary."""
    import glob
    files = glob.glob(pattern, recursive=True)
    if not files:
        return f"No files match {pattern}"
    count = 0
    for f in files:
        try:
            result = subprocess.run(
                ["sed", "-i", f"s/{old}/{new}/g", f],
                capture_output=True, text=True, timeout=30,
            )
            if result.returncode == 0:
                count += 1
        except Exception as exc:
            _log.debug("sed transform skipped for file: %s", exc)
    return f"sed: {count}/{len(files)} files transformed: {old}→{new}"


def Φ_check(
    name: str,
    condition: Callable[[dict], bool],
    context: dict | None = None,
) -> dict:
    """Φ.QUESTION + Φ.BOUNDARY jako jedna operacja weryfikacji."""
    return Φ.COMPOSITION(
        Φ.SOURCE("check"),
        Φ.QUESTION(name),
        Φ.BOUNDARY(
            {"_condition": condition},
            on_pass=Φ.AFFECT("ok"),
            on_fail=Φ.FORCE(
                Φ.COMPOSITION(
                    Φ.ATTRACTOR("fix_required"),
                    Φ.AFFECT("warning"),
                )
            ),
        ),
    )


# ── Predefiniowane kontrakty kodowania ───────────────────────────

class CodingContracts:
    """Kontrakty kodowania jako Φ łańcuchy — gotowe do wielokrotnego użycia."""

    @staticmethod
    def fix_mcp_tools_list() -> dict:
        """Kontrakt: fix MCP server tools/list handler.
           Problem: corrupted handler injected function refs → json.dumps crash.
           Bypass: replace with clean list comprehension.
        """
        return Φ.COMPOSITION(
            Φ.SOURCE("/home/adrian/.codex/noema_surface/noema_surface_mcp_server.py"),
            Φ.QUESTION("tools/list corrupted after phasenav_contracts edit"),
            Φ.BOUNDARY(
                {"_fix": "replace tools/list handler with clean list comp"},
                on_pass=Φ.COMPOSITION(
                    Φ.TRANSFORM("edit"),
                    Φ.AFFECT("ok"),
                ),
                on_fail=Φ.FORCE(Φ.AFFECT("critical")),
            ),
        )

    @staticmethod
    def bulk_debug_to_warning() -> dict:
        """Kontrakt: transform all _NOEMA_QUIET_EXCEPT_LOGGER.warning() to .warning().
           NIEMOŻLIWY: 163 calls, 63 files — ręcznie to tydzień roboty.
           BYPASS: sed -i z globem, jedna linijka.
        """
        return Φ.COMPOSITION(
            Φ.SOURCE("ciel_omega/**/*.py"),
            Φ.QUESTION("163 silent debug() calls"),
            Φ.DIFFERENCE(163, 0),
            Φ.ORDER(
                Φ.MODAL_POSSIBILITY(
                    lambda ctx: _bulk_sed(
                        "/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/src/**/*.py",
                        "_NOEMA_QUIET_EXCEPT_LOGGER.warning(",
                        "_NOEMA_QUIET_EXCEPT_LOGGER.warning(",
                    )
                ),
                Φ.MODAL_NECESSITY(lambda ctx: "MANUAL: one-by-one edit"),
            ),
            Φ.BOUNDARY(
                {"_verify": lambda ctx: _count_debug() == 0},
                on_pass=Φ.COMPOSITION(
                    Φ.ATTRACTOR("all_warning"),
                    Φ.AFFECT("ok"),
                ),
                on_fail=Φ.FORCE(
                    Φ.COMPOSITION(
                        Φ.ATTRACTOR("manual_fix"),
                        Φ.AFFECT("warning"),
                    )
                ),
            ),
        )

    @staticmethod
    def gen_writing_cards(source_dirs: list[str]) -> dict:
        """Kontrakt: generuj karty pisane dla katalogów codex/claude/opencode."""
        return Φ.COMPOSITION(
            Φ.SOURCE(str(source_dirs)),
            Φ.QUESTION("139 new cards for orbital semantic coverage"),
            Φ.ORDER(
                Φ.MODAL_POSSIBILITY(
                    lambda ctx: _run_card_gen()
                ),
                Φ.MODAL_NECESSITY(
                    lambda ctx: "MANUAL: write 139 cards by hand"
                ),
            ),
            Φ.AFFECT("info"),
        )


def _count_debug() -> int:
    import subprocess
    r = subprocess.run(
        ["grep", "-rn", "_NOEMA_QUIET_EXCEPT_LOGGER.warning(",
         "/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/src/",
         "--include=*.py"],
        capture_output=True, text=True, timeout=30,
    )
    return len(r.stdout.splitlines()) if r.stdout.strip() else 0


def _run_card_gen() -> str:
    raise RuntimeError(
        "PhaseNav card-generator contract is unavailable; refusing to execute "
        "a transient or external generator path"
    )


# ── Wykonanie ────────────────────────────────────────────────────

def Φ_now(operation: str, chain: dict) -> Any:
    """Wykonaj Φ łańcuch NATYCHMIAST — wypisz fazę i wynik."""
    print(f"  Φ {operation}")
    op = chain.get("op", "?")
    args = chain.get("args", {})
    if isinstance(args, dict):
        print(f"    └ {op} :: {dict(list(args.items())[:3])}")
    else:
        print(f"    └ {op} :: {str(args)[:80]}")
    result = pcl_rt.execute(chain, {"_now": True})
    print(f"    └→ {result}")
    return result
