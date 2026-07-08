# test_gufunc_scalar.py — .python_packages/numba/cuda/tests/cudapy/test_gufunc_scalar.py

## Tożsamość
- **id_karty:** `REPO-TEST_GUFUNC_SCALAR-191D`
- **ścieżka:** `.python_packages/numba/cuda/tests/cudapy/test_gufunc_scalar.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.676`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/cuda/tests/cudapy/test_gufunc_scalar.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.676 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `REFUSAL`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.441725`
- **R₃:** `0.537197`
- **R₆:** `0.362678`
- **R₉:** `0.509166`
- **potencjal_kappa:** `0.077364`
- **masa_semantyczna:** `-0.245874`
- **rodzaj_karty:** `0.27107`


## Rola
Example: sum each row using guvectorize

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestGUFuncScalar
- **funkcje:** `test_gufunc_scalar_output`, `test_gufunc_scalar_output_bug`, `test_gufunc_scalar_input_saxpy`, `test_gufunc_scalar_cast`, `test_gufunc_old_style_scalar_as_array`, `sum_row`, `twice`, `saxpy`, `foo`, `gufunc`

## Opis
Example: sum each row using guvectorize

See Numpy documentation for detail about gufunc:
    http://docs.scipy.org/doc/numpy/reference/c-api.generalized-ufuncs.html
