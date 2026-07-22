#!/usr/bin/env python3
"""
noema_surface_refresh.py — Automatyczne odświeżanie mmap dla KAŻDEGO systemu i subsystemu.

Uruchamiany co 15 minut przez systemd timer.
Czyta system_map_v2.json i aktualizuje /dev/shm/ciel_noema/system_map.
Dla każdego daemona/skryptu: uruchamia refresh jesli runtime_file istnieje.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import os
import pathlib
import subprocess
import sys
import time

_SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
SURFACE = pathlib.Path('/dev/shm/ciel_noema')
NOEMA_ROOT = pathlib.Path(os.environ.get("NOEMA_ROOT", str(_SCRIPT_DIR.parent)))
MAP_FILE = NOEMA_ROOT / 'system_map_v2.json'

SYSTEM_MAP_DTYPE = [
    ('id', 'U50'), ('name', 'U50'), ('ordinal', 'U10'),
    ('status', 'U20'), ('layer', 'U30'), ('type', 'U20'),
    ('last_refresh', 'f8'), ('R', 'f8'), ('tau', 'U20'), ('health', 'f8'),
]


def read_existing_system_map() -> dict:
    """Read current values from system_map mmap to preserve state."""
    import numpy as np
    mmap_file = SURFACE / 'system_map'
    if not mmap_file.exists():
        return {}
    try:
        dtype = np.dtype(SYSTEM_MAP_DTYPE)
        mmap = np.memmap(str(mmap_file), dtype=dtype, mode='r')
        result = {}
        for i in range(len(mmap)):
            key = (str(mmap[i]['ordinal']).strip(), str(mmap[i]['id']).strip())
            result[key] = {
                'last_refresh': float(mmap[i]['last_refresh']),
                'R': float(mmap[i]['R']),
                'tau': str(mmap[i]['tau']),
                'health': float(mmap[i]['health']),
            }
        return result
    except Exception as e:
        print(f'[refresh] read existing error: {e}')
        return {}


def run_script(script_path: str) -> dict:
    """Run a system's runtime_file and return its status."""
    full_path = NOEMA_ROOT / script_path
    if not full_path.exists():
        return {'status': 'missing', 'R': 0.0, 'tau': 'missing', 'health': 0.0}
    try:
        result = subprocess.run(
            [sys.executable, str(full_path), '--status'],
            capture_output=True, text=True, timeout=10,
            cwd=str(NOEMA_ROOT),
        )
        # Try to parse output as JSON
        for line in result.stdout.split('\n'):
            line = line.strip()
            if line.startswith('{') and line.endswith('}'):
                try:
                    return json.loads(line)
                except json.JSONDecodeError:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_surface_refresh.py:71 quiet except scope=run_script reason=continue")
                    raise
                    continue
        return {
            'status': 'active' if result.returncode == 0 else 'error',
            'R': 0.0, 'tau': 'unknown', 'health': 0.5,
        }
    except subprocess.TimeoutExpired:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_surface_refresh.py:77 quiet except scope=run_script reason=return {'status': 'timeout', 'R': 0.0, 'tau': 'timeout', 'health': 0.0}")
        raise
        return {'status': 'timeout', 'R': 0.0, 'tau': 'timeout', 'health': 0.0}
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_surface_refresh.py:79 quiet except scope=run_script reason=return {'status': 'error', 'R': 0.0, 'tau': str(e)[:20], 'health': 0.0}")
        raise
        return {'status': 'error', 'R': 0.0, 'tau': str(e)[:20], 'health': 0.0}


