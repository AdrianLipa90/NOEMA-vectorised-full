#!/usr/bin/env python3
"""Inspekcja pełnego API portalu."""
import urllib.request, json

BASE = "http://127.0.0.1:18888"

def get(path, timeout=3):
    try:
        with urllib.request.urlopen(f"{BASE}{path}", timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:
        return None, str(e)[:100]

# Pełna odpowiedź live
s, body = get("/api/live")
print(f"=== /api/live ({s}) ===")
try:
    d = json.loads(body)
    for k, v in d.items():
        print(f"  {k}: {str(v)[:80]}")
except Exception:
    print(body[:500])

# Sprawdź inne ścieżki
for path in ["/api/status", "/api/knowledge", "/api/knowledge/stats",
             "/api/search?q=test", "/api/docs", "/api/kb/stats"]:
    s2, b2 = get(path)
    if s2 == 200:
        print(f"\n{path} ({s2}): {b2[:200]}")
    elif s2 not in (404, None):
        print(f"\n{path}: HTTP {s2}")
