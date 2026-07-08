# qubit.py — .python_packages/sympy/physics/quantum/qubit.py

## Tożsamość
- **id_karty:** `REPO-QUBIT-30E5`
- **ścieżka:** `.python_packages/sympy/physics/quantum/qubit.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.895`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/physics/quantum/qubit.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.895 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MEMORY`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.481637`
- **R₃:** `0.436994`
- **R₆:** `0.50573`
- **R₉:** `0.517955`
- **potencjal_kappa:** `0.179117`
- **masa_semantyczna:** `0.012321`
- **rodzaj_karty:** `0.236997`


## Rola
Qubits for quantum computing.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** QubitState, Qubit, QubitBra, IntQubitState, IntQubit, IntQubitBra
- **funkcje:** `matrix_to_qubit`, `matrix_to_density`, `qubit_to_matrix`, `measure_all`, `measure_partial`, `measure_partial_oneshot`, `_get_possible_outcomes`, `measure_all_oneshot`, `_eval_args`, `_eval_hilbert_space`, `dimension`, `nqubits`, `qubit_values`, `flip`, `dual_class`, `_eval_innerproduct_QubitBra`, `_represent_default_basis`, `_represent_ZGate`, `_eval_trace`, `_reduced_density`, `dual_class`, `_eval_args`, `_eval_args_with_nqubits`, `as_int`, `_print_label`, `_print_label_pretty`, `dual_class`, `_eval_innerproduct_IntQubitBra`, `dual_class`, `find_index_that_is_projected`

## Opis
Qubits for quantum computing.

Todo:
* Finish implementing measurement logic. This should include POVM.
* Update docstrings.
* Update tests.
