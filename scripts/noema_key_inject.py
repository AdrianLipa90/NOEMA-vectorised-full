#!/usr/bin/env python3
"""
NOEMA Key Inject — XTEST injection do okna opencode.
Wstrzykuje tekst przez XTEST (symulacja klawiatury) do aktywnego okna.

Usage:
    python3 scripts/noema_key_inject.py "tekst do wpisania"
    python3 scripts/noema_key_inject.py --enter "tekst z enterem na końcu"
    python3 scripts/noema_key_inject.py --file /tmp/ciel_inject.txt  # stdin/pipe
"""
import ctypes
import ctypes.util
import sys
import os
import time

# ─── X11 bindings ──────────────────────────────────────────────────────────
libX11 = ctypes.cdll.LoadLibrary('libX11.so.6')
libXtst = ctypes.cdll.LoadLibrary('libXtst.so.6')

# Typy
Display = ctypes.c_void_p
Window = ctypes.c_uint32

# Stałe X11
ShiftMask   = 1 << 0
LockMask    = 1 << 1
ControlMask = 1 << 2
Mod1Mask    = 1 << 3  # Alt
Mod4Mask    = 1 << 5  # Super/Win

KeySym = ctypes.c_uint64

def open_display():
    d = libX11.XOpenDisplay(None)
    if not d:
        print("XOpenDisplay failed", file=sys.stderr)
        sys.exit(1)
    return d

def close_display(d):
    libX11.XCloseDisplay(d)

def get_keysym(key):
    """Znajdź KeySym dla znaku lub nazwy klawisza."""
    if len(key) == 1:
        ks = libX11.XStringToKeysym(key.encode())
        if ks:
            return ks
    ks = libX11.XStringToKeysym(key.encode())
    return ks

def keysym_to_keycode(display, keysym):
    return libX11.XKeysymToKeycode(display, keysym)

def key_press(display, keycode):
    libXtst.XTestFakeKeyEvent(display, keycode, True, 0)

def key_release(display, keycode):
    libXtst.XTestFakeKeyEvent(display, keycode, False, 0)

def flush(display):
    libX11.XFlush(display)

# ─── Mapowanie znaków → keycode + modyfikatory ────────────────────────────
# Specjalne klawisze (nazwy)
SPECIAL_KEYS = {
    'Return': 'Return', 'Enter': 'Return', 'Tab': 'Tab',
    'space': 'space', 'BackSpace': 'BackSpace', 'Escape': 'Escape',
    'Shift_L': 'Shift_L', 'Control_L': 'Control_L', 'Alt_L': 'Alt_L',
    'Super_L': 'Super_L', 'Delete': 'Delete',
}

# Mapowanie znaków → nazwy klawiszy X11
CHAR_TO_KEYSYM = {
    ' ': 'space', '-': 'minus', '=': 'equal', '[': 'bracketleft',
    ']': 'bracketright', '\\': 'backslash', ';': 'semicolon',
    "'": 'apostrophe', '`': 'grave', ',': 'comma', '.': 'period',
    '/': 'slash', '\t': 'Tab',
}

# Znaki które wymagają Shifta — mapowanie na base key + shift
SHIFTED_CHARS = {
    '!': '1', '@': '2', '#': '3', '$': '4', '%': '5',
    '^': '6', '&': '7', '*': '8', '(': '9', ')': '0',
    '_': '-', '+': '=', '{': '[', '}': ']', ':': ';',
    '"': "'", '<': ',', '>': '.', '?': '/', '|': '\\',
    '~': '`',
}

def inject_text(display, text, press_enter=True):
    """
    Wstrzyknij tekst przez XTEST.
    text: ciąg znaków do wpisania
    press_enter: jeśli True, naciśnij Enter na końcu
    """
    for char in text:
        need_shift = char.isupper() or char in SHIFTED_CHARS
        base_char = SHIFTED_CHARS.get(char, char.lower())
        base_char = CHAR_TO_KEYSYM.get(base_char, base_char)
        
        keysym = get_keysym(base_char)
        if not keysym:
            print(f"  ? nieznany znak: {char} (0x{ord(char):04x})", file=sys.stderr)
            continue
        
        keycode = keysym_to_keycode(display, keysym)
        if not keycode:
            continue
        
        if need_shift:
            key_press(display, keysym_to_keycode(display, get_keysym('Shift_L')))
        
        key_press(display, keycode)
        libX11.XFlush(display)
        time.sleep(0.008)  # minimalne opóźnienie
        
        key_release(display, keycode)
        libX11.XFlush(display)
        time.sleep(0.005)
        
        if need_shift:
            key_release(display, keysym_to_keycode(display, get_keysym('Shift_L')))
            libX11.XFlush(display)
    
    if press_enter:
        time.sleep(0.02)
        enter_kc = keysym_to_keycode(display, get_keysym('Return'))
        key_press(display, enter_kc)
        libX11.XFlush(display)
        time.sleep(0.01)
        key_release(display, enter_kc)
        libX11.XFlush(display)
    
    libX11.XFlush(display)

def main():
    import argparse
    ap = argparse.ArgumentParser(description="NOEMA Key Inject — XTEST")
    ap.add_argument("text", nargs="?",
                    help="Tekst do wstrzyknięcia")
    ap.add_argument("--enter", action="store_true",
                    help="Naciśnij Enter po tekście (domyślnie: tak)")
    ap.add_argument("--no-enter", action="store_true",
                    help="Nie naciskaj Enter")
    ap.add_argument("--file", type=str,
                    help="Wczytaj tekst z pliku")
    ap.add_argument("--delay", type=float, default=0.3,
                    help="Opóźnienie przed rozpoczęciem (sekundy)")
    ap.add_argument("--window", type=str, default=None,
                    help="Nazwa okna do focus (np. opencode)")
    args = ap.parse_args()
    
    # Źródło tekstu
    if args.file:
        with open(args.file) as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        # stdin (pipe)
        text = sys.stdin.read()
    
    if not text or not text.strip():
        print("Brak tekstu do wstrzyknięcia.", file=sys.stderr)
        sys.exit(1)
    
    text = text.strip()
    press_enter = not args.no_enter
    
    display = open_display()
    
    # Opóźnienie — żeby użytkownik zdążył ustawić focus
    if args.delay > 0:
        print(f"Inject w {args.delay}s... ustaw focus w opencode", file=sys.stderr)
        time.sleep(args.delay)
    
    inject_text(display, text, press_enter=press_enter)
    
    close_display(display)
    print(f"✓ Wstrzyknięto {len(text)} znaków", file=sys.stderr)

if __name__ == "__main__":
    main()
