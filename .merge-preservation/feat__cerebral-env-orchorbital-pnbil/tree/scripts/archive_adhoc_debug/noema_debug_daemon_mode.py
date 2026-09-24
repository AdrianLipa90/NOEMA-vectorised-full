#!/usr/bin/env python3
"""Debug: pokaż pełny response z mode/episodic/language info."""
import socket, json

SOCK = "/media/adrian/New Volume/CIEL_memories/run/ciel_headless.sock"
TEXT = "Czym jest system NOEMA i jak działa architektura CIELingo z PhaseMemory?"

def query_full(text):
    payload = json.dumps({"text": text, "context": {}}).encode()
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(30)
    s.connect(SOCK)
    s.sendall(payload + b"\n")
    buf = b""
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        buf += chunk
        try:
            data = json.loads(buf.decode())
            break
        except json.JSONDecodeError:
            pass
    s.close()
    return data

result = query_full(TEXT)

# Pokaż kluczowe pola
response = result.get("response") or result.get("text") or ""
print(f"=== response (pierwsze 300 znaków) ===")
print(response[:300])

print(f"\n=== metadata ===")
episodic = result.get("episodic", {})
print(f"episodic.dialogue_act: {episodic.get('dialogue_act')}")

knowledge = result.get("knowledge", {})
print(f"knowledge.decision: {knowledge.get('decision', {})}")
print(f"knowledge.n_sources: {knowledge.get('n_sources', 0)}")

lang_layer = result.get("language_layer", {})
print(f"language_layer.language: {lang_layer.get('language') if lang_layer else 'N/A'}")

print(f"elapsed_s: {result.get('elapsed_s', '?')}")

# Sprawdz response z JSON (pełny dump bez response text)
debug_copy = dict(result)
debug_copy.pop("response", None)
debug_copy.pop("text", None)
debug_copy.pop("surface", None)
debug_copy.pop("phi_sample", None)
debug_copy.pop("knowledge", None)
debug_copy.pop("web_search", None)
print(f"\n=== pełny wynik (bez response/surface/phi) ===")
print(json.dumps(debug_copy, ensure_ascii=False, indent=2)[:1000])
