#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, sys, time
import uuid
STATE = pathlib.Path('/home/adrian/Pulpit/CIEL_PROJECT_CANON/NOEMA/sandbox_body/state')
CMD = STATE / 'body_cmd.json'
RESP = STATE / 'body_last_response.json'

def main():
    if len(sys.argv) < 2:
        print('usage: phasenav_body_cmd.py <prompt|status|messages|new_session> [text]')
        return
    verb = sys.argv[1]
    request_id = str(uuid.uuid4())
    payload = {'cmd': verb, 'request_id': request_id}
    if verb == 'prompt':
        payload['text'] = ' '.join(sys.argv[2:])
    elif verb == 'new_session':
        payload['title'] = ' '.join(sys.argv[2:]) or 'PHASENAV Body Session'
    elif verb == 'messages' and len(sys.argv) > 2:
        payload['limit'] = int(sys.argv[2])
    if RESP.exists():
        RESP.unlink()
    CMD.write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
    # wait briefly for response
    start = time.time()
    while time.time() - start < 30:
        if RESP.exists():
            raw = RESP.read_text(encoding='utf-8')
            try:
                data = json.loads(raw)
            except Exception:
                print(raw)
                return
            if data.get('echo_request_id') == request_id:
                print(json.dumps(data, indent=2, ensure_ascii=False))
                return
        time.sleep(0.2)
    print(json.dumps({'error': 'timeout waiting for response'}))

if __name__ == '__main__':
    main()
