# engine.py — scripts/ciel_confidence_system/engine.py

## Tożsamość
- **id_karty:** `REPO-ENGINE-FE78`
- **ścieżka:** `scripts/ciel_confidence_system/engine.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `0.015`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_confidence_system/engine.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 0.015 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `AFFECT`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.542195`
- **R₃:** `0.629813`
- **R₆:** `0.534142`
- **R₉:** `0.565106`
- **potencjal_kappa:** `0.141102`
- **masa_semantyczna:** `0.203631`
- **rodzaj_karty:** `0.326785`


## Rola
ciel_confidence.py — Confidence scoring engine for ingested data.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ConfidenceResult
- **funkcje:** `score_source_type`, `score_cross_ref`, `score_recency`, `score_consistency`, `score_self_consistency`, `score_confidence`, `main`

## Opis
ciel_confidence.py — Confidence scoring engine for ingested data.

Każdy fakt/kawałek informacji dostaje procentową pewność (0.0 – 1.0).
Składowe:
  1. Source reliability — waga źródła (academic=0.9, blog=0.35, ...)
  2. Cross-reference count — ile niezależnych źródeł potwierdza
  3. Recency — jak świeża informacja
  4. Internal consistency — czy nie przeczy wysokiej-pewności wiedzy
  5. Self-cons
