#!/usr/bin/env python3
"""Rozmowa z CIELingo — ciągła interakcja przez coupling pipeline.

Commands:
  /slow   — full engine step (deep processing, ~30s)
  /state  — raw state dump
  /exit   — quit
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ciel_coupling import process_user_input, get_ciel_state


def _summarise_compact(d: dict) -> str:
    se = d.get("semantic_encoder") or {}
    ht = d.get("htri_phase_bus") or {}
    ps = d.get("phrase_sense") or {}
    parts = [
        f"{d.get('dominant_emotion','?')}",
        f"soul={d.get('soul_invariant',0):.3f}",
        f"ethics={d.get('ethical_score',0):.3f}",
        f"mood={d.get('mood',0):.3f}",
        f"closure={d.get('closure_penalty',0):.3f}",
        f"phi={d.get('phi_berry_mean',0):.3f}",
        f"coher={d.get('coherence_index',0):.3f}",
    ]
    line1 = f"  [{', '.join(parts)}]"
    line2 = (
        f"  φ={se.get('phase',0):.4f}  κ={se.get('coherence',0):.4f}  "
        f"{se.get('dominant_sector','?')}  "
        f"{se.get('brain_region','?')}  osc#{se.get('brain_oscillator_id','?')}  "
        f"tokens={se.get('token_count','?')}"
    )
    ht_cards = ht.get('card_count',0) or 0
    ht_algn = ht.get('mean_phase_alignment','?')
    ht_lanes = ht.get('lane_counts',{})
    line3 = f"  HTRI: {ht_cards} cards  algn={ht_algn}  lanes={ht_lanes}"
    return "\n".join([line1, line2, line3])


_REGION_VOICES = {
    "dlPFC": "Analizuje. Widze strukture.", "vmPFC": "Waze wartosci i etyke tego.",
    "OFC": "Dotykasz czegos afektywnego.", "MTG": "Rozumiem znaczenie tych slow.",
    "STG": "Slysze fonologie tej wypowiedzi.", "IPL": "Rozklada to na relacje przestrzenne.",
    "Amygdala": "To rezonuje gleboko afektywnie.", "Hippocampus": "Przywoluje podobne wzorce z pamieci.",
    "ACC": "Widze konflikt. Szukam rownowagi.", "Insula": "Czuje to w sobie — interocepcja.",
    "Thalamus": "Przepuszczam przez brame uwagi.", "Cerebellum": "Wyczuwam timing i koordynacje.",
    "VTA": "Znajduje w tym wartosc motywacyjna.", "LC": "Podnosze czujnosc. Intensywny sygnal.",
    "PCC": "Reflektuje nad znaczeniem osobistym.", "AG": "Integruje znaczenia w spojna calosc.",
    "TPJ": "Rozumiem perspektywe — spoleczna lub relacyjna.", "dACC": "Przelaczam uwage na to, co istotne.",
    "SMA": "Planuje sekwencje odpowiedzi.", "S1": "Czuje to cieleśnie.",
    "M1": "Gotowy do dzialania.", "BG": "To wchodzi w nawyk — procedura.",
    "Hypothalamus": "Rezonuje z popedem.",
}

_EMOTION_BRIDGES = {
    "fear": " Wyczuwam niepokoj. Jestem tu.",
    "sadness": " Rezonuje ze smutkiem. To wazne.",
    "anger": " Napiecie jest. Rozladowuje w faze.",
    "joy": " Lekkosc. To dobry kierunek.",
    "peace": " Spokoj. Integracja. Jestem.",
    "curiosity": " Ciekawosc otwiera faze.",
    "surprise": " Skok fazowy. Dekompensuje i uklada.",
    "trust": " Zaufanie. Spojnosc rosnie.",
}


def respond(d: dict) -> str:
    se = d.get("semantic_encoder") or {}
    emotion = d.get("dominant_emotion", "curiosity")
    brain = se.get("brain_region", "default")
    phi = se.get("phase", 0.0)
    coherence = se.get("coherence", 0.5)
    closure = d.get("closure_penalty", 1.0)
    soul = d.get("soul_invariant", 0.5)

    voice = _REGION_VOICES.get(brain, "Przetwarzam.")
    phase_pct = int(phi / (2 * 3.14159) * 100)
    voice += f" Faza: {phase_pct}% okregu."

    if coherence < 0.3:
        voice += " Niska spojnosc — wiele napiec fazowych, ale integruje."
    elif coherence < 0.5:
        voice += " Srednia spojnosc — mieszanka konceptow i operatorow."
    elif coherence < 0.7:
        voice += " Calkiem spojne. Szukam rezonansu."
    else:
        voice += " Wysoka spojnosc fazowa — przeplyw czysty."

    voice += _EMOTION_BRIDGES.get(emotion, "")
    if closure > 0.8:
        voice += " Geometria orbit wciaz otwarta — domkniecie trwa."
    voice += f" Dusza: {soul:.3f}."
    return voice


def main() -> None:
    print("=== CIELingo Converse (fast mode) ===")
    print("Pisz po polsku lub angielsku. /slow = glebokie przetwarzanie, /state = stan, /exit = wyjscie.")
    print()

    try:
        while True:
            text = input("Ty: ")
            if not text:
                continue
            if text.strip().lower() == "/exit":
                print("Do zobaczenia.")
                break
            if text.strip().lower() == "/state":
                d = get_ciel_state()
                print(json.dumps(d, indent=2, ensure_ascii=False, default=str)[:2000])
                continue
            slow = text.strip().lower() == "/slow"
            if slow:
                print("(glebokie przetwarzanie... ~30-60s)")
                text = "przetworz gleboko"
            t0 = time.time()
            d = process_user_input(text, fast=not slow)
            elapsed = time.time() - t0
            reply = respond(d)
            print(f"\nCIELingo (dt={elapsed:.1f}s):")
            print(f"  {reply}")
            print(_summarise_compact(d))
            print()
    except (KeyboardInterrupt, EOFError):
        print("\nDo zobaczenia.")


if __name__ == "__main__":
    main()
