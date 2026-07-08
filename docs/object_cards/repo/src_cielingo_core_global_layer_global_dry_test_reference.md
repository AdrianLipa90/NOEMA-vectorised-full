# global_dry_test_reference.py — src/cielingo_core/global_layer/global_dry_test_reference.py

## Tożsamość
- **id_karty:** `REPO-GLOBAL_DRY_TEST_REFE-F003`
- **ścieżka:** `src/cielingo_core/global_layer/global_dry_test_reference.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.800`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/global_layer/global_dry_test_reference.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.800 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `NEGATION`
- **odcisk_harmoniczny:** `LHLL`
- **R₁:** `0.425094`
- **R₃:** `0.614676`
- **R₆:** `0.450577`
- **R₉:** `0.387679`
- **potencjal_kappa:** `0.085998`
- **masa_semantyczna:** `-0.143065`
- **rodzaj_karty:** `0.271614`


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
