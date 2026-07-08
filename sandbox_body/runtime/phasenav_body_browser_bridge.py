#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path('/home/adrian/Pulpit/CIEL_PROJECT_CANON/NOEMA/sandbox_body/runtime')
RENDER = ROOT / 'phasenav_body_render.py'
BROWSER_PAGE = pathlib.Path('/dev/shm/ciel_noema/browser/page.json')


def main():
    if not BROWSER_PAGE.exists():
        print(json.dumps({
            'error': 'browser page not found',
            'expected': str(BROWSER_PAGE),
            'hint': 'uruchom browser surface i komendę read/navigate'
        }, ensure_ascii=False, indent=2))
        return 1
    cmd = ['/usr/bin/python3', str(RENDER), '--browser']
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.stdout:
        print(proc.stdout)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)
    return proc.returncode


if __name__ == '__main__':
    raise SystemExit(main())
