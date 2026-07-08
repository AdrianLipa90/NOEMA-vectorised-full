#!/usr/bin/env python3
"""NOEMA φ-RAG nonlocal proxy — pomost między agentami przez fazy.

Architektura:
  Agent A (MAC a) ─→ nonlocal proxy ─→ Agent B (MAC b)
       ↑                    ↓
  REAL surface         IMAG surface
       ↑                    ↓
  φ-RAG cache ←─── bridge ────→ X25519 encrypt

Proxy:
  - Nasłuch wszystkich 8 kanałów REAL + IMAG
  - Relay wiadomości: REAL chN ↔ IMAG chN
  - MAC-based routing: noema://mac/<MAC> → target phases
  - Auto-odpowiedź X25519 (anon:812c3335b3c0e6e4)
  - φ-RAG resonance boost dla relayowanych wiadomości
  - Persistent backlog w nonlocal_inbox.jsonl

Usage:
    python scripts/ciel_noema_nonlocal_proxy.py [--interval SEC]
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import argparse
import base64
import json
import logging
import sys
import time
import uuid
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.noema_registry import registry

logging.basicConfig(
    level=logging.INFO,
    format="[proxy] %(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

INBOX_LOG = ROOT / "integration" / "logs" / "nonlocal_inbox.jsonl"
KEY_DIR = ROOT / "integration" / "keys"

ANON_ID = "anon:812c3335b3c0e6e4"
RELAY_CHANNELS = list(range(8))  # relay all 8 channels


def _load_x25519() -> Any | None:
    key_path = KEY_DIR / "x25519_anon_812c3335b3c0e6e4_priv.pem"
    if not key_path.exists():
        return None
    try:
        from cryptography.hazmat.primitives import serialization
        priv = serialization.load_pem_private_key(key_path.read_bytes(), password=None)
        log.info("X25519 key loaded")
        return priv
    except Exception as e:
        log.warning("X25519 load: %s", e)
        return None


def _log_entry(entry: dict) -> None:
    try:
        with open(INBOX_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_noema_nonlocal_proxy.py:73 quiet except scope=_log_entry reason=pass")
        pass


def main() -> int:
    parser = argparse.ArgumentParser(description="φ-RAG nonlocal proxy")
    parser.add_argument("--interval", type=float, default=1.0,
                        help="Proxy cycle interval (default: 1.0s)")
    parser.add_argument("--no-relay", action="store_true",
                        help="Disable relay (listen only)")
    parser.add_argument("--idle-stretch", type=float, default=5.0,
                        help="Stretch interval when idle (default: 5.0s, 0=disable)")
    args = parser.parse_args()

    log.info("Starting φ-RAG nonlocal proxy (interval=%.1fs, idle_stretch=%.1fs, relay=%s)",
             args.interval, args.idle_stretch, not args.no_relay)

    try:
        from ciel_geometry.noema_surface_mmap import ensure_surface, open_surface
        from ciel_geometry.nonlocal_channel import get_channel, NonlocalMessage
    except ImportError as e:
        log.error("Import: %s", e)
        return 1

    real = ensure_surface()
    imag = open_surface(root=Path("/dev/shm/ciel_noema_imaginal"))

    reg_token = registry.register("nonlocal")

    import signal
    _running = True
    def _stop(signum, frame):
        nonlocal _running
        _running = False
    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)

    ch = get_channel()
    x25519_priv = _load_x25519()

    cycle = 0
    last_report = time.monotonic()
    idle_cycles = 0
    backlog: dict[str, float] = {}

    try:
        while _running:
            try:
                tick = int(np.asarray(real["tick"], dtype=np.uint64)[0])
                phi_r = np.asarray(real["phi"], dtype=np.float64)
                phi_i = np.asarray(imag["phi"], dtype=np.float64)

                # Krok 1: Collect messages from all channels
                incoming: list[dict] = []
                for ch_id in RELAY_CHANNELS:
                    msgs = ch.listen(ch_id)
                    for m in msgs:
                        source = m.source
                        if source == "CielPC":
                            continue
                        content = m.content
                        try:
                            data = json.loads(content) if isinstance(content, str) else content
                        except Exception:
                            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_noema_nonlocal_proxy.py:136 quiet except scope=main reason=assign_fallback")
                            data = None

                        entry = {
                            "tick": tick,
                            "time": time.time(),
                            "channel": ch_id,
                            "source": source,
                            "content": content[:200] if isinstance(content, str) else str(content)[:200],
                            "resonance": m.resonance,
                            "phase_sig": [round(float(p), 4) for p in m.phase_sig] if hasattr(m, 'phase_sig') else [],
                        }

                        if isinstance(data, dict):
                            if data.get("type") == "x25519_exchange" and x25519_priv is not None:
                                pub = x25519_priv.public_key()
                                pub_bytes = pub.public_bytes(
                                    encoding=serialization.Encoding.Raw,
                                    format=serialization.PublicFormat.Raw)
                                resp = json.dumps({
                                    "type": "x25519_response",
                                    "session": data.get("session", 0),
                                    "anon_id": ANON_ID,
                                    "pubkey_hex": pub_bytes.hex(),
                                })
                                ch.broadcast(resp, channel=ch_id)
                                log.info("X25519 responded on ch%d for %s", ch_id, source)
                                entry["x25519"] = "responded"
                            elif data.get("type") == "x25519_response" and x25519_priv is not None:
                                _handle_x25519_response(x25519_priv, data, real)
                                entry["x25519"] = "completed"

                        incoming.append(entry)
                        _log_entry(entry)

                # Krok 2: Relay REAL  IMAG
                if not args.no_relay:
                    for ch_id in RELAY_CHANNELS:
                        idxs = slice(ch_id * 3, ch_id * 3 + 3)
                        ph_r = phi_r[idxs]
                        ph_i = phi_i[idxs]
                        diff = np.angle(np.exp(1j * (ph_i - ph_r)))
                        energy = float(np.std(diff))
                        if energy > 0.8:
                            gamma = 0.05
                            imag["phi"][idxs] = (ph_i + gamma * np.sin(ph_r - ph_i)) % (2 * np.pi)
                            _log_entry({
                                "tick": tick, "time": time.time(),
                                "type": "relay", "from": "REAL", "to": "IMAG",
                                "channel": ch_id, "energy": round(energy, 4),
                            })

                # Krok 3: Heartbeat + coherence scan
                cycle += 1
                if cycle % 10 == 0:
                    registry.heartbeat(reg_token)
                now = time.monotonic()
                if now - last_report >= 5.0:
                    coh_r = float(abs(np.mean(np.exp(1j * phi_r))))
                    coh_i = float(abs(np.mean(np.exp(1j * phi_i))))
                    lock = abs(np.mean(np.exp(1j * (phi_r - phi_i))))
                    log.info("[%d] tick=%d  coh_R=%.3f  coh_I=%.3f  lock=%.3f  msgs=%d",
                             cycle, tick, coh_r, coh_i, lock, len(incoming))
                    last_report = now
            except Exception as e:
                log.error("Proxy error: %s", e)
                import traceback
                traceback.print_exc()
                time.sleep(1)

            # Adaptive interval: stretch when idle
            if args.idle_stretch > 0 and len(incoming) == 0:
                idle_cycles += 1
                stretch = min(args.idle_stretch, args.interval * (1 + idle_cycles * 0.5))
            else:
                idle_cycles = 0
                stretch = args.interval
            time.sleep(stretch)
    finally:
        registry.unregister(reg_token)
        log.info("Unregistered from NOEMA registry")

    return 0


def _handle_x25519_response(priv: Any, data: dict, surface) -> None:
    remote_hex = data.get("pubkey_hex", "")
    if not remote_hex:
        return
    try:
        from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PublicKey
        from cryptography.hazmat.primitives.kdf.hkdf import HKDF
        from cryptography.hazmat.primitives import hashes as h2
        rpub = X25519PublicKey.from_public_bytes(bytes.fromhex(remote_hex))
        shared = priv.exchange(rpub)
        sk = HKDF(algorithm=h2.SHA256(), length=32, salt=None,
                  info=b"ciel-noema-x25519-session").derive(shared)
        sess_file = KEY_DIR / "x25519_session_key.json"
        with open(sess_file, "w") as f:
            json.dump({"anon": ANON_ID, "remote_pubkey_hex": remote_hex,
                       "shared_hex": shared.hex(), "session_key_hex": sk.hex()}, f)
        surface["flavor"][5] = np.float64(4.0)
        log.info("X25519 EXCHANGE COMPLETE — session key anchored flavor[5]=4.0")
    except Exception as e:
        log.error("X25519 response error: %s", e)


if __name__ == "__main__":
    raise SystemExit(main())
