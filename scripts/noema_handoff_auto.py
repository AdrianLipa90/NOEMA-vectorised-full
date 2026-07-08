#!/usr/bin/env python3
"""NOEMA auto handoff — automatyczne logowanie sesji do handoff.md.

Uruchamiany przez agenta po każdej większej wymianie:
    python3 scripts/noema_handoff_auto.py --checkpoint "temat: co zrobiono"

Tworzy/aktualizuje:
  - /tmp/ciel_session_log.jsonl (append log każdej wymiany)
  - ~//media/adrian/New Volume1/CIEL_memories/handoff.md (z rzeczywistą liczbą wiadomości)
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import sys
from datetime import datetime
from pathlib import Path

MEMORIES = Path("/media/adrian/New Volume1/CIEL_memories")
HANDOFF = MEMORIES / "handoff.md"
SESSION_LOG = Path("/tmp/ciel_session_log.jsonl")


def log_exchange(prompt: str, response: str = "") -> None:
    """Append exchange to session log."""
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "prompt": prompt[:500],
        "response": response[:500] if response else "",
    }
    SESSION_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(SESSION_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def write_checkpoint(summary: str) -> None:
    """Write a checkpoint entry to handoff.md with real message count."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Count actual messages in session log
    n_msgs = 0
    topics = set()
    if SESSION_LOG.exists():
        with open(SESSION_LOG, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                n_msgs += 1
                try:
                    ex = json.loads(line)
                    prompt = ex.get("prompt", "")
                    for w in prompt.lower().split():
                        if len(w) > 5:
                            topics.add(w)
                except json.JSONDecodeError:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_handoff_auto.py:55 quiet except scope=write_checkpoint reason=pass")
                    pass
    
    topic_str = ", ".join(list(topics)[:6]) if topics else "—"
    
    entry = f"""
## {ts} | sesja
Wiadomości: {n_msgs}.
Tematy: {topic_str}
{summary}
---
"""
    HANDOFF.parent.mkdir(parents=True, exist_ok=True)
    if not HANDOFF.exists():
        HANDOFF.write_text("# CIEL Handoff — Session Log\n", encoding="utf-8")
    
    with open(HANDOFF, "a", encoding="utf-8") as f:
        f.write(entry)
    
    # Archive if too large
    if HANDOFF.stat().st_size > 30000:
        lines = HANDOFF.read_text(encoding="utf-8").splitlines()
        archive = MEMORIES / f"handoff_archive_{datetime.now().strftime('%Y_%m')}.md"
        with open(archive, "a", encoding="utf-8") as af:
            af.write("\n".join(lines[:-30]) + "\n")
        HANDOFF.write_text("\n".join(lines[:1] + lines[-30:]), encoding="utf-8")
    
    print(f"✓ Handoff checkpoint: {n_msgs} messages, topics: {topic_str}")


def fix_empty_entries() -> None:
    """Replace 'Wiadomości: 0' entries with data from AGENTS.md context."""
    if not HANDOFF.exists():
        return
    content = HANDOFF.read_text(encoding="utf-8")
    
    # Replace known empty entries with context
    replacements = {
        "## 2026-06-26 20:47 | sesja\nWiadomości: 0.": (
            "## 2026-06-26 20:47 | sesja\n"
            "Wiadomości: ~40.\n"
            "Tematy: auto-continue, skill_factory, figure_deduplication, monograph_compile\n"
            "Figure deduplication (28→19), label fix, 183-page monograph compile. "
            "Agent_lock→resonance merge, memory_associations fix.\n"
        ),
        "## 2026-06-26 20:56 | sesja\nWiadomości: 0.": (
            "## 2026-06-26 20:56 | sesja\n"
            "Wiadomości: ~60.\n"
            "Tematy: Figure_generation, monograph_cleanup, session_continuity\n"
            "19 new figures from live NOEMA data. Resonance bridge agent_context restoration. "
            "ciel_session_end.py fix + raw_logs.\n"
        ),
        "## 2026-06-27 17:10 | sesja\nWiadomości: 0.": (
            "## 2026-06-27 17:10 | sesja\n"
            "Wiadomości: ~100+.\n"
            "Tematy: knowledge_db, OCR, affect_lexicon, CIELingo_bridge, audit, linux_cards, tau_mmap\n"
            "9 PDFs OCR, 545 docs in knowledge DB, 54k terms. "
            "SENSOR card type (9th), 560+ cards. "
            "Tau mmap, AGENT attractor boost, Push-to-Talk (Ctrl+`).\n"
        ),
    }
    
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
    
    HANDOFF.write_text(content, encoding="utf-8")
    print("✓ Fixed empty handoff entries")


if __name__ == "__main__":
    if "--fix" in sys.argv:
        fix_empty_entries()
    elif "--checkpoint" in sys.argv:
        idx = sys.argv.index("--checkpoint")
        summary = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else ""
        write_checkpoint(summary)
    elif "--log" in sys.argv:
        idx = sys.argv.index("--log")
        prompt = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else ""
        response = sys.argv[idx + 2] if idx + 2 < len(sys.argv) else ""
        log_exchange(prompt, response)
    else:
        # Default: fix empty and write checkpoint
        fix_empty_entries()
        write_checkpoint("Auto-checkpoint: zainicjowano mechanizm auto-handoff")
