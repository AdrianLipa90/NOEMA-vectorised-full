# nrtopt.py — .python_packages/numba/core/runtime/nrtopt.py

## Tożsamość
- **id_karty:** `REPO-NRTOPT-8729`
- **ścieżka:** `.python_packages/numba/core/runtime/nrtopt.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.293`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/core/runtime/nrtopt.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.293 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RETURN`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.642878`
- **R₃:** `0.503912`
- **R₆:** `0.555289`
- **R₉:** `0.707983`
- **potencjal_kappa:** `-0.270999`
- **masa_semantyczna:** `-0.074142`
- **rodzaj_karty:** `0.291714`


## Rola
NRT specific optimizations

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_remove_redundant_nrt_refct`, `remove_redundant_nrt_refct`, `_extract_functions`, `_process_function`, `_extract_basic_blocks`, `_process_basic_block`, `_examine_refct_op`, `_prune_redundant_refct_ops`, `_move_and_group_decref_after_all_increfs`

## Opis
NRT specific optimizations
