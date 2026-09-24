#!/usr/bin/env python3
"""Debug: sprawdz jaki jezyk wykrywa realize_native_reply i jaki akt."""
import sys
sys.path.insert(0, "/home/adrian/noema/src")

from ciel_sot_agent.conversation_bridge import realize_native_reply, _lang, _detect_act, build_lingo_frame

text = "Czym jest system NOEMA i jak działa jego architektura?"

# Test _lang
lang_from_text = _lang(None, text)
lang_from_en_state = _lang("en", text)
lang_explicit_pl = _lang("pl", text)
print(f"_lang(None, text) = {lang_from_text!r}")
print(f"_lang('en', text) = {lang_from_en_state!r}")
print(f"_lang('pl', text) = {lang_explicit_pl!r}")

# Fake memories (list of Polish prose strings)
fake_memories = [
    {"text": "CIELingo jest modułem językowym NOEMA.", "source": "phasememory"},
    {"text": "PhaseNav jest językiem programowania NOEMA opartym na wektoryzowanych bramkach fazowych.", "source": "phasememory"},
    {"text": "NOEMA jest systemem wielomodalnym opartym na 24 oscylatorach Kuramoto.", "source": "phasememory"},
]

ciel_state = {
    "language": "en",  # symuluj stan surface'u z language=en
    "sector_memory": {
        "governed_retrieval": {
            "coherence_surface": fake_memories
        }
    }
}

# Test bez language — symuluje stary kod
result_no_lang = realize_native_reply(text, ciel_state=ciel_state)
print(f"\n[bez language] reply: {result_no_lang.get('reply', '')[:200]}")

# Test z language="pl" — symuluje nowy kod
result_with_pl = realize_native_reply(text, ciel_state=ciel_state, language="pl")
print(f"\n[language='pl'] reply: {result_with_pl.get('reply', '')[:200]}")

# Sprawdz co _detect_act mówi
frame = build_lingo_frame(text, ciel_state=ciel_state, language="pl")
act = _detect_act(text, frame, 0, "pl")
print(f"\nDialogue act: {act.act}")
print(f"Act language: {act.language}")
