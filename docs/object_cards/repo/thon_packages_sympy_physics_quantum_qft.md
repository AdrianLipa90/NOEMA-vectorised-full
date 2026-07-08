# qft.py — .python_packages/sympy/physics/quantum/qft.py

## Tożsamość
- **id_karty:** `REPO-QFT-7407`
- **ścieżka:** `.python_packages/sympy/physics/quantum/qft.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.228`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/physics/quantum/qft.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.228 |
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
An implementation of qubits and gates acting on them.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** RkGate, Fourier, QFT, IQFT
- **funkcje:** `_eval_args`, `k`, `targets`, `gate_name_plot`, `get_target_matrix`, `_eval_args`, `_represent_default_basis`, `_represent_ZGate`, `targets`, `min_qubits`, `size`, `omega`, `decompose`, `_apply_operator_Qubit`, `_eval_inverse`, `omega`, `decompose`, `_eval_inverse`, `omega`

## Opis
An implementation of qubits and gates acting on them.

Todo:

* Update docstrings.
* Update tests.
* Implement apply using decompose.
* Implement represent using decompose or something smarter. For this to
  work we first have to implement represent for SWAP.
* Decide if we want upper index to be inclusive in the constructor.
* Fix the printing of Rk gates in plotting.
