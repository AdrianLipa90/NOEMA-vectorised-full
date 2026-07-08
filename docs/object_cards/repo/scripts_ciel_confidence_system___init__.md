# __init__.py — scripts/ciel_confidence_system/__init__.py

## Tożsamość
- **id_karty:** `REPO-__INIT__-8886`
- **ścieżka:** `scripts/ciel_confidence_system/__init__.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.868`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_confidence_system/__init__.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.868 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `ATTRACTOR`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.476161`
- **R₃:** `0.526498`
- **R₆:** `0.547584`
- **R₉:** `0.472579`
- **potencjal_kappa:** `4.910705`
- **masa_semantyczna:** `13.031004`
- **rodzaj_karty:** `1.5`


## Rola
ciel_confidence_system — Confidence-scored data ingestion + uncertainty tracking.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** —

## Opis
ciel_confidence_system — Confidence-scored data ingestion + uncertainty tracking.

Public API:
  engine.score_confidence()      — score text confidence (0.0–1.0)
  engine.ConfidenceResult        — structured confidence breakdown
  engine.SOURCE_WEIGHTS          — source type → base weight mapping
  ingest.ingest_text()           — ingest content with confidence scoring
  ingest.extract_fragments()
