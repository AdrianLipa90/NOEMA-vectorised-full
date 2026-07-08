#!/usr/bin/env python3
from __future__ import annotations
import json, math, pathlib, sys, time
from opencode_runtime import SandboxServer, BodyClient, BASE, DIRECTORY, STATE, PROTO
from phasenav_body_memory import append_memory

RENDER_STATE = STATE / 'body_render_state.json'
RENDER_LAST = STATE / 'body_render_last.json'
BROWSER_PAGE = pathlib.Path('/dev/shm/ciel_noema/browser/page.json')


def extract_parts(messages):
    text_parts, reasoning_parts, tool_parts, steps = [], [], [], []
    for item in messages or []:
        info = item.get('info', {})
        for part in item.get('parts', []):
            t = part.get('type')
            if t == 'text' and part.get('text'):
                text_parts.append(part['text'])
            elif t == 'reasoning' and part.get('text'):
                reasoning_parts.append(part['text'])
            elif t == 'tool':
                tool_parts.append(part)
            elif t in ('step-start', 'step-finish'):
                steps.append(part)
    return text_parts, reasoning_parts, tool_parts, steps


def derive_phasenav(reply, messages):
    info = (reply or {}).get('info', {})
    tokens = info.get('tokens', {})
    finish = info.get('finish', 'unknown')
    text_parts, reasoning_parts, tool_parts, steps = extract_parts(messages)
    output_tokens = tokens.get('output', 0) or 0
    reasoning_tokens = tokens.get('reasoning', 0) or 0
    input_tokens = tokens.get('input', 0) or 0
    cache_read = ((tokens.get('cache') or {}).get('read', 0) or 0)
    has_error = bool(info.get('error'))

    # Heurystyka rendererowa, nie fizyka kanoniczna
    coherence = 0.35
    if finish == 'stop':
        coherence += 0.18
    if text_parts:
        coherence += 0.14
    if reasoning_parts:
        coherence += 0.08
    if tool_parts:
        coherence += 0.05
    if has_error:
        coherence -= 0.22
    coherence += min(0.12, cache_read / 100000.0)
    coherence = max(0.0, min(0.99, coherence))

    uncertainty = 0.55
    if has_error:
        uncertainty += 0.25
    if finish == 'stop':
        uncertainty -= 0.10
    if text_parts:
        uncertainty -= 0.08
    if output_tokens > 0:
        uncertainty -= min(0.12, output_tokens / 1000.0)
    if reasoning_tokens > 0:
        uncertainty -= min(0.05, reasoning_tokens / 1000.0)
    uncertainty = max(0.01, min(0.99, uncertainty))

    tau = 'warm'
    if has_error:
        tau = 'fractured'
    elif finish != 'stop':
        tau = 'streaming'
    elif output_tokens > 180:
        tau = 'expansive'

    phi_task = 'response-synthesis'
    if tool_parts:
        phi_task = 'tool-mediated-response'
    elif reasoning_parts:
        phi_task = 'reasoned-response'

    gravity = round(min(9.0, 1.0 + math.log1p(input_tokens + output_tokens) / 2.0), 3)
    semantic_mass = round(min(9.0, len(' '.join(text_parts)) / 180.0 + len(tool_parts) * 0.5), 3)

    return {
        'phi_task': phi_task,
        'R': round(coherence, 4),
        'tau': tau,
        'uncertainty_margin': round(uncertainty, 4),
        'gravity': gravity,
        'semantic_mass': semantic_mass,
        'finish': finish,
        'has_error': has_error,
        'tool_count': len(tool_parts),
        'text_count': len(text_parts),
        'reasoning_count': len(reasoning_parts),
        'step_count': len(steps),
        'tokens': tokens,
        'last_text': text_parts[-1] if text_parts else None,
        'last_reasoning': reasoning_parts[-1] if reasoning_parts else None,
    }


def render_prompt(prompt: str, agent: str = 'build'):
    server = SandboxServer().start()
    client = BodyClient(BASE, DIRECTORY)
    try:
        session = client.create_session('PHASENAV Render Session')
        session_id = session['id']
        reply = client.prompt(session_id, prompt, agent=agent)
        messages = client.messages(session_id, limit=30)
        ph = derive_phasenav(reply, messages)
        rendered = {
            'session_id': session_id,
            'message_id': ((reply or {}).get('info') or {}).get('id'),
            'prompt': prompt,
            'agent': agent,
            'phasenav': ph,
            'messages': messages[-4:] if isinstance(messages, list) else messages,
            'updated_at': time.time(),
        }
        RENDER_LAST.write_text(json.dumps(rendered, indent=2, ensure_ascii=False), encoding='utf-8')
        RENDER_STATE.write_text(json.dumps(ph, indent=2, ensure_ascii=False), encoding='utf-8')
        (PROTO/'render_last.json').write_text(json.dumps(rendered, indent=2, ensure_ascii=False), encoding='utf-8')
        append_memory(
            source='sandbox-render',
            prompt=prompt,
            response=ph.get('last_text') or '',
            phasenav=ph,
            session_id=session_id,
            message_id=rendered['message_id'],
            tags=['render', agent],
            payload={
                'last_reasoning': ph.get('last_reasoning'),
                'tool_count': ph.get('tool_count'),
                'tokens': ph.get('tokens'),
            },
        )
        return rendered
    finally:
        server.stop()


def render_browser_page(agent: str = 'build', max_chars: int = 4000):
    if not BROWSER_PAGE.exists():
        raise FileNotFoundError(f'browser page not found: {BROWSER_PAGE}')
    page = json.loads(BROWSER_PAGE.read_text(encoding='utf-8'))
    title = page.get('title', '')
    url = page.get('url', '')
    text = page.get('full_text', '')[:max_chars]
    prompt = (
        f'Przeczytaj tę stronę i streść jej sens dla CIEL/NOEMA.\\n\\n'
        f'TITLE: {title}\\nURL: {url}\\n\\nCONTENT:\\n{text}'
    )
    rendered = render_prompt(prompt, agent=agent)
    rendered['sensor'] = {
        'type': 'browser-page',
        'title': title,
        'url': url,
        'word_count': page.get('word_count', 0),
    }
    RENDER_LAST.write_text(json.dumps(rendered, indent=2, ensure_ascii=False), encoding='utf-8')
    (PROTO/'render_browser_last.json').write_text(json.dumps(rendered, indent=2, ensure_ascii=False), encoding='utf-8')
    append_memory(
        source='browser-sensor',
        prompt=prompt,
        response=rendered['phasenav'].get('last_text') or '',
        phasenav=rendered['phasenav'],
        session_id=rendered.get('session_id'),
        message_id=rendered.get('message_id'),
        tags=['browser', 'sensor', agent],
        payload={'browser_page': {'title': title, 'url': url, 'word_count': page.get('word_count', 0)}},
    )
    return rendered


def main():
    args = sys.argv[1:]
    if args and args[0] == '--browser':
        rendered = render_browser_page()
    else:
        prompt = ' '.join(args).strip() or 'Powiedz krótko, czym jest NOEMA.'
        rendered = render_prompt(prompt)
    print(json.dumps({
        'session_id': rendered['session_id'],
        'message_id': rendered['message_id'],
        'phasenav': rendered['phasenav'],
        'last_text': rendered['phasenav']['last_text'],
    }, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
