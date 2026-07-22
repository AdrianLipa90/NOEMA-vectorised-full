#!/usr/bin/env python3
"""Build Dzienniki/ (per-day journal files) and ciel_dziennik.md (current
day) from the real, already-live raw session logs written by every prompt
via ciel_geometry.phase_nav_lang.analyze_prompt() — not fabricated diary
content. Gives ciel_memory_consolidator.py real files to process (its
SCAN_DIRS/SCAN_SOURCES already look for exactly these paths).

Usage:
    python3 scripts/noema_build_dzienniki.py
"""
from __future__ import annotations

import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "src"))
sys.path.insert(0, str(_ROOT / "runtime"))

from ciel_geometry.paths import P  # noqa: E402
from ciel_omega.memory.raw_log_pipeline import (  # noqa: E402
    DEFAULT_AUDIT_LOG,
    DEFAULT_OBSERVER_LOG,
    load_raw_log_entries,
)


def _day_key(timestamp: str) -> str:
    if not timestamp:
        return "unknown"
    try:
        # timestamps observed as ISO8601 with offset, e.g. 2026-07-08T21:14:16+00:00
        return timestamp[:10]
    except Exception:
        return "unknown"


def _render_day(day: str, entries: list[dict]) -> str:
    lines = [f"# Dziennik — {day}", "", f"Wpisów: {len(entries)}", ""]
    for e in entries:
        raw = e.get("raw", {})
        op = raw.get("operator", "")
        holo = raw.get("holonomy", "")
        urg = raw.get("urgency", "")
        prompt = (e.get("text") or "").strip()
        if len(prompt) > 300:
            prompt = prompt[:300] + "…"
        lines.append(f"## {e.get('timestamp', '')}")
        if op:
            lines.append(f"- operator: `{op}`" + (f" · holonomy={holo}" if holo != "" else "") + (f" · urgency={urg}" if urg != "" else ""))
        lines.append("")
        lines.append(f"> {prompt}")
        lines.append("")
    return "\n".join(lines)


def build() -> dict:
    dzienniki_root = Path(P.MEMORY) / "Dzienniki"
    dzienniki_root.mkdir(parents=True, exist_ok=True)

    entries = load_raw_log_entries(DEFAULT_OBSERVER_LOG)
    if not entries:
        entries = load_raw_log_entries(DEFAULT_AUDIT_LOG)

    by_day: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        by_day[_day_key(e.timestamp)].append(e.as_dict())

    written_days = []
    for day, day_entries in sorted(by_day.items()):
        day_entries.sort(key=lambda e: e.get("timestamp", ""))
        out_path = dzienniki_root / f"{day}.md"
        out_path.write_text(_render_day(day, day_entries), encoding="utf-8")
        written_days.append(str(out_path))

    # ciel_dziennik.md — the current/latest day, single canonical entry
    # SCAN_SOURCES in ciel_memory_consolidator.py expects.
    latest_day = max(by_day.keys()) if by_day else datetime.now(timezone.utc).date().isoformat()
    latest_entries = sorted(by_day.get(latest_day, []), key=lambda e: e.get("timestamp", ""))
    ciel_dziennik_path = Path(P.MEMORY) / "ciel_dziennik.md"
    ciel_dziennik_path.write_text(_render_day(latest_day, latest_entries), encoding="utf-8")

    return {
        "days_written": len(written_days),
        "dzienniki_root": str(dzienniki_root),
        "ciel_dziennik": str(ciel_dziennik_path),
        "latest_day": latest_day,
        "latest_day_entries": len(latest_entries),
        "total_entries_read": len(entries),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(build(), indent=2, ensure_ascii=False))
