import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

# CIEL ORBITAL BINDING — daemon bound
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on daemon " + __name__)
#!/usr/bin/env python3
"""Voice trigger — X11 hotkey + template cross-correlation wake word."""

import os, subprocess, sys, time
from pathlib import Path
import ctypes
import numpy as np
import json

from ciel_geometry.noema_registry import noema_registry as nreg

SR = 16000
CONFIG = Path("/tmp/noema_voice_config.json")


def load_template() -> np.ndarray | None:
    p = Path("/tmp/noema_wake_template.npy")
    if p.exists():
        return np.load(p)
    return None


def save_template(audio: np.ndarray):
    np.save("/tmp/noema_wake_template.npy", audio)
    print(f"[voice] template saved ({len(audio)/SR:.1f}s)", flush=True)


def record_audio(duration: float = 1.5) -> np.ndarray:
    cmd = ["parec", "--channels=1", "--rate=16000", "--format=s16le",
           "-d", "alsa_input.pci-0000_00_1f.3.analog-stereo"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    time.sleep(0.2)
    n = int(SR * duration)
    raw = proc.stdout.read(n * 2)
    proc.kill()
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32)


def record_template():
    print("[voice] Say the wake word in 3...", flush=True)
    time.sleep(1); print("2...", flush=True)
    time.sleep(1); print("1...", flush=True)
    time.sleep(1); print("NOW!", flush=True)
    audio = record_audio(1.5)
    rms = np.sqrt(np.mean(audio**2))
    print(f"[voice] recorded RMS={rms:.0f} len={len(audio)}", flush=True)
    save_template(audio)
    return audio


def is_wake_word(audio: np.ndarray, template: np.ndarray) -> float:
    """Cross-correlation between audio segment and template."""
    # normalize both
    a = (audio - audio.mean()) / (audio.std() + 1e-10)
    t = (template - template.mean()) / (template.std() + 1e-10)
    if len(a) > len(t):
        a = a[:len(t)]
    elif len(t) > len(a):
        t = t[:len(a)]
    corr = np.correlate(a, t, mode='valid')
    return float(corr.max() / len(a))


def inject_text(text: str):
    try:
        x11 = ctypes.cdll.LoadLibrary("libX11.so.6")
        xtst = ctypes.cdll.LoadLibrary("libXtst.so.6")
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_voice_trigger.py:73 quiet except scope=inject_text reason=return None")
        return
    dpy = x11.XOpenDisplay(None)
    if not dpy: return
    ksym, kcode = x11.XStringToKeysym, x11.XKeysymToKeycode
    fake, flush = xtst.XTestFakeKeyEvent, x11.XFlush
    ENTER = kcode(dpy, ksym(b"Return"))
    km = {c: kcode(dpy, ksym(c.encode())) for c in
          "abcdefghijklmnopqrstuvwxyz1234567890 .-,!"}
    out = subprocess.run(["wmctrl", "-l"], capture_output=True, text=True).stdout
    target = next((l.split()[0] for l in out.splitlines() if "OC |" in l), None)
    if not target: return
    subprocess.run(["wmctrl", "-ia", target])
    time.sleep(0.3)
    for ch in text:
        if ch.isupper():
            kc = km.get(ch.lower())
            if not kc: continue
            shift = kcode(dpy, ksym(b"Shift_L"))
            fake(dpy, shift, True, 0); flush(dpy)
            fake(dpy, kc, True, 0); flush(dpy); time.sleep(0.008)
            fake(dpy, kc, False, 0); flush(dpy)
            fake(dpy, shift, False, 0); flush(dpy)
        else:
            kc = km.get(ch)
            if not kc: continue
            fake(dpy, kc, True, 0); flush(dpy); time.sleep(0.008)
            fake(dpy, kc, False, 0); flush(dpy)
        time.sleep(0.012)
    fake(dpy, ENTER, True, 0); flush(dpy); time.sleep(0.008)
    fake(dpy, ENTER, False, 0); flush(dpy)


