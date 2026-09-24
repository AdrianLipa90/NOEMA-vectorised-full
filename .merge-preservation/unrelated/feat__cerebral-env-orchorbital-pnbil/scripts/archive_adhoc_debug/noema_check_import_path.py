#!/usr/bin/env python3
"""Sprawdz skad jest importowany conversation_bridge i czy ma _compose_memory_lines."""
import sys

# Daemon uruchamia sie z /home/adrian/noema/.venv/bin/python3
# Sprawdz sys.path i skad importuje conversation_bridge

sys.path.insert(0, "/home/adrian/noema/src")

import ciel_sot_agent.conversation_bridge as cb
print(f"Modul: {cb.__file__}")
import inspect
src = inspect.getsource(cb._compose_memory_lines)
# Sprawdz czy ma _PL_CONNECTORS vs _EN_CONNECTORS
has_pl = "_PL_CONNECTORS" in src
has_en = "_EN_CONNECTORS" in src
print(f"_PL_CONNECTORS w source: {has_pl}")
print(f"_EN_CONNECTORS w source: {has_en}")

# Sprawdz sys.path
print(f"\nsys.path[:5]: {sys.path[:5]}")

# Sprawdz site-packages
import importlib.util
spec = importlib.util.find_spec("ciel_sot_agent")
if spec:
    print(f"ciel_sot_agent spec origin: {spec.origin}")
