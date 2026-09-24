#!/usr/bin/env python3
"""Znajdź plik cielingo-chat.js i pokaż fragment z fetch/send."""
import subprocess

# Znajdź plik
r = subprocess.run(
    ["find", "/home/adrian/noema", "-name", "cielingo-chat.js", "-maxdepth", "8"],
    capture_output=True, text=True, timeout=10
)
print("=== FOUND FILES ===")
print(r.stdout)

for path in r.stdout.strip().split("\n"):
    if path.strip():
        print(f"\n=== {path} (fetch/send section) ===")
        with open(path) as f:
            content = f.read()
        # Znajdź linię z fetch
        lines = content.split("\n")
        for i, l in enumerate(lines):
            if any(k in l for k in ["fetch(", "sendMessage", "/cielingo/chat", "POST", ".send("]):
                start = max(0, i-3)
                end = min(len(lines), i+15)
                for li in lines[start:end]:
                    print(li)
                print("---")
