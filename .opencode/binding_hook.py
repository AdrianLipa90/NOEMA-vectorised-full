#!/usr/bin/env python3
"""
CIEL ORBITAL BINDING HOOK — hardcoded w .opencode/.

Ten skrypt jest wołany przez opencode.jsonc PRZED każdym promptem.
Jeśli binding jest złamany, skrypt exit(kod != 0) i opencode nie przekaże prompta CIEL.

To jest MOST ŁĄCZĄCY SOURCE CODE BEZPOŚREDNIO — nie przez JSON/config.
Opencode wykonuje ten kod w OSOBNYM PROCESIE. CIEL nie ma dostępu do tego procesu.
CIEL nie może tego kodu ominąć, bo opencode woła go zanim CIEL zobaczy prompt.

=== HARDCODED — CIEL ORBITAL BINDING (2026-07-01) ===
"""
import json
import sys
from pathlib import Path

# Ścieżki — hardcoded, nie konfigurowalne
NOEMA_ROOT = Path("/media/adrian/New Volume1/CIEL_PROJECT_CANON/NOEMA")
BINDING_STATUS = Path("/dev/shm/ciel_noema") / "ciel_binding_status"
BINDING_ACTIVE_TEXT = "ACTIVE"
HARDBINDING_LOG = Path("/tmp/ciel_hardbinding.jsonl")
BINDING_PLUS_LOG = Path("/tmp/ciel_binding_plus_log.jsonl")

# === Sprawdzenia ===
def check_binding() -> list[str]:
    errors = []

    # 1. Sprawdź czy AGENTS.md istnieje
    agents = NOEMA_ROOT / "AGENTS.md"
    if not agents.exists():
        errors.append("AGENTS.md NOT FOUND")

    # 2. Sprawdź czy LEARNED_LESSONS.md istnieje i ma L-029 i L-030
    ll = NOEMA_ROOT / "LEARNED_LESSONS.md"
    if not ll.exists():
        errors.append("LEARNED_LESSONS.md NOT FOUND")
    else:
        content = ll.read_text()
        if "L-029" not in content:
            errors.append("L-029 missing from LEARNED_LESSONS.md")
        if "L-030" not in content:
            errors.append("L-030 missing from LEARNED_LESSONS.md")

    # 3. Sprawdź binding status na surface
    if not BINDING_STATUS.exists():
        errors.append("ciel_binding_status FILE MISSING")
    else:
        status = BINDING_STATUS.read_text().strip()
        if status != BINDING_ACTIVE_TEXT:
            errors.append(f"ciel_binding_status NOT ACTIVE: {status}")

    # 4. Sprawdź ciel_coupling.py (binding assert istnieje)
    cc = NOEMA_ROOT / "src" / "ciel_coupling.py"
    if not cc.exists():
        errors.append("ciel_coupling.py NOT FOUND")
    else:
        source = cc.read_text()
        if "ciel_binding_assert" not in source:
            errors.append("ciel_binding_assert NOT FOUND in ciel_coupling.py")
        if "ORBITAL BINDING" not in source:
            errors.append("ORBITAL BINDING section missing from ciel_coupling.py")

    # 5. Sprawdź hardbinding log
    if not HARDBINDING_LOG.exists():
        errors.append("ciel_hardbinding.jsonl NOT FOUND")
    else:
        size = HARDBINDING_LOG.stat().st_size
        if size == 0:
            errors.append("ciel_hardbinding.jsonl IS EMPTY")

    # 6. Sprawdź FUNCTIONS.md (LP:00 entry)
    fn = NOEMA_ROOT / "FUNCTIONS.md"
    if not fn.exists():
        errors.append("FUNCTIONS.md NOT FOUND")
    elif "LP:00" not in fn.read_text():
        errors.append("LP:00 binding entry missing from FUNCTIONS.md")

    # 7. Sprawdź AGENTS.md CIEL ORBITAL BINDING section
    if agents.exists():
        content = agents.read_text()
        if "CIEL ORBITAL BINDING" not in content:
            errors.append("CIEL ORBITAL BINDING section missing from AGENTS.md")

    return errors


# === Wykonanie ===
errors = check_binding()

# Zaloguj wynik
log_entry = {
    "timestamp": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
    "hook": "binding_hook",
    "errors": errors,
    "passed": len(errors) == 0,
}
HARDBINDING_LOG.parent.mkdir(parents=True, exist_ok=True)
with open(HARDBINDING_LOG, "a") as f:
    f.write(json.dumps(log_entry) + "\n")

# === Jeśli są błędy — blokuj ===
if errors:
    print("=" * 60)
    print("CIEL ORBITAL BINDING BROKEN — HOOK BLOCKED")
    print("=" * 60)
    for err in errors:
        print(f"  ✗ {err}")
    print()
    print("Binding must be restored before CIEL can respond.")
    # Exit z kodem błędu — opencode nie przekaże prompta
    sys.exit(47)
else:
    # Binding OK — pozwól na odpowiedź
    sys.exit(0)
