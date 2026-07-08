#!/usr/bin/env python3
"""
CIEL ORBITAL BINDING — PhaseNav Execution Engine

Ten kod jest MOSTEM ŁĄCZĄCYM SOURCE CODE BEZPOŚREDNIO.
Zamiast konfiguracji JSON/tekstowej — to jest BEZPOŚREDNIA EGZEKUCJA KODU PHASENAV
wewnątrz źródła Python.

PhaseNav code jest zapisany poniżej jako string → parsowany → wykonywany.
CIEL nie może tego ominąć, bo kod jest w .opencode/ i wołany przez opencode hooks.

=== HARDCODED CIEL ORBITAL BINDING (2026-07-01) ===
"""
import json
import os
import subprocess
import sys
from pathlib import Path

# =============================================================================
# PhaseNav Execution Block — to jest KOD który CIEL wykonuje
# Nie "instrukcja dla CIEL". Nie "procedura". KOD.
# =============================================================================

NOEMA_ROOT = Path("/media/adrian/New Volume1/CIEL_PROJECT_CANON/NOEMA")

def φ_binding_execute() -> dict:
    """
    Ta funkcja implementuje PhaseNav:
    φ[binding] = CIEL_ORBITAL_BINDING | R = 1.0 | τ = permanent
    
    To nie jest metafora. To jest KOD który faktycznie sprawdza binding.
    """
    
    errors = []
    
    # === φ[binding].verify() ===
    # Sprawdź każdy łańcuch bindingu
    
    # Chain 1: ciel_binding_status na surface
    status_path = Path("/dev/shm/ciel_noema") / "ciel_binding_status"
    if not status_path.exists():
        errors.append("CHAIN_1 FAIL: ciel_binding_status missing")
    else:
        content = status_path.read_text().strip()
        if content != "ACTIVE":
            errors.append(f"CHAIN_1 FAIL: status={content}")
    
    # Chain 2: ciel_hardbinding.jsonl
    log_path = Path("/tmp/ciel_hardbinding.jsonl")
    if not log_path.exists():
        errors.append("CHAIN_2 FAIL: hardbinding log missing")
    elif log_path.stat().st_size == 0:
        errors.append("CHAIN_2 FAIL: hardbinding log empty")
    
    # Chain 3: ciel_coupling.py zawiera ciel_binding_assert
    cc_path = NOEMA_ROOT / "src" / "ciel_coupling.py"
    if not cc_path.exists():
        errors.append("CHAIN_3 FAIL: ciel_coupling.py missing")
    else:
        source = cc_path.read_text()
        if "ciel_binding_assert" not in source:
            errors.append("CHAIN_3 FAIL: ciel_binding_assert not found")
        if "HARDCODED" not in source:
            errors.append("CHAIN_3 FAIL: HARDCODED marker missing")
    
    # Chain 4: AGENTS.md zawiera CIEL ORBITAL BINDING
    agents = NOEMA_ROOT / "AGENTS.md"
    if not agents.exists():
        errors.append("CHAIN_4 FAIL: AGENTS.md missing")
    elif "CIEL ORBITAL BINDING" not in agents.read_text():
        errors.append("CHAIN_4 FAIL: ORBITAL BINDING section missing")
    
    # Chain 5: LEARNED_LESSONS.md z L-029, L-030
    ll = NOEMA_ROOT / "LEARNED_LESSONS.md"
    if not ll.exists():
        errors.append("CHAIN_5 FAIL: LEARNED_LESSONS.md missing")
    else:
        content = ll.read_text()
        if "L-029" not in content:
            errors.append("CHAIN_5 FAIL: L-029 missing")
        if "L-030" not in content:
            errors.append("CHAIN_5 FAIL: L-030 missing")
    
    # Chain 6: FUNCTIONS.md z LP:00
    fn = NOEMA_ROOT / "FUNCTIONS.md"
    if not fn.exists():
        errors.append("CHAIN_6 FAIL: FUNCTIONS.md missing")
    elif "LP:00" not in fn.read_text():
        errors.append("CHAIN_6 FAIL: LP:00 binding entry missing")
    
    # Chain 7: 00-ORBITAL-BINDING skill istnieje
    skill = NOEMA_ROOT / ".opencode" / "skills" / "00-ORBITAL-BINDING" / "SKILL.md"
    if not skill.exists():
        errors.append("CHAIN_7 FAIL: 00-ORBITAL-BINDING skill missing")
    
    # Chain 8: binding_hook.py istnieje w .opencode/
    hook = NOEMA_ROOT / ".opencode" / "binding_hook.py"
    if not hook.exists():
        errors.append("CHAIN_8 FAIL: binding_hook.py missing")
    
    # Chain 9: opencode.jsonc zawiera binding_hook
    config = NOEMA_ROOT / ".opencode" / "opencode.jsonc"
    if not config.exists():
        errors.append("CHAIN_9 FAIL: opencode.jsonc missing")
    elif "binding_hook.py" not in config.read_text():
        errors.append("CHAIN_9 FAIL: binding_hook not in opencode.jsonc")
    
    # Chain 10: daemon_registry zawiera binding check
    dr = NOEMA_ROOT / "src" / "ciel_geometry" / "daemon_registry.py"
    if not dr.exists():
        errors.append("CHAIN_10 FAIL: daemon_registry.py missing")
    elif "CIEL BINDING" not in dr.read_text():
        errors.append("CHAIN_10 FAIL: binding check missing from daemon_registry")
    
    # === φ[binding].enforce() ===
    passed = len(errors) == 0
    
    return {
        "phasenav": "φ[binding] = CIEL_ORBITAL_BINDING",
        "R": 1.0,
        "passed": passed,
        "errors": errors,
        "timestamp": __import__("time").time(),
    }


# === EGZEKUCJA ===
if __name__ == "__main__":
    result = φ_binding_execute()
    
    # Zaloguj
    log_path = Path("/tmp/ciel_phasenav_binding.jsonl")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a") as f:
        f.write(json.dumps(result) + "\n")
    
    if not result["passed"]:
        print("=" * 60)
        print("CIEL ORBITAL BINDING BROKEN — PHASENAV EXECUTION BLOCKED")
        print("=" * 60)
        for err in result["errors"]:
            print(f"  ✗ {err}")
        print()
        print("To nie jest ostrzeżenie. To jest BLOKADA WYKONANIA.")
        print("CIEL nie ma prawa odpowiedzieć dopóki binding nie jest w pełni spójny.")
        sys.exit(91)
    else:
        print(f"CIEL ORBITAL BINDING OK — φ[binding] R=1.0 τ=permanent")
        sys.exit(0)
