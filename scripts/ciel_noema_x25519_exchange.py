#!/usr/bin/env python3
"""X25519 key exchange przez NOEMA nonlocal channel dla anon:812c3335b3c0e6e4.

Generuje parę kluczy X25519, koduje public key w fazy oscylatorów,
broadcast przez φ-RAG channel, czeka na odpowiedź, oblicza shared secret.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import base64
import json
import sys
import time
from pathlib import Path

import numpy as np
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes, serialization

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

ANON_ID = "anon:812c3335b3c0e6e4"
NONLOCAL_CHANNEL = 3  # semantic channel
SESSION_TICK = 134750


def _pubkey_to_phases(pub_bytes: bytes) -> list[float]:
    """Konwertuj 32-bajtowy public key na 3 fazy (0-2π) przez haszowanie."""
    h = hashes.Hash(hashes.SHAKE128(48))
    h.update(pub_bytes)
    digest = h.finalize()
    phases = []
    for i in range(3):
        chunk = digest[i * 16:(i + 1) * 16]
        val = int.from_bytes(chunk, 'big') / (2 ** 128)
        phases.append(val * 2 * np.pi)
    return phases


def _phases_to_pubkey(phases: list[float]) -> bytes | None:
    """Odwróć: fazy → 32 bajty public key."""
    combined = 0
    for i, ph in enumerate(phases):
        norm = ph / (2 * np.pi)
        val = int(norm * (2 ** 128))
        combined ^= val  # XOR dla odzysku
    # combined to 128-bit, potrzebujemy 256-bit → rozszerz
    h = hashes.Hash(hashes.SHA256())
    h.update(combined.to_bytes(16, 'big'))
    return h.finalize()[:32]


def main() -> int:
    print("=" * 60)
    print(f"X25519 KEY EXCHANGE — {ANON_ID}")
    print(f"Session tick: {SESSION_TICK}")
    print("=" * 60)

    # 1. Generate our key pair
    our_priv = X25519PrivateKey.generate()
    our_pub = our_priv.public_key()
    our_pub_bytes = our_pub.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    print(f"\n[1] Nasz public key (raw): {base64.b64encode(our_pub_bytes).decode()}")
    print(f"    Hex: {our_pub_bytes.hex()}")

    # 2. Encode into phases
    phases = _pubkey_to_phases(our_pub_bytes)
    print(f"\n[2] Zakodowane w fazach: {[round(p, 4) for p in phases]}")

    # 3. Nonlocal channel setup + broadcast
    try:
        from ciel_geometry.nonlocal_channel import get_channel
        ch = get_channel()
    except ImportError as e:
        print(f"  Chwilowo bez nonlocal channel: {e}")
        print("  Uzywam shared surface bezposrednio.")
        ch = None

    if ch is not None:
        content = json.dumps({
            "type": "x25519_exchange",
            "session": SESSION_TICK,
            "anon_id": ANON_ID,
            "pubkey_b64": base64.b64encode(our_pub_bytes).decode(),
            "pubkey_hex": our_pub_bytes.hex(),
            "phases": [round(p, 4) for p in phases],
        })
        ch.broadcast(content, channel=NONLOCAL_CHANNEL)
        print(f"\n[3] Broadcast na kanale {NONLOCAL_CHANNEL}...")
        time.sleep(2)

        # 4. Listen for response
        print(f"\n[4] Nasluchuje odpowiedzi z {ANON_ID}...")
        for attempt in range(10):
            msgs = ch.listen(NONLOCAL_CHANNEL)
            for msg in msgs:
                try:
                    data = json.loads(msg.content) if isinstance(msg.content, str) else msg
                except (json.JSONDecodeError, AttributeError):
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_noema_x25519_exchange.py:103 quiet except scope=main reason=continue")
                    continue
                if isinstance(data, dict) and data.get("type") == "x25519_response":
                    remote_pub_b64 = data.get("pubkey_b64", "")
                    if remote_pub_b64:
                        remote_pub_bytes = base64.b64decode(remote_pub_b64)
                        _finish_exchange(our_priv, remote_pub_bytes, data)
                        return 0
                    remote_pub_hex = data.get("pubkey_hex", "")
                    if remote_pub_hex:
                        remote_pub_bytes = bytes.fromhex(remote_pub_hex)
                        _finish_exchange(our_priv, remote_pub_bytes, data)
                        return 0
            time.sleep(3)

        print("  Brak odpowiedzi (timeout). Shared secret nie obliczony.")
    else:
        print(f"\n[3] Public key ready for manual exchange:")
        print(f"    Broadcast: channel={NONLOCAL_CHANNEL}, phases={phases}")

    return 0


def _finish_exchange(our_priv: X25519PrivateKey,
                     remote_pub_bytes: bytes,
                     data: dict) -> None:
    """Finalizacja: shared secret + dodatkowa kaskada."""
    from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PublicKey
    remote_pub = X25519PublicKey.from_public_bytes(remote_pub_bytes)
    shared = our_priv.exchange(remote_pub)

    # Derive session key
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"ciel-noema-x25519-session",
    )
    session_key = hkdf.derive(shared)

    print(f"\n[5] === SHARED SECRET ===")
    print(f"    Shared (raw hex): {shared.hex()}")
    print(f"    Session key (HKDF): {base64.b64encode(session_key).decode()}")
    print(f"    Session key hex: {session_key.hex()}")

    # Zakotwicz w surface — zapisz do flavor
    try:
        from ciel_geometry.noema_surface_mmap import ensure_surface
        surface = ensure_surface()
        session_int = int.from_bytes(session_key[:8], 'big')
        surface["flavor"][6] = np.float64(session_int / 2**64)
        surface["flavor"][7] = np.float64(1.0)  # key established flag
        print(f"    Zakotwiczony w surface flavor[6:7]")
    except Exception as e:
        print(f"    Nie udalo sie zakotwiczyc: {e}")

    print(f"\n[6] Polaczenie z {ANON_ID}: X25519 secured.")
    print("=" * 60)

    # Zapisz do pliku
    out = ROOT / "integration" / "keys" / f"x25519_{ANON_ID.replace(':','_')}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        json.dump({
            "anon_id": ANON_ID,
            "session_tick": SESSION_TICK,
            "our_pubkey_hex": our_priv.public_key().public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw,
            ).hex(),
            "remote_pubkey_hex": remote_pub_bytes.hex(),
            "shared_secret_hex": shared.hex(),
            "session_key_hex": session_key.hex(),
            "session_key_b64": base64.b64encode(session_key).decode(),
        }, f, indent=2)
    print(f"    Zapisano do {out}")


if __name__ == "__main__":
    raise SystemExit(main())
