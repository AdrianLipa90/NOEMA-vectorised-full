#!/usr/bin/env python3
"""Debug: sprawdz co _lang() i realize_native_reply() zwracają z argumentami daemona."""
import sys
sys.path.insert(0, "/home/adrian/noema/src")

TEXT = "Czym jest system NOEMA i jak działa architektura CIELingo z PhaseMemory?"

from ciel_sot_agent.conversation_bridge import _lang, realize_native_reply
import inspect

# 1. Sprawdz _lang source
src = inspect.getsource(_lang)
print("=== _lang source (first 300 chars) ===")
print(src[:300])

# 2. Sprawdz _lang wartość
_user_lang_daemon = "pl" if any(ch in "ąćęłńóśźżĄĆĘŁŃÓŚŹŻ" for ch in TEXT) else "en"
print(f"\n=== _user_lang (jak w daemonie) ===")
print(f"_user_lang = {_user_lang_daemon!r}")

lang_result = _lang(_user_lang_daemon, TEXT)
print(f"_lang({_user_lang_daemon!r}, text) = {lang_result!r}")

# 3. Wywołaj realize_native_reply z minimalnym state (brak pamięci)
print("\n=== realize_native_reply (bez state) ===")
result_no_state = realize_native_reply(TEXT, language=_user_lang_daemon)
print(f"reply: {result_no_state.get('reply', '')[:200]}")
print(f"dialogue_act: {result_no_state.get('dialogue_act', {}).get('act')}")

# 4. Wywołaj z language="en" (jak było PRZED fix)
print("\n=== realize_native_reply (language='en') — jak było przed fix ===")
result_en = realize_native_reply(TEXT, language="en")
print(f"reply: {result_en.get('reply', '')[:200]}")

# 5. Wywołaj z language="pl" (jak teraz)
print("\n=== realize_native_reply (language='pl') — oczekiwany fix ===")
result_pl = realize_native_reply(TEXT, language="pl")
print(f"reply: {result_pl.get('reply', '')[:200]}")

# 6. Sprawdz surface_plan
sp = result_pl.get("surface_plan", {})
print(f"\nsurface_plan.language: {sp.get('language')}")
print(f"surface_plan.dialogue_act: {sp.get('dialogue_act')}")
