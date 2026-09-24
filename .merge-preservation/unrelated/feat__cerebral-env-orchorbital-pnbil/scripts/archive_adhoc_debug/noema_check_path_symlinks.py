#!/usr/bin/env python3
"""Sprawdz czy /home/admiral i /home/adrian to ta sama sciezka."""
import os
from pathlib import Path

paths = [
    "/home/adrian",
    "/home/admiral",
    "/home/adrian/noema",
    "/home/admiral/noema",
    "/home/adrian/noema/scripts/ciel_headless_daemon.py",
    "/home/admiral/noema/scripts/ciel_headless_daemon.py",
    "/home/adrian/noema/src/ciel_sot_agent/conversation_bridge.py",
    "/home/admiral/noema/src/ciel_sot_agent/conversation_bridge.py",
]

for p in paths:
    pp = Path(p)
    exists = pp.exists()
    is_link = pp.is_symlink()
    real = str(pp.resolve()) if exists else "N/A"
    print(f"{'[OK]' if exists else '[XX]'} {'->LINK' if is_link else '      '} {p}")
    if is_link:
        print(f"       target: {os.readlink(p)}")
    if exists and real != p:
        print(f"       real:   {real}")

print()
# Check inode numbers
d1 = Path("/home/adrian/noema/scripts/ciel_headless_daemon.py")
d2 = Path("/home/admiral/noema/scripts/ciel_headless_daemon.py")
if d1.exists() and d2.exists():
    s1 = d1.stat()
    s2 = d2.stat()
    print(f"adrian/daemon inode: {s1.st_ino}, size: {s1.st_size}")
    print(f"admiral/daemon inode: {s2.st_ino}, size: {s2.st_size}")
    print(f"Same file (inode): {s1.st_ino == s2.st_ino}")
    print(f"Same file (size): {s1.st_size == s2.st_size}")

    # Sprawdz _user_lang w obu plikach
    t1 = d1.read_text(errors="replace")
    t2 = d2.read_text(errors="replace")
    print(f"\n_user_lang w /home/adrian/...: {'_user_lang' in t1}")
    print(f"_user_lang w /home/admiral/..: {'_user_lang' in t2}")
    print(f"Pliki identyczne: {t1 == t2}")
