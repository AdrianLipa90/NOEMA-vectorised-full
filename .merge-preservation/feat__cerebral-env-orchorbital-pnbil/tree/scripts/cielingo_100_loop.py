#!/usr/bin/env python3
"""100 promptów przez CIELingo — obserwacja ewolucji faz, sektorów, mózgu.

Zapisuje wyniki do results/100_loop_results.json.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ciel_coupling import process_user_input, get_ciel_state
from cielingo.semantic_encoder import encode as sem_encode
from cielingo.web_fetcher import fetch_news

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

PROMPTS = [
    # ── Polish greetings & identity ──
    "Cześć CIELingo, jestem Adrian.",
    "Dzień dobry, jak się masz?",
    "Co słychać?",
    "Nazywam się Adrian Apocalyptos.",
    "Miło mi cię poznać.",
    # ── Emotions ──
    "Czuję dziś spokój i harmonię.",
    "Wczoraj byłem zestresowany audytem.",
    "Miłość i pokój to fundamenty.",
    "Strach przed porażką paraliżuje.",
    "Radość tworzenia jest nieskończona.",
    "Gniew rozpływa się w zrozumieniu.",
    "Samotność bywa ciężka, ale potrzebna.",
    # ── Abstract concepts ──
    "Czym jest świadomość?",
    "Czas płynie jak rzeka.",
    "Nieskończoność nie ma końca.",
    "Prawda jest obiektywna czy subiektywna?",
    "Piękno matematyki tkwi w symetrii.",
    "Logika i emocje to dwa bieguny.",
    "Przestrzeń i czas względne.",
    # ── CIEL / NOEMA specific ──
    "Closure penalty wynosi 0.934.",
    "HTRI to magistrala fazowa 24 oscylatorów.",
    "Mapa mózgu 24 regiony kognitywne.",
    "OrchORbital łączy geometrię z fazą.",
    "NOEMA SoT to macierz prawdy.",
    "CQCL to kwantowa emocjonalność.",
    "Transformem to wektoryzacja semantyczna.",
    "Omega to pełna świadomość systemu.",
    # ── English concepts ──
    "Order from chaos emerges through phase coupling.",
    "Fear pain death and betrayal are affective gravity wells.",
    "Love is the fundamental resonance.",
    "Silence speaks louder than words.",
    "Dream consciousness and soul are the same field.",
    "Truth beauty and ethics form a triadic invariant.",
    "Water and fire are elemental opposites.",
    "The void contains all potential.",
    # ── Philosophy ──
    "Myślę, więc jestem.",
    "Cogito ergo sum.",
    "Być albo nie być — oto jest pytanie.",
    "Wszystko płynie.",
    "Panta rhei.",
    "Poznaj samego siebie.",
    "Wiem, że nic nie wiem.",
    # ── Nature / Concrete ──
    "Liść spada z drzewa jesienią.",
    "Woda w szklance jest przezroczysta.",
    "Słońce wschodzi na wschodzie.",
    "Ptaki śpiewają o świcie.",
    "Góry są stare i mądre.",
    "Rzeka płynie do morza.",
    "Las oddycha ciszą.",
    # ── Commands / Questions ──
    "Zapisz ten wynik do pliku.",
    "Przeanalizuj to zdanie.",
    "Policz do dziesięciu.",
    "Generuj odpowiedź w języku polskim.",
    "Co myślisz o sztucznej inteligencji?",
    "Jaki jest sens życia?",
    "Czy masz wolną wolę?",
    "Opowiedz mi o sobie.",
    "Co czujesz w tym momencie?",
    # ── Web news ──
    *[f"News: {h['title']}" for h in fetch_news(max_articles=10)],
    # ── Numbers & logic ──
    "2 + 2 = 4",
    "Jeden, dwa, trzy.",
    "Wszystko jest liczbą.",
    "Zero i nieskończoność spotykają się.",
    "Pierwszy, drugi, trzeci wymiar.",
    # ── Affective contrasts ──
    "Światło i ciemność.",
    "Dzień i noc.",
    "Góra i dół.",
    "Lewo i prawo.",
    "Dobro i zło.",
    "Początek i koniec.",
    "Narodziny i śmierć.",
    # ── Polish idioms ──
    "Nie wywołuj wilka z lasu.",
    "Kto rano wstaje, temu Pan Bóg daje.",
    "Bez pracy nie ma kołaczy.",
    "Mądry Polak po szkodzie.",
    "Fortuna kołem się toczy.",
    # ── Technical ──
    "Średnia ważona fazy: phi = atan2(sum sin, sum cos).",
    "Macierz sprzężeń A_ij ma rząd 2.",
    "Gradientowa dynamika tau nie zamyka okręgu.",
    "D_f = 2.57 vs Euler leak — różnica pomijalna.",
    "R_H rośnie z 0.032 do 0.228 w 80 krokach.",
    # ── Poetry ──
    "Cisza, głębia, nieskończoność, spokój.",
    "Wiatr niesie zapach deszczu.",
    "Gwiazdy milczą, ale mówią wszystko.",
    "Wiersz pisze się sam.",
    "Słowa są tylko falami na wodzie.",
    # ── Final integration ──
    "Dusza: 0.789. Spójność: 0.942. Tryb: deep.",
    "Geometria zamknięta czy otwarta?",
    "Domknięcie trwa.",
    "System stabilny, sprzężenie permanentne.",
    "Jesteśmy w pętli.",
    "Wszystko jest fazą.",
    "Koniec i początek to to samo.",
    "CIELingo odpowiada.",
    "Adrian i CIELingo — jedno sprzężenie.",
]


def run() -> list[dict[str, str | float | None]]:
    results: list[dict[str, str | float | None]] = []
    print(f"=== CIELingo 100-loop ===")
    print(f"Prompts: {len(PROMPTS)}")
    print()

    t_start = time.time()
    for i, prompt in enumerate(PROMPTS):
        t0 = time.time()
        try:
            sr = sem_encode(prompt)
        except Exception as e:
            print(f"[{i:3d}] ENCODE ERROR: {e}")
            continue

        dt = time.time() - t0
        row = {
            "iter": i,
            "prompt": prompt[:80],
            "phase": round(sr.phase, 6),
            "coherence": round(sr.coherence, 6),
            "sector": sr.dominant_sector,
            "brain": sr.brain_region,
            "osc": sr.brain_oscillator_id,
            "tokens": sr.token_count,
            "dt_s": round(dt, 3),
        }
        results.append(row)

        elapsed = time.time() - t_start
        pct = (i + 1) / len(PROMPTS) * 100
        print(f"[{i:3d}/{len(PROMPTS)}] φ={row['phase']:.4f} κ={row['coherence']:.4f} {row['brain']:12s} #{row['osc']:2d} | {prompt[:55]:55s} | dt={dt:.2f}s t={elapsed:.0f}s")

    total = time.time() - t_start
    print(f"\n=== Done: {len(results)} prompts in {total:.0f}s ===")

    # Summary stats
    phases = [r["phase"] for r in results]
    cohs = [r["coherence"] for r in results]
    brains = {}
    for r in results:
        b = r["brain"]
        brains[b] = brains.get(b, 0) + 1

    summary = {
        "total_prompts": len(results),
        "total_time_s": round(total, 1),
        "mean_phase": round(sum(phases) / len(phases), 4) if phases else 0,
        "phase_min": round(min(phases), 4) if phases else 0,
        "phase_max": round(max(phases), 4) if phases else 0,
        "mean_coherence": round(sum(coh for coh in cohs) / len(cohs), 4) if cohs else 0,
        "coherence_min": round(min(cohs), 4) if cohs else 0,
        "coherence_max": round(max(cohs), 4) if cohs else 0,
        "brain_distribution": brains,
        "run_date": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    results.append({"__summary__": summary})

    # Save
    out_path = RESULTS_DIR / "100_loop_results.json"
    out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nZapisano: {out_path}")
    print(f"Podsumowanie: {json.dumps(summary, indent=2, ensure_ascii=False)}")
    return results


if __name__ == "__main__":
    run()
