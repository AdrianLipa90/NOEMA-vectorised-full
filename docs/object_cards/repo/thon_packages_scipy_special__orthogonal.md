# _orthogonal.py — .python_packages/scipy/special/_orthogonal.py

## Tożsamość
- **id_karty:** `REPO-_ORTHOGONAL-5BE3`
- **ścieżka:** `.python_packages/scipy/special/_orthogonal.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.973`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/special/_orthogonal.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.973 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ASSERTION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.563342`
- **R₃:** `0.601856`
- **R₆:** `0.54039`
- **R₉:** `0.584219`
- **potencjal_kappa:** `-0.098441`
- **masa_semantyczna:** `0.347732`
- **rodzaj_karty:** `0.261593`


## Rola
A collection of functions to find the weights and abscissas for

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** orthopoly1d
- **funkcje:** `_gen_roots_and_weights`, `roots_jacobi`, `jacobi`, `roots_sh_jacobi`, `sh_jacobi`, `roots_genlaguerre`, `genlaguerre`, `roots_laguerre`, `laguerre`, `roots_hermite`, `_compute_tauk`, `_initial_nodes_a`, `_initial_nodes_b`, `_initial_nodes`, `_pbcf`, `_newton`, `_roots_hermite_asy`, `hermite`, `roots_hermitenorm`, `hermitenorm`, `roots_gegenbauer`, `gegenbauer`, `roots_chebyt`, `chebyt`, `roots_chebyu`, `chebyu`, `roots_chebyc`, `chebyc`, `roots_chebys`, `chebys`

## Opis
A collection of functions to find the weights and abscissas for
Gaussian Quadrature.

These calculations are done by finding the eigenvalues of a
tridiagonal matrix whose entries are dependent on the coefficients
in the recursion formula for the orthogonal polynomials with the
corresponding weighting function over the interval.

Many recursion relations for orthogonal polynomials are given:

.. ma
