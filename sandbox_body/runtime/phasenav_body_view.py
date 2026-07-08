#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib
STATE = pathlib.Path('/home/adrian/Pulpit/CIEL_PROJECT_CANON/NOEMA/sandbox_body/state/body_render_state.json')
LAST = pathlib.Path('/home/adrian/Pulpit/CIEL_PROJECT_CANON/NOEMA/sandbox_body/state/body_render_last.json')
if LAST.exists():
    print(LAST.read_text(encoding='utf-8'))
elif STATE.exists():
    print(STATE.read_text(encoding='utf-8'))
else:
    print(json.dumps({'error': 'no render state yet'}, ensure_ascii=False))
