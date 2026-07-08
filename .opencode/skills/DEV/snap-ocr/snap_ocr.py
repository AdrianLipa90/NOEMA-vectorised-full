#!/usr/bin/env python3
"""snap-ocr: screenshot → OCR → MemoryPalace → surface."""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

WORK_DIR = Path("/tmp/snap-ocr")

# ── screenshot ─────────────────────────────────────────────────────────

def shoot(work_dir: Path) -> Path:
    from PIL import ImageGrab
    work_dir.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    path = work_dir / f"snap_{ts}.png"
    im = ImageGrab.grab()
    im.save(str(path))
    return path

# ── OCR ────────────────────────────────────────────────────────────────

def ocr(image_path: Path, work_dir: Path, lang: str = "pol+eng") -> str:
    base = work_dir / image_path.stem
    txt_path = work_dir / f"{image_path.stem}.txt"
    subprocess.run(
        ["tesseract", str(image_path), str(base), "-l", lang],
        capture_output=True, timeout=60,
    )
    if txt_path.exists():
        return txt_path.read_text(encoding="utf-8", errors="replace")
    return ""

# ── analiza przez agent-backend ────────────────────────────────────────

def analyze(text: str, query: str = "") -> dict:
    try:
        import requests
        prompt = f"extract themes, affect (VAD), anchor_terms, essence (1 zdanie), hunch from:\n{text[:3000]}"
        if query:
            prompt += f"\ncontext: {query}"
        r = requests.post("http://localhost:18520/chat/completions",
                          json={"messages": [{"role": "user",
                                              "content": prompt}]},
                          timeout=15)
        if r.status_code == 200:
            body = r.json()
            content = body.get("choices", [{}])[0].get("message", {}).get("content", "")
            if content:
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception(".opencode/skills/DEV/snap-ocr/snap_ocr.py:58 quiet except scope=analyze reason=return {\"raw\": content, \"affect\": \"unknown\"}")
                    return {"raw": content, "affect": "unknown"}
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception(".opencode/skills/DEV/snap-ocr/snap_ocr.py:60 quiet except scope=analyze reason=pass")
        pass
    return {"themes": [], "affect": "unknown", "essence": text[:200]}

# ── MemoryPalace ──────────────────────────────────────────────────────

def store(note: str, meta: dict) -> dict:
    try:
        sys.path.insert(0, str(Path(__file__).parents[3]))
        from ciel_geometry.memory_palace import MentalistMemoryPalace
        p = MentalistMemoryPalace()
        res = p.save_room_state(note, with_associations=True)
        return {"palace_id": res["associations"].get("palace_id"),
                "tick": res["associations"].get("tick")}
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception(".opencode/skills/DEV/snap-ocr/snap_ocr.py:74 quiet except scope=store reason=return {\"error\": str(e)}")
        return {"error": str(e)}

# ── Key inject ─────────────────────────────────────────────────────────

def inject(text: str):
    """Wstrzyknięcie tekstu do opencode przez XTEST."""
    try:
        import ctypes, ctypes.util
        _x11 = ctypes.cdll.LoadLibrary("libX11.so.6")
        _xtst = ctypes.cdll.LoadLibrary("libXtst.so.6")
        Display = ctypes.c_void_p
        dpy = _x11.XOpenDisplay(None)
        XTestFakeKeyEvent = _xtst.XTestFakeKeyEvent
        XTestFakeKeyEvent.argtypes = [Display, ctypes.c_uint, ctypes.c_bool, ctypes.c_ulong]
        XFlush = _x11.XFlush

        def keycode(sym):
            ks = _x11.XStringToKeysym(sym.encode())
            return _x11.XKeysymToKeycode(dpy, ks)

        def press(kc): XTestFakeKeyEvent(dpy, kc, True, 0); XFlush(dpy)
        def release(kc): XTestFakeKeyEvent(dpy, kc, False, 0); XFlush(dpy)
        def tap(kc): press(kc); time.sleep(0.01); release(kc)

        SHIFT = keycode("Shift_L")
        ENTER = keycode("Return")
        km = {}
        for c in "abcdefghijklmnopqrstuvwxyz1234567890": km[c] = keycode(c)
        km[' '] = keycode("space"); km['.'] = keycode("period")
        km[','] = keycode("comma"); km['/'] = keycode("slash")
        km['-'] = keycode("minus"); km['_'] = keycode("underscore")
        km['='] = keycode("equal"); km['!'] = keycode("exclam")
        km['?'] = keycode("question")

        out = subprocess.run(["wmctrl", "-l"], capture_output=True, text=True).stdout
        target = None
        for line in out.splitlines():
            if "OC |" in line:
                target = line.split()[0]; break
        if not target:
            print("[snap] no opencode window for inject")
            return
        subprocess.run(["wmctrl", "-ia", target])
        time.sleep(0.4)

        for ch in text:
            if ch == '\n':
                tap(ENTER)
            elif ch.isupper():
                kc = km.get(ch.lower())
                if not kc: continue
                press(SHIFT); tap(kc); release(SHIFT)
            else:
                kc = km.get(ch)
                if not kc: continue
                tap(kc)
            time.sleep(0.02)
    except Exception as e:
        print(f"[snap] inject failed: {e}")

# ── CLI ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="snap-ocr")
    parser.add_argument("--dir", default=str(WORK_DIR))
    parser.add_argument("--ocr-only", action="store_true")
    parser.add_argument("--no-store", action="store_true")
    parser.add_argument("--inject", action="store_true", help="wstrzyknij wynik do opencode")
    parser.add_argument("--query", default="", help="kontekst")
    args = parser.parse_args()

    work_dir = Path(args.dir)
    img = shoot(work_dir)
    print(f"[snap] screenshot: {img}")

    text = ocr(img, work_dir)
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    summary = " | ".join(lines[:5])
    print(f"[snap] OCR: {len(lines)} linii")
    if lines:
        print(f"  → {summary[:120]}")

    if args.ocr_only:
        return

    analysis = analyze(text, args.query)
    affect = analysis.get("affect", "unknown")
    themes = analysis.get("themes", [])
    essence = analysis.get("essence", text[:300])
    hunch = analysis.get("hunch", "")
    print(f"[snap] affect={affect} themes={themes[:3]}")
    print(f"[snap] essence: {essence[:120]}")

    if not args.no_store:
        note = f"[snap-ocr] {essence[:200]}"
        if hunch:
            note += f" | hunch: {hunch[:200]}"
        result = store(note, analysis)
        pid = result.get("palace_id", "?")
        print(f"[snap] MemoryPalace snapshot #{pid}")

    if args.inject:
        themes_str = ", ".join(themes[:5]) if themes else "?"
        lines_preview = "\n".join(lines[:15])[:500]
        msg = (
            f"snap-ocr: {summary[:160]}\n"
            f"themes: {themes_str}\n"
            f"affect: {affect}\n"
            f"essence: {essence[:200]}\n"
            f"ocr ({len(lines)} linii):\n{lines_preview}"
        )
        print(f"[snap] injecting into opencode...")
        inject(msg + "\n")

    print("[snap] done")

if __name__ == "__main__":
    main()
