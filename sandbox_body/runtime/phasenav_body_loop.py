#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, sys, time
from opencode_runtime import SandboxServer, BodyClient, BASE, DIRECTORY, STATE, PROTO

STATE_FILE = STATE / 'body_state.json'


def dump_state(**kw):
    data = {
        'phi_task': 'body-loop',
        'R': kw.get('R', 0.0),
        'tau': kw.get('tau', 'probe'),
        'mode': kw.get('mode', 'idle'),
        'uncertainty_margin': kw.get('uncertainty_margin', 1.0),
        'session_id': kw.get('session_id'),
        'message_id': kw.get('message_id'),
        'last_event': kw.get('last_event'),
        'updated_at': time.time(),
    }
    STATE_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')


def main():
    prompt = ' '.join(sys.argv[1:]).strip() or 'Powiedz krótko, czym jest NOEMA w tym repozytorium.'
    dump_state(mode='boot', tau='ignite', R=0.1, uncertainty_margin=0.9)
    server = SandboxServer().start()
    client = BodyClient(BASE, DIRECTORY)
    try:
        agents = client.agents()
        (PROTO/'agents.json').write_text(json.dumps(agents, indent=2, ensure_ascii=False), encoding='utf-8')
        sess = client.create_session('PHASENAV Body Sandbox')
        session_id = sess['id']
        (PROTO/'session_created.json').write_text(json.dumps(sess, indent=2, ensure_ascii=False), encoding='utf-8')
        dump_state(mode='session_created', tau='primed', R=0.25, uncertainty_margin=0.75, session_id=session_id, last_event='session.created')
        reply = client.prompt(session_id, prompt)
        (PROTO/'prompt_reply.json').write_text(json.dumps(reply, indent=2, ensure_ascii=False), encoding='utf-8')
        mid = reply.get('info', {}).get('id')
        dump_state(mode='prompted', tau='stream-settled', R=0.55, uncertainty_margin=0.45, session_id=session_id, message_id=mid, last_event='message.created')
        msgs = client.messages(session_id, limit=20)
        (PROTO/'messages.json').write_text(json.dumps(msgs, indent=2, ensure_ascii=False), encoding='utf-8')
        # derive minimal summary
        text_parts = []
        for item in msgs:
            for part in item.get('parts', []):
                if part.get('type') == 'text' and part.get('text'):
                    text_parts.append(part['text'])
        summary = {'session_id': session_id, 'message_id': mid, 'prompt': prompt, 'text_parts': text_parts[-5:]}
        (PROTO/'body_summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding='utf-8')
        dump_state(mode='complete', tau='warm', R=0.82, uncertainty_margin=0.18, session_id=session_id, message_id=mid, last_event='session.idle')
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    finally:
        server.stop()

if __name__ == '__main__':
    main()
