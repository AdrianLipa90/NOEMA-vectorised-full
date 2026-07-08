# libhyper.py — .python_packages/mpmath/libmp/libhyper.py

## Tożsamość
- **id_karty:** `REPO-LIBHYPER-3C91`
- **ścieżka:** `.python_packages/mpmath/libmp/libhyper.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `6.223`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mpmath/libmp/libhyper.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 6.223 |
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
This module implements computation of hypergeometric and related

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** NoConvergence
- **funkcje:** `make_hyp_summator`, `mpf_erf`, `erfc_check_series`, `mpf_erfc`, `ei_taylor`, `complex_ei_taylor`, `ei_asymptotic`, `complex_ei_asymptotic`, `mpf_ei`, `mpc_ei`, `mpf_e1`, `mpc_e1`, `mpf_expint`, `mpf_ci_si_taylor`, `mpc_ci_si_taylor`, `mpf_ci_si`, `mpf_ci`, `mpf_si`, `mpc_ci`, `mpc_si`, `mpf_besseljn`, `mpc_besseljn`, `mpf_agm`, `mpf_agm1`, `mpc_agm`, `mpc_agm1`, `mpf_ellipk`, `mpc_ellipk`, `mpf_ellipe`, `mpc_ellipe`

## Opis
This module implements computation of hypergeometric and related
functions. In particular, it provides code for generic summation
of hypergeometric series. Optimized versions for various special
cases are also provided.
