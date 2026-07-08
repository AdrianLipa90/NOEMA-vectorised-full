# rv.py — .python_packages/sympy/stats/rv.py

## Tożsamość
- **id_karty:** `REPO-RV-D8B5`
- **ścieżka:** `.python_packages/sympy/stats/rv.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.748`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/stats/rv.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.748 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ORDER`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.408132`
- **R₃:** `0.527143`
- **R₆:** `0.447287`
- **R₉:** `0.516074`
- **potencjal_kappa:** `0.213299`
- **masa_semantyczna:** `0.199346`
- **rodzaj_karty:** `0.279908`


## Rola
Main Random Variables Module

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** RandomDomain, SingleDomain, MatrixDomain, ConditionalDomain, PSpace, SinglePSpace, RandomSymbol, RandomIndexedSymbol, RandomMatrixSymbol, ProductPSpace, IndependentProductPSpace, ProductDomain, Density, NamedArgsMixin, Distribution
- **funkcje:** `is_random`, `_`, `random_symbols`, `pspace`, `sumsets`, `rs_swap`, `given`, `expectation`, `probability`, `density`, `cdf`, `characteristic_function`, `moment_generating_function`, `where`, `sample`, `quantile`, `sample_iter`, `sample_iter_lambdify`, `sample_iter_subs`, `sampling_P`, `sampling_E`, `sampling_density`, `dependent`, `independent`, `pspace_independent`, `rv_subs`, `_value_check`, `_symbol_converter`, `sample_stochastic_process`, `symbols`

## Opis
Main Random Variables Module

Defines abstract random variable type.
Contains interfaces for probability space object (PSpace) as well as standard
operators, P, E, sample, density, where, quantile

See Also
========

sympy.stats.crv
sympy.stats.frv
sympy.stats.rv_interface
