# global_dry_test_reference.py — build/lib/cielingo_core/global_layer/global_dry_test_reference.py

## Tożsamość
- **id_karty:** `REPO-GLOBAL_DRY_TEST_REFE-1F90`
- **ścieżka:** `build/lib/cielingo_core/global_layer/global_dry_test_reference.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.947`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo_core/global_layer/global_dry_test_reference.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.947 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ASSERTION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.563342`
- **R₃:** `0.601856`
- **R₆:** `0.54039`
- **R₉:** `0.584219`
- **potencjal_kappa:** `-0.098441`
- **masa_semantyczna:** `0.347732`
- **rodzaj_karty:** `0.261593`


## Rola
Global dry-test reference builder v0.9A.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** GlobalDryTestReference
- **funkcje:** `_signal_for_case`, `run_global_dry_test_reference`, `validate`, `to_dict`, `stable_hash`

## Opis
Global dry-test reference builder v0.9A.

Runs corpus cases through the full advisory chain and exports reference objects.

This is not SOURCE, not canon, and not NOEMA SoT. It is an artifact-grounded
reference over local dry-run output.
