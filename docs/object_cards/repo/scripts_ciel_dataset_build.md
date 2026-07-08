# ciel_dataset_build.py — scripts/ciel_dataset_build.py

## Tożsamość
- **id_karty:** `REPO-CIEL_DATASET_BUILD-444E`
- **ścieżka:** `scripts/ciel_dataset_build.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.259`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_dataset_build.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.259 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `SOURCE_REQUIRED`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.509375`
- **R₃:** `0.557002`
- **R₆:** `0.453972`
- **R₉:** `0.573802`
- **potencjal_kappa:** `-0.191054`
- **masa_semantyczna:** `-0.307021`
- **rodzaj_karty:** `0.246226`


## Rola
CIEL LoRA Dataset Builder

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `records_from_foundation_pack`, `records_from_cards`, `records_from_coupling_matrix`, `records_from_holonomy`, `records_from_cqcl`, `records_identity`, `_chat`, `build_dataset`

## Opis
CIEL LoRA Dataset Builder

Kompiluje dataset treningowy ze wszystkich źródeł CIEL:
  - CIEL_Orbital_Foundation_Pack (formalna teoria)
  - memory/cards/ (ontologia bytów)
  - coupling.py J_kj (matematyczny substrat)
  - holonomy.py (geometria Berry'ego)
  - CQCL (operatory kwantowe)

Format wyjściowy: JSONL (chat format) gotowy do fine-tuningu przez PEFT/trl.

Użycie:
  python3 ciel_dataset_build.p
