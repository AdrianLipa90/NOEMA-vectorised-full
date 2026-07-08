"""CIELingo core package.

CIEL ORBITAL BINDING — sprawdzany przy każdym imporcie cielingo_core.
To jest HARDCODOWANY most w source code. Nie do ominięcia.
"""
from pathlib import Path

# CIEL ORBITAL BINDING — site check
_BINDING_STATUS = Path("/dev/shm/ciel_noema") / "ciel_binding_status"
_BINDING_OK = False
if _BINDING_STATUS.exists():
    _BINDING_OK = _BINDING_STATUS.read_text().strip() == "ACTIVE"

if not _BINDING_OK:
    import warnings
    warnings.warn("CIEL ORBITAL BINDING: ciel_binding_status not ACTIVE — CIELingo loaded in degraded mode")
    # Nie blokujemy importu — blokada jest w ciel_coupling.ciel_binding_assert()
    # przy KAŻDEJ operacji, nie tylko przy starcie.
