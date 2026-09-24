#!/usr/bin/env python3
"""Sprawdź portal i ciel_agent_backend."""
import urllib.request, json

def get(url, timeout=3):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, {}
    except Exception as e:
        return None, str(e)[:100]

# Portal health
s, b = get("http://127.0.0.1:18888/api/live")
print(f"Portal /api/live: {s} → docs={b.get('kb_docs','?')} terms={b.get('kb_terms','?')} aff={b.get('kb_affinity','?')}")

# Portal knowledge search test
s2, b2 = get("http://127.0.0.1:18888/api/search?q=CIELingo")
if s2 == 200:
    results = b2.get("results", [])
    print(f"Portal search 'CIELingo': {len(results)} wyników")
    for r in results[:3]:
        print(f"  - {r.get('title','?')[:60]} (score={r.get('score','?')})")
else:
    print(f"Portal search: {s2} {b2}")

# ciel_agent_backend endpointy
print("\nciel_agent_backend (18520):")
for path in ["/api/status", "/api/health", "/api/model", "/status"]:
    s3, b3 = get(f"http://127.0.0.1:18520{path}")
    if s3 == 200:
        print(f"  {path}: {str(b3)[:150]}")
    elif s3 == 404:
        pass  # ignoruj 404
    else:
        print(f"  {path}: {s3}")
