#!/usr/bin/env python3
"""Sprawdz jaka wersja _lang jest zaladowana przez daemon."""
import sys
sys.path.insert(0, "/home/adrian/noema/src")

import ciel_sot_agent.conversation_bridge as cb
import inspect

# Pobierz source _lang
src = inspect.getsource(cb._lang)
print("=== _lang source ===")
print(src)

# Test
print("\n=== Test _lang ===")
result_pl = cb._lang("en", "Czym jest system NOEMA i jak działa jego architektura?")
result_en = cb._lang("en", "What is the NOEMA system?")
print(f"_lang('en', 'Czym...działa...') = {result_pl!r}")
print(f"_lang('en', 'What is...') = {result_en!r}")

# Sprawdz czy text_is_polish wins
print(f"\ntext_is_polish wins: {'text_is_polish' in src}")
