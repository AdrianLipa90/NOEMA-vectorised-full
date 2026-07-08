# test_cython_optimize.py — .python_packages/scipy/optimize/tests/test_cython_optimize.py

## Tożsamość
- **id_karty:** `REPO-TEST_CYTHON_OPTIMIZE-73A5`
- **ścieżka:** `.python_packages/scipy/optimize/tests/test_cython_optimize.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `6.204`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/optimize/tests/test_cython_optimize.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 6.204 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `FORCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.552175`
- **R₃:** `0.435218`
- **R₆:** `0.571397`
- **R₉:** `0.579087`
- **potencjal_kappa:** `0.300939`
- **masa_semantyczna:** `0.016845`
- **rodzaj_karty:** `0.260112`


## Rola
Test Cython optimize zeros API functions: ``bisect``, ``ridder``, ``brenth``,

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `test_bisect`, `test_ridder`, `test_brenth`, `test_brentq`, `test_brentq_full_output`

## Opis
Test Cython optimize zeros API functions: ``bisect``, ``ridder``, ``brenth``,
and ``brentq`` in `scipy.optimize.cython_optimize`, by finding the roots of a
3rd order polynomial given a sequence of constant terms, ``a0``, and fixed 1st,
2nd, and 3rd order terms in ``args``.

.. math::

    f(x, a0, args) =  ((args[2]*x + args[1])*x + args[0])*x + a0

The 3rd order polynomial function is written in
