#!/usr/bin/env python3
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import pathlib
import sys
import time

from opencode_runtime import SandboxServer, BodyClient, DIRECTORY, STATE, PROTO
from phasenav_body_render import derive_phasenav
from phasenav_body_memory import append_memory
from phasenav_body_skills import find_skills, enrich_prompt, log_skill_usage, contract_context

CONTINUITY_FILE = STATE / 'body_continuity.json'
OUT_FILE = STATE / 'body_continuity_last.json'


def load_continuity() -> dict:
    if not CONTINUITY_FILE.exists():
        return {}
    try:
        return json.loads(CONTINUITY_FILE.read_text(encoding='utf-8'))
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/phasenav_body_continuity.py:23 quiet except scope=load_continuity reason=return {}")
        return {}


def save_continuity(payload: dict):
    CONTINUITY_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding='utf-8')


def run_prompt(prompt: str, agent: str = 'build', skill_aware: bool = True):
    """Send a prompt through the sandbox body with optional skill-aware enrichment.

    Args:
        prompt: The prompt text
        agent: opencode agent to use (default: 'build')
        skill_aware: If True, enriches prompt with matching skill context + contracts

    Returns:
        dict with session_id, message_id, phasenav, skills_used, contracts_applied
    """
    continuity = load_continuity()
    parent_id = continuity.get('session_id')

    # PhaseNav state before action (C-002)
    ph_pre = {
        'phi_task': 'skill-aware-prompt',
        'R': 0.0,
        'tau': 'priming',
        'decision': f'run_prompt with skill_aware={skill_aware}',
    }

    # Step 1: Enrich prompt with skills + contracts (C-001, C-010)
    skills_used = []
    contracts_applied = []
    if skill_aware:
        enriched, skills_used, contracts_applied = enrich_prompt(prompt)
        actual_prompt = enriched
    else:
        actual_prompt = prompt

    server = SandboxServer(port=4101).start()
    client = BodyClient(server.base, DIRECTORY)
    try:
        title = 'PHASENAV Body Continuity Session'
        session = client.create_session(title, parent_id=parent_id)
        session_id = session['id']
        reply = client.prompt(session_id, actual_prompt, agent=agent)
        messages = client.messages(session_id, limit=30)
        ph = derive_phasenav(reply, messages)

        # Log skill usage (C-010 audit trail)
        for s in skills_used:
            log_skill_usage(s['skill_name'], prompt, session_id)

        result = {
            'session_id': session_id,
            'parent_id': parent_id,
            'message_id': ((reply or {}).get('info') or {}).get('id'),
            'prompt': prompt,
            'enriched': skill_aware,
            'skills_used': [s['skill_name'] for s in skills_used],
            'contracts_applied': [c['id'] for c in contracts_applied],
            'agent': agent,
            'phasenav': ph,
            'phasenav_pre': ph_pre,
            'messages': messages[-4:] if isinstance(messages, list) else messages,
            'updated_at': time.time(),
        }
        OUT_FILE.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
        (PROTO / 'continuity_last.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
        save_continuity({
            'session_id': session_id,
            'parent_id': parent_id,
            'title': title,
            'last_summary': {
                'last_text': ph.get('last_text'),
                'phi_task': ph.get('phi_task'),
                'R': ph.get('R'),
                'tau': ph.get('tau'),
                'skills_used': [s['skill_name'] for s in skills_used],
            },
            'updated_at': time.time(),
        })
        append_memory(
            source='continuity-orchestrator',
            prompt=actual_prompt,
            response=ph.get('last_text') or '',
            phasenav=ph,
            session_id=session_id,
            message_id=result['message_id'],
            tags=['continuity', agent, 'skill-aware'] if skill_aware else ['continuity', agent],
            payload={
                'parent_id': parent_id,
                'agent': agent,
                'skills_used': [s['skill_name'] for s in skills_used],
                'contracts_applied': [c['id'] for c in contracts_applied],
                'original_prompt': prompt,
            },
        )
        return result
    finally:
        server.stop()


def main():
    prompt = ' '.join(sys.argv[1:]).strip() or 'Powiedz krótko, jaki jest stan continuity nowego ciała.'
    skill_aware = '--raw' not in sys.argv  # --raw bypasses skill enrichment
    result = run_prompt(prompt, skill_aware=skill_aware)
    print(json.dumps({
        'session_id': result['session_id'],
        'parent_id': result['parent_id'],
        'message_id': result['message_id'],
        'phasenav': result['phasenav'],
        'skills_used': result['skills_used'],
        'contracts_applied': result['contracts_applied'],
        'enriched': result['enriched'],
        'last_text': result['phasenav'].get('last_text'),
    }, indent=2, ensure_ascii=False))
    # Log to auto-log FIFO if available
    try:
        fifo = pathlib.Path('/dev/shm/ciel_noema/auto_log.fifo')
        if fifo.exists():
            log_entry = json.dumps({
                'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime()),
                'role': 'system',
                'content': f'continuity-run: {prompt[:120]}... skills={result["skills_used"]} contracts={result["contracts_applied"]}',
                'tags': 'continuity,body,skill-aware' if skill_aware else 'continuity,body,raw',
            })
            fifo.write_text(log_entry + '\n')
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("sandbox_body/runtime/phasenav_body_continuity.py:151 quiet except scope=main reason=pass")
        pass  # FIFO write is best-effort


if __name__ == '__main__':
    main()