def read_surface_values() -> dict:
    """Read key metrics from surface mmap files."""
    import numpy as np
    result = {}
    try:
        # Read phi → compute R
        phi_file = SURFACE / 'phi'
        if phi_file.exists():
            phi = np.memmap(str(phi_file), dtype='float64', mode='r', shape=(36,))
            result['surface_R'] = float(np.abs(np.mean(np.exp(1j * phi))))
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_surface_refresh.py:93 quiet except scope=read_surface_values reason=pass")
        raise
        pass
    try:
        flavor_file = SURFACE / 'flavor'
        if flavor_file.exists():
            flavor = np.memmap(str(flavor_file), dtype='float64', mode='r', shape=(6,))
            result['flavor_coherence'] = float(flavor[0])
            result['flavor_mood'] = float(flavor[3])
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_surface_refresh.py:101 quiet except scope=read_surface_values reason=pass")
        raise
        pass
    try:
        tick_file = SURFACE / 'tick'
        if tick_file.exists():
            result['tick'] = int(np.memmap(str(tick_file), dtype='float64', mode='r', shape=(1,))[0])
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_surface_refresh.py:107 quiet except scope=read_surface_values reason=pass")
        raise
        pass
    return result


def refresh_all():
    """Main: rebuild system_map mmap from system_map_v2.json + live values."""
    import numpy as np

    if not SURFACE.exists():
        print(f'[refresh] Surface {SURFACE} not found')
        return 1

    if not MAP_FILE.exists():
        print(f'[refresh] Map file {MAP_FILE} not found')
        return 1

    # Load system map
    with open(MAP_FILE) as f:
        data = json.load(f)

    # Preserve existing values
    existing = read_existing_system_map()

    # Read live surface metrics
    surface_vals = read_surface_values()

    # Build entries
    entries = []
    now = time.time()

    for s in data['systems']:
        sid = s.get('id', '')
        key = (s.get('ordinal', ''), sid)
        old = existing.get(key, {})

        entries.append({
            'id': sid[:50],
            'name': s.get('name', '')[:50],
            'ordinal': s.get('ordinal', '')[:10],
            'status': s.get('status', 'unknown')[:20],
            'layer': s.get('layer', '')[:30],
            'type': s.get('type', 'system')[:20],
            'last_refresh': old.get('last_refresh', now),
            'R': old.get('R', surface_vals.get('surface_R', 0.0)),
            'tau': old.get('tau', 'unknown')[:20],
            'health': old.get('health', surface_vals.get('flavor_coherence', 0.0)),
        })

        for sub in s.get('subsystems', []):
            sub_key = (sub.get('ordinal', ''), sub.get('id', ''))
            sub_old = existing.get(sub_key, {})
            entries.append({
                'id': sub.get('id', '')[:50],
                'name': sub.get('name', '')[:50],
                'ordinal': sub.get('ordinal', '')[:10],
                'status': sub.get('status', s.get('status', 'unknown'))[:20],
                'layer': s.get('layer', '')[:30],
                'type': 'subsystem',
                'last_refresh': sub_old.get('last_refresh', now),
                'R': sub_old.get('R', 0.0),
                'tau': sub_old.get('tau', 'unknown')[:20],
                'health': sub_old.get('health', 0.0),
            })

    print(f'[refresh] Building {len(entries)} entries')

    # Write mmap
    dtype = np.dtype(SYSTEM_MAP_DTYPE)
    arr = np.zeros(len(entries), dtype=dtype)
    for i, e in enumerate(entries):
        for k, v in e.items():
            try:
                arr[i][k] = v
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_surface_refresh.py:181 quiet except scope=refresh_all reason=pass")
                raise
                pass

    mmap_file = SURFACE / 'system_map'
    if mmap_file.exists():
        mmap_file.unlink()
    mmap = np.memmap(str(mmap_file), dtype=dtype, mode='w+', shape=(len(arr),))
    mmap[:] = arr[:]
    mmap.flush()

    print(f'[refresh] Written {len(arr)} entries ({mmap_file.stat().st_size} bytes)')
    print(f'[refresh] surface_R={surface_vals.get("surface_R", "N/A"):.4f}')
    return 0


if __name__ == '__main__':
    sys.exit(refresh_all())
