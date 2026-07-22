#!/usr/bin/env python3
"""Sprawdź endpointy serwera na 18520."""
import urllib.request, json

BASE = "http://127.0.0.1:18520"

# Próbuj typowe ścieżki LLM API
paths = [
    "/api/generate",
    "/api/tags",
    "/api/chat",
    "/api/version",
    "/v1/completions",
    "/v1/chat/completions",
    "/completion",
    "/completions",
    "/api",
    "/info",
    "/status",
    "/",
]

for path in paths:
    try:
        req = urllib.request.Request(f"{BASE}{path}", method="GET")
        with urllib.request.urlopen(req, timeout=2) as r:
            body = r.read().decode("utf-8", errors="replace")[:200]
            print(f"  OK {r.status} {path}: {body[:150]}")
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print(f"  HTTP {e.code} {path}")
        # 404 ignoruj
    except Exception as e:
        print(f"  ERR {path}: {e}")
