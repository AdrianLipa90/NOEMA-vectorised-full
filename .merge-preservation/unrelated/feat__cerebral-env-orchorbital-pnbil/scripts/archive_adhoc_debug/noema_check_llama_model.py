#!/usr/bin/env python3
"""Sprawdź załadowany model w llama-server."""
import urllib.request, json

BASE = "http://127.0.0.1:18520"

for path in ["/props", "/v1/models", "/model.json"]:
    try:
        with urllib.request.urlopen(f"{BASE}{path}", timeout=3) as r:
            body = json.loads(r.read())
            print(f"{path}: {json.dumps(body, ensure_ascii=False)[:300]}")
    except Exception as e:
        print(f"{path}: {e}")
