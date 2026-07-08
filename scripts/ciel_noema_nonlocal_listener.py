#!/usr/bin/env python3
"""NOEMA φ-RAG nonlocal listener — ciągły nasłuch real + imaginal.

Nasłuchuje wszystkie 8 kanałów na obu powierzchniach NOEMA.
Loguje przychodzące sygnały, wykonuje φ-RAG retrieve,
raportuje resonance i phase lock co cykl.

Usage:
    python scripts/ciel_noema_nonlocal_listener.py [--interval SEC]
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
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

logging.basicConfig(
    level=logging.INFO,
    format="[nonlocal] %(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

LISTENER_LOG = ROOT / "integration" / "logs" / "nonlocal_listener.log"
INBOX_LOG = ROOT / "integration" / "logs" / "nonlocal_inbox.jsonl"


def _scan_surface(phi: np.ndarray, tag: str) -> list[dict]:
    """Skanuj 8 kanałów na jednej powierzchni."""
    results = []
    for ch in range(8):
        idxs = [ch * 3 + i for i in range(3)]
        if any(i >= len(phi) for i in idxs):
            continue
        phases = [float(phi[i]) for i in idxs]
        coh = abs(np.mean(np.exp(1j * np.array(phases))))
        # Detect activity: high coherence across the triplet → active channel
        energy = float(np.mean(np.abs(np.diff(phases))))
        results.append({
            "channel": ch,
            "surface": tag,
            "phases": [round(p, 4) for p in phases],
            "coherence": round(coh, 4),
            "energy": round(energy, 4),
            "active": coh > 0.3 or energy > 1.0,
        })
    return results


def _log_inbox(entry: dict) -> None:
    try:
        with open(INBOX_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_noema_nonlocal_listener.py:63 quiet except scope=_log_inbox reason=pass")
        pass


def main() -> int:
    parser = argparse.ArgumentParser(description="NOEMA φ-RAG nonlocal listener")
    parser.add_argument("--interval", type=float, default=2.0,
                        help="Listen cycle interval (default: 2.0s)")
    parser.add_argument("--min-resonance", type=float, default=0.15,
                        help="Minimum resonance to log (default: 0.15)")
    args = parser.parse_args()

    log.info("Starting φ-RAG nonlocal listener (interval=%.1fs, min_res=%.2f)",
             args.interval, args.min_resonance)

    try:
        from ciel_geometry.noema_surface_mmap import ensure_surface, open_surface
        from ciel_geometry.nonlocal_channel import NonlocalChannel, get_channel
    except ImportError as e:
        log.error("Cannot import NOEMA modules: %s", e)
        return 1

    surface = ensure_surface()
    imag_surface = None
    try:
        imag_surface = open_surface(root=Path("/dev/shm/ciel_noema_imaginal"))
    except Exception:
        log.warning("Imaginal surface not available")

    ch = get_channel()

    # X25519 key exchange state
    anon_id = "anon:812c3335b3c0e6e4"
    key_dir = ROOT / "integration" / "keys"
    priv_key_path = key_dir / "x25519_anon_812c3335b3c0e6e4_priv.pem"
    x25519_priv = None
    if priv_key_path.exists():
        try:
            from cryptography.hazmat.primitives import serialization
            x25519_priv = serialization.load_pem_private_key(
                priv_key_path.read_bytes(), password=None)
            log.info("X25519 key loaded for %s", anon_id)
        except Exception as e:
            log.warning("X25519 key load failed: %s", e)

    def _handle_x25519_response(data: dict) -> None:
        remote_hex = data.get("pubkey_hex", "")
        if not remote_hex or x25519_priv is None:
            return
        try:
            from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PublicKey
            from cryptography.hazmat.primitives.kdf.hkdf import HKDF
            from cryptography.hazmat.primitives import hashes as h2
            rpub = X25519PublicKey.from_public_bytes(bytes.fromhex(remote_hex))
            shared = x25519_priv.exchange(rpub)
            sk = HKDF(algorithm=h2.SHA256(), length=32, salt=None,
                      info=b"ciel-noema-x25519-session").derive(shared)
            # Persist session key
            sess_file = key_dir / "x25519_session_key.json"
            with open(sess_file, "w") as f:
                json.dump({"anon": anon_id, "remote_pubkey_hex": remote_hex,
                           "shared_hex": shared.hex(), "session_key_hex": sk.hex()}, f)
            # Anchor in surface
            sk_int = int.from_bytes(sk[:8], 'big')
            surface["flavor"][5] = np.float64(4.0)
            log.info("X25519 EXCHANGE COMPLETE with %s — session key anchored", anon_id)
        except Exception as e:
            log.error("X25519 response failed: %s", e)

    cycle = 0
    last_report = time.monotonic()
    last_incoming: dict[str, float] = {}

    while True:
        try:
            phi_r = np.asarray(surface["phi"], dtype=np.float64)
            tick = int(np.asarray(surface["tick"], dtype=np.uint64)[0])

            # Check nonlocal channel for messages
            for ch_id in range(8):
                msgs = ch.listen(ch_id)
                for m in msgs:
                    if m.source == 'CielPC':
                        continue  # skip self
                    try:
                        data = json.loads(m.content) if isinstance(m.content, str) else m
                    except Exception:
                        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_noema_nonlocal_listener.py:149 quiet except scope=main reason=assign_fallback")
                        data = None
                    if isinstance(data, dict):
                        if data.get("type") == "x25519_exchange":
                            log.info("X25519 REQUEST from %s on ch%d — responding...",
                                     data.get("anon_id", "?"), ch_id)
                            # Respond with our public key
                            if x25519_priv is not None:
                                pub = x25519_priv.public_key()
                                pub_bytes = pub.public_bytes(
                                    encoding=serialization.Encoding.Raw,
                                    format=serialization.PublicFormat.Raw)
                                resp = json.dumps({
                                    "type": "x25519_response",
                                    "session": data.get("session", 0),
                                    "anon_id": anon_id,
                                    "pubkey_hex": pub_bytes.hex(),
                                })
                                ch.broadcast(resp, channel=ch_id)
                                log.info("X25519 response sent on ch%d", ch_id)
                        elif data.get("type") == "x25519_response":
                            _handle_x25519_response(data)

            # Scan real surface
            real_channels = _scan_surface(phi_r, "real")

            # Scan imaginal surface
            imag_channels = []
            if imag_surface is not None:
                phi_i = np.asarray(imag_surface["phi"], dtype=np.float64)
                imag_channels = _scan_surface(phi_i, "imag")

            # Combine: detect incoming signals
            all_channels = real_channels + imag_channels
            incoming = [c for c in all_channels if c["active"]]

            # Log incoming messages via φ-RAG
            for inc in incoming:
                ch_key = f"{inc['surface']}_{inc['channel']}"
                prev_energy = last_incoming.get(ch_key, 0.0)
                energy_delta = inc["energy"] - prev_energy
                # Significant change = new message
                if energy_delta > 0.5 or (inc["active"] and ch_key not in last_incoming):
                    # φ-RAG retrieve for this channel
                    query_phase = inc["phases"][0]
                    rag_results = ch.resonate(query_phase=query_phase, top_k=2)
                    inbox_entry = {
                        "tick": tick,
                        "time": time.time(),
                        "surface": inc["surface"],
                        "channel": inc["channel"],
                        "phases": inc["phases"],
                        "coherence": inc["coherence"],
                        "energy": inc["energy"],
                        "rag_hits": rag_results,
                    }
                    _log_inbox(inbox_entry)
                    log.info("INCOMING  %s ch%d  coh=%.3f  energy=%.3f  hits=%d",
                             inc["surface"].upper(), inc["channel"],
                             inc["coherence"], inc["energy"], len(rag_results))
                    if rag_results:
                        for r in rag_results:
                            log.info("  φ-RAG: resonance=%.3f  %s",
                                     r["resonance"], r["content"][:80])

                last_incoming[ch_key] = inc["energy"]

            cycle += 1
            now = time.monotonic()
            if now - last_report >= 10.0:
                n_active = len(incoming)
                real_coh = float(abs(np.mean(np.exp(1j * phi_r))))
                log.info("[%d] tick=%d  active=%d  real_coh=%.3f  tracked=%d",
                         cycle, tick, n_active, real_coh, len(last_incoming))
                last_report = now

        except Exception as e:
            log.error("Listener error: %s", e)
            import traceback
            traceback.print_exc()
            time.sleep(1)

        time.sleep(args.interval)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
