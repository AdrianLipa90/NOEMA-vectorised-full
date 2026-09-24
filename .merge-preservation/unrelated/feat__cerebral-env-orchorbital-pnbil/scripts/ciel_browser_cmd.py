#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys
import uuid

CMD = pathlib.Path('/dev/shm/ciel_noema/browser/cmd.json')


def main():
    if len(sys.argv) < 2:
        print('usage: ciel_browser_cmd.py <navigate|read|search|click|scroll|status|close|quit> [arg]')
        return 1
    verb = sys.argv[1]
    payload = {'request_id': str(uuid.uuid4()), 'cmd': verb}
    if verb in ('navigate', 'goto') and len(sys.argv) > 2:
        payload['url'] = ' '.join(sys.argv[2:])
    elif verb in ('search', 'find') and len(sys.argv) > 2:
        payload['query'] = ' '.join(sys.argv[2:])
    elif verb == 'click' and len(sys.argv) > 2:
        payload['text'] = ' '.join(sys.argv[2:])
    elif verb == 'scroll' and len(sys.argv) > 2:
        payload['dir'] = sys.argv[2]
    CMD.write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
