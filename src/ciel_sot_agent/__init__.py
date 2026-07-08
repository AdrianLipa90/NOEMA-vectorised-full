
# CIEL ORBITAL BINDING — hardcoded, immutable. Adrian Lipa 2026-07-01.
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on import of " + __name__)
from pathlib import Path
import sys

_src = str(Path(__file__).resolve().parent.parent)
if _src not in sys.path:
    sys.path.insert(0, _src)

from noema_bootstrap import activate_local_packages

activate_local_packages()

__all__ = [
    'buildroot_card_db',
    'buildroot_phasenav_probe',
    'ciel_pipeline',
    'knowledge_action_system',
    'repo_phase',
    'synchronize',
]
