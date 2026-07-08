# parfor_iss9490_usecase.py — .python_packages/numba/tests/parfor_iss9490_usecase.py

## Tożsamość
- **id_karty:** `REPO-PARFOR_ISS9490_USECA-B1F6`
- **ścieżka:** `.python_packages/numba/tests/parfor_iss9490_usecase.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.643`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/tests/parfor_iss9490_usecase.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.643 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


## Rola
This is a testcase for https://github.com/numba/numba/issues/9490.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `stable_fit`, `check`

## Opis
This is a testcase for https://github.com/numba/numba/issues/9490.
The bug is very sensitive to the control-flow and variable uses.
It is impossible to shrink the reproducer in any meaningful way.

The test is also sensitive to PYTHONHASHSEED.
PYTHONHASHSEED=1 will trigger the bug.

Example of traceback:

  File "/numba/parfors/parfor.py", line 2070, in _arrayexpr_to_parfor
    index_vars, loopnes
