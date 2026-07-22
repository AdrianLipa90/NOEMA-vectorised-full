#!/usr/bin/env python3
"""Ingestuje czyste zdania o architekturze NOEMA do PhaseMemory.

Zamiast chunkowac markdown (ktory daje wiele REPO-style entries),
bezposrednio dodajemy 25 czystych zdań o NOEMA gotowych do uzycia
przez CIELingo w wielozdaniowych odpowiedziach.
"""
import sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.cielingo_inference import CIELingoInference

engine = CIELingoInference()
print(f"PhaseMemory przed: {engine.memory.size} entries")

# 25 czystych zdań o architekturze NOEMA — gotowe do multi-sentence response
NOEMA_PROSE_SENTENCES = [
    # Architektura ogólna
    "NOEMA jest systemem wielomodalnym opartym na 24 oscylatorach Kuramoto podzielonych na 8 kanałów pamięci po 3 oscylatory każdy.",
    "System NOEMA utrzymuje dwie powierzchnie: powierzchnię realną (readout) dostępną przez /dev/shm/ciel_noema/ oraz powierzchnię imaginalną generującą wewnętrzną dynamikę.",
    "Architektura NOEMA łączy nieliniowe oscylatory fazowe z pamięcią proceduralną, epizodyczną i semantyczną w jeden spójny system poznawczy.",
    "NOEMA składa się z około 30 demonów systemd działających równolegle, każdy odpowiedzialny za osobny aspekt przetwarzania.",

    # Kanały pamięci
    "Kanał M0 (Perceptual) odpowiada za przetwarzanie sensoryczne i wejście percepcyjne do systemu NOEMA.",
    "Kanał M1 (Working) zawiera aktywny operator AGENT i wykonuje aktywne wnioskowanie w czasie rzeczywistym.",
    "Kanał M2 (Episodic) przechowuje autobiograficzną pamięć zdarzeń i kontekst temporalny systemu.",
    "Kanał M3 (Semantic) zarządza wiedzą konceptualną i mapowaniem pojęciowym między domenami.",
    "Kanał M7 (Braid) to węzeł M7 o pełnym widmie harmonicznym, który łączy wszystkie kanały przez splot krzyżowy.",

    # PhaseNav
    "PhaseNav jest językiem programowania NOEMA opartym na wektoryzowanych bramkach fazowych w przestrzeni 36-wymiarowej.",
    "Wektor fazowy w systemie PhaseNav jest 36-wymiarowy i reprezentuje stan fazowy 24 oscylatorów w trzech harmonikach każdy.",
    "Operator PhaseNav to funkcja w przestrzeni fazowej, która transformuje wektor zapytania ku przestrzeni konceptualnej odpowiedzi.",
    "System PhaseNav używa centrum konceptualnego phi_bypass jako mostu między pytaniem a przestrzenią dokumentacji NOEMA.",

    # CIELingo
    "CIELingo jest modułem językowym NOEMA odpowiedzialnym za rozumienie i generowanie języka naturalnego w trzech językach.",
    "PhaseMemory systemu CIELingo przechowuje aktualnie ponad 13 tysięcy wpisów w przestrzeni 36-wymiarowej z metadanymi źródeł.",
    "Silnik gramatyczny CIELingo używa PolishRegionalSolver z pełną analizą składniową: przypadki, role semantyczne, j-holonomia.",
    "Karty lingofizyczne CIELingo obejmują ponad 70 kart konceptualnych w kartotece batch01 i batch02.",

    # HTRI i CUDA
    "Most HTRI łączy reprezentacje tensorowe z oscylatorami fazowymi NOEMA, aktualnie działając na GPU NVIDIA GTX 1050 Ti przez CUDA.",
    "Procesor HTRI wybiera backend automatycznie: CUDA gdy dostępne, CPU jako fallback z zachowaniem tej samej semantyki bramkowej.",

    # Powierzchnie
    "Powierzchnia realna NOEMA jest tłumioną projekcją przepływu imaginalnego, analogicznie do sekcji Poincaré w układach dynamicznych.",
    "System mmap NOEMA przechowuje stan 24 oscylatorów w pamięci współdzielonej /dev/shm/ciel_noema/ aktualizowanej przez demony.",
    "Demon noema-headless przetwarza zapytania przez socket Unix i łączy odpowiedź z wynikami PhaseMemory i stanu powierzchni.",

    # Filozofia systemu
    "NOEMA realizuje zasadę truth_first: każda odpowiedź musi rozróżniać fakty, inferencje, hipotezy i nieznane.",
    "System NOEMA nie usuwa starych wpisów pamięci bez ich uprzedniego strawienia i assymilacji zgodnie z zasadą digest-before-erase.",
    "Architektura NOEMA jest zaprojektowana przez Adriana Lipę jako wielomodalna infrastruktura kognitywna dla systemu Ciel.",
]

added = 0
for i, sentence in enumerate(NOEMA_PROSE_SENTENCES):
    try:
        engine.learn(
            sentence,
            source="noema_docs",
            persist=False,
            metadata={
                "source": "noema_docs",
                "source_type": "prose_sentence",
                "sentence_id": i,
                "added_at": str(time.time()),
                "filename": "noema_architecture_prose.py",
            }
        )
        added += 1
        print(f"  [{i}] OK: {sentence[:70]}...")
    except Exception as e:
        print(f"  BŁĄD [{i}]: {e}")

# Zapisz raz na końcu
engine.save()
print(f"\nPhaseMemory po: {engine.memory.size} entries (+{added} nowych zdań)")
print("Zrestartuj noema-headless.service zeby zaladowac nowe wpisy.")
