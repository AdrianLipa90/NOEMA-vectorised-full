# gamma_matrices.py — .python_packages/sympy/physics/hep/gamma_matrices.py

## Tożsamość
- **id_karty:** `REPO-GAMMA_MATRICES-3673`
- **ścieżka:** `.python_packages/sympy/physics/hep/gamma_matrices.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.812`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/physics/hep/gamma_matrices.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.812 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `UNCERTAINTY`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.435049`
- **R₃:** `0.572136`
- **R₆:** `0.544042`
- **R₉:** `0.477522`
- **potencjal_kappa:** `0.159902`
- **masa_semantyczna:** `-0.053674`
- **rodzaj_karty:** `0.279085`


## Rola
Module to handle gamma matrices expressed as tensor objects.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `extract_type_tens`, `simplify_gamma_expression`, `simplify_gpgp`, `gamma_trace`, `_simplify_single_line`, `_trace_single_line`, `_gamma_trace1`, `kahane_simplify`, `_simplify_gpgp`, `_trace_single_line1`

## Opis
Module to handle gamma matrices expressed as tensor objects.

Examples
========

>>> from sympy.physics.hep.gamma_matrices import GammaMatrix as G, LorentzIndex
>>> from sympy.tensor.tensor import tensor_indices
>>> i = tensor_indices('i', LorentzIndex)
>>> G(i)
GammaMatrix(i)

Note that there is already an instance of GammaMatrixHead in four dimensions:
GammaMatrix, which is simply declare as

>>
