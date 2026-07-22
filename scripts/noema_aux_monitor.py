#!/usr/bin/env python3
"""NOEMA aux-channel monitor — merges CIEL conversation, mood/ethical/soul
state, per-channel (M0-M11) coherence, and memory/orbital signals into one
stream, so the whole live picture is visible instead of one metric at a time.

Sources merged:
  - ciel_thread_memory.jsonl — CIEL conversation (real "calls")
  - ciel_state.json — mood_normalized, ethical_score, soul_invariant, coherence_index
  - portal /api/live — channel_coh per M0-M11
  - gravity surface array — semantic_density (memory pressure), tau_dilation

Emits one line per: new conversation exchange, OR any tracked metric
changing by more than its threshold since the last check — not every poll,
to avoid flooding.

Usage:
    python3 scripts/noema_aux_monitor.py [--interval 5]
"""
from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

SURFACE_DIR = Path("/dev/shm/ciel_noema")
THREAD_LOG = SURFACE_DIR / "ciel_thread_memory.jsonl"
STATE_PATH = SURFACE_DIR / "ciel_state.json"
PORTAL_LIVE = "http://127.0.0.1:18888/api/live"
AUDIT_LOG = Path("/media/adrian/New Volume/CIEL_memories/state/aux_monitor_audit.jsonl")


def _audit(event_type: str, payload: dict) -> None:
    """Append a deviation event to the persistent audit log — every
    reported deviation must be re-findable later, not just printed once
    to a console that scrolls away."""
    entry = {"ts": time.time(), "type": event_type, **payload}
    try:
        AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
        with AUDIT_LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError:
        pass

# Absolute-change thresholds below which a metric's drift is not reported
_THRESHOLDS = {
    "mood_normalized": 0.05,
    "ethical_score": 0.05,
    "soul_invariant": 0.05,
    "coherence_index": 0.05,
    "semantic_density": 0.5,
}
# M6/M8/M9/M11 are a known, already-investigated volatile baseline this
# session (three fix rounds, not fully resolved) — the Kuramoto surface
# genuinely oscillates fast (10Hz core loop) and single-poll deltas on a
# 5s cadence flag transient, self-correcting swings as if they were new
# incidents. Report a channel only when it has been BELOW the health
# floor for _SUSTAINED_POLLS consecutive polls — that's the difference
# between "known noisy but recovering" and "actually stuck low".
_CHANNEL_HEALTH_FLOOR = 0.35
_SUSTAINED_POLLS = 3


def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return {}


def _read_portal_live() -> dict:
    try:
        with urllib.request.urlopen(PORTAL_LIVE, timeout=3) as resp:
            return json.loads(resp.read())
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError):
        return {}


def _read_gravity() -> dict:
    try:
        import numpy as np
        g = np.memmap(str(SURFACE_DIR / "gravity"), dtype=np.float64, mode="r")
        return {"semantic_density": round(float(g[0]), 4), "tau_dilation": round(float(g[1]), 4)}
    except Exception:
        return {}


def _last_line(path: Path) -> str | None:
    try:
        with path.open("rb") as f:
            f.seek(0, 2)
            size = f.tell()
            block = min(4096, size)
            f.seek(size - block)
            lines = f.read().splitlines()
            return lines[-1].decode("utf-8", errors="replace") if lines else None
    except OSError:
        return None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--interval", type=float, default=5.0)
    args = ap.parse_args()

    last_line_seen: str | None = _last_line(THREAD_LOG)
    last_metrics: dict = {}
    low_streak: dict[str, int] = {}
    reported_stuck: set[str] = set()

    while True:
        # 1. New conversation exchange?
        current_last = _last_line(THREAD_LOG)
        if current_last and current_last != last_line_seen:
            try:
                entry = json.loads(current_last)
                state = _read_json(STATE_PATH)
                print(
                    f"[aux:{entry.get('role','?')}] "
                    f"mood={state.get('mood_normalized','?')} "
                    f"ethical={state.get('ethical_score','?')} "
                    f"soul={state.get('soul_invariant','?')} | "
                    f"{(entry.get('content','') or '')[:180]}"
                )
                _audit("exchange", {
                    "role": entry.get("role"),
                    "content": (entry.get("content", "") or "")[:500],
                    "mood": state.get("mood_normalized"),
                    "ethical_score": state.get("ethical_score"),
                    "soul_invariant": state.get("soul_invariant"),
                })
            except json.JSONDecodeError:
                pass
            last_line_seen = current_last

        # 2. Core state drift
        state = _read_json(STATE_PATH)
        gravity = _read_gravity()
        merged = {**state, **gravity}
        for key, threshold in _THRESHOLDS.items():
            if key not in merged:
                continue
            prev = last_metrics.get(key)
            cur = merged[key]
            if prev is not None and abs(cur - prev) >= threshold:
                print(f"[state] {key}: {prev:.4f} -> {cur:.4f} (Δ{cur - prev:+.4f})")
                _audit("state_drift", {"metric": key, "prev": prev, "cur": cur, "delta": cur - prev})
        last_metrics = merged

        # 3. Per-channel (M0-M11) SUSTAINED low coherence (not single-poll jitter)
        live = _read_portal_live()
        channels = live.get("channel_coh", {})
        for name, val in channels.items():
            if val < _CHANNEL_HEALTH_FLOOR:
                low_streak[name] = low_streak.get(name, 0) + 1
            else:
                if name in reported_stuck:
                    print(f"[channel] {name} recovered: now {val:.3f} (was stuck low)")
                    _audit("channel_recovered", {"channel": name, "cur": val})
                low_streak[name] = 0
                reported_stuck.discard(name)

            if low_streak.get(name, 0) >= _SUSTAINED_POLLS and name not in reported_stuck:
                print(f"[channel] {name} STUCK LOW: {val:.3f} for {low_streak[name]} consecutive polls")
                _audit("channel_stuck_low", {"channel": name, "cur": val, "consecutive_polls": low_streak[name]})
                reported_stuck.add(name)

        time.sleep(args.interval)


if __name__ == "__main__":
    main()
