# collatz_semantic_htri_sync.py — build/lib/cielingo/collatz_semantic_htri_sync.py

## Tożsamość
- **id_karty:** `REPO-COLLATZ_SEMANTIC_HTR-B86D`
- **ścieżka:** `build/lib/cielingo/collatz_semantic_htri_sync.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.643`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo/collatz_semantic_htri_sync.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.643 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_PERMISSION`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.453718`
- **R₃:** `0.541785`
- **R₆:** `0.466054`
- **R₉:** `0.529069`
- **potencjal_kappa:** `0.025212`
- **masa_semantyczna:** `0.161862`
- **rodzaj_karty:** `0.285369`


## Rola
Synchronize CIELingo Collatz routing, semantic cards and HTRI phases.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** CardSyncState
- **funkcje:** `_stable_oscillator`, `_angle_delta`, `_card_seed`, `synchronize_card`, `synchronization_report`, `as_dict`

## Opis
Synchronize CIELingo Collatz routing, semantic cards and HTRI phases.

This is a deterministic planning/diagnostic surface.  It does not run primary
NOEMA inference and it does not claim physical HTRI entrainment.  It maps local
language-card phases/masses onto a 120-oscillator 7.83 Hz reference grid so the
runtime can see where semantic routing is synchronized or congested.
