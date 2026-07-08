# test_interaction.py — .python_packages/numpy/matrixlib/tests/test_interaction.py

## Tożsamość
- **id_karty:** `REPO-TEST_INTERACTION-9BCA`
- **ścieżka:** `.python_packages/numpy/matrixlib/tests/test_interaction.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.188`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numpy/matrixlib/tests/test_interaction.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.188 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
Tests of interaction of matrix with other parts of numpy.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestConcatenatorMatrix
- **funkcje:** `test_fancy_indexing`, `test_polynomial_mapdomain`, `test_sort_matrix_none`, `test_partition_matrix_none`, `test_dot_scalar_and_matrix_of_objects`, `test_inner_scalar_and_matrix`, `test_inner_scalar_and_matrix_of_objects`, `test_iter_allocate_output_subtype`, `like_function`, `test_array_astype`, `test_stack`, `test_object_scalar_multiply`, `test_nanfunctions_matrices`, `test_nanfunctions_matrices_general`, `test_average_matrix`, `test_dot_matrix`, `test_ediff1d_matrix`, `test_apply_along_axis_matrix`, `test_kron_matrix`, `test_array_equal_error_message_matrix`, `test_array_almost_equal_matrix`, `double`, `test_matrix`, `test_matrix_scalar`, `test_matrix_builder`

## Opis
Tests of interaction of matrix with other parts of numpy.

Note that tests with MaskedArray and linalg are done in separate files.
