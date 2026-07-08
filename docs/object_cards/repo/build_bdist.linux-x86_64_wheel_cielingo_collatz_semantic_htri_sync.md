# collatz_semantic_htri_sync.py — build/bdist.linux-x86_64/wheel/cielingo/collatz_semantic_htri_sync.py

## Tożsamość
- **id_karty:** `REPO-COLLATZ_SEMANTIC_HTR-FA56`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo/collatz_semantic_htri_sync.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.886`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo/collatz_semantic_htri_sync.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.886 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CAUSE`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.440841`
- **R₃:** `0.698384`
- **R₆:** `0.560357`
- **R₉:** `0.385177`
- **potencjal_kappa:** `0.165796`
- **masa_semantyczna:** `0.077602`
- **rodzaj_karty:** `0.2472`


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
