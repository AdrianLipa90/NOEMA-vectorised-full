# hyp2f1_data.py — .python_packages/scipy/special/_precompute/hyp2f1_data.py

## Tożsamość
- **id_karty:** `REPO-HYP2F1_DATA-E111`
- **ścieżka:** `.python_packages/scipy/special/_precompute/hyp2f1_data.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.475`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/special/_precompute/hyp2f1_data.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.475 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ADDITION`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.662589`
- **R₃:** `0.614656`
- **R₆:** `0.542851`
- **R₉:** `0.417608`
- **potencjal_kappa:** `0.07638`
- **masa_semantyczna:** `0.206164`
- **rodzaj_karty:** `0.259027`


## Rola
This script evaluates scipy's implementation of hyp2f1 against mpmath's.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `get_region`, `get_result`, `get_result_no_mp`, `get_results`, `_make_hyp2f1_test_case`, `make_hyp2f1_test_cases`, `main`

## Opis
This script evaluates scipy's implementation of hyp2f1 against mpmath's.

Author: Albert Steppi

This script is long running and generates a large output file. With default
arguments, the generated file is roughly 700MB in size and it takes around
40 minutes using an Intel(R) Core(TM) i5-8250U CPU with n_jobs set to 8
(full utilization). There are optional arguments which can be used to restrict
(
