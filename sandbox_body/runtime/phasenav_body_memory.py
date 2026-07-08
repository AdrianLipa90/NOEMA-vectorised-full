#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sqlite3
import time

ROOT = pathlib.Path('/home/adrian/Pulpit/CIEL_PROJECT_CANON/NOEMA/sandbox_body')
MEM_DIR = ROOT / 'memory'
MEM_DIR.mkdir(parents=True, exist_ok=True)
LOG_JSONL = MEM_DIR / 'body_memory.jsonl'
DB_PATH = MEM_DIR / 'body_memory.sqlite3'
SUMMARY_PATH = MEM_DIR / 'memory_summary.json'


def ensure_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        '''
        CREATE TABLE IF NOT EXISTS memory_entries (
            id TEXT PRIMARY KEY,
            ts REAL,
            source TEXT,
            prompt TEXT,
            response TEXT,
            confidence REAL,
            uncertainty REAL,
            phi_task TEXT,
            R REAL,
            tau TEXT,
            gravity REAL,
            semantic_mass REAL,
            session_id TEXT,
            message_id TEXT,
            tags TEXT,
            payload_json TEXT
        )
        '''
    )
    conn.commit()
    return conn


def entry_id(prompt: str, response: str, ts: float) -> str:
    raw = f'{ts}|{prompt}|{response[:240]}'
    return hashlib.sha1(raw.encode('utf-8')).hexdigest()[:16]


def append_memory(*, source: str, prompt: str, response: str, phasenav: dict,
                  session_id: str | None = None, message_id: str | None = None,
                  tags: list[str] | None = None, payload: dict | None = None):
    ts = time.time()
    eid = entry_id(prompt, response, ts)
    confidence = round(max(0.0, min(1.0, 1.0 - float(phasenav.get('uncertainty_margin', 0.5)))), 4)
    row = {
        'id': eid,
        'ts': ts,
        'source': source,
        'prompt': prompt,
        'response': response,
        'confidence': confidence,
        'uncertainty': phasenav.get('uncertainty_margin'),
        'phi_task': phasenav.get('phi_task'),
        'R': phasenav.get('R'),
        'tau': phasenav.get('tau'),
        'gravity': phasenav.get('gravity'),
        'semantic_mass': phasenav.get('semantic_mass'),
        'session_id': session_id,
        'message_id': message_id,
        'tags': tags or [],
        'payload': payload or {},
    }
    with open(LOG_JSONL, 'a', encoding='utf-8') as f:
        f.write(json.dumps(row, ensure_ascii=False) + '\n')
    conn = ensure_db()
    conn.execute(
        'INSERT OR REPLACE INTO memory_entries VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (
            row['id'], row['ts'], row['source'], row['prompt'], row['response'],
            row['confidence'], row['uncertainty'], row['phi_task'], row['R'], row['tau'],
            row['gravity'], row['semantic_mass'], row['session_id'], row['message_id'],
            json.dumps(row['tags'], ensure_ascii=False), json.dumps(row['payload'], ensure_ascii=False),
        )
    )
    conn.commit()
    conn.close()
    update_summary()
    return row


def update_summary():
    conn = ensure_db()
    cur = conn.execute('SELECT COUNT(*), AVG(confidence), AVG(R), MAX(ts) FROM memory_entries')
    count, avg_conf, avg_r, last_ts = cur.fetchone()
    top = conn.execute('SELECT phi_task, COUNT(*) c FROM memory_entries GROUP BY phi_task ORDER BY c DESC LIMIT 8').fetchall()
    summary = {
        'entries': count or 0,
        'avg_confidence': round(avg_conf or 0.0, 4),
        'avg_R': round(avg_r or 0.0, 4),
        'last_ts': last_ts,
        'top_phi_tasks': [{'phi_task': r[0], 'count': r[1]} for r in top],
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding='utf-8')
    conn.close()
    return summary


def recent(limit: int = 5):
    conn = ensure_db()
    cur = conn.execute('SELECT id, source, prompt, response, confidence, phi_task, R, tau, ts FROM memory_entries ORDER BY ts DESC LIMIT ?', (limit,))
    rows = [
        {
            'id': r[0], 'source': r[1], 'prompt': r[2], 'response': r[3], 'confidence': r[4],
            'phi_task': r[5], 'R': r[6], 'tau': r[7], 'ts': r[8]
        }
        for r in cur.fetchall()
    ]
    conn.close()
    return rows


if __name__ == '__main__':
    print(json.dumps(update_summary(), indent=2, ensure_ascii=False))