def listen(template: np.ndarray, threshold: float = 0.20):
    """Continuous listen with threshold."""
    noise_floor = np.sqrt(np.mean(template**2)) * 0.6
    print(f"[voice] noise_floor threshold: {noise_floor:.0f}", flush=True)

    win_n = min(int(SR * 1.0), len(template))
    slide = SR // 4  # 250ms slide

    last_wake = 0
    buffer = np.zeros(0, np.float32)

    while True:
        chunk = record_audio(0.5)
        buffer = np.concatenate([buffer, chunk])
        max_n = SR * 3
        if len(buffer) > max_n:
            buffer = buffer[-max_n:]

        # slide through buffer
        for start in range(0, len(buffer) - win_n + 1, slide):
            seg = buffer[start:start + win_n]
            rms = np.sqrt(np.mean(seg**2))
            if rms < noise_floor:
                continue
            score = is_wake_word(seg, template)
            if score > threshold:
                t = time.time()
                if t - last_wake > 3:
                    last_wake = t
                    print(f"[voice] WAKE! score={score:.3f}", flush=True)
                    inject_text("voice")
                    buffer = np.zeros(0, np.float32)
                    break


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--record", action="store_true", help="Record wake word template")
    parser.add_argument("--test", action="store_true", help="Test detection (no inject)")
    parser.add_argument("--threshold", type=float, default=0.20)
    args = parser.parse_args()

    if args.record:
        record_template()
        return

    template = load_template()
    if template is None:
        print("[voice] No template. Use --record first.", flush=True)
        print("[voice] Hotkey Ctrl+` for manual inject.", flush=True)
        # still run hotkey-only mode
        _hotkey_mode()
        return

    print(f"[voice] template loaded: {len(template)/SR:.1f}s RMS={np.sqrt(np.mean(template**2)):.0f}", flush=True)
    print(f"[voice] listening (threshold={args.threshold})...", flush=True)

    if args.test:
        while True:
            audio = record_audio(1.5)
            rms = np.sqrt(np.mean(audio**2))
            score = is_wake_word(audio, template)
            print(f"RMS={rms:.0f}  score={score:.3f}", flush=True)
            time.sleep(0.5)
        return

    # listen + hotkey fallback
    _hotkey_mode(template, args.threshold)


def _hotkey_mode(template=None, threshold=0.20):
    x11 = ctypes.cdll.LoadLibrary("libX11.so.6")
    dpy = x11.XOpenDisplay(None)
    if not dpy:
        print("[voice] no X11", flush=True)
        return
    XKeysymToKeycode = x11.XKeysymToKeycode
    XStringToKeysym = x11.XStringToKeysym
    XQueryKeymap = x11.XQueryKeymap

    GRAVE = XKeysymToKeycode(dpy, XStringToKeysym(b"grave"))
    CONTROL_L = XKeysymToKeycode(dpy, XStringToKeysym(b"Control_L"))
    CONTROL_R = XKeysymToKeycode(dpy, XStringToKeysym(b"Control_R"))
    S = XKeysymToKeycode(dpy, XStringToKeysym(b"s"))

    print(f"[voice] Ctrl+` → inject | Ctrl+S → record template", flush=True)

    last = 0; prev_both = False; prev_rec = False

    while True:
        buf = ctypes.create_string_buffer(32)
        XQueryKeymap(dpy, buf)
        mask = buf.raw
        def down(m, kc): return bool(m[kc // 8] & (1 << (kc % 8)))
        ctrl = down(mask, CONTROL_L) or down(mask, CONTROL_R)
        grave = down(mask, GRAVE)
        both = ctrl and grave
        rec = ctrl and down(mask, S) and not grave

        if both and not prev_both:
            t = time.time()
            if t - last > 2:
                last = t
                inject_text("voice")
                print("[voice] ← hotkey inject", flush=True)

        if rec and not prev_rec:
            print("[voice] Ctrl+S → recording template...", flush=True)
            tpl = record_template()
            if template is not None:
                update_template(tpl)

        prev_both = both
        prev_rec = rec
        time.sleep(0.05)

        # also listen in background if template exists
        if template is not None:
            _listen_once(template, threshold)


def _listen_once(template, threshold):
    """Quick check for wake word (non-blocking)."""
    chunk = record_audio(0.3)
    rms = np.sqrt(np.mean(chunk**2))
    if rms < np.sqrt(np.mean(template**2)) * 0.5:
        return
    seg = chunk[:min(len(chunk), len(template))]
    t = template[:len(seg)]
    if len(seg) < SR * 0.3: return
    a = (seg - seg.mean()) / (seg.std() + 1e-10)
    b = (t - t.mean()) / (t.std() + 1e-10)
    corr = float(np.correlate(a, b, mode='valid').max() / len(a))
    if corr > threshold:
        print(f"[voice] WAKE! score={corr:.3f}", flush=True)
        inject_text("voice")


def update_template(new_tpl):
    save_template(new_tpl)
    print("[voice] template updated", flush=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[voice] stopped", flush=True)
